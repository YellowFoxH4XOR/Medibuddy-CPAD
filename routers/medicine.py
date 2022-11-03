from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import db_session
from database.models import Medicine
from routers.helper import (
    check_if_medicine_exists
)


router = APIRouter(
    prefix="/medicine",
    tags=["Medicine"],
    responses={404: {"description": "Not found"}},
)

class MedicinePayload(BaseModel):
    name: str
    quantity: int
    type: str
    details: dict
    price: int



@router.get("/allmeds", status_code=status.HTTP_200_OK)
async def find_all_meds():
    try:
        db_objs = db_session.query(Medicine).all()
        if db_objs:
            final_list = []
            all_name = []
            for obj in db_objs:
                all_name.append(obj.name)
                temp_dict = {
                                "itemId": obj.id,
                                "itemName": obj.name,
                                "storeQuantity": obj.quantity,
                                "type": obj.type,
                                "details": obj.details,
                                "price": obj.price
                }
                final_list.append(temp_dict)
            return {"result": final_list, "names": all_name}
        else:
            return {"result": []}
    except Exception:
        raise HTTPException(
                status_code=418, detail="Exception occurred while fetching details"
            )

@router.post(
    "/add",
    tags=["Medicine"],
    responses={417: {"description": "Exception Failed"}},
    status_code=status.HTTP_201_CREATED
)
async def add_medicine(data: MedicinePayload):
    med_exists = await check_if_medicine_exists(data.name)
    if(not med_exists):
        try:
            med_obj = Medicine(
                name=data.name,
                quantity=data.quantity,
                type=data.type,
                details=data.details,
                price=data.price
            )
            db_session.add(med_obj)
            db_session.commit()
            return {
                    "message": "Med added successfully",
                    "name": data.name
            }
        except Exception:
            db_session.rollback()
            raise HTTPException(
                status_code=418, detail="Exception occurred while adding Med"
            )
        
    else:
        raise HTTPException(
            status_code=409, detail="Medicine already exists please update quantity"
        )
