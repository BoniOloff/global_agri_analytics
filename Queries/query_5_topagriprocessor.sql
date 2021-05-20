# Determine whether a high or upper middle income country country is a processor only / producer only / or both, and sort by share of rural population

SELECT c.country_name, ss.year, cs.income_group, com.commodity_name, ss.processed, 
mfg.production_value, mfg.manufacturing, mfg.characteristic,
	(cs.population_rural / (cs.population_rural + cs.population_urban)) AS rural_population
FROM
	country_stat cs 
    INNER JOIN
    country c ON cs.country_id = c.country_id
    INNER JOIN
    stock_stat ss ON ss.country_id = c.country_id AND ss.year = cs.year
    INNER JOIN
    commodity com ON com.commodity_id = ss.commodity_id
	INNER JOIN
    (SELECT p.country_id, p.year, p.commodity_id, ss.processed, p.production_value, 
    (ss.processed / p.production_value) AS manufacturing,
		(CASE 
			WHEN (ss.processed / p.production_value) > 1 THEN 'Processor Only'
			WHEN (ss.processed / p.production_value) > 0.5 THEN 'Producer and Processor'
			ELSE 'Producer Only' END) AS characteristic
	FROM
		stock_stat ss 
		INNER JOIN 
		production_stat p ON p.country_id = ss.country_id AND
		p.commodity_id = ss.commodity_id AND p.year = ss.year
	WHERE
		ss.processed IS NOT NULL AND (p.year BETWEEN 2016 AND 2018) 
	GROUP BY
		p.country_id, p.commodity_id) AS mfg ON mfg.country_id = ss.country_id AND 
        mfg.year = ss.year AND mfg.commodity_id = ss.commodity_id
WHERE
	ss.loss IS NOT NULL AND
	cs.gdp_agri IS NOT NULL AND
	(cs.year BETWEEN 2016 AND 2018) AND
    (cs.income_group = 'UM' OR
    cs.income_group = 'H') 
GROUP BY cs.country_id, cs.year, ss.commodity_id
ORDER BY rural_population DESC
