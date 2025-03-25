## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| TRADE_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data and destination | SQL Server Auth likely | None            | Part 1                  |
| TRADE_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for dimension tables             | SQL Server Auth likely            |  None                  | Part 1                 |
|DFAIT_Staging|OLE DB|Server: [Inferred], Database: [Inferred]|Destination for reference data|SQL Server Auth likely|None|Part 2|

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1|

## 3. Package Flow Analysis

The package `TRADE_DIMENSION` is designed to load and transform data for several dimension tables related to trade. The package starts with an expression task, and the main workflow is orchestrated through several sequence containers, each responsible for loading a specific dimension table. Overall, the package truncates, loads, and performs DBCC checks on dimension tables.

*   **Overall Control Flow:**

    1.  `Dimensions - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`: An Expression Task that always evaluates to true (1 == 1).  Probably a placeholder.
    2.  `SEQC-COUNTRY-POST HIERARCHY`: Loads country and post hierarchy dimensions.
    3.  `SEQC-DATES`: Loads date-related dimensions.
    4.  `SEQC-D_STRATEGIA_DATE`: Loads Strategia date dimensions.
    5.  `SEQC-D_STRATEGIA_DATE_PARTNER`: Loads Strategia date partner dimensions.
    6.  `SEQC-D_STRATEGIA_DATE_POSITION`: Loads Strategia date position dimensions.
    7.  `SEQC-D_STRATEGIA_FUNDING_SOURCE`: Loads Strategia funding source dimensions.
    8.  `SEQC-D_STRATEGIA_INDICATOR`: Loads Strategia indicator dimensions.
    9.  `SEQC-D_STRATEGIA_INITIATIVE`: Loads Strategia initiative dimensions.
    10. `SEQC-D_STRATEGIA_INITIATIVE_TYPE`: Loads Strategia initiative type dimensions.
    11. `SEQC-D_STRATEGIA_MULTI_MISSION_TYPE`: Loads Strategia multi-mission type dimensions.
    12. `SEQC-D_STRATEGIA_POSITION_TYPE`: Loads Strategia position type dimensions.
    13. `SEQC-D_TRADE_BUSINESS_LINE`: Loads trade business line dimensions.
    14. `SEQC-D_TRADE_CASE`: Loads trade case dimensions.
    15. `SEQC-D_TRADE_CONTACT`: Loads trade contact dimensions.
    16. `SEQC-D_TRADE_EMPLOYEE`: Loads trade employee dimensions.
    17. `SEQC-D_TRADE_FDI_PROJECT`: Loads trade FDI project dimensions.
    18. `SEQC-D_TRADE_FUNDING`: Loads trade funding dimensions.
    19. `SEQC-D_TRADE_ISSUES`: Loads trade issues dimensions.
    20. `SEQC-D_TRADE_OBJECTIVE`: Loads trade objective dimensions.
    21. `SEQC-D_TRADE_ORGANIZATION_RELATIONSHI`: Loads trade organization relationship dimensions.
    22. `SEQC-D_TRADE_OUTCALL`: Loads trade outcall dimensions.
    23. `SEQC-D_TRADE_SECTOR`: Loads trade sector dimensions.
    24. `SEQC-D_TRADE_SERVICE`: Loads trade service dimensions.
    25. `SEQC-D_TRADE_SERVICE_TYPE`: Loads trade service type dimensions.
    26. `SEQC-D_TRADE_SURVEY`: Loads trade survey dimensions.
    27. `SEQC-D_TRADE_SURVEY_CHOICES`: Loads trade survey choices dimensions.
    28. `SEQC-D_TRADE_SURVEY_QUESTIONS`: Loads trade survey questions dimensions.

#### DFT-D_TRADE_COUNTRY

*   **Source:** OLE DB Source (`OLEDB_SRC-D_TRADE_COUNTRY`) extracts data from `dbo.S_TRADE_COUNTRY` view
*   **Transformations:** None.
*   **Destination:** OLE DB Destination (`OLEDB_DEST-D_TRADE_COUNTRY`) loads data into `dbo.D_TRADE_COUNTRY` table.

#### DFT-DIMENSION_D_TRADE_POST_HIERARCHY

*   **Source:** OLE DB Source (`OLEDB_SRC_S_TRADE_POST_HIERARCHY`) extracts data from `dbo.S_TRADE_POST_HIERARCHY`
*   **Transformations:**
    *   `Lookup`: Looks up `COUNTRY_SID` based on `ALPHA_2_CD` from `dbo.D_TRADE_COUNTRY`.
    *   `Derived Column`: Creates `COUNTRY_SID_DRV` using `REPLACENULL` on the looked up `COUNTRY_SID` and `-3`.
    *   `Derived Column`: Converts `POST_ID` to integer (`POST_ID_DRV`).
*   **Destination:** OLE DB Destination (`OLEDB_DEST_R_D_TRADE_POST_HIERARCHY`) loads data into `dbo.D_TRADE_POST_HIERARCHY`.

#### DFT-R_TRADE_POST_HIERARCHY

*   **Source:** OLE DB Source (`OLEDB-SRC-R_TRADE_POST_HIERARCHY`) extracts data from `dbo.D_TRADE_POST_HIERARCHY`
*   **Transformations:** None.
*   **Destination:** OLE DB Destination (`OLEDB-DEST-R_TRADE_POST_HIERARCHY`) loads data into `dbo.R_TRADE_POST_HIERARCHY`.

#### DFT-D_TRADE_DATE

*   **Source:** OLE DB Source (`OLEDB_SRC-D_TRADE_DATE`) extracts data from `dbo.S_TRADE_DATE`
*   **Transformations:** None.
*   **Destination:** OLE DB Destination (`OLEDB_DEST-D_TRADE_DATE`) loads data into `dbo.D_TRADE_DATE` table.

#### DFT-D_TRADE_FIN_DATE

*   **Source:** OLE DB Source (`OLEDB_SRC-D_TRADE_FIN_DATE`) extracts data from a SELECT statement using the `D_TRADE_DATE` table.
*   **Transformations:** None.
*   **Destination:** OLE DB Destination (`OLEDB_DEST-D_TRADE_FIN_DATE`) loads data into `dbo.D_TRADE_FIN_DATE` table.

#### DFT-DIMENSION_D_STRATEGIA_DATE

*   **Source:** OLE DB Source (`OLEDB_SRC-FiscalYear`) extracts data from `dbo.FiscalYear`.
*   **Transformations:**
    *   `Derived Column`: Creates `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   `Derived Column`: Creates `Default_FY_Year1` based on `DEFAULT_FISCAL_YEAR` column.
*   **Destination:** OLE DB Destination (`OLEDB_Dest-D_STRATEGIA_DATE`) loads data into `dbo.D_STRATEGIA_DATE` table.

#### DFT-DIMENSION_D_TRADE_OPPORTUNITY

*   **Source:** OLE DB Source (`OLEDB_SRC_S_TRADE_OPPORTUNITY_VIEW`) extracts data from `dbo.S_TRADE_OPPORTUNITY_VIEW`.
*   **Transformations:**
    *   `Data Conversion`: Converts the `OPPORTUNITY_DESCR` and `OPPORTUNITY_NBR` columns to Unicode.
*   **Destination:** OLE DB Destination (`OLEDB_DEST_R_D_TRADE_OPPORTUNITY`) loads data into `dbo.D_TRADE_OPPORTUNITY` table.

#### DFT-DIMENSION_D_TRADE_SERVICE

*   **Source:** OLE DB Source (`OLEDB_SRC-S_TRADE_SERVICE_VIEW`) extracts data from `dbo.S_TRADE_SERVICE_VIEW`.
*   **Transformations:**
    *   `Multicast`: Copies the data flow.
    *   `Merge Join`: Combines the data with a data flow from `OLEDB_SRC-W1_TRADE_SERVICE_TRIO1` based on `SERVICE_NBR`.
    *   `Conditional Split`: Splits data based on whether the `DRIVE_SERVICE_NBR` column is null.
    *   `Union ALL`: Combines the data flows.
*   **Destination:** OLE DB Destination (`OLEDB_Dest-D_TRADE_SERVICE`) loads data into `dbo.D_TRADE_SERVICE` table.

#### DFT-DIMENSION_D_STRATEGIA_INITIATIVE

*   **Source:** None Specified.
*   **Transformations:** None Specified.
*   **Destination:** None Specified.

#### DFT-DIMENSION_D_STRATEGIA_FUNDING_SOURCE

*   **Source:** None Specified.
*   **Transformations:** None Specified.
*   **Destination:** None Specified.

#### DFT-DIMENSION_D_STRATEGIA_POSITION_TYPE

*   **Source:** None Specified.
*   **Transformations:** None Specified.
*   **Destination:** None Specified.

#### DFT-DIMENSION_D_STRATEGIA_DATE_PARTNER

*   **Source:** None Specified.
*   **Transformations:** None Specified.
*   **Destination:** None Specified.

#### DFT-DIMENSION_D_STRATEGIA_DATE_SECTOR

*   **Source:** None Specified.
*   **Transformations:** None Specified.
*   **Destination:** None Specified.

## 4. Code Extraction

```sql
SELECT DISTINCT "COUNTRY_ID",
		"ALPHA_2_CD",
		"COUNTRY_EN",
		"COUNTRY_FR",
		"IBM_SUPPORTED_COUNTRY_EN",
		"IBM_SUPPORTED_COUNTRY_FR",
		"REGION_ID",
		"REGION_NAME_EN",
		"REGION_NAME_FR",
		getdate()  as  ETL_CREA_DT,
	    getdate()  as  ETL_UPDT_DT

  FROM dbo.S_TRADE_COUNTRY
```

Context: SQL query used in `OLEDB_SRC-D_TRADE_COUNTRY` to extract data from the staging table.

```sql
DBCC CHECKIDENT ('dbo.D_TRADE_COUNTRY', RESEED, 1)
```

Context: SQL query used in `ESQL-DBCC - D_TRADE_COUNTRY` to reset identity column in the destination table.

```sql
SET IDENTITY_INSERT dbo.D_TRADE_COUNTRY ON

INSERT INTO dbo.D_TRADE_COUNTRY
    ( [COUNTRY_SID]
      ,[COUNTRY_ID]
      ,[ALPHA_2_CD]
      ,[COUNTRY_EN]
      ,[COUNTRY_FR]
      ,[IBM_SUPPORTED_COUNTRY_EN]
      ,[IBM_SUPPORTED_COUNTRY_FR]
      ,[REGION_ID]
      ,[REGION_NAME_EN]
      ,[REGION_NAME_FR]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT])
VALUES 
    (  -3,
         -3,
  NULL,
  'Uncoded',
  'Non codé',
  'Uncoded',
  'Non codé',
  -3,
  'Uncoded',
  'Non codé',
  getdate(),
     getdate()

)

SET IDENTITY_INSERT dbo.D_TRADE_COUNTRY OFF
```

Context: SQL query used in `ESQLT- Insert Unknown Members_D_TRADE_COUNTRY` to insert a default "Uncoded" member into the dimension table.

```sql
Truncate table dbo.D_TRADE_COUNTRY;
```

Context: SQL query used in `ESQLT- Truncate D_TRADE_COUNTRY` to truncate the dimension table before loading.

```sql
SELECT	case when COUNTRY_SID=-3 then '-3'
        else ALPHA_2_CD end as INPUT_CD,
	    COUNTRY_SID as OUTPUT_SID
FROM   "dbo"."D_TRADE_COUNTRY"
```

Context: SQL query used in `LKP_TRFM_S_TRADE_POST_HIERARCHY` to create look up table.

```sql
(DT_I4)#{Package\SEQC-COUNTRY-POST HIERARCHY\SEQC-D_TRADE_POST_HIERARCHY\DFT-DIMENSION_D_TRADE_POST_HIERARCHY\OLEDB_SRC_S_TRADE_POST_HIERARCHY.Outputs[OLE DB Source Output].Columns[POST_ID]}
```

Context: Expression used in Derived Column `DRVCOL_TRFM_S_TRADE_POST_HIERACHY` to cast POST_ID to I4.

```sql
[REPLACENULL](#{Package\SEQC-COUNTRY-POST HIERARCHY\SEQC-D_TRADE_POST_HIERARCHY\DFT-DIMENSION_D_TRADE_POST_HIERARCHY\LKP_TRFM_S_TRADE_POST_HIERACHY.Outputs[Lookup Match Output].Columns[COUNTRY_SID]},-3)
```

Context: Expression used in Derived Column `DRVCOL_TRFM_S_TRADE_POST_HIERACHY` to replace null value for column COUNTRY_SID with -3

## 5. Output Analysis

| Destination Table                     | Description                                                                                                                                                                                                          |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dbo.D_TRADE_COUNTRY                  | Stores country dimension data.                                                                                                                                                                                              |
| dbo.D_TRADE_POST_HIERARCHY           | Stores post hierarchy dimension data.                                                                                                                                                                                          |
| dbo.R_TRADE_POST_HIERARCHY           | Stores relationship data for trade post hierarchy.                                                                                                                                                                                             |
| dbo.D_TRADE_DATE                   | Stores trade date dimension data.                                                                                                                                                                                               |
| dbo.D_TRADE_FIN_DATE                   | Stores trade financial date dimension data.                                                                                                                                                                                               |
| dbo.D_STRATEGIA_DATE  | Stores Strategia date dimension data                                                                                                                                                                                             |
| dbo.D_TRADE_OPPORTUNITY  | Stores trade opportunity dimension data                                                                                                                                                                                             |
| dbo.D_TRADE_SERVICE  | Stores trade service dimension data                                                                                                                                                                                           |
| dbo.D_STRATEGIA_FUNDING_SOURCE  | Stores trade Strategia funding source dimension data                                                                                                                                                                                             |
| dbo.D_STRATEGIA_INDICATOR  | Stores trade Strategia indicator dimension data                                                                                                                                                                                            |
| dbo.D_STRATEGIA_INITIATIVE  | Stores trade Strategia initiative dimension data                                                                                                                                                                                            |
| dbo.D_STRATEGIA_INITIATIVE_TYPE  | Stores trade Strategia initiative type dimension data                                                                                                                                                                                               |
| dbo.D_STRATEGIA_MULTI_MISSION_TYPE  | Stores trade Strategia multi mission type dimension data                                                                                                                                                                                               |
| dbo.D_STRATEGIA_POSITION_TYPE  | Stores trade Strategia position type dimension data                                                                                                                                                                                             |
| dbo.D_TRADE_BUSINESS_LINE  | Stores trade business line dimension data                                                                                                                                                                                              |
| dbo.D_TRADE_CASE  | Stores trade case dimension data                                                                                                                                                                                             |
| dbo.D_TRADE_CONTACT  | Stores trade contact dimension data                                                                                                                                                                                            |
| dbo.D_TRADE_EMPLOYEE  | Stores trade employee dimension data                                                                                                                                                                                             |
| dbo.D_TRADE_FDI_PROJECT   | Stores trade FDI project dimension data                                                                                                                                                                                            |
| dbo.D_TRADE_FUNDING  | Stores trade funding data                                                                                                                                                                                             |
| dbo.D_TRADE_ISSUES  | Stores trade issues data                                                                                                                                                                                              |
| dbo.D_TRADE_OBJECTIVE  | Stores trade objective data                                                                                                                                                                                             |
| dbo.D_TRADE_ORGANIZATION_RELATIONSHI  | Stores trade organization relationship data                                                                                                                                                                                         |
| dbo.D_TRADE_OUTCALL  | Stores trade outcall data                                                                                                                                                                                        |
| dbo.D_TRADE_SECTOR  | Stores trade sector dimension data                                                                                                                                                                                           |
| dbo.D_TRADE_SERVICE_TYPE  | Stores trade service type dimension data                                                                                                                                                                                        |
| dbo.D_TRADE_SURVEY  | Stores trade survey data                                                                                                                                                                                             |
| dbo.D_TRADE_SURVEY_CHOICES  | Stores trade survey choices data                                                                                                                                                                                            |
| dbo.D_TRADE_SURVEY_QUESTIONS  | Stores trade survey questions data                                                                                                                                                                                            |

## 6. Package Summary

*   **Input Connections:** 2
    *   TRADE_REPORTING
    *   TRADE_STAGING
    *   DFAIT_Staging
*   **Output Destinations:** 28 dimension tables
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 10+
    *   Data Flow Tasks: 3+
    *   Execute SQL Tasks: 7+
    *   Expression Tasks: 1
    *   Derived Column: 4+
    *   Lookup: 1+
    *   Data Conversion: 1+
    *   Union All: 1+
    *   Conditional Split: 1+
*   Overall package complexity assessment: High.
*   Potential performance bottlenecks:
    *   Multiple extractions and loads to staging and reporting databases.
    *   Likely a bottleneck on the lookups, consider caching.
*   Critical path analysis:
    * The sequence of truncating, inserting default members, and loading data into each dimension table appears to be a serial operation.
*   Error handling mechanisms:
    *   Error output paths on OLE DB Sources and Destinations.
    *   Event handlers for `OnError` and `OnPostExecute` events to update ETL process status.  The error description from the system variable is not being captured.
