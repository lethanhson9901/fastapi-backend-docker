from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.customer_db
customer_collection = database.get_collection("customer_info")

class CustomerInfoModel(BaseModel):
    conversation_id: str
    chat_history: str
    phone_number: str
    can_promote: str
    product_type: str
    purpose: str
    is_necessary: str
    amount: int

class ResponseModel(BaseModel):
    message: str
    data: CustomerInfoModel

app = FastAPI()

async def get_customer_info_by_id(conversation_id: str):
    return await customer_collection.find_one({"conversation_id": conversation_id})

@app.get("/info/{conversation_id}", response_model=CustomerInfoModel)
async def get_customer_info(conversation_id: str):
    customer_info = await get_customer_info_by_id(conversation_id)
    if customer_info:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Customer info retrieved successfully",
                "data": CustomerInfoModel(**customer_info).dict()
            }
        )
    else:
        raise HTTPException(status_code=404, detail="Conversation ID not found")

@app.post("/", response_model=ResponseModel)
async def create_customer_info(customer_info: CustomerInfoModel):
    customer_info_dict = customer_info.dict()
    await customer_collection.insert_one(customer_info_dict)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Customer info created successfully",
            "data": customer_info.dict()
        }
    )

@app.put("/", response_model=ResponseModel)
async def update_customer_info(customer_info: CustomerInfoModel):
    update_result = await customer_collection.update_one(
        {"conversation_id": customer_info.conversation_id},
        {"$set": customer_info.dict()}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversation ID not found")
    return JSONResponse(
        status_code=200,
        content={
            "message": "Customer info updated successfully",
            "data": customer_info.dict()
        }
    )
