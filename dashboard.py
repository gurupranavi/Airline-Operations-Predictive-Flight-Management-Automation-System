from datetime import datetime
import statistics

class Dashboard:
    def __init__(self, config):
        self.config = config
    
    def display(self, **data):
        print("\n" + "="*100)
        print("AIRLINE OPERATIONS DASHBOARD")
        print("="*100)
        
        logs_data = data.get('logs_data', {})
        delay_predictions = data.get('delay_predictions', {})
        crew_schedule = data.get('crew_schedule', {})
        load_predictions = data.get('load_predictions', {})
        health_alerts = data.get('health_alerts', {})
        route_suggestions = data.get('route_suggestions', [])
        
        self._display_flight_summary(logs_data)
        self._display_delay_summary(delay_predictions)
        self._display_crew_status(crew_schedule, logs_data)
        self._display_load_summary(load_predictions)
        self._display_health_summary(health_alerts)
        self._display_route_analysis(route_suggestions)
        self._display_weather_risk(logs_data)
        
        print("\n" + "="*100)
        print("END OF DASHBOARD")
        print("="*100)
    
    def _display_flight_summary(self, logs_data):
        flights = logs_data.get('flight_schedule', [])
        
        print("\nFLIGHT OPERATIONS SUMMARY")
        print("-" * 50)
        print(f"Total Flights Monitored: {len(flights)}")
        
        if flights:
            status_count = {}
            for flight in flights:
                status = flight.get('status', 'UNKNOWN')
                status_count[status] = status_count.get(status, 0) + 1
            
            print("\nFlight Status Distribution:")
            for status, count in status_count.items():
                print(f"  {status}: {count}")
            
            delays = [f.get('current_delay', 0) for f in flights]
            avg_delay = statistics.mean(delays) if delays else 0
            print(f"\nAverage Current Delay: {avg_delay:.1f} minutes")
            
            aircraft_types = {}
            for flight in flights:
                ac_type = flight.get('aircraft_type', 'UNKNOWN')
                aircraft_types[ac_type] = aircraft_types.get(ac_type, 0) + 1
            
            print("\nAircraft Fleet Distribution:")
            for ac_type, count in aircraft_types.items():
                print(f"  {ac_type}: {count}")
    
    def _display_delay_summary(self, delay_predictions):
        print("\nDELAY PREDICTIONS SUMMARY")
        print("-" * 50)
        
        if not delay_predictions:
            print("No delay predictions available")
            return
        
        severity_count = {'NONE': 0, 'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
        total_delay = 0
        delayed_flights = 0
        
        for prediction in delay_predictions.values():
            severity = prediction.get('severity', 'NONE')
            severity_count[severity] = severity_count.get(severity, 0) + 1
            
            delay = prediction.get('predicted_delay', 0)
            total_delay += delay
            if delay > 0:
                delayed_flights += 1
        
        print(f"Flights with Predicted Delays: {delayed_flights}/{len(delay_predictions)}")
        print(f"Total Predicted Delay Minutes: {total_delay}")
        
        print("\nDelay Severity Distribution:")
        for severity, count in severity_count.items():
            print(f"  {severity}: {count}")
        
        if delayed_flights > 0:
            print("\nTop 3 Most Delayed Flights:")
            sorted_predictions = sorted(
                delay_predictions.items(),
                key=lambda x: x[1].get('predicted_delay', 0),
                reverse=True
            )[:3]
            
            for flight_id, prediction in sorted_predictions:
                if prediction['predicted_delay'] > 0:
                    print(f"  {flight_id}: {prediction['predicted_delay']} min - {prediction['route']}")
    
    def _display_crew_status(self, crew_schedule, logs_data):
        print("\nCREW STATUS SUMMARY")
        print("-" * 50)
        
        crew_members = logs_data.get('crew_schedules', [])
        print(f"Total Crew Members: {len(crew_members)}")
        
        if crew_members:
            status_count = {}
            role_count = {}
            
            for crew in crew_members:
                status = crew.get('status', 'UNKNOWN')
                role = crew.get('role', 'UNKNOWN')
                
                status_count[status] = status_count.get(status, 0) + 1
                role_count[role] = role_count.get(role, 0) + 1
            
            print("\nCrew Availability:")
            for status, count in status_count.items():
                print(f"  {status}: {count}")
            
            print("\nCrew Role Distribution:")
            for role, count in role_count.items():
                print(f"  {role}: {count}")
        
        if crew_schedule:
            compliant = 0
            non_compliant = 0
            
            for assignment in crew_schedule.values():
                if assignment['compliance_check']['is_compliant']:
                    compliant += 1
                else:
                    non_compliant += 1
            
            print(f"\nCrew Assignment Compliance: {compliant}/{len(crew_schedule)} flights compliant")
            if non_compliant > 0:
                print(f"  {non_compliant} flights have crew assignment issues")
    
    def _display_load_summary(self, load_predictions):
        print("\nPASSENGER LOAD SUMMARY")
        print("-" * 50)
        
        if not load_predictions:
            print("No load predictions available")
            return
        
        total_capacity = 0
        total_predicted = 0
        status_count = {}
        
        for prediction in load_predictions.values():
            total_capacity += prediction.get('capacity', 0)
            total_predicted += prediction.get('predicted_load', 0)
            
            status = prediction.get('status', 'UNKNOWN')
            status_count[status] = status_count.get(status, 0) + 1
        
        if total_capacity > 0:
            overall_load_factor = total_predicted / total_capacity
            print(f"Overall Load Factor: {overall_load_factor:.1%}")
            print(f"Total Predicted Passengers: {total_predicted}")
            print(f"Total Available Seats: {total_capacity}")
        
        print("\nFlight Status Distribution:")
        for status, count in status_count.items():
            print(f"  {status}: {count}")
        
        overbooking_risks = [f for f, p in load_predictions.items() 
                           if p.get('status') == 'OVERBOOKING RISK']
        
        if overbooking_risks:
            print(f"\nOverbooking Risk: {len(overbooking_risks)} flights")
            for flight_id in overbooking_risks[:3]:
                print(f"  {flight_id}")
    
    def _display_health_summary(self, health_alerts):
        print("\nAIRCRAFT HEALTH SUMMARY")
        print("-" * 50)
        
        critical = len(health_alerts.get('critical', []))
        warning = len(health_alerts.get('warning', []))
        
        print(f"Critical Alerts: {critical}")
        print(f"Warning Alerts: {warning}")
        
        if critical > 0:
            print("\nCRITICAL ALERTS:")
            for alert in health_alerts['critical'][:3]:
                print(f"  {alert['aircraft_id']}: {alert['alert_type']}")
        
        if health_alerts.get('critical') or health_alerts.get('warning'):
            all_alerts = health_alerts.get('critical', []) + health_alerts.get('warning', [])
            alert_types = {}
            
            for alert in all_alerts:
                alert_type = alert.get('alert_type', 'UNKNOWN')
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            print("\nAlert Type Distribution:")
            for alert_type, count in alert_types.items():
                print(f"  {alert_type}: {count}")
    
    def _display_route_analysis(self, route_suggestions):
        print("\nROUTE ANALYSIS SUMMARY")
        print("-" * 50)
        
        if not route_suggestions:
            print("No route issues detected")
            return
        
        print(f"Flights with Route Issues: {len(route_suggestions)}")
        
        high_severity = [r for r in route_suggestions if r.get('severity') == 'HIGH']
        medium_severity = [r for r in route_suggestions if r.get('severity') == 'MEDIUM']
        
        if high_severity:
            print("\nHIGH SEVERITY ISSUES:")
            for suggestion in high_severity[:3]:
                print(f"  {suggestion['flight_id']} ({suggestion['route']}):")
                for issue in suggestion.get('issues', [])[:2]:
                    print(f"    {issue}")
        
        if medium_severity:
            print("\nMEDIUM SEVERITY ISSUES:")
            for suggestion in medium_severity[:2]:
                print(f"  {suggestion['flight_id']} ({suggestion['route']}):")
                print(f"    {suggestion.get('suggestion', 'No suggestion')}")
    
    def _display_weather_risk(self, logs_data):
        print("\nWEATHER RISK SUMMARY")
        print("-" * 50)
        
        weather_logs = logs_data.get('weather_logs', [])
        
        if not weather_logs:
            print("No weather data available")
            return
        
        conditions = {}
        for log in weather_logs:
            condition = log['weather_data'].get('conditions', 'UNKNOWN')
            conditions[condition] = conditions.get(condition, 0) + 1
        
        print("Current Weather Conditions:")
        for condition, count in conditions.items():
            print(f"  {condition}: {count}")
        
        risky_conditions = ['Thunderstorm', 'Fog', 'Rain']
        risky_airports = []
        
        for log in weather_logs:
            condition = log['weather_data'].get('conditions', '')
            if condition in risky_conditions:
                airport = log.get('airport', 'UNKNOWN')
                if airport not in risky_airports:
                    risky_airports.append(airport)
        
        if risky_airports:
            print(f"\nRisky Weather at: {', '.join(risky_airports)}")