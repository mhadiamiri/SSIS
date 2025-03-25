```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| ODS_SAP           | OLE DB          | Server: Not available, Database: Not Available  | Source for data extraction in Data Flow Tasks. | Credentials likely required to access the ODS_SAP database. | None | Part 1, 2, 3, 4                  |
| DATA_HUB           | OLE DB          | Server: Not available, Database: Not Available  | Destination for data loading in Data Flow Tasks. Also used for ETL run status logging. | Credentials likely required to access the DATA_HUB database. | None            | Part 1, 2, 3, 4                 |
| ETL_STG_DATA_HUB           | OLE DB          | Server: Not available, Database: Not Available  | Used as destination to write staging tables | Credentials likely required to access the ETL_STG_DATA_HUB database.  | None            | Part 1                  |
| ODS_GC_SOURCE_DB           | OLE DB          | Server: Not available, Database: Not Available  | Used as source for data in GCS | Credentials likely required to access the ODS_GC_SOURCE_DB database.  | `User::V_GCS_SRC_QRY__SAP_PROJECT_HIERARCHY`            | Part 1, 3                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| DATA_HUB_03_PROJECT_BUDGET.dtsx |  Relative Path | Child: Executed by `EXEC-PKG-DATA_HUB_PROJECT_BUDGET` | None specified in the XML. |  Need to verify that the relative path resolves correctly during deployment. | Part 1|
| DATA_HUB_02_PROJECT_WBS.dtsx | Relative Path | Child: Executed by `EXEC-PKG-DATA_HUB_PROJECT_WBS` | None specified in the XML. |  Need to verify that the relative path resolves correctly during deployment. | Part 1|

## 3. Package Flow Analysis

**Control Flow:**

The control flow is organized into Sequence Containers, defining logical units of work. Key containers include:

1.  `ESQLT-Delete FAS data and Truncate table`:  Likely the first task, responsible for cleaning up existing data. (Part 1)
2.  `SEQC-GCS-FAS_MERGE-STAGING TABLE`: Sequence container that loads staging table. (Part 1)
    *   `ESQLT-TRUNCATE - S_SAP_GCS_FAS_WBS_MAP` Truncates staging table (Part 1)
    *    `DFT-S_SAP_GCS_FAS_WBS_MAP` Loads the staging table (Part 1)
3.  `SEQC-Load SAP_ACCOUNTING_COCUMENT`: Sequence container that loads accounting document data. (Part 1)
    *   `ESQLT-Drop_Index_In_Three_tables`: Drop indexes in target tables (Part 1)
    *   `ESQL_Load_SAP_ACCOUNTING_DOCUMENT_LINE_ITEM` Load data to S_SAP_ACCOUNTING_DOCUMENT_LINE_ITEM (Part 1)
    *    `ESQLT-Recreate_Index_In_Tow_Tables` Re-Create Indexes In Two Tables (Part 1)
    *   `DFT-SAP_UNIFIED_COMMITMENT_PAYMENTS` Load  SAP_UNIFIED_COMMITMENT_PAYMENTS (Part 1)
    *   `ESQLT-POPULATE ACT DOC ITEM - WBS NBR`: Updates `WBS_NBR` in `SAP_ACCOUNTING_DOCUMENT_LINE_ITEM`. (Part 1)
    *   `ESQLT-Recreate_Index_In_One_Table` Re-Create Indexes in one table (Part 1)
4. `SEQC-DPI-Load_DATA_HUB`: Sequence container that loads project documents (Part 1)
    *    `ESQLT-Load DATA_HUB DPI Code Tables`: Load code tables (Part 1)
    *    `DFT-SAP_PROJECT_DOCUMENT_CATEGORY`: Loads project documents (Part 1)
    *    `DFT-SAP_PROJECT_DOCUMENT_RESPONSIBILITY`: Loads project document resposibility (Part 1)
5.  `EXEC-PKG-DATA_HUB_PROJECT_WBS`: Executes child package `DATA_HUB_02_PROJECT_WBS.dtsx`. (Part 1)
6.  `EXEC-PKG-DATA_HUB_PROJECT_BUDGET`: Executes child package `DATA_HUB_03_PROJECT_BUDGET.dtsx`. (Part 1)
7.  `EXPRESSIONT_DHUB-Start Task Each branch depends on value in package parameter - ProcessDataFlowNode` (Part 1)
    -   `DFT-SAP_ACCOUNTING_DOCUMENT_LINE_ITEM used Join Task`:  Data flow task, currently disabled. (Part 1)
8.  `SEQC-Load\_DATA\_HUB\_BUDGET\_ALLOCATION` (Part 2)
9.  `SEQC-Load\_DATA\_HUB\_CODE\_TABLES` (Part 2)
10. `SEQC-LOAN\_INITIATIVES` (Part 2)
11. `SEQC-PROJECT WBS` (Part 2, 3)
    *   `SEQC-SAP_PROJECT_FINANCE` (Part 2)
    *   `SEQC-SAP_PROJECT_HIERARCHY` (Part 2, 3)
    *   `SEQC-SAP_PROJECT_PDS_ALLOCATION` (Part 3)
    *   `SEQC-SAP_PROJECT_WBS` (Part 3)
12. `SEQC-SAP_ACCOUNTING_DOCUMENT_LINE_ITEM-WBS-NBR UPDATE-dec22` (disabled) (Part 3)

**Data Flow Tasks:**

*   **DFT-SAP_ACCOUNTING_DOCUMENT_LINE_ITEM used Join Task (Disabled):** (Part 1)
    *   **Source:** `OLE DB _ODS_SAP_BSEG` and `OLE DB _ODS_DEEMED_VENDOR` (Part 1)
    *   **Transformations:**  `Merge Join`, `Derived Column_Remove "zzzz"`, `Derived Column_Remove_Blank` (Part 1)
    *   **Destination:** `OLEDB_SAP_ACCOUNTING_DOCUMENT_LINE_ITEM_ALL` (Part 1)
    *   **Error Handling:** `FailComponent` is set for error rows in `Derived Column_Remove "zzzz"`. (Part 1)

*   **DFT-SAP_FUND:** (Part 1)
    *   **Source:** `OLE DB ODS_SAP_FMFINCODE` (Part 1)
    *   **Destination:** `OLE DB -DHUB_SAP_FUND` (Part 1)

*   **DFT-SAP_ACCOUNTING_DOCUMENT_TYPE:** (Part 1)
    *   **Source:** `OLE DB _ODS_T003` (Part 1)
    *   **Destination:** `OLE DB_Load_Dhub_SAP_ACCOUNTING_DOCUMENT_TYPE` (Part 1)

*   **DFT-SAP_AID_TYPE:** (Part 1)
    *   **Source:** `OLE DB  ODS_ZAPS_TPAID` (Part 1)
    *   **Destination:** `OLE DB DATA-HUB_SAP_AID_TYP` (Part 1)

*   **DFT-SAP_GCS_FAS_MAP_WBS:** (Part 1)
    *   **Source:** `OLE DB -ODS_SAP_ZOAT_WBS_MAP` (Part 1)
    *   **Destination:** `OLE DB DATA_HUB_SAP_GCS_FAS_MAP_WBS` (Part 1)

*   **DFT-SAP_PROJECT:** (Part 1)
    *   **Source:** `OLE DB _ODS_Proj` (Part 1)
    *   **Destination:** `OLE DB_Load_Dhub_GC_Project` (Part 1)

*   **DFT-SAP_PROJECT_HIERARCHY:** (Part 1, 3)
    *   **Source:** `OLE DB  SAP Source` / `OLEDB_SRC-PRPS and PHPI - FAS` / `OLEDB_SRC-PRPS and PRHI - GCS` (Part 1, 3)
    *   **Transformations:** `Derived Column` / `DRV-HK columns` / `DRV -HK and BUSI Col`, Data Conversion (`DCNV-Reduce Length`) (Part 1, 3)
    *   **Destination:** `OLE DB Load SAP_PROJECT_HIERARCHY` / `OLEDB_DST-SAP_PROJECT_HIERARCHY` (Part 1, 3)

*   **DFT-SAP\_BUDGET\_ALLOCATION\_HEADER**: (Part 2)
    *   **Source:** OLE DB Source (OLE DB\_SRC\_SAP\_BPBK) extracts data from the `[dbo].BPBK` table in the ODS_SAP database.(Part 2)
    *   **Destination:** OLE DB Destination (OLE DB\_DEST Load\_Dhub\_SAP\_BUDGET\_ALLOCATION\_HEADER) loads data into the `Dhub_SAP_BUDGET_ALLOCATION_HEADER` table in the DATA_HUB database. Fast Load is enabled with `TABLOCK,CHECK_CONSTRAINTS` options. (Part 2)
    *   **Data Movement:** Direct transfer from source to destination with minimal transformation (RTRIM, LTRIM and adding extra columns). (Part 2)

*   **DFT-SAP\_BUDGET\_ANNUAL\_ALLOCATION\_LINE\_ITEM**: (Part 2) Source from `[dbo].[BPVJ]`

*   **DFT-SAP\_BUDGET\_TOTAL\_ALLOCATION\_LINE\_ITEM**: (Part 2) Source from `[dbo].[BPVG]`

*   **DFT-SAP\_COMMITMENT\_TYPE**: (Part 2) Source from `TKBBAT`

*   **DFT-SAP\_COST\_CENTRE**: (Disabled) (Part 2) Attempts to load SAP Cost Centre data. Source from `csks` and `cskt`

*   **DFT-SAP\_CURRENCY**: (Part 2) Source from `TCURC` and `TCURT`

*   **DFT-SAP\_EXCHANGE\_RATES**: (Part 2)

*   **DFT-SAP\_FUNCTIONAL\_AREA**: (Part 2)

*   **DFT-CRS\_LOAN\_PROFILE**: (Part 2)

*   **DFT-OGD\_EDC\_LOAN**: (Part 2)

*   **DFT-SAP\_AID\_TYPE\_CATEGORY**: (Part 2)

*   **DFT-SAP\_LOAN\_CONFIGURATION**: (Part 2)

*   **DFT-SAP\_LOAN\_POLICY\_MARKER**: (Part 2)

*   **DFT_SAP_PROJECT_PDS_ALLOCATION - FAS**: (Part 3)
    *   **Source:** `OLEDB-SRC-ZAPS_PDS_CD - FAS` (Part 3)
    *  **Destination:** `OLEDB_DST-SAP_PROJECT_PDS_ALLOCATION` (Part 3)

*   **DFT_SAP_PROJECT_PDS_ALLOCATION - GCS**: (Part 3)
    *   **Source:** `OLEDB_SRC-ZAPS_PDS_CD-GCS` (Part 3)
    *   **Transformations:** `DRV-HK COLUMNS`, Data Conversion (`DCNV-REDUCE COLUMN_LENGTH`) (Part 3)
    *   **Destination:** `OLE DB_DEST_Dhub_SAP_PROJECT_PDS_ALLOCATION` (Part 3)

*   **DFT-SAP_PROJECT_WBS-FAS**: (Part 3)
    *   **Source:** `OLE DB _ODS_Proj` (Part 3)
    *   **Transformations:** Data Conversion (Part 3)
    *   **Destination:** `OLE DB_Load_Dhub_SAP_Project_WBS` (Part 3)

*   **DFT-SAP_PROJECT_WBS-GCS**: (Part 3)
    *   **Source:** `OLE DB _ODS_Proj` (Part 3)
    *   **Transformations:** Data Conversion (Part 3)
    *   **Destination:** `OLE DB_Load_Dhub_SAP_Project_WBS` (Part 3)

## 4. Code Extraction

```sql
-- From OLE DB_SRC_SAP_BPBK (DFT-SAP_BUDGET_ALLOCATION_HEADER)
SELECT RTRIM(LTRIM(BELNR)) [BUDGET_ALLOCATION_NBR]
      ,RTRIM(LTRIM(USNAM)) [CREATED_BY_USER_ID]
      ,CPUDT [DOCUMENT_CREATE_DT]
      ,RTRIM(LTRIM(BPDK_BELNR)) [ENTRY_DOCUMENT_NBR]
      ,FISCAL_YEAR [FY]
      , 'FAS' [SAP_MERGE_SOURCE_CD]
      , getdate()  [ETL_CREA_DT]
      , getdate()  [ETL_UPDT_DT]
  FROM [dbo].BPBK
```

```sql
-- From OLE DB_SRC_SAP_BPVJ (DFT-SAP_BUDGET_ANNUAL_ALLOCATION_LINE_ITEM)
SELECT RTRIM(LTRIM(BELNR)) [BUDGET_ALLOCATION_NBR]
      ,RTRIM(LTRIM(BUZEI)) [BUDGET_ALLOCATION_ITEM_NBR]
      ,RTRIM(LTRIM(LEDNR)) [BUDGET_LEDGER_CD]
      ,RTRIM(LTRIM(VORGA)) [BUDGET_TY_CD]
      ,RTRIM(LTRIM(A.KALNR)) [COST_ESTIMATE_NBR]
      ,RTRIM(LTRIM(USNAM)) [CREATED_BY_USER_ID]
      ,RTRIM(LTRIM(TWAER)) [CURRENCY_CD]
      ,RTRIM(LTRIM(PLDAT)) [CURRENCY_TRANSLATION_DT]
      ,RTRIM(LTRIM(DEL_BPGE)) [DELETED_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(DEL_BPJA)) [DELETED_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(DEL_BPPE)) [DELETED_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(DELBZ)) [DELETED_LINE_ITEM_4_CNT]
      ,CPUDT [DOCUMENT_CREATE_DT]
      ,BLDAT [DOCUMENT_DT]
      ,RTRIM(LTRIM(KURST)) [EXCHANGE_RT_TY_CD]
      ,RTRIM(LTRIM(FOBEL)) [FOLLOW_DOCUMENT_NBR]
      ,RTRIM(LTRIM(GEBER)) [FUND_NBR]
      ,RTRIM(LTRIM(GJAHR)) [FY]
      ,RTRIM(LTRIM(POSIT)) [INTERNAL_COMMITMENT_ITEM_NBR]
      ,RTRIM(LTRIM(SGTEXT)) [ITEM_TXT]
      ,RTRIM(LTRIM(SUM_BPGE)) [LOCAL_OBJECT_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(SUM_BPJA)) [LOCAL_OBJECT_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(SUM_BPPE)) [LOCAL_OBJECT_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(SUMBZ)) [LOCAL_OBJECT_LINE_ITEM_4_CNT]
      ,RTRIM(LTRIM(TRGKZ)) [OBJECT_IND]
      ,WLJHR [OVER_ALL_LOCAL_CURRENCY_LEDGER_AMT]
      ,WTJHR [OVER_ALL_ORIGINAL_CURRENCY_LEDGER_AMT]
      ,RTRIM(LTRIM(A.OBJNR)) [PROJ_WBS_INTERNAL_CD]
	  ,PRPS.POSID AS WBS_NBR
      ,RTRIM(LTRIM(VERANT)) [RESPONSIBLE_USER_ID]
      ,RTRIM(LTRIM(NAMTEXT)) [TEXT_NM]
      ,RTRIM(LTRIM(WRTTP)) [VALUE_TY_CD]
      ,RTRIM(LTRIM(VERSN)) [VERSON_NBR]
      ,'FAS' [SAP_MERGE_SOURCE_CD]
	  ,'FAS' AS HK_SAP_SOURCE_CD
       , getdate()  [ETL_CREA_DT]
      , getdate()  [ETL_UPDT_DT]
  FROM [dbo].[BPVJ] a
  LEFT join dbo.PRPS PRPS
  on PRPS.OBJNR = a.OBJNR
```

```sql
-- From OLE DB _SAP_BPVG (DFT-SAP_BUDGET_TOTAL_ALLOCATION_LINE_ITEM)
SELECT RTRIM(LTRIM(BELNR)) [BUDGET_ALLOCATION_NBR]
      ,RTRIM(LTRIM(BUZEI)) [BUDGET_ALLOCATION_ITEM_NBR]
      ,RTRIM(LTRIM(LEDNR)) [BUDGET_LEDGER_CD]
      ,RTRIM(LTRIM(VORGA)) [BUDGET_TY_CD]
      ,RTRIM(LTRIM(A.KALNR)) [COST_ESTIMATE_NBR]
      ,RTRIM(LTRIM(USNAM)) [CREATED_BY_USER_ID]
      ,RTRIM(LTRIM(TWAER)) [CURRENCY_CD]
      ,RTRIM(LTRIM(PLDAT)) [CURRENCY_TRANSLATION_DT]
      ,RTRIM(LTRIM(DEL_BPGE)) [DELETED_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(DEL_BPJA)) [DELETED_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(DEL_BPPE)) [DELETED_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(DELBZ)) [DELETED_LINE_ITEM_4_CNT]
      ,CPUDT [DOCUMENT_CREATE_DT]
      ,BLDAT [DOCUMENT_DT]
      ,RTRIM(LTRIM(KURST)) [EXCHANGE_RT_TY_CD]
      ,RTRIM(LTRIM(FOBEL)) [FOLLOW_DOCUMENT_NBR]
      ,RTRIM(LTRIM(GEBER)) [FUND_NBR]
      ,RTRIM(LTRIM(GJAHR)) [FY]
      ,RTRIM(LTRIM(POSIT)) [INTERNAL_COMMITMENT_ITEM_NBR]
      ,RTRIM(LTRIM(SGTEXT)) [ITEM_TXT]
      ,RTRIM(LTRIM(SUM_BPGE)) [LOCAL_OBJECT_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(SUM_BPJA)) [LOCAL_OBJECT_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(SUM_BPPE)) [LOCAL_OBJECT_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(SUMBZ)) [LOCAL_OBJECT_LINE_ITEM_4_CNT]
      ,RTRIM(LTRIM(TRGKZ)) [OBJECT_IND]
      ,WLGES [OVER_ALL_LOCAL_CURRENCY_LEDGER_AMT]
      ,WTGES [OVER_ALL_ORIGINAL_CURRENCY_LEDGER_AMT]
      ,RTRIM(LTRIM(A.OBJNR)) [PROJ_WBS_INTERNAL_CD]
	  ,PRPS.POSID AS WBS_NBR
      ,RTRIM(LTRIM(VERANT)) [RESPONSIBLE_USER_ID]
      ,RTRIM(LTRIM(NAMTEXT)) [TEXT_NM]
      ,RTRIM(LTRIM(WRTTP)) [VALUE_TY_CD]
      ,RTRIM(LTRIM(VERSN)) [VERSON_NBR]
      ,'FAS' [SAP_MERGE_SOURCE_CD]
	  ,'FAS' AS HK_SAP_SOURCE_CD
       , getdate()  [ETL_CREA_DT]
      , getdate()  [ETL_UPDT_DT]
  FROM [dbo].[BPVG] A
  LEFT join dbo.PRPS PRPS
  on PRPS.OBJNR = a.OBJNR
```

```sql
--From OLE DB _SAP_TKBBAT (DFT-SAP_COMMITMENT_TYPE)
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
BLART COMMITMENT_TYPE_CD,
BATXT COMMITMENT_TYPE_EN_NM,
null COMMITMENT_TYPE_FR_NM,
BLTYP COMMITMENT_DOCUMENT_CATEGORY,
  convert(date,getdate()) as ETL_CREA_DT,
	  convert(date,getdate()) as ETL_UPDT_DT,
'FAS' SAP_MERGE_SOURCE_CD

  FROM TKBBAT
  where SPRAS = 'E'
```

```sql
--From LKP_TRFM-TCURT - ENGLISH DESCR (DFT-SAP_CURRENCY)
SELECT ltrim(rtrim(E.WAERS)) AS CURRENCY_CD_LKP_VALUE, 
       ltrim(rtrim(E.KTEXT)) AS CURRENCY_SHORT_EN_DESCR,
	   ltrim(rtrim(E.LTEXT)) AS CURRENCY_LONG_EN_DESCR
FROM TCURT E

WHERE SPRAS = 'E'
```

```sql
--From LKP_TRFM-TCURT - FRENCH DESCR (DFT-SAP_CURRENCY)
SELECT
ltrim(rtrim(f.WAERS)) AS CURRENCY_CD_LKP_VALUE, 
ltrim(rtrim(f.KTEXT)) AS CURRENCY_SHORT_FR_DESCR,	
 ltrim(rtrim(f.LTEXT)) AS CURRENCY_LONG_FR_DESCR	
FROM TCURT F

WHERE SPRAS = 'F'
```

```sql
--From OLE DB _SAP_KBLP (DFT-SAP_COST_CENTRE)
WITH TEMP1 AS
(
SELECT
T1.kostl     AS  AGGCOST_CENTRE,
MIN(T1.DATAB) AS MINDATAB,
MAX(T1.DATBI) AS MAXDATBI
FROM   "csks" T1
-- WHERE T1.KOSTL = '0000041051'
GROUP BY T1.kostl
)
--SELECT * FROM TEMP1
,
TEMP2 AS
(
SELECT
     T1.kostl  AS COST_CENTRE,
     T1.DATAB,
     T2.DATBI,
       CASE
         WHEN T2."ltext" IS NULL THEN 'UnCoded'
         ELSE T2."ltext"
       END          AS EN_NM,
       CASE
         WHEN T3."ltext" IS NULL THEN 'Non-Codé'
         ELSE T3."ltext"
       END          AS FR_NM,
       T1.khinr     AS PARENT_COST_CENTRE,
       '0005'       AS COST_CENTRE_TYPE,
       T1.kokrs     AS CONTRLNG_AREA_CD,
       T1.func_area AS FUNCTIONAL_AREA_CD,

'FAS' AS SOURCE_ID
FROM   "csks" T1
       JOIN "cskt" T2
         ON T1."kostl" = T2."kostl"
AND T1.DATBI = T2.DATBI
            AND T2."spras" = 'E'
       LEFT JOIN "cskt" T3
              ON T1."kostl" = T3."kostl"
AND T1.DATBI = T3.DATBI
                 AND T3."spras" = 'F'


WHERE   T1.kokrs = '0050'
)

SELECT
T2.COST_CENTRE [COST_CENTRE_NBR_SRC] ,
 case
            when SUBSTRING( T2.COST_CENTRE, 1, 5) = '00000'
                then cast(SUBSTRING( T2.COST_CENTRE, 5, len(T2.COST_CENTRE) ) as varchar(10))
            else CAST(T2.COST_CENTRE AS VARCHAR(10))
         end [COST_CENTRE_NBR] ,
--T2.DATAB,
--T2.DATBI,
--T1.MINDATAB,
--T1.MAXDATBI,
RTRIM(T2.EN_NM) COST_CENTRE_EN_NM ,
RTRIM(T2.FR_NM) COST_CENTRE_FR_NM,
RTRIM(T2.PARENT_COST_CENTRE) [PARENT_COST_CENTRE_NBR_SRC],
RTRIM(T2.PARENT_COST_CENTRE) [PARENT_COST_CENTRE_NBR],
--T2.COST_CENTRE_TYPE COST_CENTRE_TYPE_CD,
T2.CONTRLNG_AREA_CD,
T2.FUNCTIONAL_AREA_CD,
       Getdate()    AS ETL_CREA_DT,
 Getdate()    AS ETL_UPDT_DT,
T2.SOURCE_ID,
'FAS' as HK_SAP_MERGE_SOURCE_CD
FROM TEMP2 T2 JOIN TEMP1 T1
ON T1.AGGCOST_CENTRE = T2.COST_CENTRE
WHERE GETDATE() BETWEEN T2.DATAB AND T2.DATBI
OR
T1.MAXDATBI < GETDATE()
OR
T1.MINDATAB > GETDATE()
```

```sql
--From OLE DB _SAP_BPVG (DFT-SAP_BUDGET_TOTAL_ALLOCATION_LINE_ITEM)
SELECT RTRIM(LTRIM(BELNR)) [BUDGET_ALLOCATION_NBR]
      ,RTRIM(LTRIM(BUZEI)) [BUDGET_ALLOCATION_ITEM_NBR]
      ,RTRIM(LTRIM(LEDNR)) [BUDGET_LEDGER_CD]
      ,RTRIM(LTRIM(VORGA)) [BUDGET_TY_CD]
      ,RTRIM(LTRIM(A.KALNR)) [COST_ESTIMATE_NBR]
      ,RTRIM(LTRIM(USNAM)) [CREATED_BY_USER_ID]
      ,RTRIM(LTRIM(TWAER)) [CURRENCY_CD]
      ,RTRIM(LTRIM(PLDAT)) [CURRENCY_TRANSLATION_DT]
      ,RTRIM(LTRIM(DEL_BPGE)) [DELETED_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(DEL_BPJA)) [DELETED_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(DEL_BPPE)) [DELETED_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(DELBZ)) [DELETED_LINE_ITEM_4_CNT]
      ,CPUDT [DOCUMENT_CREATE_DT]
      ,BLDAT [DOCUMENT_DT]
      ,RTRIM(LTRIM(KURST)) [EXCHANGE_RT_TY_CD]
      ,RTRIM(LTRIM(FOBEL)) [FOLLOW_DOCUMENT_NBR]
      ,RTRIM(LTRIM(GEBER)) [FUND_NBR]
      ,RTRIM(LTRIM(GJAHR)) [FY]
      ,RTRIM(LTRIM(POSIT)) [INTERNAL_COMMITMENT_ITEM_NBR]
      ,RTRIM(LTRIM(SGTEXT)) [ITEM_TXT]
      ,RTRIM(LTRIM(SUM_BPGE)) [LOCAL_OBJECT_LINE_ITEM_1_CNT]
      ,RTRIM(LTRIM(SUM_BPJA)) [LOCAL_OBJECT_LINE_ITEM_2_CNT]
      ,RTRIM(LTRIM(SUM_BPPE)) [LOCAL_OBJECT_LINE_ITEM_3_CNT]
      ,RTRIM(LTRIM(SUMBZ)) [LOCAL_OBJECT_LINE_ITEM_4_CNT]
      ,RTRIM(LTRIM(TRGKZ)) [OBJECT_IND]
      ,WLGES [OVER_ALL_LOCAL_CURRENCY_LEDGER_AMT]
      ,WTGES [OVER_ALL_ORIGINAL_CURRENCY_LEDGER_AMT]
      ,RTRIM(LTRIM(A.OBJNR)) [PROJ_WBS_INTERNAL_CD]
	  ,PRPS.POSID AS WBS_NBR
      ,RTRIM(LTRIM(VERANT)) [RESPONSIBLE_USER_ID]
      ,RTRIM(LTRIM(NAMTEXT)) [TEXT_NM]
      ,RTRIM(LTRIM(WRTTP)) [VALUE_TY_CD]
      ,RTRIM(LTRIM(VERSN)) [VERSON_NBR]
      ,'FAS' [SAP_MERGE_SOURCE_CD]
	  ,'FAS' AS HK_SAP_SOURCE_CD
       , getdate()  [ETL_CREA_DT]
      , getdate()  [ETL_UPDT_DT]
  FROM [dbo].[BPVG] A
  LEFT join dbo.PRPS PRPS
  on PRPS.OBJNR = a.OBJNR
```

```sql
-- From OLE DB _SAP_AUTHORITY (DFT-SAP_FUND_AUTHORITY)
SELECT 
AUTHORITY_CODE AS  VOTE_AUTHORITY_CD,
cast(ENGLISH_NAME as varchar(150)) AS [VOTE_AUTHORITY_EN_NM] ,
cast( FRENCH_NAME as varchar(150)) AS [VOTE_AUTHORITY_FR_NM],
  convert(date,getdate()) as ETL_CREA_DT,
	  convert(date,getdate()) as ETL_UPDT_DT,
'FAS' as SAP_MERGE_SOURCE_CD
FROM SP_AUTHORITY T1
```

```sql
--From OLE DB _SAP_FMHISV (DFT-SAP_FUND_CENTRE)
SELECT    lTrim(rtrim(T1.FISTL)) as FUND_CENTRE_CD,
       
CASE
       WHEN T3.BESCHR is null then 'Not Available'
       WHEN LEN(T3.BESCHR) < 1 THEN T3.BEZEICH
       ELSE T3.BESCHR
END as FUND_CENTRE_EN_NM,

 CASE
       WHEN T4.BESCHR is null  then 'Indisponible'
       WHEN LEN(T4.BESCHR) < 1 THEN T4.BEZEICH
       ELSE T4.BESCHR
END as FUND_CENTRE_FR_NM,

       HILEVEL as FUND_CENTER_TYPE_CD,
       T1.PARENT_ST as PARENT_FUND_CENTER_CD,
       T2.DATAB as VALID_FROM_DT,
       T2.DATBIS as VALID_TO_DT,
       T2.ERFDAT as CREATION_DT,
       T2.ERFNAME as CREATED_BY_USERID,
       T2.AENDAT as LAST_UPDATED_DT,
       T2.AENNAME as LAST_UPDATED_BY_USERID,
       'FAS' as SAP_MERGE_SOURCE_CD,
	   cast(getdate() as date) as ETL_CREA_DT,
	   cast(getdate() as date) as ETL_UPDT_DT

 

FROM   "FMHISV" T1

 

       join "FMFCTR" T2
       on T1.FISTL = T2.FICTR
       AND T1.FIKRS = T2.FIKRS
       AND T1.FIKRS = '0050'

 

LEFT        join "FMFCTRT" T3
       on T1."FISTL" = T3."FICTR"
       AND T1.FIKRS = '0050'
       AND T3.SPRAS = 'E'

 

LEFT         join "FMFCTRT" T4
       on T1."FISTL" = T4."FICTR"
       AND T1.FIKRS = '0050'
       AND T4.SPRAS = 'F'

 


WHERE T1.FIKRS = '0050'
```

```sql
--From OLE DB _SAP_TKBBAT (DFT-SAP_COMMITMENT_TYPE)
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
BLART COMMITMENT_TYPE_CD,
BATXT COMMITMENT_TYPE_EN_NM,
null COMMITMENT_TYPE_FR_NM,
BLTYP COMMITMENT_DOCUMENT_CATEGORY,
  convert(date,getdate()) as ETL_CREA_DT,
	  convert(date,getdate()) as ETL_UPDT_DT,
'FAS' SAP_MERGE_SOURCE_CD

  FROM TKBBAT
  where SPRAS = 'E'
```

```sql
--From OLE DB_SRC-TCURC (DFT-SAP_CURRENCY)
SELECT 
       ltrim(rtrim(C.WAERS)) AS CURRENCY_CD, 
       ltrim(rtrim(C.ISOCD)) AS ISO_CURRENCY_CD, 
       ltrim(rtrim(C.ALTWR)) AS ALTERNATE_CURRENCY_KEY,
       C.GDATU AS CURRENCY_VALIDITY_END_DT,
       GETDATE() AS ETL_CREA_DT,
       GETDATE() AS ETL_UPDT_DT, 
       'FAS' AS SAP_MERGE_CD	   
FROM TCURC C
WHERE C.MANDT  ='030'
```

```sql
-- From ESQLT-SAP_PROJECT_HIERACHY-DELETE FAS
/*Delete Rule.
 1.Delete records that were loaded in GCS entry.
 2.Please note that implicit conversions are marked as GCS.
 */
DELETE  DATA_HUB.DBO.SAP_PROJECT_HIERARCHY where SAP_MERGE_SOURCE_CD = 'FAS';
```

```sql
-- From ESQLT-SAP_PROJECT_HIERACHY-TRUNCATE
TRUNCATE TABLE DATA_HUB.DBO.SAP_PROJECT_HIERARCHY;
```

```sql
-- From OLEDB-SRC-ZAPS_PDS_CD - FAS
SELECT ISNULL(LTRIM(RTRIM(ZAPS_PDS_CD.OBJNR)), '') AS PROJECT_PDS_OBJECT_NBR
                ,--PK
                ISNULL(LTRIM(RTRIM(PRPS.PSPNR)), '') AS INTERNAL_WBS_