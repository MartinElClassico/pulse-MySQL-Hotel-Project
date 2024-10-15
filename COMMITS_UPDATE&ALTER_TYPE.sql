
--region update rum to have new field status and migrate data from old fields to there. 
ALTER TABLE rum
ADD COLUMN status ENUM('checkat_in', 'checkat_ut', 'städas', 'underhållsarbetas');

UPDATE rum
SET status = CASE
    WHEN checked_in = TRUE THEN 'checkat_in'
    WHEN checked_out = TRUE THEN 'checkat_ut'
    -- Add any other conditions if needed
    ELSE status  -- To handle cases where neither is set
END;
--endregion

ALTER TABLE rum
DROP COLUMN checked_in,
DROP COLUMN checked_out;
-- endregion

-- region 
-->>rum
--istället för att ha checked_in och checked_out ha enbart antingen checked_in eller eventuellt "status".
--Fördel med status är att kunna ha en lista över händelser som påverkar rummet, exempelvis: 
ALTER TABLE faktura
ADD COLUMN status ENUM('checkat_in', 'checkat_ut', 'städas', 'underhållsarbetas')
--TODO:
-- note do not have testdate created for this yet! 
--endregion
