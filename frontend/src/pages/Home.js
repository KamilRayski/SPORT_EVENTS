// frontend/src/pages/Home.js
import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import EventForm from "../components/EventForm";

function Home() {
  const [events, setEvents] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const fetchEvents = async () => {
    try {
      const res = await fetch("http://localhost:8000/events/");
      const data = await res.json();
      setEvents(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleCreateEvent = async (eventData) => {
    try {
      const res = await fetch("http://localhost:8000/events/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData),
      });
      if (res.ok) {
        alert("Wydarzenie utworzone!");
        setShowForm(false);
        fetchEvents();
      } else {
        const errData = await res.json();
        alert("Błąd tworzenia wydarzenia: " + (errData.error || "???"));
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container style={{ marginTop: 20 }}>
      <Row>
        <Col>
          <h2>Lista wydarzeń</h2>
          <Button variant="primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? "Schowaj formularz" : "Nowe wydarzenie"}
          </Button>

          {showForm && (
            <div style={{ marginTop: 20 }}>
              <EventForm onSave={handleCreateEvent} />
            </div>
          )}

          <ul style={{ marginTop: 20 }}>
            {events.map((ev) => (
              <li key={ev.id}>
                <a href={`/events/${ev.id}`}>{ev.title}</a> — {ev.address}
                {" | "}Organizator:{" "}
                {ev.creator_username
                  ? `${ev.creator_username} (${ev.creator_email})`
                  : "Brak"}
              </li>
            ))}
          </ul>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
