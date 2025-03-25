## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| CCEM_SOURCE           | Dynamics CRM          | Server: [Inferred], Auth: [Inferred] | Source for multiple dataflows | Dynamics CRM Auth likely | None                  | Part 1, 2, 3, 4, 5, 6, 7|
| ODS_CCEM           | OLE DB          | Server: [Inferred], Database: [Inferred] | Destination for multiple dataflows | SQL Server Auth likely | None           | Part 1, 2, 3, 4, 5, 6, 7                |
| CSP_ArcGIS           | OLE DB          | Server: [Inferred], Database: [Inferred] | Destination for multiple dataflows | SQL Server Auth likely | None           | Part 1, 2               |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4, 5, 6, 7|

## 3. Package Flow Analysis

The package `CSP_ArcGIS` consists of a single Sequence Container. The sequence container contains several data flow tasks and Execute SQL tasks.

*   **Sequence Container:** Contains the entire workflow.
*   **ESQLT-Truncate\_Tables:** Execute SQL Task to truncate staging tables in the ODS_CCEM database, before the data load.
*   **DFT-ccem\_affectedperson\_CSP:** Data Flow Task to load or transform `ccem_affectedperson` data from CCEM_SOURCE to ODS_CCEM.
*   **DFT-ccem\_tripdestination\_CSP:** Data Flow Task to load or transform `ccem_tripdestination` data from CCEM_SOURCE to ODS_CCEM.
*   **DFT-ccem\_departure\_CSP:** Data Flow Task to load or transform `ccem_departure` data from CCEM_SOURCE to ODS_CCEM.
*   **DFT- ccem\_crisis\_CSP:** Data Flow Task to load or transform `ccem_crisis` data from CCEM_SOURCE to ODS_CCEM.
*   **DFT-contact\_CSP:** Data Flow Task to load or transform `contact` data from CCEM_SOURCE to ODS_CCEM.
*   **DFT-ccem\_country\_CSP:** Data Flow Task to load or transform `ccem_country` data from CCEM_SOURCE to ODS_CCEM.
*   **ESQLT-Truncate\_Delete\_Dest\_Tables:** Execute SQL Task to truncate destination tables in the CSP_ArcGIS database.
*   **DFT-CSP\_ArcGIS-CCEM\_CRISIS:** Data Flow Task to load or transform `ccem_tripdestination` data from ODS_CCEM to CSP_ArcGIS.
*   **DFT-CSP\_ArcGIS-CCEM\_ROCA 1:** Data Flow Task to load or transform `ccem_tripdestination` data from ODS_CCEM to CSP_ArcGIS.
*   **DFT-CSP\_ArcGIS-CCEM\_ROCA:** Data Flow Task to load or transform `ccem_tripdestination` data from ODS_CCEM to CSP_ArcGIS. This task is disabled.

**Data Flow Task Details:**

#### DFT- ccem_crisis_CSP

*   **Source:** `CRM_SRC-ccem_crisis` extracts data from the `ccem_crisis` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-ccem_crisis_CSP` loads data into the `[ccem_crisis_CSP]` table in the ODS_CCEM database.

#### DFT- ccem_departure_CSP

*   **Source:** `CRM_SRC-ccem_departure` extracts data from the `ccem_departure` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-ccem_departure_CSP` loads data into the `[ccem_departure_CSP]` table in the ODS_CCEM database.

#### DFT-ccem_affectedperson_CSP

*   **Source:** `CRM_SRC-ccem_affectedperson` extracts data from the `ccem_affectedperson` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-ccem_affectedperson_CSP` loads data into the `[ccem_affectedperson_CSP]` table in the ODS_CCEM database.

#### DFT-ccem_country_CSP

*   **Source:** `CRM_SRC-ccem_country` extracts data from the `ccem_country` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-ccem_country` loads data into the `[ccem_country_CSP]` table in the ODS_CCEM database.

#### DFT-ccem_tripdestination_CSP

*   **Source:** `CRM_SRC-ccem_tripdestination` extracts data from the `ccem_tripdestination` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-ccem_tripdestination_CSP` loads data into the `[ccem_tripdestination_CSP]` table in the ODS_CCEM database.

#### DFT-contact_CSP

*   **Source:** `CRM_SRC-contact` extracts data from the `contact` entity in the Dynamics CRM (CCEM_SOURCE).
*   **Transformations:**
    *   `DRVCOL_TRFM-etl_date`: Adds `etl_crea_dt` and `etl_updt_dt` columns with the current date and time using GETDATE().
*   **Destination:** `OLEDB_DEST-contact_CSP` loads data into the `[contact_CSP]` table in the ODS_CCEM database.

#### DFT-CSP_ArcGIS-CCEM_CRISIS

*   **Source:** `OLEDB_SRC-ccem_tripdestination` extracts data from a custom SQL query against the ODS_CCEM database involving joins on `ccem_affectedperson_CSP`, `contact_CSP`, `ccem_crisis_CSP`, `ccem_departure_CSP`.
*   **Transformations:** None.
*   **Destination:** `OLEDB_Dest-CCEM_CRISIS` loads data into the `[CCEM_CRISIS]` table in the CSP_ArcGIS database.

#### DFT-CSP_ArcGIS-CCEM_ROCA 1

*   **Source:** `OLEDB_SRC-ccem_tripdestination` extracts data from a custom SQL query against the ODS_CCEM database involving joins on `ccem_tripdestination_CSP` and `ccem_country_CSP`.
*   **Transformations:** None.
*   **Destination:** `OLEDB_Dest-CCEM_ROCA` loads data into the `[CCEM_ROCA]` table in the CSP_ArcGIS database.

## 4. Code Extraction

```sql
truncate table dbo.ccem_affectedperson_CSP;
truncate table [dbo].[contact_CSP];
truncate table [dbo].[ccem_crisis_CSP];
truncate table [dbo].[ccem_departure_CSP];
truncate table [dbo].[ccem_country_CSP];
truncate table [dbo].[ccem_tripdestination_CSP];
```

Context: SQL to truncate tables in the ODS_CCEM database.

```sql
truncate table [dbo].[ccem_crisis];
delete from [dbo].[CCEM_ROCA]
where date= cast(getdate() as date)
```

Context: SQL to truncate and delete from tables in the CSP_ArcGIS database.

```sql
select 
	 a.ccem_identification  ,
     a.ccem_group, 
      a.ccem_ismaincontactforgroup,
      a.ccem_longitude,
      a.ccem_latitude,
      a.ccem_totalclientneeds,
      a.statuscode,
      a.ccem_line1,
      a.ccem_departure_repayform,
      a.ccem_priority,
      a.ccem_seats,
      a.createdon,
      a.modifiedon,
      a.ccem_affectedpersonid,
	  cc.firstname,
        cc.lastname,
        cc.birthdate,
        cc.ccem_statusincanada,
        cc.emailaddress1,
        cc.address1_telephone1,
		cr.ccem_identification as ccem_crisis,
		cd.ccem_identification as ccem_departure,
a.createdbyname,
	  a.modifiedbyname,
    getdate() as etl_crea_dt,
   getdate() as etl_updt_dt
	  FROM [dbo].[ccem_affectedperson_CSP] a
	  join [dbo].[contact_CSP] cc
	  on a.[ccem_contact] = cc.contactid 
	  left outer	 join  [dbo].[ccem_crisis_CSP] cr
	  on a.[ccem_crisis] = cr.[ccem_crisisid]  
	  left outer join [dbo].[ccem_departure_CSP] cd
	  on a.[ccem_departure] =cd.[ccem_departureid]
```

Context: SQL query to extract data for DFT-CSP_ArcGIS-CCEM_CRISIS.

```sql
select count(*) as totalNumberRegistrants
,cast(getdate() as date) as date
, concat(c.ccem_identificationenglish,'|-/-|',ccem_identificationfrench)  as ccem_country_ccem_identification
, c.ccem_identificationenglish
,c.ccem_identificationfrench
,ccem_gc_identifier 
,getdate() as etl_crea_dt
,getdate() as etl_updt_dt
    FROM [dbo].[ccem_tripdestination_CSP] t  
	 join [dbo].[ccem_country_CSP] c
	on t.ccem_country = c.ccem_countryid 
	group by  concat(c.ccem_identificationenglish,'|-/-|',ccem_identificationfrench)  ,
c.ccem_identificationenglish
,c.ccem_identificationfrench
,ccem_gc_identifier
```

Context: SQL query to extract data for DFT-CSP_ArcGIS-CCEM_ROCA 1 and DFT-CSP_ArcGIS-CCEM_ROCA.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.ccem_affectedperson_CSP  | Stores affected person data        | Part 3      |
| dbo.contact_CSP  | Stores contact data        | Part 3      |
| dbo.ccem_crisis_CSP  | Stores ccem_crisis data        | Part 3      |
| dbo.ccem_departure_CSP  | Stores ccem_departure data       | Part 3      |
| dbo.ccem_country_CSP  | Stores ccem_country data        | Part 3      |
| dbo.ccem_tripdestination_CSP  | Stores ccem_tripdestination data        | Part 3      |
| dbo.CCEM_CRISIS  | Stores ccem_tripdestination data for ArcGIS        | Part 3      |
| dbo.CCEM_ROCA  | Stores ccem_tripdestination data for ArcGIS        | Part 3      |

## 6. Package Summary

*   **Input Connections:** 2
    *   Dynamics CRM (CCEM_SOURCE)
    *   ODS_CCEM (OLE DB)
*   **Output Destinations:** 3
    *   ODS_CCEM (OLE DB)
    *   CSP_ArcGIS (OLE DB)
    *   Dynamics CRM (ODS_CCEM)
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 8
    *   Execute SQL Tasks: 2
    *   Derived Column: 2
*   **Transformations:**
    *   Derived Column: 2
*   **Script tasks:** 0
*   Overall package complexity assessment: Medium
*   Potential performance bottlenecks:
    *   Data conversion operations in data flows
    *   Large data volume extraction from Dynamics CRM
    *   SQL queries
*   Critical path analysis: The critical path involves the sequential execution of truncate tasks, data flow tasks, and destination loads.
*   Error handling mechanisms: Error handling is configured at the component level, failing the component on error. There are OLE DB Destination Error Outputs.
