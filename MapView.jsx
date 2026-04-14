/*import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

export default function MapView({ items }) {
  const center = items?.length ? [items[0].latitude, items[0].longitude] : [20.5937, 78.9629];

  return (
    <div className="rounded-3xl overflow-hidden border border-white/10">
      <MapContainer center={center} zoom={12} scrollWheelZoom={true} style={{ height: "380px", width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {items.map((item) => (
          <Marker key={item.id} position={[item.latitude, item.longitude]}>
            <Popup>
              <b>{item.name}</b><br />
              Wait: {item.waiting_time} min<br />
              Distance: {item.distance_km} km
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}*/
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";

function RecenterMap({ center }) {
  const map = useMap();

  useEffect(() => {
    if (center) {
      map.setView(center, 13);
    }
  }, [center]);

  return null;
}

export default function MapView({ items = [], userLocation = null }) {
  const center = userLocation
    ? userLocation
    : items.length
    ? [items[0].latitude, items[0].longitude]
    : [28.6139, 77.2090]; // default Delhi

  return (
    <MapContainer
      center={center}
      zoom={13}
      style={{ height: "400px", width: "100%" }}
    >
      <RecenterMap center={center} />

      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* User location */}
      {userLocation && (
        <Marker position={userLocation}>
          <Popup>You are here</Popup>
        </Marker>
      )}

      {/* Restaurants */}
      {items.map((item, idx) => (
        <Marker key={idx} position={[item.latitude, item.longitude]}>
          <Popup>
            <b>{item.name}</b><br />
            Wait: {item.waiting_time} min<br />
            Distance: {item.distance_km} km
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
