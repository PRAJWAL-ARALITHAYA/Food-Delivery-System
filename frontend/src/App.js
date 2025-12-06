import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Navigation from "./components/Navigation";
import HomePage from "./components/HomePage";
import MenuPage from "./components/MenuPage";
import OrdersPage from "./components/OrdersPage";
import CustomersPage from "./components/CustomersPage";
import DeliveryStaffPage from "./components/DeliveryStaffPage";
import "./App.css";

function App() {
  return (
    <Router>
      <Navigation />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/menu/:restaurantId" element={<MenuPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/delivery-staff" element={<DeliveryStaffPage />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
