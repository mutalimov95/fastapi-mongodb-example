from mongoengine import (BooleanField, StringField)

from app.models.base import BaseModel


class User(BaseModel):
    email = StringField(required=True)
    hashed_password = StringField(required=True)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
