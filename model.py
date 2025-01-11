from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlmodel import Field, SQLModel, Column

class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Annotated[int, Field(default=None)] = None
    updated_at: datetime = Field(sa_column=Column(sa.TIMESTAMP(timezone=True)))