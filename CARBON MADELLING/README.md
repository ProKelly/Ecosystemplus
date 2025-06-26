# Farm Carbon Emission Calculator

A Python-based system for calculating carbon emissions from farming activities. This tool helps farmers understand their carbon footprint and provides recommendations for reducing emissions.

## System Overview

The system consists of four main modules:

### 1. Emission Factors (`emission_factors.py`)
Contains all the constants and factors used in calculations:
- Fertilizer emission levels (none, low, medium, high)
- Livestock emission factors per animal type
- Fuel emission factor (2.68 kg CO₂e per liter)
- Farming method multipliers (conventional, organic, agroforestry, conservation, permaculture)
- Seasonal variations (dry and rainy seasons)
- Farming tips and recommendations

### 2. Calculations (`calculations.py`)
Core calculation functions:
- `calculate_fertilizer_emissions`: Computes emissions from fertilizer use
- `calculate_livestock_emissions`: Computes emissions from livestock
- `calculate_fuel_emissions`: Computes emissions from fuel consumption

Each calculation takes into account:
- Farm area
- Farming method (emission reduction factor)
- Current season (seasonal adjustment factors)

### 3. Report Generator (`report_generator.py`)
Generates comprehensive emission reports by:
- Collecting data from all emission sources
- Calculating total emissions
- Organizing data for display

### 4. Main Program (`main.py`)
User interface and data collection:
- Interactive prompts for farm data
- Input validation
- Formatted report display
- Seasonal and source-specific recommendations

## Calculation Logic

### Fertilizer Emissions
```
Base emissions = Area × Fertilizer level factor
Seasonal adjustment = Base emissions × Season factor
Final emissions = Seasonal adjustment × Farming method factor
```

### Livestock Emissions
```
Base emissions = Sum of (Animal count × Animal emission factor)
Seasonal adjustment = Base emissions × Season factor
Final emissions = Seasonal adjustment × Farming method factor
```

### Fuel Emissions
```
Base emissions = Fuel liters × Fuel emission factor
Seasonal adjustment = Base emissions × Season factor
Final emissions = Seasonal adjustment × Farming method factor
```

## Farming Methods and Their Impact

Each farming method has a different emission reduction factor:
- Conventional: 1.0 (baseline)
- Organic: 0.7 (30% reduction)
- Agroforestry: 0.8 (20% reduction)
- Conservation: 0.85 (15% reduction)
- Permaculture: 0.75 (25% reduction)

## Seasonal Variations

The system accounts for seasonal differences:

### Dry Season
- Fertilizer: 20% higher emissions
- Livestock: 10% higher emissions
- Fuel: No change

### Rainy Season
- Fertilizer: 20% lower emissions
- Livestock: 10% lower emissions
- Fuel: 20% higher emissions

## Usage

1. Run the program:
```bash
python main.py
```

2. Follow the prompts to enter:
   - Farm area (in hectares)
   - Current season
   - Farming method
   - Fertilizer usage level
   - Livestock counts (if any)
   - Fuel usage (if any)

3. The system will generate a report showing:
   - Monthly emissions from each source
   - Total emissions
   - Farming method impact
   - Season-specific recommendations
   - Source-specific tips

## Output Format

Emissions are displayed in:
- Kilograms of CO₂e (carbon dioxide equivalent)
- Tonnes of CO₂e (for values ≥ 1000 kg)

## Recommendations

The system provides three types of recommendations:
1. Season-specific tips
2. Source-specific tips (based on highest emission source)
3. General farming tips

## Dependencies

- Python 3.6 or higher
- No external libraries required

## Future Improvements

Potential areas for enhancement:
1. Add more detailed seasonal variations
2. Include more farming methods
3. Add support for different regions
4. Implement data export functionality
5. Add historical data tracking 