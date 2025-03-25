## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---|---|---|---|---|---|---|
| Excel Connection Manager | EXCEL | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\Users\admLIUJ6\Documents\Project\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES"; | Source for Data Flow Task  | File System Permissions | None | Part 1 |
| ODS_CCEM | OLE DB | Server: [Inferred], Database: [Inferred] | Destination for Data Flow Tasks | SQL Server Auth likely | None | Part 1, 2 |
| CCEM_SOURCE | Dynamics CRM | details not extracted | Source for Data Flow Tasks | CRM Authentication | None | Part 1, 2|

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|---|---|---|---|---|---|
| None Found | | | | No dependent SSIS packages tasks found | Part 1, 2 |

## 3. Package Flow Analysis

- The package starts with an Expression Task: EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode
-  Next a Sequence Container called SEQC_1 is executed.
- Inside the Sequence Container are several data flow tasks and an Execute SQL Task, which are executed sequentially:
    - DFT- CCEM_EMRGNCY_ASSISTANCEREQUEST
    - DFT-CCEM_EMRGNCY_CRISIS
    - DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON
    - DFT-CCEM_EMRGNCY_CRISIS_CONTACT
    - DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_STATISTICS
    - DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_SUBDIVISION_STATISTICS
    - ESQLT-Truncate_Tables
- The package also includes OnError and OnPostExecute event handlers which contain Execute SQL Tasks that update ETL process status.

#### DFT- CCEM_EMRGNCY_ASSISTANCEREQUEST
*   **Source:** Dynamics CRM Source (ccem_assistancerequest)
*   **Transformations:**
    * DRVCOL_TRFM-etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
    * OLE DB DEST CCEM_EMRGNCY_ASSISTANCEREQUEST: inserts data into `[dbo].[CCEM_EMRGNCY_ASSISTANCEREQUEST]`

#### DFT-CCEM_EMRGNCY_CRISIS
*   **Source:** CRM_SRC-ccem_crisis (ccem_crisis)
*   **Transformations:**
        * DRVCOL_TRFM-etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
    * OLEDB_DEST-ccem_emrgncy_crisis: inserts data into `[dbo].[ccem_emrgncy_crisis]`

#### DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON

*   **Source:** CRM_SRC-ccem_affectedperson (ccem_affectedperson)

*   **Transformations:**
        * DRVCOL_TRFM-etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
    * OLEDB_DEST-ccem_emrgncy_crisis_affectedperson: inserts data into `[dbo].[ccem_emrgncy_crisis_affectedperson]`

#### DFT-CCEM_EMRGNCY_CRISIS_CONTACT

*   **Source:** CRM_SRC-contact (contact)

*   **Transformations:**
        * DRVCOL_TRFM-etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
    * OLEDB_DEST-ccem_emrgncy_crisis_contact: inserts data into `[dbo].[ccem_emrgncy_crisis_contact]`

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_STATISTICS

*   **Source:** CRM SRC-ccem_countryStatistics(ccem_countryStatistics)

*   **Transformations:**
            * DRVCOL_TRFM-etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
        * OLEDB_Dest-CCEM_EMRGNCY_CRISIS_COUNTRY_STATISTICS: inserts data into `[dbo].[ccem_emrgncy_crisis_countrystatistics]`

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_SUBDIVISION_STATISTICS
*   **Source:** CRM SRC-ccem_subdivisionStatistics (ccem_subdivisionStatistics)
*   **Transformations:**
            * DRV_TRSFM_etl_date: sets etl_crea_dt and etl_updt_dt to GETDATE().
*   **Destinations:**
        * OLEDB_Dest-CCEM_EMRGNCY_CRISIS_COUNTRY_SUBDIVISION_STATISTICS: inserts data into `[dbo].[ccem_emrgncy_crisis_countrysubdivisionstatistics]`

## 4. Code Extraction

```sql
TRUNCATE TABLE ccem_emrgncy_crisis;
TRUNCATE TABLE ccem_emrgncy_crisis_affectedperson;
TRUNCATE TABLE ccem_emrgncy_crisis_contact;
truncate table ccem_emrgncy_crisis_countrystatistics;
truncate table ccem_emrgncy_crisis_countrysubdivisionstatistics;
TRUNCATE TABLE CCEM_EMRGNCY_ASSISTANCEREQUEST;
```

Context: SQL statements used to truncate tables in ESQLT-Truncate_Tables task.

```sql

 UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 0
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =0
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_HOURLY_REFRESH.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;

```

Context: SQL query used to set the ETL status to failed in ESQLT- Update ETL Process Status to Failed

```sql

UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where e.ETL_COMPONENT_ID = 0
and e.ETL_SUB_COMPONENT_ID =( SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =0
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_HOURLY_REFRESH.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;

```

Context: SQL query used to set the ETL status to succeeded ESQLT- Update ETL Process Status to Succeeded

```sql
 INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )
VALUES (0
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =0
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_HOURLY_REFRESH.dtsx'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;

```

Context: SQL query used to set the ETL status to Running in ESQLT- Create Record with Running Status

## 5. Output Analysis

| Destination Table | Description | Source Part |
|---|---|---|
| `[dbo].[CCEM_EMRGNCY_ASSISTANCEREQUEST]` | Stores assistance request data | Part 3 |
| `[dbo].[ccem_emrgncy_crisis]` | Stores crisis data | Part 3 |
| `[dbo].[ccem_emrgncy_crisis_affectedperson]` | Stores affected person data | Part 3 |
| `[dbo].[ccem_emrgncy_crisis_contact]` | Stores contact data | Part 3 |
| `[dbo].[ccem_emrgncy_crisis_countrystatistics]` | Stores country statistics data | Part 3 |
| `[dbo].[ccem_emrgncy_crisis_countrysubdivisionstatistics]` | Stores country subdivision statistics data | Part 3 |
| ETL_RUN_STATUS | table used to track the ETL status | Part 3 |

## 6. Package Summary

*   **Input Connections:** 3
*   **Output Destinations:** 6 fact tables + ETL_RUN_STATUS
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 6
    *   Execute SQL Tasks: 3
    *   Expression Task: 2
    *   Derived Column: 7
* Overall package complexity assessment: Medium
* Potential performance bottlenecks: The package truncates all tables at the beginning of the load sequence.
* Critical path analysis: All Data Flow Tasks and the Execute SQL Task within SEQC_1 are executed sequentially, representing the critical path.
* Document error handling mechanisms: The package has an OnError event handler that updates the ETL status to failed.
