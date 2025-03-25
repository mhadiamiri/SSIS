## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager | EXCEL | `Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\Documents\\Project\\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";` | Unused Connection Manager | File system access to the specified Excel file. Ensure the SSIS service account or the executing user has read access to the file and the directory. If the file contains sensitive data, appropriate access controls should be in place. The "HDR=YES" property in the connection string indicates that the first row contains headers, which could expose column names. This doesn't introduce a direct security risk, but it's good to be aware of the data's structure. | None | Part 1 |
| Project.ConnectionManagers[CCEM_SOURCE] | Dynamics CRM | N/A - Dynamics CRM connection details are managed within the Project Connection Manager. Details would include the CRM server URL, authentication type, username/password (if applicable), and organization. | Source to extract data from Microsoft Dynamics 365 CE/CRM. | Authentication credentials (username/password, OAuth, etc.). Securely store and manage these credentials within the SSIS project. Ensure the service account or executing user has the appropriate permissions within Dynamics CRM to access the specified entities. | @[$Project::PRJ_PRM_ETL_COMPONENT_ID] | Part 1, 2, 3, 4, 5 |
| Project.ConnectionManagers[ODS_CCEM] | OLE DB | N/A - OLE DB connection details are likely managed within the Project Connection Manager. Details would include the SQL Server instance, database name, authentication type, username/password (if applicable). | Destination to load data into a SQL Server database (likely the ODS layer). | SQL Server authentication credentials (username/password or integrated security) must be securely stored and managed. Ensure the service account or executing user has the appropriate permissions within SQL Server to write to the specified tables. Consider using SQL Server Agent proxy accounts to manage permissions. | @[$Project::PRJ_PRM_ETL_COMPONENT_ID] | Part 1, 2, 3, 4, 5 |
| {D8FDA38C-C16C-4DCA-8B17-3556DD7B8002} | OLE DB | Server = (From Project Connection Manager ODS_CCEM) | Destination for landing data from CRM | Credentials for accessing the database | None visible in this snippet | Part 3, 4, 5 |
| {2E0913B4-078C-4D1D-893E-D98B8C3F2656} | Dynamics CRM | Server = (From Project Connection Manager CCEM_SOURCE) | Source data from Dynamics CRM | Credentials for accessing CRM | None visible in this snippet | Part 3, 4, 5 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| DFT- ccem\_crisis | Package\SEQC-LANDING-SP1-5-crisis | Loads ccem\_crisis data from CRM to ODS | Succeeds ESQLT-Truncate\_Tables |  | Part 3 |
| DFT- ccem\_departure | Package\SEQC-LANDING-SP1-5-crisis | Loads ccem\_departure data from CRM to ODS | Succeeds DFT- ccem_crisis |  | Part 3 |
| DFT- stringmap | Package\SEQC-LANDING-SP1-5-crisis | Loads stringmap data from CRM to ODS | Succeeds DFT- ccem_departure |  | Part 3 |
| DFT-account | Package\SEQC-LANDING-SP1-5-crisis | Loads account data from CRM to ODS | Succeeds DFT- stringmap |  | Part 3 |
| DFT\_organization | Package\SEQC-LANDING-SP1-5-crisis | Loads organization data from CRM to ODS | Succeeds DFT-account |  | Part 3 |
| DFT-ccem\_sla_setting | Package\SEQC-LANDING-SP7 | Loads ccem_sla_setting data from CRM to ODS | Succeeds DFT_ccem_sla |  | Part 3 |
| DFT_ccem_sla | Package\SEQC-LANDING-SP7 | Loads ccem_sla data from CRM to ODS | Succeeds ESQLT- Truncate Landing_Tables |  | Part 3 |
| DFT- L_ccem_region_country | Package\SEQC-LANDING_SP1-1 | Loads ccem_region_country data from CRM to ODS | Succeeds DFT-ccem_tripdestination |  | Part 3 |
| DFT-ccem_case_contacts | Package\SEQC-LANDING_SP1-1 | Loads ccem_case_contact data from CRM to ODS | Succeeds DFT-ccem_country |  | Part 3 |
| DFT-ccem_country | Package\SEQC-LANDING_SP1-1 | Loads ccem_country data from CRM to ODS | Succeeds DFT-ccem_case_contacts |  | Part 3 |
| DFT-ccem_trip | Package\SEQC-LANDING_SP1-1 | Loads ccem_trip data from CRM to ODS | Succeeds DFT-ccem_region |  | Part 3 |
| DFT-ccem_tripdestination | Package\SEQC-LANDING_SP1-1 | Loads ccem_tripdestination data from CRM to ODS | Succeeds DFT-ccem_trip |  | Part 3 |

## 3. Package Flow Analysis

*   **EXPRESSIONT- Landing - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode:**  This is an Expression Task. Its expression is `1 == 1`, which always evaluates to true. This task likely serves as a starting point or a placeholder. (Part 1)
*   **SEQC- LANDIN_1-6_CCEM_CASE:** This is a Sequence Container. It contains multiple Data Flow Tasks that extract and load data. (Part 1)
    *   **DFT- L\_campaign:** Extracts data from Dynamics CRM (campaign entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_abduction:** Extracts data from Dynamics CRM (ccem_abduction entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_accident:** Extracts data from Dynamics CRM (ccem_accident entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_adoption:** Extracts data from Dynamics CRM (ccem_adoption entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_arrest:** Extracts data from Dynamics CRM (ccem_arrest entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_arrest\_prison\_visit:** Extracts data from Dynamics CRM (ccem_prisonvisit entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_arrest\_transfer:** Extracts data from Dynamics CRM (ccem_arrest_transfer entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_assault:** Extracts data from Dynamics CRM (ccem_assault entity), adds audit columns, and loads it to ODS. This task is disabled.
    *   **DFT- L\_ccem\_crime:** Extracts data from Dynamics CRM (ccem_crime entity), adds audit columns, and loads it to ODS. This task is disabled.
    *   **DFT- L\_ccem\_custody:** Extracts data from Dynamics CRM (ccem_custody entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_desertion:** Extracts data from Dynamics CRM (ccem_desertion entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_distress:** Extracts data from Dynamics CRM (ccem_distress entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_evacuation:** Extracts data from Dynamics CRM (ccem_evacuation entity), adds audit columns, and loads it to ODS.
    *   **DFT- L\_ccem\_fraud:** Extracts data from Dynamics CRM (ccem_fraud entity), adds audit columns, and loads it to ODS. This task is disabled.
    *   **DFT- L\_ccem\_homicide:** Extracts data from Dynamics CRM (ccem_homicide entity), adds audit columns, and loads it to ODS.  This task is disabled.
*   **ESQLT- Truncate Landing_1** (Execute SQL Task) likely truncates tables before the data flows are executed. (Part 2)

#### DFT- L\_campaign

*   **Source:** Dynamics CRM Source\_campaign (extracts from the *campaign* entity using the CCEM\_SOURCE connection manager).
*   **Transformation:** Derived Column (adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns using the `GETDATE()` function).
*   **Destination:** OLE DB\_DEST\_ODS\_campaign (loads data into the *campaign* table in the ODS schema using the ODS\_CCEM connection manager).
*   **Error Handling:**  The OLE DB destination has an "OLE DB Destination Error Output" for handling errors during the load process. By default, it is configured to `FailComponent`. (Part 2)

#### DFT_organization

*   **Source:** `Dynamics CRM Source` (likely extracting from the `organization` entity).
*   **Transformation:** `Derived Column` (creates `etl_crea_dt` and `etl_updt_dt` columns, which are timestamps).
*   **Destination:** `OLE DB Destination` (loads data into the `organization` table in the ODS database).
*   **Error Handling:** The OLE DB Destination has an error output configured, allowing for rows that fail the destination insert to be redirected.

#### DFT-ccem\_welfare\_activity

*   **Source:** A Dynamics CRM Source component (`CRM_SRC-ccem_welfare_activity`) extracts data from the `ccem_welfare_activity` entity in Dynamics CRM.
*   **Transformation:** A Derived Column transformation (`DRVCOL_TRFM-etl_date`) adds two new columns: `etl_crea_dt` and `etl_updt_dt`. Both columns are populated with the current date and time using the `GETDATE()` function.
*   **Destination:** An OLE DB Destination component (`OLEDB_DEST-ccem_welfare_activity`) loads the transformed data into the `dbo.ccem_welfare_activity` table in SQL Server. Fast load options include `TABLOCK` and `CHECK_CONSTRAINTS`. `FastLoadKeepIdentity` and `FastLoadKeepNulls` are set to `false`.
*   **Error Handling:**  Error handling is set to `FailComponent`, meaning any errors during data extraction will cause the task to fail. (Part 5)

## 4. Code Extraction

```sql
-- SQL Queries (extracted from Variables):

-- Variable: V_SQL_INSERT_ON_PRE_EXECUTE
-- Purpose: To insert a record into the ETL_RUN_STATUS table before the package executes.
INSERT INTO [ETL_RUN_STATUS] (
	[ETL_COMPONENT_ID]
	,[ETL_SUB_COMPONENT_ID]
	,[ETL_RUN_STATUS_DESC]
	,[ETL_RUN_MAIN_COMPONENT_IND]
	,[ETL_RUN_RECORD_CREA_DT]
	,[ETL_RUN_RECORD_UPDT_DT]
)
VALUES (
	<Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
	,(\
		SELECT ETL_SUB_COMPONENT_ID
		FROM ETL_SUB_COMPONENT
		WHERE ETL_COMPONENT_ID = <Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
			AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\'
		)
	,\'RUNNING\'
	,0
	,GETDATE()
	,GETDATE()
)
;

-- Variable: V_SQL_UPDATE_ON_ERROR
-- Purpose: To update the ETL_RUN_STATUS table to mark the component as \'FAILED\' in case of an error.
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = \'FAILED\'
	,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE ETL_RUN_STATUS.ETL_RUN_STATUS_ID in (
		select max(e.ETL_RUN_STATUS_ID)
		from ETL_RUN_STATUS e
		where e.ETL_COMPONENT_ID = <Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
			and e.ETL_SUB_COMPONENT_ID =(\
				SELECT ETL_SUB_COMPONENT_ID
				FROM ETL_SUB_COMPONENT
				WHERE ETL_COMPONENT_ID = <Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
					AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\'
				)
		AND ETL_RUN_STATUS_DESC = \'RUNNING\'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0
		)
;

-- Variable: V_SQL_UPDATE_ON_POST_EXECUTE
-- Purpose: To update the ETL_RUN_STATUS table to mark the component as \'SUCCEEDED\' after successful execution.
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = \'SUCCEEDED\'
	,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE ETL_RUN_STATUS.ETL_RUN_STATUS_ID in (
		select max(e.ETL_RUN_STATUS_ID)
		from ETL_RUN_STATUS e
		where e.ETL_COMPONENT_ID = <Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
			and e.ETL_SUB_COMPONENT_ID =(\
				SELECT ETL_SUB_COMPONENT_ID
				FROM ETL_SUB_COMPONENT
				WHERE ETL_COMPONENT_ID = <Project Parameter: PRJ_PRM_ETL_COMPONENT_ID>
					AND ETL_SUB_COMPONENT_NM = \'CCEM_Landing.dtsx\'
				)
		AND ETL_RUN_STATUS_DESC = \'RUNNING\'
		AND ETL_RUN_MAIN_COMPONENT_IND = 0
		)
;
```

```csharp
// Code Extraction: Derived Column Transformation Expressions (example)

//DFT- L_campaign
// Column: ETL_CREA_DT
// Expression: GETDATE()

// Column: ETL_UPDT_DT
// Expression: GETDATE()
```

```sql
-- SQL Query from ESQLT- Truncate Landing_1
TRUNCATE TABLE dbo.systemuser;
TRUNCATE TABLE dbo.ccem_case;
TRUNCATE TABLE dbo.ccem_mission;
TRUNCATE TABLE dbo.campaign;
TRUNCATE TABLE dbo.ccem_abduction;
TRUNCATE TABLE dbo.ccem_accident;
TRUNCATE TABLE dbo.ccem_adoption;
TRUNCATE TABLE dbo.ccem_arrest;
TRUNCATE TABLE dbo.ccem_assault;
TRUNCATE TABLE dbo.ccem_crime;
TRUNCATE TABLE dbo.ccem_custody;
TRUNCATE TABLE dbo.ccem_death;
TRUNCATE TABLE dbo.ccem_desertion;
TRUNCATE TABLE dbo.ccem_distress;
TRUNCATE TABLE dbo.ccem_fund;
TRUNCATE TABLE dbo.ccem_general;
TRUNCATE TABLE dbo.ccem_lost;
TRUNCATE TABLE dbo.ccem_marriage;
TRUNCATE TABLE dbo.ccem_medical;
TRUNCATE TABLE dbo.ccem_transfer;
TRUNCATE TABLE dbo.ccem_welfare;
TRUNCATE TABLE dbo.ccem_wellbeing;
TRUNCATE TABLE dbo.ccem_arrest_transfer;
TRUNCATE TABLE dbo.ccem_prisonvisit;
```

```dts
-- Expression from Derived Column Transformations in each DFT
[GETDATE]()
```

```sql
-- SQL used in ESQLT-Truncate_Tables task
truncate table  ccem_crime_activity;
truncate table  ccem_crisis_activity;
truncate table  ccem_custody_activity;
truncate table  ccem_death_activity;
truncate table  ccem_departure_activity;
truncate table  ccem_desertion_activity;
truncate table  ccem_distress_activity;
truncate table  ccem_fund_activity;
```

```sql
truncate table  ccem_general_activity;
truncate table  ccem_lost_activity;
truncate table  ccem_marriage_activity;
truncate table  ccem_medical_activity;
truncate table  ccem_transfer_activity;
truncate table  ccem_welfare_activity;
truncate table  ccem_wellbeing_activity;
```

```sql
truncate table  ccem_abduction_activity;
truncate table  ccem_accident_activity;
truncate table  ccem_adoption_activity;
truncate table  ccem_arrest_activity;
truncate table  ccem_assault_activity;
```

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| campaign | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_abduction | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_accident | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_adoption | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_arrest | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_prisonvisit | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_arrest_transfer | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_assault | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_crime | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_custody | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_desertion | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_distress | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_evacuation | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_fraud | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_homicide | Target tables are named after the CRM entity | Part 1, 2 |
| ccem_crisis_activity |  | Part 4 |
| ccem_departure_activity |  | Part 4 |
| ccem_desertion_activity |  | Part 4 |
| ccem_distress_activity |  | Part 4 |
| ccem_fund_activity |  | Part 4 |
| ccem_general_activity |  | Part 4 |
| ccem_lost_activity |  | Part 4 |
| ccem_marriage_activity |  | Part 4 |
| ccem_medical_activity |  | Part 4 |
| ccem_transfer_activity |  | Part 4 |
| ccem_welfare_activity |  | Part 4 |
| ccem_wellbeing_activity |  | Part 4 |
| account | | Part 3 |
| organization | | Part 3 |
| systemuser | | Part 2 |
| contact | | Part 3 |
| ccem_case_contact |  | Part 3 |
| ccem_country | | Part 3 |
| ccem_region | | Part 3 |
| ccem_trip | | Part 3 |
| ccem_tripdestination |  | Part 3 |
| ccem_region_country |  | Part 3 |
| stringmap | | Part 3 |
| ccem_sla | | Part 3 |
| ccem_sla_settings |  | Part 3 |

## 6. Package Summary

*   **Input Connections:** 2 (1 Excel, 1 Dynamics CRM) or 1 (Dynamics CRM)
*   **Output Destinations:** 16 (OLE DB Destinations - SQL Server) or Multiple OLE DB Destinations
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 1
    *   Sequence Containers: 1 or 2 or 3
    *   Data Flow Tasks: 16 or 13 or 11 or 7
    *   Execute SQL Task: 1 or 3
*   **Transformations:**
    *   Derived Column: 16 or one in each DFT
*   **Script Tasks:** 0
*   **Overall Package Complexity:** Medium.
*   **Potential Performance Bottlenecks:**
    *   **Dynamics CRM Source:** Retrieving large amounts of data from Dynamics CRM can be a bottleneck.
    *   **Sequential Execution:** The Data Flow Tasks within the Sequence Container execute sequentially.
    *   **Data Volume:** depends on the data volume in the source Dynamics CRM entities.
    *   **Network Latency:**  Communication latency between the SSIS server and the Dynamics CRM and SQL Server instances.
    *   **Lack of Incremental Load:** The truncate and load approach could be inefficient for large tables, suggesting a lack of incremental load strategy.
*   **Critical Path Analysis:** The critical path is the sequence of Data Flow Tasks within the Sequence Container, as these are the core data movement activities.
*   **Error Handling:** The error handling is basic, with "FailComponent" set on the main data flow components (Source, Derived Column, and Destination).
