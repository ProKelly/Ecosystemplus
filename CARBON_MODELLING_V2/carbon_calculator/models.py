from django.db import models

# Keeping models minimal since we're not using database storage
# These are just for reference and potential future use

# Data structures used in the application:
# 
# FarmData dict structure:
# {
#     'area_hectares': float,
#     'season': str ('dry' or 'rainy'),  # Auto-detected
#     'farming_method': str ('conventional', 'organic', 'agroforestry', 'conservation', 'permaculture'),
#     'fertilizer_level': str ('none', 'low', 'medium', 'high'),
#     'livestock': dict,  # {'cattle': 5, 'goat': 10, ...}
#     'monthly_fuel_liters': float
# }
#
# EmissionReport dict structure:
# {
#     'farm_data': dict,
#     'emissions': {
#         'fertilizer_emissions': float,
#         'livestock_emissions': float,
#         'fuel_emissions': float,
#         'total_emissions': float
#     },
#     'metrics': {
#         'emissions_per_hectare': float,
#         'carbon_intensity': str
#     },
#     'recommendations': list,
#     'calculation_info': dict
# }
