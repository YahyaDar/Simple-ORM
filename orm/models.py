from orm.connection import db
from orm.fields import Field
from typing import Type, TypeVar, List, Dict, Any

T = TypeVar("T", bound="Model")


class Model:
    table_name: str
    fields: Dict[str, Field]
    primary_key: str = "id"

    def __init__(self, **kwargs):
        # Set model attributes from the provided keyword arguments
        for field_name in self.fields.keys():
            setattr(self, field_name, kwargs.get(field_name))

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    @classmethod
    def create_table(cls):
        # Generate the CREATE TABLE SQL statement
        columns = [f"{name} {str(field)}" for name, field in cls.fields.items()]
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({columns_str});"
        db.execute(query)

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        # Ensure primary key is included in the insert if required
        if cls.primary_key not in kwargs:
            raise ValueError(f"Primary key '{cls.primary_key}' is required for '{cls.__name__}' creation.")

        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        values = tuple(kwargs.values())
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders}) RETURNING *;"
        result = db.fetch(query, values)
        return cls(**result[0]) if result else None

    @classmethod
    def get(cls: Type[T], **conditions) -> T:
        # Generate the SELECT SQL statement
        condition_str = " AND ".join([f"{k} = %s" for k in conditions.keys()])
        query = f"SELECT * FROM {cls.table_name} WHERE {condition_str} LIMIT 1;"
        result = db.fetch(query, tuple(conditions.values()))
        return cls(**result[0]) if result else None

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        # Fetch all rows
        query = f"SELECT * FROM {cls.table_name};"
        results = db.fetch(query)
        return [cls(**row) for row in results]

    def update(self, **kwargs) -> None:
        # Generate the UPDATE SQL statement
        columns = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (getattr(self, self.primary_key),)
        query = f"UPDATE {self.table_name} SET {columns} WHERE {self.primary_key} = %s;"
        db.execute(query, values)

    def delete(self) -> None:
        # Generate the DELETE SQL statement
        pk_value = getattr(self, self.primary_key)
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s;"
        db.execute(query, (pk_value,))


# Singleton instance of Database
db = db
