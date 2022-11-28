USE [SCDRunbook]
GO

/****** Object:  View [dbo].[SCD_EXPORTS]    Script Date: 11/28/2022 11:03:26 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create view [dbo].[SCD_EXPORTS] AS (

/* List of SCD Exports (exporting to file or Message Queue). 
*/

SELECT 
SCD_CONFIG.[Batch Job Group],
SCD_CONFIG.[Batch Job],
SCD_CONFIG.[Batch Job Name],
--SCD_CONFIG.[Batch Task (IK)],
SCD_CONFIG.[Reference File Export],
ISNULL(SCD_REF_FILES.ENTIRE_REF_FILE_PATH,'') as 'ENTIRE_REFERENCE_FILE_STRING',
ISNULL(REPLACE(T_FILES_TO_FOLDER.TARGET_FOLDER,'\\bcimcs8\sharedir','S:'),'') AS 'LAN_OUTPUT',
SCD_CONFIG.[Extraction Setup],
SCD_CONFIG.[Data Format Setup],
SCD_CONFIG.[Extract Table],
ISNULL(ABAT.ABAT_PATH,'MANUAL') AS 'ACTIVE_BATCH_PATH'

FROM [SCDRunbook].[dbo].[SCD_CONFIG] SCD_CONFIG

OUTER APPLY (
    SELECT REPLACE(STRING_AGG([COMPONENT_TEXT],'') WITHIN GROUP (ORDER BY [COMPONENT_INDEX]),'\\','\') as REF_FILE_PATH FROM [SCDRunbook].[dbo].[SCD_REF_FILES]
	WHERE
    SCD_REF_FILES.REFERENCE_FILE = SCD_CONFIG.[Reference File Export] 
	AND SCD_REF_FILES.[COMPONENT_TYPE] != 'SimCorp Dimension directory'
) AS SCD_REF_FILES(ENTIRE_REF_FILE_PATH)

OUTER APPLY (

  SELECT 
  STRING_AGG(SP.PATH_NAME,'; ')  
  
  FROM [SCDRunbook].[dbo].[ABAT_BATCH_JOB_GROUPS_TO_PARENT] ABAT_BJG

  JOIN [SCDRunbook].[dbo].SCHEDULED_PLANS_LIST SP ON 
  SP.ID  = ABAT_BJG.[Job Plan ID]  

  WHERE 
  ABAT_BJG.[Batch Job Group Name] = SCD_CONFIG.[Batch Job Group]  AND
  (
  SP.PATH_NAME LIKE 'PROD/Scheduled_Plans/%' OR 
  SP.PATH_NAME LIKE 'PROD/Constraint_Triggered_Plans/%' OR 
  SP.PATH_NAME LIKE 'PROD/Adhoc_Plans/%'
  )
    
) as ABAT(ABAT_PATH) 

LEFT JOIN [SCDRunbook].[dbo].T_FILES_TO_FOLDER on [SCDRunbook].[dbo].T_FILES_TO_FOLDER.BATCH_JOB = SCD_CONFIG.[Batch Job]

WHERE 

SCD_CONFIG.[Batch Task (IK)] IN ('Extracts Exporter Definitions - Execute','Extraction Setups - Execute')

)
GO

