## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {4382894D-116E-46C6-BEBD-4E4EFACB27AE} | OLE DB          | Server: [Inferred], Database: [Inferred] | Used within event handlers to update ETL process status | SQL Server Auth likely | User::V_SQL_UPDATE_ON_ERROR, User::V_SQL_UPDATE_ON_POST_EXECUTE, User::V_SQL_INSERT_ON_PRE_EXECUTE_MASTER_RUN_STATUS, User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER, User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS | Part 1, All Event Handlers|

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| DATA_HUB_01.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING")  | Executes when process node is STAGING | Part 1|
| DATA_HUB_00_GCS_LOAD.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") \|\| (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING") | Executes when process node is ALL or STAGING | Part 1|
| MART_GC_DIMS.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") OR (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION") | Executes when process node is ALL or DIMENSION | Part 1|
| MART_GC_FACTS.dtsx | [Inferred] | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT") OR  (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") | Executes when process node is FACT or ALL | Part 1|
| SWS_VALIDATE_01.dtsx | [Inferred] | Parent | Always after MART_GC_FACTS.dtsx | Executes always after the fact package | Part 1|

## 3. Package Flow Analysis

The package `GC_MASTER.dtsx` orchestrates the execution of several other packages based on the value of the project parameter `PRJ_PRM_PROCESS_NODE`.

*   The package begins with an `Expression Task`, which always evaluates to true.
*   Based on the value of `PRJ_PRM_PROCESS_NODE` the package executes different branches:

    *   **STAGING:** Executes `DATA_HUB_01.dtsx` and `DATA_HUB_00_GCS_LOAD.dtsx`
    *   **DIMENSION:** Executes `MART_GC_DIMS.dtsx`
    *   **FACT:** Executes `MART_GC_FACTS.dtsx`
    *   **ALL:** Executes all packages, following a specific order: `DATA_HUB_00_GCS_LOAD.dtsx`, `DATA_HUB_01.dtsx`, `MART_GC_DIMS.dtsx`, `MART_GC_FACTS.dtsx`, `SWS_VALIDATE_01.dtsx`
*   The package also contains Event Handlers that manage the ETL process status.

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
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS')           
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query inserts a record into the `ETL_RUN_STATUS` table, marking the master package as running.

```sql
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
		ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND 
	      ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'     
		--ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS_GC'
		)
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
  )
;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table, marking any previous running instance of the master package as terminated by rerun.

```sql
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
					WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
					)
			AND ETL_SUB_COMPONENT_NM = 'DATA_HUB_01.DTSX'  
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
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
					WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
					)
			AND ETL_SUB_COMPONENT_NM = 'DATA_HUB_02_PROJECT_WBS.DTSX'      
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
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
					WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
					)
			AND ETL_SUB_COMPONENT_NM = 'DATA_HUB_03_PROJECT_BUDGET.DTSX'      
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
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
					WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
					)
			AND ETL_SUB_COMPONENT_NM = 'MART_GC_DIMS.DTSX'      
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
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
					WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
					)
			AND ETL_SUB_COMPONENT_NM = 'MART_GC_FACTS.DTSX'      
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
		)
		AND ETL_RUN_STATUS_DESC = 'RUNNING'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0
    	
)                                                                                        
;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table, marking any previous running instances of the sub-components  as terminated by rerun.

```sql
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
    WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table, marking the master package as failed.

```sql
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
    WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );
```

Context: This SQL query updates the `ETL_RUN_STATUS` table, marking the master package as succeeded.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS           | Stores ETL run status information  | All SQL Tasks in Event Handlers                                   |

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** 1 (`ETL_RUN_STATUS` table)
*   **Package Dependencies:** 5
*   **Activities:**
    *   Execute Package Tasks: 5
    *   Expression Task: 1
    *   Execute SQL Tasks: 7 (3 in `OnPreExecute`, 1 in `OnError`, 1 in `OnPostExecute`)
*   **Transformations:** None
*   **Script tasks:** 0
*   **Overall package complexity assessment:** Medium. The package is primarily an orchestrator, with conditional execution of other packages.
*   **Potential performance bottlenecks:** The queries updating `ETL_RUN_STATUS` might become a bottleneck if the table is very large and not properly indexed.
*   **Critical path analysis:** The critical path depends on the value of `PRJ_PRM_PROCESS_NODE`. When set to "ALL", the critical path includes all dependent packages executed sequentially.
*   **Document error handling mechanisms:** The `OnError` event handler updates the `ETL_RUN_STATUS` table with a "FAILED" status.
