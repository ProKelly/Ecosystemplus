"""
Generate emission reports from farm data and store in PostgreSQL.
Based on the original logic from the git repository.
"""
from typing import Dict, Union
from .calculations import (
    calculate_fertilizer_emissions,
    calculate_livestock_emissions,
    calculate_fuel_emissions
)
from .models import FarmData, EmissionReport
from .emission_factors import FARMING_TIPS

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
        farm_instance = data
    else:
        data_dict = data
        farm_instance = None

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
    report_data = {
        'fertilizer_emissions': fertilizer_emissions,
        'livestock_emissions': livestock_emissions,
        'fuel_emissions': fuel_emissions,
        'total_emissions': total_emissions,
        'farming_method': data_dict['farming_method'],
        'season': data_dict['season'],
        'area_hectares': data_dict['area_hectares'],
        'emissions_per_hectare': total_emissions / data_dict['area_hectares'] if data_dict['area_hectares'] > 0 else 0,
        'recommendations': get_recommendations(data_dict, fertilizer_emissions, livestock_emissions, fuel_emissions)
    }
    
    # Store in PostgreSQL if we have a FarmData instance
    if farm_instance:
        save_report_to_database(farm_instance, report_data)
    
    return report_data

def get_recommendations(farm_data: Dict, fertilizer_emissions: float, livestock_emissions: float, fuel_emissions: float) -> list:
    """
    Generate personalized recommendations based on emission profile.
    """
    recommendations = []
    total_emissions = fertilizer_emissions + livestock_emissions + fuel_emissions
    
    # Determine which source contributes most
    if total_emissions == 0:
        return ["Continue your current sustainable practices!"]
    
    fertilizer_ratio = fertilizer_emissions / total_emissions
    livestock_ratio = livestock_emissions / total_emissions
    fuel_ratio = fuel_emissions / total_emissions
    
    # Add specific recommendations based on highest emission sources
    if fertilizer_ratio > 0.4:  # Fertilizer is major contributor
        recommendations.extend(FARMING_TIPS['fertilizer'][:2])
    
    if livestock_ratio > 0.4:  # Livestock is major contributor
        recommendations.extend(FARMING_TIPS['livestock'][:2])
    
    if fuel_ratio > 0.3:  # Fuel is significant contributor
        recommendations.extend(FARMING_TIPS['fuel'][:2])
    
    # Always add some general tips
    recommendations.extend(FARMING_TIPS['general'][:2])
    
    # Add farming method specific recommendations
    farming_method = farm_data['farming_method']
    if farming_method == 'conventional':
        recommendations.append("Consider transitioning to organic or agroforestry methods to reduce emissions")
    elif farming_method in ['organic', 'agroforestry', 'permaculture']:
        recommendations.append("Great choice! Your sustainable farming method is helping reduce emissions")
    
    return recommendations[:6]  # Limit to 6 recommendations

def save_report_to_database(farm_data: FarmData, report_data: Dict) -> EmissionReport:
    """
    Save the emission report to PostgreSQL database.
    """
    try:
        # Create and save the emission report
        emission_report = EmissionReport.objects.create(
            farm_data=farm_data,
            fertilizer_emissions=report_data['fertilizer_emissions'],
            livestock_emissions=report_data['livestock_emissions'],
            fuel_emissions=report_data['fuel_emissions'],
            total_emissions=report_data['total_emissions'],
            full_report=report_data
        )
        
        print(f"✅ Report saved to database with ID: {emission_report.id}")
        return emission_report
        
    except Exception as e:
        print(f"❌ Error saving report to database: {e}")
        return None

def get_recent_reports(limit: int = 10) -> list:
    """
    Get recent emission reports from the database.
    """
    try:
        reports = EmissionReport.objects.select_related('farm_data').order_by('-generated_at')[:limit]
        return [
            {
                'id': report.id,
                'total_emissions': report.total_emissions,
                'farm_area': report.farm_data.area_hectares,
                'farming_method': report.farm_data.farming_method,
                'season': report.farm_data.season,
                'generated_at': report.generated_at.strftime('%Y-%m-%d %H:%M'),
                'emissions_per_hectare': report.total_emissions / report.farm_data.area_hectares if report.farm_data.area_hectares > 0 else 0
            }
            for report in reports
        ]
    except Exception as e:
        print(f"❌ Error fetching reports: {e}")
        return []

def get_emission_statistics() -> Dict:
    """
    Get basic statistics from stored reports.
    """
    try:
        from django.db.models import Avg, Count, Max, Min
        
        stats = EmissionReport.objects.aggregate(
            total_reports=Count('id'),
            avg_emissions=Avg('total_emissions'),
            max_emissions=Max('total_emissions'),
            min_emissions=Min('total_emissions'),
            avg_emissions_per_hectare=Avg('total_emissions') / Avg('farm_data__area_hectares') if EmissionReport.objects.count() > 0 else 0
        )
        
        # Get distribution by farming method
        method_distribution = {}
        from django.db.models import Count
        methods = EmissionReport.objects.values('farm_data__farming_method').annotate(count=Count('id'))
        for method in methods:
            method_distribution[method['farm_data__farming_method']] = method['count']
        
        stats['farming_method_distribution'] = method_distribution
        return stats
        
    except Exception as e:
        print(f"❌ Error fetching statistics: {e}")
        return {}
