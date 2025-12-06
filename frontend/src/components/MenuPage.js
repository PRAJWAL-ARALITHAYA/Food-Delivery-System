import React, { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { Container, Row, Col, Card, Button, Modal, Form, Alert, Spinner } from "react-bootstrap";
import api from "../api";
import "./MenuPage.css";

function MenuPage() {
  const { restaurantId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const restaurant = location.state?.restaurant || {};

  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cart, setCart] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [orderLoading, setOrderLoading] = useState(false);
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: ''
  });
  const [showCustomerForm, setShowCustomerForm] = useState(false);
  const [imageErrors, setImageErrors] = useState({});

  const handleImageError = (e, itemId) => {
    console.log(`Image error for menu item ${itemId}`);
    setImageErrors(prev => ({ ...prev, [itemId]: true }));
    e.target.style.display = 'none';
  };

  const getImageUrl = (item) => {
    if (imageErrors[item.id]) {
      return null;
    }
    if (item.image_url && item.image_url.trim() !== '') {
      return item.image_url;
    }
    return null;
  };

  useEffect(() => {
    const fetchMenuItems = async () => {
      try {
        setLoading(true);
        const response = await api.getMenuItems(restaurantId);
        setMenuItems(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch menu items. Please try again.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMenuItems();
  }, [restaurantId]);

  const handleAddToCart = (item) => {
    setCart((prev) => ({
      ...prev,
      [item.id]: (prev[item.id] || 0) + 1,
    }));
  };

  const handleRemoveFromCart = (itemId) => {
    setCart((prev) => {
      const newCart = { ...prev };
      if (newCart[itemId] > 1) {
        newCart[itemId] -= 1;
      } else {
        delete newCart[itemId];
      }
      return newCart;
    });
  };

  const calculateTotal = () => {
    return Object.entries(cart).reduce((total, [itemId, quantity]) => {
      const item = menuItems.find((mi) => mi.id === parseInt(itemId));
      return total + (item ? parseFloat(item.price || 0) * quantity : 0);
    }, 0);
  };

  const handleProceedToCheckout = () => {
    if (Object.keys(cart).length === 0) {
      alert("Please add items to your cart");
      return;
    }
    // Show customer form first
    setShowCustomerForm(true);
    setShowModal(true);
  };

  const handlePlaceOrder = async () => {
    if (!customerInfo.name.trim()) {
      alert("Please enter your name");
      return;
    }

    try {
      setOrderLoading(true);
      
      // Find or create customer
      const customerResponse = await api.findOrCreateCustomer(customerInfo);
      const customerId = customerResponse.data.id;
      
      const orderItems = Object.entries(cart).map(([itemId, quantity]) => ({
        menu_item_id: parseInt(itemId),
        quantity,
      }));

      const response = await api.createOrder({
        customer_id: customerId,
        restaurant_id: parseInt(restaurantId),
        items: orderItems,
        total_price: calculateTotal(),
        delivery_address: customerInfo.address,
        payment_method: 'Cash'
      });

      if (response.status === 201) {
        alert("Order placed successfully!");
        setCart({});
        setShowModal(false);
        setShowCustomerForm(false);
        setCustomerInfo({ name: '', email: '', phone: '', address: '', city: '' });
        setTimeout(() => navigate("/orders"), 500);
      }
    } catch (err) {
      alert("Failed to place order. Please try again.");
      console.error(err);
    } finally {
      setOrderLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading menu...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <Button variant="secondary" className="mb-4" onClick={() => navigate("/")}>
        ← Back to Restaurants
      </Button>

      <div className="mb-5">
        <h2 className="fw-bold mb-2">{restaurant.name}</h2>
        <p className="text-muted">
          {restaurant.cuisine} • ⭐ {restaurant.rating} • ⏱️ {restaurant.delivery_time} min
        </p>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row xs={1} md={2} lg={3} className="g-4 mb-5">
        {menuItems.map((item) => (
          <Col key={item.id}>
            <Card className="menu-card h-100 shadow-sm">
              <div style={{ position: 'relative', height: '200px', overflow: 'hidden' }}>
                {getImageUrl(item) && !imageErrors[item.id] ? (
                  <img
                    src={getImageUrl(item)}
                    alt={item.name}
                    style={{
                      width: '100%',
                      height: '200px',
                      objectFit: 'cover',
                      display: 'block'
                    }}
                    onError={(e) => {
                      console.log('Image load error:', e.target.src);
                      handleImageError(e, item.id);
                    }}
                  />
                ) : (
                  <div 
                    className="d-flex align-items-center justify-content-center"
                    style={{
                      width: '100%',
                      height: '200px',
                      backgroundColor: '#e9ecef',
                      fontSize: '48px'
                    }}
                  >
                    🍽️
                  </div>
                )}
              </div>
              <Card.Body className="d-flex flex-column">
                <Card.Title className="fw-bold">{item.name}</Card.Title>
                <Card.Text className="text-muted flex-grow-1">
                  <small>{item.description}</small>
                </Card.Text>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="fw-bold text-primary">₹{parseFloat(item.price || 0).toFixed(2)}</span>
                  {cart[item.id] ? (
                    <div className="btn-group" role="group">
                      <Button variant="outline-danger" size="sm" onClick={() => handleRemoveFromCart(item.id)}>
                        -
                      </Button>
                      <span className="px-2 py-1">{cart[item.id]}</span>
                      <Button variant="outline-success" size="sm" onClick={() => handleAddToCart(item)}>
                        +
                      </Button>
                    </div>
                  ) : (
                    <Button variant="outline-primary" size="sm" onClick={() => handleAddToCart(item)}>
                      Add to Cart
                    </Button>
                  )}
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {Object.keys(cart).length > 0 && (
        <div className="sticky-bottom bg-white border-top p-3">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <span className="me-3">Items in cart: {Object.values(cart).reduce((a, b) => a + b, 0)}</span>
              <span className="fw-bold">Total: ₹{calculateTotal().toFixed(2)}</span>
            </div>
            <Button variant="success" size="lg" onClick={handleProceedToCheckout}>
              Proceed to Checkout
            </Button>
          </div>
        </div>
      )}

      <Modal show={showModal} onHide={() => {
        setShowModal(false);
        setShowCustomerForm(false);
      }} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {showCustomerForm ? "Customer Information" : "Review Your Order"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {showCustomerForm ? (
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Name <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter your name"
                  value={customerInfo.name}
                  onChange={(e) => setCustomerInfo({ ...customerInfo, name: e.target.value })}
                  required
                />
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Enter your email (optional)"
                  value={customerInfo.email}
                  onChange={(e) => setCustomerInfo({ ...customerInfo, email: e.target.value })}
                />
                <Form.Text className="text-muted">
                  If you've ordered before, we'll update your information
                </Form.Text>
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>Phone</Form.Label>
                <Form.Control
                  type="tel"
                  placeholder="Enter your phone number"
                  value={customerInfo.phone}
                  onChange={(e) => setCustomerInfo({ ...customerInfo, phone: e.target.value })}
                />
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>Delivery Address</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter delivery address"
                  value={customerInfo.address}
                  onChange={(e) => setCustomerInfo({ ...customerInfo, address: e.target.value })}
                />
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>City</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter your city"
                  value={customerInfo.city}
                  onChange={(e) => setCustomerInfo({ ...customerInfo, city: e.target.value })}
                />
              </Form.Group>
            </Form>
          ) : (
            <div className="mb-3">
              <h6 className="fw-bold mb-3">Order Summary</h6>
              {Object.entries(cart).map(([itemId, quantity]) => {
                const item = menuItems.find((mi) => mi.id === parseInt(itemId));
                return (
                  <div key={itemId} className="d-flex justify-content-between mb-2">
                    <span>
                      {item?.name} x {quantity}
                    </span>
                    <span>₹{(parseFloat(item?.price || 0) * quantity).toFixed(2)}</span>
                  </div>
                );
              })}
              <hr />
              <div className="d-flex justify-content-between fw-bold">
                <span>Total</span>
                <span>₹{calculateTotal().toFixed(2)}</span>
              </div>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => {
            setShowModal(false);
            setShowCustomerForm(false);
          }}>
            Cancel
          </Button>
          {showCustomerForm ? (
            <Button variant="primary" onClick={() => setShowCustomerForm(false)}>
              Continue to Review
            </Button>
          ) : (
            <Button variant="success" onClick={handlePlaceOrder} disabled={orderLoading}>
              {orderLoading ? "Placing Order..." : "Place Order"}
            </Button>
          )}
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

export default MenuPage;
