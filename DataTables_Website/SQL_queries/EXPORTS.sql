SELECT [Batch Job Group] + ' | ' + [Batch Job] AS 'Batch Job Group | Batch Job'
      ,[Batch Job Name]
      ,[Reference File Export]
      ,[ENTIRE_REFERENCE_FILE_STRING] AS 'Entire Reference File String'
      ,[LAN_OUTPUT] AS 'LAN Output'
      ,[Extraction Setup]
      ,[Data Format Setup]
      ,[Extract Table]
      ,[ACTIVE_BATCH_PATH] as 'ActiveBatch Path'
  FROM [SCDRunbook].[dbo].[SCD_EXPORTS]