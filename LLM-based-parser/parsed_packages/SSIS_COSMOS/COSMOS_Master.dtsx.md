## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {BB61CA3C-2DA6-4CFC-9E99-55C9BF05831F}  | OLE DB          | Server: [Inferred], Database: [Inferred] | Testing connection | SQL Server Auth likely | None | Part 1 |
| {84B8B96C-F61C-41FC-B363-0BE5DC63AAD9} | OLE DB          | Server: [Inferred], Database: [Inferred]  | Testing connection | SQL Server Auth likely | None | Part 1 |
| {EAD46801-DF7E-4A66-8392-A332378304A0}   | OLE DB          | Server: [Inferred], Database: [Inferred]  | Testing connection | SQL Server Auth likely | None | Part 1 |
| {FF0865AB-8993-4DEC-A8B5-2E067FE20155} | OLE DB          | Server: [Inferred], Database: [Inferred]  | Testing connection | SQL Server Auth likely | None | Part 1 |
| {3653D0A0-E512-4269-94C0-866616C4F312}   | OLE DB          | Server: [Inferred], Database: [Inferred]  | ETL Run Status updates | SQL Server Auth likely | None | Part 1 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| COSMOS_Dimension.dtsx |  [Inferred]     | Parent package executes child | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION") OR (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") | Executes Dimension Package        | Part 1,2,3 |
| COSMOS_Fact.dtsx      |  [Inferred]     | Parent package executes child | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT") OR (UPPER(TRIM(@[$Project::PRM_PROCESS_NODE])) == "ALL") | Executes Fact Package              | Part 1,2,3 |
| COSMOS_Landing.dtsx   |  [Inferred]     | Parent package executes child | True  | Executes Landing Package           | Part 1,2,3 |
| COSMOS_Staging.dtsx   |  [Inferred]     | Parent package executes child | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING") OR True | Executes Staging Package         | Part 1,2,3 |

## 3. Package Flow Analysis

The package `COSMOS_Master.dtsx` orchestrates the execution of other packages based on the value of the project parameter `PRJ_PRM_PROCESS_NODE`.

*   The package first executes an expression task `EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process_Node` which always evaluates to true.
*   Based on the value of `PRJ_PRM_PROCESS_NODE` the package executes different child packages:
    *   If `PRJ_PRM_PROCESS_NODE` is "DIMENSION", then `EPKGT_COSMOS_DIMENSION` is executed.
    *   If `PRJ_PRM_PROCESS_NODE` is "FACT", then `EPKGT_COSMOS_FACT` is executed.
    *   If `PRJ_PRM_PROCESS_NODE` is "STAGING", then `EPKGT_COSMOS_STAGING` is executed.
    *   `EPKGT_COSMOS_LANDING` is always executed.
*   If `PRJ_PRM_PROCESS_NODE` is "ALL", then `EPKGT_COSMOS_STAGING`, `EPKGT_COSMOS_DIMENSION` and `EPKGT_COSMOS_FACT` are executed in sequence.
*   The package contains a sequence container `DELETE AFTER CONFIGURING THE PROJECT` which tests the connection to different databases using Execute SQL Tasks. This container seems to be for testing purposes and should be removed in production.

### Event Handlers

The package uses event handlers for `OnPreExecute`, `OnPostExecute`, and `OnError` events. These event handlers update the `ETL_RUN_STATUS` table.

*   **OnPreExecute:**
    *   Executes `ESQLT-Set Hung Job Status to Terminated for Master`, which executes the SQL statement in the `User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER` variable.
    *   Executes `ESQLT-Set Hung Job Status to Terminated for Sub Components`, which executes the SQL statement in the `User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS` variable.
    *   Executes `ESQLT- Create Record with Running Status for Master Package`, which executes the SQL statement in the `User::V_SQL_INSERT_ON_PRE_EXECUTE_MASTER_RUN_STATUS` variable.
*   **OnPostExecute:**
    *   Executes `ESQLT- Update ETL Process Status to Succeeded`, which executes the SQL statement in the `User::V_SQL_UPDATE_ON_POST_EXECUTE` variable.
*   **OnError:**
    *   Executes `ESQLT- Update ETL Process Status to Failed`, which executes the SQL statement in the `User::V_SQL_UPDATE_ON_ERROR` variable.

## 4. Code Extraction

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_MASTER_RUN_STATUS
INSERT INTO [ETL_RUN_STATUS]
           ([ETL_COMPONENT_ID]           
           ,[ETL_RUN_STATUS_DESC]
           ,[ETL_RUN_MAIN_COMPONENT_IND]
           ,[ETL_RUN_RECORD_CREA_DT]
           ,[ETL_RUN_RECORD_UPDT_DT])
     VALUES
           (
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'COSMOS_Master.dtsx' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS')           
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query is used to insert a record in the ETL_RUN_STATUS table with status 'RUNNING' when the master package starts execution.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER
-- STEP 01 
-- SET HUNG JOBS STATUS FOR MAIN COMPONENT
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = 13
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
  );
```

Context: This SQL query is used to update the status of any previously running instance of the master package to 'TERMINATED BY RERUN'.

```markdown
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
    WHERE ETL_COMPONENT_ID = 13
     AND ETL_SUB_COMPONENT_NM = 'COSMOS_Landing.dtsx'
    )
   AND ETL_COMPONENT_ID = 13
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID = 13
     AND ETL_SUB_COMPONENT_NM = 'COSMOS_Staging.dtsx'
    )
   AND ETL_COMPONENT_ID = 13
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
  UNION
  
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS
  WHERE etl_sub_component_id IN (
    SELECT ETL_SUB_COMPONENT_ID
    FROM ETL_SUB_COMPONENT
    WHERE ETL_COMPONENT_ID = 13
       AND ETL_SUB_COMPONENT_NM = 'COSMOS_Dimension.dtsx'
      )
     AND ETL_COMPONENT_ID = 13
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
    
    UNION
    
    SELECT ETL_RUN_STATUS_ID
    FROM ETL_RUN_STATUS
    WHERE etl_sub_component_id IN (
      SELECT ETL_SUB_COMPONENT_ID
      FROM ETL_SUB_COMPONENT
      WHERE ETL_COMPONENT_ID = 13
       AND ETL_SUB_COMPONENT_NM = 'COSMOS_Fact.dtsx'
      )
     AND ETL_COMPONENT_ID = 13
     AND ETL_RUN_STATUS_DESC = 'RUNNING'
     AND ETL_RUN_MAIN_COMPONENT_IND = 0
  );
```

Context: This SQL query is used to update the status of any previously running instances of the child packages to 'TERMINATED BY RERUN'.

```markdown
-- From User::V_SQL_UPDATE_ON_ERROR
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(ETL_RUN_STATUS_ID)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'COSMOS_Master.dtsx'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;
```

Context: This SQL query is used to update the status of the master package to 'FAILED' in the ETL_RUN_STATUS table when an error occurs.

```markdown
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(etl_run_status_id)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'COSMOS_Master.dtsx'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/COSMOS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

Context: This SQL query is used to update the status of the master package to 'SUCCEEDED' in the ETL_RUN_STATUS table when the package completes successfully.

## 5. Output Analysis

| Destination Table   | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS  | Stores ETL run status information  | Part 1, Event Handlers |

## 6. Package Summary

*   **Input Connections:** 5
*   **Output Destinations:** 1 (`ETL_RUN_STATUS`)
*   **Package Dependencies:** 4
*   **Activities:**
    *   Execute Package Tasks: 4
    *   Execute SQL Tasks: 10 (5 in connection test sequence container, 3 in OnPreExecute, 1 in OnPostExecute, 1 in OnError)
    *   Expression Tasks: 5 (1 main flow and 1 in each event handler)
    *   Sequence Containers: 1 (connection test)
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: The initial queries in `OnPreExecute` to terminate hung jobs might take a while depending on the size of the `ETL_RUN_STATUS` table.
*   Critical path analysis: The critical path depends on the value of `PRJ_PRM_PROCESS_NODE`.
*   Error handling mechanisms: The package uses event handlers to log errors and update the `ETL_RUN_STATUS` table.
