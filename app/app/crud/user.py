from typing import Optional

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_by_email(*, email: str) -> Optional[User]:
        try:
            return User.objects(email=email).get()
        except User.DoesNotExist:
            return

    def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
        ).save()
        return db_obj

    def update(self, *, db_obj: User, obj_in: UserUpdate) -> User:
        use_obj_in = obj_in
        if obj_in.password:
            update_data = obj_in.dict(exclude_unset=True)
            hashed_password = get_password_hash(obj_in.password)
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            use_obj_in = UserInDB.parse_obj(update_data)
        return super().update(db_obj=db_obj, obj_in=use_obj_in)

    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
