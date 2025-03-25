```markdown
## 1. Input Connection Analysis

| Connection Manager Name  | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
| -------------------------- | --------------- | -------------------------- | ---------------------- | -------------------- | -------------------- | ----------- |
| MART_GC_REPORTING       | OLE DB          | Server: [Inferred], Database: [Inferred] | Destination for Dimensions | SQL Server Auth likely | None                | Part 1,2,3                  |
| GC_STAGING        | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for Dimension staging tables | SQL Server Auth likely | None                | Part 1,2,3                 |
| GC_STAGING_SRC_OTHER  | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for Dimension tables | SQL Server Auth likely | None                | Part 1,2,3                  |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
| -------------------------- | -------------------- | ------------------------------ | ----------------------------------- | --------------------------------------- | ----------- |
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found | Part 1,2,3                 |

## 3. Package Flow Analysis

The package `SSIS_FINANCE_DIMENSION` is designed to load several dimension tables related to finance data.

*   **Control Flow:** The package starts with an `Expression Task` (`EXPRESSIONT- FINANCE Dimensions - Start Task - ProcessDataFlowNode`) that contains a simple expression `1 == 1`, likely used for validation.
*   **Sequence Containers:** The package uses sequence containers to group related tasks.  There is a top level container for `D_GC_ACCOUNTING_DOC_LINE_ITEM` (SEQC\_DIM\_1\_D\_GC\_ACCOUNTING\_DOC\_LINE\_ITEM) and a second top level container for `D_GC_ACCOUNTING_DOCUMENT` (SEQC\_DIM\_2\_D\_GC\_ACCOUNTING\_DOCUMENT).

#### SEQC_DIM_1_D_GC_ACCOUNTING_DOC_LINE_ITEM

*   **Task:** Truncates and drops indexes on the `D_GC_ACCOUNTING_DOC_LINE_ITEM` table. (ESQLT- Truncate D\_GC\_ACCOUNTING\_DOC\_LINE\_ITEM and Drop Indexes)
*   **Task:** Creates temporary tables (S\_GC\_\*\_TMP\_K).  This is done in a separate Sequence Container.
    *   **DFT-Load\_S\_GC\_ACCOUNTING\_DOC\_LINE\_ITEM\_TMP:** Loads data from  `dbo.S_GC_ACCOUNTING_DOC_LINE_ITEM` (source) to  `dbo.S_GC_ACCOUNTING_DOC_LINE_ITEM_TMP_K`  (destination).
    *   **DFT-Load\_S\_GC\_COUNTRY\_TMP:**  Loads data from `S_GC_COUNTRY` to a temp table.
    *   **DFT-Load\_S\_GC\_FUNCTIONAL\_AREA\_TMP:**  Loads data from `S_GC_FUNCTIONAL_AREA` to a temp table.
    *   **DFT-Load\_S\_GC\_TRANSACTION\_TYPE\_TMP:** Loads data from `S_GC_TRANSACTION_TYPE` to a temp table.
    *   **ESQLT-Create\_Index\_On\_Temp\_Table\_All\_Dim:** Creates indexes on temp tables.
*   **Task:** Inserts a default row into `D_GC_ACCOUNTING_DOC_LINE_ITEM`
*   **Task:** Inserts data into  `D_GC_ACCOUNTING_DOC_LINE_ITEM` from the temp table.
*   **Task:** Drops the temp tables (S\_GC\_\*\_TMP\_K).
*   **Task:** Creates indexes on `D_GC_ACCOUNTING_DOC_LINE_ITEM`.

#### SEQC_DIM_2_D_GC_ACCOUNTING_DOCUMENT

*   **Task:** Truncates and drops indexes on the `D_GC_ACCOUNTING_DOCUMENT` table.
*   **DFT-GC_STAGING_to_D_GC_ACCOUNTING_DOCUMENT_TEMP:** Loads data from `GC_STAGING` to `D_GC_ACCOUNTING_DOCUMENT_TEMP`
*   **Task:** Inserts a default row into  `D_GC_ACCOUNTING_DOCUMENT`
*   **Task:** Drops the temp table
*   **Task:** Creates indexes on `D_GC_ACCOUNTING_DOCUMENT`

#### SEQC_DIM_3_D_GC_TRANSACTION_TYPE

*   **Task:** Truncates destination tables: D\_GC\_TRANSACTION\_TYPE, D\_GC\_FUNDS\_RESERVATION\_ITEM, D\_GC\_ORDER
*   **DFT-D_GC_TRANSACTION_TYPE:** Loads data from `S_GC_TRANSACTION_TYPE` to `D_GC_TRANSACTION_TYPE`, with casting.
*   **DFT-D_GC_FUNDS_RESERVATION_ITEM:** Loads data from S\_GC\_FUNDS\_RESERVATION\_ITEM and S\_GC\_PROGRAM\_ACTIVITY to `D_GC_FUNDS_RESERVATION_ITEM`
*   **DFT-D_GC_ORDER:** Loads data from `S_GC_ORDER` and `S_GC_CURRENCY` to `D_GC_ORDER`.
*   **Task:** Inserts a default record into `D_GC_FUNDS_RESERVATION_ITEM`
*   **Task:** Inserts a default record into `D_GC_ORDER`
*   **Task:** Inserts a default record into `D_GC_TRANSACTION_TYPE`.

#### SEQC_DIM_4_DFT-D_CURRENCY_CODES

*   **Task:** Truncates destination tables: D\_CURRENCY\_CODES, D\_GC\_ANNUAL\_BUDGET, D\_GC\_COMMITMENT\_ITEM, D\_GC\_CUSTOMER,  D\_GC\_FUNDS\_RESERVATION\_DOCUMENT, D\_GC\_GL\_ACCOUNT, D\_GC\_MATERIAL
*   **DFT-D_CURRENCY_CODES:** Loads data from `S_GC_CURRENCY` to `D_CURRENCY_CODES`
*   **DFT-D_GC_CUSTOMER:** Loads data from `S_GC_CUSTOMER` to `D_GC_CUSTOMER`
*   **DFT-D_GC_GL_ACCOUNT:** 	Loads data from `S_GC_GL_ACCOUNT` to `D_GC_GL_ACCOUNT`
*   **DFT-D_GC_MATERIAL:**	Loads data from `S_GC_MATERIAL_MASTER` to `D_GC_MATERIAL`
*   **SEQC-D_GC_ANNUAL_BUDGET:** Loads data from `S_GC_ANNUAL_BUDGET` to `D_GC_ANNUAL_BUDGET`
*   **Task:** Inserts a default record into `D_CURRENCY_CODES`
*   **Task:** Inserts a default record into `D_GC_FUNDS_RESERVATION_ITEM`
*   **Task:** Inserts a default record into `D_GC_MATERIAL`
*   **Task:** Inserts a default record into `D_GC_GL_ACCOUNT`

## 4. Code Extraction

```markdown
-- From ESQLT- Create Index D_GC_ACCOUNTING_DOC_LINE_ITEM
DROP INDEX IF EXISTS  [ix_pk_GC_ACCOUNTING_DOC_LINE_ITEM] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];


DROP INDEX IF EXISTS [D_GC_ACCOUNTING_DOC_LINE_ITEM_ACCOUNTING_DOCUMENT_NBR_ix] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [A] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [B] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [C] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

CREATE NONCLUSTERED INDEX [D_GC_ACCOUNTING_DOC_LINE_ITEM_ACCOUNTING_DOCUMENT_NBR_ix] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
(
	[ACCOUNTING_DOCUMENT_NBR] ASC,
	[ACCOUNTING_DOCUMENT_ITEM_NBR] ASC,
	[FY] ASC
)
INCLUDE ( 	[ACCOUNTING_DOCUMENT_ITEM_SID]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 100) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [A] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
(
	[FY] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 100) ON [PRIMARY]
GO


CREATE NONCLUSTERED INDEX [B] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
(
	[ACCOUNTING_DOCUMENT_NBR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 100) ON [PRIMARY]
GO


CREATE NONCLUSTERED INDEX [C] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
(
	[ACCOUNTING_DOCUMENT_ITEM_NBR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 100) ON [PRIMARY];
GO


CREATE UNIQUE CLUSTERED INDEX [ix_pk_GC_ACCOUNTING_DOC_LINE_ITEM] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
(
	ACCOUNTING_DOCUMENT_ITEM_SID ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
```

This SQL code recreates the indexes on the `D_GC_ACCOUNTING_DOC_LINE_ITEM` table.

```sql
-- From ESQLT- Insert_D_GC_ACCOUNTING_DOC_LINE_ITEM
INSERT INTO [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
           ([ACCOUNTING_DOCUMENT_NBR]
           ,[FY]
           ,[ACCOUNTING_DOCUMENT_ITEM_NBR]
           ,[CLEARING_DOCUMENT_NBR]
           ,[POSTING_TYPE_KEY]
           ,[ACCOUNT_TYPE_CD]
           ,[SPECIAL_GL_TYPE_CD]
           ,[SPECIAL_GL_TRANSCTN_TYPE_CD]
           ,[TARGET_SPECIAL_GL_TYPE_CD]
           ,[DEBIT_CREDIT_CD]
           ,[TAX_CD]
           ,[WITHHOLDING_TAX_CD]
           ,[GL_AMT_CURRENCY_CD]
           ,[GL_AMT_CURRENCY_DESCR_EN]
           ,[GL_AMT_CURRENCY_DESCR_FR]
           ,[TAX_TYPE_CD]
           ,[ALLOCATION_REFERENCE_NBR]
           ,[LINE_ITEM_TEXT]
           ,[TRANSACTION_TYPE_CD]
           ,[TRANSACTION_TYPE_EN_DESCR]
           ,[TRANSACTION_TYPE_FR_DESCR]
           ,[GL_TRANSACTION_TYPE_CD]
           ,[FINANCIAL_BUDGET_ITEM_NBR]
           ,[MAIN_ASSET_NBR]
           ,[SUB_ASSET_NBR]
           ,[ASSET_TRANSACTION_TYPE_CD]
           ,[STAT_POSTNG_2_COST_CENTR_IND]
           ,[STAT_POSTING_TO_ORDER_IND]
           ,[STAT_POSTING_PROJECT_IND]
           ,[STAT_POSTNG_2_PROFL_ANLYS_IND]
           ,[OPEN_ITEM_MANAGEMENT_IND]
           ,[PAYMENT_TRANSACTION_IND]
           ,[BALANCE_SHEET_ACCOUNT_IND]
           ,[PL_ACCOUNT_TYPE_CD]
           ,[SPECIAL_GL_ALLOCATION_NBR]
           ,[FOLLOWING_DOCUMENT_TYPE_CD]
           ,[BASELINE_PAYMENT_DT]
           ,[PAYMENT_METHOD_CD]
           ,[PAYMENT_BLOCKING_KEY]
           ,[DESTINATION_COUNTRY_CD]
           ,[DESTINATION_COUNTRY_EN_NM]
           ,[DESTINATION_COUNTRY_FR_NM]
           ,[SUPPLYING_COUNTRY_CD]
           ,[SUPPLYING_COUNTRY_EN_NM]
           ,[SUPPLYING_COUNTRY_FR_NM]
           ,[MANUAL_GL_ACCOUNT_IND]
           ,[COMMITMENT_ITEM_KEY]
           ,[REVERSE_CLEARING_IND]
           ,[PAYMENT_METHOD_SUPPLEMENT_CD]
           ,[PAYEE_KEY]
           ,[PROGRAM_ACTIVITY_NBR]
           ,[PRI_NBR]
           ,[FUNCTIONAL_AREA_CD]
           ,[FUNCTIONAL_AREA_EN_NM]
           ,[FUNCTIONAL_AREA_FR_NM]
           ,[FUNDED_PROGRAM_CD]
           ,[ROW_INSERT_DT]
           ,[ETL_CREA_DT]
           ,[ETL_UPDT_DT])
SELECT
--  [ACCOUNTING_DOCUMENT_ITEM_SID]
  [ACCOUNTING_DOCUMENT_NBR]
      ,[FY]
      ,[ACCOUNTING_DOCUMENT_ITEM_NBR]
      ,[CLEARING_DOCUMENT_NBR]
      ,[POSTING_TYPE_KEY]
      ,[ACCOUNT_TYPE_CD]
      ,[SPECIAL_GL_TYPE_CD]
      ,[SPECIAL_GL_TRANSCTN_TYPE_CD]
      ,[TARGET_SPECIAL_GL_TYPE_CD]
      ,[DEBIT_CREDIT_CD]
      ,[TAX_CD]
      ,[WITHHOLDING_TAX_CD]
      ,[GL_AMT_CURRENCY_CD]
      ,[GL_AMT_CURRENCY_DESCR_EN]
      ,[GL_AMT_CURRENCY_DESCR_FR]
      ,[TAX_TYPE_CD]
      ,[ALLOCATION_REFERENCE_NBR]
      ,[LINE_ITEM_TEXT]
      ,[TRANSACTION_TYPE_CD]
      ,[TRANSACTION_TYPE_EN_DESCR]
      ,[TRANSACTION_TYPE_FR_DESCR]
      ,[GL_TRANSACTION_TYPE_CD]
      ,[FINANCIAL_BUDGET_ITEM_NBR]
      ,[MAIN_ASSET_NBR]
      ,[SUB_ASSET_NBR]
      ,[ASSET_TRANSACTION_TYPE_CD]
      ,[STAT_POSTNG_2_COST_CENTR_IND]
      ,[STAT_POSTING_TO_ORDER_IND]
      ,[STAT_POSTING_PROJECT_IND]
      ,[STAT_POSTNG_2_PROFL_ANLYS_IND]
      ,[OPEN_ITEM_MANAGEMENT_IND]
      ,[PAYMENT_TRANSACTION_IND]
      ,[BALANCE_SHEET_ACCOUNT_IND]
      ,[PL_ACCOUNT_TYPE_CD]
      ,[SPECIAL_GL_ALLOCATION_NBR]
      ,[FOLLOWING_DOCUMENT_TYPE_CD]
      ,[BASELINE_PAYMENT_DT]
      ,[PAYMENT_METHOD_CD]
      ,[PAYMENT_BLOCKING_KEY]
      ,[DESTINATION_COUNTRY_CD]
      ,[DESTINATION_COUNTRY_EN_NM]
      ,[DESTINATION_COUNTRY_FR_NM]
      ,[SUPPLYING_COUNTRY_CD]
      ,[SUPPLYING_COUNTRY_EN_NM]
      ,[SUPPLYING_COUNTRY_FR_NM]
      ,[MANUAL_GL_ACCOUNT_IND]
      ,[COMMITMENT_ITEM_KEY]
      ,[REVERSE_CLEARING_IND]
      ,[PAYMENT_METHOD_SUPPLEMENT_CD]
      ,[PAYEE_KEY]
      ,[PROGRAM_ACTIVITY_NBR]
      ,[PRI_NBR]
      ,[FUNCTIONAL_AREA_CD]
      ,[FUNCTIONAL_AREA_EN_NM]
      ,[FUNCTIONAL_AREA_FR_NM]
      ,[FUNDED_PROGRAM_CD]
      ,[ROW_INSERT_DT]
,GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT
FROM (
SELECT
        T2."ACCOUNTING_DOCUMENT_NBR",
        T2."ACCOUNTING_DOCUMENT_ITEM_NUM" as "ACCOUNTING_DOCUMENT_ITEM_NBR",
        T2."FY",
        T2."CLEARING_DOCUMENT_NBR",
        T2."POSTING_TYPE_KEY",
        T2."ACCOUNT_TYPE_CD",
        T2."SPECIAL_GL_TYPE_CD",
        T2."SPECIAL_GL_TRANSCTN_TYPE_CD",
        T2."TARGET_SPECIAL_GL_TYPE_CD",
        T2."DEBIT_CREDIT_CD",
        T2."TAX_CD",
        T2."WITHHOLDING_TAX_CD",
        T2."GL_AMT_CURRENCY_CD",
        T2."TAX_TYPE_CD",
        T2."ALLOCATION_REFERENCE_NBR",
        T2."LINE_ITEM_TEXT",
        T2."TRANSACTION_TYPE_CD",
        T2."GL_TRANSACTION_TYPE_CD",
        T2."FINANCIAL_BUDGET_ITEM_NBR",
        T2."MAIN_ASSET_NBR",
        T2."SUB_ASSET_NBR",
        T2."ASSET_TRANSACTION_TYPE_CD",

CASE
       When T2.STAT_POSTNG_2_COST_CENTR_IND = 'X' Then 1
       Else T2.STAT_POSTNG_2_COST_CENTR_IND
END as STAT_POSTNG_2_COST_CENTR_IND,


CASE
       When T2."STAT_POSTING_TO_ORDER_IND" = 'X' Then 1
       Else T2."STAT_POSTING_TO_ORDER_IND"
END as STAT_POSTING_TO_ORDER_IND,


CASE
       When T2."STAT_POSTING_PROJECT_IND" = 'X' Then 1
       Else T2."STAT_POSTING_PROJECT_IND"
END as STAT_POSTING_PROJECT_IND,


CASE
       When T2."STAT_POSTNG_2_PROFL_ANLYS_IND" = 'X' Then 1
       Else T2."STAT_POSTNG_2_PROFL_ANLYS_IND"
END as STAT_POSTNG_2_PROFL_ANLYS_IND,


CASE
       When T2."OPEN_ITEM_MANAGEMENT_IND" = 'X' Then 1
       Else T2."OPEN_ITEM_MANAGEMENT_IND"
END as OPEN_ITEM_MANAGEMENT_IND,


CASE
       When T2."PAYMENT_TRANSACTION_IND" = 'X' Then 1
       Else T2."PAYMENT_TRANSACTION_IND"
END as PAYMENT_TRANSACTION_IND,


CASE
       When T2."BALANCE_SHEET_ACCOUNT_IND" = 'X' Then 1
       Else T2."BALANCE_SHEET_ACCOUNT_IND"
END as BALANCE_SHEET_ACCOUNT_IND,


        T2."PL_ACCOUNT_TYPE_CD",
        T2."SPECIAL_GL_ALLOCATION_NBR",
        T2."FOLLOWING_DOCUMENT_TYPE_CD",
        T2."BASELINE_PAYMENT_DT",
        T2."PAYMENT_METHOD_CD",
        T2."PAYMENT_BLOCKING_KEY",
        T2."DESTINATION_COUNTRY_CD",
        --T5.EN_COMMON_NM as SUPPLYING_COUNTRY_EN_NM,

        CASE
         when T5.EN_COMMON_NM IS NULL THEN 'Uncoded'
         else T5.EN_COMMON_NM
END as DESTINATION_COUNTRY_EN_NM,


        CASE
         when T5.FR_COMMON_NM IS NULL THEN 'Uncoded'
         else T5.FR_COMMON_NM
END as DESTINATION_COUNTRY_FR_NM,


CASE
         when T5.EN_COMMON_NM IS NULL THEN 'Uncoded'
         else T5.EN_COMMON_NM
END as SUPPLYING_COUNTRY_EN_NM,

CASE
         when T5.FR_COMMON_NM IS NULL THEN 'Uncoded'
         else T5.FR_NM
END as SUPPLYING_COUNTRY_FR_NM,

        T2."SUPPLYING_COUNTRY_CD",


CASE
       When T2."MANUAL_GL_ACCOUNT_IND" = 'X' Then 1
       Else T2."MANUAL_GL_ACCOUNT_IND"
END as MANUAL_GL_ACCOUNT_IND,

        T2."COMMITMENT_ITEM_KEY",

CASE
       When T2."REVERSE_CLEARING_IND" = 'X' Then 1
       Else T2."REVERSE_CLEARING_IND"
END as REVERSE_CLEARING_IND,

        T2."PAYMENT_METHOD_SUPPLEMENT_CD",
        T2."PAYEE_KEY",
        T2."PROGRAM_ACTIVITY_NBR",
        T2."PRI_NBR",
        T2."FUNCTIONAL_AREA_CD",
        T2."FUNDED_PROGRAM_CD",


CASE
         when T3.EN_DESCR IS NULL THEN 'Uncoded'
         else T3.EN_DESCR
END as TRANSACTION_TYPE_EN_DESCR,

CASE
         when T3.FR_DESCR IS NULL THEN 'Uncoded'
         else T3.FR_DESCR
END as TRANSACTION_TYPE_FR_DESCR,


   CASE
         when T6.EN_NM IS NULL THEN 'Uncoded'
         else T6.EN_NM
END as FUNCTIONAL_AREA_EN_NM,

 CASE
         when T6.FR_NM IS NULL THEN 'Uncoded'
         else T6.FR_NM
END as FUNCTIONAL_AREA_FR_NM,

T4."CURRENCY_DESCR_EN",
T4."CURRENCY_DESCR_FR",
        rtrim(cast (isnull(T4."CURRENCY_DESCR_EN",'0') as varchar)) as GL_AMT_CURRENCY_DESCR_EN ,
        rtrim(cast (isnull(T4."CURRENCY_DESCR_FR",'0') as varchar)) as GL_AMT_CURRENCY_DESCR_FR ,

        CAST(getdate() as date) as [ROW_INSERT_DT]
FROM dbo.S_GC_ACCOUNTING_DOC_LINE_ITEM_TMP_K T2


left join dbo.S_GC_TRANSACTION_TYPE_TMP_K T3
on T2.TRANSACTION_TYPE_CD = T3.TRANSACTION_TYPE_CD


left join "dbo"."D_CURRENCY_CODES" T4
on T2.GL_AMT_CURRENCY_CD = T4.CURRENCY_CD  -- Need to add an index

left join dbo.S_GC_COUNTRY_TMP_K T5
on T2.SUPPLYING_COUNTRY_CD = T5.COUNTRY_CD -- Need to add an index

left join dbo.S_GC_FUNCTIONAL_AREA_TMP_K T6
on  T2.FUNCTIONAL_AREA_CD = T6.FUNCTIONAL_AREA_CD  ) T
```

This SQL code inserts data into the `D_GC_ACCOUNTING_DOC_LINE_ITEM` destination table. It selects data from the temporary table `dbo.S_GC_ACCOUNTING_DOC_LINE_ITEM_TMP_K` and joins it with other temporary dimension tables (`dbo.S_GC_TRANSACTION_TYPE_TMP_K`, `"dbo"."D_CURRENCY_CODES"`,  `dbo.S_GC_COUNTRY_TMP_K`, `dbo.S_GC_FUNCTIONAL_AREA_TMP_K`) to populate the dimension columns.

```sql
-- From ESQLT- Truncate D_GC_ACCOUNTING_DOC_LINE_ITEM and Drop Indexes
TRUNCATE TABLE
  dbo.D_GC_ACCOUNTING_DOC_LINE_ITEM;

DROP INDEX IF EXISTS [D_GC_ACCOUNTING_DOC_LINE_ITEM_ACCOUNTING_DOCUMENT_NBR_ix] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [A] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [B] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [C] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];

DROP INDEX IF EXISTS  [ix_pk_GC_ACCOUNTING_DOC_LINE_ITEM] ON [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM];
```

This SQL code truncates the target table `D_GC_ACCOUNTING_DOC_LINE_ITEM` and drops all non-clustered indexes.

```sql
-- From ESQLT-Drop_Temp_Table_All_Dim
--use GC_REPORTING_SSIS_K

DROP TABLE IF EXISTS [dbo].S_GC_TRANSACTION_TYPE_TMP_K;

DROP TABLE IF EXISTS [dbo].S_GC_COUNTRY_TMP_K;

DROP TABLE IF EXISTS [dbo].S_GC_FUNCTIONAL_AREA_TMP_K;
```

This SQL code drops all temporary tables used for staging.

```sql
-- From ESQLT-Insert '03' - D_GC_ACCOUNTING_DOC_LINE_ITEM
SET IDENTITY_INSERT [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM] ON;

INSERT INTO [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM]
           ([ACCOUNTING_DOCUMENT_ITEM_SID]
           ,[ACCOUNTING_DOCUMENT_NBR]
           ,[FY]
           ,[ACCOUNTING_DOCUMENT_ITEM_NBR]
           ,[CLEARING_DOCUMENT_NBR]
           ,[POSTING_TYPE_KEY]
           ,[ACCOUNT_TYPE_CD]
           ,[SPECIAL_GL_TYPE_CD]
           ,[SPECIAL_GL_TRANSCTN_TYPE_CD]
           ,[TARGET_SPECIAL_GL_TYPE_CD]
           ,[DEBIT_CREDIT_CD]
           ,[TAX_CD]
           ,[WITHHOLDING_TAX_CD]
           ,[GL_AMT_CURRENCY_CD]
           ,[GL_AMT_CURRENCY_DESCR_EN]
           ,[GL_AMT_CURRENCY_DESCR_FR]
           ,[TAX_TYPE_CD]
           ,[ALLOCATION_REFERENCE_NBR]
           ,[LINE_ITEM_TEXT]
           ,[TRANSACTION_TYPE_CD]
           ,[TRANSACTION_TYPE_EN_DESCR]
           ,[TRANSACTION_TYPE_FR_DESCR]
           ,[GL_TRANSACTION_TYPE_CD]
           ,[FINANCIAL_BUDGET_ITEM_NBR]
           ,[MAIN_ASSET_NBR]
           ,[SUB_ASSET_NBR]
           ,[ASSET_TRANSACTION_TYPE_CD]
           ,[STAT_POSTNG_2_COST_CENTR_IND]
           ,[STAT_POSTING_TO_ORDER_IND]
           ,[STAT_POSTING_PROJECT_IND]
           ,[STAT_POSTNG_2_PROFL_ANLYS_IND]
           ,[OPEN_ITEM_MANAGEMENT_IND]
           ,[PAYMENT_TRANSACTION_IND]
           ,[BALANCE_SHEET_ACCOUNT_IND]
           ,[PL_ACCOUNT_TYPE_CD]
           ,[SPECIAL_GL_ALLOCATION_NBR]
           ,[FOLLOWING_DOCUMENT_TYPE_CD]
           ,[BASELINE_PAYMENT_DT]
           ,[PAYMENT_METHOD_CD]
           ,[PAYMENT_BLOCKING_KEY]
           ,[DESTINATION_COUNTRY_CD]
           ,[DESTINATION_COUNTRY_EN_NM]
           ,[DESTINATION_COUNTRY_FR_NM]
           ,[SUPPLYING_COUNTRY_CD]
           ,[SUPPLYING_COUNTRY_EN_NM]
           ,[SUPPLYING_COUNTRY_FR_NM]
           ,[MANUAL_GL_ACCOUNT_IND]
           ,[COMMITMENT_ITEM_KEY]
           ,[REVERSE_CLEARING_IND]
           ,[PAYMENT_METHOD_SUPPLEMENT_CD]
           ,[PAYEE_KEY]
           ,[PROGRAM_ACTIVITY_NBR]
           ,[PRI_NBR]
           ,[FUNCTIONAL_AREA_CD]
           ,[FUNCTIONAL_AREA_EN_NM]
           ,[FUNCTIONAL_AREA_FR_NM]
           ,[FUNDED_PROGRAM_CD]
           ,[ROW_INSERT_DT]
           ,[ETL_CREA_DT]
           ,[ETL_UPDT_DT])
(SELECT  top 1
 '-3' as ACCOUNTING_DOCUMENT_ITEM_SID_,
        '-3' as "ACCOUNTING_DOCUMENT_NBR",
        '0000' as "FY",
        '-3' as "ACCOUNTING_DOCUMENT_ITEM_NBR",
        '-3' as "CLEARING_DOCUMENT_NBR",
        '-3' as "POSTING_TYPE_KEY",
        '0' as "ACCOUNT_TYPE_CD",
        '0' as "SPECIAL_GL_TYPE_CD",
        '0' as "SPECIAL_GL_TRANSCTN_TYPE_CD",
        '0' as "TARGET_SPECIAL_GL_TYPE_CD",
        '0' as "DEBIT_CREDIT_CD",
        '-3' as "TAX_CD",
        '-3' as "WITHHOLDING_TAX_CD",
        '-3' as "GL_AMT_CURRENCY_CD",
        'Uncoded' as GL_AMT_CURRENCY_DESCR_EN ,
        'Non codé' as GL_AMT_CURRENCY_DESCR_FR ,
        '0' as "TAX_TYPE_CD",
        '-3' as "ALLOCATION_REFERENCE_NBR",
        '' as "LINE_ITEM_TEXT",
        '-3' as "TRANSACTION_TYPE_CD",
 'Uncoded' as TRANSACTION_TYPE_EN_DESCR,
'Non codé' as TRANSACTION_TYPE_FR_DESCR,
        '-3' as "GL_TRANSACTION_TYPE_CD",
        '-3' as "FINANCIAL_BUDGET_ITEM_NBR",
        '-3' as "MAIN_ASSET_NBR",
        '-3' as "SUB_ASSET_NBR",
        '-3' as "ASSET_TRANSACTION_TYPE_CD",
        '0' as "STAT_POSTNG_2_COST_CENTR_IND",
        '0' as"STAT_POSTING_TO_ORDER_IND",
        '0' as "STAT_POSTING_PROJECT_IND",
        '0' as "STAT_POSTNG_2_PROFL_ANLYS_IND",
        '0' as "OPEN_ITEM_MANAGEMENT_IND",
        '0' as "PAYMENT_TRANSACTION_IND",
        '0' as "BALANCE_SHEET_ACCOUNT_IND",
        '-3' as "PL_ACCOUNT_TYPE_CD",
        '-3' as "SPECIAL_GL_ALLOCATION_NBR",
        '0' as "FOLLOWING_DOCUMENT_TYPE_CD",
        NULL "BASELINE_PAYMENT_DT",
        '0' as "PAYMENT_METHOD_CD",
        '0' as "PAYMENT_BLOCKING_KEY",
        '-3' as "DESTINATION_COUNTRY_CD",
        'Uncoded' as DESTINATION_COUNTRY_EN_NM_,
         'Non codé' as DESTINATION_COUNTRY_FR_NM_,
        '-3' as "SUPPLYING_COUNTRY_CD",
 'Uncoded' as SUPPLYING_COUNTRY_EN_NM_,
 'Non codé'  as SUPPLYING_COUNTRY_FR_NM_,
        '0' as "MANUAL_GL_ACCOUNT_IND",
        '-3' as "COMMITMENT_ITEM_KEY",
        '0' as "REVERSE_CLEARING_IND",
        '-3' as "PAYMENT_METHOD_SUPPLEMENT_CD",
        '-3' as "PAYEE_KEY",
        '-3' as "PROGRAM_ACTIVITY_NBR",
        '-3' as "PRI_NBR",
        '-3' as "FUNCTIONAL_AREA_CD",
'Uncoded' as FUNCTIONAL_AREA_EN_NM,
'Non codé' as FUNCTIONAL_AREA_FR_NM,
        '-3' as "FUNDED_PROGRAM_CD",
        CAST(getdate() as date) as [ROW_INSERT_DT],
    getdate() AS ETL_CREA_DT,
    getdate() AS ETL_UPDT_DT);

SET IDENTITY_INSERT [dbo].[D_GC_ACCOUNTING_DOC_LINE_ITEM] OFF;
```

This SQL code inserts a default row with placeholder values into the `D_GC_ACCOUNTING_DOC_LINE_ITEM` table. It is often used for handling unknown or unmapped scenarios.

```sql
-- From ESQLT-Creating_Temp_Table_All_Dim
--use GC_REPORTING_SSIS_K

DROP TABLE IF EXISTS [dbo].S_GC_TRANSACTION_TYPE_TMP_K;

DROP TABLE IF EXISTS [dbo].S_GC_COUNTRY_TMP_K;

DROP TABLE IF EXISTS [dbo].S_GC_FUNCTIONAL_AREA_TMP_K;

CREATE TABLE [dbo].[S_GC_FUNCTIONAL_AREA_TMP_K](
	[FUNCTIONAL_AREA_CD] [varchar](16) NOT NULL,
	[EN_NM] [varchar](25) NOT NULL,
	[FR_NM] [varchar](25) NOT NULL,
	[VALID_FROM_DT] [nvarchar](10) NULL,
	[VALID_TO_DT] [nvarchar](10) NULL,
	[UPDATE_DT] [datetime2](7) NOT NULL,
	[SOURCE_ID] [varchar](3) NOT NULL,
	[ETL_CREA_DT] [datetime] NOT NULL,
	[ETL_UPDT_DT] [datetime] NOT NULL
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[S_GC_COUNTRY_TMP_K](
	[COUNTRY_CD] [varchar](3) NOT NULL,
	[COUNTRY_ISO_CD] [varchar](3) NULL,
	[EN_NM] [varchar](15) NOT NULL,
	[FR_NM] [varchar](15) NOT NULL,
	[COUNTRY_LEVEL_CD] [varchar](1) NOT NULL,
	[COUNTRY_INTERVENTION_CD] [varchar](1) NOT NULL,
	[CNTRY_OFCL_DVLMNT_ASSTNC_CD] [varchar](1) NOT NULL,
	[COUNTRY_ACTIVE_CD] [varchar](1) NOT NULL,
	[EXTRACT_DT] [datetime2](7) NOT NULL,
	[EN_LONG_NM] [varchar](60) NOT NULL,
	[FR_LONG_NM] [varchar](60) NOT NULL,
	[EN_COMMON_NM] [varchar