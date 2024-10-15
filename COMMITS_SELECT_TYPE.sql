/*Se när det är middag bokad och för hur många personer 
- SELECT X, y from middag. (order by date)
** EXAMPLE QUERY:
*/
SELECT datum, antal_personer, grupp_bokning_id FROM middag 
ORDER BY datum;

/*Se vem i personalen som gjort bokning 
        Selectsats med sökning i bokning samt personal
        *** SQL QUERY:::
        */
SELECT personal.fornamn, personal.efternamn, bokning.bokning_id, personal.personal_id
FROM personal
INNER JOIN bokning ON personal.personal_id = bokning.personal_id;