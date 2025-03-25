## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| GC_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for ZOAT mapping tables |  SQL Server Auth likely | None            | All DFTs                  |
| SAP_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source of ZOAT mapping tables | SQL Server Auth likely            |  All DFTs                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All Parts|

## 3. Package Flow Analysis

The package's control flow begins with an Expression Task that sets the stage for subsequent data flow tasks. The package then proceeds to execute two main sequence containers named `SEQC-1_Mapping_ZOAT_FKBER_MAP` and `SEQC-2_Mapping_ZOAT_BLAND_MAP`, and `SEQC-3_Mapping_ZOAT_PORD_MAP`. These sequence containers encapsulate a series of data flow tasks that extract, transform, and load mapping data from SAP_SOURCE to GC_SOURCE. The execution of these sequence containers depends on the value of the project parameter `PRJ_PRM_PROCESS_NODE`.

#### SEQC- 1_Mapping_ZOAT_FKBER_MAP

*   Begins by truncating tables in the SQL Server database.
*   **DFT- ZOAT_FKBER_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_FKBER_MAP) extracts data from `dbo.ZOAT_FKBER_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_FKBER_MAP) loads data into `dbo.ZOAT_FKBER_MAP` in GC_SOURCE.
*   **DFT- ZOAT_GEBER_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_GEBER_MAP) extracts data from `dbo.ZOAT_GEBER_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_GEBER_MAP) loads data into `dbo.ZOAT_GEBER_MAP` in GC_SOURCE.
*   **DFT- ZOAT_IMPR_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_IMPR_MAP) extracts data from `dbo.ZOAT_IMPR_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_IMPR_MAP) loads data into `dbo.ZOAT_IMPR_MAP` in GC_SOURCE.
*   **DFT- ZOAT_KOSTL_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_KOSTL_MAP) extracts data from `dbo.ZOAT_KOSTL_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_KOSTL_MAP) loads data into `dbo.ZOAT_KOSTL_MAP` in GC_SOURCE.
*   **DFT- ZOAT_MWSKZ_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_MWSKZ_MAP) extracts data from `dbo.ZOAT_MWSKZ_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_MWSKZ_MAP) loads data into `dbo.ZOAT_MWSKZ_MAP` in GC_SOURCE.
*   All data flow tasks run sequentially.
*   Error handling is set to `FailComponent`.

#### SEQC- 2_Mapping_ZOAT_BLAND_MAP

*   Begins by truncating tables in the SQL Server database.
*   **DFT- ZOAT_BLAND_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_BLAND_MAP) extracts data from `dbo.ZOAT_BLAND_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_BLAND_MAP) loads data into `dbo.ZOAT_BLAND_MAP` in GC_SOURCE.
*   **DFT- ZOAT_BLART_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_BLART_MAP) extracts data from `dbo.ZOAT_BLART_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_BLART_MAP) loads data into `dbo.ZOAT_BLART_MAP` in GC_SOURCE.
*   **DFT- ZOAT_BSART_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_BSART_MAP) extracts data from `dbo.ZOAT_BSART_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_BSART_MAP) loads data into `dbo.ZOAT_BSART_MAP` in GC_SOURCE.
*   **DFT- ZOAT_EKGRP_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_EKGRP_MAP) extracts data from `dbo.ZOAT_EKGRP_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_EKGRP_MAP) loads data into `dbo.ZOAT_EKGRP_MAP` in GC_SOURCE.
*   **DFT- ZOAT_FICTR_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_FICTR_MAP) extracts data from `dbo.ZOAT_FICTR_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_FICTR_MAP) loads data into `dbo.ZOAT_FICTR_MAP` in GC_SOURCE.
*   **DFT- ZOAT_FIPEX_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_FIPEX_MAP) extracts data from `dbo.ZOAT_FIPEX_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_FIPEX_MAP) loads data into `dbo.ZOAT_FIPEX_MAP` in GC_SOURCE.
*   All data flow tasks run sequentially.
*   Error handling is set to `FailComponent`.

#### SEQC-3_Mapping_ZOAT_PORD_MAP

*   Begins by truncating tables in the SQL Server database.
*   **DFT- ZOAT_PORD_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_PORD_MAP) extracts data from `dbo.ZOAT_PORD_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_PORD_MAP) loads data into `dbo.ZOAT_PORD_MAP` in GC_SOURCE.
*   **DFT- ZOAT_PREQ_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_PREQ_MAP) extracts data from `dbo.ZOAT_PREQ_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_PREQ_MAP) loads data into `dbo.ZOAT_PREQ_MAP` in GC_SOURCE.
*   **DFT- ZOAT_SAKNR_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_SAKNR_MAP) extracts data from `dbo.ZOAT_SAKNR_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_SAKNR_MAP) loads data into `dbo.ZOAT_SAKNR_MAP` in GC_SOURCE.
*   **DFT- ZOAT_USNAM_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_USNAM_MAP) extracts data from `dbo.ZOAT_USNAM_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_USNAM_MAP) loads data into `dbo.ZOAT_USNAM_MAP` in GC_SOURCE.
*   **DFT- ZOAT_WBS_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_WBS_MAP) extracts data from `dbo.ZOAT_WBS_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_WBS_MAP) loads data into `dbo.ZOAT_WBS_MAP` in GC_SOURCE.
*  **DFT- ZOAT_ZLSCH_MAP:**
    *   **Source:** OLE DB Source (OLEDB_SRC-ZOAT_ZLSCH_MAP) extracts data from `dbo.ZOAT_ZLSCH_MAP` in SAP_SOURCE.
    *   **Destination:** OLE DB Destination (OLEDB_DEST-ZOAT_ZLSCH_MAP) loads data into `dbo.ZOAT_ZLSCH_MAP` in GC_SOURCE.
    *   This task is disabled.
*   All data flow tasks run sequentially.
*   Error handling is set to `FailComponent`.

## 4. Code Extraction

```markdown
-- From ESQLT- Truncate Staging Tables_In_SEQC- 1_Mapping_ZOAT_FKBER_MAP
TRUNCATE TABLE dbo.ZOAT_FKBER_MAP;
TRUNCATE TABLE dbo.ZOAT_GEBER_MAP;
TRUNCATE TABLE dbo.ZOAT_IMPR_MAP;
TRUNCATE TABLE dbo.ZOAT_KOSTL_MAP;
TRUNCATE TABLE dbo.ZOAT_MWSKZ_MAP;
```

Context: This T-SQL code truncates the specified tables.

```sql
-- From OLEDB_SRC-ZOAT_FKBER_MAP
SELECT	"MANDT",
	"GCS_FKBER",
	"FAS_FKBER",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_FKBER_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_FKBER_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_GEBER_MAP
SELECT	"MANDT",
	"GCS_FIKRS",
	"GCS_GEBER",
	"FAS_GEBER",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_GEBER_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_GEBER_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_IMPR_MAP
SELECT	"CLIENT",
	"GCS_OBJNR",
	"GCS_POSNR",
	"PRNAM",
	"POSID",
	"GJAHR",
	"FAS_OBJNR",
	"FAS_POSNR",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_IMPR_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_IMPR_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_KOSTL_MAP
SELECT	"MANDT",
	"GCS_KOKRS",
	"GCS_KOSTL",
	"GCS_DATBI",
	"GCS_DATAB",
	"FAS_KOSTL",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_KOSTL_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_KOSTL_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_MWSKZ_MAP
SELECT	"MANDT",
	"GCS_MWSKZ",
	"FAS_MWSKZ",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_MWSKZ_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_MWSKZ_MAP`.

```sql
-- From ESQLT- Truncate Staging Tables_In_SEQC- 2_Mapping_ZOAT_BLAND_MAP
TRUNCATE TABLE dbo.ZOAT_BLAND_MAP;
TRUNCATE TABLE dbo.ZOAT_BLART_MAP;
TRUNCATE TABLE dbo.ZOAT_BSART_MAP;
TRUNCATE TABLE dbo.ZOAT_EKGRP_MAP;
TRUNCATE TABLE dbo.ZOAT_FICTR_MAP;
TRUNCATE TABLE dbo.ZOAT_FIPEX_MAP;
```

Context: This T-SQL code truncates the specified tables.

```sql
-- From OLEDB_SRC-ZOAT_BLAND_MAP
SELECT	"MANDT",
	"GCS_LAND1",
	"GCS_BLAND",
	"FAS_LAND1",
	"FAS_BLAND",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_BLAND_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_BLAND_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_BLART_MAP
SELECT	"MANDT",
	"GCS_BLART",
	"FAS_BLART",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_BLART_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_BLART_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_BSART_MAP
SELECT	"MANDT",
	"GCS_BSTYP",
	"GCS_BSART",
	"FAS_BSART",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_BSART_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_BSART_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_EKGRP_MAP
SELECT	"MANDT",
	"GCS_EKGRP",
	"FAS_EKGRP",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_EKGRP_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_EKGRP_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_FICTR_MAP
SELECT	"MANDT",
	"GCS_FICTR",
	"FAS_FICTR",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_FICTR_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_FICTR_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_FIPEX_MAP
SELECT	"MANDT",
	"GCS_FIKRS",
	"GCS_FIPEX",
	"FAS_FIPEX",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_FIPEX_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_FIPEX_MAP`.

```sql
-- From ESQLT- Truncate Staging Tables_In_S_GC_PROJ_SUB_CONTINENT_REGION
TRUNCATE TABLE dbo.ZOAT_PORD_MAP;
TRUNCATE TABLE dbo.ZOAT_PREQ_MAP;
TRUNCATE TABLE dbo.ZOAT_SAKNR_MAP;
TRUNCATE TABLE dbo.ZOAT_USNAM_MAP;
TRUNCATE TABLE dbo.ZOAT_WBS_MAP;
TRUNCATE TABLE dbo.ZOAT_LFB1_MAP;
```

Context: This T-SQL code truncates the specified tables.

```sql
-- From OLEDB_SRC-ZOAT_PORD_MAP
SELECT	"CLIENT",
	"GCS_EBELN",
	"FAS_EBELN",
	"GCS_PO_VALUE_TC",
	"GCS_PO_VALUE_LC",
	"GCS_INVOICED_TC",
	"GCS_INVOICED_LC",
	"GC_ROW_ID",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_PORD_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_PORD_MAP`.

```sql
SELECT	"LIFNR",
	"ALTKN",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_LFB1_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_LFB1_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_PREQ_MAP
SELECT	"CLIENT",
	"GCS_BANFN",
	"FAS_BANFN",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_PREQ_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_PREQ_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_SAKNR_MAP
SELECT	"MANDT",
	"GCS_KTOPL",
	"GCS_SAKNR",
	"FAS_SAKNR",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_SAKNR_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_SAKNR_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_USNAM_MAP
SELECT	"MANDT",
	"GCS_USNAM",
	"FAS_USNAM",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_USNAM_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_USNAM_MAP`.

```sql
-- From OLEDB_SRC-ZOAT_WBS_MAP
SELECT	"CLIENT",
	"GCS_OBJNR",
	"GCS_POSID",
	"GCS_PSPID",
	"GCS_POSID_INT",
	"GCS_PSPID_INT",
	"FAS_OBJNR",
	"FAS_POSID",
	"FAS_PSPNR",
	"FAS_PSPID",
	"GC_ROW_ID",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."ZOAT_WBS_MAP"
```

Context: This SQL query is used inside the OLE DB Source to extract data from table `ZOAT_WBS_MAP`.

```sql
User::V_SQL_INSERT_ON_PRE_EXECUTE
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
   AND ETL_SUB_COMPONENT_NM = 'PROJECT_MAPPING_TABLES.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: This SQL query is used to update the status of the ETL process to running.

```sql
User::V_SQL_UPDATE_ON_ERROR
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PROJECT_MAPPING_TABLES.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the status of the ETL process to failed.

```sql
User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PROJECT_MAPPING_TABLES.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the status of the ETL process to succeeded.

```
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING")
```

Context: This is an expression used to determine if the sequence container `SEQC-1` should be executed based on the value of project parameter `PRJ_PRM_PROCESS_NODE`.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.ZOAT_FKBER_MAP      | Stores ZOAT and FKBER mapping data | DFT- ZOAT_FKBER_MAP|
| dbo.ZOAT_GEBER_MAP      | Stores ZOAT and GEBER mapping data | DFT- ZOAT_GEBER_MAP|
| dbo.ZOAT_IMPR_MAP       | Stores ZOAT and IMPR mapping data  | DFT- ZOAT_IMPR_MAP|
| dbo.ZOAT_KOSTL_MAP      | Stores ZOAT and KOSTL mapping data | DFT- ZOAT_KOSTL_MAP|
| dbo.ZOAT_MWSKZ_MAP      | Stores ZOAT and MWSKZ mapping data | DFT- ZOAT_MWSKZ_MAP|
| dbo.ZOAT_BLAND_MAP      | Stores ZOAT and BLAND mapping data | DFT- ZOAT_BLAND_MAP|
| dbo.ZOAT_BLART_MAP      | Stores ZOAT and BLART mapping data | DFT- ZOAT_BLART_MAP|
| dbo.ZOAT_BSART_MAP      | Stores ZOAT and BSART mapping data | DFT- ZOAT_BSART_MAP|
| dbo.ZOAT_EKGRP_MAP      | Stores ZOAT and EKGRP mapping data | DFT- ZOAT_EKGRP_MAP|
| dbo.ZOAT_FICTR_MAP      | Stores ZOAT and FICTR mapping data | DFT- ZOAT_FICTR_MAP|
| dbo.ZOAT_FIPEX_MAP      | Stores ZOAT and FIPEX mapping data | DFT- ZOAT_FIPEX_MAP|
| dbo.ZOAT_PORD_MAP       | Stores ZOAT and PORD mapping data  | DFT- ZOAT_PORD_MAP|
| dbo.ZOAT_LFB1_MAP       | Stores ZOAT and LFB1 mapping data  | DFT- ZOAT_LFB1_MAP|
| dbo.ZOAT_PREQ_MAP       | Stores ZOAT and PREQ mapping data  | DFT- ZOAT_PREQ_MAP|
| dbo.ZOAT_SAKNR_MAP      | Stores ZOAT and SAKNR mapping data | DFT- ZOAT_SAKNR_MAP|
| dbo.ZOAT_USNAM_MAP      | Stores ZOAT and USNAM mapping data | DFT- ZOAT_USNAM_MAP|
| dbo.ZOAT_ZLSCH_MAP      | Stores ZOAT and ZLSCH mapping data | DFT- ZOAT_ZLSCH_MAP|

*   The package uses event handlers with T-SQL to log success or failure to the `ETL_RUN_STATUS` table.

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** 1
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 2
    *   Sequence Containers: 3
    *   Data Flow Tasks: 17
    *   Execute SQL Tasks: 4
*   Overall package complexity assessment: medium.
*   Potential performance bottlenecks: Large datasets could cause performance issues within the data flow tasks.
*   Critical path analysis: The critical path would be the sequential execution of the data flow tasks within each sequence container.
* The package uses event handlers with T-SQL to log success or failure to the `ETL_RUN_STATUS` table.
