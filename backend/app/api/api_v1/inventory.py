from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_project_manager,
    get_current_user,
    get_db_session,
)
from app.models.inventory import InventoryItem
from app.models.user import User
from app.schemas.inventory import InventoryCreate, InventoryOut, InventoryUpdate

router = APIRouter()


@router.get("/", response_model=List[InventoryOut])
def list_inventory(
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> List[InventoryOut]:
    items = db.query(InventoryItem).order_by(InventoryItem.updated_at.desc()).all()
    return [InventoryOut.from_orm(item) for item in items]


@router.post("/", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item_in: InventoryCreate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_project_manager),
) -> InventoryOut:
    item = InventoryItem(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return InventoryOut.from_orm(item)


@router.put("/{item_id}", response_model=InventoryOut)
def update_inventory_item(
    item_id: int,
    item_in: InventoryUpdate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_project_manager),
) -> InventoryOut:
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    for field, value in item_in.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return InventoryOut.from_orm(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_project_manager),
) -> None:
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    db.delete(item)
    db.commit()
