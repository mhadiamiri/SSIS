## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_GC_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for the vendor data | SQL Server Auth likely | None            | SEQC-R_GC_VENDOR_MULTILINGUALISM, DFT-R_GCS_VENDOR_MAP, DFT-R_GC_VENDOR_MULTILINGUALISM                  |
| GC_SOURCE_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for vendor map data             | SQL Server Auth likely            |  None                  | SEQC-R_GC_VENDOR_MULTILINGUALISM, DFT-R_GCS_VENDOR_MAP                 |
| GC_STAGING_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for vendor multilingualism data | SQL Server Auth likely |  None                  | SEQC-R_GC_VENDOR_MULTILINGUALISM, DFT-R_GC_VENDOR_MULTILINGUALISM                 |
| {A5B76FD7-D378-486C-8549-B9BE51A7D083}           | OLE DB          | Server: [Inferred], Database: [Inferred]  | ETL Status Logging | SQL Server Auth likely | User::V_SQL_UPDATE_ON_ERROR, User::V_SQL_UPDATE_ON_POST_EXECUTE, User::V_SQL_INSERT_ON_PRE_EXECUTE                  | None                  | Package.EventHandlers                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package starts with an `Expression Task` named `EXPRESSIONT- FINANCE Refrence- Start Task - ProcessDataFlowNode`. The expression is simply `1 == 1`, serving as a starting point.
*   The next task is a `Sequence Container` named `SEQC-R_GC_VENDOR_MULTILINGUALISM`.
*   Inside the sequence container, there is an `Execute SQL Task` named `ESQLT- Truncate Tables` that truncates two tables: `dbo.R_GC_VENDOR_MULTILINGUALISM` and `dbo.R_GCS_VENDOR_MAP`.
*   The next task is a `Data Flow Task` named `DFT-R_GC_VENDOR_MULTILINGUALISM`.
*   Then a `Data Flow Task` named `DFT-R_GCS_VENDOR_MAP`.

#### DFT-R_GC_VENDOR_MULTILINGUALISM

*   **Source:** OLE DB Source (OLEDB\_SRC-S\_GC\_VENDOR\_MULTILINGUALISM) extracts data from `S_GC_VENDOR_MULTILINGUALISM`.
*   **Transformations:** None apparent. The source data goes directly to the destination.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-R\_GC\_VENDOR\_MULTILINGUALISM) loads data into `dbo.R_GC_VENDOR_MULTILINGUALISM`.

#### DFT-R_GCS_VENDOR_MAP

* **Source:** OLE DB Source extracts data from `dbo.ZOAT_LFB1_MAP` using the `GC_SOURCE_C` connection.
* **Transformations:**
    * Data Conversion: Converts `LIFNR` and `ALTKN` from `str` to `wstr`.
* **Destination:** OLE DB Destination loads data into `dbo.R_GCS_VENDOR_MAP` using the `MART_GC_REPORTING` connection.

## 4. Code Extraction

```sql
-- From OLEDB_SRC_S_GCS_VENDOR_MAP
SELECT	"LIFNR",
	"ALTKN",
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM   "dbo"."ZOAT_LFB1_MAP"
```

Context: This SQL query is used to extract data from the `ZOAT_LFB1_MAP` table in the `DFT-R_GCS_VENDOR_MAP` Data Flow Task.

```sql
-- From OLEDB_SRC_S_GC_VENDOR_MULTILINGUALISM
SELECT
      cast(T1.[VENDOR_NBR] as varchar(10) ) as VENDOR_NBR,
      T1.SOURCE_ID,
      T1.[DETAIL_LANGUAGE_CD],
      T1.[OFFICIAL_LANGUAGE_CD],
      T1.[VENDOR_OPERATING_NM_LINE_1],
      T1.[VENDOR_OPERATING_NM_LINE_2],
      T1.[VENDOR_ACRONYM],
      T1.[INTERNET_ADDRESS_URL],
      T1.[URL_LANGUAGE_CD],
      T1.[MAILING_ADDRESS_LINE_1],
      T1.[MAILING_ADDRESS_LINE_2],
      T1.[MAILING_POSTAL_CD],
      T1.[MAILING_COUNTRY_CD],
      T1.[PHYSICAL_ADDRESS_LINE_1],
      T1.[PHYSICAL_ADDRESS_LINE_2],
      T1.[PHYSICAL_CITY_NM],
      T1.[PHYSICAL_REGION_CD],
      T1.[PHYSICAL_POSTAL_CD],
      T1.[PHYSICAL_COUNTRY_CD],
      T1.[EMAIL_ADDRESS_URL],
      T1.[MAIN_TELEPHONE_NBR],
      T1.[MAIN_FAX_NBR],
      T1.[CREATION_DT],
      T1.[LAST_UPDATED_DT],
      T1.[CREATED_BY_USER_ID],
      T1.[SEARCH_TERM],
	  convert(date, getdate()) as ROW_INSERT_DTT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
  FROM S_GC_VENDOR_MULTILINGUALISM T1
```

Context: This SQL query is used to extract data from the `S_GC_VENDOR_MULTILINGUALISM` table in the `DFT-R_GC_VENDOR_MULTILINGUALISM` Data Flow Task.

```sql
-- From ESQLT- Truncate Tables
TRUNCATE TABLE dbo.R_GC_VENDOR_MULTILINGUALISM ;
TRUNCATE TABLE dbo.R_GCS_VENDOR_MAP ;
```

Context: This SQL query is used to truncate the tables `dbo.R_GC_VENDOR_MULTILINGUALISM` and `dbo.R_GCS_VENDOR_MAP`.

```sql
--From User::V_SQL_UPDATE_ON_ERROR
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'CONTRACT_REFERENCE.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the ETL status to 'FAILED' in case of an error.

```sql
--From User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'CONTRACT_REFERENCE.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the ETL status to 'SUCCEEDED' after successful execution.

```sql
--From User::V_SQL_INSERT_ON_PRE_EXECUTE
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
   AND ETL_SUB_COMPONENT_NM = 'CONTRACT_REFERENCE.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: This SQL query is used to insert a record with 'RUNNING' status in the `ETL_RUN_STATUS` table before the package execution.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.R_GC_VENDOR_MULTILINGUALISM  | Stores vendor multilingualism data   | DFT-R_GC_VENDOR_MULTILINGUALISM|
| dbo.R_GCS_VENDOR_MAP  | Stores vendor map data   | DFT-R_GCS_VENDOR_MAP|

## 6. Package Summary

*   **Input Connections:** 3
*   **Output Destinations:** 2
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 2
    *   Sequence Containers: 1
    *   Data Flow Tasks: 2
    *   Execute SQL Tasks: 4
    *   Data Conversion: 1
*   **Overall package complexity assessment:** Medium
*   **Potential performance bottlenecks:** None apparent from the metadata alone.  Performance will depend on the size of the tables involved and the speed of the connections.
*   **Critical path analysis:** The critical path is linear, starting with the expression task, then sequence container which truncates tables, loads vendor multilingualism data, and loads vendor mapping data.
*   **Error handling mechanisms:** The package contains `OnError`, `OnPreExecute`, and `OnPostExecute` event handlers, implementing ETL status logging.
