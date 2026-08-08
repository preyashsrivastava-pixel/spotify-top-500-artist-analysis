IF OBJECT_ID('artist_streaming_info_clean', 'U') IS NOT NULL
    DROP TABLE artist_streaming_info_clean;
GO
SELECT
        TRIM(artist_name) AS artist_name ,
        TRIM(sex) as sex,
        TRIM(country_of_origin) as country_of_origin,
        TRIM(primary_language) as primary_language,
        TRIM(primary_genre) as primary_genre,
        TRIM(artist_type) as artist_type,
        CAST(debut_year AS INTEGER) as debut_year,
        CAST(total_streams_m AS REAL) AS total_streams,
        CAST(lead_streams_m AS REAL) AS lead_streams,
        CAST(feature_streams_m AS REAL) AS feature_streams,
        CAST(solo_streams_m AS REAL) AS solo_streams,
        CAST(collaborative_streams_m AS REAL) AS collaborative_streams,
        CAST(solo_stream_pct AS REAL) AS pct_solo,
        CAST(collaborative_stream_pct AS REAL) AS pct_collab
  INTO artist_streaming_info_clean
  FROM artist_streaming_info;
