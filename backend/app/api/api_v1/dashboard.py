from collections import Counter
from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.models.inventory import InventoryItem
from app.models.project import Project
from app.models.ticket import Ticket
from app.models.user import User
from app.models.wiki import WikiPage

router = APIRouter()


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> Dict[str, Dict[str, int]]:
    projects_count = db.query(Project).count()
    tickets_count = db.query(Ticket).count()
    users_count = db.query(User).count()
    inventory_count = db.query(InventoryItem).count()
    wikis_count = db.query(WikiPage).count()

    status_counts = Counter(
        status for (status,) in db.query(Ticket.status).all()
    )

    return {
        "totals": {
            "projects": projects_count,
            "tickets": tickets_count,
            "users": users_count,
            "inventory": inventory_count,
            "wikis": wikis_count,
        },
        "tickets_by_status": {status.value: count for status, count in status_counts.items()},
    }
