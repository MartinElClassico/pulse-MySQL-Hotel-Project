-- @block
-- skapa databasen först
CREATE DATABASE hotell_hedvig;
-- säg till database att utgå ifrån denna
USE hotell_hedvig;
-- @block
CREATE TABLE rum_typ(
    rum_typ_id  VARCHAR(255) PRIMARY KEY,
    max_antal_personer SMALLINT NOT NULL
);

-- @block
CREATE TABLE erbjudande(
    erbjudande_id  INT PRIMARY KEY AUTO_INCREMENT,
    prisavdrag DECIMAL(8,2) NOT NULL,
    villkor VARCHAR(255),
    `start` DATETIME NOT NULL,
    slut DATETIME
);
-- @block
CREATE TABLE personal(
    personal_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255) NOT NULL,
    efternamn VARCHAR(255) NOT NULL,
    roll VARCHAR(255) NOT NULL
);
-- @block
CREATE TABLE huvud_gast(
    huvud_gast_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255) NOT NULL,
    efternamn VARCHAR(255) NOT NULL,
    mejl_address VARCHAR(255) NOT NULL,
    telefon_nummer VARCHAR(30)  NOT NULL -- för att kunna hålla nummer inklusive specialtecken såsom + och -- och () så ska 30 vara tillräckligt.
);
-- @block 
CREATE TABLE kund(
    kund_id INT PRIMARY KEY AUTO_INCREMENT,
    fornamn VARCHAR(255) NOT NULL,
    efternamn VARCHAR(255) NOT NULL,
    mejl_address VARCHAR(255) NOT NULL,
    telefon_nummer VARCHAR(30) NOT NULL
);
-- @block
CREATE TABLE rum_pris(
    rum_pris_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_typ_id VARCHAR(255) NOT NULL,
    pris_per_natt DECIMAL(8,2) NOT NULL,
    `start` DATETIME NOT NULL,
    slut DATETIME,
    CONSTRAINT rum_pris_fk_rum_typ FOREIGN KEY (rum_typ_id) REFERENCES rum_typ(rum_typ_id)
);
-- @block
CREATE TABLE rum(
    rum_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_typ_id VARCHAR(255)  NOT NULL,
    `status` ENUM('checkat_in', 'checkat_ut', 'stadas', 'underhallsarbetas') NOT NULL,
    vaningsplan VARCHAR(255),
    CONSTRAINT rum_fk_rum_typ FOREIGN KEY (rum_typ_id) REFERENCES rum_typ(rum_typ_id)
);
-- @block
CREATE TABLE grupp_bokning(
    grupp_bokning_id INT PRIMARY KEY AUTO_INCREMENT
);
-- @block
CREATE TABLE faktura(
    faktura_id INT PRIMARY KEY AUTO_INCREMENT,
    personal_id INT NOT NULL,
    erbjudande_id INT, -- note: auto generator always has values for this attribute
    `status` ENUM('pagaende', 'betald', 'obetald', 'kommande'),
    CONSTRAINT faktura_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT faktura_fk_erbjudande FOREIGN KEY (erbjudande_id) REFERENCES erbjudande(erbjudande_id)
);
-- @block
CREATE TABLE middag(
    middag_id INT PRIMARY KEY AUTO_INCREMENT,
    grupp_bokning_id INT NOT NULL,
    antal_personer SMALLINT NOT NULL,
    datum DATETIME NOT NULL,
    CONSTRAINT middag_fk_grupp_bokning FOREIGN KEY (grupp_bokning_id) REFERENCES grupp_bokning(grupp_bokning_id)
);
-- @block
CREATE TABLE forsaljning(
    forsaljning_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_id INT NOT NULL,
    personal_id INT NOT NULL,
    faktura_id INT NOT NULL,
    summa DECIMAL(8,2) NOT NULL,
    datum DATETIME NOT NULL,
    CONSTRAINT forsaljning_fk_rum FOREIGN KEY (rum_id) REFERENCES rum(rum_id),
    CONSTRAINT forsaljning_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT forsaljning_fk_faktura FOREIGN KEY (faktura_id) REFERENCES faktura(faktura_id)
);
-- @block
CREATE TABLE bokning(
    bokning_id INT PRIMARY KEY AUTO_INCREMENT,
    rum_id INT NOT NULL,
    kund_id INT NOT NULL,
    huvud_gast_id INT NOT NULL,
    personal_id INT NOT NULL,
    rum_pris_id INT NOT NULL,
    grupp_bokning_id INT, 
    faktura_id INT NOT NULL,
    incheckning DATE NOT NULL,
    utcheckning DATE NOT NULL,
    bokning_datum DATETIME NOT NULL,
    antal_gaster SMALLINT NOT NULL,
    CONSTRAINT bokning_fk_rum FOREIGN KEY (rum_id) REFERENCES rum(rum_id),
    CONSTRAINT bokning_fk_kund FOREIGN KEY (kund_id) REFERENCES kund(kund_id),
    CONSTRAINT bokning_fk_huvud_gast FOREIGN KEY (huvud_gast_id) REFERENCES huvud_gast(huvud_gast_id),
    CONSTRAINT bokning_fk_personal FOREIGN KEY (personal_id) REFERENCES personal(personal_id),
    CONSTRAINT bokning_fk_rum_pris FOREIGN KEY (rum_pris_id) REFERENCES rum_pris(rum_pris_id),
    CONSTRAINT bokning_fk_grupp_bokning FOREIGN KEY (grupp_bokning_id) REFERENCES grupp_bokning(grupp_bokning_id),
    CONSTRAINT bokning_fk_faktura FOREIGN KEY (faktura_id) REFERENCES faktura(faktura_id)
    -- perhaps make a restraint so that faktura_id behaves as if "NOT NULL" when "grupp bokning id" is null.
); 



