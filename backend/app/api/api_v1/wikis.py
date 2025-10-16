from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_project_manager,
    get_current_user,
    get_db_session,
)
from app.models.user import User, UserRole
from app.models.wiki import WikiPage
from app.schemas.wiki import WikiCreate, WikiOut, WikiUpdate

router = APIRouter()


@router.get("/", response_model=List[WikiOut])
def list_wikis(
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> List[WikiOut]:
    wikis = db.query(WikiPage).order_by(WikiPage.updated_at.desc()).all()
    return [WikiOut.from_orm(wiki) for wiki in wikis]


@router.post("/", response_model=WikiOut, status_code=status.HTTP_201_CREATED)
def create_wiki(
    wiki_in: WikiCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> WikiOut:
    if current_user.role == UserRole.VISUALIZADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para crear wikis")
    wiki = WikiPage(**wiki_in.dict())
    db.add(wiki)
    db.commit()
    db.refresh(wiki)
    return WikiOut.from_orm(wiki)


@router.put("/{wiki_id}", response_model=WikiOut)
def update_wiki(
    wiki_id: int,
    wiki_in: WikiUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> WikiOut:
    wiki = db.query(WikiPage).filter(WikiPage.id == wiki_id).first()
    if not wiki:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki no encontrada")
    if current_user.role == UserRole.VISUALIZADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para editar wikis")

    for field, value in wiki_in.dict(exclude_unset=True).items():
        setattr(wiki, field, value)
    db.add(wiki)
    db.commit()
    db.refresh(wiki)
    return WikiOut.from_orm(wiki)


@router.delete("/{wiki_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wiki(
    wiki_id: int,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_project_manager),
) -> None:
    wiki = db.query(WikiPage).filter(WikiPage.id == wiki_id).first()
    if not wiki:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki no encontrada")
    db.delete(wiki)
    db.commit()
