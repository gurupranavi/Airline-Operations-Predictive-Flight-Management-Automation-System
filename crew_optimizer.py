from datetime import datetime, timedelta

class CrewOptimizer:
    def __init__(self, config):
        self.config = config
        self.crew_rules = config['crew_rules']
    
    def optimize_schedule(self, logs_data):
        flights = logs_data['flight_schedule']
        crew_members = logs_data['crew_schedules']
        
        schedule = {}
        
        for flight in flights:
            flight_id = flight['flight_id']
            aircraft_type = flight.get('aircraft_type', 'A320')
            
            aircraft_size = self.config['aircraft_types'][aircraft_type]['type']
            required_crew = self.crew_rules['required_crew_per_flight'][aircraft_size]
            
            assigned_crew = self._assign_crew_to_flight(
                flight, crew_members, required_crew
            )
            
            schedule[flight_id] = {
                'flight': flight,
                'required_crew': required_crew,
                'assigned_crew': assigned_crew,
                'compliance_check': self._check_compliance(flight, assigned_crew)
            }
        
        return schedule
    
    def _assign_crew_to_flight(self, flight, crew_members, required_crew):
        assigned = {
            'pilots': [],
            'crew': []
        }
        
        pilots_needed = required_crew['pilots']
        pilots_assigned = 0
        
        for crew in crew_members:
            if crew['role'] in ['Pilot', 'Co-Pilot']:
                if self._is_crew_available(crew, flight):
                    assigned['pilots'].append({
                        'crew_id': crew['crew_id'],
                        'name': crew['name'],
                        'role': crew['role']
                    })
                    pilots_assigned += 1
                    
                    if pilots_assigned >= pilots_needed:
                        break
        
        crew_needed = required_crew['crew']
        crew_assigned = 0
        
        for crew in crew_members:
            if crew['role'] in ['Senior Attendant', 'Attendant']:
                if self._is_crew_available(crew, flight):
                    assigned['crew'].append({
                        'crew_id': crew['crew_id'],
                        'name': crew['name'],
                        'role': crew['role']
                    })
                    crew_assigned += 1
                    
                    if crew_assigned >= crew_needed:
                        break
        
        assigned['has_enough_pilots'] = len(assigned['pilots']) >= pilots_needed
        assigned['has_enough_crew'] = len(assigned['crew']) >= crew_needed
        assigned['total_assigned'] = len(assigned['pilots']) + len(assigned['crew'])
        
        return assigned
    
    def _is_crew_available(self, crew, flight):
        if crew.get('duty_hours_today', 0) > self.crew_rules['max_duty_hours']:
            return False
        
        if crew.get('rest_hours_remaining', 0) < self.crew_rules['min_rest_hours']:
            return False
        
        if len(crew.get('assigned_flights', [])) >= self.crew_rules['max_consecutive_flights']:
            return False
        
        if crew.get('status') != 'AVAILABLE':
            return False
        
        return True
    
    def _check_compliance(self, flight, assigned_crew):
        issues = []
        
        if not assigned_crew['has_enough_pilots']:
            issues.append("Insufficient pilots")
        
        if not assigned_crew['has_enough_crew']:
            issues.append("Insufficient cabin crew")
        
        if assigned_crew['total_assigned'] == 0:
            issues.append("No crew assigned")
        
        return {
            'is_compliant': len(issues) == 0,
            'issues': issues
        }
    
    def display_schedule(self, schedule):
        print("\n" + "="*80)
        print("CREW SCHEDULE & ASSIGNMENTS")
        print("="*80)
        
        for flight_id, assignment in schedule.items():
            flight = assignment['flight']
            assigned = assignment['assigned_crew']
            compliance = assignment['compliance_check']
            
            print(f"\nFlight: {flight_id} ({flight['route']})")
            print(f"  Scheduled: {flight['scheduled_departure'][11:16]}")
            print(f"  Aircraft: {flight['aircraft_id']} ({flight['aircraft_type']})")
            print(f"  Status: {flight['status']}")
            
            print(f"\n  Required Crew:")
            print(f"    Pilots: {assignment['required_crew']['pilots']}")
            print(f"    Cabin Crew: {assignment['required_crew']['crew']}")
            
            print(f"\n  Assigned Crew ({assigned['total_assigned']} total):")
            
            if assigned['pilots']:
                print(f"    Pilots:")
                for pilot in assigned['pilots']:
                    print(f"      {pilot['name']} ({pilot['role']})")
            
            if assigned['crew']:
                print(f"    Cabin Crew:")
                for crew_member in assigned['crew']:
                    print(f"      {crew_member['name']} ({crew_member['role']})")
            
            print(f"\n  Compliance: {'COMPLIANT' if compliance['is_compliant'] else 'NON-COMPLIANT'}")
            if not compliance['is_compliant']:
                for issue in compliance['issues']:
                    print(f"    {issue}")
            
            print("-" * 80)
            