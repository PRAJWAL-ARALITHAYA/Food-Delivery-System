import React, { useState, useEffect } from "react";
import { Container, Table, Button, Badge, Spinner, Alert, Modal, Form } from "react-bootstrap";
import api from "../api";
import "./OrdersPage.css";

function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showItemsModal, setShowItemsModal] = useState(false);
  const [selectedOrderForItems, setSelectedOrderForItems] = useState(null);
  const [orderDetails, setOrderDetails] = useState(null);
  const [availableMenuItems, setAvailableMenuItems] = useState([]);
  const [selectedMenuItemId, setSelectedMenuItemId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [loadingItems, setLoadingItems] = useState(false);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await api.getOrders();
      setOrders(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch orders. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteOrder = async (orderId) => {
    if (window.confirm("Are you sure you want to delete this order?")) {
      try {
        await api.deleteOrder(orderId);
        setOrders(orders.filter((o) => o.id !== orderId));
        alert("Order deleted successfully!");
      } catch (err) {
        alert("Failed to delete order. Please try again.");
        console.error(err);
      }
    }
  };

  const handleManageItems = async (order) => {
    try {
      setLoadingItems(true);
      setSelectedOrderForItems(order);

      // Fetch order details with items
      const orderResponse = await api.getOrder(order.id);
      setOrderDetails(orderResponse.data);

      // Fetch menu items for the restaurant
      const menuResponse = await api.getMenuItems(order.restaurant_id);
      setAvailableMenuItems(menuResponse.data);

      setShowItemsModal(true);
      setSelectedMenuItemId("");
      setQuantity(1);
    } catch (err) {
      alert("Failed to load order items. Please try again.");
      console.error(err);
    } finally {
      setLoadingItems(false);
    }
  };

  const handleAddItem = async () => {
    if (!selectedMenuItemId) {
      alert("Please select a menu item");
      return;
    }

    try {
      const response = await api.addOrderItem(selectedOrderForItems.id, {
        menu_item_id: parseInt(selectedMenuItemId),
        quantity: parseInt(quantity),
      });

      // Update the order in the list
      setOrders(orders.map((o) => (o.id === selectedOrderForItems.id ? { ...o, total_price: response.data.new_total } : o)));

      // Refresh order details
      const updatedOrder = await api.getOrder(selectedOrderForItems.id);
      setOrderDetails(updatedOrder.data);

      setSelectedMenuItemId("");
      setQuantity(1);
      alert("Item added successfully!");
    } catch (err) {
      alert("Failed to add item. Please try again.");
      console.error(err);
    }
  };

  const handleRemoveItem = async (itemId) => {
    if (window.confirm("Are you sure you want to remove this item?")) {
      try {
        const response = await api.removeOrderItem(selectedOrderForItems.id, itemId);

        // Update the order in the list
        setOrders(orders.map((o) => (o.id === selectedOrderForItems.id ? { ...o, total_price: response.data.new_total } : o)));

        // Refresh order details
        const updatedOrder = await api.getOrder(selectedOrderForItems.id);
        setOrderDetails(updatedOrder.data);

        alert("Item removed successfully!");
      } catch (err) {
        alert("Failed to remove item. Please try again.");
        console.error(err);
      }
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      Pending: "warning",
      Confirmed: "info",
      Preparing: "primary",
      "Out for Delivery": "secondary",
      Delivered: "success",
      Cancelled: "danger",
    };
    return <Badge bg={variants[status] || "secondary"}>{status}</Badge>;
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading orders...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <h1 className="mb-5 fw-bold">📦 My Orders</h1>

      {error && <Alert variant="danger">{error}</Alert>}

      {orders.length === 0 ? (
        <Alert variant="info">
          No orders found. <a href="/">Start ordering now!</a>
        </Alert>
      ) : (
        <div className="table-responsive">
          <Table striped bordered hover className="orders-table">
            <thead className="table-dark">
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Restaurant</th>
                <th>Items</th>
                <th>Total Price</th>
                <th>Delivery Staff</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td className="fw-bold">#{order.id}</td>
                  <td>
                    {order.customer_name ? (
                      <div>
                        <strong>{order.customer_name}</strong>
                        {order.customer_email && (
                          <>
                            <br />
                            <small className="text-muted">{order.customer_email}</small>
                          </>
                        )}
                      </div>
                    ) : (
                      <span className="text-muted">Guest</span>
                    )}
                  </td>
                  <td>{order.restaurant_name}</td>
                  <td className="items-cell">
                    <small>{order.items || "No items"}</small>
                  </td>
                  <td className="fw-bold text-success">₹{parseFloat(order.total_price || 0).toFixed(2)}</td>
                  <td>
                    {order.delivery_staff_name ? (
                      <div>
                        <strong>{order.delivery_staff_name}</strong>
                        {order.delivery_address && (
                          <>
                            <br />
                            <small className="text-muted">{order.delivery_address}</small>
                          </>
                        )}
                      </div>
                    ) : (
                      <span className="text-muted">Not assigned</span>
                    )}
                  </td>
                  <td>{getStatusBadge(order.status)}</td>
                  <td className="text-muted">
                    <small>{new Date(order.created_at).toLocaleDateString()}</small>
                  </td>

                  <td>
                    <Button variant="outline-success" size="sm" className="me-2" onClick={() => handleManageItems(order)}>
                      Manage Items
                    </Button>
                    <Button variant="outline-danger" size="sm" onClick={() => handleDeleteOrder(order.id)}>
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )}

      <div className="mt-5">
        <a href="/" className="btn btn-primary">
          ← Continue Shopping
        </a>
      </div>

      <Modal show={showItemsModal} onHide={() => setShowItemsModal(false)} size="lg" centered>
        <Modal.Header closeButton>
          <Modal.Title>Manage Order Items</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {loadingItems ? (
            <div className="text-center">
              <Spinner animation="border" role="status" />
            </div>
          ) : orderDetails ? (
            <>
              <h6 className="mb-3">
                Order #{orderDetails.id} - Total: ₹{parseFloat(orderDetails.total_price).toFixed(2)}
              </h6>

              {/* Customer and Delivery Info */}
              <div className="row mb-3">
                <div className="col-md-6">
                  <h6 className="fw-bold">Customer Details:</h6>
                  <p className="mb-1">
                    <strong>Name:</strong> {orderDetails.customer_name || "Guest"}
                  </p>
                  {orderDetails.customer_email && (
                    <p className="mb-1">
                      <strong>Email:</strong> {orderDetails.customer_email}
                    </p>
                  )}
                  {orderDetails.customer_phone && (
                    <p className="mb-1">
                      <strong>Phone:</strong> {orderDetails.customer_phone}
                    </p>
                  )}
                  {orderDetails.delivery_address && (
                    <p className="mb-1">
                      <strong>Delivery Address:</strong> {orderDetails.delivery_address}
                    </p>
                  )}
                </div>
                <div className="col-md-6">
                  <h6 className="fw-bold">Delivery Information:</h6>
                  {orderDetails.delivery_staff_name ? (
                    <>
                      <p className="mb-1">
                        <strong>Delivery Staff:</strong> {orderDetails.delivery_staff_name}
                      </p>
                      {orderDetails.delivery_staff_phone && (
                        <p className="mb-1">
                          <strong>Phone:</strong> {orderDetails.delivery_staff_phone}
                        </p>
                      )}
                      {orderDetails.vehicle_type && (
                        <p className="mb-1">
                          <strong>Vehicle:</strong> {orderDetails.vehicle_type}
                        </p>
                      )}
                    </>
                  ) : (
                    <p className="text-muted">Not assigned</p>
                  )}
                  {orderDetails.payment_method && (
                    <p className="mb-1">
                      <strong>Payment Method:</strong> {orderDetails.payment_method}
                    </p>
                  )}
                </div>
              </div>
              <hr />

              {/* Current Items in Order */}
              <h6 className="mt-4 mb-2">Current Items:</h6>
              {orderDetails.items && orderDetails.items.length > 0 ? (
                <div className="mb-4">
                  <table className="table table-sm table-bordered">
                    <thead>
                      <tr>
                        <th>Item Name</th>
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {orderDetails.items.map((item) => (
                        <tr key={item.id}>
                          <td>{item.name}</td>
                          <td>{item.quantity}</td>
                          <td>₹{parseFloat(item.price * item.quantity).toFixed(2)}</td>
                          <td>
                            <Button variant="danger" size="sm" onClick={() => handleRemoveItem(item.id)}>
                              Remove
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <Alert variant="warning">No items in this order</Alert>
              )}

              {/* Add New Item Section */}
              <h6 className="mt-4 mb-3">Add New Item:</h6>
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Select Item</Form.Label>
                  <Form.Select value={selectedMenuItemId} onChange={(e) => setSelectedMenuItemId(e.target.value)}>
                    <option value="">-- Choose an item --</option>
                    {availableMenuItems.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.name} - ₹{parseFloat(item.price).toFixed(2)}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Quantity</Form.Label>
                  <Form.Control type="number" min="1" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
                </Form.Group>
              </Form>
            </>
          ) : null}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowItemsModal(false)}>
            Close
          </Button>
          <Button variant="success" onClick={handleAddItem} disabled={!selectedMenuItemId}>
            Add Item
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

export default OrdersPage;
