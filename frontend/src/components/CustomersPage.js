import React, { useState, useEffect } from "react";
import { Container, Table, Badge, Spinner, Alert, Card, Row, Col } from "react-bootstrap";
import api from "../api";
import "./CustomersPage.css";

function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchCustomers();
    fetchStats();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await api.getCustomers();
      // Check if response has error
      if (response.data.error) {
        setError(response.data.error);
        setCustomers([]);
      } else {
        setCustomers(response.data);
        setError(null);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || "Failed to fetch customers. Please try again.";
      setError(errorMessage);
      console.error("Error fetching customers:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.getSummaryReport();
      setStats(response.data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    }
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading customers...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <h1 className="mb-5 fw-bold">👥 Customers</h1>

      {error && (
        <Alert variant="danger">
          <Alert.Heading>Error Loading Customers</Alert.Heading>
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

      {stats && (
        <Row className="mb-4">
          <Col md={3}>
            <Card className="text-center">
              <Card.Body>
                <h3 className="text-primary">{stats.total_customers}</h3>
                <p className="text-muted mb-0">Total Customers</p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="text-center">
              <Card.Body>
                <h3 className="text-success">{stats.total_orders}</h3>
                <p className="text-muted mb-0">Total Orders</p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="text-center">
              <Card.Body>
                <h3 className="text-info">₹{parseFloat(stats.total_revenue || 0).toFixed(2)}</h3>
                <p className="text-muted mb-0">Total Revenue</p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3}>
            <Card className="text-center">
              <Card.Body>
                <h3 className="text-warning">₹{parseFloat(stats.avg_order_value || 0).toFixed(2)}</h3>
                <p className="text-muted mb-0">Avg Order Value</p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {customers.length === 0 ? (
        <Alert variant="info">No customers found.</Alert>
      ) : (
        <div className="table-responsive">
          <Table striped bordered hover className="customers-table">
            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Address</th>
                <th>City</th>
                <th>Joined Date</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td className="fw-bold">#{customer.id}</td>
                  <td>
                    <strong>{customer.name}</strong>
                  </td>
                  <td>
                    <a href={`mailto:${customer.email}`}>{customer.email}</a>
                  </td>
                  <td>{customer.phone || <span className="text-muted">-</span>}</td>
                  <td>{customer.address || <span className="text-muted">-</span>}</td>
                  <td>
                    {customer.city ? (
                      <Badge bg="secondary">{customer.city}</Badge>
                    ) : (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td className="text-muted">
                    <small>
                      {customer.created_at
                        ? new Date(customer.created_at).toLocaleDateString()
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

export default CustomersPage;

