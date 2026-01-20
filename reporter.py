import json
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, config):
        self.config = config
    
    def generate_daily_report(self, **data):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'output/reports/aviation_report_{date_str}.txt'
        
        with open(filename, 'w') as f:
            f.write(self._generate_report_content(date_str, **data))
        
        print(f"Report saved: {filename}")
        return filename
    
    def generate_custom_report(self, date, **data):
        filename = f'output/reports/aviation_report_custom_{date}.txt'
        
        with open(filename, 'w') as f:
            f.write(self._generate_report_content(date, **data))
        
        return filename
    
    def _generate_report_content(self, report_date, **data):
        content = []
        
        content.append("="*80)
        content.append(f"AVIATION OPERATIONS DAILY REPORT")
        content.append(f"Date: {report_date}")
        content.append(f"Airline: {self.config['airline']['name']} ({self.config['airline']['code']})")
        content.append("="*80)
        content.append("\n")
        
        logs_data = data.get('logs_data', {})
        delay_predictions = data.get('delay_predictions', {})
        crew_schedule = data.get('crew_schedule', {})
        load_predictions = data.get('load_predictions', {})
        health_alerts = data.get('health_alerts', {})
        route_suggestions = data.get('route_suggestions', [])
        
        content.append("1. EXECUTIVE SUMMARY")
        content.append("-"*40)
        
        flights = logs_data.get('flight_schedule', [])
        content.append(f"Total Flights Monitored: {len(flights)}")
        
        delayed = sum(1 for p in delay_predictions.values() 
                     if p.get('predicted_delay', 0) > 0)
        content.append(f"Flights with Predicted Delays: {delayed}")
        
        critical_alerts = len(health_alerts.get('critical', []))
        warning_alerts = len(health_alerts.get('warning', []))
        content.append(f"Critical Aircraft Alerts: {critical_alerts}")
        content.append(f"Warning Alerts: {warning_alerts}")
        content.append("\n")
        
        content.append("2. FLIGHT OPERATIONS")
        content.append("-"*40)
        
        if flights:
            status_count = {}
            for flight in flights:
                status = flight.get('status', 'UNKNOWN')
                status_count[status] = status_count.get(status, 0) + 1
            
            for status, count in status_count.items():
                content.append(f"{status}: {count}")
            
            current_delays = [f for f in flights if f.get('current_delay', 0) > 0]
            if current_delays:
                content.append(f"\nCurrently Delayed Flights: {len(current_delays)}")
                for flight in current_delays[:5]:
                    content.append(f"  {flight['flight_id']}: {flight['current_delay']} min delay")
        content.append("\n")
        
        content.append("3. DELAY PREDICTIONS")
        content.append("-"*40)
        
        if delay_predictions:
            severity_groups = {}
            for flight_id, prediction in delay_predictions.items():
                severity = prediction.get('severity', 'NONE')
                if severity not in severity_groups:
                    severity_groups[severity] = []
                severity_groups[severity].append(prediction)
            
            for severity, predictions in severity_groups.items():
                if severity != 'NONE':
                    content.append(f"\n{severity} Severity Delays ({len(predictions)} flights):")
                    for pred in predictions[:3]:
                        content.append(f"  {pred['flight_id']}: {pred['predicted_delay']} min - {pred['route']}")
                        if pred.get('reasons'):
                            content.append(f"    Reasons: {', '.join(pred['reasons'][:2])}")
        content.append("\n")
        
        content.append("4. CREW SCHEDULING")
        content.append("-"*40)
        
        if crew_schedule:
            compliant = sum(1 for a in crew_schedule.values() 
                           if a['compliance_check']['is_compliant'])
            content.append(f"Compliant Assignments: {compliant}/{len(crew_schedule)}")
            
            non_compliant = [f for f, a in crew_schedule.items() 
                            if not a['compliance_check']['is_compliant']]
            
            if non_compliant:
                content.append(f"\nNon-Compliant Flights ({len(non_compliant)}):")
                for flight_id in non_compliant[:5]:
                    assignment = crew_schedule[flight_id]
                    issues = assignment['compliance_check']['issues']
                    content.append(f"  {flight_id}: {', '.join(issues)}")
        content.append("\n")
        
        content.append("5. PASSENGER LOAD PREDICTIONS")
        content.append("-"*40)
        
        if load_predictions:
            total_capacity = 0
            total_predicted = 0
            
            for prediction in load_predictions.values():
                total_capacity += prediction.get('capacity', 0)
                total_predicted += prediction.get('predicted_load', 0)
            
            if total_capacity > 0:
                load_factor = total_predicted / total_capacity
                content.append(f"Overall Load Factor: {load_factor:.1%}")
                content.append(f"Total Predicted Passengers: {total_predicted}")
                content.append(f"Total Available Capacity: {total_capacity}")
            
            overbooking = [f for f, p in load_predictions.items() 
                          if p.get('status') == 'OVERBOOKING RISK']
            
            if overbooking:
                content.append(f"\nOverbooking Risk ({len(overbooking)} flights):")
                for flight_id in overbooking[:3]:
                    pred = load_predictions[flight_id]
                    content.append(f"  {flight_id}: {pred['predicted_load']}/{pred['capacity']} seats")
        content.append("\n")
        
        content.append("6. AIRCRAFT HEALTH MONITORING")
        content.append("-"*40)
        
        if health_alerts:
            critical = health_alerts.get('critical', [])
            warning = health_alerts.get('warning', [])
            
            content.append(f"Critical Alerts: {len(critical)}")
            content.append(f"Warning Alerts: {len(warning)}")
            
            if critical:
                content.append("\nCritical Alerts:")
                for alert in critical[:3]:
                    content.append(f"  {alert['aircraft_id']}: {alert['alert_type']}")
                    content.append(f"    {alert['message']}")
            
            all_alerts = critical + warning
            if all_alerts:
                aircraft_with_alerts = set(alert['aircraft_id'] for alert in all_alerts)
                content.append(f"\nAircraft with Alerts: {len(aircraft_with_alerts)}")
        content.append("\n")
        
        content.append("7. ROUTE ANALYSIS & DIVERSION SUGGESTIONS")
        content.append("-"*40)
        
        if route_suggestions:
            content.append(f"Flights with Route Issues: {len(route_suggestions)}")
            
            high_severity = [r for r in route_suggestions if r.get('severity') == 'HIGH']
            if high_severity:
                content.append(f"\nHigh Severity Issues ({len(high_severity)}):")
                for suggestion in high_severity[:3]:
                    content.append(f"  {suggestion['flight_id']} ({suggestion['route']})")
                    content.append(f"    Issues: {', '.join(suggestion.get('issues', []))}")
                    content.append(f"    Suggestion: {suggestion.get('suggestion', 'None')}")
        else:
            content.append("No major route issues detected.")
        content.append("\n")
        
        content.append("8. RECOMMENDATIONS & ACTIONS REQUIRED")
        content.append("-"*40)
        
        recommendations = []
        
        if health_alerts.get('critical'):
            recommendations.append("Immediate maintenance required for aircraft with critical alerts")
        
        if route_suggestions:
            high_severity = [r for r in route_suggestions if r.get('severity') == 'HIGH']
            if high_severity:
                recommendations.append(f"Review and possibly reschedule {len(high_severity)} high-risk flights")
        
        overbooking = [f for f, p in load_predictions.items() 
                      if p.get('status') == 'OVERBOOKING RISK'] if load_predictions else []
        if overbooking:
            recommendations.append(f"Manage overbooking for {len(overbooking)} flights")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                content.append(f"{i}. {rec}")
        else:
            content.append("No urgent actions required. Operations are running smoothly.")
        
        content.append("\n" + "="*80)
        content.append("END OF REPORT")
        content.append("="*80)
        
        return '\n'.join(content)