## Query 1 
## Top 2 & Bottom 2 countries who export most compare to their domestic production

(SELECT c.country_name, com.commodity_name, t.year, p.production_value, 
SUM(t.export_value) AS total_export, 
(SUM(t.export_value) / p.production_value * 100) AS export_ratio, 
'Top 2 Countries' as Category, SUM(t.import_value) AS total_import
FROM country c
	INNER JOIN production_stat p ON p.country_id = c.country_id
    INNER JOIN commodity com ON com.commodity_id = p.commodity_id
    INNER JOIN trade_stat t ON t.commodity_id = com.commodity_id AND
    t.year = p.year AND t.from_country_id = c.country_id AND
    t.from_country_id = p.country_id
WHERE 
	t.export_value > 0 AND p.production_value > 0 
    AND com.commodity_name LIKE 'orange%' AND 
    p.year = 2019 AND t.import_value IS NOT NULL
GROUP BY t.from_country_id
ORDER BY export_ratio DESC
LIMIT 2)
UNION
(SELECT c.country_name, com.commodity_name, t.year, p.production_value, 
SUM(t.export_value) AS total_export, 
(SUM(t.export_value) / p.production_value * 100) AS export_ratio, 
'Bottom 2 Countries' as Category, SUM(t.import_value) AS total_import
FROM country c
	INNER JOIN production_stat p ON p.country_id = c.country_id
    INNER JOIN commodity com ON com.commodity_id = p.commodity_id
    INNER JOIN trade_stat t ON 
    t.commodity_id = com.commodity_id AND t.year = p.year AND
    t.from_country_id = c.country_id AND t.from_country_id = p.country_id
WHERE 
	t.export_value > 0 AND p.production_value > 0 AND 
    com.commodity_name LIKE 'orange%' AND p.year = 2019 AND 
    t.import_value IS NOT NULL
GROUP BY t.from_country_id
ORDER BY export_ratio ASC
LIMIT 2);
