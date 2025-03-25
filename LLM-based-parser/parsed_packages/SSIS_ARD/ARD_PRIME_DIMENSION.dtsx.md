```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| DATA_HUB           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for dimension data | SQL Server Auth likely | None | Part 1, 2, 3                  |
| ARD_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for dimension data | SQL Server Auth likely | None | Part 1, 2, 3                  |
| ARD_PRIME_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for dimension data (Unknown Members) | SQL Server Auth likely | None | Part 1, 2, 3                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `ARD_PRIME_DIMENSION` primarily loads dimension tables. It starts with an `Expression Task` then proceeds with two `Sequence Containers`: `SEQC - LOAD DIMENSION TABLES - SPRINT 2` and `SEQC - LOAD DIMENSION TABLES - SPRINT 3`. A third sequence, `SEQC - TRUNCATE TABLES & INSERT UNKNOWN MEMBER`, truncates the target dimension tables and inserts "unknown member" rows.  The detailed breakdown of each data flow task within the Sequence Containers follows:

#### DFT - D_PRM_COST_PERIOD

*   **Source:** `OLEDB_SRC - PRM_COST_PERIOD` extracts data from `dbo.PRM_COST_PERIOD` in the `DATA_HUB` database.
*   **Transformations:**
    *   `LKP - PRM_CURRENCY_TYPE - BASE`: Lookups `CURRENCY_BASE_CD`, `CURRENCY_BASE_EN_NM`, and `CURRENCY_BASE_FR_NM` from `dbo.PRM_CURRENCY_TYPE` based on `CURRENCY_BASE_ID`.
    *   `LKP - PRM_CURRENCY_TYPE - OTHER`: Lookups `CURRENCY_OTHER_CD`, `CURRENCY_OTHER_EN_NM`, and `CURRENCY_OTHER_FR_NM` from `dbo.PRM_CURRENCY_TYPE` based on `CURRENCY_OTHER_ID`.
    *   `DRV_TRFM - DATES AND DIM`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `COST_PERIOD_ID` to string).
*   **Destination:** `OLEDB_SRC - D_PRM_COST_PERIOD` inserts data into `dbo.D_PRM_COST_PERIOD` in the `ARD_REPORTING` database.

#### DFT - D_PRM_CURRENCY

*   **Source:** `OLEDB_SRC - PRM_CURRENCY_TYPE` extracts data from `dbo.PRM_CURRENCY_TYPE` in the `DATA_HUB` database.
*   **Transformations:**
    *   `DRV_TRFM - DIM & DATES`: Creates `DIM_ID` (converting `CURRENCY_ID` to string), `ETL_CREA_DT`, and `ETL_UPDT_DT` (using `GETDATE()`).
*   **Destination:** `OLEDB_DEST - D_PRM_CURRENCY` inserts data into `dbo.D_PRM_CURRENCY` in the `ARD_REPORTING` database.

#### DFT - D_PRM_FORECAST_TYPE

*   **Source:** `OLEDB_SRC - PRM_FORECAST_TYPE` extracts data from `dbo.PRM_FORECAST_TYPE` in the `DATA_HUB` database.
*   **Transformations:**
    *   `DRV_TRFM - DIM & DATES`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `FORECAST_TYPE_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_FORECAST_TYPE` inserts data into `dbo.D_PRM_FORECAST_TYPE` in the `ARD_REPORTING` database.

#### DFT - D_PRM_LEASE

*   **Source:** `OLEDB_SRC - PRM_LEASE` extracts data from `dbo.PRM_LEASE` in the `DATA_HUB` database.
*   **Transformations:**
    *   Numerous `Lookup` transformations to retrieve English and French descriptions from various dimension tables:  `PRM_ARLU_RENT_REVISION_TYPE`, `PRM_BASE_RENT_REVISION_TYPE`, `PRM_COST_REVISION_TYPE_1`, `PRM_COST_REVISION_TYPE_2`, `PRM_CURRENCY_TYPE`, `PRM_DEPOSIT_TYPE`, `PRM_LEASE_TYPE`, and `PRM_NOTICE_TYPE`.
    *   `DRV_TRFM - DATES AND DIM`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), `DIM_ID` (converting `LEASE_ID` to string),  `RENEWAL_CLAUSE_IND_EN`, `RENEWAL_CLAUSE_IND_FR`, `DRV_NO_OF_RENEWAL_TERM_EN`, `DRV_NO_OF_RENEWAL_TERM_FR`, `DRV_LEASE_TERM_EN`, `DRV_LEASE_TERM_FR`, `EARLY_TERMINATION_CLAUSE_IND_EN`, `EARLY_TERMINATION_CLAUSE_IND_FR`, `DIPLOMATIC_CLAUSE_IND_EN`, `DIPLOMATIC_CLAUSE_IND_FR`, `PURCHASE_OPTION_IND_EN`, `PURCHASE_OPTION_IND_FR`, `RESTORATION_CLAUSE_IND_EN`, `RESTORATION_CLAUSE_IND_FR`, `EXPANSION_CLAUSE_IND_EN`, `EXPANSION_CLAUSE_IND_FR`, `COMPRESSION_CLAUSE_IND_EN`, `COMPRESSION_CLAUSE_IND_FR`, `AUTO_RENEWAL_CLAUSE_IND_EN`, `AUTO_RENEWAL_CLAUSE_IND_FR`
*   **Destination:** `OLEDB_DEST - D_PRM_LEASE` inserts data into `dbo.D_PRM_LEASE` in the `ARD_REPORTING` database.

#### DFT - D_PRM_MISSION

*   **Source:** `OLEDB_SRC - PRM_MISSION` extracts data from `dbo.PRM_MISSION` in the `DATA_HUB` database.
*   **Transformations:**
    *   `DRV_TRFM - DATA TYPE CONVERSION`: Converts `MISSION_CATEGORY_ID` to `DT_I4` (integer).
    *   Numerous `Lookup` transformations to retrieve related data: `PRM_AMA`, `PRM_CITY`, `PRM_COUNTRY`, `PRM_GEO_REGION`, `PRM_MISSION - PARENT`, `PRM_MISSION_CATEGORY`, `PRM_MISSION_STATUS`, `PRM_TL3`, `SRSF_AREA`, `SRSF_AREA_REGION`, `SRSF_RMO`
    *   `DRV_TRFM - DATES AND DIM_ID`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `MISSION_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_MISSION` inserts data into `dbo.D_PRM_MISSION` in the `ARD_REPORTING` database.

#### DFT - D_PRM_OCCUPANT

*   **Source:** `OLEDB_SRC - PRM_OCCUPANT` extracts data from `dbo.PRM_OCCUPANT` in the `DATA_HUB` database.
*   **Transformations:**
    *   `LKP_PRM_TITLE`: Lookup to retrieve `CATEGORY_TYPE_ID` from `PRM_TITLE`.
    *   `DRV_FO&OF_YEN_ID`: Derives `DRV_FAMILY_OPTION_ID` and `DRV_OTHER_FACTOR_ID` based on `CATEGORY_TYPE_ID`,  `FAMILY_OPTION_IND`, and `OTHER_FACTOR_IND`.
    *   `LKP_PRM_YES_NO_NA - FAMILY OPTION`: Lookup to retrieve `DRV_FAMILY_OPTION_EN` and `DRV_FAMILY_OPTION_FR` based on `DRV_FAMILY_OPTION_ID`.
    *   `LKP_PRM_YES_NO_NA - OTHER FACTORS`: Lookup to retrieve `DRV_OTHER_FACTOR_EN` and `DRV_OTHER_FACTOR_FR` based on `DRV_OTHER_FACTOR_ID`.
    *   `DRV_TRFM - DATES AND DIM`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `OCCUPANT_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_OCCUPANT` inserts data into `dbo.D_PRM_OCCUPANT` in the `ARD_REPORTING` database.

#### DFT - D_PRM_RENT_TYPE

*   **Sources:**
    *   `OLEDB_SRC - BASE` extracts data from a static SQL query in the `ARD_PRIME_SOURCE` database.
    *   `OLEDB_SRC - OTHER` extracts data from a static SQL query in the `ARD_PRIME_SOURCE` database.
*   **Transformations:**
    *   `Union All`: Combines the output from the two sources.
    *   `DRV_TRFM - DATES AND DIM`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `RENT_TYPE_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_RENT_TYPE` inserts data into `dbo.D_PRM_RENT_TYPE` in the `ARD_REPORTING` database.

#### DFT - D_PRM_SPACE_THRESHOLD

*   **Source:** `OLEDB_SRC - PRM_SPACE_THRESHOLD_BY_FY` extracts data from `dbo.PRM_SPACE_THRESHOLD_BY_FY` in the `DATA_HUB` database.
*   **Transformations:**
    *   `DRV_TRFM - DATES`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `SPACE_THRESHOLD_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_SPACE_THRESHOLD` inserts data into `dbo.D_PRM_SPACE_THRESHOLD` in the `ARD_REPORTING` database.

#### DFT - D_PRM_STRUCTURE_CONDITION

*   **Source:** `OLEDB_SRC - PRM_STRUCTURE_CONDITION_BY_FY` extracts data from `dbo.PRM_STRUCTURE_CONDITION_BY_FY` in the `DATA_HUB` database.
*   **Transformations:**
    *   `LKP - PRM_STRUCTURE_CONDITION_TYPE`: Lookup to retrieve descriptions from `dbo.PRM_STRUCTURE_CONDITION_TYPE`.
    *   `DRV_TRFM - DIM & DATES`: Creates `ETL_CREA_DT`, `ETL_UPDT_DT` (using `GETDATE()`), and `DIM_ID` (converting `STRUCTURE_CONDITION_ID` to string).
*   **Destination:** `OLEDB_DEST - D_PRM_STRUCTURE_CONDITION` inserts data into `dbo.D_PRM_STRUCTURE_CONDITION` in the `ARD_REPORTING` database.

#### DFT - INSERT UNKNOWN MEMBERS

*   Multiple `OLEDB_SRC` components act as sources, each returning a single row for the unknown member.
*   Multiple `Derived Column` components add `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
*   `OLEDB_DEST` components then insert these rows into the respective dimension tables.

## 4. Code Extraction

```sql
SELECT [CURRENCY_TYPE_ID] AS [CURRENCY_BASE_ID]
      ,[CURRENCY_TYPE_CD] AS [CURRENCY_BASE_CD]
      ,[CURRENCY_TYPE_EN_NM] AS [CURRENCY_BASE_EN_NM]
      ,[CURRENCY_TYPE_FR_NM] AS [CURRENCY_BASE_FR_NM]   
  FROM [dbo].[PRM_CURRENCY_TYPE]
```

SQL Query from `LKP - PRM_CURRENCY_TYPE - BASE`

```sql
select * from (SELECT [CURRENCY_TYPE_ID] AS [CURRENCY_BASE_ID]
      ,[CURRENCY_TYPE_CD] AS [CURRENCY_BASE_CD]
      ,[CURRENCY_TYPE_EN_NM] AS [CURRENCY_BASE_EN_NM]
      ,[CURRENCY_TYPE_FR_NM] AS [CURRENCY_BASE_FR_NM]   
  FROM [dbo].[PRM_CURRENCY_TYPE]) [refTable]
where [refTable].[CURRENCY_BASE_ID] = ?
```

SQL Parameterized Query from `LKP - PRM_CURRENCY_TYPE - BASE`

```sql
SELECT [CURRENCY_TYPE_ID] AS [CURRENCY_OTHER_ID]
      ,[CURRENCY_TYPE_CD] AS [CURRENCY_OTHER_CD]
      ,[CURRENCY_TYPE_EN_NM] AS [CURRENCY_OTHER_EN_NM]
      ,[CURRENCY_TYPE_FR_NM] AS [CURRENCY_OTHER_FR_NM]
  FROM [dbo].[PRM_CURRENCY_TYPE]
```

SQL Query from `LKP - PRM_CURRENCY_TYPE - OTHER`

```sql
select * from (SELECT [CURRENCY_TYPE_ID] AS [CURRENCY_OTHER_ID]
      ,[CURRENCY_TYPE_CD] AS [CURRENCY_OTHER_CD]
      ,[CURRENCY_TYPE_EN_NM] AS [CURRENCY_OTHER_EN_NM]
      ,[CURRENCY_TYPE_FR_NM] AS [CURRENCY_OTHER_FR_NM]
  FROM [dbo].[PRM_CURRENCY_TYPE]) [refTable]
where [refTable].[CURRENCY_OTHER_ID] = ?
```

SQL Parameterized Query from `LKP - PRM_CURRENCY_TYPE - OTHER`

```sql
SELECT  
COST_PERIOD_ID
, COST_PERIOD_START_DTM AS COST_START_DT
, COST_PERIOD_END_DTM AS COST_END_DT
      ,[COST_PERIOD_CURRENCY_TYPE_ID] AS [CURRENCY_BASE_ID]
      ,[COST_PERIOD_CURRENCY_TYPE_2_ID] AS [CURRENCY_OTHER_ID]


, COST_PERIOD_LAST_UPDATED_DTM AS LAST_UPDATED_DT
, COST_PERIOD_UPDATED_BY_USER_NM AS UPDATED_BY_ID
FROM dbo.PRM_COST_PERIOD
```

SQL query from `OLEDB_SRC - PRM_COST_PERIOD`

```sql
SELECT [CURRENCY_TYPE_ID] AS [CURRENCY_ID]
      ,[CURRENCY_TYPE_CD] AS [CURRENCY_CD]
      ,[CURRENCY_TYPE_EN_NM] AS [CURRENCY_EN_NM]
      ,[CURRENCY_TYPE_FR_NM] AS [CURRENCY_FR_NM]
      ,[CURRENCY_TYPE_ACTIVE_IND] AS [CURRENCY_ACTIVE_IND]
  FROM [dbo].[PRM_CURRENCY_TYPE]
```

SQL query from `OLEDB_SRC - PRM_CURRENCY_TYPE`

```sql
SELECT [FORECAST_TYPE_ID] AS [FORECAST_TYPE_ID]
      ,[FORECAST_TYPE_ACTIVE_IND] AS [FORECAST_TYPE_ACTIVE_IND]
      ,[FORECAST_TYPE_RO_TXT] AS [FORECAST_TYPE_RO]
      ,[FORECAST_TYPE_EN_DESCR] AS [FORECAST_TYPE_EN_NM]
      ,[FORECAST_TYPE_FR_DESCR] AS [FORECAST_TYPE_FR_NM]
FROM [dbo].[PRM_FORECAST_TYPE]
```

SQL query from `OLEDB_SRC - PRM_FORECAST_TYPE`

```sql
SELECT [LEASE_ID]
      ,[LEASE_START_DTM] AS [LEASE_START_DT]
      ,[LEASE_END_DTM] AS [LEASE_END_DT]
      ,[LEASE_NOTICE_DTM] AS [NOTICE_DT]
	  ,[LEASE_EARLY_TERMINATION_DTM] AS [EARLY_TERMINATION_DT]
	  ,[LEASE_FIRST_PAYMENT_DUE_BASE_DTM] AS [FIRST_PAYMENT_DUE_BASE_DT]
      ,[LEASE_FIRST_PAYMENT_DUE_OTHER_DTM] AS [FIRST_PAYMENT_DUE_OTHER_DT]
	  ,[LEASE_RENEWAL_TERM_NBR] AS [RENEWAL_TERM]
      ,[LEASE_TERMS_NBR] AS [LEASE_NO_TERMS]
      ,[LEASE_TERM_NBR] AS [LEASE_TERM]
	  ,[LEASE_RENEWAL_CLAUSE] AS [RENEWAL_CLAUSE_IND]
      ,[LEASE_AUTOMATIC_RENEWAL] AS [AUTOMATIC_RENEWAL_IND]
      ,[LEASE_DIPLOMATIC_CLAUSE] AS [DIPLOMATIC_CLAUSE_IND]
      ,[LEASE_PURCHASE_OPTION] AS [PURCHASE_OPTION_IND]
      ,[LEASE_RESTORATION_CLAUSE] AS [RESTORATION_CLAUSE_IND]
      ,[LEASE_EXPANSION_CLAUSE] AS [EXPANSION_CLAUSE_IND]
 ,[LEASE_AUTO_RENEWAL_CLAUSE] AS [AUTO_RENEWAL_CLAUSE_IND]
      ,[LEASE_COMPRESSION_CLAUSE] AS [COMPRESSION_CLAUSE_IND]
      ,[LEASE_RECEIVED_BY_HQ] AS [RECEIVED_BY_HQ_IND]
      ,[LEASE_HQ_VERIFIED] AS [HQ_VERIFIED_IND]
      ,[LEASE_EARLY_TERMINATION_CLAUSE] AS [EARLY_TERMINATION_CLAUSE_IND]
      ,[LEASE_TERMINATED_EARLY] AS [TERMINATED_EARLY_IND]
      ,[LEASE_INDEFINITE_IND] AS [INDEFINITE_IND]
      ,[LEASE_BCR_FREQUENCY_NBR] AS  [BCR_FREQUENCY]	  
	  ,[LEASE_BCR_FIRST_DTM] AS [BCR_FIRST_DT]
      ,[LEASE_OCR_FREQUENCY_NBR] AS [OCR_FREQUENCY]
      ,[LEASE_OCR_FIRST_DTM] AS [OCR_FIRST_DT]
      ,[LEASE_NOTES_TXT] AS [LEASE_NOTE_TXT]
      ,[LEASE_TERM_NOTES_TXT] AS [TERM_NOTE_TXT]
      ,[LEASE_TYPE_ID]
      ,[LEASE_BASE_RENT_REVISION_TYPE_ID] AS [BASE_RENT_REVISION_TYPE_ID]
      ,[LEASE_NOTICE_TYPE_ID] AS [NOTICE_TYPE_ID]
	  ,[LEASE_BASE_PAYMENT_SCHEDULE_TYPE_ID] AS [PAYMENT_SCHEDULE_BASE_TYPE_ID]
      ,[LEASE_OTHER_PAYMENT_SCHEDULE_TYPE_ID] AS [PAYMENT_SCHEDULE_OTHER_TYPE_ID]
      ,[LEASE_COST_REVISION_TYPE_ID] AS [COST_REVISION_TYPE_1_ID]
      ,[LEASE_COST_REVISION_TYPE2_ID] AS [COST_REVISION_TYPE_2_ID]
	  ,[LEASE_ARLU_RENT_REVISION_TYPE_ID] AS [ARLU_RENT_REVISION_TYPE_ID]
	  ,[LEASE_DEPOSIT_TYPE_ID] AS [DEPOSIT_TYPE_ID]
	  ,[LEASE_LAST_UPDATED_DTM] AS [LAST_UPDATED_DT]
      ,[LEASE_UPDATED_BY_USER_NM] AS [UPDATED_BY_ID]
,[LEASE_CURRENCY_TYPE_ID] AS [CURRENCY_DEPOSIT_ID]	
, Term_year = case 
			when (case 
		when datediff(day, dateadd(year,case when MONTH(LEASE_START_DTM) &gt; MONTH(LEASE_END_DTM) then datediff(year, LEASE_START_DTM, LEASE_END_DTM) - 1 else datediff(year, LEASE_START_DTM, LEASE_END_DTM) end, LEASE_START_DTM), LEASE_END_DTM) &gt; 15
		then datediff(month, dateadd(year
					,case when MONTH(LEASE_START_DTM) &gt; MONTH(LEASE_END_DTM) then datediff(year, LEASE_START_DTM, LEASE_END_DTM) - 1 else datediff(year, LEASE_START_DTM, LEASE_END_DTM) end, LEASE_START_DTM)
					,LEA