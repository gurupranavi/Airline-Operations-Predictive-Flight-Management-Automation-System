from datetime import datetime

class DelayPredictor:
    def __init__(self, config):
        self.config = config
        self.thresholds = config['thresholds']
    
    def predict_all_flights(self, logs_data):
        predictions = {}
        
        for flight in logs_data['flight_schedule']:
            flight_id = flight['flight_id']
            predictions[flight_id] = self.predict_delay(flight, logs_data)
        
        return predictions
    
    def predict_delay(self, flight, logs_data):
        delay_minutes = 0
        reasons = []
        
        weather_delay, weather_reasons = self._check_weather_delays(flight, logs_data)
        delay_minutes += weather_delay
        reasons.extend(weather_reasons)
        
        maint_delay, maint_reasons = self._check_maintenance_delays(flight, logs_data)
        delay_minutes += maint_delay
        reasons.extend(maint_reasons)
        
        op_delay, op_reasons = self._check_operational_delays(flight, logs_data)
        delay_minutes += op_delay
        reasons.extend(op_reasons)
        
        if delay_minutes == 0:
            severity = "NONE"
        elif delay_minutes <= 30:
            severity = "LOW"
        elif delay_minutes <= 90:
            severity = "MEDIUM"
        else:
            severity = "HIGH"
        
        return {
            'predicted_delay': delay_minutes,
            'reasons': reasons,
            'severity': severity,
            'flight_id': flight['flight_id'],
            'route': flight['route']
        }
    
    def _check_weather_delays(self, flight, logs_data):
        delay = 0
        reasons = []
        
        route = flight['route']
        if '-' in route:
            airports = [route.split('-')[0], route.split('-')[1]]
            
            for airport in airports:
                airport_weather = []
                for weather_log in logs_data['weather_logs']:
                    if weather_log['airport'] == airport:
                        airport_weather.append(weather_log)
                
                if airport_weather:
                    latest_weather = airport_weather[0]
                    weather_data = latest_weather['weather_data']
                    
                    if latest_weather.get('crosswind_knots', 0) > self.thresholds['crosswind_max_knots']:
                        delay += 45
                        reasons.append(f"High crosswind at {airport}")
                    
                    if weather_data['conditions'] == 'Thunderstorm':
                        delay += 90
                        reasons.append(f"Thunderstorm at {airport}")
                    
                    if weather_data['visibility_meters'] < self.thresholds['visibility_min_meters']:
                        delay += 30
                        reasons.append(f"Low visibility at {airport}")
        
        return delay, reasons
    
    def _check_maintenance_delays(self, flight, logs_data):
        delay = 0
        reasons = []
        aircraft_id = flight['aircraft_id']
        
        aircraft_engine_logs = []
        for engine_log in logs_data['engine_logs']:
            if engine_log['aircraft_id'] == aircraft_id:
                aircraft_engine_logs.append(engine_log)
        
        if aircraft_engine_logs:
            latest_log = aircraft_engine_logs[0]
            metrics = latest_log['metrics']
            
            if 'engine_thrust_percent' in metrics:
                thrust_dev = abs(100 - metrics['engine_thrust_percent'])
                if thrust_dev > self.thresholds['engine_thrust_deviation_percent']:
                    delay += 60
                    reasons.append(f"Engine thrust deviation: {thrust_dev:.1f}%")
            
            if latest_log.get('status') == 'WARNING':
                delay += 30
                reasons.append("Aircraft maintenance warning")
            
            if 'cabin_pressure_psi' in metrics:
                if metrics['cabin_pressure_psi'] < 10.8:
                    delay += 45
                    reasons.append(f"Low cabin pressure: {metrics['cabin_pressure_psi']:.1f} psi")
        
        return delay, reasons
    
    def _check_operational_delays(self, flight, logs_data):
        delay = 0
        reasons = []
        
        if flight.get('runway_queue', 0) > self.thresholds['runway_queue_max_minutes']:
            delay += flight['runway_queue']
            reasons.append(f"Runway queue: {flight['runway_queue']} min")
        
        if flight.get('boarding_time_minutes', 0) > self.thresholds['boarding_max_minutes']:
            delay += 30
            reasons.append(f"Boarding delay: {flight['boarding_time_minutes']} min")
        
        crew_available = self._check_crew_availability(flight, logs_data)
        if not crew_available:
            delay += 60
            reasons.append("Crew shortage")
        
        return delay, reasons
    
    def _check_crew_availability(self, flight, logs_data):
        available_crew = 0
        for crew in logs_data['crew_schedules']:
            if crew['status'] == 'AVAILABLE':
                available_crew += 1
        
        return available_crew > 5