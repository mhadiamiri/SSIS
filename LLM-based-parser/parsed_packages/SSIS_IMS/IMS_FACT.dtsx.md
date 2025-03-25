## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| {AB65343F-E6C6-45D9-BA69-82D0AFC2EA84} | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data, destination, truncate tables | SQL Server Auth likely | None            | Part 1                  |
| {37452364-AB82-4570-AB2A-725C7F3B201E} | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data             | SQL Server Auth likely            |  None                  | Part 1                 |
| {B9183ED9-5D9B-4607-B068-453F55DA1186} | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely            |  None                  | Part 1                 |
| IMS_SSIS_DFAIT_REPORTING | OLE DB | Server:  [Inferred], Database: [Inferred] | Used to access lookup tables (Dimension tables) and destination | Depends on the database and authentication method used. Need credentials to access the database. | ParameterMap properties in each Lookup transformation. Ex: ECON_OBJECT_ID | Part 2, Part 3, Part 4 |
| IMS_SSIS_DFAIT_STAGING | OLE DB | Server: [Inferred], Database: [Inferred] | Source data from staging tables (W2_MM_CORRECTIONS, W2_MM_AMENDMENTS, W2_MM_PROCUREMENT) | Depends on the database and authentication method used. Need credentials to access the database. | None apparent in given snippets | Part 2, Part 3, Part 4 |
| Project.ConnectionManagers[IMS_SSIS_DFAIT_REPORTING] | OLE DB | Server=?; Database=?; Authentication=Windows Authentication or similar | Used by OLE DB Destination component to write data | Windows Authentication or SQL Server Authentication | None visible | Part 4 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

### Control Flow

*   Sequence Containers: Used for grouping data flow tasks related to specific fact tables (e.g., F_MM_AMENDMENTS, F_MM_CORRECTIONS, F_MM_PROCUREMENT, F_FIN_ACTUALS, F_FIN_BUDGET, F_FIN_BUDGET_RATES, F_FIN_EXPENDITURE_ADJUSTMENTS).
*   Execute SQL Tasks: Used for truncating destination tables before data loading (e.g., `ESQLT - Truncate F_MM_PROCUREMENT`, `ESQLT- Truncate Staging Tables`).
*   Data Flow Tasks: Used to extract, transform, and load data from staging tables to fact tables (e.g., `DFT-F_MM_AMENDMENTS`, `DFT-F_MM_CORRECTIONS`, `DFT-F_MM_PROCUREMENT`, `DFT-F_FIN_ACTUALS`).

#### DFT-F_MM_AMENDMENTS

*   **Source:** `OLEDB_SRC - W2_MM_AMENDMENTS` extracts data from the `W2_MM_AMENDMENTS` staging table.
*   **Lookups:** Several Lookup transformations are performed to enrich the source data with dimension table SIDs based on corresponding IDs/codes (e.g., `LKP - D_FIN_DOCUMENT_TYPE`, `LKP - D_FIN_ECON_OBJECT`, `LKP - D_FIN_FISCAL_DATE`, `LKP - D_FIN_FUND`, `LKP - D_FIN_GL`, `LKP - D_FIN_VENDOR`, `LKP - D_MM_AGREEMENT_TYPE`, `LKP - D_MM_COMMODITY_TYPE`, `LKP - D_MM_INTELLECTUAL_PROPERTY`, `LKP - D_MM_LIMITED_TENDERING`, `LKP - D_MM_MATERIAL_GROUP`, `LKP - D_MM_PLANT`, `LKP - D_MM_PURCHASING_ORG`, `LKP - D_MM_PURCHASING_GROUP`, `LKP - D_MM_SOLICITATION_PROCEDURE`).
*   **Derived Columns**:  ETL Dates and CALC creates new ETL related columns and calculates values.
*   **Data Conversion:** `DCONV_TRFM-F_MM_PROCUREMENT` performs data type conversions before loading to the fact table.
*   **Destination:**
    *   `OLEDB_DEST - F_MM_AMENDMENTS`: Loads the transformed data into the `F_MM_AMENDMENTS` fact table.
    *   `OLE DB Destination`: Loads rejected data into the `REJECT_IMS_MASTER` table.

#### DFT-F_MM_CORRECTIONS

*   **Source:** `OLEDB_SRC - W1_MM_CORRECTIONS` extracts data from the `W1_MM_CORRECTIONS` staging table.
*   **Derived Columns:** `DRV - ETL Dates and CALC` creates new ETL-related columns.
*   **Lookups:** Similar to DFT-F_MM_AMENDMENTS, several Lookup transformations are used to find dimension SIDs based on source data.
*   **Union All:** `UNIONALL_TRFM-LKP_NO_MATCH`: Combines rows that didn\'t find a match in various lookups.
*   **Destination:**
    *   `OLE DB Destination`: Loads rejected records from lookup transformation into a reject table `REJECT_IMS_MASTER`.
    *   `OLEDB_DEST - F_MM_CORRECTIONS`: Destination to load data into `F_MM_CORRECTIONS`.

#### DFT-F_MM_PROCUREMENT

*   **Source:** `OLEDB_SRC - W2_MM_PROCUREMENT`: Extracts data from the `W2_MM_PROCUREMENT` staging table.
*   **Lookups:** Several lookup transformations are executed to retrieve dimension surrogate keys (SIDs) (e.g., `LKP-D_FIN_FISCAL_DATE`, `LKP-D_FIN_FUND`, `LKP-D_COMMON_FUND_CENTRE`, `LKP-D_FIN_OTHER - VALUE_TYPE`, `LKP-D_FIN_COMPANY`,  `LKP-D_FIN_OTHER - TRANSACTION_CURRENCY`,  `LKP-D_FIN_OTHER - ORDER_TYPE`,  `LKP-D_FIN_OTHER - LC_CURRENCY`,  `LKP-D_FIN_OTHER - PURCHASING_DOC_TYPE`,  `LKP-D_FIN_USER - PURCHASE_DOC_USER`, `LKP- D_MM_AGREEMENT_TYPE`, `LKP- D_MM_METHOD_OF_SUPPLY`, `LKP- D_MM_SOLICITATION_PROCEDURE`, `LKP- D_MM_PLANT`, `LKP- D_MM_PURCHASING_ORG`, `LKP- D_MM_PURCHASING_GROUP`, `LKP- D_MM_MATERIAL_GROUP`, `LKP- D_MM_INTELLECTUAL_PROPERTY`).
*   **Transformation:** `DRV - ETL Dates and CALC`: Derives `ETL_CREA_DT` and `ETL_UPDT_DT` using the `GETDATE()` function.
*   **Conversion:** `DCONV_TRFM-F_MM_PROCUREMENT`: Converts columns to the appropriate datatypes.
*   **Destination:** `OLEDB_DEST - F_MM_PROCUREMENT`: Loads the transformed data into the `F_MM_PROCUREMENT` fact table.

#### DFT-F_FIN_ACTUALS

*   **Source:** `OLEDB_SRC-W3_FIN_ACTUALS`: Extracts data from `dbo.W3_FIN_ACTUALS`.
*   **Transformations:**
    *   `DRV- START_END_DATES`: Derived Column transformation to create `ETL_CREA_DT` and `ETL_UPDT_DT`.
    *   `LKP-D_COMMON_FUND_CENTRE`: Performs a lookup on the `D_COMMON_FUND_CENTRE` dimension table.
    *   `DRV_TRFM-*`: Several derived column transformations to create `REASON` columns based on lookup failures (e.g., `DRV_TRFM-D_FIN_OTHER_ORDER_TYPE.Outputs`, `DRV_TRFM-D_FIN_OTHER_HQ_MISSION_TRANSACTION.Outputs`, `DRV_TRFM-D_FIN_GL_ACCOUNT_DOC_GL_ACCOUNT.Outputs`, `DRV_TRFM-D_FIN_OTHER_ACCOUNT_DOC_DOCUMENT_TYPE.Outputs`, `DRV_TRFM-D_FIN_OTHER_LOCAL_CURRENCY.Outputs`, `DRV_TRFM-D_FIN_OTHER_TRANS_CURRENCY.Outputs`, `DRV_TRFM-D_FIN_WBS_ELEMENT.Outputs`).
    *   `DCONV_TRFM-F_FIN_ACTUALS`: Data Conversion transformation which converts columns to the appropriate data type.
    *   `Union_All_F_FIN_ACTUALS`: Union All transformation combines multiple inputs into one output.
*   **Destinations:**
    *   `OLEDB_DEST-F_FIN_ACTUALS`: Loads data into `[dbo].[F_FIN_ACTUALS]`.
    *   `OLEDB_TRG-REJECT_IMS_MASTER`: Loads rejected rows into the `REJECT_IMS_MASTER` table.

### Parallel Execution Paths

*   Multiple Lookup transformations can operate in parallel depending on resource availability.

## 4. Code Extraction

```sql
-- Source Query for OLEDB_SRC - W2_MM_AMENDMENTS
SELECT	DISTINCT a."PURCHASING_DOCUMENT_NBR",
       "SEQUENCE_NUMBER",
	"FISCAL_PERIOD_BKID",
	"FISCAL_YEAR",
	coalesce("COMPANY_CD",'-') as COMPANY_CD,
       coalesce(a.VENDOR_ACCT_NBR,'-') AS VENDOR_NBR,
	coalesce("COST_CENTRE",'-') as COST_CENTRE,
	"ORDER_NUMBER",
	coalesce("FUND_CENTRE_CD",'-') as FUND_CENTRE_CD,
(CASE
       WHEN LEN("BL_DOCUMENT_TYPE") = 0 THEN '-'
       ELSE "BL_DOCUMENT_TYPE"
END) as BL_DOCUMENT_TYPE,
(CASE
       WHEN LEN(GL_ACCOUNT) = 0 OR GL_ACCOUNT IS NULL THEN '-'
       ELSE GL_ACCOUNT
END) AS GL,
(CASE
       WHEN LEN(ECON_OBJECT_ID) = 0 OR ECON_OBJECT_ID IS NULL THEN '-'
       ELSE ECON_OBJECT_ID
END) AS ECON_OBJECT_ID,
      rtrim(cast(coalesce (a.FUND,'-') as char(10))) as FUND_ID,  
'' as	"PREDECESSOR_DOC_ITEM",
	"VALIDITY_START_DATE",
	"VALIDITY_END_DATE",
	"PO_CREATED_ON_DATE",
	"PURCHASE_DATE",
	"ENTRY_DATE",
	"TIME_OF_ENTRY",
(CASE
       WHEN LEN(COMODITY_TYPE_CD) > 0 THEN COMODITY_TYPE_CD
       ELSE '-'
END ) as COMMODITY_LU,
(CASE
       WHEN LEN("IP_GROUP_CD") > 0 THEN ltrim(rtrim("IP_GROUP_CD"))
       ELSE '-'
END ) as IP_GROUP_LU,
(CASE
       WHEN LEN(LIMITED_TENDERING_CD) > 0 THEN LIMITED_TENDERING_CD
       ELSE '-'
END ) as TENDERING_LU,
       coalesce(a."PLANT_CD",'-') as PLANT_LU,
       coalesce(a."PURCHASING_ORG_CD",'-') as PURCH_ORG_LU,
       coalesce(a."PURCHASING_GROUP_CD",'-') as PURCH_GRP_LU,
       coalesce("MATERIAL_GROUP_CD",'-') as MAT_GRP_LU,
       coalesce("COMMITMENT_ITEM",'-') as COMMITMENT_LU,
(CASE
       WHEN LEN(AGREEMENT_TYPE_CD) > 0 THEN AGREEMENT_TYPE_CD
       ELSE '-'
END) as AGR_TYP_LU,
       coalesce("SOL_PROCEDURE_CD",'-') as SOL_PROC_LU,
       "PROCUREMENT_AWARD_DATE",
       "INCIDENTAL_AWARD_ABORIGINAL",
       "COUNTRY",
       "FORMER_FPS",
       "TERMINATION_DATE",
       "ON_PENSION",
       "ON_INCENTIVE",
       "MULTI_YEAR_CONTRACT",
       DELIVERY_DATE,
	"STATUS",
	"PO_AMENDMENT_SHORT_TXT",
	"AMENDMENT_DATE",
       SO_SA,
       EXCLUSIONS,
       CURRENCY,
       AMENDED_CORRECTED_FLAG,
       PURCHASING_DATE,
       SHORT_TEXT,
---------- Measures -------------------
      CAD_GROSS_PRICE,
      CAD_TAXES,
      CAD_NET_INCL_TAXES,
      "GROSS_PRICE",
      "NET_INCL_TAX",
      "TAXES",
-- change made June 4  Laura wants Amended value to be Amended Value from the override table.
 -- original    "AMENDMENT_AMOUNT" as AMENDMENT_VALUE,
-- new because we now need it at the top line number
--coalesce("AMENDMENT_VALUE","AMENDMENT_AMOUNT") as AMENDMENT_VALUE,
-- this is WRONG as found by Paulette
--(CASE
--      WHEN "SEQUENCE_NUMBER" = '000001' OR len("SEQUENCE_NUMBER") = 0 THEN coalesce("AMENDMENT_VALUE","AMENDMENT_AMOUNT")
 --     ELSE 0
--END) as AMENDMENT_VALUE,
(CASE
        WHEN a."PURCHASING_DOCUMENT_NBR" IN (SELECT DISTINCT "PURCHASE_DOC" FROM "dbo"."S1_MM_ADJUSTMENT_OVERIDES") THEN
          (CASE
                 WHEN "SEQUENCE_NUMBER" = '000001' OR len("SEQUENCE_NUMBER") = 0 THEN T2."AMENDMENT_VALUE"
                 ELSE 0.0
           END)
        ELSE AMENDMENT_AMOUNT
END) as AMENDMENT_VALUE,
(CASE
      WHEN "SEQUENCE_NUMBER" = '000001' OR len("SEQUENCE_NUMBER") = 0 THEN coalesce(coalesce(T2."AMENDED_CONTRACT_VALUE","ORIGINAL_PROCUREMENT_VALUE" + POSITIVE_ADMENDMENTS - NEGATIVE_ADMENDMENTS),0)
      ELSE 0
END) as AMENDED_CONTRACT_VALUE,
      coalesce("CAD_NET_INCL_TAXES",0) as NEW_VALUE,
(CASE
      WHEN "SEQUENCE_NUMBER" = '000001' OR len("SEQUENCE_NUMBER") = 0 THEN  coalesce(T2."ORIGINAL_CONTRACT_VALUE","ORIGINAL_PROCUREMENT_VALUE",0)
      ELSE 0
END) as ORIGINAL_CONTRACT_VALUE,
	coalesce("POSITIVE_ADMENDMENTS",0) as POSITIVE_AMENDMENTS,
	coalesce("NEGATIVE_ADMENDMENTS",0) as NEGATIVE_AMENDMENTS,
	coalesce("LAST_POSITIVE_ADMENDMENTS",0) as LAST_POSITIVE_AMENDMENTS,
	coalesce("LAST_NEGATIVE_ADMENDMENTS",0) as LAST_NEGATIVE_AMENDMENTS
FROM   "dbo"."W2_MM_AMENDMENTS" a LEFT OUTER JOIN "dbo"."S1_MM_ADJUSTMENT_OVERIDES" T2
ON a."PURCHASING_DOCUMENT_NBR" = T2."PURCHASE_DOC"
--where a.PURCHASING_DOCUMENT_NBR = '99'
--where PURCHASING_DOCUMENT_NBR like ('0007308277')
```

Context: This SQL query is used to extract data from the `W2_MM_AMENDMENTS` staging table.

```sql
-- Source Query for OLEDB_SRC - W1_MM_CORRECTIONS
SELECT	
LTRIM(RTRIM("FISCAL_PERIOD_BKID")) AS FISCAL_PERIOD_BKID_LU ,
LTRIM(RTRIM(  coalesce("COST_CENTRE", '-')))   AS COST_CENTRE_LU,
LTRIM(RTRIM("FUND_CENTRE_CD")) AS FUND_CENTRE_CD_LU,
LTRIM(RTRIM(coalesce(cast("FUND_CENTRE_CD" as VARCHAR(100)), 'xxxxx')))  AS FUND_CENTER_ID_LU,
LTRIM(RTRIM("COMPANY_CD")) AS COMPANY_CD_LU,
LTRIM(RTRIM(CASE WHEN LEN(a.VENDOR_ACCT_NBR) > 0 THEN a.VENDOR_ACCT_NBR ELSE '-' END)) AS VENDOR_NBR_LU,
LTRIM(RTRIM((CASE WHEN LEN(BL_DOCUMENT_TYPE) > 0 THEN BL_DOCUMENT_TYPE ELSE '-' END ))) as BL_DOCUMENT_TYPE_LU,
LTRIM(RTRIM((CASE WHEN LEN(GL_ACCOUNT) = 0 OR GL_ACCOUNT IS NULL THEN '-'   ELSE GL_ACCOUNT END))) AS GL_LU,
LTRIM(RTRIM((CASE WHEN LEN(ECON_OBJECT_ID) = 0 OR ECON_OBJECT_ID IS NULL THEN '-' ELSE ECON_OBJECT_ID END))) AS ECON_OBJECT_LU,
LTRIM(RTRIM((CASE WHEN LEN(a.FUND) = 0 OR a.FUND IS NULL THEN '-' ELSE a.FUND END))) as FUND_LU,  
LTRIM(RTRIM((CASE WHEN LEN(COMMITMENT_ITEM) = 0 OR COMMITMENT_ITEM IS NULL THEN '-'  ELSE COMMITMENT_ITEM END))) as COMMITMENT_LU,
LTRIM(RTRIM((CASE WHEN LEN(COMODITY_TYPE_CD) > 0 THEN COMODITY_TYPE_CD ELSE '-' END ))) as COMMODITY_LU,
LTRIM(RTRIM((CASE WHEN LEN("IP_GROUP_CD") > 0 THEN a."IP_GROUP_CD"  ELSE '-' END ))) as IP_GROUP_LU,
LTRIM(RTRIM(LIMITED_TENDERING_CD)) as TENDERING_LU,
LTRIM(RTRIM(coalesce(a."PLANT_CD",'-'))) as PLANT_LU,
LTRIM(RTRIM(coalesce("PURCHASING_ORG_CD",'-'))) as PURCH_ORG_LU,
LTRIM(RTRIM(coalesce("PURCHASING_GROUP_CD",'-'))) as PURCH_GRP_LU,
LTRIM(RTRIM(coalesce("MATERIAL_GROUP_CD",'-'))) as MAT_GRP_LU,
LTRIM(RTRIM((CASE WHEN LEN(AGREEMENT_TYPE_CD) > 0 THEN AGREEMENT_TYPE_CD ELSE '-' END))) as AGR_TYP_LU,
LTRIM(RTRIM(coalesce("SOL_PROCEDURE_CD",'-'))) as SOL_PROC_LU,

"PURCHASING_DOCUMENT_NBR",
	ORDER_NUMBER,
		"FISCAL_YEAR",
	"PREDECESSOR_DOC_ITEM",
	"VALIDITY_START_DATE",
	"VALIDITY_END_DATE",
	"PO_CREATED_ON_DATE",
	"PURCHASE_DATE",
	"ENTRY_DATE",
	"TIME_OF_ENTRY",
	"DELIVERY_DATE",
"PROCUREMENT_AWARD_DATE",
"INCIDENTAL_AWARD_ABORIGINAL",
"COUNTRY",
"FORMER_FPS",
"TERMINATION_DATE",
"ON_PENSION",
"ON_INCENTIVE",
"MULTI_YEAR_CONTRACT",
"STATUS",
"CORRECTION_DATE",
ISNULL("CORRECTION_NBR",'') AS CORRECTION_NBR ,
"CORRECTION_SEQUENCE",
"CORRECTION_AMT",
"CORRECTION_YEAR",
"CORRECTION_REASON_CD",
ISNULL("CORRECTION_REASON_TXT",'') AS CORRECTION_REASON_TXT,
"ACTUAL_ORIGINAL",
"ACTUAL_CONSUMED",
"PURCHASE_REQUISITIONS",
"FUNDS_PRE_COMMITMENT",
"OUTSTANDING_COMMITMENTS",
SO_SA
FROM   "dbo"."W1_MM_CORRECTIONS" a
```

Context: This SQL query is used to extract data from the `W1_MM_CORRECTIONS` staging table.

```sql
SELECT DISTINCT "PURCHASE_DOC_NUMBER"
	,"PURCHASE_DOC_ITEM_NUMBER"
	,LINE_NUMBER
	,a.FISCAL_PERIOD_BKID
	,a.FISCAL_YEAR
	,a.AMOUNT_IN_AREA_CURRENCY AS AMOUNT_IN_AREA_CURRENCY
	,rtrim(CAST("FUND_ID" AS CHAR(10))) AS FUND_ID
	,VALUE_TYPE
	,AMOUNT_TYPE
	,COMPANY_CD
	,a.DESCRIPTION
	,ltrim(rtrim(VENDOR_NBR)) AS VENDOR_NBR
	,a.COMMITMENT_ITEM
	,ltrim(rtrim(TRANSACTION_CURRENCY)) AS TRANSACTION_CURRENCY
	,GL
	,ECON_OBJECT_ID
	,(\
		CASE 
			WHEN LEN(a.WBS_ELEMENT) = 0
				OR a.WBS_ELEMENT IS NULL
				THEN '-'
			ELSE ltrim(rtrim(a.WBS_ELEMENT))
			END
		) AS WBS_ELEMENT
	,ltrim(rtrim(a.COST_CENTRE)) AS COST_CENTRE
	,a.ORDER_NUMBER
	,ORDER_TYPE
	,LC_FM_AREA_CURRENCY_AMOUNT
	,LC_PURCHASE_ORDERS
	,LC_ACTUAL_CONSUMED
	,LC_ACTUAL_ORIGINAL
	,LC_FUNDS_COMMITMENT
	,LC_FUNDS_RESERVATION
	,LC_FUNDS_PRE_COMMITMENT
	,LC_PURCHASE_REQUISITIONS
	,FUND_CENTRE_CD
	,FUND_TYPE
	,a.TRACKING_NBR
	,a.PURCHASE_DOC_HEADER_CREATE_DT
	,PURCHASE_DOC_HEADER_CREATED_BY
	,m.[PRINCIPAL_PURCHASE_AGREEMENT_NBR]    -----Added by Julian on Request of Laura on Nov28, 2023
	,CE_GROUP_BKID
	,a.PREDECESSOR_DOC_NBR
	,a.PREDECESSOR_DOC_ITEM
	,PURCHASE_REQ_NBR
	,LOCAL_CURRENCY_CD
	,a.PURCHASING_DOC_TYPE
	,ORDER_TXT
	,(\
		CASE 
			WHEN LEN(RESP_COST_CENTRE) = 0
				OR RESP_COST_CENTRE IS NULL
				THEN '-'
			ELSE ltrim(rtrim(RESP_COST_CENTRE))
			END
		) AS RESP_COST_CENTRE
	,CONVERSION_RATE
	,RATIO
	,BL_DOCUMENT_TYPE AS BL_DOCUMENT_TYPE_LU
	,EST_ORDER_TOTAL_COST
	,a.VALIDITY_START_DATE
	,a.VALIDITY_END_DATE
	,a.PO_CREATED_ON_DATE
	,a.PURCHASE_DATE
	,a.ENTRY_DATE
	,a.TIME_OF_ENTRY
	,a.CURRENCY
	,a.METHOD_OF_SUPPLY AS METHOD_OF_SUPPLY_LU
	,TARGET_QUANTITY
	,ORDER_UNIT
	,\
	---- procurement dims
	"COMMODITY" AS COMMODITY_LU
	,(\
		CASE 
			WHEN LEN("IP_GROUP") > 0
				THEN rtrim(ltrim(IP_GROUP))
			ELSE '-'
			END
		) AS IP_GROUP_LU
	,TENDERING AS TENDERING_LU
	,"PLANT" AS PLANT_LU
	,"PURCH_ORG" AS PURCH_ORG_LU
	,"PURCH_GRP" AS PURCH_GRP_LU
	,MAT_GRP AS MAT_GRP_LU
	,"AGR_TYP" AS AGR_TYP_LU
	,"SOL_PROC" AS SOL_PROC_LU
	,\
	---- procurement facts
	"PROCUREMENT_AWARD_DATE"
	,"INCIDENTAL_AWARD_ABORIGINAL"
	,"COUNTRY"
	,"FORMER_FPS"
	,"TERMINATION_DATE"
	,"ON_PENSION"
	,"ON_INCENTIVE"
	,"MULTI_YEAR_CONTRACT"
	,DELIVERY_DATE
	,SHORT_TEXT
	,a.SO_SA
	,GROSS_PRICE
	,NET_INCL_TAX
	,TAXES
	,a.RESOURCE_INDICATOR
	,a.RESOURCE_NAME
	,a.CAD_GROSS_PRICE
	,a.CAD_TAXES
	,a.CAD_NET_INCL_TAXES
	,a.EXCHANGE_RATE
	,a.CONTRACT_VALUE
	,a.CAD_CONTRACT_VALUE
	,a.PURCHASING_DATE
	,a.DELETED_FLAG
	,a.ACCT_ASSIGN_PERCENTAGE
	,EXCLUSIONS,\
	a.[TC_ACTUAL_CONSUMED] ,\
	a.[TC_ACTUAL_ORIGINAL],\
	TC_PURCHASE_ORDERS
FROM dbo.W2_MM_PROCUREMENT a
LEFT OUTER JOIN dbo.S1_IMS_PURCHASING_DOC_HEADER m on a.[PURCHASE_DOC_NUMBER] = m.[PURCHASING_DOC_NBR]   -----Added by Julian on Request of Laura on Nov28, 2023
WHERE (\
		a.FISCAL_YEAR >= (\
			SELECT BI_YEAR
			FROM dbo.R_IMS_BI_YEAR_CONTROL
			WHERE BI_YEAR_ID = 1
			)\
		)
```

Context: This SQL query is used to extract data from the `W2_MM_PROCUREMENT` staging table.

```sql
SELECT	"CE_GROUP_SID",
	"CE_GROUP_BKID"
FROM   "dbo"."D_FIN_CE_GROUP"
```

Context: This SQL query is used inside the `LKP-D_FIN_CE_GROUP` Lookup Transformation.

```sql
SELECT	"COMMITMENT_ID",
	"COMMITMENT_SID"
FROM [dbo].[D_FIN_COMMITMENT]
```

Context: This SQL query is used inside the `LKP-D_FIN_COMMITMENT` Lookup Transformation.

```sql
SELECT [COMPANY_SID]
      ,[COMPANY_CD]
  FROM [dbo].[D_FIN_COMPANY]
```

Context: This SQL query is used inside the `LKP-D_FIN_COMPANY` Lookup Transformation.

```sql
SELECT\t"COST_CENTRE_SID",

\tltrim(rtrim("COST_CENTRE_ID")) as 
"COST_CENTRE_ID"
FROM   "dbo"."D_FIN_COST_CENTRE"
```

Context: This SQL query is used inside the `LKP-D_FIN_COST_CENTRE - COST CENTRE` Lookup Transformation.

```sql
SELECT\t
"COST_CENTRE_SID" AS RESP_COST_CENTRE_SID,
LTRIM(RTRIM("COST_CENTRE_ID")) as RESP_COST_CENTRE_ID

FROM   "dbo"."D_FIN_COST_CENTRE"
```

Context: This SQL query is used inside the `LKP-D_FIN_COST_CENTRE - RESP_COST_CENTRE` Lookup Transformation.

```sql
SELECT	"ECON_OBJ_SID",
	"ECON_OBJ_BKID"
FROM   "dbo"."D_FIN_ECON_OBJECT"
```

Context: This SQL query is used inside the `LKP-D_FIN_ECON_OBJECT` Lookup Transformation.

```sql
SELECT	"FISCAL_DATE_BKID",
	"FISCAL_DATE_SID"
FROM   "dbo"."D_FIN_FISCAL_DATE"
```

Context: This SQL query is used inside the `LKP-D_FIN_FISCAL_DATE` Lookup Transformation.

```sql
SELECT RTRIM(FUND_BKID) as FUND_BKID,
FUND_SID    
FROM dbo.D_FIN_FUND
```

Context: This SQL query is used inside the `LKP-D_FIN_FUND` Lookup Transformation.

```sql
SELECT	DIM_BKID,
	DIM_SID
FROM   "dbo"."D_FIN_OTHER"
```

Context: This SQL query is used inside the `LKP-D_FIN_OTHER - *` Lookup Transformations.

```sql
SELECT	"USER_BKID",
	"USER_SID"
FROM   "dbo"."D_FIN_USER"
```

Context: This SQL query is used inside the `LKP-D_FIN_USER - PURCHASE_DOC_USER` Lookup Transformation.

```sql
SELECT\t"VENDOR_SID",

\tltrim(rtrim("VENDOR_ID")) as "VENDOR_ID"

FROM   "dbo"."D_FIN_VENDOR"
```

Context: This SQL query is used inside the `LKP-D_FIN_VENDOR` Lookup Transformation.

```sql
SELECT\tltrim(rtrim("WBS_ELEMENT_BKID")) as "WBS_ELEMENT_BKID",
		"WBS_ELEMENT_SID"

FROM   "dbo"."D_FIN_WBS_ELEMENT"
```

Context: This SQL query is used inside the `LKP-D_FIN_WBS_ELEMENT` Lookup Transformation.

```sql
SELECT	"AGREEMENT_TYPE_SID",
	"AGREEMENT_TYPE_CD"
FROM   "dbo"."D_MM_AGREEMENT_TYPE"
```

Context: This SQL query is used inside the `LKP-D_MM_AGREEMENT_TYPE` Lookup Transformation.

```sql
SELECT\tltrim(rtrim("METHOD_OF_SUPPLY_CD")) as "METHOD_OF_SUPPLY_CD",
        	"METHOD_SUPPLY_SID"

FROM   "dbo"."D_MM_METHOD_OF_SUPPLY"
```

Context: This SQL query is used inside the `LKP-D_MM_METHOD_OF_SUPPLY` Lookup Transformation.

```sql
SELECT	"SP_CD",
	"SP_ID"
FROM   "dbo"."D_MM_SOLICITATION_PROCEDURE"
```

Context: This SQL query is used inside the `LKP-D_MM_SOLICITATION_PROCEDURE` Lookup Transformation.

```sql
TRUNCATE TABLE dbo.F_MM_PROCUREMENT;
```

Context: This SQL query is used in a task to truncate the destination table.

```sql
SELECT coalesce(FUND_CENTER_ID, '-3') as FUND_CENTER_ID_LU,
       coalesce(FISCAL_DATE_BKID, '-3') as FISCAL_DATE_BKID_LU,
       coalesce(VALUE_TYPE_BKID, '-3') as VALUE_TYPE_BKID_LU,
       coalesce(AMOUNT_TYPE_BKID, '-3') as AMOUNT_TYPE_BKID_LU,
       coalesce(TRANSACTION_CURRENCY_BKID, '-3') as TRANSACTION_CURRENCY_BKID_LU,
       coalesce(LOCAL_CURRENCY_BKID, '-3') as LOCAL_CURRENCY_BKID_LU,
       coalesce(COMPANY_CODE, '-3') as COMPANY_CODE_LU,
       coalesce(GL_ACCOUNT, '-3') as GL_ACCOUNT_LU,
       coalesce(COMMITMENT_ITEM, '-3') as COMMITMENT_ITEM_LU,
       coalesce(ACCOUNT_DOC_FUND_ID, '-3') as ACCOUNT_DOC_FUND_ID_LU,
       coalesce(ACCOUNT_DOC_GL_ACCOUNT, '-3') as ACCOUNT_DOC_GL_ACCOUNT_LU,
       coalesce(ACCOUNT_DOC_DOCUMENT_TYPE, '-3') as ACCOUNT_DOC_DOCUMENT_TYPE_LU,
       coalesce(ACCOUNT_DOC_ENTERED_BY, '-3') as ACCOUNT_DOC_ENTERED_BY_LU,
       coalesce(VENDOR_ID, '-3') as VENDOR_ID_LU,
       coalesce(WBS_ELEMENT, '-3') as WBS_ELEMENT_LU,
       coalesce(CE_GROUP_BKID, '-3') as CE_GROUP_BKID_LU,
       coalesce(HQ_MISSION_TRANSACTION_CD, '-3') as HQ_MISSION_TRANSACTION_CD_LU,
       coalesce(RESP_COST_CENTRE, '-3') as RESP_COST_CENTRE_LU,
       coalesce(ORDER_TYPE, '-3') as ORDER_TYPE_LU,
       coalesce(ACCOUNT_DOC_FUND_CENTER_ID, '-3') as ACCOUNT_DOC_FUND_CENTER_ID_LU,

       DOCUMENT_NBR,
       POSTING_LINE,
       ITEM_TXT,
       FISCAL_YEAR,
       FI_DOCUMENT_NBR,
       FI_DOC_ITEM,
       FI_FISCAL_YEAR,
       DOC_DATE,
       ACCOUNT_DOC_PO_NBR,
       ACCOUNT_DOCUMENT_ORDER_NBR,
       ACCOUNT_DOC_AMOUNT_CURRENCY,
       ACCOUNT_DOC_DOCUMENT_DATE,
       ACCOUNT_DOC_ITEM_TEXT,
       ORDER_NBR,
       EST_ORDER_TOTAL_COST,
       POSTING_KEY,
       FUNDS_MGMT_UPDATE_DT,
       PREDECESSOR_DOC_NBR,
       PREDECESSOR_DOC_ITEM,
       ORDER_TXT,
       POSTING_DATE,
       ENTRY_DATE,
       ENTRY_TIMESTAMP,
       CAD_AMOUNT,
       TC_AMOUNT,
       LC_AMOUNT,
       LC_CONVERSION_RATE,
       LC_RATIO

FROM   dbo.W3_FIN_ACTUALS
```

Context: This SQL query is used to extract data from the `W3_FIN_ACTUALS` table.

```sql
SELECT\tFUND_CENTRE_CD,
	FC_SID AS FUND_CENTRE_SID
FROM  D_COMMON_FUND_CENTRE
```

Context: This SQL query is used inside the `LKP-D_COMMON_FUND_CENTRE` Lookup Transformation.

```sql
SELECT [COMMITMENT_SID]