-- add trigger to rum_typ where it updates the checked_in and checked out to 

DELIMITER $$

CREATE TRIGGER before_room_update 
BEFORE UPDATE ON rooms
FOR EACH ROW
BEGIN
    -- If checked_out is set to TRUE, set checked_in to FALSE
    IF NEW.checked_out = TRUE THEN
        SET NEW.checked_in = FALSE;
    END IF;

    -- If checked_in is set to TRUE, set checked_out to FALSE
    IF NEW.checked_in = TRUE THEN
        SET NEW.checked_out = FALSE;
    END IF;
END$$

DELIMITER ;