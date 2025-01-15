import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import EventDetails from "./pages/EventDetails";


function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: 10, background: "#eee" }}>
        <Link to="/" style={{ marginRight: 10 }}>Home</Link>
        <Link to="/dashboard" style={{ marginRight: 10 }}>Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/events/:id" element={<EventDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
