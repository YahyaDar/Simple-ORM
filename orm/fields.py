class Field:
    def __init__(self, data_type: str, primary_key=False, unique=False, not_null=False, default=None, foreign_key=None):
        self.data_type = data_type
        self.primary_key = primary_key
        self.unique = unique
        self.not_null = not_null
        self.default = default
        self.foreign_key = foreign_key

    def __str__(self):
        parts = [self.data_type]

        if self.primary_key:
            parts.append("PRIMARY KEY")
        if self.unique:
            parts.append("UNIQUE")
        if self.not_null or self.primary_key:
            parts.append("NOT NULL")
        if self.default is not None:
            parts.append(f"DEFAULT '{self.default}'")
        if self.foreign_key:
            parts.append(f"REFERENCES {self.foreign_key}")

        return " ".join(parts)


# Helper classes for common types:

class Integer(Field):
    def __init__(self, auto_increment=False, **kwargs):
        data_type = "SERIAL" if auto_increment else "INTEGER"
        super().__init__(data_type, **kwargs)


class String(Field):
    def __init__(self, **kwargs):
        super().__init__("VARCHAR(255)", **kwargs)


class ForeignKey(Field):
    def __init__(self, ref_table: str, ref_column: str, **kwargs):
        foreign_key = f"{ref_table}({ref_column})"
        super().__init__("INTEGER", foreign_key=foreign_key, **kwargs)
