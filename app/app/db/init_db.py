from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate


def init_db():
    user = crud.user.get_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(obj_in=user_in)  # noqa: F841
