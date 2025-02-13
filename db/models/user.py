from db.models.tablemodel import TableModel
from sqlmodel import Field
from datetime import datetime,timezone

class User(TableModel, table=True):
    __tablename__='Users'
    username:str = Field(nullable=False)
    email:str = Field(nullable=False, unique=True, index=True)
    password:str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    role: str = Field(nullable=False, max_length=10, index=True)
    otp:str = Field(nullable=True)
    otp_created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    email_verification:bool = Field(default=False)
    
