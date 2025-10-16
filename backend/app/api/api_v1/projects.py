from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_admin,
    get_current_project_manager,
    get_db_session,
)
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter()


@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db_session)) -> List[ProjectOut]:
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [ProjectOut.from_orm(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db_session)) -> ProjectOut:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return ProjectOut.from_orm(project)


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db_session),
    _: None = Depends(get_current_project_manager),
) -> ProjectOut:
    project = Project(**project_in.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut.from_orm(project)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db_session),
    _: None = Depends(get_current_project_manager),
) -> ProjectOut:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut.from_orm(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db_session),
    _: None = Depends(get_current_admin),
) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    db.delete(project)
    db.commit()
