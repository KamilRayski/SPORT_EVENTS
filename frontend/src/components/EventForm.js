import React, { useState } from "react";
import { Form, Button, Card } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const EventForm = ({ onSave }) => {
  const [title, setTitle] = useState("");
  const [address, setAddress] = useState("");
  const [date, setDate] = useState(new Date());
  const [capacity, setCapacity] = useState(10);
  const [creatorName, setCreatorName] = useState("");
  const [creatorEmail, setCreatorEmail] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      title,
      address,
      date: date.toISOString(),
      capacity,
      creator_name: creatorName,
      creator_email: creatorEmail,
      description,
    });
  };

  return (
    <Card className="p-3 mb-4">
      <h3>Nowe wydarzenie</h3>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Tytuł wydarzenia</Form.Label>
          <Form.Control
            type="text"
            placeholder="Wprowadź tytuł"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Adres</Form.Label>
          <Form.Control
            type="text"
            placeholder="Wprowadź adres"
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
            className="form-control"
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
          <Form.Label>Organizator - nazwa</Form.Label>
          <Form.Control
            type="text"
            placeholder="Wprowadź nazwę organizatora"
            value={creatorName}
            onChange={(e) => setCreatorName(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Organizator - email</Form.Label>
          <Form.Control
            type="email"
            placeholder="Wprowadź email organizatora"
            value={creatorEmail}
            onChange={(e) => setCreatorEmail(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Opis wydarzenia</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder="Wprowadź opis wydarzenia"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Zapisz
        </Button>
      </Form>
    </Card>
  );
};

export default EventForm;
