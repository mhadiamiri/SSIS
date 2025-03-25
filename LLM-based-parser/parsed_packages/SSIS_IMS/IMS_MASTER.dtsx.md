## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {3653D0A0-E512-4269-94C0-866616C4F312} | OLE DB | Server: [Inferred], Database: [Inferred] |  Execute SQL Tasks in event handlers to update ETL status |  SQL Server Authentication likely | None | Event Handlers |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| IMS_DIMENSION.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION") or (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") after IMS_STAGING | Package Parameter |
| IMS_FACT.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT") or (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") after IMS_DIMENSION | Package Parameter |
| IMS_STAGING.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING")  | Package Parameter |

## 3. Package Flow Analysis

The package `IMS_MASTER.dtsx` acts as a master package, orchestrating the execution of other packages based on the value of the `PRJ_PRM_PROCESS_NODE` project parameter.

*   The package starts with an Expression Task that always evaluates to true.
*   Based on the value of `PRJ_PRM_PROCESS_NODE`, one or more Execute Package Tasks (EPKGT) are executed:
    *   `EPKGT-IMS_SSIS_DFAIT_STAGING` (executes `IMS_STAGING.dtsx`)
    *   `EPKGT-IMS DIMENSION` (executes `IMS_DIMENSION.dtsx`)
    *   `EPKGT-IMS FACT` (executes `IMS_FACT.dtsx`)
*   The precedence constraints determine the execution order and conditions. The `ALL` option triggers the execution of all three packages in a specific order: `IMS_STAGING` -> `IMS_DIMENSION` -> `IMS_FACT`. Other values trigger a subset of package executions.
* Event Handlers are configured for `OnPreExecute`, `OnPostExecute`, and `OnError` events. These handlers execute SQL tasks to update the `ETL_RUN_STATUS` table, logging the status of the master package.

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
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'IMS_MASTER.DTSX' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS')           
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query inserts a new record into the `ETL_RUN_STATUS` table with a 'RUNNING' status when the master package starts.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN 
  (
  SELECT ETL_RUN_STATUS_ID
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE 
		--ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'    -- 'STRATEGIA_MASTER.DTSX'
		ETL_COMPONENT_NM = 'STRATEGIA_MASTER.DTSX'
		AND 
		--ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'      -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
		ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
		)
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
  )
;
```

Context: This SQL Query updates the status of previously running ETL processes to "TERMINATED BY RERUN" before starting the current process.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE ETL_RUN_STATUS_ID IN 

(                                  -- First Bracket Start
	SELECT ETL_RUN_STATUS_ID
	FROM ETL_RUN_STATUS
	WHERE ETL_SUB_COMPONENT_ID IN 
		(                              
			SELECT ETL_SUB_COMPONENT_ID
			FROM ETL_SUB_COMPONENT
			WHERE ETL_COMPONENT_ID IN 
					(
					SELECT ETL_COMPONENT_ID
					FROM ETL_COMPONENT
					WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
					)
			AND ETL_SUB_COMPONENT_NM = 'STRATEGIA_STAGING.dtsx'    -- 'STRATEGIA_STAGING.DTSX'   
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
		)
		AND ETL_RUN_STATUS_DESC = 'RUNNING'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
 
	UNION


		SELECT ETL_RUN_STATUS_ID
	FROM ETL_RUN_STATUS
	WHERE ETL_SUB_COMPONENT_ID IN 
		(                               -- Second Bracket Start
			SELECT ETL_SUB_COMPONENT_ID
			FROM ETL_SUB_COMPONENT
			WHERE ETL_COMPONENT_ID IN 
					(
					SELECT ETL_COMPONENT_ID
					FROM ETL_COMPONENT
					WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
					)
			AND ETL_SUB_COMPONENT_NM = 'STRATEGIA_DIMENSION.dtsx'    -- 'STRATEGIA_DIMENSION.DTSX'  
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
		)
		AND ETL_RUN_STATUS_DESC = 'RUNNING'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0

   
	UNION


	SELECT ETL_RUN_STATUS_ID
	FROM ETL_RUN_STATUS
	WHERE ETL_SUB_COMPONENT_ID IN 
		(                               -- Second Bracket Start
			SELECT ETL_SUB_COMPONENT_ID
			FROM ETL_SUB_COMPONENT
			WHERE ETL_COMPONENT_ID IN 
					(
					SELECT ETL_COMPONENT_ID
					FROM ETL_COMPONENT
					WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
					)
			AND ETL_SUB_COMPONENT_NM = 'STRATEGIA_FACT.dtsx'    -- 'STRATEGIA_FACT.DTSX' 
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
		)
		AND ETL_RUN_STATUS_DESC = 'RUNNING'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0
    
)                                                                                        -- First Bracket End
;
```

Context: This SQL Query updates the status of previously running sub component ETL processes to "TERMINATED BY RERUN" before starting the current process.

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
    WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to set the status to 'FAILED' when an error occurs in the master package.

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
    WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to set the status to 'SUCCEEDED' when the master package completes successfully.

```markdown
-- From constraint expressions
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION")
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRM_PROCESS_NODE])) == "STAGING")
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT")
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")
(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")
```

Context: These are expressions used in precedence constraints to determine which packages to execute based on the value of the `PRJ_PRM_PROCESS_NODE` project parameter.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS | Stores the status of ETL runs | Event Handlers |

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** 1 (ETL_RUN_STATUS)
*   **Package Dependencies:** 3 (IMS_STAGING.dtsx, IMS_DIMENSION.dtsx, IMS_FACT.dtsx)
*   **Activities:**
    *   Execute Package Tasks: 3
    *   Expression Task: 1 + 2 in the event handlers for a total of 3
    *   Execute SQL Task: 6 (3 in OnPreExecute, 1 in OnError, and 1 in OnPostExecute)
*   **Transformations:** None explicitly defined in the master package XML. Transformations are expected to be within the dependent packages.
*   **Script tasks:** 0
*   Overall package complexity assessment: Medium. The package is relatively simple in its control flow, but the dependency on project parameters and multiple dependent packages increases the complexity.
*   Potential performance bottlenecks: The performance will largely depend on the execution time of the dependent packages. Ensure that indexing and query optimization are performed in the dependent packages.
*   Critical path analysis: The critical path depends on the value of the `PRJ_PRM_PROCESS_NODE` parameter. If set to `ALL`, the critical path includes the sequential execution of `IMS_STAGING`, `IMS_DIMENSION`, and `IMS_FACT`.
*   Document error handling mechanisms: The package uses event handlers to log errors and update the ETL status in the `ETL_RUN_STATUS` table. When an error occurs, the `OnError` event handler executes an SQL task to update the status to 'FAILED'. The `OnPreExecute` and `OnPostExecute` event handlers update the status to 'RUNNING' and 'SUCCEEDED', respectively.
