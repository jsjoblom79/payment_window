import os, win32api

from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.testing.pickleable import User

from assets.data.payment import Base, Payment


class DataAPI:
    def __init__(self):
        try:
            self.engine = create_engine("sqlite:///payments.db")
            self.session = sessionmaker(bind=self.engine, expire_on_commit=False)
            self.db = scoped_session(self.session)

            Base.metadata.create_all(self.engine)

        except Exception as e:
            print(e)
            raise

    def get_payment_fields(self):
        return [
            'id',
            'ssn_hash',
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
        print(user)
        print(name)
        return {
            "user": user,
            "name": name
        }