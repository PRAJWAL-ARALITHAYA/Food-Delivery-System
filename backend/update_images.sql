-- Update Restaurant Images with Better URLs
-- Run this in phpMyAdmin to update existing restaurant images

USE food_delivery;

UPDATE restaurants SET image_url = 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop' WHERE name = 'Pizza Palace';
UPDATE restaurants SET image_url = 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop' WHERE name = 'Burger Bistro';
UPDATE restaurants SET image_url = 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop' WHERE name = 'Sushi Supreme';
UPDATE restaurants SET image_url = 'https://images.unsplash.com/photo-1565299585323-38174c3c6a0a?w=400&h=300&fit=crop' WHERE name = 'Taco Fiesta';
UPDATE restaurants SET image_url = 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop' WHERE name = 'Curry House';

-- Update Menu Item Images
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&h=200&fit=crop' WHERE name = 'Margherita Pizza';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&h=200&fit=crop' WHERE name = 'Pepperoni Pizza';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=200&fit=crop' WHERE name = 'Garlic Bread';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=300&h=200&fit=crop' WHERE name = 'Caesar Salad';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop' WHERE name = 'Classic Burger';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=300&h=200&fit=crop' WHERE name = 'Double Cheeseburger';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300&h=200&fit=crop' WHERE name = 'French Fries';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&h=200&fit=crop' WHERE name = 'Milkshake';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300&h=200&fit=crop' WHERE name = 'California Roll';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=300&h=200&fit=crop' WHERE name = 'Spicy Tuna Roll';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=300&h=200&fit=crop' WHERE name = 'Salmon Sashimi';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop' WHERE name = 'Miso Soup';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1565299585323-38174c3c6a0a?w=300&h=200&fit=crop' WHERE name = 'Beef Tacos';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1615367423057-4b4c5c5c5c5c?w=300&h=200&fit=crop' WHERE name = 'Chicken Enchiladas';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=300&h=200&fit=crop' WHERE name = 'Guacamole Dip';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1587668178277-295251f900ce?w=300&h=200&fit=crop' WHERE name = 'Churros';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop' WHERE name = 'Butter Chicken';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop' WHERE name = 'Tandoori Chicken';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=200&fit=crop' WHERE name = 'Naan Bread';
UPDATE menu_items SET image_url = 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&h=200&fit=crop' WHERE name = 'Mango Lassi';

SELECT 'Images updated successfully!' AS status;

