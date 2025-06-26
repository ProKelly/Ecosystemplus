"""
Generate emission reports from farm data.
"""
from typing import Dict, Union
from calculations import (
    calculate_fertilizer_emissions,
    calculate_livestock_emissions,
    calculate_fuel_emissions
)
from models import FarmData

def generate_emission_report(data: Union[Dict, FarmData]) -> Dict:
    """
    Generate a comprehensive emission report from farm data.
    
    Args:
        data: Union[Dict, FarmData]
    
    Returns:
        Dict containing emission breakdown and total
    """
    # Allow both dict- and dataclass-based inputs for flexibility
    if isinstance(data, FarmData):
        data_dict = data.as_dict()
    else:
        data_dict = data

    # Calculate emissions from each source
    fertilizer_emissions = calculate_fertilizer_emissions(
        data_dict['area_hectares'],
        data_dict['fertilizer_level'],
        data_dict['farming_method'],
        data_dict['season']
    )
    
    livestock_emissions = calculate_livestock_emissions(
        data_dict['livestock'],
        data_dict['farming_method'],
        data_dict['season']
    )
    
    fuel_emissions = calculate_fuel_emissions(
        data_dict['monthly_fuel_liters'],
        data_dict['farming_method'],
        data_dict['season']
    )
    
    # Calculate total emissions
    total_emissions = fertilizer_emissions + livestock_emissions + fuel_emissions
    
    # Generate report
    return {
        'fertilizer_emissions': fertilizer_emissions,
        'livestock_emissions': livestock_emissions,
        'fuel_emissions': fuel_emissions,
        'total_emissions': total_emissions,
        'farming_method': data_dict['farming_method'],
        'season': data_dict['season']
    } 