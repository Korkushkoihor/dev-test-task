from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import AdminOrManager, SessionDep
from app.models import MetricsPublic, User

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/", response_model=MetricsPublic)
def read_metrics(session: SessionDep, _: AdminOrManager) -> MetricsPublic:
    user_count = session.exec(select(func.count()).select_from(User)).one()
    active_user_count = session.exec(
        select(func.count()).select_from(User).where(User.is_active.is_(True))
    ).one()
    return MetricsPublic(user_count=user_count, active_user_count=active_user_count)
