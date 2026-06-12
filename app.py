import sys

# --- Contextual Constants & Baselines ---
GRID_INTENSITY = {
    "coal-heavy": 0.9,     # High carbon intensity grid (kg CO2e/kWh)
    "mixed": 0.45,         # Average grid mix
    "renewable-dominant": 0.1 # Low carbon intensity grid
}

TRANSPORT_FACTORS = {
    "petrol_car": 0.170,   # per km
    "diesel_car": 0.171,   # per km
    "electric_vehicle": 0.045, # per km (indirect grid emissions)
    "public_transit": 0.035,   # per km
    "bicycle_walk": 0.000  
}

DIET_FACTORS = {
    "heavy_meat": 2.90,    # per day
    "low_meat": 1.70,     # per day
    "vegetarian": 1.20,    # per day
    "vegan": 0.90          # per day
}

def calculate_footprint(context: dict) -> dict:
    """
    Calculates dynamic carbon footprint metrics based on user context
    and generates automated targeted strategies.
    """
    grid_type = context.get("grid_type", "mixed")
    emissions_factor = GRID_INTENSITY.get(grid_type, 0.45)
    annual_energy_emissions = context.get("monthly_kwh", 0) * emissions_factor * 12

    vehicle = context.get("vehicle_type", "public_transit")
    transport_factor = TRANSPORT_FACTORS.get(vehicle, 0.035)
    annual_transport_emissions = context.get("annual_km", 0) * transport_factor

    diet_type = context.get("diet_type", "low_meat")
    diet_factor = DIET_FACTORS.get(diet_type, 1.70)
    annual_diet_emissions = diet_factor * 365

    total_kg = annual_energy_emissions + annual_transport_emissions + annual_diet_emissions
    total_tons = total_kg / 1000.0

    recommendations = []
    if grid_type in ["coal-heavy", "mixed"] and context.get("monthly_kwh", 0) > 150:
        recommendations.append("⚡ Action: Your regional grid relies on fossil fuels. Transitioning to smart-scheduling or rooftop solar reduces impact dramatically.")
    if vehicle in ["petrol_car", "diesel_car"] and context.get("annual_km", 0) > 8000:
        recommendations.append("🚗 Action: High internal-combustion mileage detected. Optimize route grouping or consider transition corridors.")
    elif vehicle == "electric_vehicle" and grid_type == "coal-heavy":
        recommendations.append("🔌 Insight: EV charging occurs on a high-emission grid. Shift charging behavior to off-peak daytime solar peaks.")
    if diet_type == "heavy_meat":
        recommendations.append("🌱 Action: Shifting away from heavy red meat intake cuts dietary footprint baselines by up to 40%.")

    return {
        "breakdown": {
            "energy_tons": annual_energy_emissions / 1000.0,
            "transport_tons": annual_transport_emissions / 1000.0,
            "diet_tons": annual_diet_emissions / 1000.0
        },
        "total_tons": total_tons,
        "recommendations": recommendations
    }

def main():
    print("==============================================")
    print("   CARBON FOOTPRINT AWARENESS ENGINE v1.0   ")
    print("==============================================\n")
    
    user_context = {
        "grid_type": "mixed",         
        "monthly_kwh": 240,           
        "vehicle_type": "petrol_car",  
        "annual_km": 11000,           
        "diet_type": "heavy_meat"     
    }
    
    results = calculate_footprint(user_context)
    
    print(f"📊 Total Footprint: {results['total_tons']:.2f} metric tons CO2e/year\n")
    print("📂 Section Breakdown:")
    print(f"  - Housing Energy : {results['breakdown']['energy_tons']:.2f} tons")
    print(f"  - Transportation : {results['breakdown']['transport_tons']:.2f} tons")
    print(f"  - Dietary Habits : {results['breakdown']['diet_tons']:.2f} tons\n")
    
    print("💡 Algorithmic Strategy Recommendations:")
    for rec in results['recommendations']:
        print(rec)
    print("\n==============================================")

if __name__ == "__main__":
    main()
