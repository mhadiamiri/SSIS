```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager  | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\Documents\\Project\\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES"; | Potential lookup, but not used in Data Flow Tasks | Access to specified file location | None apparent           | Part 1        |
| CCEM_SOURCE  | DynamicsCRM     | Server, Organization Name, Authentication Type (Inferred) | Source for data extraction in Data Flow Tasks             | Requires appropriate CRM credentials and permissions            | N/A                  | Part 1, 2, 3, 4                 |
| ODS_CCEM     | OLEDB           | Server, Database name, Authentication Type (Inferred) | Destination for data loading and ETL status updates             | Requires appropriate database credentials and permissions            | N/A                      | Part 1, 2, 3, 4             |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

- The package contains a main sequence container (implicit).
- The package uses several Data Flow Tasks (DFTs) to extract data from Dynamics CRM, transform it, and load it into SQL Server tables.

#### DFT-CCEM_EMRGNCY_CRISIS

*   **Source:** CRM_SRC-ccem_crisis (Dynamics 365 CE/CRM Source) extracts data from the `ccem_crisis` entity.
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_ACCOUNT

*   **Source:** CRM SRC_account (Dynamics 365 CE/CRM Source) extracts data from the `account` entity.
*   **Transformation:** `DRV_TRSFM_etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_Dest-ccem_emrgncy_crisis_account` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis_account]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_ACCOUNT 1 (Disabled)

*   **Source:** CRM SRC_account (Dynamics 365 CE/CRM Source) extracts data from the `account` entity.
*   **Transformation:** `DRV_TRSFM_etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_Dest-XXXccem_emrgncy_crisis_account` (OLE DB Destination) loads data into the `[dbo].[xccem_emrgncy_crisis_account]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON

*   **Source:** CRM_SRC-ccem_affectedperson (Dynamics 365 CE/CRM Source) extracts data from the `ccem_affectedperson` entity.
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis_affectedperson` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis_affectedperson]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON_CLIENTNEEDS

*   **Source:** CRM_SRC-ccem_affectedperson_clientneeds (Dynamics 365 CE/CRM Source) extracts data from the `ccem_affectedperson_clientneeds` entity.
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column): Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis_affectedperson_clientneeds` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis_affectedperson_clientneeds]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_AFFECTEDPERSON_SERVICESPROVIDED

*   **Source:** CRM_SRC-ccem_affectedperson_servicesprovid (Dynamics 365 CE/CRM Source) extracts data from the `ccem_affectedperson_servicesprovid` entity.
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis_affectedperson_servicesprovided` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis_affectedperson_servicesprovided]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_CLIENT_NEEDS

*   **Source:** CRM SRC-clientNeeds (Dynamics 365 CE/CRM Source) extracts data from the `ccem_clientneeds` entity.
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis_client_needs` (OLE DB Destination) loads data into the `[dbo].[ccem_emrgncy_crisis_client_needs]` table.
*   **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_CONTACT

*   **Source:** `CRM SRC-CCEM_COUNTRY` and `CRM_SRC-contact`
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column): Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time (GETDATE()).
*   **Destination:** `OLEDB_DEST-ccem_emrgncy_crisis_contact` and `OLEDB_DEST-ccem_emrgncy_crisis_contact2` loads data into the `[dbo].[ccem_emrgncy_crisis_contact]` table and `[dbo].[ccem_emrgncy_crisis_contact2]`.
* **Error Handling:** Fail component for errors.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY

1.  **Source:** `CRM SRC-CCEM_COUNTRY` - Extracts data from the `ccem_country` entity in Dynamics CRM.
2.  **Transformation:** `DRV_TRSFM_etl_date` - A Derived Column transformation that adds two new columns:`etl_crea_dt` and `etl_updt_dt`, both populated with the current date and time using `GETDATE()`.
3.  **Destination:** `OLEDB_Dest-ccem_emrgncy_crisis_country` - Loads the transformed data into the `ccem_emrgncy_crisis_country` table in a SQL Server database.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_RISK

1.  **Source:** `CRM SRC-CCEM_COUNTRY_RISK` - Extracts data from the `ccem_country_risk` entity in Dynamics CRM.
2.  **Transformation:** `DRV_TRSFM_etl_date` - A Derived Column transformation that adds two new columns:`etl_crea_dt` and `etl_updt_dt`, both populated with the current date and time using `GETDATE()`.
3.  **Destination:** `OLEDB_Dest-ccem_emrgncy_crisis_country` - Loads the transformed data into the `ccem_emrgncy_crisis_country_risk` table in a SQL Server database.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_STATISTICS

1.  **Source:** `CRM SRC-ccem_countryStatistics` - Extracts data from the `ccem_countrystatistics` entity in Dynamics CRM.
2.  **Transformation:** `DRV_TRSFM_etl_date` - A Derived Column transformation that adds two new columns:`etl_crea_dt` and `etl_updt_dt`, both populated with the current date and time using `GETDATE()`.
3.  **Destination:** `OLEDB_Dest-CCEM_EMRGNCY_CRISIS_COUNTRY_STATISTICS` - Loads the transformed data into the `ccem_emrgncy_crisis_countrystatistics` table in a SQL Server database.

#### DFT-CCEM_EMRGNCY_CRISIS_COUNTRY_SUBDIVISION_STATISTICS

1.  **Source:** `CRM SRC-ccem_subdivisionStatistics` - Extracts data from the `ccem_countrysubdivisionstatistics` entity in Dynamics CRM.
2.  **Transformation:** `DRV_TRSFM_etl_date` - A Derived Column transformation that adds two new columns:`etl_crea_dt` and `etl_updt_dt`, both populated with the current date and time using `GETDATE()`.
3.  **Destination:** `OLEDB_Dest-CCEM_EMRGNCY_CRISIS_COUNTRY_SUBDIVISION_STATISTICS` - Loads the transformed data into the `ccem_emrgncy_crisis_countrysubdivisionstatistics` table in a SQL Server database.

#### DFT-CCEM_EMRGNCY_CRISIS_DEPARTURE, DFT-CCEM_EMRGNCY_CRISIS_ENQUIRER, DFT-CCEM_EMRGNCY_CRISIS_LOCATION, DFT-CCEM_EMRGNCY_CRISIS_LOCATION_TRIP, DFT-CCEM_EMRGNCY_CRISIS_SERVICE_PROVIDED

*   **Source:**  CRM Source component (KingswaySoft) extracts data from Dynamics 365 CE/CRM entities: `ccem_departure`, `ccem_enquirer`, `ccem_crisisLocation`, `ccem_crisislocation_trip`, and `ccem_servicesProvided`.
*   **Transformation:** A "Derived Column" transformation (`DRVCOL_TRFM-etl_date`) creates new columns `etl_crea_dt` (ETL creation date) and `etl_updt_dt` (ETL update data). The expression used is `GETDATE()`.
*   **Destination:** The destination is an "OLE DB Destination" component. This component loads the transformed data into SQL Server tables in the `ODS_CCEM` database. The destination tables are named according to the source entity (e.g., `ccem_emrgncy_crisis_departure`, `ccem_emrgncy_crisis_enquirer`, `ccem_emrgncy_crisis_location`, `ccem_emrgncy_crisis_location_trip`, `ccem_emrgncy_crisis_service_provided`).
*   **Error Handling:** Each OLE DB Destination has an "OLE DB Destination Error Output." This allows rows that fail to insert to be redirected for error handling and logging.

## 4. Code Extraction

```sql
-- SQL Queries (Embedded in Variables)
-- Variable: User::V_SQL_INSERT_ON_PRE_EXECUTE
-- Purpose: Insert a "running" status record into the ETL_RUN_STATUS table.
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_Landing_SEQ.dtsx'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )
 ;
```

```sql
-- Variable: User::V_SQL_UPDATE_ON_ERROR
-- Purpose: Update the ETL_RUN_STATUS table to mark the package as "failed".
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_Landing_SEQ.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

```sql
-- Variable: User::V_SQL_UPDATE_ON_POST_EXECUTE
-- Purpose: Update the ETL_RUN_STATUS table to mark the package as "succeeded".
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
   AND ETL_SUB_COMPONENT_NM = 'CCEM_EMRGNCY_CRISIS_Landing_SEQ.dtsx')
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

```csharp
-- Expression:  Package\\DFT-CCEM_EMRGNCY_CRISIS\\DRVCOL_TRFM-etl_date.Outputs[Derived Column Output].Columns[etl_crea_dt].Properties[Expression]
-- Purpose: get current date
[GETDATE]()
```

```csharp
-- Expression:  Package\\DFT-CCEM_EMRGNCY_CRISIS\\DRVCOL_TRFM-etl_date.Outputs[Derived Column Output].Columns[etl_updt_dt].Properties[Expression]
-- Purpose: get current date
[GETDATE]()
```

```sql
-- SQL Statements (from ESQLT-Truncate_Tables)
TRUNCATE TABLE ccem_emrgncy_crisis;
TRUNCATE TABLE ccem_emrgncy_crisis_account;
TRUNCATE TABLE ccem_emrgncy_crisis_affectedperson;
TRUNCATE TABLE ccem_emrgncy_crisis_affectedperson_clientneeds;
TRUNCATE TABLE ccem_emrgncy_crisis_affectedperson_servicesprovided;
TRUNCATE TABLE ccem_emrgncy_crisis_client_needs;
TRUNCATE TABLE ccem_emrgncy_crisis_contact;
TRUNCATE TABLE ccem_emrgncy_crisis_country;
TRUNCATE TABLE ccem_emrgncy_crisis_country_risk;
TRUNCATE TABLE ccem_emrgncy_crisis_departure;
TRUNCATE TABLE ccem_emrgncy_crisis_enquirer;
TRUNCATE TABLE ccem_emrgncy_crisis_location;
TRUNCATE TABLE ccem_emrgncy_crisis_location_trip;
TRUNCATE TABLE ccem_emrgncy_crisis_service_provided;
TRUNCATE TABLE ccem_emrgncy_crisis_trip;
TRUNCATE TABLE ccem_emrgncy_crisis_tripdestination;
truncate table ccem_emrgncy_crisis_countrystatistics;
truncate table ccem_emrgncy_crisis_countrysubdivisionstatistics;
```

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| `[dbo].[ccem_emrgncy_crisis]`| Stores emergency crisis data | Part 1|
| `[dbo].[ccem_emrgncy_crisis_account]`  | Stores emergency crisis account data | Part 1, 4|
| `[dbo].[ccem_emrgncy_crisis_affectedperson]`  | Stores emergency crisis affected person data | Part 1, 4|
| `[dbo].[ccem_emrgncy_crisis_affectedperson_clientneeds]` | Stores emergency crisis affected person client needs data | Part 1, 4|
| `[dbo].[ccem_emrgncy_crisis_affectedperson_servicesprovided]` | Stores emergency crisis affected person services provided data | Part 1, 4|
| `[dbo].[ccem_emrgncy_crisis_client_needs]` | Stores emergency crisis client needs data | Part 1, 4|
| `[dbo].[ccem_emrgncy_crisis_contact]` | Stores emergency crisis contact data | Part 2, 4|
| `[dbo].[ccem_emrgncy_crisis_country]` | Stores emergency crisis country data | Part 3, 4|
| `[dbo].[ccem_emrgncy_crisis_country_risk]` | Stores emergency crisis country risk data | Part 3, 4|
| `[dbo].[ccem_emrgncy_crisis_countrystatistics]` | Stores emergency crisis country statistics data | Part 3, 4|
| `[dbo].[ccem_emrgncy_crisis_countrysubdivisionstatistics]` | Stores emergency crisis country subdivision statistics data | Part 3, 4|
| ccem_emrgncy_crisis_departure | Stores departure data | Part 4 |
| ccem_emrgncy_crisis_enquirer | Stores enquirer data | Part 4 |
| ccem_emrgncy_crisis_location | Stores location data | Part 4 |
| ccem_emrgncy_crisis_location_trip | Stores location trip data | Part 4 |
| ccem_emrgncy_crisis_service_provided | Stores service provided data | Part 4 |

## 6. Package Summary

*   **Input Connections:** 2 (Dynamics CRM, Excel)
*   **Output Destinations:** 7-16 fact tables
*   **Package Dependencies:** 0
*   **Activities:**
    *   Data Flow Tasks: 7-14
    *   Derived Column Transformations: 6-14
    *   Execute SQL Task: 1
*   **Transformations:** Derived Column
*   **Script tasks:** 0
* Overall package complexity assessment: moderate.
* Potential performance bottlenecks: Dynamics CRM Source, OLE DB Destination.
* Critical path analysis: The data flow tasks appear to execute sequentially.
* Error Handling Mechanisms: The primary error handling mechanism is the "Fail Component" setting on most data flow components. ETL Status Table: Updates the ETL_RUN_STATUS table.
```