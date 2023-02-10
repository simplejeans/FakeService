from .enums import SchemaColumnTypeEnum, SchemaColumnSeparatorEnum, SchemaStringCharacterEnum

SCHEMA_COLUMN_TYPE = (
    (SchemaColumnTypeEnum.FULL_NAME.value, "Full Name"),
    (SchemaColumnTypeEnum.INTEGER.value, "Integer"),
    (SchemaColumnTypeEnum.JOB.value, "Job"),
    (SchemaColumnTypeEnum.EMAIL.value, "Email"),
    (SchemaColumnTypeEnum.PHONE_NUMBER.value, "Phone Number"),
)

SCHEMA_COLUMN_SEPARATOR = (
    (SchemaColumnSeparatorEnum.COMMA.value, "Comma (,)"),
    (SchemaColumnSeparatorEnum.DOT.value, "Dot (.)"),
)

SCHEMA_STRING_CHARACTER = (
    (SchemaStringCharacterEnum.SINGLE_QUOTE.value, "Single-quote (')"),
    (SchemaStringCharacterEnum.DOUBLE_QUOTE.value, 'Double-quote (")'),
)