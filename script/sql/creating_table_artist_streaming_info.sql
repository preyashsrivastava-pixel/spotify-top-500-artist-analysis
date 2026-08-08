IF OBJECT_ID('artist_streaming_info', 'U') IS NOT NULL
    DROP TABLE artist_streaming_info;
GO

CREATE TABLE artist_streaming_info (
    artist_name NVARCHAR(100),
    sex NVARCHAR(20),
    country_of_origin NVARCHAR(100),
    primary_language NVARCHAR(50),
    primary_genre NVARCHAR(100),
    artist_type NVARCHAR(50),
    debut_year INT,
    total_streams_m FLOAT,
    lead_streams_m FLOAT,
    feature_streams_m FLOAT,
    solo_streams_m FLOAT, 
    solo_stream_pct FLOAT,
    collaborative_streams_m FLOAT,
    collaborative_stream_pct FLOAT
);
