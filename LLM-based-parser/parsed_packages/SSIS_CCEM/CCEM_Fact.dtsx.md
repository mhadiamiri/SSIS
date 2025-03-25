## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Flat File Connection Manager   | FLATFILE | File: Z:\Julian\15_CCEM_SSIS\12_Ticket\3_Arrest & Detention Star\TEST_F_ARREST.txt | Source for data flow | File System Permissions Likely | None | Part 1 |
| MART_CCEM           | OLE DB          | [Inferred] | Lookup data and destination | SQL Server Authentication Likely | @[$Project::PRJ_PRM_DIM_UNKNOWN_MEMBER_SID]            | Part 1 |
| CCEM_STAGING           | OLE DB          | [Inferred] | Source for fact tables             | SQL Server Authentication Likely            | None                 | Part 1                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1|

## 3. Package Flow Analysis

The package `CCEM_Fact` is designed to load data into various fact tables related to the CCEM (Consular Case Management System). It involves a series of tasks, sequence containers, and data flow tasks.

*   **Control Flow:**

    1.  `EXPRESSIONT- Fact Tables - Start Task`: An expression task that always evaluates to true (1 == 1).  Serves as a starting point.
    2.  `ESQLT- Truncate REJECT_CCEM_MASTER`: Truncates the `dbo.REJECT_CCEM_MASTER` table.
    3.  `SEQC-F_CCEM_ARREST_DETENTION`:  A sequence container for the `F_CCEM_ARREST_DETENTION` fact table loading process.
    4.  `SEQC-F_CCEM_ARREST_DETENTION 1`: A disabled sequence container. Likely a backup or previous version of the above sequence.
    5.  `SEQC-F_CCEM_CRISIS`:  A sequence container for the `F_CCEM_CRISIS` fact table loading process.
    6.  `SEQC-F_CCEM_DEPARTURE`:  A sequence container for the `F_CCEM_DEPARTURE` fact table loading process.
    7.  `SEQC-F_CCEM_REGISTRATION`: Load Fact table CCEM REGISTRATION.
    8.  `SEQC-F_CCEM_REGISTRATION_AGG`: Load Fact table CCEM REGISTRATION AGGREGATION.
    9.  `Sequence Container`: Contains two data flow tasks: `SEQC-F_CCEM_ACTIVITY` and `SEQC-F_CCEM_CASE`.

#### DFT- F_CCEM_ARREST_DETENTION

*   **Source:** No explicitly defined source.
*   **Transformations:**
    *   `Merge Join` and `Merge Join 2`, `Merge Join 3`, `Merge Join 4`, `Merge Join 5`, `Merge Join 6`: Several merge join transformations are used to combine data from staging tables and dimension tables.
    *   `LKP-D_CCEM_SUBCATEGORY`: Lookup from `D_CCEM_SUBCATEGORY` table.
    *   `DRV_TRFM_UNKNOWN_SID`: Derived column transformation to handle potentially null SID values in the data flow.
*   **Destinations:**
    *   `OLEDB_DEST_F_CCEM_ARREST_DETENTION`: Destination to write the transformed data into the `dbo.F_CCEM_ARREST_DETENTION` table.

#### DFT- F_CCEM_CRISIS

*   **Source:** OLE DB Source extracts data from staging table  `CCEM_CRISIS`.
*   **Transformations:**
    *   `LKP-D_CCEM_CRISIS`: Lookup from `D_CCEM_CRISIS` table.
    *   `DRV_TRFM-Unknown_Value`: Derived column transformation to handle potentially null SID values in the data flow.
*   **Destinations:**
    *   `OLEDB_DEST-F_CCEM_CRISIS`: Destination to write the transformed data into the `dbo.F_CCEM_CRISIS` table.

#### DFT- F_CCEM_DEPARTURE

*   **Source:** OLE DB Source extracts data from staging table  `CCEM_DEPARTURE`.
*   **Transformations:**
    *   `LKP-D_CCEM_DEPARTURE`: Lookup from `D_CCEM_DEPARTURE` table.
    *   `DRV_TRFM-Unknown_Value`: Derived column transformation to handle potentially null SID values in the data flow.
*   **Destinations:**
    *   `OLEDB_DEST-F_CCEM_DEPARTURE`: Destination to write the transformed data into the `dbo.F_CCEM_DEPARTURE` table.

#### DFT- F_CCEM_REGISTRATION

*   **Source:** OLE DB Source extracts data from staging table  `CCEM_REGISTRATION`.
*   **Transformations:**
    *   `LKP_D_CCEM_CLIENT`: Lookup from `D_CCEM_CLIENT` table.
    *   `DRV_TRFM-Unknown_Value`: Derived column transformation to handle potentially null SID values in the data flow.
*   **Destinations:**
    *   `OLEDB_DEST-F_CCEM_REGISTRATION`: Destination to write the transformed data into the `dbo.F_CCEM_REGISTRATION` table.

#### DFT- CCEM_REGISTRATION_AGG

*   **Source:** OLE DB Source extracts data from   `F_CCEM_REGISTRATION`.
*   **Transformations:** None explicitly listed aside from inherent aggregation.
*   **Destinations:**
    *   `OLE DB Dest_F_CCEM_REGISTRATION_AGG`: Destination to write the transformed data into the `dbo.F_CCEM_REGISTRATION_AGG` table.

#### DFT- F_CCEM_ACTIVITY and DFT- F_CCEM_CASE (Nested within Sequence Container)

*   `DFT- F_CCEM_ACTIVITY`:
    *   **Source:** OLE DB Source extracts data from staging table  `CCEM_CASE_ACTIVITY`.
    *   **Transformations:**
        *   `LKP_D_CCEM_CASE`: Lookup from `D_CCEM_CASE` table.
        *   `DRV_TRFM_FACT_TABLE_NAME`: Derived column transformation to name fact table.
        *   `DRV_TRFM-D_CCEM_CASE`: Derived column transformation to set REASON.
    *   **Destinations:**
        *   `OLEDB_Dest-F_CCEM_ACTIVITY`: Destination to write the transformed data into the `dbo.F_CCEM_ACTIVITY` table.
        *   `OLEDB_Dest-REJECT_CCEM_MASTER`: Destination to write the rejected data into the `dbo.REJECT_CCEM_MASTER` table.
*   `DFT- F_CCEM_CASE`:
    *   **Source:** OLE DB Source extracts data from staging table  `CCEM_CASE_ACTIVITY`.
    *   **Transformations:**
        *   `LKP-D_CCEM_SUBCATEGORY`: to get subtype SID.
        *   `DRV_TRFM-Unknown_Value`: Derived column transformation to handle potentially null SID values.
    *   **Destinations:**
        *   `OLEDB_Dest-F_CCEM_ACTIVITY`: Destination to write the transformed data into the `dbo.F_CCEM_ACTIVITY` table.
        *   `OLEDB_Dest-REJECT_CCEM_MASTER`: Destination to write the rejected data into the `dbo.REJECT_CCEM_MASTER` table.

## 4. Code Extraction

```sql
TRUNCATE TABLE dbo.REJECT_CCEM_MASTER;
```

Context: This SQL command is executed to truncate the `REJECT_CCEM_MASTER` table.

```sql
SELECT [ARREST_FLAG_SID]
      ,[IS_CURRENT_DETENTION_IND]
    
      ,[IS_LAST_VISIT_IND]
     
  FROM [dbo].[D_CCEM_ARREST_DETENTION_FLAG]
```

Context: This SQL query retrieves data from the `D_CCEM_ARREST_DETENTION_FLAG` dimension table.

```sql
select * from (SELECT [ARREST_FLAG_SID]
      ,[IS_CURRENT_DETENTION_IND]
    
      ,[IS_LAST_VISIT_IND]
     
  FROM [dbo].[D_CCEM_ARREST_DETENTION_FLAG]) [refTable]
where [refTable].[IS_LAST_VISIT_IND] = ? and [refTable].[IS_CURRENT_DETENTION_IND] = ?
```

Context: This SQL query retrieves data from the `D_CCEM_ARREST_DETENTION_FLAG` dimension table based on input parameters.

```sql
SELECT  [EMPLOYEE_SID]
      ,[EMPLOYEE_ID]
    
  FROM [dbo].[D_CCEM_EMPLOYEE]
```

Context: This SQL query retrieves data from the `D_CCEM_EMPLOYEE` dimension table.

```sql
select * from (SELECT  [EMPLOYEE_SID]
      ,[EMPLOYEE_ID]
    
  FROM [dbo].[D_CCEM_EMPLOYEE]) [refTable]
where [refTable].[EMPLOYEE_ID] = ?
```

Context: This SQL query retrieves data from the `D_CCEM_EMPLOYEE` dimension table based on input parameters.

```sql
SELECT  [SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
   
  FROM [dbo].[D_CCEM_SUBCATEGORY]
```

Context: This SQL query retrieves data from the `D_CCEM_SUBCATEGORY` dimension table.

```sql
select * from (SELECT  [SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
   
  FROM [dbo].[D_CCEM_SUBCATEGORY]) [refTable]
where [refTable].[SUBCATEGORY_NBR] = ?
```

Context: This SQL query retrieves data from the `D_CCEM_SUBCATEGORY` dimension table based on input parameters.

```sql
SELECT 

 [MISSION_SID]
,[MISSION_ID]

FROM [dbo].[D_CCEM_MISSION]
order by 2
```

Context: This SQL query retrieves data from the D_CCEM_MISSION dimension table.

```sql
SELECT  

    [ARREST_PRISONER_SID]
      , coalesce( [CASE_ID],'-3') as [CASE_ID]
      , coalesce([ARREST_ID],'-3') as [ARREST_ID]
      , coalesce([ARREST_TRANSFER_ID],'-3') as [ARREST_TRANSFER_ID]
      , coalesce([ARREST_ACTIVITY_ID],'-3') as [ARREST_ACTIVITY_ID]
     
  FROM [dbo].[D_CCEM_ARREST_PRISONER]

order by 2,3, 4, 5
```

Context: This SQL query retrieves data from the D_CCEM_ARREST_PRISONER dimension table.

```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: This SQL query retrieves data from the `D_CCEM_CLIENT` dimension table.

```sql
SELECT 
 [COUNTRY_SID]
 ,[COUNTRY_ID]

FROM [dbo].[D_CCEM_COUNTRY]
order by 2
```

Context: This SQL query retrieves data from the `D_CCEM_COUNTRY` dimension table.

```sql
SELECT case when [DATE_SID] = -3 then '-3'
       else cast([DATE] as varchar) end as INPUT_CD,
	   [DATE_SID] as OUTPUT_SID

  FROM [dbo].[D_CALENDAR_DATE]
order by 1
```

Context: This SQL query retrieves data from the `D_CALENDAR_DATE` dimension table for visit dates.

```sql
SELECT distinct   

	  coalesce(ar.[CASE_ID] ,'-3') as [CASE_ID_LU]
	 ,coalesce(ar.[ARREST_ID] ,'-3') as [ARREST_ID_LU]
	 ,coalesce(ar.[ARREST_TRANSFER_ID] ,'-3') as [ARREST_TRANSFER_ID_LU]
	 ,coalesce(ar.[ARREST_ACTIVITY_ID] ,'-3') as [ARREST_ACTIVITY_ID_LU]
	 ,coalesce(cli.[CONTACT_ID] ,'-3') as [CONTACT_ID_LU]
	 ,coalesce(m.[MISSION_ID] ,'-3') as [MISSION_CD_LU]
	 ,coalesce(m.[SUPERVISING_MISSION_ID] ,'-3') as [SUPERV_MISSION_CD_LU]
	 ,coalesce(c.[COUNTRY_ID] ,'-3') as [COUNTRY_CD_LU]
	 ,coalesce(cast(cast(ar.[VISIT_START_DT] as date)as varchar),'-3') as [VISIT_DT_LU]
	 ,coalesce(ar.[PRISON_ID] ,'-3') as [PRISON_ID_LU]
	 
	 

      ,cast(ar.[DETENTION_START_DT] as date) as [DETENTION_START_DT] 
      ,cast(ar.[DETENTION_END_DT] as date) as [DETENTION_END_DT]	 
      ,ar.[DISTINCT_PRISONER_CNT]
      ,ar.[VISIT_CNT]
      ,cast(ar.[VISIT_START_DT] as date ) as [VISIT_DT]

	  ,ar.LATEST_DETENTION_IND
	  ,ar.LATEST_VISIT_IND
	  ,subc.SUBCATEGORY_NBR
	  ,coalesce(ar.CREATED_BY_ID_ACTIV, ar.CREATED_BY_ID_TRANS) as [EMPLOYEE_ID]

      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
	  

  
  FROM [dbo].[CCEM_ARREST_DETENTION] ar
  

LEFT JOIN dbo.CCEM_CASE c
ON ar.CASE_ID = c.CASE_ID

LEFT JOIN dbo.CCEM_SUBCATEGORY subc
ON c.SUBCATEGORY_ID=subc.SUBCATEGORY_NBR

LEFT JOIN dbo.CCEM_MISSION m
ON c.MISSION_ID=m.MISSION_ID

LEFT JOIN dbo.CCEM_CLIENT cli
ON ar.ARR_CONTACT=cli.CONTACT_ID

order by 1, 2, 3, 4
```

Context: This SQL query is used to extract data from the CCEM_ARREST_DETENTION staging table.

```sql
TRUNCATE TABLE F_CCEM_ARREST_DETENTION;
```

Context: SQL command used to truncate the destination fact table.

```sql
SELECT 

 [MISSION_SID]
,[MISSION_ID]

FROM [dbo].[D_CCEM_MISSION]
order by 2
```

Context: Extracting mission data.
```sql
SELECT case when [DATE_SID] = -3 then '-3'
       else cast([DATE] as varchar) end as INPUT_CD,
	   [DATE_SID] as OUTPUT_SID

  FROM [dbo].[D_CALENDAR_DATE]
order by 1
```

Context: calendar data.
```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: calendar data.

```sql
SELECT  [EMPLOYEE_SID]
      ,[EMPLOYEE_ID]
    
  FROM [dbo].[D_CCEM_EMPLOYEE]
```

Context: dimension employee query.

```sql
SELECT  [SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
   
  FROM [dbo].[D_CCEM_SUBCATEGORY]
```

Context: dimension query.

```sql
SELECT 

 [CASE_SID]
   
      ,[CASE_ID]
    
  FROM [dbo].[D_CCEM_CASE]
order by 2
```

Context: dimension query.

```sql
SELECT 

 [MISSION_SID]
,[MISSION_ID]

FROM [dbo].[D_CCEM_MISSION]
order by 2
```

Context: dimension query.

```sql
SELECT  [EMPLOYEE_SID]
      ,[EMPLOYEE_ID]
    
  FROM [dbo].[D_CCEM_EMPLOYEE]
```

Context: dimension query.

```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: dimension query.

```sql
SELECT  [SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
   
  FROM [dbo].[D_CCEM_SUBCATEGORY]
```

Context: dimension query.

```sql
SELECT  [EMPLOYEE_SID]
      ,[EMPLOYEE_ID]
    
  FROM [dbo].[D_CCEM_EMPLOYEE]
```

Context: dimension query.

```sql
SELECT 

 [MISSION_SID]
,[MISSION_ID]

FROM [dbo].[D_CCEM_MISSION]
order by 2
```

Context: dimension query.

```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: dimension query.

```sql
SELECT  [SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
   
  FROM [dbo].[D_CCEM_SUBCATEGORY]
```

Context: dimension query.

```sql
TRUNCATE TABLE F_CCEM_CRISIS;
```

Context: SQL command used to truncate the destination fact table.

```sql
SELECT 
 [COUNTRY_SID]
 ,[COUNTRY_ID]

FROM [dbo].[D_CCEM_COUNTRY]
order by 2
```

Context: Calendar dimension query.

```sql
SELECT 
 [COUNTRY_SID]
 ,[COUNTRY_ID]

FROM [dbo].[D_CCEM_COUNTRY]
order by 2
```

Context: Calendar dimension query.

```sql
SELECT case when [DATE_SID] = -3 then '-3'
       else cast([DATE] as varchar) end as INPUT_CD,
	   [DATE_SID] as OUTPUT_SID

  FROM [dbo].[D_CALENDAR_DATE]
order by 1
```

Context: Calendar dimension query.

```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: Calendar dimension query.

```sql
TRUNCATE TABLE F_CCEM_DEPARTURE;
```

Context: SQL command used to truncate the destination fact table.

```sql
SELECT 
 [COUNTRY_SID]
 ,[COUNTRY_ID]

FROM [dbo].[D_CCEM_COUNTRY]
order by 2
```

Context: Calendar dimension query.
```sql
SELECT case when [DATE_SID] = -3 then '-3'
       else cast([DATE] as varchar) end as INPUT_CD,
	   [DATE_SID] as OUTPUT_SID

  FROM [dbo].[D_CALENDAR_DATE]
order by 1
```

Context: Calendar dimension query.

```sql
SELECT 

 [CLIENT_SID]
,[CONTACT_ID]
      
  FROM [dbo].[D_CCEM_CLIENT]
order by 2
```

Context: Calendar dimension query.

```sql
TRUNCATE TABLE DBO.F_CCEM_SLA;
```

Context: SQL command used to truncate the destination fact table.

```sql
select 
 
 (select date_sid from dbo.D_CALENDAR_DATE where [DATE]=cast(getdate() as date) ) as [DATE_SID]
,[COUNTRY_SID]
,sum( REGISTRANT_CNT) as [REGISTRANT_CNT]
,sum( FAMILY_REGISTRANT_CNT) as [FAMILY_REGISTRANT_CNT]
,sum( CANADIAN_REGISTRANT_CNT) as [CANADIAN_REGISTRANT_CNT]
,0 as [REGISTRANT_INCREASE_CNT]
,0 as [FAMILY_REGISTRANT_INCREASE_CNT]
,0 as [CANADIAN_REGISTRANT_INCREASE_CNT]
,getdate() as [ETL_CREA_DT]
,getdate() as [ETL_UPDT_DT]

from dbo.[F_CCEM_REGISTRATION]
group by country_sid
```

Context: SQL query for F_CCEM_REGISTRATION_AGG.
```sql
delete from [F_CCEM_REGISTRATION_AGG] where [DATE_SID] =  (Select DATE_SID from [D_CALENDAR_DATE] where [DATE]=cast(getdate() as date) ) ;
```

Context: SQL query for F_CCEM_REGISTRATION_AGG.
```sql
--This scritp is used to calculate the count increase
--Run the script in a SQL task in SSIS ETL package , set the OLE DB to MART_CCEM Connection Manager
IF EXISTS (SELECT * 
           FROM   sys.OBJECTS 
           WHERE  OBJECT_ID = Object_id(N'[dbo].[#temp_recent_load]') 
                  AND TYPE IN ( N'U' )) 
  DROP TABLE [dbo].#TEMP_RECENT_LOAD 

IF EXISTS (SELECT * 
           FROM   sys.OBJECTS 
           WHERE  OBJECT_ID = Object_id(N'[dbo].[#temp_last_load]') 
                  AND TYPE IN ( N'U' )) 
  DROP TABLE [dbo].#TEMP_LAST_LOAD 

IF EXISTS (SELECT * 
           FROM   sys.OBJECTS 
           WHERE  OBJECT_ID = Object_id(N'[dbo].#temp_increase_count') 
                  AND TYPE IN ( N'U' )) 
  DROP TABLE [dbo].#TEMP_INCREASE_COUNT 

SELECT [DATE_SID], 
       [COUNTRY_SID], 
       [REGISTRANT_CNT], 
       [FAMILY_REGISTRANT_CNT], 
       [CANADIAN_REGISTRANT_CNT] 
INTO   #temp_recent_load 
FROM   [dbo].[F_CCEM_REGISTRATION_AGG] 
WHERE  [DATE_SID] = (SELECT Max(DATE_SID) 
                     FROM   [dbo].[F_CCEM_REGISTRATION_AGG]) 

SELECT [DATE_SID], 
       [COUNTRY_SID], 
       [REGISTRANT_CNT], 
       [FAMILY_REGISTRANT_CNT], 
       [CANADIAN_REGISTRANT_CNT] 
INTO   #temp_last_load 
FROM   [dbo].[F_CCEM_REGISTRATION_AGG] 
WHERE  [DATE_SID] = (SELECT Max(DATE_SID) 
                     FROM   [dbo].[F_CCEM_REGISTRATION_AGG] 
                     WHERE  DATE_SID < (SELECT TOP 1 DATE_SID 
                                        FROM   #temp_recent_load)) 

SELECT r.[DATE_SID], 
       r.[COUNTRY_SID], 
       r.[REGISTRANT_CNT] - COALESCE(t.[REGISTRANT_CNT], 0)                   AS 
       [REGISTRANT_INCREASE_CNT], 
       r.[FAMILY_REGISTRANT_CNT] - COALESCE(t.[FAMILY_REGISTRANT_CNT], 0)     AS 
       [FAMILY_REGISTRANT_INCREASE_CNT], 
       r.[CANADIAN_REGISTRANT_CNT] - COALESCE(t.[CANADIAN_REGISTRANT_CNT], 0) AS 
       [CANADIAN_REGISTRANT_INCREASE_CNT] 
INTO   #temp_increase_count 
FROM   #temp_recent_load r 
       LEFT OUTER JOIN #temp_last_load t 
                    ON r.COUNTRY_SID = t.COUNTRY_SID 

MERGE INTO [dbo].[F_CCEM_REGISTRATION_AGG] a 
using #temp_increase_count b 
ON a.[DATE_SID] = B.[DATE_SID] 
   AND a.[COUNTRY_SID] = B.[COUNTRY_SID] 
WHEN matched THEN 
  UPDATE SET a.[REGISTRANT_INCREASE_CNT] = b.[REGISTRANT_INCREASE_CNT], 
a.[FAMILY_REGISTRANT_INCREASE_CNT] = b.[FAMILY_REGISTRANT_INCREASE_CNT], 
a.[CANADIAN_REGISTRANT_INCREASE_CNT] = b.[CANADIAN_REGISTRANT_INCREASE_CNT]; 
```

Context: SQL query for F_CCEM_REGISTRATION_AGG.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.REJECT_CCEM_MASTER  | Stores rejected rows with reasons   | Part 1 |
| dbo.F_CCEM_ARREST_DETENTION   | Stores arrest detention data              | Part 1      |
| dbo.F_CCEM_CRISIS  | Stores crisis data              | Part 1      |
| dbo.F_CCEM_DEPARTURE   | Stores departure data              | Part 1      |
| dbo.F_CCEM_REGISTRATION  | Stores registration data              | Part 1      |
| dbo.F_CCEM_REGISTRATION_AGG  | Stores registration aggregation data              | Part 1      |
| dbo.F_CCEM_ACTIVITY   | Stores activity data              | Part 1      |
| dbo.F_CCEM_CASE  | Stores case data              | Part 1      |

## 6. Package Summary

*   **Input Connections:** 3
*   **Output Destinations:** 9
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 2
    *   Sequence Containers: 7
    *   Data Flow Tasks: 9
    *   Execute SQL Tasks: 8
    *   Derived column transformations: 1
    *   Lookup transformations: 13
*   **Overall package complexity assessment:** High
*   **Potential performance bottlenecks:** The multiple full-cache lookup transformations and merge joins could be performance bottlenecks, especially with large datasets. Check data skew, indexing, and memory usage.
*   **Critical path analysis:** The critical path likely involves the largest data flow tasks (i.e., the fact table loads).
*   **Error handling mechanisms:** Fail component, Ignore Failure. The package has an OnError event handler that updates the ETL process status to 'FAILED'.
