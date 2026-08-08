--SANITY CHECKS-- 

--Check 1: Any duplicate artists?--

SELECT 
	artist_name,
	COUNT(*) AS frequency
FROM artist_streaming_info_clean
GROUP BY artist_name 
HAVING COUNT(*)>1 or COUNT(*) IS NULL;

--Check 2: Does Lead + Feature roughly equal Total?--
SELECT * FROM (
SELECT 
	artist_name,
	lead_streams,
	feature_streams,
	lead_streams + feature_streams as total,
	total_streams,
	ABS(total_streams-(lead_streams + feature_streams)) as difference
FROM artist_streaming_info_clean )t
WHERE difference > 1
ORDER BY difference desc


-- Check 2b: Same check, but as a % of total_streams (more meaningful than raw diff)

  
  SELECT artist_name, total_streams,
       (lead_streams + feature_streams) AS total,
       ROUND(ABS(total_streams - (lead_streams + feature_streams)) * 100.0 / total_streams, 3) AS pct_diff
FROM artist_streaming_info_clean
ORDER BY pct_diff DESC
;


--Check 2c: Checking values where pct_diff>1--


SELECT * FROM (
		SELECT 
			artist_name,
			total_streams,
			(lead_streams + feature_streams) AS total,
            ROUND(ABS(total_streams - (lead_streams + feature_streams)) * 100.0 / total_streams, 3) AS pct_diff
		FROM artist_streaming_info_clean
         )t
WHERE pct_diff>1;

--Thus for no artist is the relative difference >1% thus the anomaly is not significant--



-- Check 3: Does Solo % + Collab % roughly equal 100?

SELECT artist_name,pct_solo+pct_collab AS hundred
FROM artist_streaming_info_clean
WHERE pct_solo+pct_collab != 100;

-- Check 4: Any missing/null values?--
SELECT
    SUM(CASE WHEN artist_name IS NULL OR TRIM(artist_name) = '' THEN 1 ELSE 0 END) AS missing_artist_name,
    SUM(CASE WHEN sex IS NULL OR TRIM(sex) = '' THEN 1 ELSE 0 END) AS missing_sex,
    SUM(CASE WHEN country_of_origin IS NULL OR TRIM(country_of_origin) = '' THEN 1 ELSE 0 END) AS missing_country,
    SUM(CASE WHEN primary_language IS NULL OR TRIM(primary_language) = '' THEN 1 ELSE 0 END) AS missing_language,
    SUM(CASE WHEN primary_genre IS NULL OR TRIM(primary_genre) = '' THEN 1 ELSE 0 END) AS missing_genre,
    SUM(CASE WHEN artist_type IS NULL OR TRIM(artist_type) = '' THEN 1 ELSE 0 END) AS missing_artist_type,
    SUM(CASE WHEN debut_year IS NULL THEN 1 ELSE 0 END) AS missing_debut_year,
    SUM(CASE WHEN total_streams IS NULL THEN 1 ELSE 0 END) AS missing_total_streams,
    SUM(CASE WHEN lead_streams IS NULL THEN 1 ELSE 0 END) AS missing_lead_streams,
    SUM(CASE WHEN feature_streams IS NULL THEN 1 ELSE 0 END) AS missing_feature_streams,
    SUM(CASE WHEN solo_streams IS NULL THEN 1 ELSE 0 END) AS missing_solo_streams,
    SUM(CASE WHEN pct_solo IS NULL THEN 1 ELSE 0 END) AS missing_pct_solo,
    SUM(CASE WHEN collaborative_streams IS NULL THEN 1 ELSE 0 END) AS missing_collab_streams,
    SUM(CASE WHEN pct_collab IS NULL THEN 1 ELSE 0 END) AS missing_pct_collab,
    SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS missing_id
FROM artist_streaming_info_clean;

-- Check 5: Any weird debut years (e.g. future years, or absurdly old)?


SELECT
  DISTINCT debut_year 
  FROM artist_streaming_info_clean
  
  ORDER BY debut_year;





