from datetime import date
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum

class LoanStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class Users(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    username: str
    hashed_password: str

    loanApplications: list["LoanApplications"] = Relationship(back_populates="user")

class LoanApplications(SQLModel, table=True):
    loan_id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    loan_amount: int
    annual_income: int
    credit_score: int
    employment_status: str
    application_date: date = Field(default_factory=date.today)

    user: Optional[Users] = Relationship(back_populates="loanApplications")
    loanAnalysisResult: Optional["LoanAnalysisResult"] = Relationship(back_populates="loanApplication")

class LoanAnalysisResult(SQLModel, table=True):
    loan_id: int = Field(primary_key=True, foreign_key="loanapplications.loan_id")
    status: Optional[LoanStatus]

    loanApplication: Optional[LoanApplications] = Relationship(back_populates="loanAnalysisResult")

class CreateUserRequest(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str




class LoanAnalysisResultResponse(SQLModel):
    loan_id: int
    status: Optional[LoanStatus]

    class Config:
        orm_mode = True

class LoanApplicationResponse(SQLModel):
    loan_id: int
    user_id: int
    loan_amount: int
    annual_income: int
    credit_score: int
    employment_status: str
    application_date: date
    loanAnalysisResult: Optional[LoanAnalysisResultResponse] = None

    class Config:
        orm_mode = True
