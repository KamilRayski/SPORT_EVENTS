import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import DatePicker from "react-datepicker";

const EventForm = ({ onSave }) => {
  const [title, setTitle] = useState("");
  const [address, setAddress] = useState("");
  const [date, setDate] = useState(new Date());
  const [capacity, setCapacity] = useState(10);
  const [creatorName, setCreatorName] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      title,
      address,
      date: date.toISOString(),
      capacity,
      creator_name: creatorName,
      latitude: parseFloat(latitude) || null,
      longitude: parseFloat(longitude) || null,
    });
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3">
        <Form.Label>Tytuł wydarzenia</Form.Label>
        <Form.Control
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Adres</Form.Label>
        <Form.Control
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Data</Form.Label>
        <br />
        <DatePicker
          selected={date}
          onChange={(val) => setDate(val)}
          showTimeSelect
          dateFormat="Pp"
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Ilość uczestników</Form.Label>
        <Form.Control
          type="number"
          min={1}
          value={capacity}
          onChange={(e) => setCapacity(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Twoje imię/nick (Organizator)</Form.Label>
        <Form.Control
          type="text"
          value={creatorName}
          onChange={(e) => setCreatorName(e.target.value)}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Współrzędne (opcjonalnie)</Form.Label>
        <Form.Control
          type="text"
          placeholder="Szerokość geo (lat)"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
        />
        <Form.Control
          type="text"
          placeholder="Długość geo (lng)"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
        />
      </Form.Group>

      <Button variant="primary" type="submit">
        Zapisz
      </Button>
    </Form>
  );
};

export default EventForm;
