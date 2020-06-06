from typing import Union

from mongoengine.fields import ObjectId
from pydantic import BaseModel, validator


class InDBBase(BaseModel):
    id: str = None

    @validator("id", pre=True)
    def _objectid_to_str(cls, value: Union[ObjectId, str]) -> str:
        if isinstance(value, ObjectId):  # here value is ObjectId
            return str(value)
        return value

    class Config:
        orm_mode = True
