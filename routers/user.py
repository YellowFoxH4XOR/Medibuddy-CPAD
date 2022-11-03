from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import db_session
from database.models import User
from routers.helper import (
    check_if_user_exists, hash_pass, decode_hash_pass, find_top_transactions
)


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

class UserPayload(BaseModel):
    """User Payload for signup

    Args:
        BaseModel (_type_): pydantic
    """
    email: str
    password: str


@router.get("/login-user", status_code=status.HTTP_200_OK)
async def login_user(email, password):
    """This Route is used to get the current logged in user details

    Raises:
        HTTPException: 418 exception

    Returns:
        dict: response
    """
    try:
        db_obj = db_session.query(User).filter(User.email == email).first()
        if db_obj and password == await(decode_hash_pass(db_obj.hashed_password)):
            orders = []
            for obj in find_top_transactions(email):
                tmp_dict = {
                        "orderId": obj.id,
                        "orderStatus": obj.order_status,
                        "orderedOn": obj.ordered_on,
                        "items": obj.ordered_items
                    }
                orders.append(tmp_dict)
            response = {
                'message': "Logged in",
                'loggedIn': True,
                'email': email,
                'pastOrders': orders
            }
            return response
        else:
            return {"message": "Username or Password Wrong", 'email': email}
    except Exception:
        raise HTTPException(
                status_code=418, detail="Exception occurred while getting details"
            )

@router.post(
    "/add-user",
    tags=["User"],
    responses={417: {"description": "Exception Failed"}},
    status_code=status.HTTP_201_CREATED
)
async def add_user(data: UserPayload):
    """ User Signup
    Args:
        data (UserPayload): Payload to create new user

    Raises:
        HTTPException: 409 conflict
        HTTPException: 418 exception

    Returns:
        str: status
    """
    user_exists = await check_if_user_exists(data.email)
    if(not user_exists):
        try:
            user_obj = User(
                email=data.email,
                hashed_password=await hash_pass(data.password)
            )
            db_session.add(user_obj)
            db_session.commit()
            return {
                    "message": "User added successfully",
                    "email": data.email
            }
        except Exception:
            db_session.rollback()
            raise HTTPException(
                status_code=418, detail="Exception occurred while saving details"
            )
        
    else:
        raise HTTPException(
            status_code=409, detail="Username already taken"
        )
