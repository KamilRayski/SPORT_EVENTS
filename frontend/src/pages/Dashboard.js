import React from "react";
import { Container, Row, Col } from "react-bootstrap";

function Dashboard() {
  return (
    <Container style={{ marginTop: 20 }}>
      <Row>
        <Col>
          <h2>Dashboard</h2>
          <p>Tu mogą być np. statystyki wydarzeń, liczba zapisanych osób itd.</p>
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
