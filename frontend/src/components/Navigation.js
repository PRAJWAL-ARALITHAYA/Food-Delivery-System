import React from "react";
import { Navbar, Nav, Container, NavDropdown } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./Navigation.css";

function Navigation() {
  return (
    <Navbar bg="dark" data-bs-theme="dark" sticky="top" expand="lg" className="navbar-shadow">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold fs-5">
          🍕 FoodHub
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/">
              Home
            </Nav.Link>
            <Nav.Link as={Link} to="/orders">
              My Orders
            </Nav.Link>
            <NavDropdown title="Manage" id="manage-dropdown">
              <NavDropdown.Item as={Link} to="/customers">
                👥 Customers
              </NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/delivery-staff">
                🚚 Delivery Staff
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;
