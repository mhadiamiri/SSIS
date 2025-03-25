```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager | EXCEL           | `Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\Documents\\Project\\PROJECT\\Analysis\\Build_Summary_PROJECT_SP1.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";` | Reads data from an Excel file. Potentially used as a lookup or configuration data source. | Access to the file system where the Excel file is stored. Depending on the contents of the Excel file, sensitivity of data should be assessed. | None                 | Part 1                  |
| GC_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for data loaded from various sources. Staging area for cleansed data. Used as destination for inserting and updating various tables. | SQL Server Auth likely, Requires permissions to read and write to the specified database and tables |  None                  | Part 1, 2, 3, 4, 5                 |
| SAP_SOURCE              | OLE DB          | Server: [Inferred], Database: [Inferred] | Source of data from SAP system.  Used to read from tables. | Secure SAP database credentials, access to the SAP database. Knowledge of the SAP schema is required. | None                 | Part 1, 2, 3, 4, 5                 |
| BI_Conformed | OLE DB | Server: [Inferred], Database: [Inferred] | Source table for BI_COUNTRY_CD_UPDATE table  | SQL Server Auth likely, Requires permissions to read to the specified database and tables. | None evident from the snippet. | Part 2 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4, 5 |

## 3. Package Flow Analysis

*   The package control flow consists of the following activities, executed in sequence:

    1.  **ESQLT- Drop_TMP_Table_BI_Country 1:** An Execute SQL Task that attempts to drop a table named `[dbo].[BI_COUNTRY_CD_UPDATE]` if it exists.
    2.  **EXPRESSIONT- PROJECT Stage 30 - Start Task - ProcessDataFlowNode:** An Expression Task with the expression `1 == 1`. This task likely serves as a starting point or a placeholder and doesn't perform any meaningful data transformation. It has an `OnPreExecute` event handler, but is empty.

*   The main container is `SEQC- 30-13-S_GC_AID_TYPE`, and there are other sequence containers such as `SEQC- 30-14-S_GC_CHANNEL` and `SEQC- 30-15-S_GC_COUNTRY_LEVEL` within the package.

*   The tasks are contained inside sequence containers which allows for grouping and possibly some level of ordering between groups but not within the group.

#### SEQC- 30-1-S_GC_CRS_ACTIVITY_BREAKDOWN

*   This container seems to be responsible for staging and loading data related to GC CRS activity breakdown.
*   *ESQLT- Truncate Staging Tables_In_S_GC_CRS_ACTIVITY_BREAKDOWN*: Execute SQL Task that truncates the `dbo.S_GC_CRS_ACTIVITY_BREAKDOWN` table.
*   *DFT-Insert-S_GC_CRS_ACTIVITY_BREAKDOWN*: Data Flow Task that loads data into the `dbo.S_GC_CRS_ACTIVITY_BREAKDOWN` table.
*   *DFT- Upsert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR*: Data Flow Task that performs an upsert operation on the `dbo.S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR` table. It uses a Merge Join and Conditional Split to handle both insert and update scenarios.
*   *DFT- Append_S_GC_WBS_BUDGET_TRANSACTION*: Data Flow Task that appends data to the `dbo.S_GC_WBS_BUDGET_TRANSACTION` table.
*   *DFT- Append-S_GC_WBS_OBJECT_XREF*: Data Flow Task that appends data to the `dbo.S_GC_WBS_OBJECT_XREF` table.

#### SEQC- 30-10-S_GC_PROJECT_SUMMARIZATION

*   This container is focused on summarizing project-level data, including themes and CFP information.
*   *DFT- Upsert-S_GC_PROJECT_SUMMARIZATION*: Data Flow Task that performs a merge operation on the `dbo.S_GC_PROJECT_SUMMARIZATION` table.
*   *ESQLT-STAGE S_GC_PROJECT_THEMATIC_PRIORITY into temp*: Execute SQL Task that stages data from the S_GC_PROJECT_THEMATIC_PRIORITY table into a temporary table.
*   *DFT- Upsert-S_GC_PROJECT_THEMATIC_PRIORITY 1*: Data Flow Task that performs an upsert using the staged S_GC_PROJECT_THEMATIC_PRIORITY data.
*   *DFT- Update-S_GC_WBS_INTERNAL_No_MAPPING*: Data Flow Task that updates the `dbo.S_GC_WBS_INTERNAL_No_MAPPING` table.
*   *DFT- Upsert -S_GC_PROJECT_WBS_CFP*: Data Flow Task Upserts data related to Project WBS CFP.
*   *ESQLT- Create_Index_S_GC_PROJECT_WBS*: Execute SQL Task that creates an index on S_GC_PROJECT_WBS
*   *ESQLT-Upsert -S_GC_PROJECT_WBS*: Execute SQL Task that performs a merge operation on the S_GC_PROJECT_WBS table
*   *DFT- Upsert -S_GC_PROJECT_WBS_Not_used*: Disabled Data Flow Task

#### SEQC- 30-11-S_GC_CRSS_CUTNG_SECTOR_MRKR

*   This container is likely responsible for managing cross-cutting sector marker data.

    *   *DFT- Upsert -S_GC_CRSS_CUTNG_SECTOR_MRKR*: Data Flow Task that performs a merge operation on the S_GC_CRSS_CUTNG_SECTOR_MRKR table
    *   *DFT- Upsert -S_GC_DELIVERY_MECHANISM*: Data Flow Task that performs a merge operation on the S_GC_DELIVERY_MECHANISM table
    *   *DFT- Upsert -S_GC_DIRECTIVE_RESPONSIVE*: Data Flow Task that performs a merge operation on the S_GC_DIRECTIVE_RESPONSIVE table
    *   *DFT- Upsert -S_GC_FINANCE_TYPE*: Data Flow Task that performs a merge operation on the S_GC_FINANCE_TYPE table
    *   *DFT- Upsert -S_GC_FINANCE_TYPE_CATEGORY*: Data Flow Task that performs a merge operation on the S_GC_FINANCE_TYPE_CATEGORY table

#### SEQC- 30-12-S_GC_FOOD_AID_TYPE

*   This container is likely responsible for managing food aid type data.

    *   DFT- Upsert -S_GC_CRS_WBS: Data Flow Task that performs a merge operation on the S_GC_CRS_WBS table
    *   DFT- Upsert -S_GC_FOOD_AID_TYPE: Data Flow Task that performs a merge operation on the S_GC_FOOD_AID_TYPE table
    *   DFT- Upsert -S_GC_FOOD_OPERATION_SUBTYPE: Data Flow Task that performs a merge operation on the S_GC_FOOD_OPERATION_SUBTYPE table
    *   DFT- Upsert -S_GC_FOOD_OPERATION_TYPE: Data Flow Task that performs a merge operation on the S_GC_FOOD_OPERATION_TYPE table
    *   DFT- Upsert -S_GC_FUND_CENTRE: Data Flow Task that performs a merge operation on the S_GC_FUND_CENTRE table
    *   DFT- Upsert -S_GC_GENDER_EQUALITY: Data Flow Task that performs a merge operation on the S_GC_GENDER_EQUALITY table
    *   DFT- Upsert -S_GC_GEOMAPPING: Data Flow Task that performs a merge operation on the S_GC_GEOMAPPING table

#### SEQC- 30-13-S_GC_AID_TYPE

*   This container is likely responsible for managing aid type data.

    *   DFT- Upsert -S_GC_AID_TYPE: Data Flow Task that performs a merge operation on the S_GC_AID_TYPE table
    *   DFT- Upsert -S_GC_AID_TYPE_CATEGORY: Data Flow Task that performs a merge operation on the S_GC_AID_TYPE_CATEGORY table
    *   DFT- Upsert -S_GC_CRS_WBS: Data Flow Task that performs a merge operation on the S_GC_CRS_WBS table
    *   DFT- Upsert -S_GC_GEOMAPPING: Data Flow Task that performs a merge operation on the S_GC_GEOMAPPING table

#### SEQC- 30-14-S_GC_CHANNEL

*   The control flow within `SEQC- 30-14-S_GC_CHANNEL` consists of a sequence of Data Flow Tasks (DFTs). The DFTs seem to be executed sequentially based on precedence constraints with the following destinations:

    1.  `DFT- Insert -S_GC_CHANNEL`
    2.  `DFT- Insert -S_GC_CHANNEL_CATEGORY`
    3.  `DFT- Insert -S_GC_LOAN_PROFILE`
    4.  `DFT- TMP_Table_BI_Country`
    5.  `DFT- Upsert -S_GC_CEAA_DECISION`
    6.  `DFT- Upsert -S_GC_CEAA_REQUIREMENT`
    7.  `DFT- Upsert -S_GC_CEAA_RESULT`

#### SEQC- 30-15-S_GC_COUNTRY_LEVEL

*   The control flow within `SEQC- 30-15-S_GC_COUNTRY_LEVEL` consists of a sequence of Data Flow Tasks (DFTs). The DFTs seem to be executed sequentially based on precedence constraints with the following destinations:

    1.  `DFT- Upsert -S_GC_COUNTRY_LEVEL`
    2.  `DFT- Upsert -S_GC_COUNTRY_SUB_CONTINENT_RGN`
    3.  `DFT- Upsert S_GC_CRSS_CUTNG_MRKR_TYP`
    4.  `DFT- Upsert -S_GC_CRSS_CUTNG_SECTOR_MRKR_TYP`
    5.  `DFT- Upsert -S_GC_CRSS_CUTNG_MRKR`
    6.  `DFT- Upsert -S_GC_DISTRICT`
    7.  `DFT- Upsert -S_GC_PROJECT_EIP_DOC_SECTION`

#### SEQC- 30-16-S_GC_WBS_SECTOR_CRSS_CUTNG_MRKR

*   The control flow within `SEQC- 30-16-S_GC_WBS_SECTOR_CRSS_CUTNG_MRKR` consists of a sequence of Data Flow Tasks (DFTs). The DFTs seem to be executed sequentially based on precedence constraints with the following destinations:

    1.  `DFT- Insert 2-S_GC_EIP_DOC_SECTION_LEVEL3`
    2.  `DFT- Upsert -S_GC_EIP_DOC_SECTION`
    3.  `DFT- Upsert -S_GC_EIP_DOC_SECTION_LEVEL1`
    4.  `DFT- Upsert -S_GC_EIP_DOC_SECTION_LEVEL2`

#### SEQC- 30-17-S_GC_ACTIVITY_ROLE

*   groups tasks related to activity roles.

#### SEQC- 30-18-S_GC_PROGRAM_DATA_STRCUTURE

*   groups tasks related to program data structure.

#### SEQC- 30-19-S_GC_ACTIVITY_DOC_CATEGORY

*   groups tasks related to activity document categories.

#### SEQC- 30-2-S_GC_GEOMAPPING_PROJ_SCOPE

*   groups tasks related to geomapping project scope.

#### SEQC- 30-20-S_GC_PROJECT_TEAM

*   1.  `DFT- Upsert -S_GC_CROSS_CUTTING_THEME`
    2.  `DFT- Upsert -S_GC_CRS_LOAN_PROFILE`
    3.  `DFT- Upsert -S_GC_INDIVIDUAL`
    4.  `DFT- Upsert -S_GC_POLICY_MARKER_RANK`

#### DFT- Append-S_GC_WBS_OBJECT_XREF

*   **Source:** OLEDB_SRC-PRPS (SAP_SOURCE)
    *   Retrieves data from the "PRPS" table in the SAP_SOURCE database and joins it with the `ZOAT_WBS_MAP` table.
*   **Destination:** OLEDB_DEST-S_GC_WBS_OBJECT_XREF (GC_STAGING)
    *   Target Table: `[dbo].[S_GC_WBS_OBJECT_XREF]`
    *   Loads data into the `S_GC_WBS_OBJECT_XREF` table in the GC_STAGING database.
*   **Transformations:** There are no explicit transformations specified in this data flow task. Data is directly moved from source to destination.
*   **Error Handling:** The `errorRowDisposition` property is set to `FailComponent` on both the source and destination, meaning that any error during data conversion or insertion will cause the entire component to fail. The destination also has an error output configured.

#### DFT- Upsert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR

*   **Source 1:** OLEDB_SRC-New-ZAPS_CCMWBS (SAP_SOURCE)
*   **Source 2:** OLEDB_SRC-Existing-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR (GC_STAGING)
*   **Transformation:** MRJ_TRFM-Left_Outer
    *   Join Type: Left Outer Join
    *   Join Columns: WBS_NBR, CROSS_CUTTING_MARKER_TYPE_CD.
*   **Transformation:** CSPLIT_TRFM-Insert_Update
    *   Uses Conditional Split to route data to Insert or Update output.
    *   Insert Condition: `ISNULL(WBS_NBR_EXIST)`
    *   Update Condition: `WBS_NBR_EXIST == WBS_NBR && CROSS_CUTTING_MARKER_TYPE_CD_EXIST == CROSS_CUTTING_MARKER_TYPE_CD`
*   **Destination (Insert):** OLEDB_DEST_Insert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR (GC_STAGING)
    * Inserting new records.
    * Columns: WBS_NBR, MARKER_SCORE_CD, UPDATE_DT, SOURCE_ID, CROSS_CUTTING_MARKER_TYPE_CD, MARKER_SCORE_PCT, ETL_CREA_DT, ETL_UPDT_DT
*   **Destination (Update):** OLEDB_DEST-Update-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR (GC_STAGING)
    *   Updates existing records in the S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR table.
*   **Error Handling:** The `errorRowDisposition` property is set to `FailComponent` on the source and destination. Both destination transforms have error outputs configured.

*   **Common Pattern:** The provided snippets show a common pattern for the `Upsert` DFTs:
    *   **Source 1:** Reads "New" data from a SAP table.
    *   **Source 2:** Reads "Existing" data from a staging table.
    *   **Merge Join:** Performs a Left Outer Join to identify records that exist or do not exist in the staging table.
    *   **Conditional Split:**  Splits the data flow into "Insert" and "Update" paths based on whether a matching record was found in the staging table.
    *   **Destination:** Inserts new records into the staging table using `OLE DB Destination`.  Updates existing records in the staging table using `OLE DB Command`.

## 4. Code Extraction

```sql
-- ESQLT- Drop_TMP_Table_BI_Country 1
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[BI_COUNTRY_CD_UPDATE]') AND type in (N'U'))
DROP TABLE [dbo].[BI_COUNTRY_CD_UPDATE];
```

```sql
-- OLEDB_SRC-PRPS (DFT- Append-S_GC_WBS_OBJECT_XREF)
SELECT
  "PSPNR" AS "WBS_ID",
  POSID AS "WBS_OBJECT_NBR",
  ISNULL(T2.GCS_POSID,' ') AS "GCS_WBS_OBJECT_NBR",
  "ERNAM" AS "UPDATED_BY_USERID",
  "AEDAT" AS LAST_UPDATE_DT,
  cast(getdate() as date) AS "UPDATE_DT",
  'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM "PRPS" T1
LEFT JOIN ZOAT_WBS_MAP T2 ON
T1.POSID=T2.FAS_POSID
```

```sql
-- OLEDB_DEST-Update-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR (DFT- Upsert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR)
UPDATE [dbo].[S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR]
   SET
      [MARKER_SCORE_PCT] = ?
      ,[MARKER_SCORE_CD] = ?
      ,[UPDATE_DT] = ?
      ,[SOURCE_ID] = ?
      ,[ETL_UPDT_DT] = ?
 WHERE [WBS_NBR] = ?
      AND [CROSS_CUTTING_MARKER_TYPE_CD] = ?
```

```sql
-- OLEDB_SRC-Existing-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR (DFT- Upsert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR)
SELECT     WBS_NBR,
    CROSS_CUTTING_MARKER_TYPE_CD
FROM DBO.S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR
ORDER BY  WBS_NBR,
    CROSS_CUTTING_MARKER_TYPE_CD
```

```sql
-- OLEDB_SRC-New-ZAPS_CCMWBS (DFT- Upsert-S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR)
SELECT
    T1."POSID" AS WBS_NBR,
    T2."ZA_CCMTYPE" AS CROSS_CUTTING_MARKER_TYPE_CD,
    T2."ZA_PERC" AS MARKER_SCORE_PCTG,
    T2."ZA_MARKER" AS MARKER_SCORE_CD,
    cast(getdate() as date) as UPDATE_DT,
    'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM ZAPS_CCMWBS T2
JOIN PRPS T1
on T1.OBJNR = T2.OBJNR
ORDER BY     T1."POSID",
    T2."ZA_CCMTYPE"
```

```sql
-- OLEDB_SRC-S_GC_CRS_ACTIVITY_BREAKDOWN (DFT-Insert-S_GC_CRS_ACTIVITY_BREAKDOWN)
SELECT ZA_CRSID AS CRS_ID,
GEO_CD  AS GEO_REGION_CD,
SECTOR_CD AS SECTOR_CD,
ZA_NOSID  AS NATURE_OF_SUBMISSION_CD,
ZA_R_YEAR AS REPORTING_YEAR,
ZA_CUST_PROJ AS CRS_PROJECT_NBR,
ZA_COMMIT AS COMMITMENT_AMT,
ZA_DISBURS AS DISBURSEMENT_AMT,
ZA_CUKY  AS CURRENCY_KEY_CD,
ZA_LR_DATE AS LAST_REPORT_DT,
ZA_GEOAREA AS GEOGRAPHIC_AREA_DESCR,
getdate() as UPDATE_DATE
      ,'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
from  ZAPS_CRSACTIVIT
```

```sql
-- ESQLT- Truncate Staging Tables_In_S_GC_CRS_ACTIVITY_BREAKDOWN (SEQC- 30-1-S_GC_CRS_ACTIVITY_BREAKDOWN)
TRUNCATE TABLE dbo.S_GC_CRS_ACTIVITY_BREAKDOWN;
```

```sql
-- OLEDB_SRC-S_GC_WBS_BUDGET_TRANSACTION (DFT- Append_S_GC_WBS_BUDGET_TRANSACTION)
SELECT distinct -- needed because of duplicates created with full outer join
  IsNull(T1.GJAHR,T2.GJAHR) FISCAL_YEAR
--  ,T1.BELNR BPVJ
--  ,T2.BELNR BPVG
  ,IsNull(T1.BELNR,T2.BELNR) DOCUMENT_NUMBER
  ,IsNull(T1.BUZEI ,T2.BUZEI ) POSTING_ROW
  ,IsNull(T1.OBJNR,T2.OBJNR) OBJECT_NUMBER
  ,IsNull(PRPS_J.POSID,PRPS_G.POSID) WBS_NBR
  ,IsNull(T1.WLJHR,T2.WLGES) BUDGET_AMOUNT
  ,IsNull(T1.VORGA,T2.VORGA) BUDGET_TYPE

  ,CASE IsNull(T1.VORGA,T2.VORGA)
    WHEN 'KBN0' THEN 'Budget Supplement'      -- / Supplément budgétaire
    WHEN 'KBR0' THEN 'Budget Return'        -- / Rendement budgétaire
    WHEN 'KBUD' THEN 'Budgetting'          -- / Budgétisation
    WHEN 'KBUE' THEN 'Budget Transfer (receiver)'  -- / Transfert de budget (séquestre)
    WHEN 'KBUS' THEN 'Budget Transfer (sender)'    -- / Transfert de budget (expéditeur)
    WHEN 'KBUT' THEN 'Budget Transfer (transfer)'  -- / Transfert de budget (transfert)
    WHEN 'KBFR' THEN 'Budget Release'        -- / Déblocage de budget
    WHEN 'KBU1' THEN 'Sender of carryover'      -- / Report émetteur
    WHEN 'KBU2' THEN 'Receiver of carryover'    -- / Report récepteur
    WHEN 'KBU3' THEN 'Sender of advance'      -- / Anticipation émetteur
    WHEN 'KBU4'  THEN 'Receiver of advance'      -- / Anticipation récepteur
    WHEN 'KSTE' THEN 'Unit costing (planning)'    -- / Budgétisation CCR unitaire
    WHEN 'KSTP' THEN 'Total cost planning'      -- / Budgétisation coûts (complets)
    WHEN 'KSTR'  THEN 'Revenue planning (total)'    -- / Budgétis. Produits (total)
    ELSE 'Budgeting (Other)'
    END
    AS BUDGET_TYPE_EN_NM
  ,CASE IsNull(T1.VORGA,T2.VORGA)
    WHEN 'KBN0' THEN 'Supplément budgétaire'
    WHEN 'KBR0' THEN 'Rendement budgétaire'
    WHEN 'KBUD' THEN 'Budgétisation'
    WHEN 'KBUE' THEN 'Transfert de budget (séquestre)'
    WHEN 'KBUS' THEN 'Transfert de budget (expéditeur)'
    WHEN 'KBUT' THEN 'Transfert de budget (transfert)'
    WHEN 'KBFR' THEN 'Déblocage de budget'
    WHEN 'KBU1' THEN 'Report émetteur'
    WHEN 'KBU2' THEN 'Report récepteur'
    WHEN 'KBU3' THEN 'Anticipation émetteur'
    WHEN 'KBU4'  THEN 'Anticipation récepteur'
    WHEN 'KSTE' THEN 'Budgétisation CCR unitaire'
    WHEN 'KSTP' THEN 'Budgétisation coûts (complets)'
    WHEN 'KSTR'  THEN 'Budgétis. Produits (total)'
    ELSE 'Budgétisation (autre)'
    END
    AS BUDGET_TYPE_FR_NM
  ,IsNull(T1.TWAER,T2.TWAER) CURRENCY_CODE
  ,IsNull(T1.CPUDT,T2.CPUDT) DOCUMENT_CREATE_DATE
  ,IsNull(T1.USNAM,T2.USNAM) DOC_CREATE_USER
  ,CASE   -- data cleansing
        WHEN YEAR(isNull(T1.BLDAT,T2.BLDAT)) = 1010 THEN convert(date,'2010-' + convert(char(2),month(isNull(T1.BLDAT,T2.BLDAT))) + '-' + convert(char(2),day(isNull(T1.BLDAT,T2.BLDAT))))
        WHEN YEAR(isNull(T1.BLDAT,T2.BLDAT)) = 1001 THEN convert(date,'2001-' + convert(char(2),month(isNull(T1.BLDAT,T2.BLDAT))) + '-' + convert(char(2),day(isNull(T1.BLDAT,T2.BLDAT))))
        WHEN YEAR(isNull(T1.BLDAT,T2.BLDAT)) = 10   THEN convert(date,'2010-' + convert(char(2),month(isNull(T1.BLDAT,T2.BLDAT))) + '-' + convert(char(2),day(isNull(T1.BLDAT,T2.BLDAT))))
        WHEN YEAR(isNull(T1.BLDAT,T2.BLDAT)) = 9    THEN convert(date,'2009-' + convert(char(2),month(isNull(T1.BLDAT,T2.BLDAT))) + '-' + convert(char(2),day(isNull(T1.BLDAT,T2.BLDAT))))
          ELSE T1.BLDAT

  END AS DOCUMENT_DATE
  ,'FAS' SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM dbo.BPVJ T1

full outer join dbo.BPVG T2
on T2.BELNR = T1.BELNR
and T2.OBJNR = T1.OBJNR

LEFT JOIN dbo.ZOAT_WBS_MAP MAP_J
on MAP_J.GCS_OBJNR = T1.OBJNR

LEFT JOIN dbo.ZOAT_WBS_MAP MAP_G
on MAP_G.GCS_OBJNR = T2.OBJNR

LEFT JOIN dbo.PRPS PRPS_J
on PRPS_J.OBJNR = T1.OBJNR

LEFT JOIN dbo.PRPS PRPS_G
on PRPS_G.OBJNR = T2.OBJNR

WHERE isnull(PRPS_J.STUFE, PRPS_G.STUFE ) = 2
and len(IsNull(PRPS_J.POSID,PRPS_G.POSID)) = 10
and IsNull(PRPS_J.POSID,PRPS_G.POSID) like 'P%'
```

```sql
-- OLEDB_SRC-Existing-S_GC_WBS_INTERNAL_No_MAPPING (DFT- Update-S_GC_WBS_INTERNAL_No_MAPPING)
SELECT  [FAS_POSID] FROM DBO.S_GC_WBS_INTERNAL_No_MAPPING
ORDER BY [FAS_POSID]
```

```sql
-- OLEDB_SRC-New-S_GC_WBS_INTERNAL_No_MAPPING (DFT- Update-S_GC_WBS_INTERNAL_No_MAPPING)
SELECT distinct
       a.[GCS_POSID]
      ,a.[FAS_POSID]
      ,SUBSTRING(a.[GCS_INTERNAL_PROJECT_NBR], PATINDEX('%[^0]%', a.[GCS_INTERNAL_PROJECT_NBR]+'.'), LEN(a.[GCS_INTERNAL_PROJECT_NBR])) AS [GCS_INTERNAL_PROJECT_NBR]
      ,SUBSTRING(a.[GCS_INTERNAL_WBS_NBR], PATINDEX('%[^0]%', a.[GCS_INTERNAL_WBS_NBR]+'.'), LEN(a.[GCS_INTERNAL_WBS_NBR])) AS [GCS_INTERNAL_WBS_NBR]
      ,S.INTERNAL_PROJECT_NBR AS [FAS_INTERNAL_PROJECT_NBR]
      ,S.INTERNAL_WBS_NBR   AS [FAS_INTERNAL_WBS_NBR],
getdate() as ETL_UPDT_DT
  FROM [dbo].[S_GC_WBS_INTERNAL_No_MAPPING] a
  JOIN [dbo].S_GC_PROJECT_WBS S
  on S.WBS_NBR = a.FAS_POSID
ORDER BY a.[FAS_POSID]
```

```sql
-- OLEDB_DEST-Update-S_GC_WBS_INTERNAL_No_MAPPING (DFT- Update-S_GC_WBS_INTERNAL_No_MAPPING)
UPDATE [dbo].[S_GC_WBS_INTERNAL_No_MAPPING]
   SET [GCS_POSID] = ?
      ,[GCS_INTERNAL_PROJECT_NBR] = ?
      ,[GCS_INTERNAL_WBS_NBR] = ?
      ,[FAS_INTERNAL_PROJECT_NBR] = ?
      ,[FAS_INTERNAL_WBS_NBR] = ?
      ,[ETL_UPDT_DT] = ?
 WHERE [FAS_POSID] = ?
```

```sql
-- OLEDB_SRC-Existing-S_GC_PROJECT_THEMES (DFT- Upsert -S_GC_PROJECT_THEMES)
SELECT     WBS_NBR,
    CROSS_CUTTING_MARKER_TYPE_CD
FROM DBO.S_GC_PROJECT_WBS_CRSS_CUTNG_MRKR
ORDER BY  WBS_NBR,
    CROSS_CUTTING_MARKER_TYPE_CD
```

```sql
-- OLEDB_SRC-New-ZAPS_CCMWBS (DFT- Upsert -S_GC_PROJECT_THEMES)
SELECT
    T1."POSID" AS WBS_NBR,
    T2."ZA_CCMTYPE" AS CROSS_CUTTING_MARKER_TYPE_CD,
    T2."ZA_PERC" AS MARKER_SCORE_PCTG,
    T2."ZA_MARKER" AS MARKER_SCORE_CD,
    cast(getdate() as date) as UPDATE_DT,
    'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM ZAPS_CCMWBS T2
JOIN PRPS T1
on T1.OBJNR = T2.OBJNR
ORDER BY     T1."POSID",
    T2."ZA_CCMTYPE"
```

```sql
-- ESQLT- Create_Index_S_GC_PROJECT_WBS (SEQC- 30-10-S_GC_PROJECT_SUMMARIZATION)
IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_PROJECT_WBS]') AND name = N'IX_GC_PROJECT_WBS')
DROP INDEX [IX_GC_PROJECT_WBS] ON [dbo].[S_GC_PROJECT_WBS] WITH ( ONLINE = OFF );

CREATE UNIQUE NONCLUSTERED INDEX [IX_GC_PROJECT_WBS] ON [dbo].[S_GC_PROJECT_WBS]
(
  [WBS_NBR] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY];
```

```sql
-- ESQLT-STAGE S_GC_PROJECT_THEMATIC_PRIORITY into temp (SEQC- 30-10-S_GC_PROJECT_SUMMARIZATION)
-- This truncate will delete the data from the previous run.
TRUNCATE TABLE S_GC_PROJECT_THEMATIC_PRIORITY_UPSERT_TMP;

-- Now STAGE THE the GC_STAGING_01
INSERT INTO S_GC_PROJECT_THEMATIC_PRIORITY_UPSERT_TMP ( WBS_NBR, THEMATIC_PRIORITY_CD)
(
select WBS_NBR, THEMATIC_PRIORITY_CD
from S_GC_PROJECT_THEMATIC_PRIORITY
)
;
```

```sql
-- ESQLT-Upsert -S_GC_PROJECT_WBS (SEQC- 30-10-S_GC_PROJECT_SUMMARIZATION)
USE [GC_STAGING]
GO

/****** Object:  Table [dbo].[TMP_S_GC_PROJECT_WBS_GCS]    Script Date: 2024-11-14 11:37:19 AM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TMP_S_GC_PROJECT_WBS_GCS]') AND type in (N'U'))
DROP TABLE [dbo].[TMP_S_GC_PROJECT_WBS_GCS]
GO


USE SAP_SOURCE

SELECT

T1."POSID"                  AS WBS_NBR,
isnull(T4.GCS_POSID_INT,'') AS GCS_WBS_NBR,

cast(Getdate() as date)   AS UPDATE_DT,
T1.objnr                  AS OBJECT_NBR,
T1."pspnr"                AS INTERNAL_WBS_NBR,
T1."post1"                AS WBS_NM,
Ltrim(T1.stufe)           AS WBS_LEVEL,
T1."vernr"                AS OFFICER_NBR,


CASE
  WHEN Len(T1."fkstl") = '0' THEN NULL
  WHEN T1."fkstl" = ' ' THEN NULL
  ELSE Substring('0000000000' + T1."fkstl", Len(T1