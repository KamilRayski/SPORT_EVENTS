// frontend/src/pages/EventDetails.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

function EventDetails() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [coords, setCoords] = useState(null);

  const fetchEvent = async () => {
    try {
      const res = await fetch(`http://localhost:8000/events/${id}`);
      const data = await res.json();
      setEvent(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchEvent();
  }, [id]);

  useEffect(() => {
    if (event?.address) {
      geocodeAddress(event.address);
    }
  }, [event]);

  const geocodeAddress = async (address) => {
    try {
      const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        address
      )}`;
      const res = await fetch(url, {
        headers: { "User-Agent": "MySportsApp/1.0" },
      });
      const data = await res.json();
      if (data && data.length > 0) {
        // Bierzemy pierwszy wynik
        setCoords({
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon),
        });
      }
    } catch (err) {
      console.error("Geocoding error:", err);
    }
  };

  if (!event) return <div>Ładowanie...</div>;

  const handleSignup = async () => {
    const userName = prompt("Twoje imię:");
    const userEmail = prompt("Twój email:");
    if (!userName || !userEmail) return;

    try {
      const res = await fetch(`http://localhost:8000/events/${id}/signups`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: userName, email: userEmail }),
      });
      if (res.ok) {
        alert("Zapisano pomyślnie!");
        fetchEvent();
      } else {
        const errData = await res.json();
        alert("Błąd: " + (errData.error || "???"));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const defaultIcon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    shadowUrl:
      "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  });
  L.Marker.prototype.options.icon = defaultIcon;

  const freeSpots =
    event.capacity - (event.signups_count || 0);

  return (
    <Container style={{ marginTop: 20 }}>
      <Row>
        <Col>
          <h2>{event.title}</h2>
          <p>
            <strong>Organizator:</strong>{" "}
            {event.creator_username} ({event.creator_email})
          </p>
          <p>
            <strong>Adres:</strong> {event.address}
          </p>
          <p>
            <strong>Data:</strong>{" "}
            {new Date(event.date).toLocaleString()}
          </p>
          <p>
            <strong>Wolne miejsca:</strong> {freeSpots} /{" "}
            {event.capacity}
          </p>
          <p>
            <strong>Opis:</strong> {event.description}
          </p>
          <Button variant="success" onClick={handleSignup}>
            Zapisz się
          </Button>
        </Col>
      </Row>

      {coords && (
        <Row style={{ marginTop: 20 }}>
          <Col>
            <MapContainer
              center={[coords.lat, coords.lng]}
              zoom={13}
              style={{ height: "300px", width: "100%" }}
            >
              <TileLayer
                attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={[coords.lat, coords.lng]}>
                <Popup>{event.title}</Popup>
              </Marker>
            </MapContainer>
          </Col>
        </Row>
      )}
    </Container>
  );
}

export default EventDetails;
