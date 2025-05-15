from typing import Dict, Any, List, Tuple


class QueryBuilder:
    @staticmethod
    def select(table: str, conditions: Dict[str, Any] = None, limit: int = None) -> Tuple[str, Tuple]:
        query = f"SELECT * FROM {table}"
        params = ()

        if conditions:
            condition_str = " AND ".join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {condition_str}"
            params = tuple(conditions.values())

        if limit:
            query += f" LIMIT {limit}"

        query += ";"
        return query, params

    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> Tuple[str, Tuple]:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *;"
        return query, tuple(data.values())

    @staticmethod
    def update(table: str, data: Dict[str, Any], primary_key: str, pk_value: Any) -> Tuple[str, Tuple]:
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {columns} WHERE {primary_key} = %s;"
        return query, tuple(data.values()) + (pk_value,)

    @staticmethod
    def delete(table: str, primary_key: str, pk_value: Any) -> Tuple[str, Tuple]:
        query = f"DELETE FROM {table} WHERE {primary_key} = %s;"
        return query, (pk_value,)

