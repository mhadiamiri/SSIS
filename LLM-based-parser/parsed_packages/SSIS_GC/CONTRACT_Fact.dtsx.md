## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_GC_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for fact tables, Lookup data | SQL Server Auth likely | None | Part 1, 2, 3                  |
| GC_STAGING_SOURCE_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for staging tables             | SQL Server Auth likely            |  None                  | Part 2                 |
| GC_STAGING_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for staging tables             | SQL Server Auth likely            |  None                  | Part 2                 |
| SAP_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for staging tables             | SAP Authentication likely            |  None                  | Part 2                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package `CONTRACT_FACT` begins by truncating and creating multiple temporary staging tables using `Execute SQL Tasks (ESQL)`.
*   It then proceeds to load data into these temporary tables from various sources.
*   Next, it populates the fact tables.
*   Finally, drops the temporary tables.
*   Error handling is implemented via `Event Handlers` to update the ETL process status to "Failed" in case of an error.

#### DFT- F_GC_HOLDBACK_RELEASE

*   **Source:** OLEDB\_SRC-S_GC_HOLDBACK_RELEASE_TMP extracts data from `dbo.S_GC_HOLDBACK_RELEASE_TMP` using a complex SQL Query that joins to `DBO.D_GC_PURCHASE_ORDER`,  `dbo.S_GC_DOCUMENT_TYPE_TMP` and `dbo.D_GC_WBS_LEVEL_2`
*   **Transformations:**
    *   `DCONV_TRFM-`: Converts  `DOCUMENT_TYPE_EN_DESC`, `DOCUMENT_TYPE_FR_DESC` and `LAST_UPDATE_DT` from `str` to `wstr`.
*   **Destinations:**
    *   `OLEDB_DEST-F_GC_HOLDBACK_RELEASE` saves successfully mapped rows to `dbo.F_GC_HOLDBACK_RELEASE`.

#### DFT- Load- S_GC_DOCUMENT_TYPE_TMP

*   **Source:** OLEDB\_SRC-S_GC_DOCUMENT_TYPE extracts data from `dbo.S_GC_DOCUMENT_TYPE`.
*   **Destinations:**
    *   `OLEDB_DEST-S_GC_DOCUMENT_TYPE_TMP` saves successfully mapped rows to `dbo.S_GC_DOCUMENT_TYPE_TMP`.

#### DFT- Load- S_GC_HOLDBACK_RELEASE_TMP

*   **Source:** OLEDB\_SRC-S_GC_HOLDBACK_RELEASE extracts data from `dbo.S_GC_HOLDBACK_RELEASE`.
*   **Destinations:**
    *   `OLEDB_DEST-S_GC_HOLDBACK_RELEASE_TMP` saves successfully mapped rows to `dbo.S_GC_HOLDBACK_RELEASE_TMP`.

#### DFT- F_GC_ACCOUNT_ASSIGNMENTS

*   **Source:** OLEDB\_SRC-S_GC_ACCOUNT_ASSIGNMENTS extracts data from `dbo.S_GC_ACCOUNT_ASSIGNMENTS`.
*   **Destinations:**
    *   `OLEDB_DEST-F_GC_ACCOUNT_ASSIGNMENTS` saves successfully mapped rows to `dbo.F_GC_ACCOUNT_ASSIGNMENTS`.

#### DFT- F_GC_PR_ACCOUNT_ASSIGNMENT

*   **Source:** OLEDB\_SRC-s_gc_pr_account_assignment_TMP extracts data from `dbo.s_gc_pr_account_assignment_TMP`.
*   **Destinations:**
    *   `OLEDB_DEST-F_GC_PR_ACCOUNT_ASSIGNMENT` saves successfully mapped rows to `dbo.F_GC_PR_ACCOUNT_ASSIGNMENT`.

#### DFT-Load-S_GC_FUNCTIONAL_AREA_TMP

*   **Source:** OLEDB\_SRC-S_GC_FUNCTIONAL_AREA extracts data from `dbo.S_GC_FUNCTIONAL_AREA`.
*   **Destinations:**
    *   `OLEDB_DEST-S_GC_FUNCTIONAL_AREA_TMP` saves successfully mapped rows to `dbo.S_GC_FUNCTIONAL_AREA_TMP`.

## 4. Code Extraction

```markdown
-- Example from ESQL-Drop_tmp_Table
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP];
```

Context: This SQL code is used to conditionally drop temporary tables before creation, ensuring a clean slate for data loading.

```sql
-- Example from OLEDB_SRC-S_GC_HOLDBACK_RELEASE_TMP
SELECT
      COALESCE(WBS.WBS_LEVEL_2_SID, '-3') AS WBS_LEVEL_2_SID,
      COALESCE(PO.PURCHASE_ORDER_SID, '-3') AS PURCHASE_ORDER_SID,
--      COALESCE(GL.GL_ACCOUNT_SID,'-3') AS GL_ACCOUNT_SID,
		CASE
		  WHEN GL_MAP.GL_ACCOUNT_SID IS NOT NULL THEN GL_MAP.GL_ACCOUNT_SID
		  WHEN GL.GL_ACCOUNT_SID IS NOT NULL THEN GL.GL_ACCOUNT_SID
		  ELSE '-3'
		END AS GL_ACCOUNT_SID,

      FISCAL_YR,
      MATERIAL_DOC_NBR,
      MATERIAL_DOC_ITEM,
 POSTING_DT,
 DOCUMENT_DT,
      REFERENCE_DOC_NBR,
      DOCUMENT_TYPE_CD,
      DT.EN_DESCR AS DOCUMENT_TYPE_EN_DESC,
      DT.FR_DESCR AS DOCUMENT_TYPE_FR_DESC,
      DEBIT_CREDIT_IND,
      POSTING_PERIOD,
      HOLDBACK_RELEASE_AMT,
      POSTING_KEY,
      ITEM_TEXT,
      --HR.WBS_NBR,
      REVERSE_DOC_NBR,
      REVERSE_DOC_YR,
      HR.LAST_UPDATED_BY_USERID,

CONVERT(CHAR(10),    cast(GETDATE() as DATE)) AS LAST_UPDATE_DT,
CONVERT(CHAR(10),    cast(GETDATE() as DATE)) AS ROW_INSERT_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
   FROM dbo.S_GC_HOLDBACK_RELEASE_TMP AS HR
  LEFT JOIN DBO.D_GC_PURCHASE_ORDER AS PO
	ON PO.PO_DOCUMENT_NBR = HR.PO_DOCUMENT_NBR
	and HR.SOURCE_ID = PO.SOURCE_ID
   JOIN dbo.S_GC_DOCUMENT_TYPE_TMP AS DT
	ON DT.DOCUMENT_TYPE_CD = HR.DOCUMENT_TYPE
-- GL Account
  LEFT OUTER JOIN dbo.D_GC_GL_ACCOUNT AS GL_MAP
      ON  GL_MAP.GL_ACCOUNT_NBR = HR.GL_ACCOUNT
      AND HR.SOURCE_ID = 'GCS'
      AND GL_MAP.SOURCE_ID = 'FAS'
	  AND HR.GL_ACCOUNT IN (SELECT DISTINCT
	                              FAS_SAKNR
	                            FROM dbo.ZOAT_SAKNR_MAP_TMP)

  LEFT OUTER JOIN dbo.D_GC_GL_ACCOUNT AS GL
      ON  GL.GL_ACCOUNT_NBR = HR.GL_ACCOUNT
      AND HR.SOURCE_ID = GL.SOURCE_ID

  LEFT JOIN DBO.D_GC_WBS_LEVEL_2 AS WBS
	ON WBS.WBS_NBR = SUBSTRING(HR.WBS_NBR,1,10)
```

Context: This SQL query populates the F_GC_HOLDBACK_RELEASE table.

```sql
-- Example from SEQC--F_GC_HOLDBACK_RELEASE_J\ESQL-Create_S_GC_HOLDBACK_RELEASE_TMP
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].S_GC_HOLDBACK_RELEASE_TMP') AND type in (N'U')) 
DROP TABLE [dbo].S_GC_HOLDBACK_RELEASE_TMP;

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].S_GC_DOCUMENT_TYPE_TMP') AND type in (N'U')) 
DROP TABLE [dbo].S_GC_DOCUMENT_TYPE_TMP;

CREATE TABLE [dbo].S_GC_DOCUMENT_TYPE_TMP(
 [DOCUMENT_TYPE_CD] [varchar](2) NOT NULL,
 [EN_DESCR] [varchar](20) NULL,
 [FR_DESCR] [varchar](20) NULL,
 [NBR_RANGE_CD] [varchar](2) NOT NULL,
 [ALLOWED_ACCOUNT_TYPE_LIST] [varchar](5) NOT NULL,
 [PARENT_DOCUMENT_TYPE_CD] [varchar](2) NOT NULL,
 [DOCUMENT_POSTED_NET_IND] [varchar](1) NOT NULL,
 [POSTING_FROM_SAP_BILLING_IND] [varchar](1) NOT NULL,
 [BATCHABLE_TYPE_IND] [varchar](1) NOT NULL,
 [INITL_ACCNT_ASSIGNMNT_TYP_IND] [varchar](1) NOT NULL,
 [ONE_CUSTOMER_VENDOR_IND] [varchar](1) NOT NULL,
 [INTER_COMPANY_POSTING_IND] [varchar](1) NOT NULL,
 [MANUAL_PARTNER_ENTRY_IND] [varchar](1) NOT NULL,
 [AUTHORIZATION_GROUP_CD] [varchar](4) NOT NULL,
 [DEBIT_RECOVERY_IND] [varchar](2) NOT NULL,
 [CREDIT_RECOVERY_IND] [varchar](2) NOT NULL,
 [DOCUMENT_HEADER_TEXT_IND] [varchar](1) NOT NULL,
 [REFERENCE_NBR_IND] [varchar](1) NOT NULL,
 [ADJUSTING_TYPE_IND] [varchar](1) NOT NULL,
 [EXCHANGE_RATE_TYPE_CD] [varchar](4) NOT NULL,
 [NEGATIVE_POSTINGS_ALLOWED_IND] [varchar](1) NOT NULL,
 [POST_TO_ASSETS_ALLOWED_IND] [varchar](1) NOT NULL,
 [POST_TO_CUSTOMER_ALLOWED_IND] [varchar](1) NOT NULL,
 [POST_TO_VENDOR_ALLOWED_IND] [varchar](1) NOT NULL,
 [POST_TO_MATERIAL_ALLOWED_IND] [varchar](1) NOT NULL,
 [POST_TO_GL_ALLOWED_IND] [varchar](1) NOT NULL,
 [OFFICIAL_NBRNG_APPLCBL_IND] [varchar](1) NOT NULL,
 [SELF_ISSUED_DOCUMENT_IND] [varchar](1) NOT NULL,
 [CHECK_POSTING_DT_IND] [varchar](1) NOT NULL,
 [UPDATE_DT] [datetime2](7) NOT NULL,
 [SOURCE_ID] [varchar](3) NOT NULL
) ON [PRIMARY];


CREATE TABLE [dbo].[S_GC_HOLDBACK_RELEASE_TMP](
 [PO_DOCUMENT_NBR] [varchar](10) NULL,
 [FISCAL_YR] [varchar](4) NOT NULL,
 [GL_ACCOUNT] [varchar](10) NOT NULL,
 [MATERIAL_DOC_NBR] [varchar](10) NOT NULL,
 [MATERIAL_DOC_ITEM] [varchar](3) NOT NULL,
 [POSTING_DT] [datetime2](7) NULL,
 [DOCUMENT_DT] [datetime2](7) NULL,
 [REFERENCE_DOC_NBR] [varchar](16) NOT NULL,
 [DOCUMENT_TYPE] [varchar](2) NOT NULL,
 [DEBIT_CREDIT_IND] [varchar](1) NOT NULL,
 [POSTING_PERIOD] [varchar](2) NOT NULL,
 [HOLDBACK_RELEASE_AMT] [numeric](18, 7) NULL,
 [POSTING_KEY] [varchar](2) NOT NULL,
 [ITEM_TEXT] [varchar](50) NOT NULL,
 [WBS_NBR] [varchar](24) NULL,
 [REVERSE_DOC_NBR] [varchar](10) NOT NULL,
 [REVERSE_DOC_YR] [varchar](4) NOT NULL,
 [LAST_UPDATED_BY_USERID] [varchar](12) NOT NULL,
 [LAST_UPDATE_DT] [datetime2](7) NULL,
 [UPDATE_DT] [datetime] NOT NULL,
 [SOURCE_ID] [varchar](3) NOT NULL,
 [ETL_CREA_DT] [datetime] NOT NULL,
 [ETL_UPDT_DT] [datetime] NOT NULL
) ON [PRIMARY];

```

Context: This SQL code creates the temporary staging tables used for data loading and transformation.
```sql
-- Example from SEQC-F_GC_ACCOUNT_ASSIGNMENTS_C\ESQL-Create_tmp_Table_Index
 IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]') AND name = N'ix1S_GC_ACCOUNT_ASSIGNMENTS_TMP')
DROP INDEX [ix1S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP] WITH ( ONLINE = OFF )


CREATE NONCLUSTERED INDEX [ix1S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]
(
 [PO_DOCUMENT_NBR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
GO
 IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]') AND name = N'ix2S_GC_ACCOUNT_ASSIGNMENTS_TMP')
DROP INDEX [ix2S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP] WITH ( ONLINE = OFF )

CREATE NONCLUSTERED INDEX [ix2S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]
(
 [PO_LINE_ITEM_NBR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];


GO
 IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]') AND name = N'ix3S_GC_ACCOUNT_ASSIGNMENTS_TMP')
DROP INDEX [ix3S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP] WITH ( ONLINE = OFF )

CREATE NONCLUSTERED INDEX [ix3S_GC_ACCOUNT_ASSIGNMENTS_TMP] ON [dbo].[S_GC_ACCOUNT_ASSIGNMENTS_TMP]
(
 [ACCOUNT_ASSIGNMENT_NBR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
GO
```

Context: This SQL code creates indexes on temporary tables.
```sql
TRUNCATE TABLE DBO.F_GC_ACCOUNT_ASSIGNMENTS;
TRUNCATE TABLE DBO.F_GC_PR_ACCOUNT_ASSIGNMENT
```

Context: This SQL Truncates fact tables before data insertion.
```sql
DROP INDEX IF EXISTS  [XIF1F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF2F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF4F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF5F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF6F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF7F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XIF8F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

DROP INDEX IF EXISTS  [XPKF_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS];

CREATE UNIQUE NONCLUSTERED INDEX [XIF1F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [FC_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF2F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [COST_CENTRE_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF4F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [FUND_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF5F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [PURCHASE_ORDER_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF6F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [PO_LINE_ITEM_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF7F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [WBS_LEVEL_2_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [XIF8F_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [WBS_LEVEL_3_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

CREATE UNIQUE NONCLUSTERED INDEX [XPKF_GC_ACCOUNT_ASSIGNMENTS] ON [dbo].[F_GC_ACCOUNT_ASSIGNMENTS]
(
 [ACCOUNT_ASSIGNMENTS_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
```

Context: This SQL code removes and creates indexes on fact tables to enhance query performance.

```sql
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
   ETL_COMPONENT_NM = 'GC_MASTER.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/GC' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'CONTRACT_FACT.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
```

Context: This SQL marks ETL status as SUCCEEDED.

## 5. Output Analysis

| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.F_GC_HOLDBACK_RELEASE   | Stores holdback release fact data   | Part 2|
| dbo.S_GC_DOCUMENT_TYPE_TMP   | Stores document types data   | Part 2|
| dbo.S_GC_HOLDBACK_RELEASE_TMP  | Stores holdback release data   | Part 2|
| dbo.F_GC_ACCOUNT_ASSIGNMENTS | Stores GC Account Assignments | Part 2|
| dbo.F_GC_PR_ACCOUNT_ASSIGNMENT | Stores GC PR Account Assignments | Part 2|
| dbo.S_GC_FUNCTIONAL_AREA_TMP | Stores GC Functional Areas | Part 2|
| dbo.D_GC_SERVICE_LIMITS   | Stores service limits data   | Part 2|
| dbo.S_GC_ACCOUNTING_DOC_LINE_ITEM_TMP   | Stores accounting document line item data   | Part 2|
| dbo.S_GC_ACCOUNTING_DOCUMENT_TMP | Stores accounting document data | Part 2|
| dbo.ZOAT_SAKNR_MAP_TMP | Stores GL Account Mapping Data | Part 2|
| dbo.D_GC_GEOGRAPHIC_REGION_TMP  | Stores geographic region data | Part 2|
| dbo.F_GC_AMENDMENT | Stores ammedment data | Part 2|
| dbo.F_GC_PURCHASE_ORDER | Stores purchase order data | Part 2|
| dbo.F_GC_SUBITEM | Stores sub item data | Part 2|

## 6. Package Summary

*   **Input Connections:** 4
*   **Output Destinations:** 9
*   **Package Dependencies:** 0
*   **Activities:**

    *   Expression Tasks: 1
    *   Execute SQL Tasks: 5
    *   Data Flow Tasks: 7
    *   Sequence Containers: 5

*   Overall package complexity assessment: Medium to High.
*   Error handling mechanisms: Implemented through event handlers that update the ETL status to 'Failed' when an error occurs.
*   Potential performance bottlenecks: Source queries with multiple joins, Data conversions, Lookups.