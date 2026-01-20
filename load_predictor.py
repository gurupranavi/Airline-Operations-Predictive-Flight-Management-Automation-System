import statistics
from datetime import datetime

class LoadPredictor:
    def __init__(self, config):
        self.config = config
    
    def predict_loads(self, logs_data):
        predictions = {}
        
        load_by_route = {}
        for load_data in logs_data['passenger_load']:
            route = load_data['route']
            if route not in load_by_route:
                load_by_route[route] = []
            load_by_route[route].append(load_data)
        
        for flight in logs_data['flight_schedule']:
            flight_id = flight['flight_id']
            route = flight['route']
            
            if route in load_by_route:
                predictions[flight_id] = self._predict_for_flight(flight, load_by_route[route])
            else:
                predictions[flight_id] = self._predict_default(flight)
        
        return predictions
    
    def _predict_for_flight(self, flight, route_loads):
        aircraft_type = flight.get('aircraft_type', 'A320')
        capacity = self.config['aircraft_types'][aircraft_type]['capacity']
        
        all_historical = []
        for load_data in route_loads:
            all_historical.extend(load_data['historical_loads'][-7:])
        
        if all_historical:
            predicted_load = statistics.mean(all_historical)
            
            seasonal_factors = [ld.get('seasonal_factor', 1.0) for ld in route_loads]
            avg_seasonal = statistics.mean(seasonal_factors) if seasonal_factors else 1.0
            predicted_load *= avg_seasonal
            
            predicted_load = min(predicted_load, capacity)
        else:
            predicted_load = capacity * 0.7
        
        current_bookings = route_loads[0].get('current_bookings', 0) if route_loads else 0
        
        if current_bookings > predicted_load:
            predicted_load = current_bookings * 1.1
        
        load_factor = predicted_load / capacity
        
        if load_factor > 0.95:
            status = "OVERBOOKING RISK"
        elif load_factor > 0.8:
            status = "HIGH DEMAND"
        elif load_factor > 0.6:
            status = "MODERATE"
        elif load_factor > 0.4:
            status = "LOW"
        else:
            status = "UNDER-UTILIZED"
        
        return {
            'route': flight['route'],
            'predicted_load': round(predicted_load),
            'current_bookings': current_bookings,
            'capacity': capacity,
            'load_factor': load_factor,
            'status': status,
            'aircraft_type': aircraft_type
        }
    
    def _predict_default(self, flight):
        aircraft_type = flight.get('aircraft_type', 'A320')
        capacity = self.config['aircraft_types'][aircraft_type]['capacity']
        
        route = flight['route']
        if 'DEL' in route or 'BOM' in route:
            predicted_load = capacity * 0.85
        elif 'LHR' in route or 'JFK' in route:
            predicted_load = capacity * 0.90
        else:
            predicted_load = capacity * 0.70
        
        load_factor = predicted_load / capacity
        
        return {
            'route': route,
            'predicted_load': round(predicted_load),
            'current_bookings': 0,
            'capacity': capacity,
            'load_factor': load_factor,
            'status': "PREDICTED",
            'aircraft_type': aircraft_type
        }