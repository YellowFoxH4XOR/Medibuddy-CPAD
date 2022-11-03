from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import db_session
from typing import List, Dict
from datetime import datetime
from database.models import Order
from routers.helper import (
    update_count
)

router = APIRouter(
    prefix="/order",
    tags=["Order"],
    responses={404: {"description": "Not found"}},
)


class OrderPayload(BaseModel):
    email: str
    ordered_items:  List[Dict]


# @router.get("/allmeds", status_code=status.HTTP_200_OK)
# async def find_all_meds():
#     try:
#         db_objs = db_session.query(Medicine).all()
#         if db_objs:
#             final_list = []
#             all_name = []
#             for obj in db_objs:
#                 all_name.append(obj.name)
#                 temp_dict = {
#                                 "itemId": obj.id,
#                                 "itemName": obj.name,
#                                 "storeQuantity": obj.quantity,
#                                 "type": obj.type,
#                                 "price": obj.price
#                 }
#                 final_list.append(temp_dict)
#             return {"details": final_list, "names": all_name}
#         else:
#             return {"details": []}
#     except Exception:
#         raise HTTPException(
#                 status_code=418, detail="Exception occurred while fetching details"
#             )

@router.post(
    "/add",
    tags=["Order"],
    responses={417: {"description": "Exception Failed"}},
    status_code=status.HTTP_201_CREATED
)
async def add_order(data: OrderPayload):
    try:
        update_count(data.ordered_items)
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        ord_obj = Order(
            user_id=data.email,
            ordered_items=data.ordered_items,
            ordered_on=timestamp
        )
        db_session.add(ord_obj)
        db_session.commit()
        db_session.flush()
        return {
                "message": "Ordered successfully",
                "order_id": ord_obj.id
        }
    except Exception:
        db_session.rollback()
        raise HTTPException(
            status_code=418, detail="Exception occurred while adding Medicine"
        )