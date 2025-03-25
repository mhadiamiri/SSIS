## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {CD92ADBF-3E1B-472A-BC3E-4745C8CD2149}  | OLE DB          | Server: [Inferred], Database: [Inferred] | Execute QA stored procedure | SQL Server Auth likely | None   | Package |
| {3653D0A0-E512-4269-94C0-866616C4F312}      | OLE DB          | Server: [Inferred], Database: [Inferred] | Execute ETL Status stored procedures | SQL Server Auth likely | None     | Event Handlers |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| CCEM_Dimension.dtsx      | [Inferred]        | Parent                     | `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION")` OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`    | Executes Dimension package   | Package |
| CCEM_Fact.dtsx           | [Inferred]        | Parent                     | `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT")` OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`    | Executes Fact package        | Package |
| CCEM_Landing.dtsx        | [Inferred]        | Parent                     | `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (FINDSTRING(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])), "LANDING", 1) != 0)`      | Executes Landing package     | Package |
| CCEM_Staging.dtsx        | [Inferred]        | Parent                     | `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING")` OR `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")`    | Executes Staging package     | Package |

## 3. Package Flow Analysis

The package `CCEM_Master.dtsx` acts as a master package, orchestrating the execution of other packages based on the value of the project parameter `PRJ_PRM_PROCESS_NODE`.

*   The package starts with an `EXPRESSIONT` task that evaluates to `true`. This task appears to be a placeholder or a starting point for workflow execution.
*   The package then uses precedence constraints based on the project parameter `@[$Project::PRJ_PRM_PROCESS_NODE]` to determine which packages to execute.
*   If `@[$Project::PRJ_PRM_PROCESS_NODE]` is "DIMENSION", the `EPKGT-CCEM_DIMENSION` task executes `CCEM_Dimension.dtsx`.
*   If `@[$Project::PRM_PROCESS_NODE]` is "STAGING", the `EPKGT-CCEM_STAGING` task executes `CCEM_Staging.dtsx`.
*   If `@[$Project::PRM_PROCESS_NODE]` is "FACT", the `EPKGT-CCEM_FACT` task executes `CCEM_Fact.dtsx`.
*   If `@[$Project::PRM_PROCESS_NODE]` is "ALL", `CCEM_Staging.dtsx`, `CCEM_Dimension.dtsx`, and `CCEM_Fact.dtsx` are executed sequentially. The order of execution is Staging -> Dimension -> Fact.
*   If `@[$Project::PRM_PROCESS_NODE]` contains "LANDING" or is "ALL", `CCEM_Landing.dtsx` is executed first, followed by `CCEM_Staging.dtsx`.
*   After the `EPKGT-CCEM_FACT` task completes, the `ESQLT- stored procedure sp_qa_ccem_etl` task executes the stored procedure `dbo.sp_qa_ccem_etl`.
*   Error handling is implemented using Event Handlers for `OnError`, `OnPostExecute`, and `OnPreExecute` events. These handlers update the `ETL_RUN_STATUS` table to reflect the status of the package execution.

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

Context: This SQL statement inserts a record into the `ETL_RUN_STATUS` table when the master package starts, indicating a "RUNNING" status. The `ETL_COMPONENT_ID` is parameterized using a project parameter.

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

Context: This SQL statement updates the `ETL_RUN_STATUS` table to mark any previous "RUNNING" instances of the master package as "TERMINATED BY RERUN". This prevents hung jobs from interfering with the current execution. The `ETL_COMPONENT_ID` is parameterized using a project parameter.

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

Context: This SQL statement updates the `ETL_RUN_STATUS` table to mark any previous "RUNNING" instances of the sub-packages (`CCEM_Landing.dtsx`, `CCEM_Staging.dtsx`, `CCEM_Dimension.dtsx`, `CCEM_Fact.dtsx`) as "TERMINATED BY RERUN". The `ETL_COMPONENT_ID` is parameterized using a project parameter.

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

Context: This SQL statement updates the `ETL_RUN_STATUS` table to mark the master package as "FAILED" if an error occurs. The `ETL_COMPONENT_ID` is parameterized using a project parameter.

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

Context: This SQL statement updates the `ETL_RUN_STATUS` table to mark the master package as "SUCCEEDED" after it completes successfully. The `ETL_COMPONENT_ID` is parameterized using a project parameter.

```sql
exec dbo.sp_qa_ccem_etl;
```

Context: This SQL statement executes the stored procedure `dbo.sp_qa_ccem_etl`. This stored procedure is likely related to quality assurance checks after the ETL process is complete.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS           | Stores the status of ETL runs. | Event Handlers |

## 6. Package Summary

*   **Input Connections:** 2
*   **Output Destinations:** 1 (ETL_RUN_STATUS table)
*   **Package Dependencies:** 4
*   **Activities:**
    *   Execute Package Tasks: 4
    *   Execute SQL Tasks: 6 (3 in the main package, 3 in event handlers)
    *   Expression Tasks: 4 (1 in the main package, 3 in event handlers)
*   Overall package complexity assessment: Medium. The package is relatively simple in its control flow, but the reliance on project parameters and the chained execution of other packages adds complexity.
*   Potential performance bottlenecks: The sequential execution of packages when `PRJ_PRM_PROCESS_NODE` is "ALL" could be a bottleneck. Consider parallel execution if dependencies allow.
*   Critical path analysis: The critical path depends on the value of the `PRJ_PRM_PROCESS_NODE` parameter. If it's "ALL", the critical path is the sequential execution of all four sub-packages.
*   Error handling mechanisms: The package utilizes event handlers to capture errors and update the `ETL_RUN_STATUS` table, providing a basic level of error logging.
