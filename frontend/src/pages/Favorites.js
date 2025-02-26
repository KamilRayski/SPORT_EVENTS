// src/pages/Favorites.js
import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);

  const fetchFavorites = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch("http://localhost:8000/favorites/", {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setFavorites(data);
      } else {
        console.error("Błąd pobierania ulubionych");
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, []);

  const removeFavorite = async (favoriteId) => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`http://localhost:8000/favorites/${favoriteId}/`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      if (res.ok) {
        fetchFavorites();
      } else {
        alert("Błąd usuwania ulubionego wydarzenia.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container style={{ marginTop: "40px" }}>
      <h2>Ulubione wydarzenia</h2>
      <Row>
        {favorites.length > 0 ? (
          favorites.map(fav => (
            <Col key={fav.id} md={4}>
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>{fav.event_title}</Card.Title>
                  <Card.Text>
                    Data: {new Date(fav.event_date).toLocaleString()}
                  </Card.Text>
                  <Button variant="danger" onClick={() => removeFavorite(fav.id)}>
                    Usuń z ulubionych
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <p>Brak ulubionych wydarzeń.</p>
        )}
      </Row>
    </Container>
  );
};

export default Favorites;
