-- Number of rows
SELECT COUNT(*)
FROM ids_data;

-- Exploring the first 10 rows of the data
SELECT *
FROM ids_data
LIMIT 10;

-- Number of distinct countries
SELECT COUNT(DISTINCT (country_name)) AS 'Number of Distinct Countries'
FROM ids_data;

-- Amount borrowed by each country
SELECT country_name, SUM(amount) AS 'Total amount borrowed'
FROM ids_data
GROUP BY 1
ORDER BY 1
LIMIT 10;

-- Amount borrowed by each country in Billions
SELECT 
    country_name,
    ROUND(SUM(amount) / 1000000000, 2) AS 'Total amount borrowed in Billions'
FROM ids_data
GROUP BY 1
ORDER BY 1
LIMIT 10;

-- Highest borrower
SELECT 
    country_name AS highest_borrower,
	  ROUND(SUM(amount) / 1000000000, 2) AS 'Total amount borrowed in Billions'
FROM ids_data
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- LOWEST borrower
SELECT 
    country_name AS lowest_borrower,
    ROUND(SUM(amount) / 1000000000, 2) AS 'Total amount borrowed in Billions'
FROM
    ids_data
GROUP BY 1
ORDER BY 2
LIMIT 1;

-- Average borrowing amount
SELECT 
    ROUND(AVG(`Total amount borrowed in Billions`), 2) AS 'Average borrowing amount'
FROM
    (SELECT 
        country_name,
        ROUND(SUM(amount) / 1000000000, 2) AS 'Total amount borrowed in Billions'
     FROM
        ids_data
     GROUP BY 1) cte;

-- Number of distinct indicators
SELECT COUNT(DISTINCT (indicator_code)) AS 'Number of indicators'
FROM ids_data;

-- Total and percent of total amount borrowed by indicators
SELECT 
    indicator_name,
    ROUND(SUM(amount) / 1000000000, 2) AS 'Total in Billion',
    ROUND((SUM(amount) / 1000000000) / (SELECT SUM(amount) / 1000000000
					FROM ids_data) * 100, 2) AS 'Percent of Total'
FROM ids_data
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- China's debt by indicators
SELECT 
    indicator_name,
    ROUND(SUM(amount) / 1000000000, 2) AS 'Total in Billion',
    ROUND((SUM(amount) / 1000000000) / (SELECT SUM(amount) / 1000000000
					FROM ids_data
                                        WHERE country_name = 'China') * 100, 2) AS 'Percent of Total'
FROM ids_data
WHERE country_name = 'China'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
