-- @block
-- skapa databasen först
CREATE DATABASE hotell_hedvig;
-- säg till database att utgå ifrån denna
USE hotell_hedvig;
-- @block
CREATE TABLE rum_typ(
    rum_typ_id  VARCHAR(255) PRIMARY KEY,
    max_antal_personer SMALLINT
);

-- @block
CREATE TABLE erbjudande(
    erbjudande_id  INT PRIMARY KEY AUTO_INCREMENT,
    prisavdrag DECIMAL(8,2),
    villkor VARCHAR(255),
    start_datum TIMESTAMP,
    slut_datum TIMESTAMP
);
-- @block
CREATE TABLE personal(
    personal_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255),
    efternamn VARCHAR(255),
    roll VARCHAR(255)
);
-- @block
CREATE TABLE huvud_gast(
    huvud_gast_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255),
    efternamn VARCHAR(255),
    mejl_address VARCHAR(255),
    telefon_nummer VARCHAR(30) -- för att kunna hålla nummer inklusive specialtecken såsom + och -- och () så ska 30 vara tillräckligt.
);
-- @block 
CREATE TABLE kund(
    kund_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255),
    efternamn VARCHAR(255),
    mejl_address VARCHAR(255),
    telefon_nummer VARCHAR(30)
);
-- @block
CREATE TABLE rum_pris(
    rum_pris_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_typ_id VARCHAR(255),
    pris_per_natt DECIMAL(8,2),
    pris_start_datum TIMESTAMP,
    pris_slut_datum TIMESTAMP,
    CONSTRAINT rum_pris_fk_rum_typ FOREIGN KEY (rum_typ_id) REFERENCES rum_typ(rum_typ_id)
);
-- @block
CREATE TABLE rum(
    rum_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_typ_id VARCHAR(255),
    personal_id INT,
    checked_in BOOLEAN,
    checked_out BOOLEAN,
    CONSTRAINT rum_fk_rum_typ FOREIGN KEY (rum_typ_id) REFERENCES rum_typ(rum_typ_id),
    CONSTRAINT rum_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id)
);
-- @block
CREATE TABLE faktura(
    faktura_id INT PRIMARY KEY AUTO_INCREMENT,
    personal_id INT,
    erbjudande_id INT,
    CONSTRAINT faktura_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT faktura_fk_erbjudande FOREIGN KEY (erbjudande_id) REFERENCES erbjudande(erbjudande_id)
);
-- @block
CREATE TABLE grupp_bokning(
    grupp_bokning_id INT PRIMARY KEY AUTO_INCREMENT,
    personal_id INT,
    faktura_id INT,
    CONSTRAINT grupp_bokning_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT grupp_bokning_fk_faktura FOREIGN KEY (faktura_id) REFERENCES faktura(faktura_id)
);
-- @block
CREATE TABLE middag(
    middag_id INT PRIMARY KEY AUTO_INCREMENT,
    grupp_bokning_id INT,
    antal_personer SMALLINT,
    datum TIMESTAMP,
    CONSTRAINT middag_fk_grupp_bokning FOREIGN KEY (grupp_bokning_id) REFERENCES grupp_bokning(grupp_bokning_id)
);
-- @block
CREATE TABLE forsaljning(
    forsaljning_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_id INT,
    personal_id INT,
    faktura_id INT,
    summa DECIMAL(8,2),
    datum TIMESTAMP,
    CONSTRAINT forsaljning_fk_rum FOREIGN KEY (rum_id) REFERENCES rum(rum_id),
    CONSTRAINT forsaljning_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT forsaljning_fk_faktura FOREIGN KEY (faktura_id) REFERENCES faktura(faktura_id)
);
-- @block
CREATE TABLE bokning(
    bokning_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_id INT,
    kund_id INT,
    huvud_gast_id INT,
    personal_id INT,
    rum_pris_id INT,
    grupp_bokning_id INT,
    datum_incheck DATE,
    datum_utcheck DATE,
    booking_datum TIMESTAMP,
    antal_gaster SMALLINT,
    CONSTRAINT bokning_fk_rum FOREIGN KEY (rum_id) REFERENCES rum(rum_id),
    CONSTRAINT bokning_fk_kund FOREIGN KEY (kund_id) REFERENCES kund(kund_id),
    CONSTRAINT bokning_fk_huvud_gast FOREIGN KEY (huvud_gast_id) REFERENCES huvud_gast(huvud_gast_id),
    CONSTRAINT bokning_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT bokning_fk_rum_pris FOREIGN KEY (rum_pris_id) REFERENCES rum_pris(rum_pris_id),
    CONSTRAINT bokning_fk_grupp_bokning FOREIGN KEY (grupp_bokning_id) REFERENCES grupp_bokning(grupp_bokning_id)
); 


