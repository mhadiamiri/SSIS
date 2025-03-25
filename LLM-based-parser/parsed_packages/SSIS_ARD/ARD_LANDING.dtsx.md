## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {9FD41A97-06DC-4776-9CEA-86CDABBBC4C3}           | OLE DB          | Server: [Inferred], Database: [Inferred] | Updates ETL Status | SQL Server Auth likely | User::V_SQL_UPDATE_ON_ERROR, User::V_SQL_UPDATE_ON_POST_EXECUTE, User::V_SQL_INSERT_ON_PRE_EXECUTE_RUN_STATUS            | Part 2, 3                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| ARD_OPERA_LANDING.dtsx |  [Inferred]                   | Child of ARD_LANDING.dtsx                | Success of ARD_PRIME_LANDING.dtsx| Executes after ARD_PRIME_LANDING.dtsx | Part 1, 2, 3|
| ARD_PRIME_LANDING.dtsx  |  [Inferred]                    | Child of ARD_LANDING.dtsx               | Success of EXPRESSIONT- LAND - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode | Executes after the Expression task | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `ARD_LANDING.dtsx` orchestrates the execution of two child packages: `ARD_PRIME_LANDING.dtsx` and `ARD_OPERA_LANDING.dtsx`. It also includes tasks for managing ETL status.

*   **EXPRESSIONT- LAND - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode:** This is an Expression Task that evaluates the expression `1 == 1`. It always evaluates to true, effectively acting as a starting point for the package.
*   **EPKGT-ARD_PRIME_LANDING:** This is an Execute Package Task that executes the `ARD_PRIME_LANDING.dtsx` package. It executes upon success of EXPRESSIONT- LAND - Start Task.
*   **EPKGT-ARD_OPERA_LANDING:** This is an Execute Package Task that executes the `ARD_OPERA_LANDING.dtsx` package. It executes upon success of `ARD_PRIME_LANDING.dtsx`.

#### Event Handlers:

*   **OnPreExecute:**
    *   **ESQLT- Create Record with Running Status:** Executes a SQL statement defined in the `User::V_SQL_INSERT_ON_PRE_EXECUTE_RUN_STATUS` variable to update the ETL run status to 'RUNNING'.
    *   **EXPRESSIONT- Start Task:** Expression Task that evaluates the expression `1 == 1`.
*   **OnPostExecute:**
    *   **ESQLT- Update ETL Process Status to Succeeded:** Executes a SQL statement defined in the `User::V_SQL_UPDATE_ON_POST_EXECUTE` variable to update the ETL run status to 'SUCCEEDED'.
    *   **EXPRESSIONT- Start Task:** Expression Task that evaluates the expression `1 == 1`.
*   **OnError:**
    *   **ESQLT- Update ETL Process Status to Failed:** Executes a SQL statement defined in the `User::V_SQL_UPDATE_ON_ERROR` variable to update the ETL run status to 'FAILED'.
    *   **EXPRESSIONT- Start Task:** Expression Task that evaluates the expression `1 == 1`.

## 4. Code Extraction

```markdown
-- SQL from User::V_SQL_INSERT_ON_PRE_EXECUTE_RUN_STATUS
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
   AND ETL_SUB_COMPONENT_NM = 'ARD_LANDING.dtsx'   
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: This SQL query inserts a record into the ETL_RUN_STATUS table indicating the start of the package execution.

```markdown
-- SQL from User::V_SQL_UPDATE_ON_ERROR
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ARD_LANDING.dtsx'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query updates the ETL_RUN_STATUS table to indicate that the package execution has failed.

```markdown
-- SQL from User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'ARD_LANDING.dtsx'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
```

Context: This SQL query updates the ETL_RUN_STATUS table to indicate that the package execution has succeeded.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS  | Stores the status of ETL package executions   | Event Handlers (OnPreExecute, OnPostExecute, OnError) |

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** 1 (ETL_RUN_STATUS)
*   **Package Dependencies:** 2 (ARD_PRIME_LANDING.dtsx, ARD_OPERA_LANDING.dtsx)
*   **Activities:**
    *   Execute Package Tasks: 2
    *   Execute SQL Tasks: 3
    *   Expression Tasks: 4
*   Overall package complexity assessment: Low to medium.
*   Potential performance bottlenecks: The execution of child packages could be a bottleneck depending on their complexity.
*   Critical path analysis: The critical path is the sequential execution of the Expression Task, ARD_PRIME_LANDING, and ARD_OPERA_LANDING.
*   Error handling mechanisms: The package includes an OnError event handler that updates the ETL status to 'FAILED'. The whole error handling is depending on variables, which is not robust.
