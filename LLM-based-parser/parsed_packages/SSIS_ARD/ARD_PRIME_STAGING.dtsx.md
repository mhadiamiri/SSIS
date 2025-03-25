## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| ARD_PRIME_LANDING           | OLE DB          | Server: [Inferred], Database: ARD_PRIME_LANDING, Integrated Security=SSPI  | Source data extraction for lookups and data transformation for loading staging tables. | Requires appropriate database user permissions to read data from the source database. Secure storage of credentials within the Project Connection Manager or Windows Authentication. | None            | Part 1, 2, 3                  |
| ARD_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for storing the transformed data into staging tables.                           | Requires appropriate database user permissions to write data to the destination database. Secure storage of credentials within the Project Connection Manager. | None visible         | Part 1                 |
| ARD_REPORTING         | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for date information                    | Requires appropriate database user permissions to read data from the source database. Secure storage of credentials within the Project Connection Manager. | None visible         | Part 1         |
| DATA_HUB           | OLE DB          | Server: [Inferred], Database: Data_Hub, Integrated Security=SSPI  | Destination for storing the transformed data into staging tables.                           | Requires appropriate database user permissions to write data to the destination database. Secure storage of credentials within the Project Connection Manager or Windows Authentication. | None visible         | Part 1, 2, 3                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   **Expression Task:**
    *   `EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`: This task simply evaluates the expression `1 == 1`, which always results in true.
*   **Sequence Container:**
    *   `SEQC - LKP TABLES`:  Loads Lookup tables.
    *   `SEQC - LOAD STAGING TABLES - SPRINT2 STRUCTURE CONDITION`:  Loads tables related to structure conditions.
    *   `SEQC - LOAD STAGING TABLES - SPRINT3 SPACT THRESHOLD`:  Loads tables related to space allocation and thresholds.
    *   `SEQC - LOAD STAGING TABLES - SPRINT4`: Loads data related to cost period, currency conversion, effective family size, mission rent ceilings, and occupant approval.
    *   `SEQC - MOVED FROM OPERA`: Loads data from the OPERA database into tables such as PRM_ACCOMMODATION, PRM_AMA, PRM_CITY, PRM_COUNTRY.

#### DFT- PRM_FORECAST_DETAIL_LKP

*   **Source:** `OLEDB_SRC - tblForecastDetail` extracts data from the `tblForecastDetail` table.
*   **Transformations:**
    *   `LKP - tblAccommodationForecast`: Performs a lookup on `tblAccommodationForecast` using `ACCOMMODATION_FORECAST_ID` to retrieve `FISCAL_YEAR_ID` and `ACCOMMODATION_FORECAST_ARCHIVE_YES_NO_NA_ID`.
    *   `LKP - tblAccommodation`: Performs a lookup on `tblAccommodation` using `PROPERTY_ID` to retrieve `MISSION_ID`, `TITLE_ID`, and `FACILITY_TYPE_ID`.
    *   `DRV_TRFM - DATES`:  Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns with the current timestamp.
*   **Destination:** `OLEDB_DEST - PRM_FORECAST_DETAIL_LKP` inserts the transformed data into the `PRM_FORECAST_DETAIL_LKP` staging table.

#### DFT - PRM_TITLE

*   **Source:** `OLEDB_SRC - tblTitle` extracts data from the `tblTitle` table in the `ARD_PRIME_LANDING` database.
*   **Transformation:** `DRV_TRFM - DATES` creates two derived columns, `ETL_CREA_DT` and `ETL_UPDT_DT`, both populated with the current date and time.
*   **Destination:** `OLEDB_DEST - PRM_TITLE` loads the data into the `PRM_TITLE` table in the `DATA_HUB` database.

## 4. Code Extraction

```sql
-- OLEDB_SRC - tblForecastDetail (SQL Command)
SELECT [fod_ID] AS FORECAST_DETAIL_ID
      ,[fod_afo_id] AS ACCOMMODATION_FORECAST_ID
      ,[fod_cty_id] AS CURRENCY_ID
      ,[fod_fty_id] AS FORECAST_TYPE_ID
FROM [dbo].[tblForecastDetail]
```

```sql
-- LKP - tblAccommodationForecast (SQL Command)
SELECT [afo_ID] AS ACCOMMODATION_FORECAST_ID
      ,[afo_acc_id] AS PROPERTY_ID
      ,CONVERT(DATE, RIGHT('0000' + CONVERT(VARCHAR(4), [afo_StartYear] - 1),4) + '-04-01') AS [FISCAL_YEAR_ID]

      ,[afo_Archive_yen_id] AS ACCOMMODATION_FORECAST_ARCHIVE_YES_NO_NA_ID
FROM [dbo].[tblAccommodationForecast]
```

```sql
-- LKP - tblAccommodation (SQL Command)
select
acc_ID AS ACCOMMODATION_ID
, acc_mis_id AS MISSION_ID
, acc_ttl_id AS TITLE_ID
, acc_fac_id AS FACILITY_TYPE_ID
FROM [dbo].[tblAccommodation]
```

```sql
-- DRV_TRFM - DATES (Expression)
[GETDATE]() -- ETL_CREA_DT
[GETDATE]() -- ETL_UPDT_DT
```

```sql
-- Source: OLEDB_SRC - tblTitle (DFT - PRM_TITLE)
SELECT [ttl_ID] AS [TITLE_ID]
      ,[ttl_ExistingPRID] AS [TITLE_EXISTING_PRID]
      ,[ttl_SiteEntirelyHeld] AS [TITLE_SITE_ENTIRELY_HELD]
      ,[ttl_SiteArea] AS [TITLE_SITE_AREA]
      ,[ttl_SiteNumberOfBuildings] AS [TITLE_SITE_BUILDINGS_NBR]
      ,[ttl_LastUpdated] AS [TITLE_LAST_UPDATED_DTM]
      ,[ttl_UpdatedBy] AS [TITLE_UPDATED_BY_USER_NM]
      ,[ttl_mis_id] AS [TITTLE_MISSION_ID]
      ,[ttl_tty_id] AS [TITLE_TITLE_TYPE_ID]
      ,[ttl_doc_2id] AS [TITLE_DOCUMENT_2ID]
      ,[ttl_doc_id] AS [TITLE_DOCUMENT_ID]
      ,[ttl_typ_id] AS [TITLE_TYPE_ID]
      ,[ttl_AssetRecNoLand] AS [TITLE_ASSET_RECORD_NO_LAND]
      ,[ttl_LandDirectory] AS [TITLE_LAND_DIRECTORY]
      ,[ttl_AppraisedValueDt] AS [TITLE_APPRAISED_VALUE_DTM]
      ,[ttl_AppraisedValueAmt] AS [TITLE_APPRAISED_VALUE_AMT]
      ,[ttl_AppraisedValueAmt_cty_id] AS [TITLE_APPRAISED_VALUE_CURRENCY_TPYE_ID]
      ,[ttl_AppraisedValueCdnEquiv] AS [TITLE_APPRAISED_VALUE_CDN_EQUIVALENT_AMT]
      ,[ttl_MarketValueDt] AS [TITLE_MARKET_VALUE_DTM]
      ,[ttl_MarketValueAmt] AS [TITLE_MARKET_VALUE_AMT]
      ,[ttl_MarketValueAmt_cty_id] AS [TITLE_MARKET_VALUE_CURRENCY_TPYE_ID]
      ,[ttl_MarketValueCdnEquiv] AS [TITLE_MARKET_VALUE_CDN_EQUIVALENT_AMT]
      ,[ttl_TransferDate] AS [TITLE_TRANSFER_DTM]
      ,[ttl_BuildingTypesOnSite] AS [TITLE_BUILDING_TYPES_ON_SITE_TXT]
  FROM [dbo].[tblTitle]
```

```sql
-- ESQLT- TRUNCATE ALL STAGING TABLES (SQL Command)
TRUNCATE TABLE dbo.PRM_STRUCTURE_CONDITION_LKP;
TRUNCATE TABLE dbo.PRM_SPACE_THRESHOLD_LKP;
TRUNCATE TABLE dbo.PRM_FORECAST_DETAIL_LKP;
TRUNCATE TABLE dbo.PRM_PROPERTY_LKP;
TRUNCATE TABLE dbo.PRM_OCCUPANCY_LKP;
TRUNCATE TABLE dbo.PRM_LEASE_COSTING_LKP;
TRUNCATE TABLE dbo.PRM_RENT_COSTING_LKP;
```

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| PRM_OR_CATEGORY | Parameter table loaded from tblORCategory | Part 2 |
| PRM_BUILDING_TYPE  | Parameter table loaded from tblBuildingType  | Part 2|
| PRM_ACCOMMODATION_GEOGRAPHIC | Parameter table loaded from tblAccommodationGeographic | Part 2 |
| PRM_NO_OF_BEDROOMS  | Parameter table loaded from tblNoOfBedrooms  | Part 2|
| PRM_OCCUPANCY_STATUS_TYPE  | Parameter table loaded from tblOccupancyStatusType  | Part 2|
| PRM_ACCOMMODATION_PROFILE | Parameter table loaded from tblAccProfile | Part 2 |
| PRM_ACCOMMODATION_STATUS | Parameter table loaded from tblAccommodationStatus | Part 2 |
| PRM_TITLE_TYPE | Parameter table loaded from tblTitleType | Part 2 |
| PRM_ACQUISITION  | Parameter table loaded from tblAcquisition | Part 2|
| PRM_YES_NO_NA | Parameter table loaded from tblYesNoNa | Part 2|
| PRM_STRUCTURE_CONDITION_BY_FY  | Parameter table loaded from tblStructureConditionByFY | Part 2|
| PRM_STRUCTURE_CONDITION_TYPE | Parameter table loaded from tblStructureConditionType | Part 2 |
| PRM_DOCUMENT_TYPE  | Parameter table loaded from tblDocumentType | Part 2|
| PRM_TYPE  | Parameter table loaded from tblType | Part 2|
| PRM_TITLE | Parameter table loaded from tblTitle | Part 2 |
| PRM_ACCOMMODATION_FORECAST | Parameter table loaded from tblAccommodationForecast | Part 2 |
| PRM_ACCOMMODATION_SIZE  | Parameter table loaded from tblAccSize | Part 2|
| PRM_ARLU_RENT_REVISION_TYPE  | Parameter table loaded from tblArluRentRevisionType | Part 2|
| PRM_BASE_RENT_REVISION_TYPE | Parameter table loaded from tblBaseRentRevisionType | Part 2 |
| PRM_CLASSIFICATION  | Parameter table loaded from tblClassification | Part 2|
| PRM_COST_REVISION_TYPE | Parameter table loaded from tblCostRevisionType | Part 2 |
| PRM_CURRENCY_TYPE | Parameter table loaded from tblCurrencyType | Part 2 |
| PRM_DEPOSIT_TYPE  | Parameter table loaded from tblDepositType | Part 2|
| PRM_LEASE_TYPE | Parameter table loaded from tblLeaseType | Part 2 |
| PRM_FORECAST_DETAIL | Parameter table loaded from tblForecastDetail | Part 2 |
| PRM_PROGRAM_CODE  | Parameter table loaded from tblProgramCode | Part 2|
| PRM_PROGRAM_TYPE | Parameter table loaded from tblProgramType | Part 2 |
| PRM_SPACE_THRESHOLD_BY_FY | Parameter table loaded from tblSpaceThresholdByFY | Part 2 |
| PRM_PRID_CREATION_DATES | Parameter table loaded from tblPridCreationDates | Part 2 |
| PRM_OCCUPANT | Parameter table loaded from tblOccupant | Part 2 |
| PRM_ACCOMMODATION | Table loaded from tblAccommodation | Part 3 |
| PRM_AMA | Table loaded from tblAMA | Part 3 |
| PRM_CITY | Table loaded from tblCity | Part 3 |
| PRM_COUNTRY | Table loaded from tblCountry | Part 3 |
| PRM_MISSION_STATUS | Table loaded from tblMissionStatus | Part 3 |
| PRM_MISSION_CATEGORY | Table loaded from tblMissionCategory | Part 3 |

## 6. Package Summary

*   **Input Connections:** 2
*   **Output Destinations:** 30+
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 1 or 4
    *   Sequence Containers: 2 or 5
    *   Data Flow Tasks: 11 or 25
    *   Execute SQL Task: 1 or 6
*   **Transformations:**
    *   Derived Column: 13+
    *   Lookup: 18+
    *   Merge Join: 7
    *   Sort: 4
    *   Unpivot: 2
    *   Conditional Split: 1

*   **Script Tasks:** 0
*   **Overall Package Complexity Assessment:** Medium.
*   **Potential Performance Bottlenecks:**
    *   Multiple Lookup transformations could be a performance bottleneck.
    *   Sort transformations can be expensive for large datasets.
    *   The sequential execution of sequence containers.
*   **Critical Path Analysis:** The critical path is determined by the sequential execution of the data flow tasks within the Sequence Containers.
*   **Error Handling Mechanisms:** Error handling is implemented on most of the components but is set to "Fail Component" or "Ignore Failure" on the Lookup Transforms.
