import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Card, Button, Spinner, Alert } from "react-bootstrap";
import api from "../api";
import "./HomePage.css";

function HomePage() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [imageErrors, setImageErrors] = useState({});
  const navigate = useNavigate();

  const handleImageError = (e, restaurantId) => {
    console.log(`Image error for restaurant ${restaurantId}`);
    setImageErrors(prev => ({ ...prev, [restaurantId]: true }));
    // Set a simple colored div as fallback
    e.target.style.display = 'none';
    const fallback = e.target.nextSibling;
    if (fallback) {
      fallback.style.display = 'block';
    }
  };

  const getImageUrl = (restaurant) => {
    console.log(`Getting image for restaurant ${restaurant.id}:`, restaurant.image_url);
    // If image failed to load, return null to show fallback
    if (imageErrors[restaurant.id]) {
      return null;
    }
    // Use original image_url if available
    if (restaurant.image_url && restaurant.image_url.trim() !== '') {
      return restaurant.image_url;
    }
    // Return null to trigger fallback
    return null;
  };

  const getEmoji = (cuisine) => {
    const emojiMap = {
      'Italian': '🍕',
      'American': '🍔',
      'Japanese': '🍣',
      'Mexican': '🌮',
      'Indian': '🍛'
    };
    return emojiMap[cuisine] || '🍽️';
  };

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        setLoading(true);
        const response = await api.getRestaurants();
        console.log("Restaurants data:", response.data);
        setRestaurants(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch restaurants. Please try again.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRestaurants();
  }, []);

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading restaurants...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <div className="mb-5 text-center">
        <h1 className="display-4 fw-bold mb-3">🍔 Food Delivery Hub</h1>
        <p className="lead text-muted">Discover delicious restaurants near you</p>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row xs={1} md={2} lg={3} className="g-4">
        {restaurants.map((restaurant) => (
          <Col key={restaurant.id}>
            <Card className="restaurant-card h-100 shadow-sm hover-shadow">
              <div style={{ position: 'relative', height: '200px', overflow: 'hidden' }}>
                {getImageUrl(restaurant) && !imageErrors[restaurant.id] ? (
                  <img
                    src={getImageUrl(restaurant)}
                    alt={restaurant.name}
                    style={{
                      width: '100%',
                      height: '200px',
                      objectFit: 'cover',
                      display: 'block'
                    }}
                    onError={(e) => {
                      console.log('Image load error:', e.target.src);
                      handleImageError(e, restaurant.id);
                    }}
                  />
                ) : (
                  <div 
                    className="d-flex flex-column align-items-center justify-content-center"
                    style={{
                      width: '100%',
                      height: '200px',
                      backgroundColor: '#e9ecef',
                      fontSize: '64px',
                      color: '#6c757d'
                    }}
                  >
                    <div>{getEmoji(restaurant.cuisine)}</div>
                    <div style={{ fontSize: '14px', marginTop: '10px', fontWeight: 'bold' }}>{restaurant.name}</div>
                  </div>
                )}
              </div>
              <Card.Body className="d-flex flex-column">
                <Card.Title className="fw-bold">{restaurant.name}</Card.Title>
                <Card.Text className="text-muted mb-2">
                  <small>{restaurant.cuisine}</small>
                </Card.Text>
                <div className="mb-3">
                  <span className="badge bg-warning text-dark me-2">⭐ {restaurant.rating}</span>
                  <span className="badge bg-info text-white">⏱️ {restaurant.delivery_time} min</span>
                </div>
                <Button variant="primary" className="mt-auto" onClick={() => navigate(`/menu/${restaurant.id}`, { state: { restaurant } })}>
                  View Menu
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default HomePage;
