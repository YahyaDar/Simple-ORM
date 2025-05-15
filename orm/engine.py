from .connection import db
from typing import Type, TypeVar, List, Optional, Dict, Any

T = TypeVar("T", bound="Model")


class Model:
    table_name: str
    primary_key: str = "id"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        values = tuple(kwargs.values())
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders}) RETURNING *;"
        result = db.fetch(query, values)
        return cls(**result[0]) if result else None

    @classmethod
    def get(cls: Type[T], **conditions) -> Optional[T]:
        condition_str = " AND ".join([f"{k} = %s" for k in conditions.keys()])
        query = f"SELECT * FROM {cls.table_name} WHERE {condition_str} LIMIT 1;"
        result = db.fetch(query, tuple(conditions.values()))
        return cls(**result[0]) if result else None

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        query = f"SELECT * FROM {cls.table_name};"
        results = db.fetch(query)
        return [cls(**row) for row in results]

    def update(self, **kwargs) -> None:
        columns = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (getattr(self, self.primary_key),)
        query = f"UPDATE {self.table_name} SET {columns} WHERE {self.primary_key} = %s;"
        db.execute(query, values)

    def delete(self) -> None:
        pk_value = getattr(self, self.primary_key)
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s;"
        db.execute(query, (pk_value,))

