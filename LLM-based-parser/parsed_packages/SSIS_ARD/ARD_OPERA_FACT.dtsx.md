## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| ARD_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data and destination | SQL Server Auth likely | @[$Project::PRJ_PRM_DIM_UNKNOWN_MEMBER_SID]            | Part 1, 2, 3                  |
| DATA_HUB           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely           |  None                  | Part 1, 2, 3                 |
| ARD_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup OPRA_OPSW_ACTIVITIES_LKP and OPRA_OPSW_PROJECT_UPDATES_LKP             | SQL Server Auth likely           |  None                  | Part 1, 2, 3                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `ARD_OPERA_FACT` is designed to load several fact tables related to the OPRA (OPERA) project. It starts with an expression task that seems to act as a trigger. The main logic is encapsulated in a sequence container called `SEQC-LOAD FACT TABLES`. Within this container, multiple Data Flow Tasks (DFTs) are used to load individual fact tables.

*   **Control Flow:**
    1.  `EXPRESSIONT- Fact Tables - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`: An expression task that likely initiates the data loading process. Its expression is a simple `1 == 1`.
    2.  `SEQC-LOAD FACT TABLES`: A sequence container that contains all the data flow tasks responsible for loading the fact tables.

*   **Data Flow Tasks:**
    *   `DFT - F_OPRA_PROJECT_ACTIVITY`: Loads data into the `F_OPRA_PROJECT_ACTIVITY` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_ACTIVITIES` extracts data from the staging database.
        *   Transformations:
            *   `LKP - OPRA_OPSW_ACTIVITIES_LKP`:  Lookup transformation using OPRA_OPSW_ACTIVITIES_LKP view on ARD_STAGING
            *   `LKP - D_OPRA_PROJECT`, `LKP - D_PRM_MISSION`, `LKP - D_OPRA_PROJECT_UPDATE`, `LKP - D_OPRA_DATE` and others: Lookup transformations to dimension tables on ARD_REPORTING.
            * DRV_TRFM - DATE_BK: Derived column transformation to handle date backfills
            *   `DRV_TRFM - DATES AND UNCODED`: Derived column transformation to create ETL timestamps and other derived columns.
        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_ACTIVITY` loads data into the `F_OPRA_PROJECT_ACTIVITY` table in the reporting database.

    *   `DFT - F_OPRA_PROJECT_ACTUAL`: Loads data into the `F_OPRA_PROJECT_ACTUAL` fact table.
        *   Source: `OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS` extracts data from the source system.
        *   Transformations:
            *   `DRV_TRFM - FISCAL_TO_CALENDAR`: Derived column transformation to convert fiscal dates to calendar dates.
            *   `LKP - D_OPRA_PROJECT`, `LKP - D_PRM_MISSION`, `LKP - D_D_OPRA_WORK_BREAKDOWN_STRUCTURE` and `LKP - D_OPRA_PROJECT_UPDATE`: Lookup transformations to dimension tables.
             *   `DRV_TRFM - DATES`: Derived column transformation to create ETL timestamps.
            *   `DRV_TRFM - Uncoded`: Derived column transformation to handle uncoded values.
            *   `AGG - Sum Actual Amount`: Aggregate transformation to sum actual amounts.
        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_ACTUAL` loads data into the `F_OPRA_PROJECT_ACTUAL` table.

    *   `DFT - F_OPRA_PROJECT_COSTING`: Loads data into the `F_OPRA_PROJECT_COSTING` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_PROJECT_COSTING` extracts data from the source system.
        *   Transformations:
           *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *   `LKP - D_OPRA_PROJECT`, `LKP - D_PRM_MISSION`, `LKP - D_OPRA_WORK_BREAKDOWN_STRUCTURE`,
            *    `LKP - D_OPRA_PROGRAM`,  `LKP - D_OPRA_FUND_SOURCE`, `LKP - D_OPRA_DATE` and others: Lookup transformations to dimension tables on ARD_REPORTING.
             *   `DRV_TRFM - DATE_BK`: Derived column transformation to handle date backfills
            *   `DRV_TRFM - DATES AND UNCODED:` Derived column transformation to create ETL timestamps and other derived columns.
        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_COSTING` loads data into the `F_OPRA_PROJECT_COSTING` table.

    *   `DFT - F_OPRA_PROJECT_FLAGGED_ISSUE`: Loads data into the `F_OPRA_PROJECT_FLAGGED_ISSUE` fact table.
        *   Source: `OLEDB_SCR - OPRA_OPSW_PROJECT_FLAGGED_ISSUES` extracts data from the source system.
        * Transformations:
            *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *   `LKP - D_OPRA_PROJECT` and other related dimension lookups.
            *   `DRV_TRFM - DATES & Uncoded`: Derived column transformation to create ETL timestamps and handle uncoded values.

        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_FLAGGED_ISSUE` loads data into the `F_OPRA_PROJECT_FLAGGED_ISSUE` table.

    *   `DFT - F_OPRA_PROJECT_PRIORITY_SECTION`: Loads data into the `F_OPRA_PROJECT_PRIORITY_SECTION` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_PROJECT_PRIORITY_SECTIONS` extracts data from the source system.
         *   Transformations:
            *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *   `LKP - D_OPRA_PROJECT` and other related dimension lookups.
            *   `DRV_TRFM - DATES & Uncoded`: Derived column transformation to create ETL timestamps and handle uncoded values.
       *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_PRIORITY_SECTION` loads data into the `F_OPRA_PROJECT_PRIORITY_SECTION` table.

    *   `DFT - F_OPRA_PROJECT_RESOURCE`: Loads data into the `F_OPRA_PROJECT_RESOURCE` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_PROJECT_RESOURCES` extracts data from the source system.
        *   Transformations:
            *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *  `LKP - D_OPRA_PROJECT` and other related dimension lookups.
            *   `DRV_TRFM - DATES & Uncoded`: Derived column transformation to create ETL timestamps and handle uncoded values.
        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_RESOURCE` loads data into the `F_OPRA_PROJECT_RESOURCE` table

    *   `DFT - F_OPRA_PROJECT_PCRA_QUESTION_ANSWER`: Loads data into the `F_OPRA_PROJECT_PCRA_QUESTION_ANSWER` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_PROJECT_PCRA_QUESTION_ANSWERS` extracts data from the source system.
        *   Transformations:
            *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *  `LKP - D_OPRA_PROJECT` and other related dimension lookups.
            *   `DRV_TRFM - DATES & Uncoded`: Derived column transformation to create ETL timestamps and handle uncoded values.
        *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_PCRA_QUESTION_ANSWER` loads data into the `F_OPRA_PROJECT_PCRA_QUESTION_ANSWER` table.

     *`DFT - F_OPRA_PROJECT_WBS_COSTING`: Loads data into the `F_OPRA_PROJECT_WBS_COSTING` fact table.
        *   Source: `OLEDB_SRC - OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING` extracts data from the source system.
           *   Transformations:
            *   `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`:  Lookup transformation using OPRA_OPSW_PROJECT_UPDATES_LKP view on ARD_STAGING
            *  `LKP - D_OPRA_PROJECT` and other related dimension lookups.
             *   `DRV_TRFM - DATE_BK`: Derived column transformation to handle backdated entries.
            *   `DRV_TRFM - DATES AND UNCODED`: Derived column transformation to create ETL timestamps and handle uncoded values.
       *   Destination: `OLEDB_DESC - F_OPRA_PROJECT_WBS_COSTING` loads data into the `F_OPRA_PROJECT_WBS_COSTING` table.
        *`ESQLT- TRUNCATE ALL FACT TABLES`: Truncates fact tables before loading data.

## 4. Code Extraction

### SQL Queries:

```sql
SELECT [ACTIVITY_ID], 1 AS date_max_min_key
FROM [dbo].[OPRA_OPSW_ACTIVITIES]
```

*   Context: This SQL query is used in the `OLEDB_SRC - OPRA_OPSW_ACTIVITIES` source component within the `DFT - F_OPRA_PROJECT_ACTIVITY` data flow task.

```sql
SELECT [PROJECT_FINANCIAL_IRD_ID]
      ,ACT.[PROJECT_FINANCIAL_PROJECT_CODE_TXT]
      ,ACT.[PROJECT_FINANCIAL_YEAR_NBR]
      ,ACT.[PROJECT_FINANCIAL_PERIOD_NBR]
      ,ACT.[PROJECT_FINANCIAL_AMT]      
      --,ACT.[PROJECT_FINANCIAL_WBS_ENDING_TXT]
      ,ACT.[PROJECT_FINANCIAL_CHECK_TXT]
      --,ACT.[PROJECT_FINANCIAL_FNT_ID]
 
  FROM [dbo].[MPSR_IMS_PROJECT_FINANCIALS] ACT

  JOIN (SELECT MAX(T.[PROJECT_FINANCIAL_IRD_ID]) AS PROJECT_FINANCIAL_IRD_ID
      ,T.[PROJECT_FINANCIAL_PROJECT_CODE_TXT]
      /*,T.[PROJECT_FINANCIAL_YEAR_NBR]
      ,T.[PROJECT_FINANCIAL_PERIOD_NBR]     
      ,T.[PROJECT_FINANCIAL_WBS_ENDING_TXT]
      ,T.[PROJECT_FINANCIAL_CHECK_TXT]
      ,T.[PROJECT_FINANCIAL_FNT_ID]*/
 
  FROM [dbo].[MPSR_IMS_PROJECT_FINANCIALS] T
   WHERE T.PROJECT_FINANCIAL_PROJECT_CODE_TXT NOT IN ('#N/A', 'NULL') 
  AND T.PROJECT_FINANCIAL_FNT_ID = 1
  AND T.PROJECT_FINANCIAL_PROJECT_CODE_TXT IS NOT NULL
  --AND T.PROJECT_FINANCIAL_WBS_ENDING_TXT LIKE '.1%'
  GROUP BY T.[PROJECT_FINANCIAL_PROJECT_CODE_TXT]
      /*,T.[PROJECT_FINANCIAL_YEAR_NBR]
      ,T.[PROJECT_FINANCIAL_PERIOD_NBR]     
      ,T.[PROJECT_FINANCIAL_WBS_ENDING_TXT]
      ,T.[PROJECT_FINANCIAL_CHECK_TXT]
      ,T.[PROJECT_FINANCIAL_FNT_ID]
	  */) MX

ON ACT.[PROJECT_FINANCIAL_IRD_ID] = MX.PROJECT_FINANCIAL_IRD_ID
      AND ACT.[PROJECT_FINANCIAL_PROJECT_CODE_TXT] = MX.PROJECT_FINANCIAL_PROJECT_CODE_TXT
      /*AND ACT.[PROJECT_FINANCIAL_YEAR_NBR] = MX.PROJECT_FINANCIAL_YEAR_NBR
      AND ACT.[PROJECT_FINANCIAL_PERIOD_NBR] = MX.PROJECT_FINANCIAL_PERIOD_NBR
       
      AND ACT.[PROJECT_FINANCIAL_WBS_ENDING_TXT] = MX.PROJECT_FINANCIAL_WBS_ENDING_TXT
      AND ACT.[PROJECT_FINANCIAL_CHECK_TXT] = MX.PROJECT_FINANCIAL_CHECK_TXT
      AND ACT.[PROJECT_FINANCIAL_FNT_ID] = MX.PROJECT_FINANCIAL_FNT_ID*/

  WHERE ACT.PROJECT_FINANCIAL_PROJECT_CODE_TXT NOT IN ('#N/A', 'NULL') 
  AND ACT.PROJECT_FINANCIAL_FNT_ID = 1
```

*   Context: This SQL query is used in the `OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS` source component within the `DFT - F_OPRA_PROJECT_ACTUAL` data flow task.

```sql
SELECT [PROJECT_COSTING_ID]
      ,[PROJECT_COSTING_VALUE_AMT]
      ,[PROJECT_COSTING_PROJECT_UPDATE_ID]
      --,[PROJECT_COSTING_DTM]
      ,[PROJECT_COSTING_WORK_BREAKDOWN_STRUCTURE_ID]
      ,[PROJECT_COSTING_PROGRAM_ID]
      ,[PROJECT_COSTING_FUND_SOURCE_ID]      
, 1 AS date_max_min_key
FROM [dbo].[OPRA_OPSW_PROJECT_COSTING]
--WHERE [PROJECT_COSTING_IS_ACTIVE_IND] = 1
```

*   Context: This SQL query is used in the `OLEDB_SRC - OPRA_OPSW_PROJECT_COSTING` source component within the `DFT - F_OPRA_PROJECT_COSTING` data flow task.

```sql
SELECT [PROJECT_FLAGGED_ISSUES_ID]
      ,[PROJECT_FLAGGED_ISSUES_PUP_ID]
      ,[PROJECT_FLAGGED_ISSUES_PRI_ID]
 FROM [dbo].[OPRA_OPSW_PROJECT_FLAGGED_ISSUES]
```

*   Context: This SQL query is used in the `OLEDB_SCR - OPRA_OPSW_PROJECT_FLAGGED_ISSUES` source component within the `DFT - F_OPRA_PROJECT_FLAGGED_ISSUE` data flow task.

```sql
SELECT [PROJECT_PRIORITY_SECTION_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_PRIORITY_SECTIONS]
```

*   Context: This SQL query is used in the `OLEDB_SRC - OPRA_OPSW_PROJECT_PRIORITY_SECTIONS` source component within the `DFT - F_OPRA_PROJECT_PRIORITY_SECTION` data flow task.

```sql
SELECT [ACTIVITY_ID], 1 AS date_max_min_key
FROM [dbo].[OPRA_OPSW_ACTIVITIES]
```

*   Context: This SQL query is used in the `OLEDB_SRC - OPRA_OPSW_ACTIVITIES` source component within the `DFT - F_OPRA_PROJECT_ACTIVITY` data flow task.

```sql
SELECT [PROJECT_UPDATE_ID]
      ,[PROJECT_ID]
      ,[PROJECT_MISSION_ID]
      ,[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_UPDATES_LKP]
```

*   Context: This SQL query is used in the `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP` source component within the `DFT - F_OPRA_PROJECT_PRIORITY_SECTION` data flow task.

```sql
SELECT [PROJECT_UPDATE_ID]
      ,[PROJECT_ID]
      ,[PROJECT_MISSION_ID]
      ,[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_UPDATES_LKP]
```

*   Context: This SQL query is used in the `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP` source component within the `DFT - F_OPRA_PROJECT_COSTING` data flow task.

```sql
SELECT [PROJECT_UPDATE_ID]
      ,[PROJECT_ID]
      ,[PROJECT_MISSION_ID]
      ,[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_UPDATES_LKP]
```

*   Context: This SQL query is used in the `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP` source component within the `DFT - F_OPRA_PROJECT_RESOURCE` data flow task.

```sql
SELECT [PROJECT_UPDATE_ID]
      ,[PROJECT_ID]
      ,[PROJECT_MISSION_ID]
      ,[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_UPDATES_LKP]
```

*   Context: This SQL query is used in the `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP` source component within the `DFT - F_OPRA_PROJECT_PCRA_QUESTION_ANSWER` data flow task.

```sql
SELECT [PROJECT_UPDATE_ID]
      ,[PROJECT_ID]     
      ,[PROJECT_MISSION_ID]
      ,[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]
FROM [dbo].[OPRA_OPSW_PROJECT_UPDATES_LKP]
```

*   Context: This SQL query is used in the `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP` source component within the `DFT - F_OPRA_PROJECT_WBS_COSTING` data flow task.

```sql
TRUNCATE TABLE dbo.F_OPRA_PROJECT_FUNDING;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_COSTING;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_ACTIVITY;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_WBS_COSTING;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_FLAGGED_ISSUE;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_PRIORITY_SECTION;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_RESOURCE; 

TRUNCATE TABLE
dbo.F_OPRA_PROJECT_PCRA_QUESTION_ANSWER;

TRUNCATE TABLE dbo.F_OPRA_PROJECT_ACTUAL;
```

*   Context: This SQL statement source is used in the `ESQLT- TRUNCATE ALL FACT TABLES` Execute SQL Task.

```sql
SELECT [DATE_SID]
   
  FROM [dbo].[D_OPRA_DATE]
```

*   Context: This SQL statement source is used in the `LKP - D_OPRA_DATE` lookup task.

```sql
select PROJECT_UPDATE_SID AS LATEST_PROJECT_UPDATE_SID, PROJECT_UPDATE_ID from dbo.D_OPRA_PROJECT_UPDATE
```

*   Context: This SQL statement source is used in the `LKP - D_OPRA_PROJECT_UPDATE` lookup task.

```sql
SELECT [MISSION_SID]
      ,[MISSION_ID]
FROM [dbo].[D_PRM_MISSION]
```

*   Context: This SQL statement source is used in the `LKP - D_PRM_MISSION` lookup task.

```sql
SELECT [WORK_BREAKDOWN_STRUCTURE_SID]
       ,[WBS_CODE]
    
  FROM [dbo].[D_OPRA_WORK_BREAKDOWN_STRUCTURE]
```

*   Context: This SQL statement source is used in the `LKP - D_D_OPRA_WORK_BREAKDOWN_STRUCTURE` lookup task.

```sql
SELECT [PROJECT_SID]
      
      ,[PROJECT_MISSION_ID]
      
      ,[PROJECT_TITLE]
    
,  [LATEST_PROJECT_UPDATE_ID]  
  FROM [dbo].[D_OPRA_PROJECT]
```

*   Context: This SQL statement source is used in the `LKP - D_OPRA_PROJECT` lookup task.

### Expression Evaluators:

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_START_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_START_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_START_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_PHASE_START_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTIVITY` Data Flow Task.

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_END_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_END_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_PHASE_END_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_PHASE_END_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTIVITY` Data Flow Task.

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_START_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_START_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_START_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_ACTIVITY_START_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTIVITY` Data Flow Task.

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_END_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_END_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_ACTIVITY_END_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_ACTIVITY_END_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTIVITY` Data Flow Task.

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTIVITY\LKP - OPRA_OPSW_ACTIVITIES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTIVITY` Data Flow Task.

```
(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_PERIOD_NBR]} <= 9 ? #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_YEAR_NBR]} - 1 : #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_YEAR_NBR]}) * 10000 + (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_PERIOD_NBR]} <= 9 ? #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_PERIOD_NBR]} + 3 : #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_ACTUAL\OLEDB_SRC - MPSR_IMS_PROJECT_FINANCIALS.Outputs[OLE DB Source Output].Columns[PROJECT_FINANCIAL_PERIOD_NBR]} - 9) * 100 + 1
```

*   Context: This expression is used to derive the `PROJECT_ACTUAL_DATE_SID` within the `DRV_TRFM - FISCAL_TO_CALENDAR` Derived Column transformation in the `DFT - F_OPRA_PROJECT_ACTUAL` Data Flow Task.

```
(DT_STR,10,1252)(#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_COSTING\LKP - OPRA_OPSW_PROJECT_UPDATES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]} > #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_COSTING\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Max_Date_Dim]} ? "FUTURE" : (#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_COSTING\LKP - OPRA_OPSW_PROJECT_UPDATES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]} < #{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_COSTING\LKP - D_OPRA_DATE - MIN&MAX.Outputs[Lookup Match Output].Columns[Min_Date_Dim]} ? "PAST" : [REPLACENULL]((DT_STR,10,1252)#{Package\SEQC-LOAD FACT TABLES\DFT - F_OPRA_PROJECT_COSTING\LKP - OPRA_OPSW_PROJECT_UPDATES_LKP.Outputs[Lookup Match Output].Columns[PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID]},"NULL VALUE")))
```

*   Context: This expression is used to derive the `PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_BK` within the `DRV_TRFM - DATE_BK` Derived Column transformation in the `DFT - F_OPRA_PROJECT_COSTING` Data Flow Task.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.F_OPRA_PROJECT_ACTIVITY| Stores project activity data     | Part 2|
| dbo.F_OPRA_PROJECT_ACTUAL| Stores project actual data        | Part 2|
| dbo.F_OPRA_PROJECT_COSTING | Stores project costing data       | Part 2|
| dbo.F_OPRA_PROJECT_FLAGGED_ISSUE | Stores project flagged issue data | Part 2|
| dbo.F_OPRA_PROJECT_PRIORITY_SECTION | Stores project priority section data | Part 2|
| dbo.F_OPRA_PROJECT_RESOURCE | Stores project resource data      | Part 2|
| dbo.F_OPRA_PROJECT_PCRA_QUESTION_ANSWER | Stores project PCRA QA data     | Part 2|

## 6. Package Summary

*   **Input Connections:** 3
    *   `ARD_REPORTING`: Used for dimension lookups and as the final destination.
    *   `DATA_HUB`: Used as a source for staging data.
    *   `ARD_STAGING`: Used as a source for staging data.
*   **Output Destinations:** 7 fact tables.
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 2.
    *   Sequence Containers: 1.
    *   Data Flow Tasks: 8.
    *   Execute SQL Tasks: 1.
    *   Lookup Transformations: Numerous instances.
    *   Derived Column Transformations: Numerous instances.
*   Overall package complexity assessment: High due to multiple data flow tasks.
*   Potential performance bottlenecks:
    *   Multiple `OLE DB Source` components extracting from the same database.
    *   Numerous lookup transformations, which can be slow if the lookup table does not fit into memory. All are set to cache type = 0.
    *   `DRV_TRFM - DATE_BK` can be optimized to reduce expensive operations.
*   Critical path analysis: The sequence container `SEQC-LOAD FACT TABLES` is the critical path because