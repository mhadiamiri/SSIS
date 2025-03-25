## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| EXCEL Connection Manager  | EXCEL           | Provider: Microsoft.ACE.OLEDB.12.0; Data Source: C:\\Users\\admLIUJ6\\Documents\\Project\\Financial Sample.xlsx; Extended Properties: "EXCEL 12.0 XML;HDR=YES";  | Reads data from an Excel file. | Excel file security, user read permissions | None            | Part 1                  |
| ODS_CCEM           | OLE DB          | Server: [Inferred], Database: [Inferred], Authentication: Integrated Security=SSPI (Likely) | Writes data to the ODS database. Destination for various fact tables. Truncates tables. | SQL Server user credentials with write/truncate access to the tables.  Principle of Least Privilege. | Command Timeout, Fast Load options, Server, Database name, username, password | Part 1, 2, 3, 4, 5                  |
| CCEM_SOURCE           | Dynamics CRM      | Server: [Inferred], OrganizationService: https://ccem_source.dynamics.com/XRMServices/2011/Organization.svc, Authentication Method | Source for fact tables. Extracts data from Dynamics CRM entities.  | Dynamics CRM user credentials with read access to the specified entities. Might use impersonation. | Batch Size, Max Rows Returned, Output Timezone, username, password, organization details |  Part 1, 2, 4, 5                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4, 5|

## 3. Package Flow Analysis

*   **Overall Control Flow:**
    *   The package primarily consists of Sequence Containers containing Data Flow Tasks (DFTs).
    *   The DFTs extract data from Dynamics CRM and load it into SQL Server tables in the ODS_CCEM database.
    *   Many Sequence Containers are used, such as `SEQC- LANDIN_1-6_CCEM_CASE`, `SEQC-LANDING-SP1-5-crisis`,   `SEQC-LANDING_SP1-1`, and `SEQC-LANDING_SP1-3-activity`.
    *   The execution order is generally sequential within each Sequence Container.
    *   Some Sequence Containers are disabled, such as `SEQC- LANDIN_1-6_CCEM_CASE` and `SEQC-LANDING_SP1-4-activity`.
    *   Many Execute SQL Tasks (ESQLT) truncate tables before data loading within the Sequence Containers.

#### DFT- L_ccem_case (Example)

*   **Source:** Dynamics CRM Source\_ccem\_case1 extracts data from the `ccem_case` entity in Dynamics CRM.
*   **Transformation:** Derived Column adds `etl_crea_dt` and `etl_updt_dt` using `GETDATE()`.
*   **Destination:** OLEDB\_DEST-ccem\_case loads the data into the `ccem_case` table in the ODS\_CCEM database.
*   **Error Handling:**  Error rows are handled by failing the component.

#### DFT- ccem_homicide (Example)

*   **Source:** `Dynamics CRM Source_ccem_homicide` extracts data from the `ccem_homicide` entity in Dynamics CRM.
*   **Transformation:** `Derived Column` creates `ETL_CREA_DT` and `ETL_UPDT_DT` with `GETDATE()`.
*   **Destination:** `OLE DB_DEST_ODS_CCEM_ccem_homicide` loads the data into the `ccem_homicide` table.
*   **Error Handling:** `errorRowDisposition` is set to "FailComponent".

#### DFT- ccem_departure_activity (Example)

*   **Source:** `CRM_SRC-ccem_departure_activity` extracts data from the `ccem_departure_activity` entity in Dynamics CRM.
*   **Transformation:** `Derived Column` adds `etl_crea_dt` and `etl_updt_dt` using the `GETDATE()` function.
*   **Destination:** `OLEDB_ccem_departure_activity` loads data into the `[dbo].[ccem_departure_activity]` table in the `ODS_CCEM` database.
*   **Error Handling:** Error rows are handled by failing the component.

#### DFT-ccem_transfer_activity (Example)

*   **Source:** `CRM_SRC-ccem_transfer_activity` (KingswaySoft Dynamics CRM Source) extracts data from the `ccem_transfer_activity` entity in Dynamics 365
*   **Transformation:** `DRVCOL_TRFM-etl_date` (Derived Column Transformation) adds two new columns: `etl_crea_dt` and `etl_updt_dt` and Populates these columns with the current date and time using the `GETDATE()` function.
*   **Destination:** `OLEDB_DEST-ccem_transfer_activity` (OLE DB Destination) loads the transformed data into the `[dbo].[ccem_transfer_activity]` table.
*   **Error Handling:** Error handling is set to `FailComponent`

## 4. Code Extraction

```sql
-- ESQLT-Truncate-CCEM_CASE
TRUNCATE TABLE ccem_case;
```

```sql
-- SQL Command in Execute SQL Task (ESQLT- Truncate Landing_1)

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
--TRUNCATE TABLE dbo.ccem_fraud;
TRUNCATE TABLE dbo.ccem_fund;
TRUNCATE TABLE dbo.ccem_general;
--TRUNCATE TABLE dbo.ccem_homicide;
--TRUNCATE TABLE dbo.ccem_kidnapping;
TRUNCATE TABLE dbo.ccem_lost;
TRUNCATE TABLE dbo.ccem_marriage;
TRUNCATE TABLE dbo.ccem_medical;
--TRUNCATE TABLE dbo.ccem_theft;
TRUNCATE TABLE dbo.ccem_transfer;
TRUNCATE TABLE dbo.ccem_welfare;
TRUNCATE TABLE dbo.ccem_wellbeing;
TRUNCATE TABLE dbo.ccem_arrest_transfer;
TRUNCATE TABLE dbo.ccem_prisonvisit;
```

```sql
truncate table  dbo.ccem_crisis_activity;
truncate table dbo.ccem_crisis;
truncate table dbo.ccem_departure_activity;
truncate table  dbo.ccem_departure;
truncate table   dbo.stringmap;
truncate table   dbo.account;
truncate table   dbo.organization;
```

```sql
TRUNCATE TABLE dbo.ccem_sla;
TRUNCATE TABLE dbo.ccem_sla_settings;
```

```sql
TRUNCATE TABLE dbo.ccem_country;
TRUNCATE TABLE dbo.contact;
TRUNCATE TABLE dbo.ccem_case_contact;
TRUNCATE TABLE dbo.ccem_region;
TRUNCATE TABLE dbo.ccem_trip;
TRUNCATE TABLE dbo.ccem_tripdestination;
TRUNCATE TABLE dbo.ccem_region_country;
```

```sql
truncate table ccem_crime_activity;
truncate table ccem_crisis_activity;
truncate table ccem_custody_activity;
truncate table ccem_death_activity;
truncate table ccem_departure_activity;
truncate table ccem_desertion_activity;
truncate table ccem_distress_activity;
truncate table ccem_fund_activity;
```

```sql
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

These SQL queries are used to truncate tables in the ODS_CCEM database before loading new data.

```
--Expression in Derived Column Transformation (DRVCOL_TRFM-etl_date)
[GETDATE]()
```

This expression is used in the Derived Column transformation to get the current date and time.  It's used to populate `etl_crea_dt` and `etl_updt_dt` columns.

```
--User::V_SQL_UPDATE_ON_ERROR
--Source: Expression for SQLTask:SqlStatementSource in the event handler OnError
--Destination: N/A

--User::V_SQL_UPDATE_ON_POST_EXECUTE
--Source: Expression for SQLTask:SqlStatementSource in the event handler OnPostExecute
--Destination: N/A

--User::V_SQL_INSERT_ON_PRE_EXECUTE
--Source: Expression for SQLTask:SqlStatementSource in the event handler OnPreExecute
--Destination: N/A
```

These variables are used to store SQL statements for event handlers, likely for updating ETL status.

```
GETDATE()
--Source: DRVCOL_TRFM-etl_date in DFT-ccem_transfer_activity, DFT-ccem_welfare_activity, DFT-ccem_wellbeing_activity
--Creates etl_crea_dt, etl_updt_dt

1==1
--Source: EXPRESSIONT- Start Task 1 in event handlers
--Validation
```

GETDATE() is used to create timestamp for metadata columns, and 1==1 for validation.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| `ccem_case` |  The `ccem_case` table in the ODS_CCEM database. | Part 1 |
| `ccem_homicide` | Writes to the `ccem_homicide` table in the ODS_CCEM database. | Part 2 |
| `ccem_departure_activity` |  Loads data into the `[dbo].[ccem_departure_activity]` table in the `ODS_CCEM` database. | Part 4 |
|  `[dbo].[ccem_transfer_activity]` |  Loads data into the `[dbo].[ccem_transfer_activity]` table in the `ODS_CCEM` database. | Part 5 |
| `[dbo].[ccem_welfare_activity]` | Loads data into the `[dbo].[ccem_welfare_activity]` table in the `ODS_CCEM` database. | Part 5 |
| `[dbo].[ccem_wellbeing_activity]` |  Loads data into the `[dbo].[ccem_wellbeing_activity]` table in the `ODS_CCEM` database. | Part 5 |

The destination points are OLE DB Destinations, loading data into tables within the `ODS_CCEM` database.

## 6. Package Summary

*   **Input Connections:** 2 (Excel, Dynamics CRM or just Dynamics CRM)
*   **Output Destinations:** Multiple OLE DB Destinations (number depends on the sequence container contents) + Execute SQL Tasks for truncating tables.  Typically one OLE DB Destination per data flow task within the sequence containers.
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: Numerous
    *   Data Flow Tasks: Numerous
    *   Execute SQL Tasks: Numerous
    *   Derived Column: Numerous instances.

*   **Transformations:** Derived Column (for ETL metadata).
*   **Script Tasks:** 0

*   **Overall package complexity assessment:** Medium. The package is relatively straightforward in terms of data flow logic, but the sheer number of Data Flow Tasks and columns involved makes it moderately complex.
*   **Potential performance bottlenecks:**
    *   Dynamics CRM Source: Performance depends on the complexity of the query, the amount of data being retrieved, and network latency.
    *   OLE DB Destination: Bulk inserts can be optimized by using appropriate batch sizes and fast load options.
    *   The full load strategy (truncating tables before loading) can be inefficient for large datasets.
*   **Critical path analysis:** The critical path is likely the sequential execution of Data Flow Tasks within the sequence containers. The `Truncate` task happens first, which impacts all the other tasks.

### Error Handling

*   The `errorRowDisposition` is set to "FailComponent," which causes the entire component to fail upon encountering an error.
*   The `OLE DB Destination` also has an error output configured, but it isn't clear from the snippets how this error output is handled.
*   Event handlers for PreExecute, OnError, OnPostExecute which update ETL process status table.
