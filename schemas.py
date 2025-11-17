"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Hair salon specific schemas
class Appointment(BaseModel):
    """
    Appointments collection schema
    Collection name: "appointment"
    """
    client_name: str = Field(..., min_length=2, description="Client full name")
    email: EmailStr = Field(..., description="Client email")
    phone: str = Field(..., min_length=7, description="Client phone number")
    service: str = Field(..., description="Requested service")
    stylist: Optional[str] = Field(None, description="Preferred stylist")
    date: str = Field(..., description="Requested date (YYYY-MM-DD)")
    time: str = Field(..., description="Requested time (HH:MM)")
    notes: Optional[str] = Field(None, description="Additional notes")
    status: str = Field("pending", description="Status of appointment")
    source: str = Field("web", description="Where the booking came from")
    created_on: Optional[datetime] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
