IF OBJECT_ID('artists_final','U') IS NOT NULL 
DROP TABLE artists_final
GO
SELECT
    *,
    -- Feature Ratio: how much of an artist's fame comes from guesting on others' songs
    ROUND(feature_streams / NULLIF(lead_streams, 0), 3) AS feature_ratio,

    -- Debut Era bucket
    CASE
        WHEN debut_year < 2010 THEN 'Pre-2010 (Legacy)'
        WHEN debut_year BETWEEN 2010 AND 2015 THEN '2010-2015 (Transition)'
        ELSE '2016+ (Streaming-Native)'
    END AS debut_era,

    -- Language grouping
    CASE WHEN primary_language = 'English' THEN 'English' ELSE 'Non-English' END AS language_group

INTO artists_final 
FROM artist_streaming_info_clean
