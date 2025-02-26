// src/pages/Home.js
import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form } from "react-bootstrap";
import EventCard from "../components/EventCard";
import EventForm from "../components/EventForm";

const Home = () => {
  const [events, setEvents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const fetchEvents = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch("http://localhost:8000/events/", {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        // Możesz obsłużyć błąd 401, np. przekierować do logowania
        console.error("Brak autoryzacji!");
        return;
      }
      const data = await res.json();
      setEvents(Array.isArray(data) ? data : data.events || []);
    } catch (err) {
      console.error(err);
    }
  };
  

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleCreateEvent = async (eventData) => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("Musisz być zalogowany, aby tworzyć wydarzenia!");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/events/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
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

  const filteredEvents = events.filter(event =>
    event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (event.description && event.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <>
      <div
        style={{
          backgroundImage: "url('/hero-bg.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          color: "white",
          padding: "100px 0",
          textAlign: "center",
        }}
      >
        <Container>
          <h1>Welcome to Sport Events</h1>
          <p>Organizuj i uczestnicz w najlepszych wydarzeniach sportowych!</p>
          <Button variant="light" onClick={() => setShowForm(!showForm)}>
            {showForm ? "Schowaj formularz" : "Utwórz nowe wydarzenie"}
          </Button>
        </Container>
      </div>
      <Container style={{ marginTop: "40px" }}>
        <Form className="mb-4">
          <Form.Control
            type="text"
            placeholder="Wyszukaj wydarzenia..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </Form>
        {showForm && (
          <Row className="mb-4">
            <Col>
              <EventForm onSave={handleCreateEvent} />
            </Col>
          </Row>
        )}
        <Row>
          {filteredEvents.length ? (
            filteredEvents.map((event) => (
              <Col key={event.id} md={4}>
                <EventCard event={event} />
              </Col>
            ))
          ) : (
            <p>Brak wydarzeń do wyświetlenia</p>
          )}
        </Row>
      </Container>
    </>
  );
};

export default Home;
