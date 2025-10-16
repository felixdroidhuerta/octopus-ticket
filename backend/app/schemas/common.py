from datetime import datetime


class ORMBase:
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TimestampMixin:
    created_at: datetime
    updated_at: datetime
