USE master;
GO

-- Drop and recreate the 'DataWarehouse' database
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'SpotifyDataCleansing')
BEGIN
    ALTER DATABASE SpotifyDataCleansing SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE SpotifyDataCleansing;
END;
GO

-- Create the 'DataWarehouse' database
CREATE DATABASE SpotifyDataCleansing;
GO

USE SpotifyDataCleansing;
