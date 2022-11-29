USE [SCDRunbook]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/* List of all Triggered Plans in PROD */
IF OBJECT_ID('dbo.TRIGGERED_PLANS_LIST', 'V') IS NOT NULL
DROP VIEW [dbo].[TRIGGERED_PLANS_LIST]
GO
CREATE VIEW [dbo].[TRIGGERED_PLANS_LIST] AS
  SELECT 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].NAME, 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].STATE,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].DESCRIPTION,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].ID

  FROM [SCDRunbook].[dbo].[ABAT_PATHNAMES] 
  
  WHERE 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].OBJECT_TYPE = 'JobPlan' AND 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME LIKE 'PROD/Triggered_Plans/%'
GO

/* List of all Adhoc Plans in PROD */
IF OBJECT_ID('dbo.ADHOC_PLANS_LIST', 'V') IS NOT NULL
DROP VIEW [dbo].[ADHOC_PLANS_LIST]
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

/* List of all Scheduled Plans in PROD */
IF OBJECT_ID('dbo.SCHEDULED_PLANS_LIST', 'V') IS NOT NULL
DROP VIEW [dbo].[SCHEDULED_PLANS_LIST]
GO
CREATE VIEW [dbo].[SCHEDULED_PLANS_LIST] AS

  SELECT 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].NAME, 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].STATE,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].DESCRIPTION,
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].ID,
  SCD_SCHEDULE_TIMES.ENTIRE_SCHEDULES

  FROM [SCDRunbook].[dbo].[ABAT_PATHNAMES] 

  OUTER APPLY (
    SELECT STRING_AGG(FORMAT(TIMES,'hh:mm tt'),'; ') WITHIN GROUP (ORDER BY TIMES) as SCHEDULE FROM [SCDRunbook].[dbo].[ABAT_SCHEDULED_PLANS]
	INNER JOIN [SCDRunbook].[dbo].[ABAT_SCHEDULES] ON [SCDRunbook].[dbo].[ABAT_SCHEDULES].ScheduleName = [SCDRunbook].[dbo].[ABAT_SCHEDULED_PLANS].SCHEDULE
	WHERE
    [SCDRunbook].[dbo].[ABAT_SCHEDULED_PLANS].ID = [SCDRunbook].[dbo].[ABAT_PATHNAMES].ID 
	
) AS SCD_SCHEDULE_TIMES(ENTIRE_SCHEDULES)

  WHERE 
    
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].OBJECT_TYPE = 'JobPlan' AND 
  (
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME LIKE 'PROD/Scheduled_Plans/%' OR 
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME LIKE 'PROD/Constraint_Triggered_Plans/%'
  )
  AND 
  (
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME NOT LIKE 'PROD/Scheduled_Plans/Admin/%' AND
  [SCDRunbook].[dbo].[ABAT_PATHNAMES].PATH_NAME NOT LIKE 'PROD/Scheduled_Plans/Constraint_And_Plan_Checks/CHECK_FILE_AGE/%' 
  )
GO

/* List of SCD Exports (exporting to file or Message Queue). */
IF OBJECT_ID('dbo.SCD_EXPORTS', 'V') IS NOT NULL
DROP VIEW [dbo].[SCD_EXPORTS]
GO
CREATE view [dbo].[SCD_EXPORTS] AS (
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

/* List of SCD Imports (Batch tasks relating to imports). */
IF OBJECT_ID('dbo.SCD_IMPORTS', 'V') IS NOT NULL
DROP VIEW [dbo].[SCD_IMPORTS]
GO
create view [dbo].[SCD_IMPORTS] AS (
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

IF OBJECT_ID('dbo.ABAT_INVENTORY_LIST', 'V') IS NOT NULL
DROP VIEW [dbo].[ABAT_INVENTORY_LIST]
GO
CREATE VIEW [dbo].[ABAT_INVENTORY_LIST] AS 

SELECT
[NAME],
[PATH_NAME],
[STATE],
[DESCRIPTION],
'SCHEDULE_OR_TRIGGER' = ISNULL([ENTIRE_SCHEDULES],'N/A')
FROM [SCDRunbook].[dbo].[SCHEDULED_PLANS_LIST]

UNION

SELECT 

[NAME],
[PATH_NAME],
[STATE],
[DESCRIPTION],
'SCHEDULE_OR_TRIGGER' = 'ADHOC'
FROM [SCDRunbook].[dbo].[ADHOC_PLANS_LIST]

UNION

SELECT 

TP.[NAME],
TP.[PATH_NAME],
TP.[STATE],
TP.[DESCRIPTION],
'SCHEDULE_OR_TRIGGER' = ISNULL(ABAT_TRIGGERS.TRIGGERS,'N/A')
FROM [SCDRunbook].[dbo].[TRIGGERED_PLANS_LIST] TP

OUTER APPLY (
    SELECT STRING_AGG([SCDRunbook].[dbo].TranslateString(REPLACE(REPLACE([SCDRunbook].[dbo].TranslateString([SCDRunbook].[dbo].[ABAT_FILETRIGGERS].Description),'${',''),'}','')),'; ') WITHIN GROUP (ORDER BY NAME) as TRIGGERS FROM [SCDRunbook].[dbo].[ABAT_FILETRIGGERS]
	INNER JOIN [SCDRunbook].[dbo].[TRIGGERED_PLANS_LIST] ON [SCDRunbook].[dbo].[ABAT_FILETRIGGERS].TriggeredPlan = [SCDRunbook].[dbo].[TRIGGERED_PLANS_LIST].NAME  
    WHERE [SCDRunbook].[dbo].[ABAT_FILETRIGGERS].TriggeredPlan = TP.NAME
) AS ABAT_TRIGGERS(TRIGGERS)
GO