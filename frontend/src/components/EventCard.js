// src/components/EventCard.js
import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const EventCard = ({ event, onFavoriteAdded }) => {
  const token = localStorage.getItem("accessToken");

  const addToFavorites = async () => {
    if (!token) {
      alert("Musisz być zalogowany, aby dodawać ulubione wydarzenia!");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/favorites/add/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ event_id: event.id }),
      });
      if (res.ok) {
        alert("Dodano do ulubionych!");
        if (onFavoriteAdded) onFavoriteAdded();
      } else {
        const data = await res.json();
        alert("Błąd: " + (data.error || "nieznany błąd"));
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Card style={{ marginBottom: '20px' }}>
      <Card.Body>
        <Card.Title>{event.title}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          {new Date(event.date).toLocaleString()}
        </Card.Subtitle>
        <Card.Text>
          {event.description ? event.description.substring(0, 100) + '...' : 'Brak opisu'}
        </Card.Text>
        <Button variant="primary" as={Link} to={`/events/${event.id}`}>
          Zobacz szczegóły
        </Button>
        {token && (
          <Button variant="warning" onClick={addToFavorites} style={{ marginLeft: "10px" }}>
            Dodaj do ulubionych
          </Button>
        )}
      </Card.Body>
    </Card>
  );
};

export default EventCard;
