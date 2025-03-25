```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_GC_REPORTING         | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for reference data | SQL Server Auth likely  | None            | All DFTs                  |
| SAP_SOURCE         | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for reference data | SQL Server Auth likely  | None            | All DFTs                  |
| Project.ConnectionManagers[MART_GC_REPORTING] | OLE DB | Server: [Inferred], Database: [Inferred] | Destination for reference data | SQL Server Auth likely | None | DFT- R_GCS_COMMITMENT_ITEM_MAP, DFT- R_GCS_COST_CENTRE_MAP, DFT- R_GCS_FUND_CENTRE_MAP 1, DFT- R_GCS_FUND_MAP, DFT- R_GCS_GL_ACCOUNT_MAP, DFT- R_GCS_IM_POSITION_MAP, DFT- R_GCS_WBS_MAP |
| Project.ConnectionManagers[SAP_SOURCE] | OLE DB | Server: [Inferred], Database: [Inferred] | Source for reference data | SQL Server Auth likely | None | DFT- R_GCS_COMMITMENT_ITEM_MAP, DFT- R_GCS_COST_CENTRE_MAP, DFT- R_GCS_FUND_CENTRE_MAP 1, DFT- R_GCS_FUND_MAP, DFT- R_GCS_GL_ACCOUNT_MAP, DFT- R_GCS_IM_POSITION_MAP, DFT- R_GCS_WBS_MAP |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All Parts|

## 3. Package Flow Analysis

#### Control Flow

*   `EXPRESSIONT- PROJECT REFERENCE - Start Task - ProcessDataFlowNode`: Expression task to evaluate if the process should execute.
*   `SEQC-Reference Tables`: Sequence Container containing the data flow tasks.
    *   Precedence Constraint: `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT")`
*   Inside `SEQC-Reference Tables`:
    *   `ESQLT- Truncate Reference Tables`: Truncates the reference tables.
    *   `DFT- R_GCS_COMMITMENT_ITEM_MAP`: Data flow task to load data into `R_GCS_COMMITMENT_ITEM_MAP`.
    *   `DFT- R_GCS_COST_CENTRE_MAP`: Data flow task to load data into `R_GCS_COST_CENTRE_MAP`.
    *   `DFT- R_GCS_FUND_MAP`: Data flow task to load data into `R_GCS_FUND_MAP`.
    *   `DFT- R_GCS_FUND_CENTRE_MAP 1`: Data flow task to load data into `R_GCS_FUND_CENTRE_MAP`.
    *   `DFT- R_GCS_GL_ACCOUNT_MAP`: Data flow task to load data into `R_GCS_GL_ACCOUNT_MAP`.
    *   `DFT- R_GCS_IM_POSITION_MAP`: Data flow task to load data into `R_GCS_IM_POSITION_MAP`.
    *   `DFT- R_GCS_WBS_MAP`: Data flow task to load data into `R_GCS_WBS_MAP`.

#### DFT- R_GCS_COMMITMENT_ITEM_MAP

*   **Source:** `OLEDB_SRC-ZOAT_FIPEX_MAP` extracts data from `dbo.ZOAT_FIPEX_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:** None
*   **Destinations:** `OLEDB_DEST-R_GCS_COMMITMENT_ITEM_MAP` saves the data to `dbo.R_GCS_COMMITMENT_ITEM_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_COST_CENTRE_MAP

*   **Sources:**
    *   `OLEDB_SRC-ZOAT_KOSTL_MAP` extracts data from `dbo.ZOAT_KOSTL_MAP` using the `SAP_SOURCE` connection.
    *   `OLEDB_SRC-R_GCS_FUND_CENTRE_MAP` extracts data from `dbo.R_GCS_COST_CENTRE_MAP` using the `MART_GC_REPORTING` connection.
*   **Transformations:**
    *   `MRJ_TRFM`: Merge Join transformation.
    *   `CSPLIT_TRFM`: Conditional Split transformation to route data based on whether `GCS_COST_CENTRE_NBR` or `FAS_COST_CENTRE_NBR` are NULL.
*   **Destinations:** `OLEDB_DEST-R_GCS_COST_CENTRE_MAP` saves the data to `dbo.R_GCS_COST_CENTRE_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_FUND_CENTRE_MAP 1

*   **Source:** `OLEDB_SRC-ZOAT_FICTR_MAP` extracts data from `dbo.ZOAT_FICTR_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:** None
*   **Destinations:** `OLEDB_DEST-R_GCS_FUND_CENTRE_MAP` saves the data to `dbo.R_GCS_FUND_CENTRE_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_FUND_MAP

*   **Source:** `OLEDB_SRC-ZOAT_GEBER_MAP` extracts data from `dbo.ZOAT_GEBER_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:**
    *   `DCNV_TRFM`: Data Conversion transformation to convert `GCS_GEBER` and `FAS_GEBER` to wstr.
*   **Destinations:** `OLEDB_DEST-R_GCS_FUND_MAP` saves the data to `dbo.R_GCS_FUND_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_GL_ACCOUNT_MAP

*   **Source:** `OLEDB_SRC-ZOAT_SAKNR_MAP` extracts data from `dbo.ZOAT_SAKNR_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:**
    *   `DCNV_TRFM`: Data Conversion transformation to convert `GCS_SAKNR` and `FAS_SAKNR` to wstr.
*   **Destinations:** `OLEDB_DEST-R_GCS_GL_ACCOUNT_MAP` saves the data to `dbo.R_GCS_GL_ACCOUNT_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_IM_POSITION_MAP

*   **Source:** `OLEDB_SRC-ZOAT_IMPR_MAP` extracts data from `dbo.ZOAT_IMPR_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:**
    *   `DCVN_TRFM`: Data Conversion transformation to convert `GCS_POSNR` and `FAS_POSNR` to wstr.
*   **Destinations:** `OLEDB_DEST-R_GCS_IM_POSITION_MAP` saves the data to `dbo.R_GCS_IM_POSITION_MAP` using the `MART_GC_REPORTING` connection.

#### DFT- R_GCS_WBS_MAP

*   **Source:** `OLEDB_SRC-ZOAT_WBS_MAP` extracts data from `dbo.ZOAT_WBS_MAP` using the `SAP_SOURCE` connection.
*   **Transformations:**
    *   `DCNV-TRFM`: Data Conversion transformation to convert `GCS_POSID_INT` and `FAS_POSID` to wstr.
*   **Destinations:** `OLEDB_DEST-R_GCS_WBS_MAP` saves the data to `dbo.R_GCS_WBS_MAP` using the `MART_GC_REPORTING` connection.

## 4. Code Extraction

```sql
-- From OLEDB_SRC-ZOAT_FIPEX_MAP
SELECT	
	"GCS_FIPEX",
	"FAS_FIPEX",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_FIPEX_MAP"
```

```sql
-- From OLEDB_SRC-R_GCS_FUND_CENTRE_MAP
SELECT   distinct [GCS_COST_CENTRE_NBR]
      ,[FAS_COST_CENTRE_NBR]
  FROM [dbo].[R_GCS_COST_CENTRE_MAP] 
ORDER BY  [GCS_COST_CENTRE_NBR]
      ,[FAS_COST_CENTRE_NBR]
```

```sql
-- From OLEDB_SRC-ZOAT_KOSTL_MAP
SELECT	distinct
	"GCS_KOSTL",
	"FAS_KOSTL",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_KOSTL_MAP"
order by "GCS_KOSTL",
	"FAS_KOSTL"
```

```sql
-- From OLEDB_SRC-ZOAT_FICTR_MAP
SELECT
	CAST("GCS_FICTR" AS VARCHAR(6) )  AS GCS_FICTR,
	CAST("FAS_FICTR"  AS VARCHAR(6) ) AS FAS_FICTR ,
GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT
FROM   "dbo"."ZOAT_FICTR_MAP"
```

```sql
-- From OLEDB_SRC-ZOAT_GEBER_MAP
SELECT	
	"GCS_GEBER",
	"FAS_GEBER",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_GEBER_MAP"
```

```sql
-- From OLEDB_SRC-ZOAT_SAKNR_MAP
SELECT	
	"GCS_SAKNR",
	"FAS_SAKNR",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_SAKNR_MAP"
```

```sql
-- From OLEDB_SRC-ZOAT_IMPR_MAP
SELECT	
	 GCS_POSNR,
	"PRNAM",
	"POSID",
	"GJAHR",
	 FAS_POSNR ,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_IMPR_MAP"
```

```sql
-- From OLEDB_SRC-ZOAT_WBS_MAP
SELECT
	"GCS_POSID_INT",
	"FAS_POSID",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_WBS_MAP"
```

```sql
-- From ESQLT- Truncate Reference Tables
TRUNCATE TABLE dbo.R_GCS_COMMITMENT_ITEM_MAP;
TRUNCATE TABLE dbo.R_GCS_COST_CENTRE_MAP;
TRUNCATE TABLE dbo.R_GCS_FUND_MAP;
TRUNCATE TABLE dbo.R_GCS_GL_ACCOUNT_MAP;
TRUNCATE TABLE dbo.R_GCS_FUND_CENTRE_MAP;
TRUNCATE TABLE dbo.R_GCS_IM_POSITION_MAP;
TRUNCATE TABLE dbo.R_GCS_WBS_MAP;
```

```sql
-- From Package.EventHandlers[OnError]\ESQLT- Update ETL Process Status to Failed
-- Value from Variable User::V_SQL_UPDATE_ON_ERROR
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
   ETL_COMPONENT_NM = 'GC_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/GC'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PROJECT_REFERENCE.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

```sql
-- From Package.EventHandlers[OnPostExecute]\ESQLT- Update ETL Process Status to Succeeded
-- Value from Variable User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   ETL_COMPONENT_NM = 'GC_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/GC' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PROJECT_REFERENCE.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
```

```sql
-- From Package.EventHandlers[OnPreExecute]\ESQLT- Create Record  with Running Status
-- Value from Variable User::V_SQL_INSERT_ON_PRE_EXECUTE
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
  WHERE ETL_COMPONENT_NM = 'GC_MASTER.DTSX'   -- 'STRATEGIA_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/GC'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'GC_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/GC' 
    )
   AND ETL_SUB_COMPONENT_NM = 'PROJECT_REFERENCE.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

#### Expression Evaluators:

```
@[System::PackageName] + ".DTSX"
```

```
"
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
  WHERE ETL_COMPONENT_NM = '"+ @[$Project::PRJ_PRM_MAIN_JOB] +"'   -- 'STRATEGIA_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = '"+ @[$Project::PRJ_PRM_DEVOPS_PATH] +"'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = '"+ @[$Project::PRJ_PRM_MAIN_JOB] +"'
     AND ETL_REPOSITORY_FULL_PATH = '"+ @[$Project::PRJ_PRM_DEVOPS_PATH] +"' 
    )
   AND ETL_SUB_COMPONENT_NM = '"+ @[User::V_ETL_COMPONENT_NAME] +"'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
"
```

```
"
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
   ETL_COMPONENT_NM = '"+ @[$Project::PRJ_PRM_MAIN_JOB] +"' 
   AND ETL_REPOSITORY_FULL_PATH = '"+ @[$Project::PRJ_PRM_DEVOPS_PATH] +"'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = '"+ @[User::V_ETL_COMPONENT_NAME] +"'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
"
```

```
"

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
   ETL_COMPONENT_NM = '"+ @[$Project::PRJ_PRM_MAIN_JOB] +"' 
   AND ETL_REPOSITORY_FULL_PATH = '"+ @[$Project::PRJ_PRM_DEVOPS_PATH] +"' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = '"+ @[User::V_ETL_COMPONENT_NAME] +"'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
"
```

```
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT")
```

```
@[System::SourceName]==@[System::PackageName]
```

## 5. Output Analysis

| Destination Table            | Description                                   | Source Part |
|-----------------------------|-----------------------------------------------|-------------|
| dbo.R_GCS_COMMITMENT_ITEM_MAP | Stores the mapping between GCS and FAS commitment items | DFT- R_GCS_COMMITMENT_ITEM_MAP |
| dbo.R_GCS_COST_CENTRE_MAP   | Stores the mapping between GCS and FAS cost centers       | DFT- R_GCS_COST_CENTRE_MAP   |
| dbo.R_GCS_FUND_MAP          | Stores the mapping between GCS and FAS funds               | DFT- R_GCS_FUND_MAP          |
| dbo.R_GCS_GL_ACCOUNT_MAP     | Stores the mapping between GCS and FAS GL accounts          | DFT- R_GCS_GL_ACCOUNT_MAP     |
| dbo.R_GCS_FUND_CENTRE_MAP   | Stores the mapping between GCS and FAS fund centers         | DFT- R_GCS_FUND_CENTRE_MAP 1  |
| dbo.R_GCS_IM_POSITION_MAP    | Stores the mapping between GCS and FAS IM positions        | DFT- R_GCS_IM_POSITION_MAP    |
| dbo.R_GCS_WBS_MAP           | Stores the mapping between GCS and FAS WBS elements        | DFT- R_GCS_WBS_MAP           |

## 6. Package Summary

*   **Input Connections:** 2
*   **Output Destinations:** 7 reference tables.
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 7
    *   Expression Tasks: 3
    *   Execute SQL Tasks: 4
    *   Data Conversion: Frequent
    *   Merge Join: 1
    * Conditional Split: 1
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: The merge join in `DFT- R_GCS_COST_CENTRE_MAP` could be a bottleneck if the inputs are not properly sorted.
*   Critical path analysis: The sequence of data flow tasks within the "SEQC-Reference Tables" sequence container is the critical path.
*   Error handling mechanisms: The package uses OnError, OnPreExecute, OnPostExecute event handlers to log ETL process status to ETL_RUN_STATUS table.
```