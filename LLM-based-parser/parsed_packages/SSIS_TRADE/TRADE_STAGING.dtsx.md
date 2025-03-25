## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                | Purpose within Package                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Security Requirements                                                                                                                                                                                        | Parameters/Variables | Source Part |
|---------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|-------------|
| TRADE_REPORTING           | OLE DB          | Server, Database, potentially Authentication Method (not visible in XML)                                                | Destination connection for loading data into the `D_TRADE_HR_DATE` table.                                                                                                                                                                                                                                                                                                                                                                                                 | Requires credentials with write access to the `TRADE_REPORTING` database and the `D_TRADE_HR_DATE` table.  Appropriate firewall rules must be in place.                                      | None visible in XML           | Part 1, 3                  |
| DFAIT_Reporting         | OLE DB          | Server, Database, potentially Authentication Method (not visible in XML)                                                | Source connection for extracting data from the `D_HR_DATE` table.                                                                                                                                                                                                                                                                                                                                                                                                       | Requires credentials with read access to the `DFAIT_Reporting` database and the `D_HR_DATE` table. Appropriate firewall rules must be in place.                                          | None visible in XML           | Part 1, 3                  |
| TRADE_LANDING           | OLE DB          | Server, Database, potentially Authentication Method (not visible in XML)                                                | Source connection for multiple data flows extracting data from landing tables/views.                                                                                                                                                                                                                                                                                                                                                                                      | Requires credentials with read access to the `TRADE_LANDING` database and specific views (e.g., `FUNDED_POSITION_V`,`HR_LAYER_V`, `COMMERCIAL_INITIATIVE_LEVEL_V`, `KPI_LAYER_V`,`DFAIT_CASE_VIEW`, `DFAIT_ORG_VIEW`, `DFAIT_OPPORTUNITY_VIEW`). Firewall rules apply. | None visible in XML           | Part 1, 2, 3                  |
| TRADE_STAGING           | OLE DB          | Server, Database, potentially Authentication Method (not visible in XML)                                                | Destination connection for loading data into staging tables.                                                                                                                                                                                                                                                                                                                                                                                                                  | Requires credentials with write access to the `TRADE_STAGING` database and various staging tables (e.g., `S1_STRATEGIA_FUNDED_POSITION`, `S1_STRATEGIA_HR_LAYER`, `S1_STRATEGIA_INITIATIVE`, `S1_STRATEGIA_KPI_LAYER`, `S_TRADE_SECTOR`, `S_TRADE_CASE`).   | None visible in XML           | Part 1, 2, 3                  |
| BI_Conformed            | OLE DB          | Server, Database, potentially Authentication Method (not visible in XML)                                                | Source connection to `R_COUNTRY_MAPPING` and `R_IBM_SUPPORTED_COUNTRY` for lookup.                                                                                                                                                                                                                                                                                                                                                                                          | Requires read access to the `BI_Conformed` database, and the specified tables.  Firewall rules apply.                                                                                              | None visible in XML           | Part 1, 3                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package consists of several sequence containers, each containing a series of Data Flow Tasks (DFTs) and Execute SQL Tasks (ESQLTs).

1.  **EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode:** This is an Expression Task that evaluates the expression `1 == 1`.

2.  **SEQC-D\_TRADE\_HR\_DATE:** This is a Sequence Container responsible for loading the `D_TRADE_HR_DATE` dimension table.

    *   **ESQLT- Truncate D\_TRADE\_HR\_DATE:** An Execute SQL Task that truncates the `dbo.D_TRADE_HR_DATE` table.
    *   **ESQLT- Insert Unknown Members-D\_TRADE\_HR\_DATE:** An Execute SQL Task that inserts a default "unknown member" record into the `dbo.D_TRADE_HR_DATE` table.
    *   **DFT-DIMENSION\_D\_TRADE\_HR\_DATE:** A Data Flow Task responsible for extracting data from `dbo.D_HR_DATE`, transforming it (implicitly, based on column mapping), and loading it into `dbo.D_TRADE_HR_DATE`.
        *   **Source:** OLE DB Source (`OLEDB_SRC--D_HR_DATE`) extracts data from the `dbo.D_HR_DATE` table in the `DFAIT_Reporting` database.
        *   **Destination:** OLE DB Destination (`OLEDB_Dest-D_TRADE_HR_DATE`) loads data into the `[dbo].[D_TRADE_HR_DATE]` table in the `TRADE_REPORTING` database.
        *   **Transformations:** There are no explicit transformations defined in the XML, but the column mappings from source to destination imply implicit data type conversions.

3.  **SEQC-STAGING\_10\_SPT14:** This sequence container is responsible for loading "S1" staging tables like `S1_STRATEGIA_FUNDED_POSITION`, `S1_STRATEGIA_HR_LAYER`, `S1_STRATEGIA_INITIATIVE`, `S1_STRATEGIA_KPI_LAYER`.

4.  **SEQC-STAGING\_1\_SPT9:** This sequence container is responsible for loading "S" staging tables like `S_TRADE_SECTOR`, `S_TRADE_CASE`, `S_TRADE_ORGANIZATION`, `S_TRADE_STATUS`, `S_TRADE_POST_HIERARCHY`, `S_TRADE_OPPORTUNITY_VIEW`.

5.  **SEQC-STAGING\_2\_SPT9:** This sequence container is responsible for loading "S" staging tables like `S_TRADE_CONTACT`, `S_TRADE_BUSINESS_LINE`, `S_TRADE_ACTIVITY_SUBTYPE`, `S1_TRADE_COUNTRY`, `S_TRADE_COUNTRY`.

6.  **SEQC-STAGING\_3\_SPT10:** This sequence container is responsible for loading "S" staging tables like `S_TRADE_ISSUES_VIEW`, `S_TRADE_SUCCESSES_VIEW`, `S_TRADE_FDI_PROJECT`, `S_TRADE_FUNDING_VIEW`, `S_TRADE_BRIDGE_FUNDING_COUNTRY`.

7.  **SEQC-STAGING\_4\_SPT11:**
    *   ESQLT- TRUNCATE STAGING\_4
    *   DFT-S\_TRADE\_EMPL\_MATCHING
    *   DFT-S\_TRADE\_ORG\_MATCHING
    *   DFT-S\_TRADE\_OUTCALL\_TRIO1
    *   DFT-W1\_TRADE\_OUTCALL\_TRIO1

8.  **SEQC-STAGING\_5\_SPT11:**
    *   ESQLT- TRUNCATE STAGING\_3
    *   DFT-S\_TRADE\_EMPLOYEE
    *   DFT-S\_TRADE\_OUTCALL\_VIEW
    *   DFT-S\_TRADE\_OBJECTIVE

9.  **SEQC-STAGING\_6\_SPT12:**
    *   ESQLT- TRUNCATE STAGING\_3
    *   DFT-S\_TRADE\_SERVICE\_VIEW
    *   DFT-S\_TRADE\_SERVICE\_TYPE
    *   DFT-S\_TRADE\_SERVICE\_VIEW\_CREATED
    *   DFT-S\_TRADE\_SERVICE\_TRIO1
    *   DFT-W1\_TRADE\_SERVICE\_TRIO1 1

10. **SEQC-STAGING\_7\_SPT13:**
    *   ESQLT- TRUNCATE STAGING\_3
    *   DFT-S\_TRADE\_ORG\_LISTS\_VIEW
    *   DFT-S\_TRADE\_OPPORTUNITY\_REFERRAL\_VIEW
    *   DFT\_S\_TRADE\_ORG\_SPC\_CHAR
    *   DFT-S\_TRADE\_ORG\_MARKETS\_INTEREST
    *   DFT-S\_TRADE\_ORGANIZATION\_RELATIONSHIP
    *   DFT-S\_TRADE\_CONNECTION
    *   DFT-S\_TRADE\_CONNECTION\_TRIO1
    *   DFT-W1\_TRADE\_CONNECTION\_TRIO1

11. **SEQC-STAGING\_8\_SPT14:** The DFT \'DFT-S\_TRADE COMMITMENTS\' is dependent on \'DFT-W1\_TRADE\_HR\'. Then DFT\'s \'DFT-S\_TRADE\_CSF\_IMS\_COMMITMENTS\', \' DFT-S\_TRADE\_CSF\_IMS\_RESERVATIONS\',  \'DFT-W\_TRADE\_COMMS\_RES\', \'DFT-S\_TRADE\_FINANCIALS\', \'DFT-S\_TRADE\_IMS\_DATA\' all execute sequentially.

    *   DFT-S\_TRADE\_COMMITMENTS
    *   DFT-S\_TRADE\_CSF\_IMS\_COMMITMENTS
    *   DFT-S\_TRADE\_CSF\_IMS\_RESERVATIONS
    *   DFT-S\_TRADE\_FINANCIALS
    *   DFT-S\_TRADE\_IMS\_DATA
    *   DFT-W1\_TRADE\_HR
    *   DFT-W\_TRADE\_COMMS\_RES
    *   ESQLT- TRUNCATE STAGING\_HR\_FINANCIAL

12. **SEQC-STAGING\_9\_SPT15** The Data Flow Tasks seem to execute sequentially in most cases.

    *   DFT-S2\_TRADE\_BUDGET
    *   DFT-S2\_TRADE\_COMMITMENTS
    *   DFT\_S\_TRADE\_ACTUALS
    *   DFT\_S\_TRADE\_FTE\_TO\_DELETE
    *   DFT-S\_TRADE\_ACTIVITIES
    *   DFT-S\_TRADE\_ACTIVITIES\_VIEW
    *   DFT-S\_TRADE\_SURVEYS
    *   DFT-S\_TRADE\_SURVEY\_QUESTIONS
    *   ESQLT- TRUNCATE STAGING\_3

**Precedence Constraints:**

*   The tasks within sequence containers generally execute sequentially, based on success.
*   The pattern is often TRUNCATE (tables) -> Load (data).

#### DFT-S\_TRADE\_CSF\_IMS\_COMMITMENTS

*   **Source:** OLE DB Source (OLEDBSRC-CSF\_IMS\_COMMITMENTS\_2011\_2016) extracts data from `dbo.CSF_IMS_COMMITMENTS_2011_2016` in the `TRADE_LANDING` database.
*   **Transformations:**
    *   `Data Conversion (CONV_TRFM_Data_Type)`: Converts `GJAHR_CALC` (wstr to str),  `FUND_CENTRE_CD` (nText to wstr), and `COMMITMENT_DOC_NBR` (nText to wstr).
    *   `Derived Column (DRV_TRFM-ETL_DATE)`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns with GETDATE().
*   **Destination:** OLE DB Destination (OLEDB\_Dest-S\_TRADE\_CSF\_IMS\_COMMITMENTS) loads data into `dbo.S_TRADE_CSF_IMS_COMMITMENTS` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-S\_TRADE\_CSF\_IMS\_RESERVATIONS

*   **Source:** OLE DB Source (OLEDB\_SRC-CSF\_IMS\_RESERVATIONS\_2011\_2016) extracts data from `dbo.CSF_IMS_RESERVATIONS_2011_2016` in the `TRADE_LANDING` database.
*   **Transformations:**
    *   `Data Conversion (CONV_TRFM_DATA_TYPE_Unicode)`: Converts  `FUNDS_RESERVATION_DOC_NBR` (nText to wstr), `DOC_COUNT` (nText to wstr).
    *   `Data Conversion (CONV_TRFM_DATA_TYPE_String)`: Converts strings.
    *    Derived Column (DRV\_TRFM-ETL\\_DATE): Adds ETL-related date columns with default values.
*   **Destination:** OLE DB Destination (OLEDB\_Dest-S\_TRADE\_CSF\_IMS\_RESERVATIONS) loads data into `dbo.S_TRADE_CSF_IMS_RESERVATIONS` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-S\_TRADE\_FINANCIALS

*   **Source:** OLE DB Source (OLEDB\_SRC-TRADE\_CSF) extracts data from `dbo.TRADE_CSF` in the `TRADE_LANDING` database.
*   **Transformations:** No explicit transformations are listed.
*   **Destination:** OLE DB Destination (OLEDB\_Dest-S\_TRADE\_FINANCIALS) loads data into `dbo.S_TRADE_FINANCIALS` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-S\_TRADE\_IMS\_DATA

*   **Source:** OLE DB Source (OLEDB\_SRC-F\_FIN\_COMMITMENTS) extracts data from  `dbo.F_FIN_COMMITMENTS` and `dbo.D_COMMON_FUND_CENTRE` in the DFAIT\_Reporting database.
*   **Transformations:** No explicit transformations are listed.
*   **Destination:** OLE DB Destination (OLEDB\_Dest-S\_TRADE\_IMS\_DATA) loads data into `dbo.S_TRADE_IMS_DATA` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-W1\_TRADE\_HR

*   **Source:** OLE DB Source (OLEDB\_SRC-HR\_From\_DFAIT) extracts data from HR tables in the DFAIT\_Reporting database using a complex SQL query.
*   **Transformations:**
    *   `Conditional Split (TRFM_Conditional Split)`: Splits data based on the `LOCATION_TXT_EN` column (`NoOttawa` condition: `LOCATION_TXT_EN != "Ottawa"`).
    *   `Derived Column (Derived Column)`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** OLE DB Destination (OLEDB\_Dest-W1\_TRADE\_HR) loads data into `dbo.W1_TRADE_HR` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-W\_TRADE\_COMMS\_RES

*   **Source 1:** OLE DB Source (OLEDB\_SRC-S\_TRADE\_CSF\_IMS\_COMMITMENTS) extracts data from `S_TRADE_CSF_IMS_COMMITMENTS` and `S_TRADE_CSF_IMS_RESERVATIONS` in the `TRADE_STAGING` database.
*   **Source 2:** OLE DB Source (OLEDB\_SRC-R\_POST\_HIERARCHY) extracts data from `dbo.R_POST_HIERARCHY` in the `BI_Conformed` database.
*   **Transformations:**
    *   `Sort (TRFM_SORT_By_POST_CODE_Left)`: Sorts by `POST_CD`.
    *   `Sort (TRFM_SORT_By_POST_CODE_Right)`: Sorts by `POST_CD`.
    *   `Merge Join (Merge Join)`: FULL join on `POST_CD`.
    *    Data Conversion (CONV\_TRFM-DATA\\_TYPE 1): Converts data types
*   **Destination:** OLE DB Destination (OLEDB\_Dest-W\_TRADE\_COMMS\_RES) loads data into `dbo.W_TRADE_COMMS_RES` in the `TRADE_STAGING` database.
*   **Error Handling:**  Fail Component.

#### DFT-S2\_TRADE\_BUDGET

*   **Source:** OLE DB Source (OLEDB\_SRC-S\_TRADE\_BUDGET) extracts data from `dbo.S_TRADE_BUDGET` in the TRADE\_STAGING database.
*   **Transformations:** No explicit transformations are listed.
*   **Destination:** OLE DB Destination (OLEDB\_Dest-S2\_TRADE\_BUDGET) loads data into `dbo.S2_TRADE_BUDGET` in the TRADE\_STAGING database.
*   **Error Handling:**  Fail Component.

#### DFT-S2\_TRADE\_COMMITMENTS

*   **Source:** OLE DB Source (OLEDB\_SRC-S\_TRADE\_COMMITMENTS) extracts data from `dbo.S_TRADE_COMMITMENTS` and `dbo.W_TRADE_COMMS_RES` in the TRADE\_STAGING database.
*   **Transformations:** No explicit transformations are listed.
*   **Destination:** Destination not defined.

#### Data Flow Tasks Breakdown:

Each DFT generally follows a pattern of:

1.  **OLE DB Source:** Extracts data from a source table or view (often in the LANDING or REPORTING database).
2.  **Transformations (if any):** Performs data cleansing, conversion, or lookups.
3.  **OLE DB Destination:** Loads the transformed data into a staging table (in the STAGING database).

**Notable Transformations**

*   **Data Conversion Tasks:** Used to change data types. For example, converting strings to Unicode.
*   **Derived Column Transformation:** Used to calculate values or create new columns based on existing ones (e.g. in DFT-W1\_TRADE\_OUTCALL\_TRIO1 to create DATE\_LU).
*   **Lookup Transformations:** Used to enrich data by joining with lookup tables (e.g. in DFT-W1\_TRADE\_OUTCALL\_TRIO1, Lookup\_ORG\_LU and Lookup\_ASSIGNED\_TO\_LU). Lookups use the `TRADE_STAGING` connection.

**Error Handling:**

*   All OLE DB Destinations and Sources have error outputs defined.
*   `errorRowDisposition="FailComponent"` is common, meaning any error will stop the entire task. `errorOrTruncationOperation="Insert"`

## 4. Code Extraction

```sql
-- Source query for OLEDB_SRC--D_HR_DATE
SELECT	"DATE_SID",
	"YEAR_ID",
	"MONTH_ID",
	"QUARTER_ID",
	"CALENDAR_YYYYMM",
	"FISCAL_YEAR",
	"FISCAL_MONTH",
	"FISCAL_QUARTER",
	"FISCAL_YYYYMM",
	"MONTH_DESC_EN",
	"MONTH_DESC_FR",
	"MONTH_START_DT",
	"MONTH_END_DT",
	"MONTH_NO",
	"PERIOD",
	"CURRENT_YEAR_ID",
	"CURRENT_QUARTER_ID",
	"CURRENT_CALENDAR_YYYYMM",
	"CURRENT_FISCAL_YEAR",
	"CURRENT_FISCAL_QUARTER",
	"CURRENT_FISCAL_YYYYMM",
	"CURRENT_PERIOD",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."D_HR_DATE"
```

Context: Extracts data from the `D_HR_DATE` table in the `DFAIT_Reporting` database for loading into the `D_TRADE_HR_DATE` dimension table in `TRADE_REPORTING`.

```sql
-- SQL statement for ESQLT- Insert Unknown Members-D_TRADE_HR_DATE
--SET IDENTITY_INSERT dbo.[D_TRADE_HR_DATE] ON

INSERT INTO [dbo].[D_TRADE_HR_DATE]
           ([DATE_SID]
      ,[YEAR_ID]
      ,[MONTH_ID]
      ,[QUARTER_ID]
      ,[CALENDAR_YYYYMM]
      ,[FISCAL_YEAR]
      ,[FISCAL_MONTH]
      ,[FISCAL_QUARTER]
      ,[FISCAL_YYYYMM]
      ,[MONTH_DESC_EN]
      ,[MONTH_DESC_FR]
      ,[MONTH_START_DT]
      ,[MONTH_END_DT]
      ,[MONTH_NO]
      ,[PERIOD]
      ,[CURRENT_YEAR_ID]
      ,[CURRENT_QUARTER_ID]
      ,[CURRENT_CALENDAR_YYYYMM]
      ,[CURRENT_FISCAL_YEAR]
      ,[CURRENT_FISCAL_QUARTER]
      ,[CURRENT_FISCAL_YYYYMM]
      ,[CURRENT_PERIOD]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT])
     VALUES
           (-3 ,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,getdate(), getdate())

--SET IDENTITY_INSERT dbo.[D_TRADE_HR_DATE] OFF
```

Context: Inserts a default "unknown member" record into the `D_TRADE_HR_DATE` table in the `TRADE_REPORTING` database.

```sql
-- SQL statement for ESQLT- Truncate D_TRADE_HR_DATE
TRUNCATE TABLE dbo.D_TRADE_HR_DATE;
```

Context: Truncates the `D_TRADE_HR_DATE` table in the `TRADE_REPORTING` database.

```sql
-- Source query for OLEDB_SRC-FUNDED_POSITION_V
SELECT DISTINCT	T1."FundedPositionID" as FUNDED_POSITION_ID,
	T1."FundedPositionTypeID" as FUNDED_POSITION_TYPE_ID,
       \'F-\' + cast(FundedPositionTypeID as char(1)) as POS_TYPE_KEY,
	T1."ResourceID" as RESOURCE_ID,
	T1."PositionVersionFiscalYearID" as POS_VERSION_FY_ID,
	T1."PartnerVersionFiscalYearID" as PAR_VERSION_FY_ID,
	T1."SectorFunctionVersionFiscalYearID" as SEC_FUNC_VERSION_FY_ID,
	T1."PlanStatusID" as PLAN_STATUS_ID,
	T1."DfaitCBS" as DFAIT_CBS_NBR,
	T1."DfaitLES" as DFAIT_LES_NBR,
	T1."PartnerCBS" as PARTNER_CBS_NBR,
	T1."PartnerLES" as PARTNER_LES_NBR,
	T1."PrioritySector" as PRIORITY_SECTOR,
       MISSIONSYMBOL,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   FUNDED_POSITION_V T1
```

Context: This query is used to extract data from the `FUNDED_POSITION_V` view in the `TRADE_LANDING` database and load it into the `S1_STRATEGIA_FUNDED_POSITION` staging table.

```sql
-- Source query for OLEDB_SRC-HR_LAYER_V
SELECT	"FiscalYearEn" as FISCAL_YEAR_EN,
	"MissionSymbol" as MISSION_SYMBOL,
	"SectorFunctionID" as FUNCTION_ID,
	"SectorFunctionTypeID" as FUNCTION_TYPE_ID,
	"PrioritySector" as PRIORITY_SECTOR,
	coalesce("DfaitCBS",0) as DFATD_CBS,
	coalesce("DfaitLES",0) as DFATD_LES,
	coalesce("PartnerCBS",0) as PARTNER_CBS,
	coalesce("PartnerLES",0) as PARTNER_LES,
                   getdate() as ETL_CREA_DT,
                   getdate() as ETL_UPDT_DT
FROM   "dbo"."HR_LAYER_V"
```

Context: This query is used to extract data from the `HR_LAYER_V` view in the `TRADE_LANDING` database and load it into the `S1_STRATEGIA_HR_LAYER` staging table.

```sql
-- Source query for OLEDB_SRC-COMMERCIAL_INITIATIVE_LEVEL_V
SELECT	"MissionSymbol" as MISSION_SYMBOL,
	"FiscalYearEn" as FISCAL_YEAR_EN,
	"FundingSourceTypeEn" as FUNDING_SOURCE_TYPE_EN,
	"FundingSourceTypeFr" as FUNDING_SOURCE_TYPE_FR,
	"FundingSourceNameEn" as FUNDING_SOURCE_NAME_EN,
	"FundingSourceNameFr" as FUNDING_SOURCE_NAME_FR,
	"Planned" as PLANNED_AMT,
	"Allocated" as ALLOCATED_AMT,
	"Actual" as ACTUAL_AMT,
	"FundingSourceTypeID" as FUNDING_SOURCE_TYPE_ID,
	"SectorFunctionNameEn" as SECTOR_FUNCTION_NAME_EN,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."COMMERCIAL_INITIATIVE_LEVEL_V"
```

Context: This query is used to extract data from the `COMMERCIAL_INITIATIVE_LEVEL_V` view in the `TRADE_LANDING` database and load it into the `S1_STRATEGIA_INITIATIVE` staging table.

```sql
-- Source query for OLEDB_SRC-KPI_LAYER_V
SELECT	"FiscalYearEn" as FISCAL_YEAR_EN,
	"MissionSymbol" as MISSION_SYMBOL,
	"SectorFunctionID" as FUNCTION_ID,
	"SectorFunctionNameEn" as SECTOR_FUNCTION_NAME_EN,
	"PerformanceIndicatorID" as PERFORMANCE_INDICATOR_ID,
	"InitiativeID" as INITIATIVE_ID,
	"InitiativeName" as INITIATIVE_NAME,
	"CurrentTarget" as CURRENT_TARGET,
"CompletionStatusID" as COMPLETION_STATUS_ID,
"MultiMissionTypeID" as MULTI_MISSION_TYPE_ID,
InitiativeTypeID as INITIATIVE_TYPE_ID,
"SectorFunctionTypeID" as SECTOR_FUNCTION_TYPE_ID,
"TrioCaseNumber" as TRIO_CASE_NBR

FROM KPI_LAYER_V
```

Context: This query is used to extract data from the `KPI_LAYER_V` view in the `TRADE_LANDING` database and load it into the `S1_STRATEGIA_KPI_LAYER` staging table.

```sql
-- SQL statement for ESQLT- TRUNCATE STAGING_1
TRUNCATE TABLE  dbo.S1_STRATEGIA_FUNDED_POSITION;
TRUNCATE TABLE  dbo.S1_STRATEGIA_HR_LAYER;
TRUNCATE TABLE  dbo.S1_STRATEGIA_INITIATIVE;
TRUNCATE TABLE  dbo.S1_STRATEGIA_KPI_LAYER;
--TRUNCATE TABLE  dbo.S1_STRATEGIA_POSITION;
```

Context: This query truncates multiple tables in the TRADE_STAGING database.

```sql
-- Source query for OLEDB_SRC-SECTOR
SELECT	DISTINCT
	"LIC" AS SECTOR_DESCR_EN,
	"VALUE"  AS SECTOR_DESCR_FR,
       \'\' AS SECTOR_SUBSECTOR_EN,
       \'\' AS SECTOR_SUBSECTOR_FR,
	getdate()  as  ETL_CREA_DT,
	getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_LOV_SECTOR"
WHERE LANG_ID = \'FRA\'
```

Context: This query is used to extract data from the `DFAIT_LOV_SECTOR` view in the `TRADE_LANDING` database and load it into the `S_TRADE_SECTOR` staging table.

```sql
-- Source query for OLEDB_SRC-CASE
SELECT	"CASE_NBR",
	"CASE_NAME_EN",
	"CASE_DESCR",
	"CASE_STATUS",
	"CASE_BUSINESS_LINE",
	"CASE_OWNER_OFFICE",
	"CASE_OWNER",
	"CASE_CREATED_ON_DT",
	getdate()  as  ETL_CREA_DT,
getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_CASE_VIEW"
```

Context: This query is used to extract data from the `DFAIT_CASE_VIEW` view in the `TRADE_LANDING` database and load it into the `S_TRADE_CASE` staging table.
```sql
-- ESQLT- TRUNCATE STAGING_4
TRUNCATE TABLE  dbo.S_TRADE_EMPL_MATCHING ;
TRUNCATE TABLE  dbo.S_TRADE_ORG_MATCHING;
TRUNCATE TABLE  dbo.S_TRADE_OUTCALL_TRIO1;
TRUNCATE TABLE  dbo.W1_TRADE_OUTCALL_TRIO1;

-- OLEDB_SRC-DFAIT_SERVICE_VIEW (DFT-S_TRADE_EMPL_MATCHING)
SELECT "USER_ID", "EMPLOYEE_ID", "USER_STATUS", getdate() as ETL_CREA_DT, getdate() as ETL_UPDT_DT
FROM "dbo"."DFAIT_SERVICE_VIEW"

-- OLEDB_SRC_DFAIT_SERVICE_VIEW (DFT-S_TRADE_ORG_MATCHING)
SELECT	DISTINCT "ORG_ID",
	"TRIO1_ORG_ID",
	getdate()  as ETL_CREA_DT,
	getdate()  as ETL_UPDT_DT
FROM   "dbo"."DFAIT_SERVICE_VIEW"

--OLEDB_SRC-TRIO1Outcalls (DFT-S_TRADE_OUTCALL_TRIO1)
SELECT	"DATE_LU",
	"ORG_LU",
	"SECTOR_LU",
	"STATUS_LU",
	"CONTACT_LU",
	"CREATED_BY_LU",
	"POST_LU",
	"OUTCALL_DT",
	"OBJECTIVE_LU",
	"ASSIGNED_TO_LU",
	"OUTCALL_NUMBER",
	1 as "OUTCALL_COUNT"
FROM   "dbo"."TRIO1Outcalls"

--OLEDB_SRC-S_TRADE_OUTCALL_TRIO1 (DFT-W1_TRADE_OUTCALL_TRIO1)
SELECT
       convert(varchar(10),(CASE WHEN MONTH(T1."OUTCALL_DT") > 3 THEN CONVERT(DATETIME, \'3/31/\' + CONVERT(VARCHAR(4), YEAR("OUTCALL_DT") + 1))
            ELSE CONVERT(DATETIME, \'3/31/\' + CONVERT(VARCHAR(4), YEAR(T1."OUTCALL_DT")))\
       END),121) as DATE_LU,

--(SELECT "ORG_ID" FROM "dbo"."S_TRADE_ORG_MATCHING" T2 WHERE T1.ORG_LU = T2."TRIO1_ORG_ID") as ORG_LU,
   T1. "ORG_LU",
(CASE
         WHEN SECTOR_LU IN (\'Advanced Materials\',\'Multi-Sectoral\',\'Non-Sectoral\',\'Tourism\', \'Undetermined\') THEN \'-\'\
         WHEN SECTOR_LU IN ( \'Aerospace &amp; Defence\',\'Space\') THEN \'Aerospace\'\
         WHEN SECTOR_LU IN (\'Agriculture, Food &amp; Beverages\', \'Fish &amp; Seafood Products\') THEN \'Agriculture, Food &amp; Beverages\'\
         WHEN SECTOR_LU LIKE \'Agricultural Technology and Eq\' THEN \'Agricultural Tech &amp; Equipment\'\
         WHEN SECTOR_LU = \'Arts &amp; Cultural Industries\' THEN \'Arts and Cultural Industries\'\
         WHEN SECTOR_LU = \'Automotive\' THEN \'Automotive\'\
         WHEN SECTOR_LU IN ( \'Bio-Industries\',\'Health Industries\') THEN \'Life Sciences\'\
         WHEN SECTOR_LU LIKE \'Building Products &amp; Constructi%\' THEN \'Infrastr/Building Prod &amp; Serv.\'\
         WHEN SECTOR_LU LIKE \'Service Industries &amp; Capital P%\' THEN \'Infrastr/Building Prod &amp; Serv.\'\
         WHEN SECTOR_LU IN ( \'Chemicals\',\'Plastics\') THEN \'Chemicals and Plastics\'\
         WHEN SECTOR_LU = \'Consumer Products\' THEN \'Consumer Products\'\
         WHEN SECTOR_LU = \'Education\' THEN \'Education\'\
         WHEN SECTOR_LU IN (\'Electric Power Equipment &amp; Ser\',\'Environmental Industries\') THEN \'Cleantech\'\
         WHEN SECTOR_LU = \'Forest Industries\' THEN \'Forest Products\'\
         WHEN SECTOR_LU like \'Information &amp; Communications T%\' THEN \'Information &amp; Comm. Technology\'\
         WHEN SECTOR_LU = \'Manufacturing Technologies\' THEN \'Machinery &amp; Equipment\'\
         WHEN SECTOR_LU like \'Metals, Minerals &amp; Related Equ%\' THEN \'Mining\'\
         WHEN SECTOR_LU = \'Ocean Technologies\' THEN \'Ocean Industries\'\
         WHEN SECTOR_LU = \'Oil &amp; Gas Equipment &amp; Services\' THEN \'Oil and Gas\'\
         WHEN SECTOR_LU = \'Rail &amp; Urban Transit\' THEN \'Transportation\'\
       ELSE \'-\'\
END) as SECTOR_LU,
(CASE
       WHEN STATUS_LU IN (\'Awaiting Response from Client\',\
                          \'Awaiting Response from IBOC\',\
                          \'Awaiting Response from PSU\',\
                          \'Ongoing\',\
                          \'Open\',\
                          \'Response from PSU\') THEN \'Open\'\
       WHEN STATUS_LU in (\'Closed\') THEN \'Service Delivered\'\
       WHEN STATUS_LU in (\'Cancelled\') THEN \'Cancelled\'\
END) as  STATUS_LU,
	T1."CONTACT_LU",
	T1."CREATED_BY_LU",
	T1."POST_LU",
	T1."OUTCALL_DT",
	T1."OBJECTIVE_LU",

 --      coalesce(T2.USER_ID,\'-\') as ASSIGNED_TO_LU,
                   T1.ASSIGNED_TO_LU,
	T1."OUTCALL_NUMBER",
	T1."OUTCALL_COUNT"
FROM   "dbo"."S_TRADE_OUTCALL_TRIO1" T1

--Lookup_ASSIGNED_TO_LU SqlCommand (DFT-W1_TRADE_OUTCALL_TRIO1)
Select  coalesce(T2.USER_ID,\'-\') as ASSIGNED_TO_LU,
  T2."USER_ID"
  FROM   "dbo"."S_TRADE_OUTCALL_TRIO1" T1 LEFT OUTER JOIN "dbo"."S_TRADE_EMPL_MATCHING" T2
       ON T1.ASSIGNED_TO_LU = T2."USER_ID"

--Lookup_ASSIGNED_TO_LU SqlCommandParam (DFT-W1_TRADE_OUTCALL_TRIO1)
select * from (Select  coalesce(T2.USER_ID,\'-\') as ASSIGNED_TO_LU,
  T2."USER_ID"
  FROM   "dbo"."S_TRADE_OUTCALL_TRIO1" T1 LEFT OUTER JOIN "dbo"."S_TRADE_