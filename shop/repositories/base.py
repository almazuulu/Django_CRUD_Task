from typing import TypeVar, Generic, Type
from django.db import models
from django.db.models.query import QuerySet

T = TypeVar('T', bound=models.Model)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_all(self) -> QuerySet[T]:
        return self.model_class.objects.all()

    def get_by_id(self, id: int) -> T:
        return self.model_class.objects.get(id=id)

    def create(self, **kwargs) -> T:
        instance = self.model_class(**kwargs)
        instance.save()
        return instance

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()

    def filter(self, **kwargs) -> QuerySet[T]:
        return self.model_class.objects.filter(**kwargs)