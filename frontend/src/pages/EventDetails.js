import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col, Button, Card } from "react-bootstrap";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

function EventDetails() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [coords, setCoords] = useState(null);

  const fetchEvent = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`http://localhost:8000/events/${id}/`, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setEvent(data);
      } else {
        console.error("Błąd pobierania szczegółów wydarzenia");
      }
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
        setCoords({
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon),
        });
      }
    } catch (err) {
      console.error("Geocoding error:", err);
    }
  };

  const handleSignup = async () => {
    const userName = prompt("Twoje imię:");
    const userEmail = prompt("Twój email:");
    if (!userName || !userEmail) return;
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`http://localhost:8000/events/${id}/signups/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
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
    shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  });
  L.Marker.prototype.options.icon = defaultIcon;

  if (!event) return <div>Ładowanie...</div>;

  const freeSpots = event.capacity - (event.signups_count || 0);

  return (
    <Container style={{ marginTop: "40px" }}>
      <Row>
        <Col md={8}>
          <Card>
            <Card.Body>
              <Card.Title>{event.title}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                {new Date(event.date).toLocaleString()}
              </Card.Subtitle>
              <Card.Text>
                <strong>Organizator:</strong> {event.creator_username} ({event.creator_email})
              </Card.Text>
              <Card.Text>
                <strong>Adres:</strong> {event.address}
              </Card.Text>
              <Card.Text>
                <strong>Opis:</strong> {event.description}
              </Card.Text>
              <Card.Text>
                <strong>Wolne miejsca:</strong> {freeSpots} / {event.capacity}
              </Card.Text>
              <Button variant="success" onClick={handleSignup}>Zapisz się</Button>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          {coords && (
            <MapContainer center={[coords.lat, coords.lng]} zoom={13} style={{ height: "300px", width: "100%" }}>
              <TileLayer
                attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={[coords.lat, coords.lng]}>
                <Popup>{event.title}</Popup>
              </Marker>
            </MapContainer>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default EventDetails;
