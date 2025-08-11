"use client";

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import to avoid SSR issues with Leaflet
const MapContainer = dynamic(() => import('react-leaflet').then(mod => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then(mod => mod.TileLayer), { ssr: false });
const Marker = dynamic(() => import('react-leaflet').then(mod => mod.Marker), { ssr: false });
const Popup = dynamic(() => import('react-leaflet').then(mod => mod.Popup), { ssr: false });
const Polyline = dynamic(() => import('react-leaflet').then(mod => mod.Polyline), { ssr: false });

interface Airport {
  name: string;
  lat: number;
  lng: number;
  city: string;
}

interface Flight {
  id: number;
  from: string;
  to: string;
  airline: string;
  price: string;
  duration: string;
}

interface Hotel {
  id: number;
  name: string;
  lat: number;
  lng: number;
  price: string;
  rating: number;
}

interface TravelMapProps {
  flights?: Flight[];
  hotels?: Hotel[];
}

export default function TravelMap({ flights = [], hotels = [] }: TravelMapProps) {
  const [isClient, setIsClient] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [selectedHotel, setSelectedHotel] = useState<Hotel | null>(null);

  useEffect(() => {
    setIsClient(true);
  }, []);

  // Airport coordinates
  const airports: Record<string, Airport> = {
    'JFK': { name: 'John F. Kennedy', lat: 40.6413, lng: -73.7781, city: 'New York' },
    'LAX': { name: 'Los Angeles Intl', lat: 33.9425, lng: -118.4081, city: 'Los Angeles' },
    'ORD': { name: "O'Hare Intl", lat: 41.9742, lng: -87.9073, city: 'Chicago' },
    'LHR': { name: 'Heathrow', lat: 51.4700, lng: -0.4543, city: 'London' },
    'CDG': { name: 'Charles de Gaulle', lat: 49.0097, lng: 2.5479, city: 'Paris' },
    'NRT': { name: 'Narita', lat: 35.7720, lng: 140.3929, city: 'Tokyo' },
  };

  // Demo data
  const flightRoutes: Flight[] = flights.length > 0 ? flights : [
    { id: 1, from: 'JFK', to: 'LAX', airline: 'United', price: '$350', duration: '5h 30m' },
    { id: 2, from: 'JFK', to: 'LHR', airline: 'British Airways', price: '$750', duration: '7h 15m' },
    { id: 3, from: 'LAX', to: 'NRT', airline: 'JAL', price: '$1200', duration: '11h 45m' },
  ];

  const hotelData: Hotel[] = hotels.length > 0 ? hotels : [
    { id: 1, name: 'Hilton Manhattan', lat: 40.7614, lng: -73.9776, price: '$250/night', rating: 4.5 },
    { id: 2, name: 'Beverly Hills Hotel', lat: 34.0812, lng: -118.4134, price: '$450/night', rating: 4.8 },
    { id: 3, name: 'The Ritz London', lat: 51.5074, lng: -0.1419, price: '$600/night', rating: 4.9 },
  ];

  if (!isClient) {
    return (
      <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-gray-500">Loading map...</div>
      </div>
    );
  }

  return (
    <div className="flex gap-4 h-96">
      {/* Left Panel - Trip Details */}
      <div className="w-72 overflow-y-auto p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">🗺️ Trip Details</h3>
        
        {/* Flights Section */}
        <div className="mb-6">
          <h4 className="font-medium mb-2">✈️ Flights</h4>
          {flightRoutes.map(flight => (
            <div
              key={flight.id}
              onClick={() => setSelectedFlight(flight)}
              className={`p-3 mb-2 rounded cursor-pointer border transition-colors ${
                selectedFlight?.id === flight.id 
                  ? 'bg-blue-100 border-blue-300' 
                  : 'bg-white border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="font-medium">
                {airports[flight.from]?.city} → {airports[flight.to]?.city}
              </div>
              <div className="text-xs text-gray-600">
                {flight.from} → {flight.to}
              </div>
              <div className="text-sm mt-1">
                {flight.airline} • {flight.price} • {flight.duration}
              </div>
            </div>
          ))}
        </div>

        {/* Hotels Section */}
        <div>
          <h4 className="font-medium mb-2">🏨 Hotels</h4>
          {hotelData.map(hotel => (
            <div
              key={hotel.id}
              onClick={() => setSelectedHotel(hotel)}
              className={`p-3 mb-2 rounded cursor-pointer border transition-colors ${
                selectedHotel?.id === hotel.id 
                  ? 'bg-green-100 border-green-300' 
                  : 'bg-white border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="font-medium">{hotel.name}</div>
              <div className="text-sm mt-1">
                {hotel.price} • ⭐ {hotel.rating}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Right Panel - Map */}
      <div className="flex-1 rounded-lg overflow-hidden">
        <MapContainer
          center={[40.7128, -74.0060]}
          zoom={2}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />
          
          {/* Flight Routes */}
          {flightRoutes.map(flight => {
            const from = airports[flight.from];
            const to = airports[flight.to];
            if (!from || !to) return null;
            
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
              />
            );
          })}

          {/* Airport Markers */}
          {Object.entries(airports).map(([code, airport]) => (
            <Marker key={code} position={[airport.lat, airport.lng]}>
              <Popup>
                <strong>{airport.name}</strong><br/>
                {airport.city} ({code})
              </Popup>
            </Marker>
          ))}

          {/* Hotel Markers */}
          {hotelData.map(hotel => (
            <Marker key={hotel.id} position={[hotel.lat, hotel.lng]}>
              <Popup>
                <strong>{hotel.name}</strong><br/>
                {hotel.price}<br/>
                Rating: ⭐ {hotel.rating}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}