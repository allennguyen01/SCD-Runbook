SELECT [Batch Job Group] + ' | ' + [Batch Job] AS 'Batch Job Group | Batch Job'
    ,[Batch Job Name]
    ,[Reference File Import] 
    ,[ENTIRE_REFERENCE_FILE_STRING] AS 'Entire Reference File String'
    ,[Data Format Setup]
    ,[ACTIVE_BATCH_PATH] AS 'ActiveBatch Path'
FROM [SCDRunbook].[dbo].[SCD_IMPORTS]
ORDER BY [Batch Job Group | Batch Job]