from enum import Enum


class SchemaColumnTypeEnum(Enum):
    FULL_NAME = "full_name"
    INTEGER = "integer"
    JOB = "job"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"


class SchemaColumnSeparatorEnum(Enum):
    COMMA = ","
    DOT = "."


class SchemaStringCharacterEnum(Enum):
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'