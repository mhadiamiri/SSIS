## 1. Input Connection Analysis

```markdown
| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| HQS-DMARDSQL01           | SMOServer         | Server: @[$Project::PRJ_PRM_SRC_DB_SRVR]  | Source Connection | UseWindowsAuthentication=True | @[$Project::PRJ_PRM_SRC_DB_SRVR]            | All                  |
| HQS-DMARDSQL02           | SMOServer         | Server: @[$Project::PRJ_PRM_SRC_DB_SRVR]  | Source Connection | UseWindowsAuthentication=True | @[$Project::PRJ_PRM_SRC_DB_SRVR]           | All                  |
| HQS-DMARDSQL22           | SMOServer         | Server: @[$Project::PRJ_PRM_SRC_DB_SRVR]  | Source Connection | UseWindowsAuthentication=True | @[$Project::PRJ_PRM_SRC_DB_SRVR]           | All                  |
| HQS-DMARDSQL31           | SMOServer         | Server: @[$Project::PRJ_PRM_SRC_DB_SRVR]  | Source Connection | UseWindowsAuthentication=True | @[$Project::PRJ_PRM_SRC_DB_SRVR]           | All                  |
| HQS-DMBISQL05           | SMOServer         | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR]  | Destination Connection | UseWindowsAuthentication=True | @[$Project::PRJ_PRM_TRGT_DB_SRVR]            | All                  |
| HQS-DMBISQL15           | SMOServer         | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR]  | Destination Connection | UseWindowsAuthentication=True | @[$Project::PRM_TRGT_DB_SRVR]            | All                  |
| HQS-DMBISQL35           | SMOServer         | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR]  | Destination Connection | UseWindowsAuthentication=True | @[$Project::PRM_TRGT_DB_SRVR]            | All                  |
| HQS-DMBISQL45           | SMOServer         | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR]  | Destination Connection | UseWindowsAuthentication=True | @[$Project::PRM_TRGT_DB_SRVR]            | All                  |
```

## 2. Package Dependencies

```markdown
| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All|
```

## 3. Package Flow Analysis

The package `ARD_PRIME_LANDING` consists of the following main tasks:

1.  **EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode**: An Expression Task that evaluates the expression `1 == 1`.
2.  **Transfer SQL Server Objects Task**: Transfers SQL Server objects from a source database to a destination database.
3.  **SEQC - LOAD Other Landing Tables**: A Sequence Container which encapsulates the loading of other landing tables.

The Sequence Container `SEQC - LOAD Other Landing Tables` includes:

*   **ESQLT- TRUNCATE Other Landing Tables**: Executes a SQL statement to truncate tables `dbo.tblAppSettings` and `dbo.CDC_Changes`.
*   **DFT - tblAppSettings**: A Data Flow Task to load data into the `dbo.tblAppSettings` table.
*   **DFT - PRM_CDC_Changes**: A Data Flow Task to load data into the `dbo.CDC_Changes` table.

#### DFT - tblAppSettings

*   **Source:** OLE DB Source (OLEDB\_SRC - tblAppSettings) extracts data from `dbo.tblAppSettings`.
*   **Transformations:**
    *   `DRV_TRFM - ETL_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns using `GETDATE()`.
*   **Destinations:**
    *   `OLEDB_DEST - tblAppSettings` saves data to `dbo.tblAppSettings`.

#### DFT - PRM_CDC_Changes

*   **Source:** OLE DB Source (OLEDB\_SRC - CDC\_Changes) extracts data from `dbo.CDC_Changes`.
*   **Transformations:**
    *   `DRV_TRFM - ETL_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns using `GETDATE()`.
*   **Destinations:**
    *   `OLEDB_DEST - CDC_Changes` saves data to `dbo.CDC_Changes`.

The package also includes event handlers for `OnPreExecute`, `OnPostExecute`, and `OnError` events, which update the ETL process status in a database table.

## 4. Code Extraction

```markdown
-- From OLEDB_SRC - CDC_Changes
SELECT [cdc_ID]
      ,[cdc_Table_name]
      ,[cdc_Column_name]
      ,[cdc_LastUpdate]
      ,[cdc_UpdatedBy]
      ,[cdc_New_value]
      ,[cdc_action]
FROM [dbo].[CDC_Changes]
```

Context: This SQL query is used to extract CDC data.

```markdown
-- From OLEDB_SRC - tblAppSettings
SELECT [aps_ID]
      ,[aps_MPMPGracePeriodEndMonth]
      ,[aps_MPMPGracePeriodEndDay]
      ,[aps_LastUpdated]
      ,[aps_UpdatedBy]
      ,[aps_SQProfileCriteria_CutoffYear]
  FROM dbo.tblAppSettings
```

Context: This SQL query is used to extract data from tblAppSettings.

```markdown
-- From ESQLT- TRUNCATE Other Landing Tables
TRUNCATE TABLE dbo.tblAppSettings;


TRUNCATE TABLE [dbo].[CDC_Changes];
```

Context: This SQL is used to truncate the tables before load.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_RUN_STATUS
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
  WHERE ETL_COMPONENT_NM = 'ARD_MASTER.DTSX'     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/ARD'   
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'ARD_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/ARD' 
    )
   AND ETL_SUB_COMPONENT_NM = 'ARD_PRIME_LANDING.dtsx'   
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: This SQL is used to insert into ETL_RUN_STATUS table.

```markdown
-- From User::V_SQL_UPDATE_ON_ERROR
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
   ETL_COMPONENT_NM = 'ARD_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/ARD'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ARD_PRIME_LANDING.dtsx'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL is used to update ETL_RUN_STATUS table when the package fails.

```markdown
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   ETL_COMPONENT_NM = 'ARD_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/ARD' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ARD_PRIME_LANDING.dtsx'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL is used to update ETL_RUN_STATUS table when the package succeeds.

## 5. Output Analysis

```markdown
| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.tblAppSettings  | Stores application settings data   | DFT - tblAppSettings|
| dbo.CDC_Changes  | Stores Change Data Capture data   | DFT - PRM_CDC_Changes|
```

## 6. Package Summary

*   **Input Connections:** 8
*   **Output Destinations:** 2
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Task: 3 (plus 1 in the main flow)
    *   Transfer SQL Server Objects Task: 1
    *   Sequence Container: 1
    *   Data Flow Tasks: 2
    *   Execute SQL Tasks: 4 (1 in the main flow, and 3 in event handlers)
    *   Derived Column: 2
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: The Transfer SQL Server Objects Task could be a bottleneck if transferring a large number of objects.
*   Critical path analysis: The critical path is the main sequence of tasks: Expression Task -> Transfer SQL Server Objects Task -> Sequence Container.
*   Error handling mechanisms: The package includes error handling mechanisms using event handlers to update the ETL process status on error.
