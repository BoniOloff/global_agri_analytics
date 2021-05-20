# Query 1
# For specific commodity (e.g. Avocados), list main provider of that commodity which a country rely on 
# and calculate the total paid tariff ($ Million)

SELECT 
	t.year, 
    com.commodity_name,
    c.country_name AS 'importer', 
    c2.country_name AS 'provider', 
    SUM(t.import_value) AS total_import, 
    sum(t.import_value * t.tariff_avg/100) as 'tariff_paid', 
    t.tariff_avg,
    (RANK() OVER ( PARTITION BY c.country_name, t.year 
    ORDER BY SUM(t.import_value) DESC )) AS provider_rank
FROM
	country c 
    INNER JOIN
    trade_stat t ON t.from_country_id =  c.country_id
    INNER JOIN
    commodity com ON com.commodity_id = t.commodity_id
    INNER JOIN
    country c2 ON c2.country_id = t.to_country_id
WHERE
	t.import_value IS NOT NULL AND
    t.tariff_avg IS NOT NULL AND
    com.commodity_name = 'Avocados' AND 
    (t.year BETWEEN '2018' AND '2019')
GROUP BY 
	t.from_country_id, t.to_country_id, t.year
ORDER BY 
	t.year DESC, c.country_name, t.import_value DESC, total_import DESC
	
    
    