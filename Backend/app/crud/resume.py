from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeResponse

class CRUDResume(CRUDBase[Resume, ResumeCreate, ResumeResponse]):
    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(Resume.owner_id == owner_id).offset(skip).limit(limit).all()

    def create_with_file(self, db: Session, *, obj_in: ResumeCreate, file_path: str, content: str, owner_id: int):
        db_obj = Resume(
            title=obj_in.title,
            file_path=file_path,
            content=content,
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

resume = CRUDResume(Resume)

