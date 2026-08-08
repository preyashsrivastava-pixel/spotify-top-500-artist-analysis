
CREATE OR ALTER PROCEDURE load_data  AS
BEGIN
	DECLARE @start_time DATETIME, @end_time DATETIME, @batch_start_time DATETIME, @batch_end_time DATETIME; 
	BEGIN TRY
		
		SET @start_time = GETDATE();
		PRINT '>> Truncating Table: artist_streaming_info';
		TRUNCATE TABLE artist_streaming_info;
		PRINT '>> Inserting Data Into: artist_streaming_info';
		BULK INSERT artist_streaming_info
        FROM 'C:\Users\preya\OneDrive\Desktop\Spotify Data Analysis\raw_data\artist_streaming_info.csv'
        WITH
        (
            FORMAT = 'CSV',
            FIRSTROW = 2,
            FIELDTERMINATOR = ',',
            ROWTERMINATOR = '\n',
            TABLOCK
        );
		SET @end_time = GETDATE();
		PRINT '>> Load Duration: ' + CAST(DATEDIFF(second, @start_time, @end_time) AS NVARCHAR) + ' seconds';
		PRINT '>> -------------';
    END TRY
    BEGIN CATCH
        PRINT '>> ERROR OCCURRED DURING LOAD';
        PRINT '>> Error Message: ' + ERROR_MESSAGE();
        PRINT '>> Error Number: ' + CAST(ERROR_NUMBER() AS NVARCHAR);
        PRINT '>> -------------';
    END CATCH
END

EXEC load_data
