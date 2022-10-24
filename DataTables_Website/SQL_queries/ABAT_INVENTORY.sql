SELECT [NAME] as 'Name'
      ,[PATH_NAME] as 'Path Name'
      ,[STATE] as 'State'
      ,[DESCRIPTION] as 'Description'
      ,SCHEDULE_OR_TRIGGER as 'Schedule or Trigger'
  FROM [SCDRunbook].[dbo].[ABAT_INVENTORY_LIST]
  ORDER BY NAME