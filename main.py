import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Appointment

app = FastAPI(title="Salon API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Salon API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# Public: list services offered (static for now)
class Service(BaseModel):
    id: str
    name: str
    duration_min: int
    price: float
    description: Optional[str] = None

SERVICES: List[Service] = [
    Service(id="cut", name="Signature Haircut", duration_min=45, price=55, description="Tailored cut and style"),
    Service(id="color", name="Color & Gloss", duration_min=90, price=120, description="Customized color and shine"),
    Service(id="blowout", name="Blowout", duration_min=40, price=45, description="Smooth, voluminous finish"),
    Service(id="treatment", name="Scalp Treatment", duration_min=30, price=35, description="Relaxing scalp therapy"),
]

@app.get("/api/services", response_model=List[Service])
def list_services():
    return SERVICES

# Appointment booking endpoint (persists to MongoDB)
@app.post("/api/appointments")
def create_appointment(appointment: Appointment):
    try:
        inserted_id = create_document("appointment", appointment)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/appointments")
def get_recent_appointments(limit: int = 20):
    try:
        docs = get_documents("appointment", {}, limit)
        # sanitize ObjectId for frontend
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"ok": True, "items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
