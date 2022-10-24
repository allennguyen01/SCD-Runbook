SELECT [NAME] AS 'Name'
      ,[PATH_NAME] AS 'Path Name'
      ,[ENTIRE_SCHEDULES] AS 'Scheduled Times'
  FROM [SCDRunbook].[dbo].[SCHEDULED_PLANS_LIST]
  WHERE STATE = 'Enabled'
  ORDER BY NAME ASC