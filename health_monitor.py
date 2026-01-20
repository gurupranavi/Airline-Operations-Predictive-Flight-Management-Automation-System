import json
from datetime import datetime

class HealthMonitor:
    def __init__(self, config):
        self.config = config
        self.thresholds = config['thresholds']
    
    def monitor_all_aircraft(self, logs_data):
        alerts = {
            'critical': [],
            'warning': []
        }
        
        logs_by_aircraft = {}
        for engine_log in logs_data['engine_logs']:
            aircraft_id = engine_log['aircraft_id']
            if aircraft_id not in logs_by_aircraft:
                logs_by_aircraft[aircraft_id] = []
            logs_by_aircraft[aircraft_id].append(engine_log)
        
        for aircraft_id, aircraft_logs in logs_by_aircraft.items():
            if aircraft_logs:
                latest_log = aircraft_logs[0]
                aircraft_alerts = self._analyze_aircraft_health(aircraft_id, latest_log)
                
                for alert in aircraft_alerts:
                    if alert['severity'] == 'CRITICAL':
                        alerts['critical'].append(alert)
                        self._log_critical_alert(alert)
                    else:
                        alerts['warning'].append(alert)
                        self._log_warning_alert(alert)
        
        return alerts
    
    def _analyze_aircraft_health(self, aircraft_id, engine_log):
        alerts = []
        metrics = engine_log.get('metrics', {})
        
        vibration = metrics.get('engine_vibration', 0)
        if vibration > self.thresholds['engine_vibration_threshold']:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'ENGINE_VIBRATION',
                'message': f'High engine vibration: {vibration:.1f}',
                'severity': 'CRITICAL' if vibration > 8.0 else 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': vibration,
                'threshold': self.thresholds['engine_vibration_threshold']
            })
        
        fuel_burn = metrics.get('fuel_burn_rate', 0)
        normal_fuel_burn = 2500
        fuel_deviation = abs(fuel_burn - normal_fuel_burn) / normal_fuel_burn * 100
        
        if fuel_deviation > self.thresholds['fuel_burn_threshold_percent']:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'FUEL_BURN_ANOMALY',
                'message': f'Abnormal fuel burn: {fuel_burn:.0f} kg/hr',
                'severity': 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': fuel_deviation,
                'threshold': self.thresholds['fuel_burn_threshold_percent']
            })
        
        oil_temp = metrics.get('oil_temperature', 0)
        if oil_temp > 110:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'OIL_TEMPERATURE',
                'message': f'High oil temperature: {oil_temp:.1f}C',
                'severity': 'WARNING' if oil_temp < 115 else 'CRITICAL',
                'timestamp': datetime.now().isoformat(),
                'metric_value': oil_temp,
                'threshold': 110
            })
        
        thrust = metrics.get('engine_thrust_percent', 100)
        thrust_deviation = abs(100 - thrust)
        if thrust_deviation > self.thresholds['engine_thrust_deviation_percent']:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'ENGINE_THRUST',
                'message': f'Engine thrust deviation: {thrust:.1f}%',
                'severity': 'CRITICAL' if thrust_deviation > 25 else 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': thrust_deviation,
                'threshold': self.thresholds['engine_thrust_deviation_percent']
            })
        
        cabin_temp = metrics.get('cabin_temperature_c', 0)
        if cabin_temp > self.thresholds['cabin_temp_max_celsius']:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'CABIN_TEMPERATURE',
                'message': f'High cabin temperature: {cabin_temp:.1f}C',
                'severity': 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': cabin_temp,
                'threshold': self.thresholds['cabin_temp_max_celsius']
            })
        
        turbulence = metrics.get('turbulence_level', 0)
        if turbulence > self.thresholds['turbulence_threshold']:
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'TURBULENCE',
                'message': f'High turbulence level: {turbulence:.1f}',
                'severity': 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': turbulence,
                'threshold': self.thresholds['turbulence_threshold']
            })
        
        if engine_log.get('status') == 'WARNING':
            alerts.append({
                'aircraft_id': aircraft_id,
                'alert_type': 'SYSTEM_WARNING',
                'message': 'Aircraft system warning flag detected',
                'severity': 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'metric_value': 'WARNING',
                'threshold': 'NORMAL'
            })
        
        return alerts
    
    def _log_critical_alert(self, alert):
        log_entry = {
            'timestamp': alert['timestamp'],
            'aircraft_id': alert['aircraft_id'],
            'alert_type': alert['alert_type'],
            'message': alert['message'],
            'severity': alert['severity']
        }
        
        try:
            with open('logs/critical_flight_alerts.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Error logging critical alert: {e}")
    
    def _log_warning_alert(self, alert):
        log_entry = {
            'timestamp': alert['timestamp'],
            'aircraft_id': alert['aircraft_id'],
            'alert_type': alert['alert_type'],
            'message': alert['message'],
            'severity': alert['severity']
        }
        
        try:
            with open('logs/aircraft_health_alerts.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Error logging warning alert: {e}")