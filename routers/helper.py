from conf import PASS_SALT
from database import db_session
from database.models import User, Medicine, Order
from sqlalchemy import desc


async def check_if_user_exists(username: str) -> bool:
    db_obj = db_session.query(User).filter(User.email == username).all()
    if(not db_obj):
        return False
    return True


async def check_if_medicine_exists(name: str) -> bool:
    db_obj = db_session.query(Medicine).filter(Medicine.name == name).all()
    if(not db_obj):
        return False
    return True

async def hash_pass(password: str) -> str:
    return PASS_SALT + password

async def decode_hash_pass(password: str) -> str:
    return ''.join(password.split(sep='---')[1:])


def update_medicine(id, quant):
    db_obj = db_session.query(Medicine).filter(Medicine.id == id).first()
    db_obj.quantity = db_obj.quantity - quant
    db_session.commit()


def update_count(items):
    for item in items:
        update_medicine(item.get('itemId'), item.get('quantity'))
    return True


def find_top_transactions(email):
    db_obj = db_session.query(Order).filter(Order.user_id == email).order_by(desc(Order.ordered_on)).limit(3).all()
    return db_obj