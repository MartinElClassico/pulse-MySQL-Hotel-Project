/*Se när det är middag bokad och för hur många personer 
- SELECT X, y from middag. (order by date)
** EXAMPLE QUERY:
*/
SELECT datum, antal_personer, grupp_bokning_id FROM middag 
ORDER BY datum;