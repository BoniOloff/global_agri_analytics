SELECT
	com.commodity_name,
    com.commodity_desc,
    c.country_name,
    p.year,
	(SUM(yield)/SUM(area_harvested)/1000) as productivity, 
    SUM(t.export_value),
    SUM(t.import_value)
FROM
	commodity com
INNER JOIN
	production_stat p ON com.commodity_id = p.commodity_id
INNER JOIN
	country c ON c.country_id = p.country_id
INNER JOIN
	trade_stat t ON t.from_country_id = p.country_id AND
    t.commodity_id = p.commodity_id
WHERE 
	t.export_value IS NOT NULL AND
	p.yield IS NOT NULL AND
	p.area_harvested IS NOT NULL AND
	p.year = 2019 AND
	com.commodity_name = 'Tomatoes'
GROUP BY
	p.year, t.from_country_id
ORDER BY 
	productivity DESC

