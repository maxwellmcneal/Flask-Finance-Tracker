import datetime as dt
from typing import Optional, List
from sqlalchemy import Integer, Float, Boolean, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db


class Account(db.Model):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(50))
    institution: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_four: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    starting_balance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ExpenseCategory(db.Model):
    __tablename__ = "expense_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


class Expense(db.Model):
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[dt.date] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Float)
    retailer: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("expense_categories.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    reconciled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    category: Mapped["ExpenseCategory"] = relationship()
    account: Mapped["Account"] = relationship()
    reimbursements: Mapped[List["Reimbursement"]] = relationship(back_populates="expense", cascade="all, delete")

    @property
    def net_amount(self):
        return self.amount - sum(r.amount for r in self.reimbursements)

class IncomeCategory(db.Model):
    __tablename__ = "income_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    
class Income(db.Model):
    __tablename__ = "income"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[dt.date] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("income_categories.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    reconciled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    category: Mapped["IncomeCategory"] = relationship()
    account: Mapped["Account"] = relationship()
    allocations: Mapped[List["IncomeAllocation"]] = relationship(back_populates="income", cascade="all, delete-orphan")
    reimbursements: Mapped[List["Reimbursement"]] = relationship(back_populates="income", cascade="all, delete-orphan")


class IncomeAllocation(db.Model):
    __tablename__ = "income_allocations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    income_id: Mapped[int] = mapped_column(ForeignKey("income.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[float] = mapped_column(Float)

    # Relationships
    income: Mapped["Income"] = relationship(back_populates="allocations")
    account: Mapped["Account"] = relationship()


class Transfer(db.Model):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[dt.date] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Float)
    from_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reconciled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    from_account: Mapped["Account"] = relationship(foreign_keys=[from_account_id])
    to_account: Mapped["Account"] = relationship(foreign_keys=[to_account_id])


class Reimbursement(db.Model):
    __tablename__ = "reimbursements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    income_id: Mapped[int] = mapped_column(ForeignKey("income.id"))
    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"))
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[dt.date] = mapped_column(Date)

    # Relationships
    income: Mapped["Income"] = relationship(back_populates="reimbursements")
    expense: Mapped["Expense"] = relationship(back_populates="reimbursements")