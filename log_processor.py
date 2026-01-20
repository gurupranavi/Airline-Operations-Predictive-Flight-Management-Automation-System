import json
import os
from datetime import datetime

class LogProcessor:
    def __init__(self, config):
        self.config = config
    
    def process_all_logs(self):
        data = {
            'engine_logs': [],
            'weather_logs': [],
            'crew_schedules': [],
            'passenger_load': [],
            'flight_schedule': []
        }
        
        files_to_process = [
            ('sample_engine_logs.json', 'engine_logs'),
            ('sample_weather_logs.json', 'weather_logs'),
            ('sample_crew_schedules.json', 'crew_schedules'),
            ('sample_passenger_load.json', 'passenger_load'),
            ('sample_flight_schedule.json', 'flight_schedule')
        ]
        
        print("\nLoading data files...")
        
        for filename, key in files_to_process:
            filepath = f'data/{filename}'
            
            if not os.path.exists(filepath):
                print(f"File not found: {filename}")
                continue
            
            try:
                with open(filepath, 'r') as f:
                    data[key] = json.load(f)
                print(f"Loaded {len(data[key])} records from {filename}")
            except json.JSONDecodeError as e:
                print(f"Error parsing {filename}: {e}")
                print(f"File might be empty or corrupted. Please run init_system.py")
                return data
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return data
        
        # Print summary
        if data['flight_schedule']:
            print("\nData Summary:")
            print(f"  Flights: {len(data['flight_schedule'])}")
            print(f"  Engine Logs: {len(data['engine_logs'])}")
            print(f"  Weather Reports: {len(data['weather_logs'])}")
            print(f"  Crew Members: {len(data['crew_schedules'])}")
            print(f"  Passenger Records: {len(data['passenger_load'])}")
        else:
            print("\nNo flight data loaded. Data files might be empty.")
        
        return data
    
    def analyze_routes(self, logs_data):
        suggestions = []
        
        if not logs_data['weather_logs'] or not logs_data['flight_schedule']:
            return suggestions
        
        weather_by_airport = {}
        for weather_log in logs_data['weather_logs']:
            airport = weather_log['airport']
            if airport not in weather_by_airport:
                weather_by_airport[airport] = []
            weather_by_airport[airport].append(weather_log)
        
        for flight in logs_data['flight_schedule']:
            route = flight['route']
            if '-' in route:
                dep_airport = route.split('-')[0]
                arr_airport = route.split('-')[1]
                
                issues = []
                
                if dep_airport in weather_by_airport:
                    latest_weather = weather_by_airport[dep_airport][0]
                    if latest_weather['weather_data']['conditions'] == 'Thunderstorm':
                        issues.append(f"Thunderstorm at {dep_airport}")
                    if latest_weather['crosswind_knots'] > self.config['thresholds']['crosswind_max_knots']:
                        issues.append(f"High crosswind at {dep_airport}")
                
                if arr_airport in weather_by_airport:
                    latest_weather = weather_by_airport[arr_airport][0]
                    if latest_weather['weather_data']['visibility_meters'] < self.config['thresholds']['visibility_min_meters']:
                        issues.append(f"Low visibility at {arr_airport}")
                
                if issues:
                    suggestion = {
                        'flight_id': flight['flight_id'],
                        'route': route,
                        'issues': issues,
                        'suggestion': 'Consider delay or alternate route',
                        'severity': 'HIGH' if 'Thunderstorm' in str(issues) else 'MEDIUM'
                    }
                    suggestions.append(suggestion)
        
        return suggestions