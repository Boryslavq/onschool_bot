from sqlalchemy import exc

from database.db_api import db, Users, Bills
from asgiref.sync import sync_to_async


@sync_to_async
def create_user(user_id: int, username: str, fullname: str):
    user = Users(user_id=user_id, username=username, fullname=fullname)
    bill = Bills(users=user)
    try:
        db.session.add(user)
        db.session.add(bill)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()


@sync_to_async
def add_bill_id(user_id: int, bill: str):
    db.session.query(Bills).filter(Bills.user_id == user_id).update({'bill_id': bill})
    db.session.commit()


@sync_to_async
def add_info(user_id: int, full_name: str, gmail: str, phone=""):
    db.session.query(Bills).filter(Bills.user_id == user_id).update(
        {"full_name": full_name, "gmail": gmail, "phone": phone})
    db.session.commit()


@sync_to_async
def get_info(user_id: int):
    return db.session.query(Bills).filter_by(user_id=user_id).first()


@sync_to_async
def get_bill_id(user_id: int, bill: str):
    return db.session.query(Bills).filter_by(bill_id=bill).first().user_id == user_id
