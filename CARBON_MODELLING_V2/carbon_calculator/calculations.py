"""
Core calculation functions for carbon emission estimates.
Based on the original logic from the git repository.
"""
from typing import Dict
from .emission_factors import (
    FERTILIZER_LEVELS,
    FERTILIZER_EMISSION_FACTOR,
    LIVESTOCK_EMISSIONS,
    FUEL_EMISSION_FACTOR,
    FARMING_METHODS,
    SEASONS
)

def calculate_fertilizer_emissions(area_hectares: float, level: str, farming_method: str, season: str) -> float:
    """
    Calculate CO₂e emissions from fertilizer application.
    
    Args:
        area_hectares: Farm area in hectares
        level: Fertilizer application level ('none', 'low', 'medium', 'high')
        farming_method: Farming method to apply emission reduction factor
        season: Current season ('dry' or 'rainy')
    
    Returns:
        float: Monthly CO₂e emissions from fertilizer in kg
    """
    if level not in FERTILIZER_LEVELS:
        raise ValueError(f"Invalid fertilizer level. Must be one of {list(FERTILIZER_LEVELS.keys())}")
    
    if farming_method not in FARMING_METHODS:
        raise ValueError(f"Invalid farming method. Must be one of {list(FARMING_METHODS.keys())}")
    
    if season not in SEASONS:
        raise ValueError(f"Invalid season. Must be one of {list(SEASONS.keys())}")
    
    # Calculate base emissions
    fertilizer_amount = FERTILIZER_LEVELS[level] * area_hectares
    
    # Calculate total emissions with all factors
    base_emissions = fertilizer_amount * FERTILIZER_EMISSION_FACTOR
    seasonal_emissions = base_emissions * SEASONS[season]['fertilizer_factor']
    return seasonal_emissions * FARMING_METHODS[farming_method]

def calculate_livestock_emissions(livestock_dict: Dict[str, int], farming_method: str, season: str) -> float:
    """
    Calculate CO₂e emissions from livestock.
    
    Args:
        livestock_dict: Dictionary with animal types as keys and counts as values
        farming_method: Farming method to apply emission reduction factor
        season: Current season ('dry' or 'rainy')
    
    Returns:
        float: Monthly CO₂e emissions from livestock in kg
    """
    if farming_method not in FARMING_METHODS:
        raise ValueError(f"Invalid farming method. Must be one of {list(FARMING_METHODS.keys())}")
    
    if season not in SEASONS:
        raise ValueError(f"Invalid season. Must be one of {list(SEASONS.keys())}")
    
    total_emissions = 0.0
    for animal_type, count in livestock_dict.items():
        if animal_type not in LIVESTOCK_EMISSIONS:
            raise ValueError(f"Invalid animal type: {animal_type}")
        total_emissions += count * LIVESTOCK_EMISSIONS[animal_type]
    
    # Apply seasonal and farming method factors
    seasonal_emissions = total_emissions * SEASONS[season]['livestock_factor']
    return seasonal_emissions * FARMING_METHODS[farming_method]

def calculate_fuel_emissions(monthly_liters: float, farming_method: str, season: str) -> float:
    """
    Calculate CO₂e emissions from fuel consumption.
    
    Args:
        monthly_liters: Average monthly fuel consumption in liters
        farming_method: Farming method to apply emission reduction factor
        season: Current season ('dry' or 'rainy')
    
    Returns:
        float: Monthly CO₂e emissions from fuel in kg
    """
    if farming_method not in FARMING_METHODS:
        raise ValueError(f"Invalid farming method. Must be one of {list(FARMING_METHODS.keys())}")
    
    if season not in SEASONS:
        raise ValueError(f"Invalid season. Must be one of {list(SEASONS.keys())}")
    
    # Calculate base emissions
    base_emissions = monthly_liters * FUEL_EMISSION_FACTOR
    
    # Apply seasonal and farming method factors
    seasonal_emissions = base_emissions * SEASONS[season]['fuel_factor']
    return seasonal_emissions * FARMING_METHODS[farming_method]
