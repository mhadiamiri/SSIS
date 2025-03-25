```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager | EXCEL                  | `Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\Documents\\Project\\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";` | Read data from Excel file | User credentials, file system access | None                 | Part 1                  |
| CCEM_SOURCE                   | Dynamics 365 CE/CRM   | Connection details managed at the *project* level | Source for Dynamics 365 data  | Dynamics 365 credentials | None                 | Part 1, 2, 4, 5                  |
| ODS_CCEM                      | OLE DB                 | Connection details managed at the *project* level; Server=\\[Server Name];Database=\\[Database Name];Integrated Security=SSPI; | Destination for transformed data | Credentials to OLE DB database; Integrated Security | None                 | Part 1, 2, 3, 4, 5                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| SEQC- LANDING_SP1-6_CCEM_CASE | Unknown | Parent: *Current Package*. Child: *SEQC- LANDIN_1-6_CCEM_CASE*. | Success of `SEQC_LANDING_SP1-2-activity` |  Need to ensure the path is valid and accessible during runtime. | Part 5 |
| SEQC-LANDING_SP1-1 | Unknown | Parent: *Current Package*. Child: *SEQC-LANDING-SP1-5-crisis* | Success of `SEQC-LANDING-SP1-5-crisis` | Need to ensure the path is valid and accessible during runtime. | Part 5 |
| SEQC-LANDING_SP1-3-activity | Unknown | Parent: *Current Package*. Child: *SEQC-LANDING-SP1-4-activity* | Success of `EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` | Need to ensure the path is valid and accessible during runtime. | Part 5 |
| SEQC-LANDING_SP1-4-activity | Unknown | Parent: *Current Package*. Child: *SEQC- LANDIN_1-6_CCEM_CASE* | Success of `EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` | Need to ensure the path is valid and accessible during runtime. | Part 5 |
| SEQC- LANDING-SP7 | Unknown | Parent: *Current Package*. Child: *SEQC-LANDING-SP7* | Success of `EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` | Need to ensure the path is valid and accessible during runtime. | Part 5 |

## 3. Package Flow Analysis

### Control Flow

1.  **Expression Task:** `EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`
    *   Expression: `1 == 1` (Always evaluates to true)
    *   Purpose: Placeholder or basic check.
2.  Based on the expression evaluation, one of the following sequence containers is executed:
    *   `SEQC_LANDING_SP1-2-activity`
    *   `SEQC-LANDING_SP1-3-activity`
    *   `SEQC-LANDING_SP1-4-activity`
    *   `SEQC-LANDING-SP7`
3.  **Sequence Container:** `SEQC- LANDIN_1-6_CCEM_CASE`
    *   Purpose: Groups Data Flow Tasks related to CCEM cases.
    *   Data Flow Tasks within the Sequence Container (executed sequentially):
        1.  DFT- L_campaign
        2.  DFT- L_ccem_abduction
        3.  DFT- L_ccem_accident
        4.  DFT- L_ccem_adoption
        5.  DFT- L_ccem_arrest_prison_visit
        6.  DFT- L_ccem_arrest_transfer
        7.  DFT- L_ccem_distress
        8.  DFT-L_ccem_fraud (Disabled)
4. **Data Flow Task:** `DFT-contact-old-nov17` (Disabled)
5. Sequence Containers:
    *   SEQC-LANDING-SP1-5-crisis
    *   SEQC-LANDING_SP1-1

### Data Flow Tasks

Each data flow task within sequence container follows a similar pattern:

1.  **Source:** Dynamics CRM Source component (e.g., `Dynamics CRM Source_ccem_abduction`, `Dynamics CRM Source_ccem_accident`, `CRM_SRC-ccem_*_activity`).
    *   Extracts data from a specific entity in Microsoft Dynamics 365 CE/CRM (e.g., `ccem_abduction`, `ccem_accident`, `ccem_crime_activity`).
    *   Uses the `CCEM_SOURCE` connection manager.
2.  **Transformation:** Derived Column (`DRV_TRSFM_etl_date`, `Derived Column`).
    * Creates new columns ETL_CREA_DT and ETL_UPDT_DT with value GETDATE().
3.  **Destination:** OLE DB Destination (e.g., `OLE DB_DEST_ODS_CCEM_ccem_abduction`, `OLE DB_DEST_ODS_CCEM_ccem_accident`, `OLEDB_DEST-ccem_*_activity`).
    *   Loads data into a table in an OLE DB destination (likely a SQL Server database).
    *   Uses the `ODS_CCEM` connection manager.
    *   The destination table name is specified in the `OpenRowset` property (e.g., `[ccem_abduction]`).

#### DFT- L_ccem_fund:

*   **Source:** Dynamics CRM Source (`Dynamics CRM Source_ccem_fund`) extracts data from the `ccem_fund` entity.  Retrieves a large number of columns.
*   **Transformation:** Derived Column (`Derived Column`) calculates `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
*   **Destination:** OLE DB Destination (`OLE DB_DEST_ODS_CCEM_ccem_fund`) loads data into the `ccem_fund` table in the ODS database.  Uses fast load options: `TABLOCK,CHECK_CONSTRAINTS`.
*   **Error Handling:** Error row disposition is set to "FailComponent".

#### DFT- ccem\_crisis, DFT-ccem\_departure, DFT-stringmap, DFT-account, DFT_organization:

*   **Source:** Dynamics CRM Source
*   **Destination:** OLE DB Destination (ODS_CCEM, table dbo.ccem\\_crisis, dbo.ccem\\_departure, dbo.stringmap, dbo.account, dbo.organization)
*   **Transformations:** Derived Column (ETL\\_CREA\\_DT, ETL\\_UPDT_DT)
*   **Data Movement:** Data from Dynamics CRM is extracted, two columns are derived , and then the data is loaded into the  tables in the ODS\\_CCEM database.
*   **Error Handling:**  Error row disposition is set to "FailComponent" for the OLE DB Destination. OLE DB Destination Error Output is used.

#### DFT-ccem\\_crime\\_activity, DFT-ccem\\_crisis\\_activity, DFT-ccem\\_custody\\_activity, DFT-ccem\\_death\\_activity, DFT-ccem\\_departure\\_activity, DFT-ccem\\_desertion\\_activity, DFT-ccem\\_distress\\_activity, DFT-ccem\\_fund\\_activity, DFT-ccem_medical_activity:

*   **Source:** A `CRM_SRC-ccem_*_activity` component extracts data from Dynamics CRM. The specific entity extracted depends on the Data Flow Task name.
*   **Transformation:** The data passes through a Derived Column transformation `DRVCOL_TRFM-etl_date` or `Derived Column` transformation. This transformation adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using the `GETDATE()` function.
*   **Destination:** The transformed data is loaded into an OLE DB destination table `OLEDB_DEST-ccem_*_activity` using the connection manager `ODS_CCEM`. The specific destination table depends on the Data Flow Task name.

### Precedence Constraints:

*   The Expression Task has a Success precedence constraint to the next task.
*   The data flow tasks within the sequence container WILL execute sequentially one after another, based on successful transfer.

## 4. Code Extraction

#### SQL Queries (within Variables)

##### V_SQL_INSERT_ON_PRE_EXECUTE

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
   AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\'
  )
 ,\'RUNNING\'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;
```

*   **Purpose:** Inserts a new record into the `ETL_RUN_STATUS` table to indicate that the package is starting to run.
*   **Parameterization:** Uses the project-level parameter `$Project::PRJ_PRM_ETL_COMPONENT_ID` to determine the ETL component ID.  Also pulls the ETL_SUB_COMPONENT_ID from the ETL_SUB_COMPONENT table.
*   **Dynamic SQL:** Yes, the SQL is constructed dynamically using the expression evaluator.

##### V_SQL_UPDATE_ON_ERROR

```sql
 UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = \'FAILED\'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 8
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\')
 AND ETL_RUN_STATUS_DESC = \'RUNNING\'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

*   **Purpose:** Updates the `ETL_RUN_STATUS` table to indicate that the package has failed.  It targets the most recent "RUNNING" status record for the current component.
*   **Parameterization:** Uses the project-level parameter `$Project::PRJ_PRM_ETL_COMPONENT_ID` to filter the update. Also pulls the ETL_SUB_COMPONENT_ID from the ETL_SUB_COMPONENT table.
*   **Dynamic SQL:** Yes, the SQL is constructed dynamically using the expression evaluator.

##### V_SQL_UPDATE_ON_POST_EXECUTE

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = \'SUCCEEDED\'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 8
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\')
 AND ETL_RUN_STATUS_DESC = \'RUNNING\'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

*   **Purpose:** Updates the `ETL_RUN_STATUS` table to indicate that the package has succeeded.  It targets the most recent "RUNNING" status record for the current component.
*   **Parameterization:** Uses the project-level parameter `$Project::PRJ_PRM_ETL_COMPONENT_ID` to filter the update.  Also pulls the ETL_SUB_COMPONENT_ID from the ETL_SUB_COMPONENT table.
*   **Dynamic SQL:** Yes, the SQL is constructed dynamically using the expression evaluator.

#### Expressions

##### User::V_ETL_COMPONENT_NAME

```
@[System::PackageName] + ".DTSX"
```

*  **Purpose:** creates the name of the dtsx package by taking system variable PackageName and concatenating ".DTSX"

#### ESQLT-Truncate\_Tables task SQL

```sql
truncate table  dbo.ccem_crisis_activity;
truncate table dbo.ccem_crisis;
truncate table dbo.ccem_departure_activity;
truncate table  dbo.ccem_departure;
truncate table   dbo.stringmap;
truncate table   dbo.account;
truncate table   dbo.organization;
truncate table  ccem_crime_activity;
truncate table  ccem_custody_activity;
truncate table  ccem_death_activity;
truncate table  ccem_desertion_activity;
truncate table  ccem_distress_activity;
truncate table  ccem_fund_activity;
truncate table  ccem_general_activity;
truncate table  ccem_lost_activity;
truncate table  ccem_marriage_activity;
truncate table  ccem_medical_activity;
truncate table  ccem_transfer_activity;
truncate table  ccem_welfare_activity;
truncate table  ccem_wellbeing_activity;
truncate table  ccem_abduction_activity;
truncate table  ccem_accident_activity;
truncate table  ccem_adoption_activity;
truncate table  ccem_arrest_activity;
truncate table  ccem_assault_activity;
```

#### Derived Column Expressions

```
GETDATE()
```

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.ccem_crisis |  | Part 3 |
| dbo.ccem_departure |  | Part 3 |
| dbo.stringmap |  | Part 3 |
| dbo.account |  | Part 3 |
| dbo.organization |  | Part 3 |
| dbo.ccem_crisis_activity |  | Part 3, 4 |
| dbo.ccem_departure_activity |  | Part 3, 4 |
| dbo.ccem_crime_activity |  | Part 4 |
| dbo.ccem_custody_activity |  | Part 4 |
| dbo.ccem_death_activity |  | Part 4 |
| dbo.ccem_desertion_activity |  | Part 4 |
| dbo.ccem_distress_activity |  | Part 4 |
| dbo.ccem_fund_activity |  | Part 4 |
| dbo.ccem_medical_activity |  | Part 4 |
| dbo.ccem_transfer_activity |  | Part 5 |
| dbo.ccem_welfare_activity |  | Part 5 |
| dbo.ccem_wellbeing_activity |  | Part 5 |
| dbo.ccem_abduction_activity |  | Part 5 |
| dbo.ccem_accident_activity |  | Part 5 |
| dbo.ccem_fund | Data is written | Part 2 |

## 6. Package Summary

*   **Input Connections:** 2
    *   Excel Connection Manager
    *   CCEM_SOURCE (Dynamics CRM)
*   **Output Destinations:** 1 (ODS_CCEM, OLE DB) and 19+ fact tables
*   **Package Dependencies:** 5
*   **Activities:**
    *   Data Flow Tasks: 18+
    *   Sequence Containers: 5
    *   Execute SQL Tasks: 3
    *   Expression Tasks: 3
    *   Derived Columns: 18+

*   **Transformations:** Derived Column (GETDATE())

*   **Script Tasks:** 0
*   **Overall Package Complexity Assessment:** Medium to high. The package consists of multiple sequence container with multiple data flow tasks. Each data flow task extracts data from Dynamics CRM and loads it into separate tables. The transformations are relatively simple. The number of tables being loaded into makes the package more complex.
*   **Potential Performance Bottlenecks:**
    *   **Dynamics CRM Source:**  Performance can be impacted by the volume of data being extracted from Dynamics CRM and the complexity of the FetchXML queries.
    *   **OLE DB Destination:**  Write performance to the destination database can be a bottleneck, especially under heavy load. Fast Load options (TABLOCK, CHECK_CONSTRAINTS) are used.
    *   **Sequential Execution:**  Running the Data Flow Tasks sequentially within the sequence container may limit overall throughput. Consider parallel execution if dependencies allow.
    *   **Full Table Truncation:** The `ESQLT-Truncate_Tables` task truncates the tables before each load. This can be inefficient for large tables. Consider using incremental loading strategies.
*   **Critical Path Analysis:** The critical path is the sequential execution of the data flow tasks within the sequence container.
*   **Error Handling Mechanisms:**
    *   Error row disposition is set to "FailComponent" for the data flow components.
    *   Event Handlers (OnError events) are used to record the status of ETL processes and provide error handling. User variables are used to store SQL queries that update the ETL_RUN_STATUS table.
    *   Row-level Error Handling: Implemented in the OLE DB Destinations. Rows that fail to load are directed to the error output.
```