## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_GC_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination database | SQL Server Auth likely | None            | All                  |
| GC_STAGING_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source database | SQL Server Auth likely | None            | All                  |
| GC_REPORTING_SOURCE_C           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source database for currency codes | SQL Server Auth likely | None            | Part 2                  |
| SAP_SOURCE           | OLE DB          | Server: [Inferred]  | Source database | SQL Server Auth likely | None            | Part 2                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All|

## 3. Package Flow Analysis

The package `CONTRACT_DIMENSION` performs several data loading operations into dimension tables. The Control Flow starts with an Expression Task and then proceeds to execute multiple sequence containers that truncate, load, and insert default values into various dimension tables. The package truncates and loads data into the following Dimensions:
`D_GC_ACCOUNT_ASSIGNMENTS`, `D_GC_AGREEMENT_TYPE`, `D_GC_COMMODITY_TYPE`, `D_GC_COST_CENTRE`, `D_GC_MATERIAL_GROUP`, `D_GC_PURCHASE_ORDER`, and `D_GC_SUBITEM`.

#### DFT-D_GC_ACCOUNT_ASSIGNMENTS

*   **Source:** OLE DB Source (OLEDB\_SRC-S\_GC\_ACCOUNT\_ASSIGNMENTS) extracts data from `[dbo].[S_GC_ACCOUNT_ASSIGNMENTS]`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST\_D\_GC\_ACCOUNT\_ASSIGNMENTS) loads data into `[dbo].[D_GC_ACCOUNT_ASSIGNMENTS]`.

#### DFT-D_GC_AGREEMENT_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC\_S\_GC\_AGREEMENT\_TYPE) extracts data from `[dbo].[S_GC_AGREEMENT_TYPE]`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST\_D\_GC\_AGREEMENT\_TYPE) loads data into `[dbo].[D_GC_AGREEMENT_TYPE]`.

#### DFT-D_GC_COMMODITY_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC\_S\_GC_COMMODITY\_TYPE) extracts data from `[dbo].[S_GC_COMMODITY_TYPE]`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST\_D\_GC_COMMODITY\_TYPE) loads data into `[dbo].[D_GC_COMMODITY_TYPE]`.

#### DFT-D_GC_COST_CENTRE

*   **Source:** OLE DB Source (OLEDB\_SRC\_S_GC_COST_CENTRE) extracts data from `dbo.s_gc_cost_centre`.
*   **Transformations:** Data Conversion (DCONV\_TRFM) converts `COST_CENTRE_EN_NM`, `COST_CENTRE_FR_NM`, and `COST_CENTRE_TYPE_CD` to wstr.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST\_D\_GC_COST_CENTRE) loads data into `[dbo].[D_GC_COST_CENTRE]`.

#### DFT-D_GC_MATERIAL_GROUP

*   **Source:** OLE DB Source (OLEDB\_SRC\_S_GC_MATERIAL_GROUP) extracts data from `dbo.S_GC_MATERIAL_GROUP a, dbo.S_GC_MATERIAL_MASTER b`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST\_D\_GC_MATERIAL_GROUP) loads data into `[dbo].[D_GC_MATERIAL_GROUP]`.

#### DFT-D_CURRENCY_CODES_TMP

*   **Source:** OLE DB Source (OLEDB\_SRC-D_CURRENCY_CODES) extracts data from `[dbo].[D_CURRENCY_CODES]`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-D_CURRENCY_CODES_TMP) loads data into `[dbo].[D_CURRENCY_CODES_TMP]`.

#### DFT-D_GC_ADVANCE_JUSTIFICATION

*   **Source:** OLE DB Source (OLEDB\_SRC-S_GC_ADVANCE_JUSTIFICATION_TMP) extracts data from `dbo.S_GC_ADVANCE_JUSTIFICATION_TMP AS AJ LEFT JOIN dbo.D_GC_PO_LINE_ITEM AS DLI ...`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-D_GC_ADVANCE_JUSTIFICATION) loads data into `[dbo].[D_GC_ADVANCE_JUSTIFICATION]`.

#### DFT-S_GC_ADVANCE_JUSTIFICATION_TMP

*   **Source:** OLE DB Source (OLEDB\_SRC-S_GC_ADVANCE_JUSTIFICATION) extracts data from `[dbo].[S_GC_ADVANCE_JUSTIFICATION]`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-S_GC_ADVANCE_JUSTIFICATION_TMP) loads data into `[dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP]`.

#### DFT-Insert-D_GC_PURCHASE_ORDER

*   **Source:** OLE DB Source (OLEDB\_SRC-S_GC_PURCHASE_ORDER) extracts data from `dbo.S_GC_PURCHASE_ORDER a`.
*   **Transformations:** Data Conversion (DCONV_TRFM) converts several string columns to wstr.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-D_GC_PURCHASE_ORDER) loads data into `[dbo].[D_GC_PURCHASE_ORDER]`.

#### DFT-Insert-D_GC_PAYMENT

*   **Source:** OLE DB Source (OLEDB\_SRC-S_GC_PAYMENT) extracts data from `[dbo].[S_GC_PAYMENT] AS P`.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-D_GC_PAYMENT) loads data into `[dbo].[D_GC_PAYMENT]`.

#### DFT-D_GC_PURCHASE_ORDER_LINE_ITEM

*   **Source:** OLE DB Source (OLEDB\_SRC_S_GC_PO_LINE_ITEM) extracts data from a query involving `dbo.S_GC_PO_LINE_ITEM c`.
*   **Transformations:** Data Conversion (DCONV_TRFM) converts some string columns to wstr.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST_D_GC_PURCHASE_ORDER_LINE_ITEM) loads data into `[dbo].[D_GC_PO_LINE_ITEM]`.

#### DFT-Insert-tmp_table

*   **Source:** Two OLE DB Sources (OLEDB\_SRC-T001W_GCS and OLEDB\_SRC-T001W_SAP) extract data from `dbo.T001W` and `SAP_SOURCE.dbo.T001W` respectively.
*   **Transformations:** Union All (Union All) combines the outputs of the two sources.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST-cde_PLANT_TMP) loads data into `[cde_PLANT_TMP]`.

#### DFT-Update_D_GC_VENDOR_SWS

*   **Source:** OLE DB Source (OLEDB\_SRC_D_GC_VENDOR) extracts data from `D_GC_VENDOR DV`.
*   **Transformations:** Data Conversion (DCONV_TRFM) converts string columns to wstr.
*   **Destinations:** OLE DB Command (OLEDB\_CMD_UPDATE_D_GC_VENDOR) updates rows in `dbo.D_GC_VENDOR`. The update statement is `UPDATE DBO.D_GC_VENDOR SET [SWS_VENDOR_CLASSIFICATION_EN_NM] = ?,[SWS_VENDOR_CLASSIFICATION_FR_NM] = ? ,ETL_UPDT_DT = ? WHERE [VENDOR_SID] = ?`.

## 4. Code Extraction

```sql
SELECT distinct
       coalesce([PO_DOCUMENT_NBR],'-3') as PO_DOCUMENT_NBR
      ,coalesce([PO_LINE_ITEM_NBR],'-3') as PO_LINE_ITEM_NBR
      ,coalesce([ACCOUNT_ASSIGNMENT_NBR],'-3') as ACCOUNT_ASSIGNMENT_NBR
      ,coalesce([PROJECT_NBR],'-3') as PROJECT_NBR
      ,coalesce([WBS_NBR],'-3') as WBS_NBR
      ,coalesce([FUNCTIONAL_AREA_CD],'-3') as FUNCTIONAL_AREA_CD
      ,Cast(GetDate() as date) as ROW_INSERT_DT
      ,SOURCE_ID,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
  FROM [dbo].[S_GC_ACCOUNT_ASSIGNMENTS]
```

Context: SQL query used to extract data for loading into the `D_GC_ACCOUNT_ASSIGNMENTS` dimension.

```sql
SELECT
"AGREEMENT_TYPE_CD",
"EN_NM",
"FR_NM",
"UPDATE_DT",
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM "dbo"."S_GC_AGREEMENT_TYPE"
```

Context: SQL query used to extract data for loading into the `D_GC_AGREEMENT_TYPE` dimension.

```sql
select
"COMMODITY_TYPE_CD",
"EN_NM",
"FR_NM",
"UPDATE_DT",
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM "dbo"."S_GC_COMMODITY_TYPE"
```

Context: SQL query used to extract data for loading into the `D_GC_COMMODITY_TYPE` dimension.

```sql
SELECT cost_centre                   AS COST_CENTRE_NBR,
       source_id                     AS SOURCE_ID,
       CAST(parent_cost_centre      AS VARCHAR(10))      AS PARENT_COST_CENTRE_NBR,
       en_nm                         AS COST_CENTRE_EN_NM,
       fr_nm                         AS COST_CENTRE_FR_NM,
       cost_centre_type              AS COST_CENTRE_TYPE_CD,
       CONVERT(DATE, Getdate(), 110) AS ROW_INSERT_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM   dbo.s_gc_cost_centre
```

Context: SQL query used to extract data for loading into the `D_GC_COST_CENTRE` dimension.

```sql
select
 b.material_nbr as MATERIAL_NBR,
 b.en_nm MATERIAL_EN_NM,
 b.fr_nm  MATERIAL_FR_NM,
 a.material_group_cd AS MATERIAL_GROUP_CD,
 a.en_nm MATERIAL_GROUP_EN_NM,
 a.fr_nm MATERIAL_GROUP_FR_NM,
 b.UPDATE_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
 from dbo.S_GC_MATERIAL_GROUP a,
 dbo.S_GC_MATERIAL_MASTER b
 where a.material_group_cd = b.material_group_cd
```

Context: SQL query used to extract data for loading into the `D_GC_MATERIAL_GROUP` dimension.

```sql
SELECT cost_centre                   AS COST_CENTRE_NBR,
       source_id                     AS SOURCE_ID,
       CAST(parent_cost_centre      AS VARCHAR(10))      AS PARENT_COST_CENTRE_NBR,
       en_nm                         AS COST_CENTRE_EN_NM,
       fr_nm                         AS COST_CENTRE_FR_NM,
       cost_centre_type              AS COST_CENTRE_TYPE_CD,
       CONVERT(DATE, Getdate(), 110) AS ROW_INSERT_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM   dbo.s_gc_cost_centre
```

Context: SQL query used to extract data for loading into the `D_GC_COST_CENTRE` dimension.

```sql
SELECT
 b.material_nbr as MATERIAL_NBR,
 b.en_nm MATERIAL_EN_NM,
 b.fr_nm  MATERIAL_FR_NM,
 a.material_group_cd AS MATERIAL_GROUP_CD,
 a.en_nm MATERIAL_GROUP_EN_NM,
 a.fr_nm MATERIAL_GROUP_FR_NM,
 b.UPDATE_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
 from dbo.S_GC_MATERIAL_GROUP a,
 dbo.S_GC_MATERIAL_MASTER b
 where a.material_group_cd = b.material_group_cd
```

Context: SQL query used to extract data for loading into the `D_GC_MATERIAL_GROUP` dimension.

```sql
SELECT
 b.material_nbr as MATERIAL_NBR,
 b.en_nm MATERIAL_EN_NM,
 b.fr_nm  MATERIAL_FR_NM,
 a.material_group_cd AS MATERIAL_GROUP_CD,
 a.en_nm MATERIAL_GROUP_EN_NM,
 a.fr_nm MATERIAL_GROUP_FR_NM,
 b.UPDATE_DT,
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
 from dbo.S_GC_MATERIAL_GROUP a,
 dbo.S_GC_MATERIAL_MASTER b
 where a.material_group_cd = b.material_group_cd
```

Context: SQL query used to extract data for loading into the `D_GC_MATERIAL_GROUP` dimension.

```sql
SELECT
"AGREEMENT_TYPE_CD",
"EN_NM",
"FR_NM",
"UPDATE_DT",
 GETDATE() AS ETL_CREA_DT,
 GETDATE() AS ETL_UPDT_DT
FROM "dbo"."S_GC_AGREEMENT_TYPE"
```

Context: SQL query used to extract data for loading into the `D_GC_AGREEMENT_TYPE` dimension.

```sql
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[D_CURRENCY_CODES_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[D_CURRENCY_CODES_TMP];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP];




CREATE TABLE [dbo].[D_CURRENCY_CODES_TMP](
 [CURRENCY_KEY] [bigint] NOT NULL,
 [CURRENCY_CD] [varchar](7) NULL,
 [CURRENCY_DESCR_EN] [varchar](40) NULL,
 [CURRENCY_DESCR_FR] [varchar](40) NULL,
 [SKEY] [varchar](20) NULL
) ON [PRIMARY];

CREATE TABLE [dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP](
 [PO_DOCUMENT_NBR] [varchar](10) NULL,
 [GCS_PO_DOCUMENT_NBR] [varchar](10) NOT NULL,
 [PO_LINE_ITEM_NBR] [varchar](5) NOT NULL,
 [MATERIAL_DOCUMENT_NBR] [varchar](10) NOT NULL,
 [MATERIAL_DOCUMENT_YEAR] [varchar](4) NOT NULL,
 [ADVANCE_JUST_SERIAL_NBR] [varchar](2) NOT NULL,
 [REFERENCE_MATERIAL_DOC_NBR] [varchar](16) NOT NULL,
 [DECIMAL_CNT] [int] NOT NULL,
 [CURRENCY_KEY] [varchar](5) NOT NULL,
 [EXCHANGE_RATE] [numeric](9, 5) NOT NULL,
 [ADVANCE_JUSTIFICATION_AMT] [numeric](18, 7) NULL,
 [TAX_AMT] [numeric](13, 2) NOT NULL,
 [ITEM_TEXT] [varchar](50) NOT NULL,
 [REVERSE_DOCUMENT_NBR] [varchar](10) NULL,
 [LOGICALLY_DELETED_FLAG] [varchar](1) NULL,
 [USER_NM] [varchar](12) NOT NULL,
 [ACCOUNTING_DOC_ENTRY_DT] [nvarchar](10) NULL,
 [ACCOUNTING_DOC_ENTRY_TIME] [varchar](41) NULL,
 [CREATED_BY_USERID] [varchar](12) NOT NULL,
 [DEBIT_CREDIT_FLAG] [varchar](1) NULL,
 [UPDATE_DT] [datetime2](7) NOT NULL,
 [SOURCE_ID] [varchar](3) NOT NULL,
 [ETL_CREA_DT] [datetime] NOT NULL,
 [ETL_UPDT_DT] [datetime] NOT NULL
) ON [PRIMARY];
GO
```

Context: SQL used to create temporary tables to insert advance justification data.

```sql
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[D_CURRENCY_CODES_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[D_CURRENCY_CODES_TMP];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[S_GC_ADVANCE_JUSTIFICATION_TMP];
```

Context: SQL used to drop temporary tables used in loading advance justification data.

```sql
TRUNCATE TABLE dbo.D_GC_ADVANCE_JUSTIFICATION ;
```

Context: SQL used to truncate the D_GC_ADVANCE_JUSTIFICATION table.

```sql
SET IDENTITY_INSERT DBO.D_GC_ADVANCE_JUSTIFICATION ON;

INSERT [dbo].D_GC_ADVANCE_JUSTIFICATION ([ADVANCE_JUSTIFICATION_SID], [MATERIAL_DOCUMENT_NBR], [MATERIAL_DOCUMENT_YEAR], [ADVANCE_JUST_SERIAL_NBR], [REFERENCE_MATERIAL_DOC_NBR], [CURRENCY_KEY], [CURRENCY_DESCR_EN], [CURRENCY_DESCR_FR],
 [EXCHANGE_RATE], [ITEM_TEXT], [LOGICALLY_DELETED_FLAG], [USER_NM], [CREATED_BY_USERID], [DEBIT_CREDIT_FLAG], [DECIMAL_CNT], [REVERSE_DOCUMENT_NBR], [LOGICALLY_DELETED_IND], 
 [ACCOUNTING_DOC_ENTRY_DT], [ACCOUNTING_DOC_ENTRY_TM], [PURCHASE_ORDER_SID], [PURCHASE_ORDER_NBR], [SOURCE_ID], [PO_LINE_ITEM_SID], [PO_LINE_ITEM_NBR], [ROW_INSERT_DT],ETL_CREA_DT, ETL_UPDT_DT) 
 VALUES (-3, N'-3', N'-3', N'-3', N'-3', N'-3', N'UNCODED', N'NON CODE', CAST(-3.00000 AS Numeric(9, 5)), N'-3',
  NULL, N'-3', N'-3', N'0', NULL, N'-3', N'0', N'-3', N'-3', -3, N'-3', NULL, -3, N'-3', CAST(N'2021-05-08' AS Date), getdate(), getdate());

SET IDENTITY_INSERT DBO.D_GC_ADVANCE_JUSTIFICATION  OFF;
```

Context: SQL used to insert default values into the `D_GC_ADVANCE_JUSTIFICATION` dimension.

```sql
TRUNCATE TABLE dbo.D_GC_COMMODITY_TYPE;
```

Context: SQL used to truncate the `D_GC_COMMODITY_TYPE` table.

```sql
SET IDENTITY_INSERT DBO.D_GC_COMMODITY_TYPE ON;


INSERT [dbo].D_GC_COMMODITY_TYPE ([COMMODITY_TYPE_CD], [EN_NM], [FR_NM], [UPDATE_DT], [COMMODITY_TYPE_SID],ETL_CREA_DT, ETL_UPDT_DT) VALUES (N'-3', N'Uncoded', N'Non codé', N'2021-05-08 21:49:09.057',-3, getdate(), getdate());

SET IDENTITY_INSERT DBO.D_GC_COMMODITY_TYPE OFF;
```

Context: SQL used to insert default values into the `D_GC_COMMODITY_TYPE` dimension.

```sql
TRUNCATE TABLE dbo.D_GC_COST_CENTRE;
```

Context: SQL used to truncate the `D_GC_COST_CENTRE` table.

```sql
SET IDENTITY_INSERT DBO.D_GC_COST_CENTRE ON;


INSERT [dbo].D_GC_COST_CENTRE ([COST_CENTRE_SID], [COST_CENTRE_NBR], [SOURCE_ID], [PARENT_COST_CENTRE_NBR], [COST_CENTRE_EN_NM], [COST_CENTRE_FR_NM], [COST_CENTRE_TYPE_CD], [ROW_INSERT_DT],ETL_CREA_DT, ETL_UPDT_DT)
 VALUES (-3, N'-3', NULL, N'-3', N'Uncoded', N'Non codé', N'-3', CAST(N'2021-05-08' AS Date), getdate(), getdate())


SET IDENTITY_INSERT DBO.D_GC_COST_CENTRE OFF;
```

Context: SQL used to insert default values into the `D_GC_COST_CENTRE` dimension.

```sql
TRUNCATE TABLE dbo.D_GC_MATERIAL_GROUP;
```

Context: SQL used to truncate the D_GC_MATERIAL_GROUP table.

```sql
SET IDENTITY_INSERT DBO.D_GC_MATERIAL_GROUP ON;


INSERT [dbo].D_GC_MATERIAL_GROUP ([MATERIAL_NBR], [MATERIAL_EN_NM], [MATERIAL_FR_NM], [MATERIAL_GROUP_CD], [MATERIAL_GROUP_EN_NM], [MATERIAL_GROUP_FR_NM], [UPDATE_DT], [MATERIAL_SID],ETL_CREA_DT, ETL_UPDT_DT)
 VALUES (N'-3', N'Uncoded', N'Non codé', N'-3', N'Uncoded', N'Non codé', N'2022-05-10 08:19:52.253', N'-3', getdate(), getdate());

 SET IDENTITY_INSERT DBO.D_GC_MATERIAL_GROUP OFF;
```

Context: SQL used to insert default values into the `D_GC_MATERIAL_GROUP` dimension.

```sql
TRUNCATE TABLE dbo.D_GC_PURCHASE_ORDER ;
```

Context: SQL used to truncate the D_GC_PURCHASE_ORDER table.

```sql
SET IDENTITY_INSERT DBO.D_GC_PURCHASE_ORDER ON;


INSERT [dbo].D_GC_PURCHASE_ORDER ([PURCHASE_ORDER_SID], [PO_DOCUMENT_NBR], [GCS_PO_DOCUMENT_NBR], [SOURCE_ID],  [PO_DOCUMENT_TYPE_CD], [PO_LEVEL1_CD], [PO_LEVEL1_EN_NM], 
[PO_LEVEL1_FR_NM], [PO_LEVEL2_CD], [PO_LEVEL2_EN_NM], [PO_LEVEL2_FR_NM], [PO_LEVEL3_CD], [PO_LEVEL3_EN_NM], [PO_LEVEL3_FR_NM], [PO_LEVEL4_CD], [PO_LEVEL4_EN_NM], [PO_LEVEL4_FR_NM], 
[SOLICITATION_PROCEDURE_CD], [SOLICITATION_PROCEDURE_EN_NM], [SOLICITATION_PROCEDURE_FR_NM], [COMMODITY_TYPE_CD], [COMMODITY_TYPE_EN_NM], [COMMODITY_TYPE_FR_NM], [AGREEMENT_TYPE_CD], 
[AGREEMENT_TYPE_EN_NM], [AGREEMENT_TYPE_FR_NM], [LIMIT_TENDERING_REASON_CD], [LMTD_TNDRNG_RSN_EN_NM], [LMTD_TNDRNG_RSN_FR_NM], [PURCHASING_GROUP_CD], [PURCHASING_GROUP_EN_NM], 
[PURCHASING_GROUP_FR_NM], [TYING_STATUS_CD], [TYING_STATUS_EN_NM], [TYING_STATUS_FR_NM], [PO_STATUS_CD], [PO_STATUS_EN_NM], [PO_STATUS_FR_NM], [PURCHASING_ORGANIZATION_CD], 
[PURCHASING_ORGANIZATION_EN_NM], [PURCHASING_ORGANIZATION_FR_NM], [LANGUAGE_CD], [UPDATE_DT], [INCIDENTAL_ABORIGINAL_IND], [FORMER_PUBLIC_SERVANT_IND], [FORMER_PS_INCENTIVE_EXPIRY_DT], 
[FORMER_PS_ON_INCENTIVE_IND], [FORMER_PS_ON_PENSION_IND], [FORMER_PS_TERMNTN_DT], [NO_PWGSC_REPORTING_IND], [CREATED_BY_USERID], [LAST_UPDATED_BY_USERID], [INCOMPLETE_IND],
 [SECURITY_PROVISION_IND], [LOGICALLY_DELETED_IND], [CONDITION_DOCUMENT_NBR], [RESPONSABLE_OFFICER_USER_ID], [ROW_INSERT_DT], [AIDIS_CONTRACT_NBR], [AIDIS_STANDING_OFFER_NBR], 
 [EXCLD_PRCTV_DSCLSR_IND],ETL_CREA_DT, ETL_UPDT_DT) VALUES (-3, N'-3', N'-3', N'-3', N'-3', N'0', N'Uncoded', N'Non codé', N'-3', N'Uncoded', N'Non codé', N'-3', N'Uncoded', 
 N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', N'UNCODED', 
 N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', N'UNCODED', N'NON CODE', -3, N'UNCODED', N'NON CODE', N'-3', N'UNCODED', N'NON CODE', N'-3', 
 CAST(N'2022-05-04' AS Date), 0, 0, CAST(N'2022-05-04' AS Date), 0, 0, CAST(N'2022-05-04' AS Date), 0, N'UNCODED', N'UNCODED', 0, 0, N'0', N'-3', N'-3', 
 CAST(N'2022-05-04' AS Date), N'-3', N'-3', 0, getdate(), getdate());

 SET IDENTITY_INSERT DBO.[D_GC_PURCHASE_ORDER] OFF;
```

Context: SQL used to insert default values into the `D_GC_PURCHASE_ORDER` dimension.

```sql
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_FUNCTIONAL_AREA_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[S_GC_FUNCTIONAL_AREA_TMP];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[cde_PLANT_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[cde_PLANT_TMP];

CREATE TABLE [dbo].[S_GC_FUNCTIONAL_AREA_TMP](
 [FUNCTIONAL_AREA_CD] [varchar](16) NOT NULL,
 [EN_NM] [varchar](25) NOT NULL,
 [FR_NM] [varchar](25) NOT NULL,
 [VALID_FROM_DT] [nvarchar](10) NULL,
 [VALID_TO_DT] [nvarchar](10) NULL,
 [UPDATE_DT] [datetime2](7) NOT NULL,
 [SOURCE_ID] [varchar](3) NOT NULL
) ON [PRIMARY];

CREATE TABLE [dbo].[cde_PLANT_TMP](
 [PLANT_NBR] [varchar](4) NULL,
 [PLANT_NM] [varchar](30) NULL,
 [SOURCE_ID] [varchar](3) NULL
) ON [PRIMARY];
GO
```

Context: SQL used to create temporary tables within the *DFT-Insert-tmp\_table* package.

```sql
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_FUNCTIONAL_AREA_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[S_GC_FUNCTIONAL_AREA_TMP];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[cde_PLANT_TMP]') AND type in (N'U')) 
DROP TABLE [dbo].[cde_PLANT_TMP];
```

Context: SQL used to drop temporary tables within the *DFT-Insert-tmp\_table* package.

```sql
TRUNCATE TABLE dbo.D_GC_SUBITEM ;
```

Context: SQL used to truncate the `D_GC_SUBITEM` table.

```sql
SET IDENTITY_INSERT DBO.D_GC_SUBITEM ON;


INSERT [dbo].D_GC_SUBITEM ([SUBITEM_SID], [PACKAGE_NBR], [INTERNAL_SUB_ITEM_NBR], [SUBITEM_NBR], [SUB_PACKAGE_NBR], [SHORT_TEXT], 
[SERVICE_NBR], [MATERIAL_GROUP_CD], [USERF1_NBR], [USERF2_NBR], [USERF3_NBR], [USERF4_NBR], [ROW_INSERT_DT],ETL_CREA_DT, ETL_UPDT_DT) VALUES (-3,
 N'-3', N'-3', N'-3', N'-3', N'', N'-3',
  N'-3', N'-3', CAST(-3.000 AS Numeric(13, 3)), N'-3', N'-3', 
  CAST(N'2022-05-09' AS Date), getdate(), getdate());


SET IDENTITY_INSERT DBO.D_GC_SUBITEM  OFF;
```

Context: SQL used to insert default values into the `D_GC_SUBITEM` dimension.

```sql
UPDATE DBO.D_GC_VENDOR
SET [SWS_VENDOR_CLASSIFICATION_EN_NM] = ?,
[SWS_VENDOR_CLASSIFICATION_FR_NM] = ?
	  ,ETL_UPDT_DT = ?
WHERE [VENDOR_SID] = ?
```

Context: SQL update command used in the `OLEDB_CMD_UPDATE_D_GC_VENDOR` component.

```sql
WITH t6
     AS (SELECT Row_number()
                  OVER (
                    partition BY VENDOR_NBR, SOURCE_ID
                    ORDER BY VENDOR_CLASS_CD ) rn,
                T6.VENDOR_NBR,
                T6.SOURCE_ID,
                T6.VENDOR_CLASS_NBR,
                T6.VENDOR_CLASS_TYPE_CD,
                T6.VENDOR_TYPE_EN_NM,
                T6.VENDOR_TYPE_FR_NM,
                T6.VENDOR_CLASS_CD,
                T6.VENDOR_CLASS_EN_NM,
                T6.VENDOR_CLASS_FR_NM,
                T6.VENDOR_SUB_CLASS_CD,
                T6.VENDOR_SUB_CLASS_EN_NM,
                T6.VENDOR_SUB_CLASS_FR_NM
         FROM   s_gc_vendor_characteristic_all T6
         WHERE  ( T6.SOURCE_ID = 'GCS'
                  AND T6.VENDOR_CLASS_NBR IN ( '0000000004', '0000000005',
                                               '0000000006',
                                               '0000000007'
                                             )
                  AND T6.VENDOR_CLASS_CD IN ( '0000000046', '0000000047',
                                              '0000000049',
                                              '0000000050',
                                              '0000000067', '0000000068' ) )
                 OR ( T6.SOURCE_ID = 'FAS'
                      AND T6.VENDOR_CLASS_NBR IN ( '0000000445', '0000000446',
                                                   '0000000447',
                                                   '0000000448',
                                                   '0000000449' )
                      AND T6.VENDOR_CLASS_CD IN ( '0000000195', '0000000192',
                                                  '0000000193',
                                                  '0000000194',
                                                  '0000000196', '0000000197' ) )
        ),
     p_org
     AS (-- TFS #1022
        SELECT DISTINCT S_P_ORG.VENDOR_NBR,
                        S_P_ORG.PURCHASING_ORG_NBR,
                        S_P_ORG.BLOCKING_IND
         FROM   s_gc_vendor_purchasing_org S_P_ORG
