from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_admin,
    get_current_user,
    get_db_session,
)
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User, UserRole
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate

router = APIRouter()


@router.get("/", response_model=List[TicketOut])
def list_tickets(
    db: Session = Depends(get_db_session),
    project_id: Optional[int] = Query(None),
    status_filter: Optional[TicketStatus] = Query(None, alias="status"),
) -> List[TicketOut]:
    query = db.query(Ticket)
    if project_id is not None:
        query = query.filter(Ticket.project_id == project_id)
    if status_filter is not None:
        query = query.filter(Ticket.status == status_filter)
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return [TicketOut.from_orm(ticket) for ticket in tickets]


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db_session)) -> TicketOut:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    return TicketOut.from_orm(ticket)


@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> TicketOut:
    if current_user.role != UserRole.ADMIN and ticket_in.reporter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes crear tickets en nombre de otros usuarios")

    ticket = Ticket(**ticket_in.dict())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return TicketOut.from_orm(ticket)


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    ticket_in: TicketUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> TicketOut:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")

    if current_user.role not in {UserRole.ADMIN, UserRole.JEFE_PROYECTO} and current_user.id not in {ticket.reporter_id, ticket.assignee_id}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para actualizar este ticket")

    for field, value in ticket_in.dict(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return TicketOut.from_orm(ticket)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_admin),
) -> None:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    db.delete(ticket)
    db.commit()
