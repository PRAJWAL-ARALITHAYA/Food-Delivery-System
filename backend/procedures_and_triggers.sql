-- =====================================================
-- Minimal Procedures and Triggers
-- KEEP: one trigger that sets item price on insert and updates order total
-- KEEP: one stored procedure to assign delivery staff to an order
-- NOTE: This script is written for MySQL/MariaDB. SQLite does not support stored
-- procedures and has different trigger syntax; if you use SQLite, adapt accordingly.
-- =====================================================

USE food_delivery;

-- =====================================================
-- PROCEDURE: Assign Delivery Staff to Order
-- Picks an available delivery staff (highest rating, then fewest deliveries)
-- =====================================================
DROP PROCEDURE IF EXISTS assign_delivery_staff_to_order;

DELIMITER $$
CREATE PROCEDURE assign_delivery_staff_to_order (
    IN p_order_id INT
)
BEGIN
    DECLARE v_staff_id INT;

    SELECT id INTO v_staff_id
    FROM delivery_staff
    WHERE status = 'Available'
    ORDER BY rating DESC, total_deliveries ASC
    LIMIT 1;

    IF v_staff_id IS NOT NULL THEN
        UPDATE orders
        SET delivery_staff_id = v_staff_id,
            status = 'Out for Delivery'
        WHERE id = p_order_id;

        UPDATE delivery_staff
        SET status = 'Busy',
            total_deliveries = total_deliveries + 1
        WHERE id = v_staff_id;
    END IF;
END$$
DELIMITER ;

-- =====================================================
-- TRIGGER: Set order_items.price on INSERT and update orders.total_price
-- When a new order_items row is inserted, copy the current menu_items.price
-- into order_items.price (if NULL) and then recalculate the order total.
-- =====================================================
DROP TRIGGER IF EXISTS trg_order_items_after_insert;

DELIMITER $$
CREATE TRIGGER trg_order_items_after_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    -- Set price on the inserted order_item if not provided
    IF NEW.price IS NULL THEN
        UPDATE order_items
        SET price = (
            SELECT price FROM menu_items WHERE id = NEW.menu_item_id
        )
        WHERE id = NEW.id;
    END IF;

    -- Recalculate order total
    UPDATE orders
    SET total_price = (
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END$$
DELIMITER ;

SELECT 'Kept one trigger (set price + update total) and one procedure (assign delivery staff).' AS status;

