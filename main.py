from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB details
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.customer_db
customer_collection = database.get_collection("customer_info")

# Pydantic model for customer information
class CustomerInfoModel(BaseModel):
    conversation_id: str
    chat_history: str
    phone_number: str
    can_promote: str
    product_type: str
    purpose: str
    is_necessary: str
    amount: int

# Pydantic model for response
class ResponseModel(BaseModel):
    message: str
    data: CustomerInfoModel

# Initialize FastAPI app
app = FastAPI()

# Helper function to get customer info by conversation_id
async def get_customer_info_by_id(conversation_id: str):
    return await customer_collection.find_one({"conversation_id": conversation_id})

# GET endpoint to retrieve customer info
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

# POST endpoint to create new customer info
@app.post("/", response_model=ResponseModel)
async def create_customer_info(customer_info: CustomerInfoModel):
    existing_customer_info = await get_customer_info_by_id(customer_info.conversation_id)
    if existing_customer_info:
        raise HTTPException(status_code=409, detail="Customer info with this conversation ID already exists")
    
    customer_info_dict = customer_info.dict()
    await customer_collection.insert_one(customer_info_dict)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Customer info created successfully",
            "data": customer_info.dict()
        }
    )

# PUT endpoint to update existing customer info
@app.put("/", response_model=ResponseModel)
async def update_customer_info(customer_info: CustomerInfoModel):
    try:
        update_result = await customer_collection.update_one(
            {"conversation_id": customer_info.conversation_id},
            {"$set": customer_info.dict()}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Conversation ID not found")
        if update_result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the customer info")
        return JSONResponse(
            status_code=200,
            content={
                "message": "Customer info updated successfully",
                "data": customer_info.dict()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")