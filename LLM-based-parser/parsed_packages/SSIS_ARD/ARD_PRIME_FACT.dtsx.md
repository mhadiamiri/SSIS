```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package             | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|------------------------------------|-----------------------|-----------------------|-------------|
| ARD_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred] | Lookup data and destination | SQL Server Auth likely            |  @[$Project::PRJ_PRM_DIM_UNKNOWN_MEMBER_SID]           | Part 1, 2, 3 |
| ARD_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for fact tables             | SQL Server Auth likely            |  @[$Project::PRJ_PRM_DIM_UNKNOWN_MEMBER_SID]           | Part 1, 2, 3 |
| DATA_HUB           | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for fact tables             | SQL Server Auth likely            |  None           | Part 1, 2, 3 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `ARD_PRIME_FACT.dtsx` has a control flow that consists of a sequence container named `SEQC-LOAD FACT TABLES`, preceded by an expression task.

*   **Expression Task:** `EXPRESSIONT- Fact Tables - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` - This task contains a simple expression `1 == 1` and likely serves as a starting point or a placeholder.

*   **Sequence Container:** `SEQC-LOAD FACT TABLES` - This container encapsulates multiple data flow tasks, each responsible for loading a specific fact table.

#### DFT - F_PRM_FORECAST

*   **Source:** `OLEDB_SRC - PRM_FORECAST_DETAIL` extracts data from `dbo.PRM_FORECAST_DETAIL` with a `WHERE` clause excluding certain `forecast_detail_id` values.
*   **Transformations:**
    *   `UPVT - 5-YEAR AMT`: Unpivots `FY1_FORECAST_AMT` through `FY5_FORECAST_AMT` into a single `FORECAST_AMT` column, with `FISCAL_YEAR_SEQUENCE_NBR` indicating the year.
    *   `LKP - PRM_FORECAST_DETAIL_LKP`:  Looks up dimension keys based on `FORECAST_DETAIL_ID` from `dbo.PRM_FORECAST_DETAIL_LKP`
    *   `LKP - D_PRM_PROPERTY`: Looks up `PROPERTY_SID` from `dbo.D_PRM_PROPERTY` based on `PROPERTY_ID`.
    *   `LKP - D_PRM_MISSION`: Looks up `MISSION_SID` from `dbo.D_PRM_MISSION` based on `MISSION_ID`.
    *   `LKP - D_PRM_FORECAST_TYPE`: Looks up `FORECAST_TYPE_SID` from `dbo.D_PRM_FORECAST_TYPE` based on `FORECAST_TYPE_ID`.
    *   `LKP - D_PRM_CURRENCY`: Looks up `CURRENCY_SID` from `dbo.D_PRM_CURRENCY` based on `CURRENCY_ID`.
    *   `LKP - D_PRM_FACILITY_TYPE`: Looks up `FACILITY_TYPE_SID` from `dbo.D_PRM_FACILITY_TYPE` based on `FACILITY_TYPE_ID`.
    *   `LKP - D_PRM_TITLE`: Looks up `TITLE_SID` from `dbo.D_PRM_TITLE` based on `TITLE_ID`.
    *    `LKP - D_OPRA_DATE`: Looks up `START_FISCAL_YEAR_SID` based on `FISCAL_YEAR_ID`
    *  `DRV_TRFM - DATES & OTHER DERIVED`: Derives `ETL_CREA_DT`, `ETL_UPDT_DT` using `GETDATE()` and calculates `FISCAL_YEAR_SID` based on `START_FISCAL_YEAR_SID` and  `FISCAL_YEAR_SEQUENCE_NBR`.
    *  `DRV_TRFM - Uncoded`: Replaces Null values in Dimension SID with @[$Project::PRJ_PRM_DIM_UNKNOWN_MEMBER_SID]
*   **Destination:** `OLEDB_DEST - F_PRM_FORECAST` loads processed data into the `dbo.F_PRM_FORECAST` table.

#### DFT - F_PRM_LEASE_COSTING

*   **Sources:**
    *   `OLEDB_SRC - PRM_ACCOMMODATION` extracts `ACCOMMODATION_ID` and `ACCOMMODATION_TITLE_ID` from `dbo.PRM_ACCOMMODATION`.
    *   `OLEDB_SRC - PRM_LEASE` extracts `LEASE_ID`, `LEASE_TITLE_ID`, and `LEASE_DEPOSIT_AMT` from `dbo.PRM_LEASE`.
    *   `OLEDB_SRC - PRM_COST_PERIOD` extracts cost period details from `dbo.PRM_COST_PERIOD`.
    *  `OLEDB_SRC - PRM_LEASE_COSTING_LKP - NO CURRENT LEASE`: Extracts data from `dbo.PRM_LEASE_COSTING_LKP`
    *  `OLEDB_SRC - PRM_LEASE_COSTING_LKP - NO CURRENT CP`: Extracts data from `dbo.PRM_LEASE_COSTING_LKP`
*   **Transformations:**
    *   `MRG_JON - TITLE_ID`: merge join two source table `OLEDB_SRC - PRM_ACCOMMODATION` and `OLEDB_SRC - PRM_LEASE` on `TITLE_ID`.
    *  `DRV_TRFM - DATE_BK`: Derives  date surrogate keys `LEASE_END_DT_BK`,  `COST_PERIOD_START_DT_BK`, etc.
    *   Several Lookups join data from:  `DBO.D_PRM_TITLE`, `DBO.D_PRM_LEASE`,  `DBO.D_PRM_MISSION`, `DBO.D_PRM_CURRENCY`, `DBO.D_OPRA_DATE` etc.
    *   `Union All`: Combines rows from the multiple data flows
    *   `DRV_TRFM - DATES_COUNTS_OTHERS`: Derives `ETL_CREA_DT`, `ETL_UPDT_DT` using `GETDATE()`, calculates `COST_PERIOD_CNT` and `DRV_GROSS_RENT_AMD`.
*   **Destinations:** `OLEDB_DEST - F_PRM_LEASE_COSTING` loads processed data into the `dbo.F_PRM_LEASE_COSTING` table.

#### DFT - F_PRM_OCCUPANCY

*   **Sources:**
    *   `OLEDB_SRC - PRM_ACCOMMODATION` extracts `ACCOMMODATION_ID` and `ACCOMMODATION_TITLE_ID` from `dbo.PRM_ACCOMMODATION`.
    *   `OLEDB_SRC - PRM_OCCUPANT` extracts occupant details from `dbo.PRM_OCCUPANT`.
    * `OLEDB_SRC - PRM_LEASE_COSTING_LKP - NO CURRENT CP`: Extracts data from `dbo.PRM_LEASE_COSTING_LKP`
    * `OLEDB_SRC - PRM_LEASE_COSTING_LKP - NO CURRENT LEASE`: Extracts data from `dbo.PRM_LEASE_COSTING_LKP`
*   **Transformations:**
    *   `MRG - PROPERTY AND OCCUPANT`: merge join two source table `PRM_ACCOMMODATION` and `PRM_OCCUPANT` on `ACCOMMODATION_ID`.
    *   Several Lookups join data from: `dbo.D_PRM_TITLE`, `dbo.D_PRM_MISSION`, `dbo.D_PRM_FACILITY_TYPE`, etc.
    *   `DRV_TRFM - DATE_BK`: Derives  date surrogate keys `LEASE_END_DT_BK`,  `COST_PERIOD_START_DT_BK`, etc.
    *   `Union All`: Combines rows from the multiple data flows
    *   `DRV_TRFM - DATES AND UNCODED`: Derives `ETL_CREA_DT`, `ETL_UPDT_DT` using `GETDATE()`, calculates `COST_PERIOD_CNT` and `DRV_GROSS_RENT_AMD`.
*   **Destinations:** `OLEDB_DEST - F_PRM_OCCUPANCY` loads processed data into the `dbo.F_PRM_OCCUPANCY` table.

#### DFT - F_PRM_PROPERTY

*   **Source:** `OLEDB_SRC - PRM_ACCOMMODATION` extracts data from `dbo.PRM_ACCOMMODATION`.
*   **Transformations:**
    *   Several Lookups join data from:  `DBO.D_PRM_TITLE`, `DBO.D_PRM_LEASE`,  `DBO.D_PRM_MISSION`, `DBO.D_OPRA_DATE` etc.
    *   `DRV_TRFM - DATE_BK`: Derives  date surrogate keys `LEASE_END_DT_BK`,  `COST_PERIOD_START_DT_BK`, etc.
    *   `DRV_TRFM - DATES AND UNCODED`: sets a property count, and adds current dates for ETL.
*   **Destination:** `OLEDB_DEST - F_PRM_PROPERTY` loads processed data into the `dbo.F_PRM_PROPERTY` table.

#### DFT - F_PRM_RENT_COSTING

*   **Sources:**
    *  `OLEDB_SRC - PRM_RENT_COSTING_LKP`: Extracts data from `dbo.PRM_RENT_COSTING_LKP`
    *  `OLEDB_SRC - D_OPRA_DATE - FY LIST`: Extracts data from `dbo.D_OPRA_DATE`
*   **Transformations:**
    *   `Merge Join`: merge two source table `OLEDB_SRC - PRM_RENT_COSTING_LKP - DUMMY` and `OLEDB_SRC - D_OPRA_DATE - FY LIST` on `RENT_TYPE_ID` for the output.
    *  `DRV_TRFM - DATE_BK`: Derives  date surrogate keys `MONTH_START_DT_BK`.
    *   Several Lookups join data from:  `DBO.D_PRM_RENT_TYPE`, `DBO.D_PRM_CURRENCY` etc.

*   **Destination:** `OLEDB_DEST - F_PRM_RENT_COSTING` loads processed data into the `dbo.F_PRM_RENT_COSTING` table.

#### DFT - F_PRM_SPACE_THRESHOLD

*   **Source:** `OLEDB_SRC - PRM_SPACE_THRESHOLD_BY_FY` extracts data from `dbo.PRM_SPACE_THRESHOLD_BY_FY`.
*   **Transformations:**
    *  Several Lookups join data from:  `DBO.D_OPRA_DATE`, `DBO.PRM_SPACE_THRESHOLD_LKP` etc.
        *`LKP - D_OPRA_DATE`: extracts data for `FISCAL_YEAR_SID` from the table `dbo.D_OPRA_DATE`
    *   `DRV_TRFM - DATES AND UNCODED`: calculates `ETL_CREA_DT`, `ETL_UPDT_DT` and`SPACE_THRESHOLD_CNT`.
*   **Destination:** `OLEDB_DEST - F_PRM_SPACE_THRESHOLD` loads processed data into the `dbo.F_PRM_SPACE_THRESHOLD` table.

#### DFT - F_PRM_STRUCTURE_CONDITION

*   **Source:** `OLEDB_SRC - PRM_STRUCTURE_CONDITION_BY_FY` extracts data from `dbo.PRM_STRUCTURE_CONDITION_BY_FY`.
*   **Transformations:**
    *  Several Lookups join data from: `dbo.D_PRM_MISSION`, `dbo.D_PRM_FACILITY_TYPE` etc.
    *   `DRV_TRFM - DATE_BK`: Derives  date surrogate keys `FISCAL_DT_BK`.
    *   `DRV_TRFM - DATES AND UNCODED`: calculates`ETL_CREA_DT`, `ETL_UPDT_DT` and`STRUCTURE_CONDITION_CNT`.
*   **Destination:** `OLEDB_DEST - F_PRM_STRUCTURE_CONDITION` loads processed data into the `dbo.F_PRM_STRUCTURE_CONDITION` table.

#### DFT - PRM_CDC_Changes

*   **Source:** `OLEDB_SRC - CDC_Changes` extracts data from `dbo.CDC_Changes`.
*   **Transformations:**
       *   `DRV_TRFM - ETL_DATES`: calculates`ETL_CREA_DT`and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST - PRM_CDC_Changes` loads processed data into the `dbo.PRM_CDC_Changes` table.

#### ESQLT- TRUNCATE ALL FACT TABLES

* Tasks truncates all the fact tables: `dbo.F_PRM_STRUCTURE_CONDITION`,`dbo.F_PRM_SPACE_THRESHOLD`,`dbo.F_PRM_FORECAST`,`dbo.F_PRM_PROPERTY`,`dbo.F_PRM_OCCUPANCY`,`dbo.F_PRM_LEASE_COSTING`,`dbo.F_PRM_RENT_COSTING`,`[dbo].[PRM_CDC_Changes]`.

## 4. Code Extraction

```sql
SELECT [DATE_SID] AS [START_FISCAL_YEAR_SID]       
,[DATE_ID]
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL Query for LKP - D_OPRA_DATE

```sql
SELECT
  [DATE_SID] AS [START_FISCAL_YEAR_SID]
  ,
  [DATE_ID]
FROM
  [dbo].[D_OPRA_DATE]
```

Context: SqlCommand for LKP - D_OPRA_DATE lookup table.

```sql
SELECT [CURRENCY_SID]
      ,[CURRENCY_ID]     
FROM [dbo].[D_PRM_CURRENCY]
```

Context: SqlCommand for LKP - D_PRM_CURRENCY lookup table.

```sql
SELECT [FACILITY_TYPE_SID]
      ,[FACILITY_TYPE_ID]     
FROM [dbo].[D_PRM_FACILITY_TYPE]
```

Context: SqlCommand for LKP - D_PRM_FACILITY_TYPE lookup table.

```sql
SELECT [FORECAST_TYPE_SID]
      ,[FORECAST_TYPE_ID]
FROM [dbo].[D_PRM_FORECAST_TYPE]
```

Context: SqlCommand for LKP - D_PRM_FORECAST_TYPE lookup table.

```sql
SELECT [MISSION_SID]
      ,[MISSION_ID]
FROM [dbo].[D_PRM_MISSION]
```

Context: SqlCommand for LKP - D_PRM_MISSION lookup table.

```sql
SELECT [PROPERTY_SID]
      ,[ACCOMMODATION_ID]
FROM [dbo].[D_PRM_PROPERTY]
```

Context: SqlCommand for LKP - D_PRM_PROPERTY lookup table.

```sql
SELECT [TITLE_SID]
      ,[TITLE_ID]
FROM [dbo].[D_PRM_TITLE]
```

Context: SqlCommand for LKP - D_PRM_TITLE lookup table.

```sql
SELECT [FORECAST_DETAIL_ID]
      
--,[ACCOMMODATION_FORECAST_ID]
      
,[CURRENCY_ID]
      
,[FORECAST_TYPE_ID]
      
,[FISCAL_YEAR_ID]
   
,[PROPERTY_ID]
      ,[MISSION_ID]
      ,[TITLE_ID]
      ,[FACILITY_TYPE_ID]
  
FROM [dbo].[PRM_FORECAST_DETAIL_LKP]
```

Context: SqlCommand for LKP - PRM_FORECAST_DETAIL_LKP lookup table.

```sql
SELECT [FORECAST_DETAIL_ID]      
      ,coalesce([FORECAST_DETAIL_YEAR1_AMT],0) AS [FY1_FORECAST_AMT]
      ,coalesce([FORECAST_DETAIL_YEAR2_AMT],0) AS [FY2_FORECAST_AMT]
      ,coalesce([FORECAST_DETAIL_YEAR3_AMT],0) AS [FY3_FORECAST_AMT]
      ,coalesce([FORECAST_DETAIL_YEAR4_AMT],0) AS [FY4_FORECAST_AMT]
      ,coalesce([FORECAST_DETAIL_YEAR5_AMT],0) AS [FY5_FORECAST_AMT]
  FROM [dbo].[PRM_FORECAST_DETAIL]

where forecast_detail_id NOT IN (
306857
,306858
,306859
,306860
,306861) -- entered wrong year format
```

Context: Sql query for OLEDB_SRC - PRM_FORECAST_DETAIL

```sql
SELECT [DATE_SID]  AS [COST_PERIOD_END_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - COST_PERIOD_END

```sql
SELECT [DATE_SID]  AS [LEASE_END_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_END

```sql
SELECT [DATE_SID]  AS [LEASE_NOTICE_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_NOTICE

```sql
SELECT [DATE_SID]  AS [LEASE_START_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_START

```sql
select 1 as date_max_min_key
,max(DATE_ID) as Max_Date_Dim
, min(DATE_ID) as Min_Date_Dim
           
from [dbo].[D_OPRA_DATE]
	       where [DATE_SID] >0
```

Context: SQL query for LKP - D_OPRA_DATE - MIN&MAX

```sql
SELECT 
COST_PERIOD_ID
, COST_PERIOD_SID
FROM DBO.D_PRM_COST_PERIOD
```

Context: SQL query for LKP - D_PRM_COST_PERIOD

```sql
SELECT CURRENCY_ID
, CURRENCY_SID AS CURRENCY_BASE_SID
      
  FROM [dbo].[D_PRM_CURRENCY]
```

Context: SQL query for LKP - D_PRM_CURRENCY - BASE

```sql
SELECT CURRENCY_ID
, CURRENCY_SID AS CURRENCY_DEPOSIT_SID
      
  FROM [dbo].[D_PRM_CURRENCY]
```

Context: SQL query for LKP - D_PRM_CURRENCY - DEPOSIT

```sql
SELECT CURRENCY_ID
, CURRENCY_SID AS CURRENCY_OTHER_SID
      
  FROM [dbo].[D_PRM_CURRENCY]
```

Context: SQL query for LKP - D_PRM_CURRENCY - OTHER

```sql
select ACCOMMODATION_ID, 
ACCOMMODATION_TITLE_ID,
1 AS date_max_min_key
 from PRM_ACCOMMODATION
--where accommodation_id = 7794
ORDER by ACCOMMODATION_TITLE_ID
```

Context: SQL query for OLEDB_SRC - PRM_ACCOMMODATION

```sql
SELECT [LEASE_ID]
     
      ,[LEASE_TITLE_ID]
,LEASE_DEPOSIT_AMT
     
  FROM [dbo].[PRM_LEASE]

--where lease_id = 19289


  ORDER BY [LEASE_TITLE_ID]
```

Context: SQL query for OLEDB_SRC - PRM_LEASE

```sql
SELECT [COST_PERIOD_ID]
     
      ,[COST_PERIOD_BASE_RENT_AMT]
      ,[COST_PERIOD_OTHER_RENT_AMT]
      ,[COST_PERIOD_LEASE_ID]
      ,[COST_PERIOD_ANNUAL_BASE_AMT]
      ,[COST_PERIOD_ANNUAL_OTHER_AMT]
     ,[COST_PERIOD_EQUIV_BASE]
      ,[COST_PERIOD_EQUIV_OTHER]
     FROM [dbo].[PRM_COST_PERIOD]
	 ORDER BY [COST_PERIOD_LEASE_ID]
```

Context: SQL query for OLEDB_SRC - PRM_COST_PERIOD

```sql
select 
DISTINCT lc.ACCOMMODATION_ID
, lea_c.LEASE_ID
, NULL AS COST_PERIOD_ID
--, NULL AS COST_PERIOD_BASE_RENT_AMT
--, NULL AS COST_PERIOD_OTHER_RENT_AMT
--, NULL AS COST_PERIOD_LEASE_ID
--, NULL AS COST_PERIOD_ANNUAL_BASE_RENT_AMT
--, NULL AS COST_PERIOD_ANNUAL_OTHER_RENT_AMT
, 1 AS date_max_min_key
--, NULL AS LEASE_DEPOSIT_AMT
--, NULL AS COST_PERIOD_EQUIV_BASE
--, NULL AS COST_PERIOD_EQUIV_OTHER
, lc.TITLE_ID
, lc.FACILITY_TYPE_ID
, lc.MISSION_ID
, lea_c.LEASE_DEPOSIT_CURRENCY_ID
--, NULL AS COST_PERIOD_START_DT_ID
--, NULL AS COST_PERIOD_END_DT_ID
, lea_c.LEASE_START_DT_ID
, lea_c.LEASE_END_DT_ID
, lea_c.LEASE_NOTICE_DT_ID
, lea_c.CURRENT_LEASE_IND
, 0 AS [CURRENT_COST_PERIOD_IND]
, coalesce(lea_c.DRV_PRID_FIRST_LEASE_IND,0) as DRV_PRID_FIRST_LEASE_IND
, 1 AS MANUAL_ADDED
--, NULL AS [base_rate]
--, NULL AS [other_rate]
, NULL AS BASE_RENT_CURRENCY_ID
, NULL AS OTHER_RENT_CURRENCY_ID

from dbo.PRM_LEASE_COSTING_LKP lc

inner join dbo.PRM_LEASE_COSTING_LKP lea_c
on lc.ACCOMMODATION_ID = lea_c.ACCOMMODATION_ID
and lc.LEASE_ID = lea_c.LEASE_ID
and lea_c.CURRENT_LEASE_IND = 1

WHERE
--ACCOMMODATION_ID = 1636 and
 (COALESCE(lc.CURRENT_COST_PERIOD_IND, 0) = 0 AND lc.COST_PERIOD_ID IS NOT NULL)

AND lc.ACCOMMODATION_ID NOT IN (select distinct ACCOMMODATION_ID from dbo.PRM_LEASE_COSTING_LKP 
WHERE CURRENT_LEASE_IND =1 AND CURRENT_COST_PERIOD_IND = 1)
/*
AND ACCOMMODATION_ID NOT IN (select distinct ACCOMMODATION_ID from dbo.PRM_LEASE_COSTING_LKP 
WHERE COST_PERIOD_ID IS NULL)


AND ACCOMMODATION_ID NOT IN (select distinct ACCOMMODATION_ID from dbo.PRM_LEASE_COSTING_LKP 
WHERE (COALESCE(CURRENT_LEASE_IND, 0) = 0 AND LEASE_ID IS NOT NULL)

AND ACCOMMODATION_ID NOT IN (select distinct ACCOMMODATION_ID from dbo.PRM_LEASE_COSTING_LKP 
WHERE CURRENT_LEASE_IND =1 AND CURRENT_COST_PERIOD_IND = 1)

AND ACCOMMODATION_ID NOT IN (select distinct ACCOMMODATION_ID from dbo.PRM_LEASE_COSTING_LKP 
WHERE LEASE_ID IS NULL))
*/
```

Context: SQL query for OLEDB_SRC - PRM_LEASE_COSTING_LKP - NO CURRENT CP

```sql
select 1 as date_max_min_key
,max(DATE_ID) as Max_Date_Dim
, min(DATE_ID) as Min_Date_Dim
           
from [dbo].[D_OPRA_DATE]
	       where [DATE_SID] >0
```

Context: SqlCommand for LKP - D_OPRA_DATE - MIN&MAX

```sql
SELECT 
LEASE_ID
, LEASE_SID
FROM DBO.D_PRM_LEASE
```

Context: SQL query for LKP - D_PRM_LEASE

```sql
SELECT FACILITY_TYPE_ID, FACILITY_TYPE_SID
FROM DBO.D_PRM_FACILITY_TYPE
```

Context: SQL query for LKP - D_PRM_FACILITY_TYPE

```sql
SELECT MISSION_ID, MISSION_SID
FROM DBO.D_PRM_MISSION
```

Context: SQL query for LKP - D_PRM_MISSION

```sql
SELECT CURRENCY_ID
, CURRENCY_SID AS 
CURRENCY_BASE_SID
      
  FROM [dbo].[D_PRM_CURRENCY]
```

Context: SQL query for LKP - D_PRM_CURRENCY - BASE

```sql
SELECT [DATE_SID]  AS [LEASE_END_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_END

```sql
SELECT [DATE_SID]  AS [COST_PERIOD_END_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - COST_PERIOD_END

```sql
SELECT [DATE_SID]  AS [LEASE_NOTICE_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_NOTICE

```sql
SELECT [DATE_SID]  AS [LEASE_START_DT_SID]  
      ,[DATE_BK]     
FROM [dbo].[D_OPRA_DATE]
```

Context: SQL query for LKP - D_OPRA_DATE - LEASE_START

```sql
SELECT FORECAST_DETAIL_ID
,PROPERTY_SID
,MISSION_SID
,FORECAST_TYPE_SID
,CURRENCY_SID
,FACILITY_TYPE_SID
,TITLE_SID
,FISCAL_YEAR_SID
,ETL_CREA_DT
,ETL_UPDT_DT
,START_FISCAL_YEAR_SID
,FISCAL_YEAR_SEQUENCE_NBR AS FISCAL_YEAR_SEQUENCE_NBR
,[FORECAST_AMT]
 FROM dbo.F_PRM_FORECAST
```

Context: SqlCommand for OLEDB_DEST - F_PRM_FORECAST

```sql
select ACCOMMODATION_ID, 
ACCOMMODATION_TITLE_ID,
1 AS date_max_min_key
 from PRM_ACCOMMODATION
--where accommodation_id = 7794
ORDER by ACCOMMODATION_TITLE_ID
```

Context: SQL query for OLEDB_SRC - PRM_ACCOMMODATION

```sql
SELECT [ACCOMMODATION_ID]
      ,[LEASE_ID]
      ,[COST_PERIOD_ID]
      ,[TITLE_ID]
      ,[FACILITY_TYPE_ID]
      ,[MISSION_ID]
      ,[LEASE_DEPOSIT_CURRENCY_ID]
     -- ,[cos_cty_2id]
      
,[BASE_RENT_CURRENCY_ID]
     
 ,[OTHER_RENT_CURRENCY_ID]
      ,[COST_PERIOD_START_DT_ID]
      ,[COST_PERIOD_END_DT_ID]
      ,[LEASE_START_DT_ID]
      ,[LEASE_END_DT_ID]
      ,[LEASE_NOTICE_DT_ID]
      ,[CURRENT_LEASE_IND]
      ,[CURRENT_COST_PERIOD_IND]

      ,[DRV_PRID_FIRST_LEASE_IND]
, 0 AS  MANUAL_ADDED
  
, base_rate
, other_rate 
FROM [dbo].[PRM_LEASE_COSTING_LKP]
```

Context: SQL query for LKP - PRM_LEASE_COSTING_LKP

```sql
SELECT [SPACE_THRESHOLD_ID]      
      ,[SPACE_THRESHOLD_SECURE_T1_NBR] AS SECURE_ZONE_T1
      ,[SPACE_THRESHOLD_SECURE_T2_NBR] AS SECURE_ZONE_T2
      ,[SPACE_THRESHOLD_SECURE_T3_NBR] AS SECURE_ZONE_T3
      ,[SPACE_THRESHOLD_OPERATIONAL_T1_NBR] AS OPERATIONAL_ZONE_T1
      ,[SPACE_THRESHOLD_OPERATIONAL_T2_NBR] AS OPERATIONAL_ZONE_T2
      ,[SPACE_THRESHOLD_OPERATIONAL_T3_NBR] OPERATIONAL_ZONE_T3
      --,[SPACE_THRESHOLD_OPERATIONAL_CAPACITY_NBR]
      ,[SPACE_THRESHOLD_OPERATIONAL_OCCUPANCY_NBR] AS OPERATIONAL_ZONE_OCCUPANCY
      --,[SPACE_THRESHOLD_SECURE_CAPACITY_NBR]
      ,[SPACE_THRESHOLD_SECURE_OCCUPANCY_NBR] AS SECURE_ZONE_OCCUPANCY
, 1 as date_max_min_key
      
  FROM [dbo].[PRM_SPACE_THRESHOLD_BY_FY]
```

Context: SQL query for OLEDB_SRC - PRM_SPACE_THRESHOLD_BY_FY

```sql
SELECT [STRUCTURE_CONDITION_BY_FY_ID] AS[STRUCTURE_CONDITION_ID]
      , 1 AS date_max_min_key
  FROM [dbo].[PRM_STRUCTURE_CONDITION_BY_FY]
```

Context: SQL query for OLEDB_SRC - PRM_STRUCTURE_CONDITION_BY_FY

```sql
TRUNCATE TABLE dbo.F_PRM_STRUCTURE_CONDITION;

TRUNCATE TABLE dbo.F_PRM_SPACE_THRESHOLD;

TRUNCATE TABLE dbo.F_PRM_FORECAST;

TRUNCATE TABLE dbo.F_PRM_PROPERTY;

TRUNCATE TABLE dbo.F_PRM_OCCUPANCY;

TRUNCATE TABLE dbo.F_PRM_LEASE_COSTING;

TRUNCATE TABLE dbo.F_PRM_RENT_COSTING;

TRUNCATE TABLE [dbo].[PRM_CDC_Changes];
```

Context: SQL query for ESQLT- TRUNCATE ALL FACT TABLES

```sql
SELECT [cdc_ID]
      ,[cdc_Table_name]
      ,[cdc_Column_name]
      ,[cdc_LastUpdate]
      ,[cdc_UpdatedBy]
      ,[cdc_New_value]
      ,[cdc_action]
FROM [dbo].[CDC_Changes]
```

Context: SQL query for OLEDB_SRC - CDC_Changes

```sql
SELECT MISSION_ID, MISSION_SID
FROM DBO.D_PRM_MISSION
```

Context: SQL query for LKP - D_PRM_MISSION

```sql
SELECT FACILITY_TYPE_ID, FACILITY_TYPE_SID
FROM DBO.D_PRM_FACILITY_TYPE
```

Context: SQL query for LKP - D_PRM_FACILITY_TYPE

```sql
SELECT 
COST_PERIOD_ID
, COST_PERIOD_SID
FROM DBO.D_PRM_COST_PERIOD
```

Context: SQL query for LKP - D_PRM_COST_PERIOD

```sql
SELECT CURRENCY_ID
, CURRENCY_SID AS CURRENCY_BASE_SID
      
  FROM [dbo].[D_PRM_CURRENCY]
```

Context: SQL query for LKP - D_PRM_CURRENCY - BASE

## 5. Output Analysis

| Destination Table              | Description                                                        | Source Part                                                                                                                                                                                    |
|-------------------------------|--------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dbo.F_PRM_FORECAST`          | Stores forecast data.                                                                    | DFT - F_PRM_FORECAST                                                                                                                                     |
| `dbo.F_PRM_LEASE_COSTING`          | Stores lease costing data.                                                                    | DFT - F_PRM_LEASE_COSTING                                                                                                                                     |
| `dbo.F_PRM_OCCUPANCY`          | Stores occupancy data.                                                                    | DFT - F_PRM_OCCUPANCY                                                                                                                                     |
| `dbo.F_PRM_PROPERTY`          | Stores property data.                                                                    | DFT - F_PRM_PROPERTY                                                                                                                                     |
| `dbo.F_PRM_RENT_COSTING`          | Stores rental costs data.                                                                    | DFT - F_PRM_RENT_COSTING                                                                                                                                     |
| `dbo.F_PRM_SPACE_THRESHOLD`          | Stores space threshold data.                                                                    | DFT - F_PRM_SPACE_THRESHOLD                                                                                                                                     |
| `dbo.F_PRM_STRUCTURE_CONDITION`          | Stores structure condition data.                                                                    | DFT - F_PRM_STRUCTURE_CONDITION                                                                                                                                     |
| `dbo.PRM_CDC_Changes`          | Stores change data.                                                                    | DFT - PRM_CDC_Changes                                                                                                                                     |

## 6. Package Summary

*   **Input Connections:** 3
*   **Output Destinations:** 8 (excluding event handler destinations)
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 7
    *   Execute SQL Tasks: 2 (1 in PreExecute, 1 in OnError)
    *   Expression Tasks: 3 ( 1 before SEQC-LOAD FACT TABLES, 1 in PreExecute, 1 in OnError)
    *   Derived Column: 12+
    *   Lookup: 25+
    *   Merge Join: 2
    *   Sort: 1
    *   Union All: 2
*   Overall package complexity assessment: Medium
*   Potential performance bottlenecks: Numerous Lookup transformations could impact performance.  Data sorting within the data flow `DFT - F_PRM_LEASE_COSTING` also could be a performance bottleneck.
*   Critical path analysis: The sequence of fact table loads within `SEQC-LOAD FACT TABLES` forms a critical path.
*   Error handling mechanisms: The package uses an `OnError` event