USE [SCDRunbook]
GO

/****** Object:  View [dbo].[SCD_IMPORTS]    Script Date: 11/28/2022 11:03:41 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


create view [dbo].[SCD_IMPORTS] AS (

/* List of SCD Imports (Batch tasks relating to imports). 
*/

SELECT 
SCD_CONFIG.[Batch Job Group],
SCD_CONFIG.[Batch Job],
SCD_CONFIG.[Batch Job Name],
SCD_CONFIG.[Reference File Import],
ISNULL(SCD_REF_FILES.ENTIRE_REF_FILE_PATH,'') as 'ENTIRE_REFERENCE_FILE_STRING',
SCD_CONFIG.[Data Format Setup],
ISNULL(ABAT.ABAT_PATH,'MANUAL') AS 'ACTIVE_BATCH_PATH'
--'TRANSLATED_DESCRIPTION' = REPLACE(REPLACE([dbo].TranslateString([SCDRunbook].[dbo].[ABAT_FILETRIGGERS].Description),'${',''),'}','')

FROM [SCDRunbook].[dbo].[SCD_CONFIG] SCD_CONFIG

OUTER APPLY (
    SELECT REPLACE(STRING_AGG([COMPONENT_TEXT],'') WITHIN GROUP (ORDER BY [COMPONENT_INDEX]),'\\','\') as REF_FILE_PATH FROM [SCDRunbook].[dbo].[SCD_REF_FILES]
	WHERE
    SCD_REF_FILES.REFERENCE_FILE = SCD_CONFIG.[Reference File Import] 
	AND SCD_REF_FILES.[COMPONENT_TYPE] != 'SimCorp Dimension directory'
) AS SCD_REF_FILES(ENTIRE_REF_FILE_PATH)

OUTER APPLY (

  SELECT 
  TP.PATH_NAME
  
  FROM [SCDRunbook].[dbo].[ABAT_BATCH_JOB_GROUPS_TO_PARENT] ABAT_BJG

  JOIN [SCDRunbook].[dbo].TRIGGERED_PLANS_LIST TP ON 
  TP.NAME  = ABAT_BJG.[Job Plan Name]

  WHERE 
  ABAT_BJG.[Batch Job Group Name] = SCD_CONFIG.[Batch Job Group]  
    
) as ABAT(ABAT_PATH) 

LEFT JOIN [SCDRunbook].[dbo].[ABAT_FILETRIGGERS] ON [SCDRunbook].[dbo].[ABAT_FILETRIGGERS].TriggeredPlan = ABAT.ABAT_PATH 

WHERE 

SCD_CONFIG.[Batch Task (IK)] IN (
'Data Format Setup - Execute - Import',
'Data Format Setup - Execute - Import to Message Queue',
'Data Import - Execute',
'Direct Filter/Data Format Setup Integration - Import',
--'File Operation - Move File',
--'General Reconciliation - Execute',
'Transfer File to Message Queue - Execute' )
AND (
SCD_CONFIG.[Batch Job Group] NOT LIKE '%MIG%' AND -- Ignore MIGRATION
SCD_CONFIG.[Batch Job Group] NOT LIKE '%BLB%'     -- Ignore BLB Import
)

)
GO

