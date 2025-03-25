## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {3653D0A0-E512-4269-94C0-866616C4F312}           | OLE DB          | Server: [Inferred], Database: [Inferred]  | ETL Metadata updates | SQL Server Auth likely | None            | Event Handlers                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| FC_Dimension.dtsx | [Inferred] | Child | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION") or Always | Executes FC_Dimension package | Package Control Flow |
| FC_Staging.dtsx | [Inferred] | Child | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING") | Executes FC_Staging package | Package Control Flow |

## 3. Package Flow Analysis

The package `FC_Master.dtsx` consists of the following main components:

*   **EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process_Node**: An Expression Task that always evaluates to true (1 == 1). It acts as a starting point.
*   **EPKGT- FC STAGING**: An Execute Package Task that executes the `FC_Staging.dtsx` package. The execution is conditional based on the project parameter `PRJ_PRM_PROCESS_NODE`.
*   **EPKGT- FC Dimension**: An Execute Package Task that executes the `FC_Dimension.dtsx` package. The execution is conditional based on the project parameter `PRJ_PRM_PROCESS_NODE` or triggered by the first task.

The precedence constraints define the execution flow:

1.  The Expression Task always executes.
2.  `FC_Staging.dtsx` executes if `PRJ_PRM_PROCESS_NODE` is "ALL" or "STAGING".
3.  `FC_Dimension.dtsx` executes if `PRJ_PRM_PROCESS_NODE` is "ALL" or "DIMENSION" or triggered by the first.

The package also includes event handlers for `OnPreExecute`, `OnPostExecute`, and `OnError` events. These event handlers primarily update the `ETL_RUN_STATUS` table.

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
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'FC_Master.dtsx' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC')           
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;

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
		--ETL_COMPONENT_NM = 'FC_Master.dtsx'    -- 'STRATEGIA_MASTER.DTSX'
		ETL_COMPONENT_NM = 'STRATEGIA_MASTER.DTSX'
		AND 
		--ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'      -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
		ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
		)
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
  )
;

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
					WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
					)
			AND ETL_SUB_COMPONENT_NM = 'FC_Staging.dtsx'    -- 'STRATEGIA_STAGING.DTSX'   
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
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
					WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
					AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
					)
			AND ETL_SUB_COMPONENT_NM = 'FC_Dimension.dtsx'    -- 'STRATEGIA_DIMENSION.DTSX'  
		)
		AND ETL_COMPONENT_ID IN 
		(
		SELECT ETL_COMPONENT_ID
		FROM ETL_COMPONENT
		WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
		)
		AND ETL_RUN_STATUS_DESC = 'RUNNING'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0

   
	
    
)                                                                                        -- First Bracket End
;

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
    WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;

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
    WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  );

```

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS  | Stores ETL run status updates   | Event Handlers|

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** `ETL_RUN_STATUS`
*   **Package Dependencies:** 2 (`FC_Staging.dtsx`, `FC_Dimension.dtsx`)
*   **Activities:**
    *   Execute Package Tasks: 2
    *   Expression Tasks: 4
    *   Execute SQL Tasks: 7
*   **Transformations:** None (within this master package)
*   **Script tasks:** 0

Overall package complexity assessment: Low to Medium.

Potential performance bottlenecks: The SQL updates to ETL_RUN_STATUS could become a bottleneck if run frequently and the table is not properly indexed.

Critical path analysis: The critical path depends on the value of the `PRJ_PRM_PROCESS_NODE` project parameter.

Error handling mechanisms: The `OnError` event handler updates the `ETL_RUN_STATUS` table with a "FAILED" status.
