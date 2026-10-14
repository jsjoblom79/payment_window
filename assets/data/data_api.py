import hashlib
import json
import os, win32api, re, hmac
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from mailmerge import MailMerge

from assets.data.payment import Base, Payment



def parse_date(value):
    """Convert 'YYYY-MM-DD' to a date object, or None if empty."""
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()

class DataAPI:
    def __init__(self):
        with open("assets/config.json", "r") as f:
            self.config = json.load(f)

        try:
            self.engine = create_engine("sqlite:///payments.db")
            self.session = sessionmaker(bind=self.engine, expire_on_commit=False)
            self.db = scoped_session(self.session)

            Base.metadata.create_all(self.engine)

        except Exception as e:
            print(e)
            raise

    def _hash_ssn(self, ssn):
        key = "PayWin26"
        if not key:
            raise ValueError("HASH KEY not set")
        digits = re.sub(r"\D", "", ssn or "")
        if len(digits) != 9:
            raise ValueError("SSN Must be 9 digits")
        return hmac.new(key.encode(), digestmod=hashlib.sha256).hexdigest()
    def get_payment_fields(self):
        return [
            'id',
            'last_four',
            'payment_date',
            'payment_amount',
            # 'cash_amount',
            # 'check_amount','credit_amount','void','posted','check_number','payment_method',
            # 'change_due','comments',
            'receipt_emailed_date'
        ]

    def get_all_payments(self):
        stmt = select(Payment)
        all_payments = self.db.scalars(stmt).all()
        return [payment.to_dict() for payment in all_payments]

    def get_current_user(self):
        user = os.getenv("USERNAME")
        name = win32api.GetUserNameEx(3)
        return {
            "user": user,
            "name": name
        }

    def _generate_receipt(self, data):
        with MailMerge(self.config["receipt_template"]) as doc:
            print(doc.get_merge_fields())
            print(data.to_merge().keys())
            merge_data = {k: "" if v is None else str(v) for k, v in data.to_merge().items()}
            doc.merge(**merge_data)
            doc.write(f"new_test.docx")

    def make_payment(self, data):
        print(data)
        data["payment_date"] = datetime.now()
        data["ssn_hash"] = self._hash_ssn(data.get("ssn_hash"))

        if data["receipt_emailed_date"] is not None and data["receipt_emailed_date"] != '':
            data["receipt_emailed_date"] = parse_date(data["receipt_emailed_date"])
        else:
            data["receipt_emailed_date"] = None
        new_payment = Payment(**data)
        try:
            self.db.add(new_payment)
            self.db.commit()
            self.db.refresh(new_payment)
            self._generate_receipt(new_payment)
        except SQLAlchemyError as e:
            self.db.rollback()
            print(e)

