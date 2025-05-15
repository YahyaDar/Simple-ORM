from orm.engine import Model
from orm.fields import Integer, String, ForeignKey


class University(Model):
    table_name = "university"
    primary_key = "id"
    fields = {
        "id": Integer(primary_key=True, auto_increment=True),
        "name": String(unique=True, not_null=True),
        "location": String(),
        "established_year": Integer(),
    }


class Course(Model):
    table_name = "courses"
    primary_key = "id"
    fields = {
        "id": Integer(primary_key=True, auto_increment=True),
        "name": String(unique=True, not_null=True),
        "credits": Integer(),
        "university_id": ForeignKey("university", "id"),
    }


class Teacher(Model):
    table_name = "teachers"
    primary_key = "id"
    fields = {
        "id": Integer(primary_key=True, auto_increment=True),
        "name": String(not_null=True),
        "email": String(unique=True, not_null=True),
        "university_id": ForeignKey("university", "id"),
    }


class Student(Model):
    table_name = "students"
    primary_key = "reg"
    fields = {
        "reg": String(primary_key=True),
        "name": String(not_null=True),
        "email": String(unique=True, not_null=True),
        "university_id": ForeignKey("university", "id"),
    }
