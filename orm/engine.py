from .connection import db
from .fields import Field
from typing import Type, TypeVar, List, Dict, Any

T = TypeVar("T", bound="Model")


class Model:
    table_name: str
    fields: Dict[str, Field]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_table(cls):
        columns = [f"{name} {str(field)}" for name, field in cls.fields.items()]
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({columns_str});"
        db.execute(query)

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        # Exclude primary key from insert if not in kwargs
        if cls.primary_key in cls.fields and cls.primary_key not in kwargs:
            insert_keys = [k for k in kwargs.keys()]
        else:
            insert_keys = list(kwargs.keys())

        columns = ", ".join(insert_keys)
        placeholders = ", ".join(["%s"] * len(insert_keys))
        values = tuple(kwargs[k] for k in insert_keys)
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders}) RETURNING *;"
        result = db.fetch(query, values)
        return cls(**result[0]) if result else None


    @classmethod
    def get(cls: Type[T], **conditions) -> T:
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
        pk_name = self.__class__.primary_key
        pk_value = getattr(self, pk_name)
        values = tuple(kwargs.values()) + (pk_value,)
        query = f"UPDATE {self.table_name} SET {columns} WHERE {pk_name} = %s;"
        db.execute(query, values)

    def delete(self) -> None:
        pk_name = self.__class__.primary_key
        pk_value = getattr(self, pk_name)
        query = f"DELETE FROM {self.table_name} WHERE {pk_name} = %s;"
        db.execute(query, (pk_value,))


# Singleton instance of Database
db = db
