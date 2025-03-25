## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {3653D0A0-E512-4269-94C0-866616C4F312} | OLE DB | Server: [Inferred], Database: [Inferred] | Used in Event Handlers to update ETL status | SQL Server Authentication likely | None | All Event Handlers |
| {347E8B01-4F97-43D9-98BC-39CEE8A43223} | OLE DB | Server: [Inferred], Database: [Inferred] | Used in "Execute SQL Task Stored Proc ETL Monitoring" | SQL Server Authentication likely | None | Main Package |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| PATHFINDER_Dimension.dtsx | [Inferred]       | Parent                       | Always                               |                                     | Main Package |
| PATHFINDER_ODS.dtsx       | [Inferred]      | Parent                       | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ODS") |                                    | Main Package |
| PATHFINDER_Staging.dtsx     | [Inferred]      | Parent                       | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL")   |                                    | Main Package |

## 3. Package Flow Analysis

The package `PATHFINDER_Master.dtsx` is a master package executing other packages and performing ETL monitoring.

*   The package starts with an `Expression Task`: `EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process_Node` which always evaluates to true (1==1).
*   Based on the project parameter `[$Project::PRJ_PRM_PROCESS_NODE]`, different execution paths are taken.
*   **`EPKGT- <SubjectArea> ODS`**: Executes `PATHFINDER_ODS.dtsx` if `[$Project::PRJ_PRM_PROCESS_NODE]` is "ALL" or "ODS".
*   **`EPKGT- <SubjectArea> STAGING`**: Executes `PATHFINDER_Staging.dtsx` if `[$Project::PRJ_PRM_PROCESS_NODE]` is "ALL".
*   **`EPKGT- <SubjectArea> DIMENSION`**: Executes `PATHFINDER_Dimension.dtsx` after `PATHFINDER_Staging.dtsx`.
*   Finally, the package executes `Execute SQL Task Stored Proc ETL Monitoring` which calls `stg_neics.dbo.sp_qa_NEICS_etl`.

#### Event Handlers:

*   The package implements `OnPreExecute`, `OnPostExecute`, and `OnError` event handlers at the package level.
*   These event handlers update the `ETL_RUN_STATUS` table to reflect the status of the package execution.
*   The `EPKGT-  <SubjectArea> STAGING` task also implements `OnPostExecute` and `OnError` event handlers to update the ETL status for the staging package.

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
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER') 
          
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query inserts a record into the `ETL_RUN_STATUS` table when the master package starts to indicate it is running.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER
UPDATE ETL_RUN_STATUS 

    SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
, [ETL_RUN_RECORD_UPDT_DT] = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
  
    (
SELECT ETL_RUN_STATUS_ID
  
       FROM ETL_RUN_STATUS R
  
      WHERE R.ETL_COMPONENT_ID = 

            (
SELECT ETL_COMPONENT_ID

               FROM ETL_COMPONENT
                                
              WHERE 
ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'  
                AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER')
   
    AND ETL_RUN_STATUS_DESC = 'RUNNING'
   
    AND ETL_RUN_MAIN_COMPONENT_IND = 1
)
;
```

Context: This SQL query updates the status of any previous running instance of the master package to 'TERMINATED BY RERUN' before starting a new execution.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS
UPDATE ETL_RUN_STATUS

    SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
, ETL_RUN_RECORD_UPDT_DT = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
    

(-- First Bracket Start
                

      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
   
         SELECT ETL_SUB_COMPONENT_ID
                
           FROM ETL_SUB_COMPONENT
                
          WHERE ETL_COMPONENT_ID IN 

            (
SELECT ETL_COMPONENT_ID
        
               FROM ETL_COMPONENT
                
              WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
                                                                                
                AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)

            AND ETL_SUB_COMPONENT_NM = 'ODS_NEICS.dtsx'    -- 'ODS_NEICS.DTSX'
			)
                                
            AND ETL_COMPONENT_ID IN 

                (
SELECT ETL_COMPONENT_ID
                
                   FROM ETL_COMPONENT
                                
                  WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'

                    AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)

            AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
            AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
UNION
              
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
       (SELECT ETL_SUB_COMPONENT_ID
                
          FROM ETL_SUB_COMPONENT
                                                
         WHERE ETL_COMPONENT_ID IN 
         
(
SELECT ETL_COMPONENT_ID
                
              FROM ETL_COMPONENT

             WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'

                       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER')

           AND ETL_SUB_COMPONENT_NM = 'NEICS_Staging.dtsx'    -- 'NEICS_STAGING.DTSX'
		   )
-- Second Bracket
           AND ETL_COMPONENT_ID IN 

               (
SELECT ETL_COMPONENT_ID

                  FROM ETL_COMPONENT

                 WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'

                   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)

           AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
           AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
 
UNION
                                
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
   
        SELECT ETL_SUB_COMPONENT_ID
                
          FROM ETL_SUB_COMPONENT
                
         WHERE ETL_COMPONENT_ID IN 

           (
SELECT ETL_COMPONENT_ID
        
              FROM ETL_COMPONENT
                
             WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
                                                                                
               AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)

           AND ETL_SUB_COMPONENT_NM = 'NEICS_Dimension.dtsx'    -- 'NEICS_DIMENSION.DTSX'
		   )                -- Second Bracket             
           AND ETL_COMPONENT_ID IN 

                 (
SELECT ETL_COMPONENT_ID
                
                    FROM ETL_COMPONENT
                                
                   WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'

                     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER')

           AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
           AND ETL_RUN_MAIN_COMPONENT_IND = 0

                  
UNION

                
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
                                                
        SELECT ETL_SUB_COMPONENT_ID
                                                
          FROM ETL_SUB_COMPONENT
                                                
         WHERE ETL_COMPONENT_ID IN 

           (
SELECT ETL_COMPONENT_ID
                                                                                
              FROM ETL_COMPONENT
                                                                                
             WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
                                                                                
               AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)
                                
               AND ETL_SUB_COMPONENT_NM = 'NEICS_Fact.dtsx'    -- 'NEICS_FACT.DTSX' 
)                -- Second Bracket End    
           AND ETL_COMPONENT_ID IN 

                                       (
SELECT ETL_COMPONENT_ID
                                
                                  FROM ETL_COMPONENT
                                
                                 WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'

                                   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)
                                
        AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
        AND ETL_RUN_MAIN_COMPONENT_IND = 0


    )   -- First Bracket End
;
```

Context: This SQL query updates the status of any previous running instances of the sub-components (ODS, Staging, Dimension, Fact) to 'TERMINATED BY RERUN' before starting a new execution.

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
    WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;
```

Context: This SQL query updates the status of the master package to 'FAILED' in case of an error.

```markdown
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
UPDATE ETL_RUN_STATUS

    SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
   (
SELECT max(etl_run_status_id)
  
      FROM ETL_RUN_STATUS R
  
     WHERE R.ETL_COMPONENT_ID = 
     (
SELECT ETL_COMPONENT_ID
    
        FROM ETL_COMPONENT
    
       WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
    
         AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
)
   
       AND ETL_RUN_STATUS_DESC = 'RUNNING'
   
       AND ETL_RUN_MAIN_COMPONENT_IND = 1
   
       AND ETL_SUB_COMPONENT_ID IS NULL
);
```

Context: This SQL query updates the status of the master package to 'SUCCEEDED' after successful execution.

```sql
-- From Execute SQL Task Stored Proc ETL Monitoring
exec stg_neics.dbo.sp_qa_NEICS_etl;
```

Context: This SQL query executes a stored procedure for ETL monitoring.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS  | Stores the status of ETL package executions | Event Handlers |

## 6. Package Summary

*   **Input Connections:** 2
*   **Output Destinations:** `ETL_RUN_STATUS` table
*   **Package Dependencies:** 3 (PATHFINDER_Dimension.dtsx, PATHFINDER_ODS.dtsx, PATHFINDER_Staging.dtsx)
*   **Activities:**
    *   Execute Package Tasks: 3
    *   Execute SQL Tasks: 7
    *   Expression Tasks: 5
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: The stored procedure `stg_neics.dbo.sp_qa_NEICS_etl` might be a bottleneck if it's not optimized.
*   Critical path analysis: The critical path depends on the value of the `[$Project::PRJ_PRM_PROCESS_NODE]` parameter.
*   Error handling mechanisms: The package implements error handling through event handlers that update the `ETL_RUN_STATUS` table.
