from typing import Generic, Iterator, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from mongoengine import DoesNotExist
from pydantic import BaseModel

from app.models.base import BaseModel as BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A Mongodb Document model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, id: str) -> Optional[ModelType]:
        try:
            return self.model.objects(id=id).get()
        except DoesNotExist:
            return None

    def get_multi(self, *, skip=0, limit=100) -> Iterator[ModelType]:
        return iter(self.model.objects[skip:limit])

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data).save()
        return db_obj

    def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = db_obj.to_mongo()
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.save()
        return db_obj

    def remove(self, *, id_: str) -> ModelType:
        obj = self.get(id_)
        if obj:
            obj.delete()
        return obj
