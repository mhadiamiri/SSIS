## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {3653D0A0-E512-4269-94C0-866616C4F312}           | OLE DB          | Server: [Inferred], Database: [Inferred]  | ETL Run Status logging | SQL Server Auth likely | @[$Project::PRJ_PRM_ETL_COMPONENT_ID] | Event Handlers |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| CCEM_EMRGNCY_CRISIS_Landing.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (FINDSTRING(UPPER(TRIM(@[$Project::PRM_PROCESS_NODE])), "LANDING", 1) != 0) | Standard parent-child relationship | Main Package |

## 3. Package Flow Analysis

The package `CCEM_EMRGNCY_CRISIS_Master.dtsx` orchestrates the execution of a child package and logs ETL run status.

*   **EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process\_Node:** An Expression Task that evaluates to true ( `1 == 1`).
*   **EPKGT-CCEM\_EMERGENCY\_CRISIS\_LANDING:** An Execute Package Task that runs the child package `CCEM_EMRGNCY_CRISIS_Landing.dtsx`. This task executes if the project parameter `PRJ_PRM_PROCESS_NODE` contains "LANDING" or is set to "ALL".

The package uses event handlers for logging purposes:

*   **OnPreExecute:**
    *   Executes SQL tasks to set hung job statuses to terminated for both the master package and its sub-components.
    *   Creates a new record with a "RUNNING" status for the master package in the `ETL_RUN_STATUS` table.
*   **OnPostExecute:**
    *   Executes a SQL task to update the `ETL_RUN_STATUS` table to "SUCCEEDED" for the master package.
*   **OnError:**
    *   Executes a SQL task to update the `ETL_RUN_STATUS` table to "FAILED" for the master package.

## 4. Code Extraction

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_MASTER_RUN_STATUS
INSERT INTO [ETL_RUN_STATUS]
           ([ETL_COMPONENT_ID]           
           ,[ETL_RUN_STATUS_DESC]
           ,[ETL_RUN_MAIN_COMPONENT_IND]
           ,[ETL_RUN_RECORD_CREA_DT]
           ,[ETL_RUN_RECORD_UPDT_DT])
     VALUES
           (
     8         
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

This SQL script inserts a new record into the `ETL_RUN_STATUS` table indicating that the master package is running. The `ETL_COMPONENT_ID` is parameterized via a project parameter.

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER
-- STEP 01 
-- SET HUNG JOBS STATUS FOR MAIN COMPONENT
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = 8
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
  );
```

This SQL script updates any previous "RUNNING" status records for the master package to "TERMINATED BY RERUN."  The `ETL_COMPONENT_ID` is parameterized.

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS
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
    WHERE ETL_COMPONENT_ID = 8
     AND ETL_SUB_COMPONENT_NM = 'CCEM_Landing.dtsx'
    )
   AND ETL_COMPONENT_ID = 8
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID = 8
     AND ETL_SUB_COMPONENT_NM = 'CCEM_Staging.dtsx'
    )
   AND ETL_COMPONENT_ID = 8
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID = 8
       AND ETL_SUB_COMPONENT_NM = 'CCEM_Dimension.dtsx'
      )
     AND ETL_COMPONENT_ID = 8
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
    
    UNION
    
    SELECT ETL_RUN_STATUS_ID
    FROM ETL_RUN_STATUS
    WHERE etl_sub_component_id IN (
      SELECT ETL_SUB_COMPONENT_ID
      FROM ETL_SUB_COMPONENT
      WHERE ETL_COMPONENT_ID = 8
       AND ETL_SUB_COMPONENT_NM = 'CCEM_Fact.dtsx'
      )
     AND ETL_COMPONENT_ID = 8
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
  );
```

This SQL script updates any previous "RUNNING" status records for the sub-components (Landing, Staging, Dimension, Fact) to "TERMINATED BY RERUN."  The `ETL_COMPONENT_ID` is parameterized.

```sql
-- From User::V_SQL_UPDATE_ON_ERROR
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = 8
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

This SQL script updates the master package's status to "FAILED" in the `ETL_RUN_STATUS` table. The `ETL_COMPONENT_ID` is parameterized.

```sql
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = 8
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

This SQL script updates the master package's status to "SUCCEEDED" in the `ETL_RUN_STATUS` table. The `ETL_COMPONENT_ID` is parameterized.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS           | Stores ETL run status information for the master package and sub-components. | Event Handlers |

## 6. Package Summary

*   **Input Connections:** 1 OLE DB connection for logging.
*   **Output Destinations:** 1 `ETL_RUN_STATUS` table.
*   **Package Dependencies:** 1 (`CCEM_EMRGNCY_CRISIS_Landing.dtsx`).
*   **Activities:**
    *   Expression Tasks: 2 (1 in main flow, 1 in each event handler)
    *   Execute Package Task: 1
    *   Execute SQL Tasks: 5 (3 in OnPreExecute, 1 in OnPostExecute, 1 in OnError)
*   **Transformations:** None.
*   **Script tasks:** 0
*   Overall package complexity assessment: Low.
*   Potential performance bottlenecks: The SQL update statements in the `OnPreExecute` event handler that terminate hung jobs could be a bottleneck if the `ETL_RUN_STATUS` table is large.
*   Critical path analysis: The critical path is the successful execution of the child package `CCEM_EMRGNCY_CRISIS_Landing.dtsx`. The master package primarily handles logging and pre-execution tasks.
*   Document error handling mechanisms: The package uses an `OnError` event handler to update the `ETL_RUN_STATUS` table with a "FAILED" status.
