import hashlib
import json
import os, win32api, re, hmac
from win32com import client as cl
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from mailmerge import MailMerge
from docx2pdf import convert
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
            unc_path = f"{self.config['db']}"
            db_absolute_path = os.path.abspath(unc_path)
            print(f"sqlite:///{db_absolute_path}")
            self.engine = create_engine(f"sqlite:///{db_absolute_path}")
            self.session = sessionmaker(bind=self.engine, expire_on_commit=False)
            self.db = scoped_session(self.session)

            Base.metadata.create_all(self.engine)

        except Exception as e:
            print(e)
            raise

    def fmt_date(self, value):
        if not value:
            return ""
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.strftime("%B %d, %Y %I:%M %p")  # October 15, 2026 03:45 PM

    def fmt_money(self, value):
        return "" if value is None else f"{float(value):,.2f}"  # $1,250.00

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

    def _create_email(self, docName, data):
        outlook = cl.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = data["EmailAddress"]
        mail.Subject = "Payment Receipt"
        mail.Body = f"Thank you for you recent payment of  ${self.fmt_money(data["PaymentAmount"])}.\n\nPlease find attached your payment receipt.\n\nThank you,\nFront Desk"

        sourceFile = os.path.join(self.config["saved_receipts"], docName)
        destFile = os.path.join(self.config["saved_receipts"], docName.replace("docx", "pdf"))
        convert(sourceFile, destFile)
        mail.Attachments.Add(destFile)
        mail.Display()

        os.startfile(os.path.join(self.config["saved_receipts"], docName))

    def _generate_receipt(self, data):
        with MailMerge(self.config["receipt_template"]) as doc:

            merge_data = {k: "" if v is None else str(v) for k, v in data.to_merge().items()}
            print(merge_data)
            raw = merge_data
            merge_data["PaymentDate"] = self.fmt_date(raw["PaymentDate"])
            merge_data["PaymentAmount"] = self.fmt_money(raw["PaymentAmount"])

            doc.merge(**merge_data)
            docName = f"{merge_data["FullName"].replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.docx"
            doc.write(os.path.join(self.config["saved_receipts"], docName))


            self._create_email(docName, merge_data)

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

