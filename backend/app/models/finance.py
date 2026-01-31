from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    revenue = Column(Float)
    expense_category = Column(String)
    expense_amount = Column(Float)
    receivable = Column(Float)
    payable = Column(Float)
    inventory = Column(Float)
    loan_emi = Column(Float)
    gst_paid = Column(Float)
    gst_due = Column(Float)
