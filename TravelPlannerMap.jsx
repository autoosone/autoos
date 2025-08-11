import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

/**
 * Travel Planner Map Component for Blaxel Trip Booking Agent
 * Similar to CopilotKit's travel planner example
 */
const TravelPlannerMap = ({ flights = [], hotels = [] }) => {
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [mapCenter, setMapCenter] = useState([40.7128, -74.0060]); // Default to NYC

  // Airport coordinates (example data - would come from your API)
  const airports = {
    'JFK': { name: 'John F. Kennedy', lat: 40.6413, lng: -73.7781, city: 'New York' },
    'LAX': { name: 'Los Angeles Intl', lat: 33.9425, lng: -118.4081, city: 'Los Angeles' },
    'ORD': { name: "O'Hare Intl", lat: 41.9742, lng: -87.9073, city: 'Chicago' },
    'LHR': { name: 'Heathrow', lat: 51.4700, lng: -0.4543, city: 'London' },
    'CDG': { name: 'Charles de Gaulle', lat: 49.0097, lng: 2.5479, city: 'Paris' },
    'NRT': { name: 'Narita', lat: 35.7720, lng: 140.3929, city: 'Tokyo' },
  };

  // Hotel data (example - would come from your agent)
  const hotelData = hotels.length > 0 ? hotels : [
    { id: 1, name: 'Hilton Manhattan', lat: 40.7614, lng: -73.9776, price: '$250/night', rating: 4.5 },
    { id: 2, name: 'Beverly Hills Hotel', lat: 34.0812, lng: -118.4134, price: '$450/night', rating: 4.8 },
    { id: 3, name: 'The Ritz London', lat: 51.5074, lng: -0.1419, price: '$600/night', rating: 4.9 },
  ];

  // Flight routes (example - would come from your agent)
  const flightRoutes = flights.length > 0 ? flights : [
    { id: 1, from: 'JFK', to: 'LAX', airline: 'United', price: '$350', duration: '5h 30m' },
    { id: 2, from: 'JFK', to: 'LHR', airline: 'British Airways', price: '$750', duration: '7h 15m' },
    { id: 3, from: 'LAX', to: 'NRT', airline: 'JAL', price: '$1200', duration: '11h 45m' },
  ];

  // Create custom icons
  const hotelIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const airportIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  return (
    <div style={{ display: 'flex', gap: '20px', height: '600px' }}>
      {/* Left Panel - Trip Details */}
      <div style={{ width: '300px', overflowY: 'auto', padding: '20px', background: '#f5f5f5', borderRadius: '8px' }}>
        <h2>🗺️ Travel Planner</h2>
        
        {/* Flights Section */}
        <div style={{ marginBottom: '20px' }}>
          <h3>✈️ Flights</h3>
          {flightRoutes.map(flight => (
            <div 
              key={flight.id}
              onClick={() => setSelectedFlight(flight)}
              style={{
                padding: '10px',
                margin: '5px 0',
                background: selectedFlight?.id === flight.id ? '#e3f2fd' : 'white',
                borderRadius: '4px',
                cursor: 'pointer',
                border: '1px solid #ddd'
              }}
            >
              <strong>{airports[flight.from].city} → {airports[flight.to].city}</strong>
              <div style={{ fontSize: '12px', color: '#666' }}>
                {flight.from} → {flight.to}
              </div>
              <div style={{ fontSize: '14px', marginTop: '5px' }}>
                {flight.airline} • {flight.price} • {flight.duration}
              </div>
            </div>
          ))}
        </div>

        {/* Hotels Section */}
        <div>
          <h3>🏨 Hotels</h3>
          {hotelData.map(hotel => (
            <div 
              key={hotel.id}
              onClick={() => setSelectedHotel(hotel)}
              style={{
                padding: '10px',
                margin: '5px 0',
                background: selectedHotel?.id === hotel.id ? '#e8f5e9' : 'white',
                borderRadius: '4px',
                cursor: 'pointer',
                border: '1px solid #ddd'
              }}
            >
              <strong>{hotel.name}</strong>
              <div style={{ fontSize: '14px', marginTop: '5px' }}>
                {hotel.price} • ⭐ {hotel.rating}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Right Panel - Map */}
      <div style={{ flex: 1, borderRadius: '8px', overflow: 'hidden' }}>
        <MapContainer 
          center={mapCenter} 
          zoom={2} 
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />

          {/* Airport Markers */}
          {Object.entries(airports).map(([code, airport]) => (
            <Marker 
              key={code}
              position={[airport.lat, airport.lng]}
              icon={airportIcon}
            >
              <Popup>
                <strong>{airport.name}</strong><br/>
                {airport.city} ({code})
              </Popup>
            </Marker>
          ))}

          {/* Hotel Markers */}
          {hotelData.map(hotel => (
            <Marker 
              key={hotel.id}
              position={[hotel.lat, hotel.lng]}
              icon={hotelIcon}
            >
              <Popup>
                <strong>{hotel.name}</strong><br/>
                {hotel.price}<br/>
                Rating: ⭐ {hotel.rating}
              </Popup>
            </Marker>
          ))}

          {/* Flight Routes */}
          {flightRoutes.map(flight => {
            const from = airports[flight.from];
            const to = airports[flight.to];
            return (
              <Polyline
                key={flight.id}
                positions={[
                  [from.lat, from.lng],
                  [to.lat, to.lng]
                ]}
                color={selectedFlight?.id === flight.id ? 'red' : 'blue'}
                weight={selectedFlight?.id === flight.id ? 3 : 2}
                opacity={0.7}
                dashArray={selectedFlight?.id === flight.id ? '' : '10, 10'}
              />
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
};

// Integration with Blaxel Agent
const TravelPlannerApp = () => {
  const [agentData, setAgentData] = useState({ flights: [], hotels: [] });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const API_KEY = 'bl_47yrrlxn6geic2wq9asrv5rapygyycj7';
  const ENDPOINT = 'https://run.blaxel.ai/amo/agents/template-copilot-kit-py';

  const searchTrips = async (query) => {
    setLoading(true);
    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ inputs: query })
      });

      const data = await response.json();
      // Parse agent response to extract flight and hotel data
      // This would need to be adapted based on your agent's response format
      console.log('Agent response:', data);
      
      // For demo, using mock data
      setAgentData({
        flights: [],
        hotels: []
      });
    } catch (error) {
      console.error('Error calling agent:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>🚀 Blaxel Travel Planner with Map</h1>
      
      {/* Search Bar */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="e.g., Book a flight from NYC to Paris and find hotels near Eiffel Tower"
          style={{
            flex: 1,
            padding: '12px',
            fontSize: '16px',
            border: '1px solid #ddd',
            borderRadius: '4px'
          }}
        />
        <button
          onClick={() => searchTrips(message)}
          disabled={loading}
          style={{
            padding: '12px 24px',
            background: '#007cba',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {loading ? 'Searching...' : 'Search Trips'}
        </button>
      </div>

      {/* Map Component */}
      <TravelPlannerMap 
        flights={agentData.flights} 
        hotels={agentData.hotels}
      />
    </div>
  );
};

export default TravelPlannerApp;