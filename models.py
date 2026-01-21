import datetime as dt
from sqlalchemy import Integer, Float, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db

class Expense(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[dt.date] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Float)
    retailer: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    payment_method: Mapped[str] = mapped_column(String(255))