import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => (
  <footer style={{ backgroundColor: '#343a40', color: '#fff', padding: '20px 0', marginTop: '20px' }}>
    <Container className="text-center">
      <p>&copy; {new Date().getFullYear()} Sport Events. All rights reserved.</p>
    </Container>
  </footer>
);

export default Footer;
