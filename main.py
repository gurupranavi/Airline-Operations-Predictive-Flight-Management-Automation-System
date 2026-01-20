import json
import os
import sys
from datetime import datetime, timedelta

# Import modules
try:
    from modules.log_processor import LogProcessor
    from modules.delay_predictor import DelayPredictor
    from modules.crew_optimizer import CrewOptimizer
    from modules.load_predictor import LoadPredictor
    from modules.health_monitor import HealthMonitor
    from modules.dashboard import Dashboard
    from modules.reporter import ReportGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure all module files are in the 'modules' directory.")
    sys.exit(1)

class AirlineOperationsSystem:
    def __init__(self):
        self.load_config()
        self.setup_directories()
        self.initialize_modules()
        
    def load_config(self):
        try:
            with open('airline_config.json', 'r') as f:
                self.config = json.load(f)
            print("Configuration loaded successfully")
        except FileNotFoundError:
            print("Configuration file not found. Please run init_system.py first.")
            sys.exit(1)
    
    def setup_directories(self):
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('output/reports', exist_ok=True)
    
    def initialize_modules(self):
        self.log_processor = LogProcessor(self.config)
        self.delay_predictor = DelayPredictor(self.config)
        self.crew_optimizer = CrewOptimizer(self.config)
        self.load_predictor = LoadPredictor(self.config)
        self.health_monitor = HealthMonitor(self.config)
        self.dashboard = Dashboard(self.config)
        self.reporter = ReportGenerator(self.config)
    
    def check_data_files(self):
        """Check if data files exist and are valid"""
        data_files = [
            'sample_engine_logs.json',
            'sample_weather_logs.json',
            'sample_crew_schedules.json',
            'sample_passenger_load.json',
            'sample_flight_schedule.json'
        ]
        
        all_exist = True
        for file in data_files:
            filepath = f'data/{file}'
            if not os.path.exists(filepath):
                print(f"Missing data file: {file}")
                all_exist = False
            else:
                # Check if file is valid JSON
                try:
                    with open(filepath, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    print(f"Invalid JSON in {file}")
                    all_exist = False
        
        return all_exist
    
    def process_daily_operations(self):
        print("\n" + "="*60)
        print("AIRLINE OPERATIONS PROCESSING SYSTEM")
        print("="*60)
        
        # Check data files first
        if not self.check_data_files():
            print("\nData files are missing or invalid.")
            print("Please run init_system.py to create sample data.")
            return
        
        print("\nProcessing System Logs...")
        logs_data = self.log_processor.process_all_logs()
        
        if not logs_data or not logs_data['flight_schedule']:
            print("No flight data found. Please check data files.")
            return
        
        print("\nPredicting Flight Delays...")
        delay_predictions = self.delay_predictor.predict_all_flights(logs_data)
        
        print("\nOptimizing Crew Schedules...")
        crew_schedule = self.crew_optimizer.optimize_schedule(logs_data)
        
        print("\nPredicting Passenger Load...")
        load_predictions = self.load_predictor.predict_loads(logs_data)
        
        print("\nMonitoring Aircraft Health...")
        health_alerts = self.health_monitor.monitor_all_aircraft(logs_data)
        
        print("\nAnalyzing Flight Routes...")
        route_suggestions = self.log_processor.analyze_routes(logs_data)
        
        print("\nGenerating Operations Dashboard...")
        self.dashboard.display(
            logs_data=logs_data,
            delay_predictions=delay_predictions,
            crew_schedule=crew_schedule,
            load_predictions=load_predictions,
            health_alerts=health_alerts,
            route_suggestions=route_suggestions
        )
        
        print("\nGenerating Daily Report...")
        report_path = self.reporter.generate_daily_report(
            logs_data=logs_data,
            delay_predictions=delay_predictions,
            crew_schedule=crew_schedule,
            load_predictions=load_predictions,
            health_alerts=health_alerts,
            route_suggestions=route_suggestions
        )
        
        print(f"\nDaily report generated: {report_path}")
    
    def generate_daily_report(self):
        print("\nGenerating Daily Report...")
        
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            print("Please run init_system.py to create sample data.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        
        if not logs_data['flight_schedule']:
            print("No flight data available to generate report.")
            return
        
        delay_predictions = self.delay_predictor.predict_all_flights(logs_data)
        crew_schedule = self.crew_optimizer.optimize_schedule(logs_data)
        load_predictions = self.load_predictor.predict_loads(logs_data)
        health_alerts = self.health_monitor.monitor_all_aircraft(logs_data)
        route_suggestions = self.log_processor.analyze_routes(logs_data)
        
        report_path = self.reporter.generate_daily_report(
            logs_data=logs_data,
            delay_predictions=delay_predictions,
            crew_schedule=crew_schedule,
            load_predictions=load_predictions,
            health_alerts=health_alerts,
            route_suggestions=route_suggestions
        )
        
        print(f"Daily report generated: {report_path}")
        return report_path
    
    def run_interactive_mode(self):
        while True:
            print("\n" + "="*60)
            print("AIRLINE OPERATIONS DASHBOARD MENU")
            print("="*60)
            print("1. Process Daily Operations (Full Run)")
            print("2. Generate Daily Report Only")
            print("3. View Flight Delay Predictions")
            print("4. View Crew Schedule")
            print("5. View Aircraft Health Alerts")
            print("6. View Passenger Load Predictions")
            print("7. Generate Custom Report")
            print("8. View System Configuration")
            print("9. Initialize/Reset Sample Data")
            print("10. Exit")
            print("="*60)
            
            try:
                choice = input("\nEnter your choice (1-10): ").strip()
                
                if choice == '1':
                    self.process_daily_operations()
                elif choice == '2':
                    self.generate_daily_report()
                elif choice == '3':
                    self.view_delay_predictions()
                elif choice == '4':
                    self.view_crew_schedule()
                elif choice == '5':
                    self.view_health_alerts()
                elif choice == '6':
                    self.view_load_predictions()
                elif choice == '7':
                    self.generate_custom_report()
                elif choice == '8':
                    self.view_configuration()
                elif choice == '9':
                    print("\nInitializing sample data...")
                    os.system("python init_system.py")
                elif choice == '10':
                    print("\nThank you for using Airline Operations System!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def view_delay_predictions(self):
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        if not logs_data['flight_schedule']:
            print("No flight data available.")
            return
        
        predictions = self.delay_predictor.predict_all_flights(logs_data)
        
        print("\n" + "="*60)
        print("FLIGHT DELAY PREDICTIONS")
        print("="*60)
        
        delayed_flights = 0
        for flight_id, prediction in predictions.items():
            if prediction['predicted_delay'] > 0:
                delayed_flights += 1
                print(f"\nFlight: {flight_id}")
                print(f"Route: {prediction['route']}")
                print(f"Predicted Delay: {prediction['predicted_delay']} minutes")
                print(f"Reasons: {', '.join(prediction['reasons'])}")
                print(f"Severity: {prediction['severity']}")
        
        if delayed_flights == 0:
            print("\nNo flights predicted to be delayed.")
        else:
            print(f"\nTotal delayed flights: {delayed_flights}")
    
    def view_crew_schedule(self):
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        if not logs_data['flight_schedule']:
            print("No flight data available.")
            return
        
        schedule = self.crew_optimizer.optimize_schedule(logs_data)
        self.crew_optimizer.display_schedule(schedule)
    
    def view_health_alerts(self):
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        if not logs_data.get('engine_logs'):
            print("No engine log data available.")
            return
        
        alerts = self.health_monitor.monitor_all_aircraft(logs_data)
        
        print("\n" + "="*60)
        print("AIRCRAFT HEALTH ALERTS")
        print("="*60)
        
        if not alerts['critical'] and not alerts['warning']:
            print("\nNo health alerts detected.")
            return
        
        if alerts['critical']:
            print("\nCRITICAL ALERTS:")
            for alert in alerts['critical']:
                print(f"\nAircraft: {alert['aircraft_id']}")
                print(f"Alert: {alert['alert_type']}")
                print(f"Message: {alert['message']}")
                print(f"Time: {alert['timestamp'][:19]}")
        
        if alerts['warning']:
            print("\nWARNING ALERTS:")
            for alert in alerts['warning']:
                print(f"\nAircraft: {alert['aircraft_id']}")
                print(f"Alert: {alert['alert_type']}")
                print(f"Message: {alert['message']}")
                print(f"Time: {alert['timestamp'][:19]}")
    
    def view_load_predictions(self):
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        if not logs_data['flight_schedule']:
            print("No flight data available.")
            return
        
        predictions = self.load_predictor.predict_loads(logs_data)
        
        print("\n" + "="*60)
        print("PASSENGER LOAD PREDICTIONS")
        print("="*60)
        
        for flight_id, prediction in predictions.items():
            print(f"\nFlight: {flight_id}")
            print(f"Route: {prediction['route']}")
            print(f"Predicted Load: {prediction['predicted_load']} passengers")
            print(f"Capacity: {prediction['capacity']} passengers")
            print(f"Load Factor: {prediction['load_factor']:.1%}")
            print(f"Status: {prediction['status']}")
    
    def generate_custom_report(self):
        date_str = input("Enter date (YYYY-MM-DD, leave empty for today): ").strip()
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        if not self.check_data_files():
            print("Data files are missing or invalid.")
            return
        
        logs_data = self.log_processor.process_all_logs()
        if not logs_data['flight_schedule']:
            print("No flight data available.")
            return
        
        predictions = self.delay_predictor.predict_all_flights(logs_data)
        schedule = self.crew_optimizer.optimize_schedule(logs_data)
        load_preds = self.load_predictor.predict_loads(logs_data)
        alerts = self.health_monitor.monitor_all_aircraft(logs_data)
        route_suggestions = self.log_processor.analyze_routes(logs_data)
        
        report_path = self.reporter.generate_custom_report(
            date=date_str,
            logs_data=logs_data,
            delay_predictions=predictions,
            crew_schedule=schedule,
            load_predictions=load_preds,
            health_alerts=alerts,
            route_suggestions=route_suggestions
        )
        
        print(f"\nCustom report generated: {report_path}")
    
    def view_configuration(self):
        print("\n" + "="*60)
        print("SYSTEM CONFIGURATION")
        print("="*60)
        
        print(f"\nAirline: {self.config['airline']['name']} ({self.config['airline']['code']})")
        print(f"Hub Airport: {self.config['airline']['hub_airport']}")
        
        print("\nThresholds:")
        for key, value in self.config['thresholds'].items():
            print(f"  {key}: {value}")
        
        print("\nCrew Rules:")
        for key, value in self.config['crew_rules'].items():
            if key != 'required_crew_per_flight':
                print(f"  {key}: {value}")
        
        print("\nAircraft Types:")
        for ac_type, specs in self.config['aircraft_types'].items():
            print(f"  {ac_type}: {specs['capacity']} seats, {specs['range_km']} km range")

def main():
    try:
        print("\n" + "="*60)
        print("AIRLINE OPERATIONS & FLIGHT MANAGEMENT SYSTEM")
        print("="*60)
        
        system = AirlineOperationsSystem()
        system.run_interactive_mode()
    except KeyboardInterrupt:
        print("\nSystem shutdown by user")
    except Exception as e:
        print(f"\nSystem error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()