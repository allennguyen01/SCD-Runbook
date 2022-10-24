SELECT [NAME]
      ,[PATH_NAME]
      ,[STATE]
      ,[ENTIRE_SCHEDULES]
  FROM [SCDRunbook].[dbo].[SCHEDULED_PLANS_LIST]
  WHERE STATE = 'Enabled'
  ORDER BY NAME ASC