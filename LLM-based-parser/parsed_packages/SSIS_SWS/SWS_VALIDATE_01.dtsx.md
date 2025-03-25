```markdown
## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---|---|---|---|---|---|---|
| MART_GC | OLE DB | Server: [Inferred], Database: [Inferred] | Destination for CFO Stats data | SQL Server Auth likely | None Explicitly Defined | Part 2, 3 |
| ETL_STG_MART_GC | OLE DB | Server: [Inferred], Database: [Inferred] | Source for staging data | SQL Server Auth likely | None Explicitly Defined | Part 2, 3 |
| (4382894D-116E-46C6-BEBD-4E4EFACB27AE) | OLE DB | Server: [Inferred], Database: [Inferred] | Used to update ETL status in event handlers | SQL Server Auth likely | None Explicitly Defined | Part 4 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|---|---|---|---|---|---|
| None Found |  |  |  | No dependent SSIS packages tasks found | Part 1, 2, 3, 4 |

## 3. Package Flow Analysis

* The package starts with an Expression Task `Start Task Each branch depends on value in package parameter - ProcessDataFlowNode`.
* Three tasks are conditionally executed based on the outcome of the Expression Task: `SEQC_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK`, `SEQC_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL`, and `SEQC_Q_CFO_STATS_DETAIL_COMPAIRSON`. Each is a sequence container.

#### SEQC_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK

*   Contains an Execute SQL Task `ESQL_Loading_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK` that executes the stored procedure `SP_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK`.

#### SEQC_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL

*   Contains an Execute SQL Task `ESQL_Loading_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL` that executes the stored procedure `SP_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL`.

#### SEQC_Q_CFO_STATS_DETAIL_COMPAIRSON

*   This sequence container performs a comparison between current and previous snapshots of CFO stats data.
*   It truncates tables, loads current data from the `F_GC_FINANCIAL_CFO_STATS` table into the `S_PS_CFO_STATS_GC_FINAN_SUM_CURR` staging table, and then loads the previous snapshot data into the `S_PS_CFO_STATS_GC_FINAN_SUM_PREV` staging table.
*   It identifies new, modified, and deleted records and loads them into the `Q_CFO_STATS_DETAIL_COMPAIRSON` table.

##### DFT_S_PS_CFO_STATS_GC_FINAN_SUM_CURR

*   **Source:** `OLEDB_SRC_F_GC_FINANCIAL_CFO_STATS` extracts data from `dbo.F_GC_FINANCIAL_CFO_STATS`
*   **Transformations:**
    *   Aggregation occurs based on several columns.
*   **Destination:** `OLEDB_DEST_S_PS_CFO_STATS_GC_FINAN_SUM_CURR` saves successfully transformed rows to `dbo.S_PS_CFO_STATS_GC_FINAN_SUM_CURR`.

##### DFT_S_PS_CFO_STATS_GC_FINAN_SUM_PREV
*   **Source:** `OLEDB_SRC_F_GC_FINANCIAL_CFO_STATS` extracts data from `dbo.S_PS_CFO_STATS_GC_FINAN`
*   **Transformations:**
    *   None
*   **Destination:** `OLEDB_DEST_S_PS_CFO_STATS_GC_FINAN_SUM_PREV` saves successfully transformed rows to `dbo.S_PS_CFO_STATS_GC_FINAN_SUM_PREV`.

##### DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_NEW

*   **Source:** `OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN` executes a SQL query to identify records that exist only in the current snapshot.
*   **Transformations:**
    *   None
*   **Destination:** `OLEDB_DEST_Q_CFO_STATS_DETAIL_COMPAIRSON` saves successfully transformed rows to `dbo.Q_CFO_STATS_DETAIL_COMPAIRSON`.

##### DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_NOT_EXIST
*   **Source:** `OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN` executes a SQL query to identify records that exist only in the previous snapshot.
*   **Transformations:**
    *   None
*   **Destination:** `OLEDB_DEST_Q_CFO_STATS_DETAIL_COMPAIRSON` saves successfully transformed rows to `dbo.Q_CFO_STATS_DETAIL_COMPAIRSON`.

##### DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_MODIFIED
*   **Source:** `OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN` executes a SQL query to identify records that exist in both current and previous snapshot with differences and flags them as modified.
*   **Transformations:**
    *   None
*   **Destination:** `OLEDB_DEST_Q_CFO_STATS_DETAIL_COMPAIRSON` saves successfully transformed rows to `dbo.Q_CFO_STATS_DETAIL_COMPAIRSON`.

## 4. Code Extraction

```sql
-- From OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN in DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_MODIFIED
SELECT  PREV.[WBS_NBR]
      ,PREV.[FISCAL_YEAR]
	  ,PREV.CY
      ,PREV.[NEW_VENDOR_NBR]
      ,PREV.[FLOW_TYPE_CD]
      ,PREV.[FUND_NBR]
      ,PREV.[GAC_COUNTRY_CD]
	  , PREV.DAC_SECTOR_LEVEL3_CD
--	  ,PREV.[NEW_DISBURSEMENT_AMT]
--	  ,PREV.[NEW_BUDGET_AMT]
	  ,ISNULL(CURR.[NEW_DISBURSEMENT_AMT],0.0)  - ISNULL(PREV.[NEW_DISBURSEMENT_AMT],0.0) AS DIFF_NEW_DISBURSEMENT_AMT
	  ,ISNULL(CURR.[NEW_BUDGET_AMT],0.0)  - ISNULL(PREV.[NEW_BUDGET_AMT],0.0)  AS DIFF_NEW_BUDGET_AMT
	  ,'MODIFIED' AS FLAG
       ,'CASE3-This record exist in the Current and Previous Snapshot with differences in the Amount'  AS HK_DIFF_DESCR	   
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
	  	  ,LOAD_DT =(SELECT Cast(Max(ETL_CREA_DT) AS DATE)  as LOAD_DT
                         FROM   [MART_GC].[dbo].[F_GC_FINANCIAL_CFO_STATS] )
    ,ETL_RUN_STATUS_ID = (SELECT [ETL_RUN_STATUS_ID]
                                FROM   [DW_ADMIN].[dbo].[ETL_RUN_STATUS] R
                                       LEFT OUTER JOIN
                                       [DW_ADMIN].[dbo].ETL_COMPONENT
                                       E
                                                    ON R.ETL_COMPONENT_ID =
                                                       E.ETL_COMPONENT_ID
                                WHERE  ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
                                       AND [ETL_RUN_MAIN_COMPONENT_IND] = 1
                                       AND [ETL_RUN_STATUS_DESC] = 'RUNNING')
FROM ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN_SUM_CURR CURR
 JOIN ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN_SUM_PREV PREV
ON CURR.[WBS_NBR]=PREV.[WBS_NBR]
   AND CURR.[FISCAL_YEAR]=PREV.[FISCAL_YEAR]
	AND CURR.CY=PREV.CY
   AND CURR.[NEW_VENDOR_NBR]=PREV.[NEW_VENDOR_NBR]
   AND CURR.[FLOW_TYPE_CD]=PREV.[FLOW_TYPE_CD]
   AND CURR.[FUND_NBR]=PREV.[FUND_NBR]
   AND CURR.[GAC_COUNTRY_CD]=PREV.[GAC_COUNTRY_CD]
	AND CURR. DAC_SECTOR_LEVEL3_CD=PREV.DAC_SECTOR_LEVEL3_CD
WHERE 	ABS(ISNULL(CURR.[NEW_DISBURSEMENT_AMT],0.0)  - ISNULL(PREV.[NEW_DISBURSEMENT_AMT],0.0)) >1 
	  OR ABS(ISNULL(CURR.[NEW_BUDGET_AMT],0.0)  - ISNULL(PREV.[NEW_BUDGET_AMT],0.0) ) > 1
```

This SQL query is used to identify modified records based on amount differences.
```sql
-- From OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN in DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_NEW
SELECT  CURR.[WBS_NBR] AS [WBS_NBR]
      ,CURR.[FISCAL_YEAR]  AS [FISCAL_YEAR]
	  ,CURR.CY AS CY 
      ,CURR.[NEW_VENDOR_NBR] AS [NEW_VENDOR_NBR]
      ,CURR.[FLOW_TYPE_CD] AS [FLOW_TYPE_CD]
      ,CURR.[FUND_NBR] AS [FUND_NBR]
      ,CURR.[GAC_COUNTRY_CD] AS [GAC_COUNTRY_CD]
	  , CURR.DAC_SECTOR_LEVEL3_CD AS DAC_SECTOR_LEVEL3_CD
	  ,CURR.[NEW_DISBURSEMENT_AMT] AS [NEW_DISBURSEMENT_AMT]
	  ,CURR.[NEW_BUDGET_AMT] AS [NEW_BUDGET_AMT]
	  ,'NEW' AS FLAG
       ,'CASE1-This record does not exist in the Previous Snapshot' AS HK_DIFF_DESCR	   
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
	  ,LOAD_DT =(SELECT Cast(Max(ETL_CREA_DT) AS DATE)  as LOAD_DT
                         FROM   [MART_GC].[dbo].[F_GC_FINANCIAL_CFO_STATS] )
    ,ETL_RUN_STATUS_ID = (SELECT [ETL_RUN_STATUS_ID]
                                FROM   [DW_ADMIN].[dbo].[ETL_RUN_STATUS] R
                                       LEFT OUTER JOIN
                                       [DW_ADMIN].[dbo].ETL_COMPONENT
                                       E
                                                    ON R.ETL_COMPONENT_ID =
                                                       E.ETL_COMPONENT_ID
                                WHERE  ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
                                       AND [ETL_RUN_MAIN_COMPONENT_IND] = 1
                                       AND [ETL_RUN_STATUS_DESC] = 'RUNNING')
FROM dbo.S_PS_CFO_STATS_GC_FINAN_SUM_CURR CURR
LEFT OUTER JOIN ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN_SUM_PREV PREV
ON CURR.[WBS_NBR]=PREV.[WBS_NBR]
   AND CURR.[FISCAL_YEAR]=PREV.[FISCAL_YEAR]
	AND CURR.CY=PREV.CY
   AND CURR.[NEW_VENDOR_NBR]=PREV.[NEW_VENDOR_NBR]
   AND CURR.[FLOW_TYPE_CD]=PREV.[FLOW_TYPE_CD]
   AND CURR.[FUND_NBR]=PREV.[FUND_NBR]
   AND CURR.[GAC_COUNTRY_CD]=PREV.[GAC_COUNTRY_CD]
	AND CURR. DAC_SECTOR_LEVEL3_CD=PREV.DAC_SECTOR_LEVEL3_CD
WHERE PREV.[WBS_NBR] IS NULL
```

This SQL query is used to identify new records that do not exist in the previous snapshot.

```sql
-- From OLEDB_SRC_S_PS_CFO_STATS_GC_FINAN in DFT_Q_CFO_STATS_DETAIL_COMPAIRSON_NOT_EXIST
SELECT PREV.[WBS_NBR]
      ,PREV.[FISCAL_YEAR]
	  ,PREV.CY
      ,PREV.[NEW_VENDOR_NBR]
      ,PREV.[FLOW_TYPE_CD]
      ,PREV.[FUND_NBR]
      ,PREV.[GAC_COUNTRY_CD]
	  , PREV.DAC_SECTOR_LEVEL3_CD
	  ,PREV.[NEW_DISBURSEMENT_AMT]
	  ,PREV.[NEW_BUDGET_AMT]
	  ,'NOT EXIST' AS FLAG
       ,'CASE2-This record does not exist in the Current Snapshot' AS HK_DIFF_DESCR	   
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
	  	  ,LOAD_DT =(SELECT Cast(Max(ETL_CREA_DT) AS DATE)  as LOAD_DT
                         FROM  ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN )
    ,ETL_RUN_STATUS_ID = (SELECT [ETL_RUN_STATUS_ID]
                                FROM   [DW_ADMIN].[dbo].[ETL_RUN_STATUS] R
                                       LEFT OUTER JOIN
                                       [DW_ADMIN].[dbo].ETL_COMPONENT
                                       E
                                                    ON R.ETL_COMPONENT_ID =
                                                       E.ETL_COMPONENT_ID
                                WHERE  ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
                                       AND [ETL_RUN_MAIN_COMPONENT_IND] = 1
                                       AND [ETL_RUN_STATUS_DESC] = 'RUNNING')
FROM ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN_SUM_CURR CURR
RIGHT OUTER JOIN ETL_STG_MART_GC.dbo.S_PS_CFO_STATS_GC_FINAN_SUM_PREV PREV
ON CURR.[WBS_NBR]=PREV.[WBS_NBR]
   AND CURR.[FISCAL_YEAR]=PREV.[FISCAL_YEAR]
	AND CURR.CY=PREV.CY
   AND CURR.[NEW_VENDOR_NBR]=PREV.[NEW_VENDOR_NBR]
   AND CURR.[FLOW_TYPE_CD]=PREV.[FLOW_TYPE_CD]
   AND CURR.[FUND_NBR]=PREV.[FUND_NBR]
   AND CURR.[GAC_COUNTRY_CD]=PREV.[GAC_COUNTRY_CD]
	AND CURR. DAC_SECTOR_LEVEL3_CD=PREV.DAC_SECTOR_LEVEL3_CD
WHERE CURR.[WBS_NBR] IS NULL
```

This SQL query is used to identify records that do not exist in the current snapshot.

```sql
-- From OLEDB_SRC_F_GC_FINANCIAL_CFO_STATS in DFT_S_PS_CFO_STATS_GC_FINAN_SUM_CURR
SELECT  [WBS_NBR]
      ,[FISCAL_YEAR]
	  ,CY
      ,[NEW_VENDOR_NBR]
      ,[FLOW_TYPE_CD]
      ,[FUND_NBR]
      ,[GAC_COUNTRY_CD]
	  ,ISNULL(D.DAC_SECTOR_LEVEL3_CD,'-3') AS DAC_SECTOR_LEVEL3_CD
      ,SUM([NEW_DISBURSEMENT_AMT]) AS [NEW_DISBURSEMENT_AMT]
      ,SUM([NEW_BUDGET_AMT]) AS [NEW_BUDGET_AMT]
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
  FROM [dbo].[F_GC_FINANCIAL_CFO_STATS] F
  left outer join [dbo].[D_SECTOR] D
  ON F.SECTOR_LEVEL_3_SID = D.SECTOR_SID
  WHERE [SAP_MERGE_SOURCE_CD] <> 'OGD'
  GROUP BY [WBS_NBR]
      ,[FISCAL_YEAR]
	  ,CY
      ,[NEW_VENDOR_NBR]
      ,[FLOW_TYPE_CD]
      ,[FUND_NBR]
      ,[GAC_COUNTRY_CD]
	  ,ISNULL(D.DAC_SECTOR_LEVEL3_CD,'-3')
```

This SQL query is used to extract data from the F_GC_FINANCIAL_CFO_STATS table.
```sql
-- From OLEDB_SRC_F_GC_FINANCIAL_CFO_STATS in DFT_S_PS_CFO_STATS_GC_FINAN_SUM_PREV
SELECT  [WBS_NBR]
      ,[FISCAL_YEAR]
	  ,CY
      ,[NEW_VENDOR_NBR]
      ,[FLOW_TYPE_CD]
      ,[FUND_NBR]
      ,[GAC_COUNTRY_CD]
	  , DAC_SECTOR_LEVEL3_CD
      ,SUM([NEW_DISBURSEMENT_AMT]) AS [NEW_DISBURSEMENT_AMT]
      ,SUM([NEW_BUDGET_AMT]) AS [NEW_BUDGET_AMT]
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
  FROM dbo.S_PS_CFO_STATS_GC_FINAN 
  GROUP BY [WBS_NBR]
      ,[FISCAL_YEAR]
	  ,CY
      ,[NEW_VENDOR_NBR]
      ,[FLOW_TYPE_CD]
      ,[FUND_NBR]
      ,[GAC_COUNTRY_CD]
	  ,DAC_SECTOR_LEVEL3_CD
```

This SQL query is used to extract data from the dbo.S_PS_CFO_STATS_GC_FINAN table.

```sql
-- From ESQL_Truncate_tables_in_ETL_STG_MART_GC
TRUNCATE TABLE S_PS_CFO_STATS_GC_FINAN_SUM_PREV
TRUNCATE TABLE [S_PS_CFO_STATS_GC_FINAN_SUM_CURR]
```

This SQL query is used to truncate two staging tables.

```sql
-- From ESQL_Loading_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK
execute SP_Q_CFO_STATS_BUDGET_DISB_SUMMARY_TRACK
```

This SQL query is used to execute a stored procedure.

```sql
-- From ESQL_Loading_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL
EXECUTE SP_Q_DIFF_SRC_VS_TRGT_BUDGET_DISB_DETAIL;
```

This SQL query is used to execute a stored procedure.

```
-- From ESQLT- Update ETL Process Status to Failed in Event Handler OnError
User::V_SQL_UPDATE_ON_ERROR
```

This SQL statement which is stored in a variable is used to update the ETL status to failed.

```
-- From ESQLT- Update ETL Process Status to Succeeded in Event Handler OnPostExecute
User::V_SQL_UPDATE_ON_POST_EXECUTE
```

This SQL statement which is stored in a variable is used to update the ETL status to succeeded.

```
-- From ESQLT- Create Record  with Running Status in Event Handler OnPreExecute
User::V_SQL_INSERT_ON_PRE_EXECUTE
```

This SQL statement which is stored in a variable is used to insert a record with running status.

```
-- User::V_SQL_UPDATE_ON_ERROR
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'SWS_VALIDATE_01.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

This SQL query updates ETL_RUN_STATUS to FAILED on error.

```
-- User::V_SQL_UPDATE_ON_POST_EXECUTE
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'SWS_VALIDATE_01.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

This SQL query updates ETL_RUN_STATUS to SUCCEEDED on post execute.

```
-- User::V_SQL_INSERT_ON_PRE_EXECUTE
INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )
VALUES (
 (
  SELECT ETL_COMPONENT_ID
  FROM ETL_COMPONENT
  WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'   
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS'   
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'SWS_GC_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/SWS' 
    )
   AND ETL_SUB_COMPONENT_NM = 'SWS_VALIDATE_01.DTSX'   
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

This SQL query inserts a record into ETL_RUN_STATUS with a RUNNING status on pre execute.

## 5. Output Analysis

| Destination Table | Description | Source Part |
|---|---|---|
| `dbo.Q_CFO_STATS_DETAIL_COMPAIRSON` | Stores new, modified, or deleted records | Part 2 |
| `dbo.S_PS_CFO_STATS_GC_FINAN_SUM_CURR` | Staging table for current CFO stats data | Part 2 |
| `dbo.S_PS_CFO_STATS_GC_FINAN_SUM_PREV` | Staging table for previous CFO stats data | Part 2 |

## 6. Package Summary

*   **Input Connections:** 2 Data Connections + 1 audit connection
*   **Output Destinations:** `Q_CFO_STATS_DETAIL_COMPAIRSON`,  `S_PS_CFO_STATS_GC_FINAN_SUM_CURR`, `S_PS_CFO_STATS_GC_FINAN_SUM_PREV`
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 3
    *   Data Flow Tasks: 5
    *   Execute SQL Tasks: 5
    *   Expression Task: 3
*   **Overall package complexity assessment:** Medium
*   **Potential performance bottlenecks:** Data Flow Tasks involving large datasets, Stored Procedures.
*   **Critical path analysis:** The Sequence Container `SEQC_Q_CFO_STATS_DETAIL_COMPAIRSON` appears to be on the critical path.
*   **Document error handling mechanisms:** The package uses an `OnError` event handler to update an ETL status table. It also uses `OnPreExecute` and `OnPostExecute` event handlers to record the status of the package execution.
```