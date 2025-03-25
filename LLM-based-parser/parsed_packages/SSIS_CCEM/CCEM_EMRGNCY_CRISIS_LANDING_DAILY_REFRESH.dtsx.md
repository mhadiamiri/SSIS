```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                                                                           | Purpose within Package                                                                                                                                   | Security Requirements                                 | Parameters/Variables                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Source Part |
|---------------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Excel Connection Manager  | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\Users\admLIUJ6\Documents\Project\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES"; | Not Directly Used within Package, but referenced in Connection Manager definition. Potentially for future use or external configuration. | File System Permissions to access the Excel file. | None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Part 1, 2, 3|
| CCEM_SOURCE| DynamicsCRM| To extract data from Dynamics 365 CE/CRM.| Source for ccem_emrgncy_crisis_country, ccem_country_risk, ccem_enquirer.| Dynamics CRM Connection Manager, Impersonation Caller.| None| Part 3 |
| ODS_CCEM| OleDbConnection| To access the database.| Destination for ccem_emrgncy_crisis_country, ccem_emrgncy_crisis_country_risk, ccem_emrgncy_crisis_enquirer.| The OLE DB runtime connection.| None| Part 3 |

## 2. Package Dependencies

| Dependent Package Name                        | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Source Part |
|---------------------------------------------|-------------------|-------------------------|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| CCEM_EMRGNCY_CRISIS_LANDING_HOURLY_REFRESH.dtsx |                     | Child                    | None                              | The "CALL HOURLY REFRESH PACKAGE" Execute Package Task executes this package. This means that the daily refresh calls the hourly refresh. This is a parent child relationship. The FailPackageOnFailure and FailParentOnFailure properties are set to true, so the package will fail if the child package fails.                                                                                                                                                        | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package begins with an `Expression Task` which is always set to true.
*   A `Sequence Container` contains data flow tasks and Execute SQL tasks that are only run once a day.
    *   The sequence container begins with a SQL task to truncate several tables.
    *   Three Data Flow Tasks (DFTs) then extract and load data.
        *   `DFT-CCEM_EMRGNCY_CRISIS_COUNTRY` extracts data from Dynamics CRM, adds audit columns and loads it into a SQL Server table.
        *   `DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_RISK` extracts data from Dynamics CRM, adds audit columns and loads it into a SQL Server table.
        *   `DFT-CCEM_EMRGNCY_CRISIS_ENQUIRER` extracts data from Dynamics CRM, adds audit columns and loads it into a SQL Server table.
*   Finally, another `Execute Package Task` is run to call the hourly refresh package.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY
*   **Source:** CRM SRC-CCEM_COUNTRY extracts data from the `ccem_country` entity in Dynamics CRM using the CCEM_SOURCE connection.
*   **Transformations:**
    *   `DRV_TRSFM_etl_date`: adds `etl_crea_dt` and `etl_updt_dt` using the GETDATE() function.
*   **Destination:**
    *   `OLEDB_Dest-ccem_emrgncy_crisis_country` loads data into the `ccem_emrgncy_crisis_country` table in the ODS_CCEM database.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_RISK
*   **Source:** CRM SRC-CCEM_COUNTRY_RISK extracts data from the `ccem_country_risk` entity in Dynamics CRM using the CCEM_SOURCE connection.
*   **Transformations:**
    *   `DRV_TRSFM_etl_date`: adds `etl_crea_dt` and `etl_updt_dt` using the GETDATE() function.
*   **Destination:**
    *   `OLEDB_Dest-ccem_emrgncy_crisis_country` loads data into the `ccem_emrgncy_crisis_country_risk` table in the ODS_CCEM database.

#### DFT-CCEM_EMRGNCY_CRISIS_ENQUIRER
*   **Source:** OLESRC-CRM-ccem_enquirer extracts data from the `ccem_enquirer` entity in Dynamics CRM using the CCEM_SOURCE connection.
*   **Transformations:**
    *   `DRV_TRSFM_etl_date`: adds `etl_crea_dt` and `etl_updt_dt` using the GETDATE() function.
*   **Destination:**
    *   OLEDB_DEST-CCEM_EMRGNCY_CRISIS_ENQUIRER loads data into the `ccem_emrgncy_crisis_enquirer` table in the ODS_CCEM database.

## 4. Code Extraction

```markdown
-- From User::Variable
 INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )

VALUES (  (SELECT ETL_COMPONENT_ID FROM ETL_COMPONENT WHERE UPPER(ETL_COMPONENT_DESC) = 'REPONSIBLE FOR POPULATING ODS_CCEM, CCEM_STAGING AND MART_CCEM IN THE DW' and ETL_COMPONENT_NM = 'CCEM_MASTER.DTSX'
 ) ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID =8
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_DAILY_REFRESH.dtsx'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;
```

Context: This SQL query is used to insert a new record into the `ETL_RUN_STATUS` table with a status of 'RUNNING'.

```markdown
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_DAILY_REFRESH.dtsx'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;
```

Context: This SQL query is used to insert a new record into the `ETL_RUN_STATUS` table with a status of 'RUNNING' before the package executes.

```markdown
-- From User::V_SQL_UPDATE_ON_ERROR
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_DAILY_REFRESH.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the `ETL_RUN_STATUS` table to 'FAILED' if an error occurs during package execution.

```markdown
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_LANDING_DAILY_REFRESH.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL query is used to update the `ETL_RUN_STATUS` table to 'SUCCEEDED' after the package executes successfully.

```markdown
-- From SQC-02 - THESE DFTS ARE ARE ONLY REQUIRED TO REFRESH DAILY\ESQLT-Truncate_Tables
TRUNCATE TABLE ccem_emrgncy_crisis_contact;
truncate table ccem_emrgncy_crisis_countrystatistics;
truncate table ccem_emrgncy_crisis_countrysubdivisionstatistics;
TRUNCATE TABLE ccem_emrgncy_crisis_affectedperson;
TRUNCATE TABLE ccem_emrgncy_crisis;
TRUNCATE TABLE ccem_emrgncy_crisis_enquirer;
TRUNCATE TABLE ccem_emrgncy_crisis_country;
TRUNCATE TABLE ccem_emrgncy_crisis_country_risk;
```

Context:  This SQL query is used to truncate several tables in the ODS_CCEM database.

## 5. Output Analysis

| Destination Table                       | Description                                                                                       | Source Part |
|---------------------------------------|---------------------------------------------------------------------------------------------------|-------------|
| dbo.ccem_emrgncy_crisis_country           | Stores data from the Dynamics CRM ccem_country entity.                                                 | Part 3      |
| dbo.ccem_emrgncy_crisis_country_risk        | Stores data from the Dynamics CRM ccem_country_risk entity.                                              | Part 3      |
| dbo.ccem_emrgncy_crisis_enquirer        | Stores data from the Dynamics CRM ccem_enquirer entity.                                                  | Part 3      |
| ETL_RUN_STATUS                        | Stores the status of the ETL process (Running, Succeeded, Failed). Updated at Pre and Post Execute. | Part 3      |

## 6. Package Summary

*   **Input Connections:** 2 (Dynamics CRM,  ODS_CCEM) + Excel connection manager
*   **Output Destinations:** 3 SQL Server tables in `ODS_CCEM` + `ETL_RUN_STATUS` table updates.
*   **Package Dependencies:** 1 (CCEM_EMRGNCY_CRISIS_LANDING_HOURLY_REFRESH.dtsx)
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 3
    *   Execute SQL Tasks: 2 + 3 in event handlers.
    *   Expression Tasks: 1 + 4 in Event Handlers.
    *   Derived Column: 3
    *   Execute Package Task: 1
*   **Transformations:**
    *   Derived Column Transformation: 3.
*   **Script tasks:** 0
*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: Data retrieval from Dynamics CRM can be a bottleneck if the dataset is large.
*   Critical path analysis: Data retrieval from Dynamics CRM to staging to target.
*   Error handling mechanisms:  The package uses `OnError` event handlers to update the `ETL_RUN_STATUS` table to 'FAILED'. The package is configured to fail if any of the Data Flow Tasks do, which would then trigger the event handler.
```