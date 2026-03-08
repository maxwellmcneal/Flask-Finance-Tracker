import datetime as dt
from typing import Optional
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