"""
Constants for emission factors used in carbon footprint calculations.
Based on the original logic from the git repository.
"""

# Monthly fertilizer emission factors (kg CO₂e/ha/month)
FERTILIZER_LEVELS = {
    'none': 0,      # No synthetic fertilizer
    'low': 36,      # 0-50 kg/ha/year
    'medium': 66,   # 51-100 kg/ha/year
    'high': 110     # >100 kg/ha/year
}

# Monthly CO₂e emissions per animal (kg CO₂e/month)
LIVESTOCK_EMISSIONS = {
    'cattle': 2200/12,  # 2200 kg/year
    'goat': 144/12,     # 144 kg/year
    'sheep': 160/12,    # 160 kg/year
    'rams': 160/12,     # 160 kg/year
    'pigs': 350/12,     # 350 kg/year
    'poultry': 10/12    # 10 kg/year
}

# Fuel emission factor (kg CO₂e per liter)
FUEL_EMISSION_FACTOR = 2.68

# Fertilizer emission factor (kg CO₂e per kg of fertilizer)
FERTILIZER_EMISSION_FACTOR = 1.3

# Farming method emission factors (multipliers)
FARMING_METHODS = {
    'conventional': 1.0,    # Base multiplier
    'organic': 0.7,        # 30% reduction
    'agroforestry': 0.8,   # 20% reduction
    'conservation': 0.85,  # 15% reduction
    'permaculture': 0.75   # 25% reduction
}

# Farming method descriptions in simple language
FARMING_METHOD_DESCRIPTIONS = {
    'conventional': "You use regular tilling and chemical fertilizers (like NPK or urea)",
    'organic': "You use traditional methods like compost, animal manure, and natural pest control",
    'agroforestry': "You grow trees or use alley cropping",
    'conservation': "You practice minimum tillage and use cover crops",
    'permaculture': "You farm in a way that mimics natural ecosystems, using local resources efficiently"
}

# Seasonal variations
SEASONS = {
    'dry': {
        'fertilizer_factor': 1.2,    # 20% higher emissions due to increased need
        'livestock_factor': 1.1,     # 10% higher due to feed supplements
        'fuel_factor': 1.0          # No change
    },
    'rainy': {
        'fertilizer_factor': 0.8,    # 20% lower due to natural nutrient cycling
        'livestock_factor': 0.9,     # 10% lower due to better grazing
        'fuel_factor': 1.2          # 20% higher due to wet conditions
    }
}

# Farming tips
FARMING_TIPS = {
    'fertilizer': [
        "Use local compost made from kitchen waste and residues",
        "Consider using cover crops to fix nitrogen",
        "Apply fertilizer during the early rainy season for better absorption"
    ],
    'livestock': [
        "Practice rotational grazing to prevent overgrazing",
        "Use local feed resources like residues",
        "Consider integrating livestock with farming (mixed farming)"
    ],
    'fuel': [
        "Use manual tools where possible to reduce fuel costs",
        "Maintain equipment regularly to improve fuel efficiency",
        "Consider using solar-powered irrigation systems"
    ],
    'general': [
        "Plant trees around your farm to provide shade and reduce soil erosion",
        "Use rotation to maintain soil fertility",
        "Consider drought-resistant varieties during dry seasons",
        "Practice water conservation techniques like mulching",
        "Use local varieties adapted to your climate"
    ]
}
