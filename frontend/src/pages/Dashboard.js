import React, { useState } from "react";
import { Container, Row, Col, Button, Form, Card } from "react-bootstrap";

function Dashboard() {
  const [email, setEmail] = useState("");
  const [events, setEvents] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSearch = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch("http://localhost:8000/dashboard_events/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        const data = await res.json();
        setEvents(Array.isArray(data) ? data : data.events || []);
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
    <Container style={{ marginTop: "40px" }}>
      <h2>Dashboard</h2>
      <Card className="mb-4 p-3">
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Podaj email</Form.Label>
            <Form.Control
              type="email"
              placeholder="example@domain.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Form.Group>
          <Button onClick={handleSearch}>Szukaj</Button>
        </Form>
        {errorMsg && <p style={{ color: "red" }}>{errorMsg}</p>}
      </Card>
      <Row>
        {events.length > 0 ? (
          events.map((ev) => (
            <Col key={ev.event_id} md={4}>
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>{ev.title}</Card.Title>
                  <Card.Text>
                    <strong>Adres:</strong> {ev.address} <br />
                    <strong>Data:</strong> {new Date(ev.date).toLocaleString()}
                  </Card.Text>
                  <Card.Text>
                    <strong>Uczestnicy:</strong>
                    <ul>
                      {ev.signups.map((sign, idx) => (
                        <li key={idx}>
                          {sign.username} ({sign.email})
                        </li>
                      ))}
                    </ul>
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <p>Brak wyników</p>
        )}
      </Row>
    </Container>
  );
}

export default Dashboard;
