## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| COSMOS_REPORTING_SSIS | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data and destination | SQL Server Auth likely |  CASE_CATEGORY_CD, CLIENT_CD, MISSION_CD CREATED_BY_USER_ID,  date_max_min_key, OPENEDDTLKP, FILEDDTLKP, PPTEXPIRYDTLKP, CASECREATIONDTLKP, DRV_PROCESS_DT_LKP, PERSON_CD | Part 1, 2, 3|
| COSMOS_STAGING_SSIS | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely            | CLIENT_CD            | Part 1, 2, 3|

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `COSMOS_Fact.dtsx` has the following structure:

*   **Variable Assignment:** Several user variables are assigned values using expressions. These variables appear to be used for ETL status tracking and SQL command generation.
*   **Expression Task:** `EXPRESSIONT- Fact Tables - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`: an expression task that simply evaluates `1 == 1`.
*   **Precedence Constraints:** The execution of the sequence containers depends on the value of the `$Project::PRJ_PRM_PROCESS_NODE` project parameter. If it is `ALL` or `FACT`, the `SEQC-F_CO_CASE_CLIENT` container will execute.
*   **Event Handlers:** Error and Post Execute event handlers are configured to update the ETL process status.

#### SEQC-F_CO_CASE_CLIENT

This sequence container truncates and loads staging data.

*   **Execute SQL Task:** `ESQLT- Truncate_F_CO_CASE_CLIENT`: Truncates the table `F_CO_CASE_CLIENT`.
*   **Data Flow Task:** `DFT- F_CO_CASE_CLIENT`:  Loads data into `F_CO_CASE_CLIENT`.
    *   **Source:** `OLEDB_SRC_S_CO_CASE_CLIENT` extracts data from a staging table `dbo.S_CO_CASE_CLIENT`.
    *   **Lookup Tables:**
        *   `LKP-D_CO_CLIENT`
        *   `LKP-D_CO_DATE`
        *   `LKP-D_CO_CASE_CATEGORY`
        *   `LKP-D_CO_CITIZENSHIP_SERVICE`
        *   `LKP-D_CO_IMMIGRATION_SERVICE`
        *   `LKP-D_CO_MISSION`
        *   `LKP-D_CO_GEO_COUNTRY`
        *   `LKP-S_CO_CITIZENSHIP_SERVICE`
    *   **Merge Joins:**
        *   Joins data from `OLEDB_SRC_S_CO_CASE_CLIENT` and `OLE DB_SRC_D_CO_CLIENT` based on `CASE_CD` and `CLIENT_CD`.
        *   Joins data from `ODBC SRC_D_CO_PASSPORT_SERVICE` with output from first Merge Join on `CASE_CD` and `CLIENT_CD`.
        *   Joins data from `OLE DB_SRC_D_CO_CASES` with output from second Merge Join on `CASE_CD`.
    *   **Script Component:** Performs date transformations and lookups.
    *   **Derived Column:** `DRV_TRFM-Unknown_Value`: Handles unknown members.
    *   **Derived Column:** This creates new columns and overwrites some existing ones.
    *   **Destination:** `OLEDB_DEST-F_CO_CASE_CLIENT`: Writes the transformed data to the `F_CO_CASE_CLIENT` table.

#### SEQC-F_CO_PASSPORT_SERVICE

This sequence container truncates and loads passport service data.

*   **Execute SQL Task:** `ESQLT- Truncate_F_CO_PASSPORT_SERVICE`: Truncates the table `F_CO_PASSPORT_SERVICE`.
*   **Data Flow Task:** `DFT-F_CO_PASSPORT_SERVICE`:  Loads data into `F_CO_PASSPORT_SERVICE`.
    *   **Source:** `OLEDB_SRC_S_CO_PASSPORT_SERVICE` extracts data from `dbo.S_CO_PASSPORT_SERVICE`.
    *   **Lookup Tables:**
        *   `LKP-D_CO_PASSPORT_SERVICE_PS`
        *   `LKP-D_CO_MISSION_GEO_COUNTRY_M`
        *   `LKP-D_CO_EMPLOYEE_E`
        *   `LKP-D_CO_EMPLOYEE_E1`
        *   `LKP-D_CO_DATE_ISSUE_DT_SID`
        *   `LKP-D_CO_DATE_EXPIRY_DT_SID`
        *   `LKP-D_CO_DATE_MAX_MIN_DT`
    *   **Derived Column:** `DRV_TRFM-Unknown_Value`: Handles unknown members.
    *   **Script Component:** Performs date transformations and lookups.
    *   **Destination:** `OLEDB_DEST_F_CO_PASSPORT_SERVICE`: Writes the transformed data to the `F_CO_PASSPORT_SERVICE` table.

#### SEQC-F_CO_PPT_WORKFLOW_STATUS

This sequence container truncates and loads passport workflow status data.

*   **Execute SQL Task:** `ESQLT- Truncate_F_CO_PPT_WORKFLOW_STATUS`: Truncates the table `F_CO_PPT_WORKFLOW_STATUS`.
*   **Data Flow Task:** `DFT-F_CO_PPT_WORKFLOW_STATUS`:  Loads data into `F_CO_PPT_WORKFLOW_STATUS`.
    *   **Source:** `OLEDB_SRC_S_CO_PPT_WORKFLOW_STATUS` extracts data from `dbo.S_CO_PPT_WORKFLOW_STATUS`.
    *   **Lookup Tables:**
        *   `LKP-D_CO_PASSPORT_SERVICE_PS`
        *   `LKP-D_CO_MISSION_GEO_COUNTRY_M`
        *   `LKP-D_CO_EMPLOYEE_E`
        *   `LKP-D_CO_EMPLOYEE_E1`
        *   `LKP-D_CO_CASES`
        *   `LKP-D_CO_PPT_WORKFLOW_STATUS`
        *   `LKP-D_CO_DATE_ISSUE_DT_SID`
        *   `LKP-D_CO_DATE_STATUS_MODIFIED_DT_SID`
        *   `LKP-D_CO_DATE_MAX_MIN_DT`
    *   **Derived Column:** `DRV_TRFM-Unknown_Value`: Handles unknown members.
    *   **Script Component:** Performs date transformations and lookups.
    *   **Destination:** `OLEDB_DEST_F_CO_PPT_WORKFLOW_STATUS`: Writes the transformed data to the `F_CO_PPT_WORKFLOW_STATUS` table.

## 4. Code Extraction

```sql
SELECT

       [CASE_CATEGORY_SID]
      ,[TYPE_CAT_CD]
      ,[CASE_CATEGORY_CD]


  FROM [dbo].[D_CO_CASE_CATEGORY]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_CASE_CATEGORY`.

```sql
select * from (SELECT

       [CASE_CATEGORY_SID]
      ,[TYPE_CAT_CD]
      ,[CASE_CATEGORY_CD]


  FROM [dbo].[D_CO_CASE_CATEGORY]) [refTable]
where [refTable].[CASE_CATEGORY_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_CASE_CATEGORY`.

```sql
SELECT [CITIZENSHIP_SERVICE_SID]
      ,[PERSON_CD]

  FROM [dbo].[D_CO_CITIZENSHIP_SERVICE]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_CITIZENSHIP_SERVICE`.

```sql
select * from (SELECT [CITIZENSHIP_SERVICE_SID]
      ,[PERSON_CD]

  FROM [dbo].[D_CO_CITIZENSHIP_SERVICE]) [refTable]
where [refTable].[PERSON_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_CITIZENSHIP_SERVICE`.

```sql
SELECT 1 as date_max_min_key,
 MAX(DAY_ID) as MAX_DATE,
 MIN(DAY_ID) as MIN_DATE
 
 FROM dbo.[D_CO_DATE]
 WHERE REC_TYPE='DIM'
```

Context: SQL query for Lookup Transformation `LKP-D_CO_DATE`.

```sql
select * from (SELECT 1 as date_max_min_key,
 MAX(DAY_ID) as MAX_DATE,
 MIN(DAY_ID) as MIN_DATE
 
 FROM dbo.[D_CO_DATE]
 WHERE REC_TYPE='DIM') [refTable]
where [refTable].[date_max_min_key] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_DATE`.

```sql
select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE"
```

Context: SQL query for Lookup Transformation `LKP-D_CO_DATE_CASE_CREAT_DT`.

```sql
select * from (select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE") [refTable]
where [refTable].[DATE_ID] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_DATE_CASE_CREAT_DT`.

```sql
SELECT
       [EMPLOYEE_SID]
      ,[EMPLOYEE_CD]
  FROM [dbo].[D_CO_EMPLOYEE]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_EMPLOYEE`.

```sql
select * from (SELECT
       [EMPLOYEE_SID]
      ,[EMPLOYEE_CD]
  FROM [dbo].[D_CO_EMPLOYEE]) [refTable]
where [refTable].[EMPLOYEE_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_EMPLOYEE`.

```sql
SELECT 
      [GEO_COUNTRY_SID]
      ,[COUNTRY_CD]
      --,[GEOGRAPHIC_REGION_CD]
	      
  FROM [dbo].[D_CO_GEO_COUNTRY]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_GEO_COUNTRY`.

```sql
select * from (SELECT 
      [GEO_COUNTRY_SID]
      ,[COUNTRY_CD]
      --,[GEOGRAPHIC_REGION_CD]
	      
  FROM [dbo].[D_CO_GEO_COUNTRY]) [refTable]
where [refTable].[COUNTRY_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_GEO_COUNTRY`.

```sql
SELECT [IMMIGRATION_SERVICE_SID]
      ,[PERSON_CD]


  FROM [dbo].[D_CO_IMMIGRATION_SERVICE]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_IMMIGRATION_SERVICE`.

```sql
select * from (SELECT [IMMIGRATION_SERVICE_SID]
      ,[PERSON_CD]


  FROM [dbo].[D_CO_IMMIGRATION_SERVICE]) [refTable]
where [refTable].[PERSON_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_IMMIGRATION_SERVICE`.

```sql
SELECT  [MISSION_SID]
      
              ,[MISSION_CD] 
	 
              ,[MISSION_TYPE_CD]
	  
              ,[SUPERVISORY_MISSION_SID]

  FROM [dbo].[D_CO_MISSION]
```

Context: SQL query for Lookup Transformation `LKP-D_CO_MISSION`.

```sql
select * from (SELECT  [MISSION_SID]
      
              ,[MISSION_CD] 
	 
              ,[MISSION_TYPE_CD]
	  
              ,[SUPERVISORY_MISSION_SID]

  FROM [dbo].[D_CO_MISSION]) [refTable]
where [refTable].[MISSION_CD] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_MISSION`.

```sql
SELECT
      [PERSON_CD]  
      ,cast(APPLICATION_DTM as date) AS CITS_APPLICATION_DT
      ,cast(TO_PROCESSING_DTM as date) AS CITS_TO_PROCESSING_DT  
      ,[PROCESSING_DAYS] AS CITS_PROCESSING_DAYS
      ,[PROCESSING_DAYS] AS CITS_PROCESSING_DAYS_CNT

  FROM [dbo].[S_CO_CITIZENSHIP_SERVICE]
```

Context: SQL query for Lookup Transformation `LKP-S_CO_CITIZENSHIP_SERVICE`.

```sql
select * from (SELECT
      [PERSON_CD]  
      ,cast(APPLICATION_DTM as date) AS CITS_APPLICATION_DT
      ,cast(TO_PROCESSING_DTM as date) AS CITS_TO_PROCESSING_DT  
      ,[PROCESSING_DAYS] AS CITS_PROCESSING_DAYS
      ,[PROCESSING_DAYS] AS CITS_PROCESSING_DAYS_CNT

  FROM [dbo].[S_CO_CITIZENSHIP_SERVICE]) [refTable]
where [refTable].[PERSON_CD] = ?
```

Context: Parameterized SQL query for 
Lookup Transformation `LKP-S_CO_CITIZENSHIP_SERVICE`.

```sql
WITH

NOTES(CASE_CD, LAST_NOTE_DTM, TOTAL_NOTE_CT)
AS

	  (SELECT distinct CASE_CD,
	         first_value(Entry_Dtm) over (partition by CASE_CD order by SEQUNCE_NBR desc) as LAST_NOTE_DTM,
			 Count(*) over (partition by CASE_CD) as TOTAL_NOTE_CT
	  FROM dbo.S_CO_CASE_NOTE
	  ) --do not take -3=null


SELECT   
                   C.CASE_CD
	,C.CASE_ID
                   ,C.CLIENT_CD
	,C.SNU_EN_NM
	,C.SNU_FR_NM
	,C.CASE_STATUS_CD
	,C.CASE_STATUS_EN_NM
	,C.CASE_STATUS_FR_NM
	,C.SUBJECT_DESCR
                   ,RC.value_nbr as RC_VALUE_NBR
	,RC.value_nbr AS CITS_SERV_STD_VALUE
	,C.CITY_NM
	,C.MISSION_MANAGER_CD
	,C.HQ_MANAGER_CD
	,C.HQ_UNIT_CD
	,C.CRISIS_IND
	,C.FILED_DTM AS C_FILED_DTM
                  ,C.OPENED_DTM  AS C_OPENED_DTM
	,CAST(C.FILED_DTM AS DATE) AS C_FILED_DT
                  --,CAST(C.FILED_DTM AS DATE) AS C_FILED_DT_DEST
                   ,CAST(C.OPENED_DTM AS DATE) AS C_OPENED_DT
	,C.CASE_REFERENCE_ID

	,NT.LAST_NOTE_DTM
	,cast(NT.LAST_NOTE_DTM as date) as LAST_NOTE_DT
    ,COALESCE(NT.TOTAL_NOTE_CT,0) as TOTAL_NOTE_CT

	
	,C.CASE_CREATION_DTM AS CASE_CREATION_DTM
	,CAST(C.CASE_CREATION_DTM AS DATE) AS  CASE_CREATION_DT
	,C.COUNTRY_CD
	,C.COMIP_CATEGORY_CD
                  ,C.CASE_CATEGORY_CD
	,C.MISSION_CD
	,C.CREATED_BY_USER_ID
	,1 AS "ROW_CNT"
	,1 AS date_max_min_key
	,getdate() AS ROW_INSERT_DTM
	,getdate() AS [ETL_CREA_DT]
	,getdate() AS [ETL_UPDT_DT]
FROM  dbo.S_CO_CASE_CLIENT AS C

LEFT JOIN NOTES AS NT ON NT.CASE_CD = C.CASE_CD

LEFT JOIN dbo.S_CO_COMMON_CODE_TABLE AS RC ON (
		C.CASE_CATEGORY_CD = RC.KEY_CD
		AND RC.KEY_TYPE_NM = 'COS_CASE_SERVICE_STANDARD'
		)

ORDER BY CASE_CD, CLIENT_CD
```

Context: SQL query for OLE DB Source `OLEDB_SRC_S_CO_CASE_CLIENT`.

```sql
TRUNCATE TABLE F_CO_CASE_CLIENT;
```

Context: SQL query for Execute SQL Task `ESQLT- Truncate_F_CO_CASE_CLIENT`.

```sql
select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE"
```

Context: SQL query for Lookup Transformation `LKP-D_CO_DATE_FILED_DT`.

```sql
select * from (select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE") [refTable]
where [refTable].[DATE_ID] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_DATE_FILED_DT`.

```sql
select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE"
```

Context: SQL query for Lookup Transformation `LKP-D_CO_DATE_OPEN_DT`.

```sql
select * from (select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE") [refTable]
where [refTable].[DATE_ID] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_DATE_OPEN_DT`.

```sql
select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE"
```

Context: SQL query for Lookup Transformation `LKP-D_CO_DATE_PPT_EXPIRY_DT`.

```sql
select * from (select "DATE_SID",
case when DATE_SID < 0 THEN REC_TYPE
     else cast(day_id as varchar)
end DATE_ID
from "dbo"."D_CO_DATE") [refTable]
where [refTable].[DATE_ID] = ?
```

Context: Parameterized SQL query for Lookup Transformation `LKP-D_CO_DATE_PPT_EXPIRY_DT`.

```sql
TRUNCATE TABLE F_CO_PASSPORT_SERVICE;
```

Context: SQL query for Execute SQL Task `ESQLT- Truncate_F_CO_PASSPORT_SERVICE`.

```sql
SELECT     --TOP(1000)
 	    CL.CASE_CD
                     ,CL.CLIENT_CD
                  --,PS.PERSON_CD
	   ,PS.PASSPORT_SERVICE_SID
	   ,PS.EXPIRY_DTM AS PPT_EXPIRY_DTM
	   ,PS.EXPIRY_DT AS PPT_EXPIRY_DT
	   ,PS.EXPIRY_DT AS PS_EXPIRY_DT
	--   ,PS.SERVICE_STREAM_ID 
	--   ,PS.APPLICATION_DTM AS PS_APPLICATION_DTM
	 -- ,PS.BOOKLET_RECEIVED_DTM
	   ,PS.ISSUE_DTM AS PS_ISSUE_DTM
	--   ,PS.FILED_DTM AS PS_FILED_DTM
	   ,PS.ISSUE_DT AS PS_ISSUE_DT
	   ,PS.PASSPORT_SERVICE_TYPE_CD	  
	   
FROM  dbo.D_CO_CLIENT CL

LEFT OUTER JOIN (

SELECT 	 
        PERSON_CD
	   ,PASSPORT_SERVICE_SID
	   ,EXPIRY_DTM
	   ,EXPIRY_DT
	 --  ,SERVICE_STREAM_ID
	--   ,APPLICATION_DTM
	-- ,BOOKLET_RECEIVED_DTM
	   ,ISSUE_DTM
	 --  ,FILED_DTM
	   ,ISSUE_DT
	   ,PASSPORT_SERVICE_TYPE_CD

FROM   dbo.D_CO_PASSPORT_SERVICE
	) PS ON (CL.CLIENT_CD = PS.PERSON_CD)

ORDER BY CL.CASE_CD, CL.CLIENT_CD
```

Context: SQL query for OLE DB Source `ODBC SRC_D_CO_PASSPORT_SERVICE`.

```sql
TRUNCATE TABLE F_CO_PPT_WORKFLOW_STATUS;
```

Context: SQL query for Execute SQL Task `ESQLT- Truncate_F_CO_PPT_WORKFLOW_STATUS`.

```sql
SELECT   --TOP(1000)
      [CASE_SID]
      ,[CASE_CD]

  FROM [dbo].[D_CO_CASES]
  ORDER BY [CASE_CD]
```

Context: SQL query for OLE DB Source `OLE DB_SRC_D_CO_CASES`.

```sql
SELECT   --TOP(1000)

   [CLIENT_SID]
  ,[CLIENT_CD]
  ,[CLIENT_CD] as [PERSON_CD]
  ,[CASE_CD]


FROM   [dbo].[D_CO_CLIENT]
              order by  [CASE_CD]  ,[CLIENT_CD]
```

Context: SQL query for OLE DB Source `OLE DB_SRC_D_CO_CLIENT`.

```sql
SELECT 
	 PS.PERSON_CD AS PERSON_CD
	,PS.ISSUE_DTM AS ISSUE_DTM	
	,PS.FILED_DTM AS FILED_DTM
	,PS.EXPIRY_DTM AS EXPIRY_DTM
	,PS.PPT_PROCESSING_END_DTM AS PPT_PROCESSING_END_DTM 
	,PS.BOOKLET_RECEIVED_DTM AS BOOKLET_RECEIVED_DTM	
	,CAST(PS.ISSUE_DTM AS DATE) AS ISSUE_DT
	,CAST(PS.FILED_DTM AS DATE) AS FILED_DT
	,CAST(PS.EXPIRY_DTM AS DATE) as EXPIRY_DT
                   ,CAST(PS.PPT_PROCESSING_END_DTM as DATE) as PPT_PROCESSING_END_DT
	,CAST(PS.BOOKLET_RECEIVED_DTM AS DATE) AS BOOKLET_RECEIVED_DT	
	,NULL AS PPT_PROCESSING_DAYS_CNT
	,NULL AS PPT_SERV_STD_VALUE
	,NULL AS PPT_SERV_STD_IND
	,1 AS "ROW_COUNT"
                   ,1 AS date_max_min_key
 	,PS.Mission_CD AS Mission_CD
	,PS.CREATED_EMPLOYEE__CD AS CREATED_EMPLOYEE_CD 
	,PS.REQUEST_APPROVAL_STATUS_EMPLOYEE AS REQUEST_APPROVAL_STATUS_EMPLOYEE
	,PS.APPROVAL_STATUS_EMPLOYEE_CD AS APPROVAL_STATUS_EMPLOYEE_CD	
                  ,getdate() as ROW_INSERT_DTM
	,getdate() AS [ETL_CREA_DT]
	,getdate() AS [ETL_UPDT_DT]
	
	
	
  FROM   dbo.S_CO_PASSPORT_SERVICE AS PS
    where not exists (select 1
	from [dbo].S_CO_PASSPORT_SERVICE_ARCHIVE a
	where a.PERSON_CD=PS.PERSON_CD) 
  UNION ALL
  
  
  SELECT 
	 PSA.PERSON_CD AS PERSON_CD
	,PSA.ISSUE_DTM AS ISSUE_DTM	
	,PSA.FILED_DTM AS FILED_DTM
	,PSA.EXPIRY_DTM AS EXPIRY_DTM
	,PSA.PPT_PROCESSING_END_DTM AS PPT_PROCESSING_END_DTM 
	,PSA.BOOKLET_RECEIVED_DTM AS BOOKLET_RECEIVED_DTM	
	,CAST(PSA.ISSUE_DTM AS DATE) AS ISSUE_DT
	,CAST(PSA.FILED_DTM AS DATE) AS FILED_DT
	,CAST(PSA.EXPIRY_DTM AS DATE) as EXPIRY_DT
                   ,CAST(PSA.PPT_PROCESSING_END_DTM as DATE) as PPT_PROCESSING_END_DT
	,CAST(PSA.BOOKLET_RECEIVED_DTM AS DATE) AS BOOKLET_RECEIVED_DT	
	,NULL AS DRV_PPT_PROCESSING_DAYS_CNT
	,NULL AS DRV_PPT_SERV_STD_VALUE
	,NULL AS DRV_PPT_SERV_STD_IND
	,1 AS "ROW_COUNT"
                  ,1 AS date_max_min_key
	,PSA.Mission_CD AS Mission_CD
	,PSA.CREATED_EMPLOYEE__CD AS CREATED_EMPLOYEE_CD 
	,PSA.REQUEST_APPROVAL_STATUS_EMPLOYEE AS REQUEST_APPROVAL_STATUS_EMPLOYEE
	,PSA.APPROVAL_STATUS_EMPLOYEE_CD AS APPROVAL_STATUS_EMPLOYEE_CD	
                  ,getdate() as ROW_INSERT_DTM
	,getdate() AS [ETL_CREA_DT]
	,getdate() AS [ETL_UPDT_DT]
  FROM dbo.S_CO_PASSPORT_SERVICE_ARCHIVE AS PSA
```

Context: SQL query for OLE DB Source `OLEDB_SRC_S_CO_PPT_WORKFLOW_STATUS`.

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'COSMOS_Master.dtsx' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'COSMOS_Fact.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: SQL query for updating the ETL status to FAILED.

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'COSMOS_Master.dtsx' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'COSMOS_Fact.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
```

Context: SQL query for updating the ETL status to SUCCEEDED.

```sql
INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )
VALUES (
 (
  SELECT ETL_COMPONENT_ID
  FROM ETL_COMPONENT
  WHERE ETL_COMPONENT_NM = 'COSMOS_Master.dtsx'   -- 'STRATEGIA_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'COSMOS_Master.dtsx'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS' 
    )
   AND ETL_SUB_COMPONENT_NM = 'COSMOS_Fact.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: SQL query for inserting into `ETL_RUN_STATUS` with RUNNING status.

```csharp
        
        //3. DRV_PROCESS_DT_LKP

      

            if (Row.TYPECATCD == 4)
            {
                if (Row.PSISSUEDT_IsNull )
                { Row.DRVPROCESSDTLKP = "NULL"; }
                else if (Row.PSISSUEDT > Row.MAXDATE)
                { Row.DRVPROCESSDTLKP = "FUTURE"; }
                else if (Row.PSISSUEDT < Row.MINDATE)
                { Row.DRVPROCESSDTLKP = "PAST"; }
                else
                { Row.DRVPROCESSDTLKP = Row.PSISSUEDT.ToString("yyyy-MM-dd") ; }
            }

            else
            {
                if (Row.COPENEDDT_IsNull)
                { Row.DRVPROCESSDTLKP = "NULL"; }
                else if (Row.COPENEDDT > Row.MAXDATE)
                { Row.DRVPROCESSDTLKP = "FUTURE"; }
                else if (Row.COPENEDDT < Row.MINDATE)
                { Row.DRVPROCESSDTLKP = "PAST"; }
                else
                { Row.DRVPROCESSDTLKP = Row.COPENEDDT.ToString("yyyy-MM-dd") ; }
            }

        
     

        //5. OPENED_DT_LKP

        if (Row.COPENEDDT_IsNull)
        { Row.OPENEDDTLKP = "NULL"; }
        else if (Row.COPENEDDT > Row.MAXDATE)
        { Row.OPENEDDTLKP = "FUTURE"; }
        else if (Row.COPENEDDT < Row.MINDATE)
        { Row.OPENEDDTLKP = "PAST"; }
        else
        { Row.OPENEDDTLKP = Row.COPENEDDT.ToString("yyyy-MM-dd") ; }

        

        //7. FILED_DT_LKP 

        if (Row.CFILEDDT_IsNull)
        { Row.FILEDDTLKP = "NULL"; }
        else if (Row.CFILEDDT > Row.MAXDATE)
        { Row.FILEDDTLKP = "FUTURE"; }
        else if (Row.CFILEDDT < Row.MINDATE)
        { Row.FILEDDTLKP = "PAST"; }
        else
        { Row.FILEDDTLKP = Row.CFILEDDT.ToString("yyyy-MM-dd") ; }

       

        //8.PPT_EXPIRY_DT_LKP
        if (Row.PSEXPIRYDT_IsNull)
        { Row.PPTEXPIRYDTLKP = "NULL"; }
        else if (Row.PSEXPIRYDT > Row.MAXDATE)
        { Row.PPTEXPIRYDTLKP = "FUTURE"; }
        else if (Row.PSEXPIRYDT < Row.MINDATE)
        { Row.PPTEXPIRYDTLKP = "PAST"; }
        else
        { Row.PPTEXPIRYDTLKP = Row.PSEXPIRYDT.ToString("yyyy-MM-dd"); }


       

        //9. CASE_CREATION_DT_LKP
        if (!Row.CASECREATIONDT_IsNull)
        { 
            if (Row.CASECREATIONDT > Row.MAXDATE)
            { Row.CASECREATIONDTLKP = "FUTURE"; }
             else if (Row.CASECREATIONDT < Row.MINDATE)
            { Row.CASECREATIONDTLKP = "PAST"; }
        else
        { Row.CASECREATIONDTLKP = Row.CASECREATIONDT.ToString("yyyy-MM-dd") ; }
        }
        else
        { Row.CASECREATIONDTLKP = "NULL"; }
```

Context: C# code from the Script Component to get date