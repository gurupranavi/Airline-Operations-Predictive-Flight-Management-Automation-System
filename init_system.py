
import os
import json
import random
from datetime import datetime, timedelta

def create_sample_data():
    """Create fresh sample data files"""
    
    print("Creating sample data files...")
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('output/reports', exist_ok=True)
    
    # Create sample engine logs
    engine_logs = []
    aircraft_ids = [f"GA-{i:03d}" for i in range(1, 11)]
    flight_ids = [f"GA{random.randint(100, 999)}" for _ in range(20)]
    
    for _ in range(100):
        log = {
            "flight_id": random.choice(flight_ids),
            "aircraft_id": random.choice(aircraft_ids),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 72))).isoformat(),
            "metrics": {
                "engine_thrust_percent": random.uniform(70, 105),
                "engine_vibration": random.uniform(1.0, 9.0),
                "fuel_burn_rate": random.uniform(2000, 3500),
                "oil_temperature": random.uniform(80, 120),
                "oil_pressure": random.uniform(35, 50),
                "cabin_pressure_psi": random.uniform(10.5, 11.5),
                "cabin_temperature_c": random.uniform(20, 30),
                "airspeed_knots": random.uniform(400, 550),
                "altitude_ft": random.uniform(30000, 40000),
                "turbulence_level": random.uniform(1, 10)
            },
            "status": "NORMAL" if random.random() > 0.15 else "WARNING"
        }
        engine_logs.append(log)
    
    with open('data/sample_engine_logs.json', 'w') as f:
        json.dump(engine_logs, f, indent=2)
    print(f"Created sample_engine_logs.json with {len(engine_logs)} records")
    
    # Create sample weather logs
    weather_logs = []
    airports = ["DEL", "BOM", "MAA", "BLR", "LHR", "JFK", "DXB", "SYD"]
    
    for _ in range(50):
        log = {
            "airport": random.choice(airports),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat(),
            "weather_data": {
                "temperature_c": random.uniform(10, 35),
                "wind_speed_knots": random.uniform(5, 55),
                "wind_direction": random.randint(0, 360),
                "visibility_meters": random.uniform(500, 10000),
                "humidity_percent": random.uniform(30, 95),
                "pressure_hpa": random.uniform(980, 1030),
                "conditions": random.choice(["Clear", "Cloudy", "Rain", "Fog", "Thunderstorm"])
            },
            "crosswind_knots": random.uniform(10, 60)
        }
        weather_logs.append(log)
    
    with open('data/sample_weather_logs.json', 'w') as f:
        json.dump(weather_logs, f, indent=2)
    print(f"Created sample_weather_logs.json with {len(weather_logs)} records")
    
    # Create sample crew schedules
    crew_schedules = []
    from faker import Faker
    fake = Faker()
    
    for i in range(20):
        schedule = {
            "crew_id": f"C{1000 + i}",
            "name": fake.name(),
            "role": random.choice(["Pilot", "Co-Pilot", "Senior Attendant", "Attendant"]),
            "current_location": random.choice(["DEL", "BOM", "MAA", "DXB"]),
            "duty_hours_today": random.uniform(0, 12),
            "rest_hours_remaining": random.uniform(0, 24),
            "assigned_flights": [
                f"GA{random.randint(100, 999)}" for _ in range(random.randint(0, 3))
            ],
            "next_available": (datetime.now() + timedelta(hours=random.randint(0, 12))).isoformat(),
            "status": random.choice(["AVAILABLE", "ON_DUTY", "RESTING"])
        }
        crew_schedules.append(schedule)
    
    with open('data/sample_crew_schedules.json', 'w') as f:
        json.dump(crew_schedules, f, indent=2)
    print(f"Created sample_crew_schedules.json with {len(crew_schedules)} records")
    
    # Create sample passenger load
    passenger_load = []
    routes = ["DEL-MAA", "DEL-BOM", "DEL-BLR", "DEL-HYD", "DEL-CCU", 
              "DEL-LHR", "DEL-JFK", "DEL-DXB", "DEL-SIN", "DEL-SYD"]
    
    for route in routes:
        for day in range(7):
            load = {
                "route": route,
                "date": (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d'),
                "historical_loads": [random.randint(50, 180) for _ in range(30)],
                "current_bookings": random.randint(30, 180),
                "capacity": 180,
                "seasonal_factor": random.uniform(0.8, 1.5)
            }
            passenger_load.append(load)
    
    with open('data/sample_passenger_load.json', 'w') as f:
        json.dump(passenger_load, f, indent=2)
    print(f"Created sample_passenger_load.json with {len(passenger_load)} records")
    
    # Create sample flight schedule
    flight_schedule = []
    
    for i in range(20):
        flight = {
            "flight_id": f"GA{100 + i}",
            "route": random.choice(routes),
            "scheduled_departure": (datetime.now() + timedelta(hours=random.randint(1, 24))).isoformat(),
            "scheduled_arrival": (datetime.now() + timedelta(hours=random.randint(3, 27))).isoformat(),
            "aircraft_id": f"GA-{random.randint(1, 10):03d}",
            "aircraft_type": random.choice(["A320", "B737", "A380", "ATR72"]),
            "status": random.choice(["SCHEDULED", "BOARDING", "DEPARTED", "IN_FLIGHT"]),
            "current_delay": random.randint(0, 120),
            "gate": f"Gate {random.randint(1, 50)}",
            "runway_queue": random.randint(0, 40),
            "boarding_time_minutes": random.randint(20, 60)
        }
        flight_schedule.append(flight)
    
    with open('data/sample_flight_schedule.json', 'w') as f:
        json.dump(flight_schedule, f, indent=2)
    print(f"Created sample_flight_schedule.json with {len(flight_schedule)} records")
    
    # Create default config if not exists
    if not os.path.exists('airline_config.json'):
        default_config = {
            "airline": {
                "name": "Global Airlines",
                "code": "GA",
                "hub_airport": "DEL"
            },
            "thresholds": {
                "crosswind_max_knots": 40,
                "visibility_min_meters": 1500,
                "engine_thrust_deviation_percent": 20,
                "runway_queue_max_minutes": 25,
                "boarding_max_minutes": 45,
                "turbulence_threshold": 5,
                "engine_vibration_threshold": 7.0,
                "altitude_fluctuation_threshold": 3000,
                "fuel_burn_threshold_percent": 15,
                "cabin_temp_max_celsius": 28
            },
            "crew_rules": {
                "max_duty_hours": 14,
                "min_rest_hours": 10,
                "max_consecutive_flights": 4,
                "required_crew_per_flight": {
                    "small": {"pilots": 2, "crew": 4},
                    "medium": {"pilots": 2, "crew": 6},
                    "large": {"pilots": 3, "crew": 8}
                }
            },
            "aircraft_types": {
                "A320": {"type": "medium", "capacity": 180, "range_km": 6100},
                "B737": {"type": "medium", "capacity": 178, "range_km": 6285},
                "A380": {"type": "large", "capacity": 555, "range_km": 15700},
                "ATR72": {"type": "small", "capacity": 78, "range_km": 1530}
            },
            "routes": {
                "domestic": ["DEL-MAA", "DEL-BOM", "DEL-BLR", "DEL-HYD", "DEL-CCU"],
                "international": ["DEL-LHR", "DEL-JFK", "DEL-DXB", "DEL-SIN", "DEL-SYD"]
            }
        }
        
        with open('airline_config.json', 'w') as f:
            json.dump(default_config, f, indent=2)
        print("Created airline_config.json")
    
    print("\nSample data creation complete!")

if __name__ == "__main__":
    create_sample_data()