## 1. Input Connection Analysis

| Connection Manager Name     | Connection Type | Connection String Details                                                                          | Purpose within Package                                                                | Security Requirements | Parameters/Variables | Source Part |
| :-------------------------- | :-------------- | :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ | :---------------------- | :------------------- | :---------- |
| {BAF46AE1-5DA5-4EEF-81AA-6F8488261709} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to DFAIT_Reporting                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {3FBA1246-C9E8-4563-91FD-655440BF8724} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to IPRS_BI                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {B41FF5BD-B7AF-40C4-A8DA-008172B30CCE} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to BI_CONFORMED                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {94A4696F-7FD3-4FAF-AA4C-DE86229E4199} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to DFAIT_STAGING                                                              | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {0372DF41-46F4-441D-AC47-DDFA3129B54D} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to DW_ADMIN                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {EAD46801-DF7E-4A66-8392-A332378304A0} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to TRADE_REPORTING                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {F67FE7BA-1E3D-47B7-B067-439FD8773638} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to TRADE_REPORTING_LIVE                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {FF0865AB-8993-4DEC-A8B5-2E067FE20155} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to TRADE_STAGING and execution of stored procedure	| SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {07CEF02E-2077-4F01-B270-D498CC51C6C3} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to WCMS_TCS                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {89D3420A-3652-4238-9517-94C3FEA47108} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to TRADE_LANDING                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |
| {CDDF6A15-8279-4858-A8EE-17BFA66AD72B} | OLE DB        | Server: [Inferred], Database: [Inferred]                                                                                    | Connection to TRIO_SOURCE                                                               | SQL Server Auth likely | None                 | Part 1, 2, 3 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints                                                                                                                                                                                                                                                                                                 | Notes                                                                                                                                                                                       | Source Part |
| :--------------------- | :---------------- | :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------- |
| TRADE_DIMENSION.dtsx   |                     | Child of TRADE_MASTER      | `FINDSTRING(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])), "DIMENSION", 1) != 0`OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`                                                                                                                                                                                                                                                                                                 | Executes TRADE_DIMENSION package.                                                                                                                                                         | Part 1, 2, 3 |
| TRADE_FACT.dtsx        |                     | Child of TRADE_MASTER      | `FINDSTRING(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])), "FACT", 1) != 0` OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`                                                                                                                                                                                                                                                                                       | Executes TRADE_FACT package.                                                                                                                                                              | Part 1, 2, 3 |
| TRADE_LANDING.dtsx     |                     | Child of TRADE_MASTER      | `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (FINDSTRING(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])), "LANDING", 1) != 0)`                                                                                                                                                                                                                                                                                          | Executes TRADE_LANDING package.                                                                                                                                                           | Part 1, 2, 3 |
| TRADE_STAGING.dtsx     |                     | Child of TRADE_MASTER      | `FINDSTRING(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])), "STAGE", 1) != 0` OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`                                                                                                                                                                                                                                                                                        | Executes TRADE_STAGING package.                                                                                                                                                           | Part 1, 2, 3 |

## 3. Package Flow Analysis

The TRADE_MASTER package orchestrates the execution of other packages (TRADE_LANDING, TRADE_STAGING, TRADE_DIMENSION, and TRADE_FACT) based on the value of the project parameter `PRJ_PRM_PROCESS_NODE`.

*   **Starting Point:** `EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process_Node` - This is an Expression Task that always evaluates to true. It acts as a starting point for the workflow.
*   **Conditional Execution:**
    *   If `PRJ_PRM_PROCESS_NODE` contains "DIMENSION",  `EPKGT-TRADE DIMENSION` is executed.
    *   If `PRJ_PRM_PROCESS_NODE` contains "STAGE", `EPKGT-TRADE STAGING` is executed.
    *   If `PRJ_PRM_PROCESS_NODE` contains "FACT", `EPKGT-TRADE FACT` is executed.
    *   If `PRJ_PRM_PROCESS_NODE` contains "ALL" or "LANDING", `EPKGT-TRADE LANDING` is executed.

*   **Chaining Execution:**
    *   `EPKGT-TRADE LANDING` executes first  if  `PRJ_PRM_PROCESS_NODE` is ALL, followed by `EPKGT-TRADE STAGING`.
    *   `EPKGT-TRADE STAGING` executes first  if  `PRJ_PRM_PROCESS_NODE` is ALL, followed by `EPKGT-TRADE DIMENSION`.
    *   `EPKGT-TRADE DIMENSION` executes first  if  `PRJ_PRM_PROCESS_NODE` is ALL, followed by `EPKGT-TRADE FACT`.
    *   After `EPKGT-TRADE FACT` executes when  `PRJ_PRM_PROCESS_NODE` is ALL,  `ESQLT- stored procedure sp_qa_trade_etl` is executed.

*   **Execute SQL Task - Connection testing within Sequence Container:**
    *   A sequence container named  `DELETE AFTER CONFIGURING THE PROJECT` contains a series of Execute SQL Tasks.
    *   Each Execute SQL Task tests a connection to a different database (`DFAIT_Reporting`, `IPRS_BI`, `BI_CONFORMED`, `DFAIT_STAGING`, `DW_ADMIN`, `TRADE_REPORTING`, `TRADE_REPORTING_LIVE`, `TRADE_STAGING`, `WCMS_TCS`, `TRADE_LANDING`, `TRIO_SOURCE`).
    *   All Execute SQL Tasks execute sequentially.
    *   The SQL statement executed by each task is `SELECT 1;`.

*   **Event Handlers:** The package includes event handlers for `OnPreExecute`, `OnPostExecute`, and `OnError`. The event handlers log the status of the package execution (running, succeeded, or failed) to the `ETL_RUN_STATUS` table.

## 4. Code Extraction

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - DFAIT_Reporting
SELECT 1;
```

Context: This SQL query is used to test the connection to `DFAIT_Reporting`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - IPRS_BI
SELECT 1;
```

Context: This SQL query is used to test the connection to `IPRS_BI`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST BI_CONFORMED CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `BI_CONFORMED`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST DFAIT_STAGING CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `DFAIT_STAGING`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST DW_ADMIN CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `DW_ADMIN`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST TRADE_REPORTING CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `TRADE_REPORTING`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST TRADE_REPORTING_LIVE CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `TRADE_REPORTING_LIVE`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST TRADE_STAGING CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `TRADE_STAGING`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT - TEST WCMS_TCS
SELECT 1;
```

Context: This SQL query is used to test the connection to `WCMS_TCS`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT- TRADE_LANDING CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `TRADE_LANDING`.

```markdown
-- From Package\DELETE AFTER CONFIGURING THE PROJECT\ESQLT-TEST TRIO_SOURCE CONNECTION
SELECT 1;
```

Context: This SQL query is used to test the connection to `TRIO_SOURCE`.

```markdown
-- From Package\ESQLT- stored procedure sp_qa_trade_etl
exec dbo.sp_qa_trade_etl;
```

Context: This SQL query is used to execute stored procedure `dbo.sp_qa_trade_etl`.

```markdown
-- From Package\ESQLT- stored procedure sp_qa_trade_etl.EventHandlers[OnPostExecute]\ESQLT- Create Record  with Running Status
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
   ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ESQLT- stored procedure sp_qa_trade_etl'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update status of ETL process after successful execution.

```markdown
-- From Package\ESQLT- stored procedure sp_qa_trade_etl.EventHandlers[OnPreValidate]\ESQLT- Create Record  with Running Status
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
  WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_SUB_COMPONENT_NM = 'ESQLT- stored procedure sp_qa_trade_etl'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 );
```

Context: This SQL query is used to create a record with running status before validation.

```markdown
-- From Package\ESQLT- stored procedure sp_qa_trade_etl.EventHandlers[OnTaskFailed]\ESQLT- Update ETL Process Status to Failed
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
   ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ESQLT- stored procedure sp_qa_trade_etl'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update status of ETL process to Failed after failed execution.

```markdown
-- From Package.EventHandlers[OnError]\ESQLT- Update ETL Process Status to Failed
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

Context: This SQL query is used to set the package status to FAILED in case of an error.

```markdown
-- From Package.EventHandlers[OnPostExecute]\ESQLT- Update ETL Process Status to Succeeded
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

Context: This SQL query is used to set the package status to SUCCEEDED after successful completion.

```markdown
-- From Package.EventHandlers[OnPreExecute]\ESQLT- Create Record  with Running Status for Master Package
INSERT INTO [ETL_RUN_STATUS]
           ([ETL_COMPONENT_ID]           
           ,[ETL_RUN_STATUS_DESC]
           ,[ETL_RUN_MAIN_COMPONENT_IND]
           ,[ETL_RUN_RECORD_CREA_DT]
           ,[ETL_RUN_RECORD_UPDT_DT])
     VALUES
           (
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE')           
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query is used to create a record in `ETL_RUN_STATUS` to indicate that the package is running.

```markdown
-- From Package.EventHandlers[OnPreExecute]\ESQLT- Set Hung Job Status to Terminated for Master Package
-- STEP 01 
-- SET HUNG JOBS STATUS FOR MAIN COMPONENT
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
  );
```

Context: This SQL query is used to update the status of any hung jobs for main component to terminated.

```markdown
-- From Package.EventHandlers[OnPreExecute]\ESQLT-Set Hung Job Status to Terminated for Sub Components
-- SET HUNG JOBS STATUS FOR SUB-COMPONENT
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
 ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE ETL_RUN_STATUS_ID IN (
    SELECT ETL_RUN_STATUS_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID IN (
      SELECT ETL_COMPONENT_ID
      FROM ETL_COMPONENT
      WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
      )
     AND ETL_SUB_COMPONENT_NM = 'TRADE_LANDING.DTSX'
    )
   AND ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID IN (
      SELECT ETL_COMPONENT_ID
      FROM ETL_COMPONENT
      WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
      )
     AND ETL_SUB_COMPONENT_NM = 'TRADE_STAGING.DTSX'
    )
   AND ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID IN (
      SELECT ETL_COMPONENT_ID
      FROM ETL_COMPONENT
      WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
       AND ETL_SUB_COMPONENT_NM = 'TRADE_DIMENSION.DTSX'
      )
     AND ETL_COMPONENT_ID IN (
      SELECT ETL_COMPONENT_ID
      FROM ETL_COMPONENT
      WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
      )
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
    
    UNION
    
    SELECT ETL_RUN_STATUS_ID
    FROM ETL_RUN_STATUS
    WHERE etl_sub_component_id IN (
      SELECT ETL_SUB_COMPONENT_ID
      FROM ETL_SUB_COMPONENT
      WHERE ETL_COMPONENT_ID IN (
        SELECT ETL_COMPONENT_ID
        FROM ETL_COMPONENT
        WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
         AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
        )
       AND ETL_SUB_COMPONENT_NM = 'TRADE_FACT.DTSX'
      )
     AND ETL_COMPONENT_ID IN (
      SELECT ETL_RUN_STATUS_ID
      FROM ETL_COMPONENT
      WHERE ETL_COMPONENT_NM = 'TRADE_MASTER.DTSX'
       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/TRADE'
      )
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
    )
  );  
```

Context: This SQL query is used to update the status of any hung jobs for sub components to terminated.

## 5. Output Analysis

| Destination Table | Description                                                                                                                          | Source Part |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :---------- |
| ETL_RUN_STATUS    | Stores the status of ETL processes (Running, Succeeded, Failed, Terminated by Rerun) for both the main component and sub-components. | Part 4      |

## 6. Package Summary

*   **Input Connections:** 11 (Used for testing connections).
*   **Output Destinations:** 1 (ETL_RUN_STATUS table).
*   **Package Dependencies:** 4 (TRADE_DIMENSION.dtsx, TRADE_FACT.dtsx, TRADE_LANDING.dtsx, TRADE_STAGING.dtsx).
*   **Activities:**
    *   Execute Package Tasks: 4
    *   Execute SQL Tasks: 13
    *   Expression Tasks: 5
    *   Sequence Containers: 1

*   **Transformations:** None (This package primarily orchestrates other packages and executes SQL statements).
*   **Script tasks:** 0
*   **Overall package complexity assessment:** Medium.  The package orchestrates the execution of other packages based on a project parameter. It also includes comprehensive logging and error handling.
*   **Potential performance bottlenecks:** The sequential execution of connection testing Execute SQL Tasks within the sequence container `DELETE AFTER CONFIGURING THE PROJECT` could be a bottleneck. The performance depends on the response time of each database connection.
*   **Critical path analysis:** The critical path depends on the value of the `PRJ_PRM_PROCESS_NODE` parameter. If the value is "ALL", the critical path includes `EPKGT-TRADE LANDING`, `EPKGT-TRADE STAGING`,`EPKGT-TRADE DIMENSION`, `EPKGT-TRADE FACT`, and `ESQLT- stored procedure sp_qa_trade_etl`.
*   **Document error handling mechanisms:** The package includes `OnError`, `OnPreExecute`, and `OnPostExecute` event handlers. These handlers log the status of the package execution to the `ETL_RUN_STATUS` table. If an error occurs, the `OnError` event handler will update the status to "FAILED". The `OnPreExecute` event handler terminates any hung jobs before starting a new run. The `OnPostExecute` event handler updates the status to "SUCCEEDED" after successful completion. The `ESQLT- stored procedure sp_qa_trade_etl` also includes event handlers for `OnTaskFailed`, `OnPreValidate`, and `OnPostExecute`.
