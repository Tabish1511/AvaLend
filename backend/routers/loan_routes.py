from fastapi import status, Depends, HTTPException, APIRouter
from database import engine
from typing import Annotated, List
from sqlalchemy.orm import Session, selectinload
from auth import get_current_user
from models import LoanApplications, LoanAnalysisResult, LoanStatus, LoanApplicationResponse, LoanAnalysisResultResponse

router = APIRouter()

def get_db():
    with Session(engine) as session:
        yield session

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# GET USER IN RESPONSE IF COOKIE IN BROWSER
@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}


# SUBMIT NEW LOAN APPLICATION WITH ANALYSIS OBJ AUTO CREATED
@router.post("/submit_application", status_code=status.HTTP_200_OK)
async def submit(user: user_dependency, db: db_dependency, loan_data: LoanApplications):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found on submission")

    # Create a new loan application
    loan_application = LoanApplications(
        user_id=user["id"],
        loan_amount=loan_data.loan_amount,
        annual_income=loan_data.annual_income,
        credit_score=loan_data.credit_score,
        employment_status=loan_data.employment_status
    )

    db.add(loan_application)
    db.commit()
    db.refresh(loan_application)

    # Create a loan analysis result with "pending" status
    loan_analysis = LoanAnalysisResult(
        loan_id=loan_application.loan_id,
        status=LoanStatus.PENDING
    )

    db.add(loan_analysis)
    db.commit()

    return {"message": "Loan application submitted successfully"}


@router.get("/get_all_applications", response_model=List[LoanApplicationResponse], status_code=status.HTTP_200_OK)
async def get_all_applications(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    applications = (
        db.query(LoanApplications)
          .filter(LoanApplications.user_id == user["id"])
          .options(selectinload(LoanApplications.loanAnalysisResult))
          .all()
    )
    
    return applications
