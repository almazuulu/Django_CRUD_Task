from typing import TypeVar, Generic, Type
from django.db import models
from ..repositories.base import BaseRepository

T = TypeVar('T', bound=models.Model)

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, **kwargs):
        return self.repository.create(**kwargs)

    def update(self, instance: T, **kwargs):
        return self.repository.update(instance, **kwargs)

    def delete(self, instance: T):
        self.repository.delete(instance)