
-- region update rum to have new field status and migrate data from old fields to there. 
ALTER TABLE rum
ADD COLUMN status ENUM('checkat_in', 'checkat_ut', 'städas', 'underhållsarbetas');

UPDATE rum
SET status = CASE
    WHEN checkat_in = TRUE THEN 'checkat_in'
    WHEN checkat_ut = TRUE THEN 'checkat_ut'
    -- Add any other conditions if needed
    ELSE status  -- To handle cases where neither is set
END;

ALTER TABLE rum
DROP COLUMN checkat_in,
DROP COLUMN checkat_ut;
-- endregion

-- region 
-- >>rum
-- istället för att ha checked_in och checked_out ha enbart antingen checked_in eller eventuellt "status".
-- Fördel med status är att kunna ha en lista över händelser som påverkar rummet, exempelvis: 
ALTER TABLE faktura
ADD COLUMN status ENUM('checkat_in', 'checkat_ut', 'städas', 'underhållsarbetas')
-- TODO:
-- note do not have testdate created for this yet! 
-- endregion

-- region
/* 
Lägga in erbjudandens giltighetstid
        ** enkel
        - viz. update
*/
update erbjudande 
SET start = '2024-10-15 00:00:00', slut = '2024-11-15 23:59:59'
WHERE erbjudande_id = 1

-- endregion

-- region
/* 
 Uppdatera hur många personer som ska äta
        ** enkel
        - update statement        
*/
-- usecase example: en person har blivit sjuk och ska inte vara med på middagen men sova i rummet.
update middag
SET antal_personer = antal_personer - 1
WHERE middag_id = 1

-- endregion

-- region
/* 
XXXX
        ** enkel
        - viz. update
*/
update erbjudande 
SET start = '2024-10-15 00:00:00', slut = '2024-11-15 23:59:59'
WHERE erbjudande_id = 1

-- endregion