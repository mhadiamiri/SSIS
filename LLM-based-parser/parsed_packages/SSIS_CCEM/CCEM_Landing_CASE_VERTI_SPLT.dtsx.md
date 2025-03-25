## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager  | EXCEL           | Data Source=C:\Users\admLIUJ6\Documents\Project\Financial Sample.xlsx | Source for data | File system access | None | Part 1, Part 2, Part 3 |
| ODS_CCEM           | OLE DB           | [Inferred] | Destination for data  | SQL Server Auth likely | None | Part 1, Part 2, Part 3 |
| CCEM_SOURCE           | Dynamics CRM           | [Inferred] | Source for data  | Dynamics 365 Auth likely | None | Part 1, Part 2, Part 3 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   Package Variables:
    *   `User::V_ETL_COMPONENT_NAME`:  Evaluates to "CCEM_Landing_CASE_VERTI_SPLT.DTSX".
    *   `User::V_SQL_INSERT_ON_PRE_EXECUTE`: SQL INSERT statement for `ETL_RUN_STATUS` table.
    *   `User::V_SQL_UPDATE_ON_ERROR`: SQL UPDATE statement to set `ETL_RUN_STATUS` to 'FAILED'.
    *   `User::V_SQL_UPDATE_ON_POST_EXECUTE`: SQL UPDATE statement to signal 'SUCCEEDED'.

*   Connection Managers:
    *   `Excel Connection Manager`: Excel connection to source data.
    *   `Project.ConnectionManagers[ODS_CCEM]`: OLE DB connection to destination database.
    *   `Project.ConnectionManagers[CCEM_SOURCE]`: Dynamics CRM Connection

*   Activities in Execution Order:
    1.  `EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`:  Expression task (1==1).
    2.  `ESQLT-Truncate-CCEM_CASE`: Execute SQL Task to truncate the `ccem_case` table.
    3.  `DFT-L_ccem_case`: Data flow task.
    4.  `CCEM_CASE_SPLIT`: Sequence Container.
        1.  `DFT-L_ccem_case 1`: Data flow task.
        2.  `DFT-L_ccem_case 2`: Data flow task.
    5.  `DFT-L_ccem_case 3`: Data flow task.
    6.  `DFT-L_ccem_case 4`: Data flow task.
    7.  `DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON`: Data flow task.

#### DFT-L_ccem_case

*   **Source:** Dynamics CRM Source (CRM_SRC-ccem_case1) extracts data from `ccem_case` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_case` saves successfully mapped rows to `dbo.ccem_case`.

#### DFT-L_ccem_case 1

*   **Source:** Dynamics CRM Source (Dynamics CRM Source_ccem_case1) extracts data from `ccem_case` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_case1` saves successfully mapped rows to `dbo.ccem_case1`.

#### DFT-L_ccem_case 2

*   **Source:** Dynamics CRM Source (Dynamics CRM Source_ccem_case1) extracts data from `ccem_case` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_case2` saves successfully mapped rows to `dbo.ccem_case2`.

#### DFT-L_ccem_case 3

*   **Source:** Dynamics CRM Source (Dynamics CRM Source_ccem_case1) extracts data from `ccem_case` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_case3` saves successfully mapped rows to `dbo.ccem_case3`.

#### DFT-L_ccem_case 4

*   **Source:** Dynamics CRM Source (Dynamics CRM Source_ccem_case1) extracts data from `ccem_case` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_case4` saves successfully mapped rows to `dbo.ccem_case4`.

#### DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON

*   **Source:** Dynamics CRM Source (CRM_SRC-ccem_affectedperson) extracts data from `ccem_affectedperson` entity from a Dynamics CRM instance.
*   **Transformations:**
    *   `Derived Column`: Adds `etl_crea_dt` and `etl_updt_dt` by using the `GETDATE()` function.
*   **Destinations:**
    *   `OLEDB_DEST-ccem_emrgncy_crisis_affectedperson` saves successfully mapped rows to `dbo.ccem_emrgncy_crisis_affectedperson`.

## 4. Code Extraction

```sql
TRUNCATE TABLE ccem_case;
```

Context: This SQL statement truncates the `ccem_case` table.

```sql

 INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )
VALUES (8
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = 'CCEM_Landing.dtsx'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;

```

Context: This SQL statement is used in the `User::V_SQL_INSERT_ON_PRE_EXECUTE` to insert a record into the `ETL_RUN_STATUS` table with a 'RUNNING' status at the start of the package.

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 8
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = 'CCEM_Landing.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL statement is used in the `User::V_SQL_UPDATE_ON_ERROR` to update the `ETL_RUN_STATUS` table with a 'FAILED' status upon package error.

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 8
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = 'CCEM_Landing.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL statement is used in the `User::V_SQL_UPDATE_ON_POST_EXECUTE` to update the `ETL_RUN_STATUS` table with a 'SUCCEEDED' status at the end of successful package execution.

## 5. Output Analysis

| Destination Table                        | Description                              | Source Part |
|-----------------------------------------|------------------------------------------|-------------|
| `dbo.ccem_case` | Destination table for CRM source, `ccem_case` entity | DFT-L_ccem_case |
| `dbo.ccem_case1` | Destination table for CRM source, `ccem_case` entity | DFT-L_ccem_case 1 |
| `dbo.ccem_case2` | Destination table for CRM source, `ccem_case` entity | DFT-L_ccem_case 2 |
| `dbo.ccem_case3` | Destination table for CRM source, `ccem_case` entity | DFT-L_ccem_case 3 |
| `dbo.ccem_case4` | Destination table for CRM source, `ccem_case` entity | DFT-L_ccem_case 4 |
| `dbo.ccem_emrgncy_crisis_affectedperson` | Destination table for CRM source, `ccem_affectedperson` entity | DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON |

## 6. Package Summary

*   **Input Connections:** 3
*   **Output Destinations:** 6
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 6
    *   Execute SQL Tasks: 2
    *   Expression Tasks: 3
    *   Derived Column: 7
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: CRM source and OLE DB Destinations could cause bottlenecks.
*   Critical path analysis: The critical path is the sequential execution of tasks within the `CCEM_CASE_SPLIT` sequence container.
*   Error handling mechanisms: OnError event handler updates ETL process status to 'FAILED'.
