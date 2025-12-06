import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

// Restaurants
export const getRestaurants = () => axios.get(`${API_BASE_URL}/restaurants`);
export const getRestaurant = (id) => axios.get(`${API_BASE_URL}/restaurants/${id}`);

// Menu Items
export const getMenuItems = (restaurantId) => axios.get(`${API_BASE_URL}/restaurants/${restaurantId}/menu`);
export const getMenuItem = (id) => axios.get(`${API_BASE_URL}/menu/${id}`);

// Customers
export const getCustomers = () => axios.get(`${API_BASE_URL}/customers`);
export const getCustomer = (id) => axios.get(`${API_BASE_URL}/customers/${id}`);
export const createCustomer = (customerData) => axios.post(`${API_BASE_URL}/customers`, customerData);
export const findOrCreateCustomer = (customerData) => axios.post(`${API_BASE_URL}/customers/find-or-create`, customerData);

// Delivery Staff
export const getDeliveryStaff = (status) => {
  const url = status ? `${API_BASE_URL}/delivery-staff?status=${status}` : `${API_BASE_URL}/delivery-staff`;
  return axios.get(url);
};
export const getDeliveryStaffMember = (id) => axios.get(`${API_BASE_URL}/delivery-staff/${id}`);
export const getAvailableDeliveryStaff = () => axios.get(`${API_BASE_URL}/delivery-staff/available`);

// Orders
export const getOrders = () => axios.get(`${API_BASE_URL}/orders`);
export const getOrder = (id) => axios.get(`${API_BASE_URL}/orders/${id}`);
export const createOrder = (orderData) => axios.post(`${API_BASE_URL}/orders`, orderData);
export const updateOrder = (id, status) => axios.put(`${API_BASE_URL}/orders/${id}`, { status });
export const deleteOrder = (id) => axios.delete(`${API_BASE_URL}/orders/${id}`);
export const addOrderItem = (orderId, itemData) => axios.post(`${API_BASE_URL}/orders/${orderId}/items`, itemData);
export const removeOrderItem = (orderId, itemId) => axios.delete(`${API_BASE_URL}/orders/${orderId}/items/${itemId}`);

// Reports & Analytics
export const getSummaryReport = () => axios.get(`${API_BASE_URL}/reports/summary`);
export const getOrdersByStatus = () => axios.get(`${API_BASE_URL}/reports/orders-by-status`);
export const getRestaurantRevenue = () => axios.get(`${API_BASE_URL}/reports/restaurant-revenue`);
export const getTopCustomers = (limit = 5) => axios.get(`${API_BASE_URL}/reports/top-customers?limit=${limit}`);

// Health Check
export const healthCheck = () => axios.get(`${API_BASE_URL}/health`);

export default {
  getRestaurants,
  getRestaurant,
  getMenuItems,
  getMenuItem,
  getCustomers,
  getCustomer,
  createCustomer,
  findOrCreateCustomer,
  getDeliveryStaff,
  getDeliveryStaffMember,
  getAvailableDeliveryStaff,
  getOrders,
  getOrder,
  createOrder,
  updateOrder,
  deleteOrder,
  addOrderItem,
  removeOrderItem,
  getSummaryReport,
  getOrdersByStatus,
  getRestaurantRevenue,
  getTopCustomers,
  healthCheck,
};
