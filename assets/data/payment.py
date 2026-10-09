from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # HMAC-SHA256 hex digest of the SSN (never the raw SSN). See crud.hash_ssn().
    ssn_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    payment_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    cash_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    check_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    credit_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )

    void: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    posted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    check_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)

    payment_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    change_due: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )

    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    receipt_emailed_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    def __repr__(self) -> str:
        return (
            f"<Payment id={self.id} date={self.payment_date} "
            f"amount={self.payment_amount} void={self.void} posted={self.posted}>"
        )
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ssn_hash": self.ssn_hash,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "payment_amount": float(self.payment_amount) if self.payment_amount is not None else 0.0,
            # "check_amount": float(self.check_amount) if self.check_amount is not None else 0.0,
            # "credit_amount": float(self.credit_amount) if self.credit_amount is not None else 0.0,
            # "check_number": self.check_number,
            # "payment_method": self.payment_method,
            # "void": self.void,
            # "posted": self.posted,
            # "change_due": float(self.change_due) if self.change_due is not None else 0.0,
            # "comments": self.comments,
            "receipt_emailed_date": self.receipt_emailed_date.isoformat() if self.receipt_emailed_date else None,
        }
