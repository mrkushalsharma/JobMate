from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.match import MatchScore
from app.schemas.match import MatchScoreResponse

class CRUDMatchScore(CRUDBase[MatchScore, MatchScoreResponse, MatchScoreResponse]):
    def get_by_job_resume(self, db: Session, *, job_id: int, resume_id: int):
        return db.query(self.model).filter(
            MatchScore.job_id == job_id,
            MatchScore.resume_id == resume_id
        ).first()

    def get_by_job(self, db: Session, *, job_id: int):
        return db.query(self.model).filter(MatchScore.job_id == job_id).all()

    def create_score(self, db: Session, *, job_id: int, resume_id: int, score: float):
        db_obj = MatchScore(
            job_id=job_id,
            resume_id=resume_id,
            score=score
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

match_score = CRUDMatchScore(MatchScore)

