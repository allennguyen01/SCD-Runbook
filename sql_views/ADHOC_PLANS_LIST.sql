USE [SCDRunbook]
GO

/****** Object:  View [dbo].[ADHOC_PLANS_LIST]    Script Date: 11/28/2022 11:03:13 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE VIEW [dbo].[ADHOC_PLANS_LIST] AS

  SELECT 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].NAME, 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].STATE,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].DESCRIPTION,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].ID

  FROM [SCDRunbook].[dbo].[ABAT_PATHNAMES] 


  WHERE 
    
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].OBJECT_TYPE = 'JobPlan' AND 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME LIKE 'PROD/Adhoc_Plans/%'  

GO

