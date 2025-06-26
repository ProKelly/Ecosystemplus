from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict

from models import FarmData
from report_generator import generate_emission_report

app = FastAPI(
    title="Ecosystem Plus – Carbon Modelling API",
    description="REST API to calculate monthly farm carbon emissions based on Python logic.",
    version="1.0.0",
)

# Allow browser front-end to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)


class FarmDataInput(BaseModel):
    """Defines the structure of the incoming farm data from the front-end."""
    area_hectares: float = Field(..., gt=0, description="Total farm area in hectares")
    season: str
    farming_method: str
    fertilizer_level: str
    livestock: Dict[str, int] = Field(default_factory=dict)
    monthly_fuel_liters: float = Field(..., ge=0)

@app.post("/emissions")
def calculate_emissions(data: FarmDataInput):
    """Endpoint to calculate and return farm emissions."""
    try:
        # Convert Pydantic model to the project's FarmData dataclass
        farm_data_dict = data.dict()
        # Ensure monthly_fuel_liters is present for the dataclass
        if 'monthly_fuel_liters' not in farm_data_dict:
            farm_data_dict['monthly_fuel_liters'] = farm_data_dict.pop('fuel_liters', 0)
        
        farm = FarmData(**farm_data_dict)
        report = generate_emission_report(farm)
        return {"report": report}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}") 