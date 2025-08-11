"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";
import dynamic from 'next/dynamic';
import "@copilotkit/react-ui/styles.css";
import "leaflet/dist/leaflet.css";

// Dynamically import TravelMap to avoid SSR issues
const TravelMap = dynamic(() => import('./components/TravelMap'), { 
  ssr: false,
  loading: () => <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
    <div className="text-gray-500">Loading travel map...</div>
  </div>
});

interface Trip {
  id: string;
  name: string;
  destination: string;
  flights: any[];
  hotels: any[];
}

function TravelPlannerContent() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [currentTrip, setCurrentTrip] = useState<Trip | null>(null);
  // Make trips readable by the agent
  useCopilotReadable({
    name: "trips",
    value: trips,
    description: "List of all planned trips with flights and hotels",
  });

  useCopilotReadable({
    name: "current_trip",
    value: currentTrip,
    description: "Currently selected trip being viewed on the map",
  });

  // Allow the agent to create new trips
  useCopilotAction({
    name: "create_trip",
    description: "Create a new travel trip with destination and details",
    parameters: [
      {
        name: "destination",
        type: "string",
        description: "The destination city or country for the trip",
      },
      {
        name: "tripName",
        type: "string", 
        description: "A descriptive name for the trip",
      }
    ],    handler: async ({ destination, tripName }) => {
      const newTrip: Trip = {
        id: Date.now().toString(),
        name: tripName || `Trip to ${destination}`,
        destination,
        flights: [],
        hotels: [],
      };
      
      setTrips(prev => [...prev, newTrip]);
      setCurrentTrip(newTrip);
      
      return `Created new trip: ${newTrip.name}. You can now add flights and hotels to this trip.`;
    },
  });

  // Allow the agent to update trip details
  useCopilotAction({
    name: "add_flight_to_trip",
    description: "Add a flight to the current trip",
    parameters: [
      {
        name: "from",
        type: "string",
        description: "Departure airport code (e.g., JFK, LAX)",
      },
      {
        name: "to", 
        type: "string",
        description: "Arrival airport code (e.g., CDG, NRT)",      },
      {
        name: "airline",
        type: "string",
        description: "Airline name",
      },
      {
        name: "price",
        type: "string", 
        description: "Flight price (e.g., $350)",
      }
    ],
    handler: async ({ from, to, airline, price }) => {
      if (!currentTrip) {
        return "Please create a trip first before adding flights.";
      }

      const newFlight = {
        id: Date.now(),
        from,
        to, 
        airline,
        price,
        duration: "TBD",
      };

      const updatedTrip = {
        ...currentTrip,
        flights: [...currentTrip.flights, newFlight],
      };
      setCurrentTrip(updatedTrip);
      setTrips(prev => prev.map(trip => 
        trip.id === currentTrip.id ? updatedTrip : trip
      ));

      return `Added ${airline} flight from ${from} to ${to} (${price}) to your ${currentTrip.name}.`;
    },
  });

  return (
    <div className="flex h-screen bg-gray-50">
      <div className="flex-1 flex flex-col">
        <header className="bg-white shadow-sm p-4 border-b">
          <h1 className="text-2xl font-bold text-gray-800">
            🗺️ Travel Planner
          </h1>
          <p className="text-gray-600">
            Plan trips, book flights & hotels with your AI travel assistant
          </p>
        </header>
        
        <div className="flex-1 flex">
          <div className="flex-1 p-6">
            <div className="bg-white rounded-lg shadow-sm p-6 h-full flex flex-col">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Interactive Travel Map</h2>
                {currentTrip && (
                  <div className="text-sm text-gray-600">
                    Current Trip: <span className="font-medium">{currentTrip.name}</span>                  </div>
                )}
              </div>
              
              <div className="flex-1">
                <TravelMap 
                  flights={currentTrip?.flights || []}
                  hotels={currentTrip?.hotels || []}
                />
              </div>
              
              {trips.length === 0 && (
                <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                  <p className="text-blue-800 text-sm">
                    💡 <strong>Try saying:</strong> "Plan a trip to Paris" or "Create a trip to Tokyo"
                  </p>
                </div>
              )}
            </div>
          </div>
          
          <div className="w-96 border-l bg-white">
            <CopilotChat
              labels={{
                title: "Travel Assistant",
                initial: "Hi! I'm your travel assistant. I can help you plan trips, book flights and hotels, and show everything on the interactive map. Where would you like to go?",
              }}
            />
          </div>
        </div>      </div>
    </div>
  );
}

// Main component with CopilotKit wrapper at the top level
export default function TravelPlanner() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <TravelPlannerContent />
    </CopilotKit>
  );
}