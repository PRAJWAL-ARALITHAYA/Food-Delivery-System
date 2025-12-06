import React, { useState, useEffect } from "react";
import { Container, Table, Badge, Spinner, Alert, Card, Row, Col, ButtonGroup, Button } from "react-bootstrap";
import api from "../api";
import "./DeliveryStaffPage.css";

function DeliveryStaffPage() {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    fetchDeliveryStaff();
  }, [statusFilter]);

  const fetchDeliveryStaff = async () => {
    try {
      setLoading(true);
      const response =
        statusFilter === "all"
          ? await api.getDeliveryStaff()
          : await api.getDeliveryStaff(statusFilter);
      // Check if response has error
      if (response.data.error) {
        setError(response.data.error);
        setStaff([]);
      } else {
        setStaff(response.data);
        setError(null);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || "Failed to fetch delivery staff. Please try again.";
      setError(errorMessage);
      console.error("Error fetching delivery staff:", err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      Available: "success",
      Busy: "warning",
      Offline: "secondary",
    };
    return <Badge bg={variants[status] || "secondary"}>{status}</Badge>;
  };

  const getRatingBadge = (rating) => {
    if (rating >= 4.5) return <Badge bg="success">⭐ {rating}</Badge>;
    if (rating >= 4.0) return <Badge bg="info">⭐ {rating}</Badge>;
    return <Badge bg="warning">⭐ {rating}</Badge>;
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading delivery staff...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <h1 className="mb-5 fw-bold">🚚 Delivery Staff</h1>

      {error && (
        <Alert variant="danger">
          <Alert.Heading>Error Loading Delivery Staff</Alert.Heading>
          <p>{error}</p>
          {error.includes("does not exist") && (
            <div className="mt-3">
              <p className="mb-2"><strong>To fix this:</strong></p>
              <ol>
                <li>Open phpMyAdmin: <code>http://localhost/phpmyadmin</code></li>
                <li>Select <code>food_delivery</code> database</li>
                <li>Click "SQL" tab</li>
                <li>Copy and paste contents of <code>backend/migrate_database.sql</code></li>
                <li>Click "Go" to run the migration</li>
              </ol>
              <p className="mt-2">Or see <code>MIGRATION_GUIDE.md</code> for detailed instructions.</p>
            </div>
          )}
        </Alert>
      )}

      {/* Filter Buttons */}
      <div className="mb-4">
        <ButtonGroup>
          <Button
            variant={statusFilter === "all" ? "primary" : "outline-primary"}
            onClick={() => setStatusFilter("all")}
          >
            All Staff
          </Button>
          <Button
            variant={statusFilter === "Available" ? "success" : "outline-success"}
            onClick={() => setStatusFilter("Available")}
          >
            Available
          </Button>
          <Button
            variant={statusFilter === "Busy" ? "warning" : "outline-warning"}
            onClick={() => setStatusFilter("Busy")}
          >
            Busy
          </Button>
        </ButtonGroup>
      </div>

      {/* Summary Cards */}
      <Row className="mb-4">
        <Col md={4}>
          <Card className="text-center border-success">
            <Card.Body>
              <h3 className="text-success">
                {staff.filter((s) => s.status === "Available").length}
              </h3>
              <p className="text-muted mb-0">Available</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center border-warning">
            <Card.Body>
              <h3 className="text-warning">
                {staff.filter((s) => s.status === "Busy").length}
              </h3>
              <p className="text-muted mb-0">Busy</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center border-info">
            <Card.Body>
              <h3 className="text-info">
                {staff.reduce((sum, s) => sum + (s.total_deliveries || 0), 0)}
              </h3>
              <p className="text-muted mb-0">Total Deliveries</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {staff.length === 0 ? (
        <Alert variant="info">No delivery staff found.</Alert>
      ) : (
        <div className="table-responsive">
          <Table striped bordered hover className="delivery-staff-table">
            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Vehicle Type</th>
                <th>Status</th>
                <th>Rating</th>
                <th>Total Deliveries</th>
                <th>Joined Date</th>
              </tr>
            </thead>
            <tbody>
              {staff.map((member) => (
                <tr key={member.id}>
                  <td className="fw-bold">#{member.id}</td>
                  <td>
                    <strong>{member.name}</strong>
                  </td>
                  <td>
                    <a href={`tel:${member.phone}`}>{member.phone}</a>
                  </td>
                  <td>
                    {member.vehicle_type ? (
                      <Badge bg="info">{member.vehicle_type}</Badge>
                    ) : (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td>{getStatusBadge(member.status)}</td>
                  <td>{getRatingBadge(parseFloat(member.rating || 0))}</td>
                  <td>
                    <strong>{member.total_deliveries || 0}</strong>
                  </td>
                  <td className="text-muted">
                    <small>
                      {member.created_at
                        ? new Date(member.created_at).toLocaleDateString()
                        : "-"}
                    </small>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )}

      <div className="mt-5">
        <a href="/" className="btn btn-primary">
          ← Back to Home
        </a>
      </div>
    </Container>
  );
}

export default DeliveryStaffPage;

