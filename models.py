import datetime as dt
from sqlalchemy import Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db

class Expense(db.Model):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[dt.date] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Float)
    retailer: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("expense_categories.id"))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"))
    
    # Relationships
    category: Mapped["ExpenseCategory"] = relationship()
    payment_method: Mapped["PaymentMethod"] = relationship()
    
class ExpenseCategory(db.Model):
    __tablename__ = "expense_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    
class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))