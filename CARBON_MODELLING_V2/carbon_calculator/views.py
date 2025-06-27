from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
import os
from django.http import HttpResponse
from .calculations import (
    calculate_fertilizer_emissions,
    calculate_livestock_emissions,
    calculate_fuel_emissions
)
from .emission_factors import FARMING_METHOD_DESCRIPTIONS, FARMING_TIPS

def get_current_season():
    """Auto-detect season for Cameroon based on current month."""
    current_month = datetime.now().month
    # Cameroon seasonal pattern: Wet season (March-October), Dry season (November-February)
    if 3 <= current_month <= 10:
        return 'rainy'
    else:
        return 'dry'

@api_view(['POST'])
def calculate_emissions(request):
    """
    Main endpoint to calculate farm emissions using original logic.
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['area_hectares', 'farming_method', 'fertilizer_level']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Missing required field: {field}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Prepare data with auto-detected season
        farm_data = {
            'area_hectares': float(data['area_hectares']),
            'farming_method': data['farming_method'],
            'fertilizer_level': data['fertilizer_level'],
            'monthly_fuel_liters': float(data.get('monthly_fuel_liters', 0)),
            'livestock': data.get('livestock', {}),
            'season': get_current_season()  # Auto-detect season
        }
        
        # Calculate emissions using original logic
        fertilizer_emissions = calculate_fertilizer_emissions(
            farm_data['area_hectares'],
            farm_data['fertilizer_level'],
            farm_data['farming_method'],
            farm_data['season']
        )
        
        livestock_emissions = calculate_livestock_emissions(
            farm_data['livestock'],
            farm_data['farming_method'],
            farm_data['season']
        )
        
        fuel_emissions = calculate_fuel_emissions(
            farm_data['monthly_fuel_liters'],
            farm_data['farming_method'],
            farm_data['season']
        )
        
        total_emissions = fertilizer_emissions + livestock_emissions + fuel_emissions
        
        # Generate recommendations
        recommendations = get_recommendations(
            farm_data, fertilizer_emissions, livestock_emissions, fuel_emissions
        )
        
        # Prepare response
        report = {
            'farm_data': farm_data,
            'emissions': {
                'fertilizer_emissions': round(fertilizer_emissions, 2),
                'livestock_emissions': round(livestock_emissions, 2),
                'fuel_emissions': round(fuel_emissions, 2),
                'total_emissions': round(total_emissions, 2)
            },
            'metrics': {
                'emissions_per_hectare': round(total_emissions / farm_data['area_hectares'], 2) if farm_data['area_hectares'] > 0 else 0,
                'carbon_intensity': get_carbon_intensity(total_emissions, farm_data['area_hectares'])
            },
            'recommendations': recommendations,
            'calculation_info': {
                'season': farm_data['season'],
                'methodology': 'Original EcosystemPlus Logic',
                'calculated_at': datetime.now().isoformat()
            }
        }
        
        return Response({
            'success': True,
            'report': report,
            'message': 'Emission report calculated successfully'
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response(
            {'error': f'Invalid data: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Internal error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def get_recommendations(farm_data, fertilizer_emissions, livestock_emissions, fuel_emissions):
    """Generate personalized recommendations."""
    recommendations = []
    total_emissions = fertilizer_emissions + livestock_emissions + fuel_emissions
    
    if total_emissions == 0:
        return ["Continue your current sustainable practices!"]
    
    # Determine which source contributes most
    fertilizer_ratio = fertilizer_emissions / total_emissions
    livestock_ratio = livestock_emissions / total_emissions
    fuel_ratio = fuel_emissions / total_emissions
    
    # Add specific recommendations based on highest emission sources
    if fertilizer_ratio > 0.4:
        recommendations.extend(FARMING_TIPS['fertilizer'][:2])
    
    if livestock_ratio > 0.4:
        recommendations.extend(FARMING_TIPS['livestock'][:2])
    
    if fuel_ratio > 0.3:
        recommendations.extend(FARMING_TIPS['fuel'][:2])
    
    # Always add some general tips
    recommendations.extend(FARMING_TIPS['general'][:2])
    
    # Add farming method specific recommendations
    farming_method = farm_data['farming_method']
    if farming_method == 'conventional':
        recommendations.append("Consider transitioning to organic or agroforestry methods to reduce emissions")
    elif farming_method in ['organic', 'agroforestry', 'permaculture']:
        recommendations.append("Great choice! Your sustainable farming method is helping reduce emissions")
    
    return recommendations[:6]

def get_carbon_intensity(total_emissions, area_hectares):
    """Calculate carbon intensity category."""
    if area_hectares == 0:
        return 'unknown'
    
    intensity = total_emissions / area_hectares
    
    if intensity < 1000:
        return 'low'
    elif intensity < 3000:
        return 'medium'
    elif intensity < 5000:
        return 'high'
    else:
        return 'very_high'

@api_view(['GET'])
def get_form_options(request):
    """
    Get all available options for the carbon calculator form.
    """
    FARMING_METHOD_CHOICES = [
        ('conventional', 'Conventional'),
        ('organic', 'Organic'),
        ('agroforestry', 'Agroforestry'),
        ('conservation', 'Conservation'),
        ('permaculture', 'Permaculture'),
    ]
    
    FERTILIZER_LEVEL_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    return Response({
        'farming_methods': [
            {'value': choice[0], 'label': choice[1], 'description': FARMING_METHOD_DESCRIPTIONS.get(choice[0], '')}
            for choice in FARMING_METHOD_CHOICES
        ],
        'fertilizer_levels': [
            {'value': choice[0], 'label': choice[1]}
            for choice in FERTILIZER_LEVEL_CHOICES
        ],
        'livestock_types': [
            'cattle', 'goat', 'sheep', 'rams', 'pigs', 'poultry'
        ],
        'current_season': get_current_season(),
        'tips': FARMING_TIPS
    })

@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'service': 'Carbon Modelling API v2.0 - Cameroon',
        'current_season': get_current_season(),
        'methodology': 'Original EcosystemPlus Logic'
    })

# Add regular Django view for serving the frontend
from django.shortcuts import render
from django.http import HttpResponse
import os

import os
from django.http import HttpResponse

def frontend_view(request):
    """
    Serve the frontend HTML page.
    """
    # Construct the path to the frontend HTML file
    frontend_path = os.path.join(os.path.dirname(__file__), '../frontend/index.html')

    try:
        with open(frontend_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return HttpResponse(html_content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('[31mFrontend file not found.[0m', status=404)
