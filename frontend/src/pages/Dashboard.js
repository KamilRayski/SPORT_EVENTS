// frontend/src/pages/Dashboard.js
import React, { useState } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";

function Dashboard() {
  const [email, setEmail] = useState("");
  const [events, setEvents] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSearch = async () => {
    try {
      const res = await fetch("http://localhost:8000/dashboard_events/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        const data = await res.json();
        setEvents(data);
        setErrorMsg("");
      } else {
        const errData = await res.json();
        setEvents([]);
        setErrorMsg(errData.error || "Nieznany błąd");
      }
    } catch (err) {
      console.error(err);
      setEvents([]);
      setErrorMsg("Błąd sieci lub serwera.");
    }
  };

  return (
    <Container style={{ marginTop: 20 }}>
      <Row>
        <Col>
          <h2>Dashboard</h2>
          <p>
            Wpisz email, aby zobaczyć wydarzenia utworzone przez danego
            użytkownika i listę zapisanych uczestników.
          </p>
          <input
            type="text"
            placeholder="Podaj email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ marginRight: 5 }}
          />
          <Button onClick={handleSearch}>Szukaj</Button>
          {errorMsg && <p style={{ color: "red" }}>{errorMsg}</p>}
        </Col>
      </Row>
      <Row>
        <Col>
          {events.map((ev) => (
            <div
              key={ev.event_id}
              style={{ border: "1px solid #ccc", marginTop: 10, padding: 10 }}
            >
              <h4>{ev.title}</h4>
              <p>Adres: {ev.address}</p>
              <p>Data: {new Date(ev.date).toLocaleString()}</p>
              <p>Pojemność: {ev.capacity}</p>
              <p>Opis: {ev.description}</p>
              <p>Uczestnicy:</p>
              <ul>
                {ev.signups.map((sign, idx) => (
                  <li key={idx}>
                    {sign.username} ({sign.email})
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
