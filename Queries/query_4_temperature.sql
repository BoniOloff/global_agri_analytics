# Identify the year when extreme temperature change happened and compare it with the production growth (YoY)

SELECT
	p.year,
    r.region_name,
    c.country_name,
    com.commodity_name,
    p.production_value,
    cl.temperature_chg,
	( p.production_value/lag(p.production_value) OVER (ORDER BY c.country_name, p.year) - 1) AS production_growth_yoy,
    MAX(ABS(cl.temperature_chg)) max_temp_change
FROM
	country c
    INNER JOIN
    region r ON r.region_id = c.region_id
    INNER JOIN
    production_stat p ON p.country_id = c.country_id
    INNER JOIN
    country_climate cl ON cl.country_id = c.country_id AND
    cl.year = p.year
    INNER JOIN
    commodity com ON com.commodity_id = p.commodity_id
    INNER JOIN
	(SELECT cl.country_id, MAX(ABS(cl.temperature_chg)) AS temp FROM country_climate cl 
    GROUP BY cl.country_id) AS x ON x.country_id = cl.country_id AND x.temp = cl.temperature_chg
WHERE
	p.production_value IS NOT NULL AND
    p.area_harvested IS NOT NULL AND
    p.yield IS NOT NULL AND
    com.commodity_name LIKE '%rice%' AND
    (p.year BETWEEN '2010' AND '2019')
GROUP BY
	c.country_name, com.commodity_name
HAVING
    cl.temperature_chg IN (SELECT MAX(ABS(cl.temperature_chg)) FROM country_climate cl GROUP BY cl.country_id)
ORDER BY
	r.region_name, p.year
    
    