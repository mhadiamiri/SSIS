## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| GC_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination:  Used to write data into staging tables, Source for existing data lookup, Creation of temporary tables and deletion of data. | SQL Server permissions: write/insert/update/delete, schema access | None            | Part 1, 2, 3 |
| SAP_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source: Used to extract data from an SAP system.  | SAP permissions: read access, schema access | None            | Part 1, 2, 3 |
| BI_Conformed           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source data from bi_country_cd_update table             | SQL Server Credentials            |  None                  | Part 2, 4 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

The package's control flow consists primarily of sequence containers and data flow tasks implementing upsert logic.

#### EXPRESSIONT- FINANCE Stage 30 - Start Task -ProcessDataFlowNode (Expression Task)

*   This task evaluates the expression `1 == 1`, serving as a placeholder or basic validation.

#### SEQC\_30\_1\_SP\_ACCOUNTING\_DOCUMENT

*   This container holds a single Data Flow Task to insert data into the `S_GC_ACCOUNTING_DOCUMENT` table.

    *   **DFT-Insert-SP\\_ACCOUNTING\\_DOCUMENT**

        *   **Source:** OLE DB Source (`OLEDB_SRC-S_GC_ACCOUNTING_DOCUMENT`) extracts data from the SAP system (`BKPF` table) using the `SAP_SOURCE` connection.
        *   **Destination:** OLE DB Destination (`OLEDB_DEST-GC_ACCOUNTING_DOCUMENT`) inserts the extracted data into the `S_GC_ACCOUNTING_DOCUMENT` table using the `GC_STAGING` connection.
        *   **Transformations:** No explicit transformations between source and destination.
        *   **Error Handling:** `FailComponent` on errors or truncations. Error output is not connected.

#### SEQC\_30\_2\_SP\_ACCOUNTING\_DOC\_LINE\_ITEM

*   This container and its child dataflow task are used for populating the `S_GC_ACCOUNTING_DOC_LINE_ITEM` table.

    *   **DFT-Insert-SP\\_ACCOUNTING\\_DOC\\_LINE\\_ITEM**

        *   **Source:** OLE DB Source (`OLEDB_SRC-BSEG`) extracts data from the SAP system (`BSEG` table) using the `SAP_SOURCE` connection.
        *   **Destination:** OLE DB Destination (`OLEDB_DEST-S_GC_ACCOUNTING_DOC_LINE_ITEM`) inserts the extracted data into the `S_GC_ACCOUNTING_DOC_LINE_ITEM` table using the `GC_STAGING` connection.
        *   **Transformations:** No explicit transformations between source and destination.
        *   **Error Handling:** `FailComponent` on errors or truncations. Error output is not connected.

    *   **SEQC_30_2_1-Update-S_GC_ACCOUNTING_DOC_LINE_ITEM_(DEEMED_VENDOR_NBR)**
        *   Includes data flow and sql execution tasks to update deemed vendor number in the `S_GC_ACCOUNTING_DOC_LINE_ITEM` table.
            *   DFT-Insert-S_GC_ACCOUNTING_DOC_LINE_ITEM_DEEMED_V_TEMP (Data Flow Task): This task pulls data from the `S_GC_ACCOUNTING_DOC_LINE_ITEM` table based on the logic defined in the source query and inserts it into a temporary table `S_GC_ACCOUNTING_DOC_LINE_ITEM_DEEMED_V_TEMP`.
            *   ESQLT- Create_Temp_Table_S_GC_ACCOUNTING_DOC_LINE_ITEM_DEEMED_V_TEMP (Execute SQL Task): This task creates a temporary table.
            *   DFT-Update-S_GC_ACCOUNTING_DOC_LINE_ITEM_(DEEMED) (Execute SQL Task): This task updates the `S_GC_ACCOUNTING_DOC_LINE_ITEM` table by joining it with temporary table and dropping the temporary table.

#### SEQC\_30\_3\_SP\_FUNCTIONAL\_AREA

*   This sequence container and its child dataflow task are used for populating the `S_GC_FUNCTIONAL_AREA` table.

    *   **DFT-Upsert-SP\\_FUNCTIONAL\\_AREA**

        *   **Source:** OLE DB Source (`OLEDB_SRC-TFKB_&_TFKBT_&_TFKBT`) extracts data from the SAP system (`TFKB` and `TFKBT` tables) using the `SAP_SOURCE` connection.
        *   **Lookup:** OLE DB Source (`OLEDB_SRC_Existing_S_GC_FUNCTIONAL_AREA`). It selects data from the table `S_GC_FUNCTIONAL_AREA` (`FUNCTIONAL_AREA_CD`).
        *   **Transformation:** Conditional Split (`CSPLIT_TRFM-Insert_Update`) splits the data into `Insert` and `Update` streams based on whether the Functional Area Code already exists in the destination table.
        *   **Destination:** OLE DB Destination (`OLEDB_DEST-Insert_S_GC_FUNCTIONAL_AREA`) inserts new data into the `S_GC_FUNCTIONAL_AREA` table using the `GC_STAGING` connection.
        *   **Destination:** OLE DB Command (`OLEDB_DEST-Update-S_GC_FUNCTIONAL_AREA`) updates the existing data into the `S_GC_FUNCTIONAL_AREA` table using the `GC_STAGING` connection.

#### SEQC\_30\_4\_SP\_SPECIAL\_GL\_TRANS\_TYPE\_TEXT

*   This sequence container and its child dataflow task are used for populating the `S_GC_ECONOMIC_OBJECT` table.

    *   **DFT-Upsert-SP\\_ECONOMIC\\_OBJECT**

        *   **Source:** OLE DB Source (`OLEDB_SRC-SKAT_&_SKAT`) extracts data from the SAP system (`SKAT` tables) using the `SAP_SOURCE` connection.
        *   **Lookup:** OLE DB Source (`OLEDB_SRC_Existing_S_GC_ECONOMIC_OBJECT`). It selects data from the table `S_GC_ECONOMIC_OBJECT` (`ECONOMIC_OBJECT_NBR`).
        *   **Transformation:** Conditional Split (`CSPLIT_TRFM-Insert_Update`) splits the data into `Insert` and `Update` streams based on whether the Economic Object Number already exists in the destination table.
        *   **Destination:** OLE DB Destination (`OLEDB_DEST-Insert_S_GC_ECONOMIC_OBJECT`) inserts the new data into the `S_GC_ECONOMIC_OBJECT` table using the `GC_STAGING` connection.
        *   **Destination:** OLE DB Command (`OLEDB_DEST-Update-S_GC_ECONOMIC_OBJECT`) updates the existing data into the `S_GC_ECONOMIC_OBJECT` table using the `GC_STAGING` connection.

#### SEQC\_30\_5\_SP\_PAYMNT\_METHD\_SUPLMNT\_TXT

*   This container includes several data flow tasks.

    *   DFT-Upsert-SP\_PAYMNT\_METHD\_SUPLMNT\_TXT
    *   DFT-Upsert-GC\_REVERSAL\_REASON
    *   DFT-Upsert-SP\_PRGRM\_ACTVTY\_FUND\_CNTR\_XREF
    *   DFT-Upsert-SP\_PROCESS\_TYPE
    *   DFT-Upsert-SP\_SPECIAL\_GL\_ACCOUNT
*   The tasks execute sequentially.

    *   **DFT-Upsert-SP\_SPECIAL\_GL\_ACCOUNT**
        *   Performs an upsert operation on the `S_GC_SPECIAL_GL_ACCOUNT` table.

            *   **Source:** `OLEDB_SRC-T074`.  Extracts data from "T074" table in SAP using OLE DB connection `SAP_SOURCE`.

            *   **Source:** `OLEDB_SRC_Existing_S_GC_SPECIAL_GL_ACCOUNT`. Selects existing data from the `S_GC_SPECIAL_GL_ACCOUNT` table in `GC_STAGING` database.

            *   **Transformation:** `MRJ_TRFM-Left_Outer`. Performs a left outer merge join.
            *   **Transformation:** `CSPLIT_TRFM-Insert_Update`.  A conditional split transformation.

            *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_SPECIAL_GL_ACCOUNT`. Inserts new records.
            *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_SPECIAL_GL_ACCOUNT`. Updates existing records. Uses an OLE DB Command.

#### SEQC\_30\_6\_SP\_DOCUMENT\_TYPE

*   This sequence container contains the following data flow tasks:

    *   `DFT-Upsert-SP_DOCUMENT_TYPE`
    *   `DFT-Upsert-SP_FIELD_STATUS_GROUP`
    *   `DFT-Upsert-SP_TRANSACTION_TYPE_GROUP`
    *   `DFT_Upsert-SP_FI_SL_BUDGET_ACTIVITY`
    *   `DFT_Upsert-SP_TRANSACTION_TYPE`
*   No precedence constraints, suggesting parallel execution.

    *   **DFT-Upsert-SP\_DOCUMENT\_TYPE**
        *   Performs an upsert operation on the `S_GC_DOCUMENT_TYPE` table.
            *   **Source:** `OLEDB_SRC-T042H_&_T042H`. Extracts data from "T003" table in SAP using OLE DB connection `SAP_SOURCE`.
            *   **Source:** `OLEDB_SRC_Existing_S_GC_DOCUMENT_TYPE`. Selects existing data from the `S_GC_DOCUMENT_TYPE` table in `GC_STAGING` database.
            *   **Transformation:** `MRJ_TRFM-Left_Outer`. Performs a left outer merge join.
            *   **Transformation:** `CSPLIT_TRFM-Insert_Update`.  A conditional split transformation.
            *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_DOCUMENT_TYPE`. Inserts new records.
            *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_DOCUMENT_TYPE`. Updates existing records. Uses an OLE DB Command.

    *   **DFT-Upsert-SP\_FIELD\_STATUS\_GROUP**
        *   Performs an upsert operation on the `S_GC_FIELD_STATUS_GROUP` table.
            *   **Source:** `OLEDB_SRC-ZZPAF`. Extracts data from "T004F" table in SAP using OLE DB connection `SAP_SOURCE`.
            *   **Source:** `OLEDB_SRC_Existing_S_GC_FIELD_STATUS_GROUP`. Selects existing data from the `S_GC_FIELD_STATUS_GROUP` table in `GC_STAGING` database.
            *   **Transformation:** `MRJ_TRFM-Left_Outer`. Performs a left outer merge join.
            *   **Transformation:** `CSPLIT_TRFM-Insert_Update`.  A conditional split transformation.
            *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_FIELD_STATUS_GROUP`. Inserts new records.
            *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_FIELD_STATUS_GROUP`. Updates existing records. Uses an OLE DB Command.
    *   **DFT-Upsert-SP\_TRANSACTION\_TYPE\_GROUP**
        *   Performs an upsert operation on the `S_GC_TRANSACTION_TYPE_GROUP` table.
            *   **Source:** `OLEDB_SRC-BUPROCESS_&_BUPROCESST_&_BUPROCESST`.  Extracts data from "T856X" table in SAP using OLE DB connection `SAP_SOURCE`.
            *   **Source:** `OLEDB_SRC_Existing_S_GC_TRANSACTION_TYPE_GROUP`. Selects existing data from the `S_GC_TRANSACTION_TYPE_GROUP` table in `GC_STAGING` database.
            *   **Transformation:** `MRJ_TRFM-Left_Outer`. Performs a left outer merge join.
            *   **Transformation:** `CSPLIT_TRFM-Insert_Update`.  A conditional split transformation.
            *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_TRANSACTION_TYPE_GROUP`. Inserts new records.
            *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_TRANSACTION_TYPE_GROUP`. Updates existing records. Uses an OLE DB Command.

    *   **DFT_Upsert-SP\_FI\_SL\_BUDGET\_ACTIVITY**
        *   Performs an upsert operation on the `S_GC_FI_SL_BUDGET_ACTIVITY` table.
            *   **Source:** `OLEDB_SRC-T022_&_T022T_&_T022T`.  Extracts data from "T022" table in SAP using OLE DB connection `SAP_SOURCE`.
            *   **Source:** `OLEDB_SRC_Existing_S_GC_FI_SL_BUDGET_ACTIVITY`. Selects existing data from the `S_GC_FI_SL_BUDGET_ACTIVITY` table in `GC_STAGING` database.
            *   **Transformation:** `MRJ_TRFM-Left_Outer`. Performs a left outer merge join.
            *   **Transformation:** `DRVCOL_TRFM-S_GC_FI_SL_BUDGET_ACTIVITY`. This derived column transformation creates new column values based on expressions.

            *   **Transformation:** `CSPLIT_TRFM-Insert_Update`.  A conditional split transformation.
            *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_FI_SL_BUDGET_ACTIVITY`. Inserts new records.
            *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_FI_SL_BUDGET_ACTIVITY`. Updates existing records. Uses an OLE DB Command.

    *   **DFT_Upsert-SP\_TRANSACTION\_TYPE**
        *   Performs an upsert operation on the `S_GC_TRANSACTION_TYPE` table.
            *   **Source:** OLEDB_SRC-T856\_&_T856T\_&_T856T
#### SEQC\_30\_7\_1\_SP\_COMMITMENT\_ITEM

*   This sequence container encapsulates the data flow for upserting data into the `S_GC_COMMITMENT_ITEM` table. It also creates a temporary table.

    *   **DFT-Upsert-SP\_COMMITMENT\_ITEM**

        *   **Source:** `OLEDB_SRC-S_GC_COMMITMENT_ITEM_TEMP` (reads from temporary table `S_GC_COMMITMENT_ITEM_TEMP`)
        *   **Source:** `OLEDB_SRC_Existing_S_GC_COMMITMENT_ITEM` (reads from `S_GC_COMMITMENT_ITEM` to check existing records)
        *   **Transformation:** `MRJ_TRFM-Left_Outer` (performs a left outer merge join to identify records that need to be inserted or updated). The join is based on `COMMITMENT_ITEM_NBR` and `FY`.
        *   **Transformation:** `CSPLIT_TRFM-Insert_Update` (conditional split transformation divides the data flow into "Insert" and "Update" paths based on whether a matching record exists in the destination).
        *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_COMMITMENT_ITEM` inserts new records into the `S_GC_COMMITMENT_ITEM` table.
        *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_COMMITMENT_ITEM` updates existing records in the `S_GC_COMMITMENT_ITEM` table using an OLE DB Command.
    *   **DFT- TMP_Table_S_GC_COMMITMENT_ITEM_TEMP**

        *   **Source:**  `OLEDB_SRC-FMPOSIT_&_ZOAT_FIPEX_MAP` (reads from SAP tables FMPOSIT and ZOAT_FIPEX_MAP)
        *   **Destination:** `OLEDB_DEST-Insert_S_GC_APPLICATION_OF_FUNDS_TEMP` (inserts into `S_GC_COMMITMENT_ITEM_KEY_XREF_TEMP`).

#### SEQC\_30\_7\_2\_SP\_COMMITMENT\_ITEM\_KEY\_XREF

*   This sequence container encapsulates the data flow for upserting data into the `S_GC_COMMITMENT_ITEM_KEY_XREF` table. It also creates a temporary table.

    *   **DFT-Upsert-SP\_COMMITMENT\_ITEM\_KEY\_XREF**

        *   **Source:** `OLEDB_SRC-S_GC_COMMITMENT_ITEM_KEY_XREF_TEMP` (reads from temporary table `S_GC_COMMITMENT_ITEM_KEY_XREF_TEMP`)
        *   **Source:** `OLEDB_SRC_Existing_S_GC_COMMITMENT_ITEM_KEY_XREF` (reads from `S_GC_COMMITMENT_ITEM_KEY_XREF` to check existing records)
        *   **Transformation:** `MRJ_TRFM-Left_Outer` (performs a left outer merge join to identify records that need to be inserted or updated). The join is based on `COMMITMENT_ITEM_KEY` and `COMMITMENT_ITEM_NBR`.
        *   **Transformation:** `CSPLIT_TRFM-Insert_Update` (conditional split transformation divides the data flow into "Insert" and "Update" paths based on whether a matching record exists in the destination).
        *   **Destination (Insert):** `OLEDB_DEST-Insert_S_GC_COMMITMENT_ITEM_KEY_XREF` inserts new records into the `S_GC_COMMITMENT_ITEM_KEY_XREF` table.
        *   **Destination (Update):** `OLEDB_DEST-Update-S_GC_COMMITMENT_ITEM_KEY_XREF` updates existing records in the `S_GC_COMMITMENT_ITEM_KEY_XREF` table using an OLE DB Command.
    *   **DFT-Insert-SP\_ANNUAL\_BUDGET**

        *   **Source:**  `OLEDB_SRC-FMBDT_&_ZOAT_IMPR_MAP` (reads from SAP table FMBDT, ZOAT_IMPR_MAP)
        *   **Destination:** `OLEDB_DEST-Insert_S_GC_ANNUAL_BUDGET` (inserts into `S_GC_ANNUAL_BUDGET`).

#### SEQC\_30\_9\_1\_SP\_FUNDS\_RESERVATION\_ITEM

*   This sequence container groups tasks related to loading data into `S_GC_FUNDS_RESERVATION_ITEM`.

* Each `OLE DB Destination` component has an `OLE DB Destination Error Output` configured, which allows for capturing errors during the data insertion process. The `errorRowDisposition` property is set to `FailComponent`, meaning that if an error occurs, the entire component will fail.

## 4. Code Extraction

```sql
-- Source query for OLEDB_SRC-S_GC_ACCOUNTING_DOCUMENT (Data Flow in SEQC_30_1_SP_ACCOUNTING_DOCUMENT)
SELECT
RTRIM(BELNR) AS ACCOUNTING_DOCUMENT_NBR,
RTRIM(GJAHR) AS FY,
RTRIM(BLART) AS DOCUMENT_TYPE_CD,
--TO_CHAR(BLDAT ,'YYYY-MM-DD')) AS DOCUMENT_DT,
convert(char(10),BLDAT,120) as DOCUMENT_DT,
convert(char(10),BUDAT,120) as POSTING_DT,
--TO_CHAR(BUDAT,'YYYY-MM-DD')) AS POSTING_DT,
RTRIM(MONAT) AS FISCAL_PERIOD_NBR,
--TO_CHAR(CPUDT,'YYYY-MM-DD')) AS ENTRY_DT,
convert(char(10),CPUDT,120) as ENTRY_DT,
--TO_DT(TO_CHAR(CPUTM),'HH24:MI:SS')) AS ENTRY_TIME,
RTRIM(convert(char,CPUTM,108)) AS ENTRY_TIME,

--TO_CHAR(AEDAT,'YYYY-MM-DD')) AS LAST_DOCUMENT_CHANGE_DT,
convert(char(10),AEDAT,120) as LAST_DOCUMENT_CHANGE_DT,
--TO_CHAR(UPDDT,'YYYY-MM-DD')) AS LAST_DOCUMENT_UPDATE_DT,
convert(char(10),UPDDT,120) as LAST_DOCUMENT_UPDATE_DT,
--TO_CHAR(WWERT,'YYYY-MM-DD')) AS CURRENCY_EXCHANGE_RATE_DT,
convert(char(10),WWERT,120) as CURRENCY_EXCHANGE_RATE_DT,

RTRIM(USNAM) AS LAST_UPDATE_USERID,
RTRIM(substring(TCODE,1,4)) AS TRANSACTION_TYPE_CD,
RTRIM(XBLNR) AS REFERENCE_DOCUMENT_NBR,
RTRIM(BVORG) AS CROSS_COMPANY_TRANSACTION_NUM,
RTRIM(DBBLG) AS RECURRING_ENTRY_DOCUMENT_NUM,
RTRIM(STBLG) AS REVERSING_DOCUMENT_NBR,
RTRIM(STJAH) AS REVERSING_DOC_FY,
CASE
   WHEN BKTXT='' or BKTXT=' ' then null
   ELSE ltrim(rtrim(BKTXT))
END AS DOCUMENT_HEADER_TEXT,
RTRIM(WAERS) AS CURRENCY_CD,
RTRIM(KURSF) AS CURRENCY_EXCHANGE_RATE,
CASE
    WHEN BSTAT=' ' or BSTAT='' then null
    ELSE RTRIM(BSTAT)
END AS DOCUMENT_STATUS_CD,
RTRIM(XNETB) AS DOCUMENT_POSTED_NET_IND,
RTRIM(FRATH) AS UNPLANNED_DELIVERY_COST,
RTRIM(XRUEB) AS POSTED_PREVIOUS_PERIOD_IND,
RTRIM(GLVOR) AS FI_SL_BUSINESS_ACTIVITY_CD,
RTRIM(GRPID) AS BATCH_INPUT_SESSION_NM,
RTRIM(IBLAR) AS INTERNAL_DOCUMENT_TYPE_CD,
RTRIM(AWTYP) AS REFERENCE_PROCEDURE_NM,
RTRIM(AWKEY) AS OBJECT_KEY,
RTRIM(HWAER) AS LOCAL_CURRENCY_CD,
RTRIM(XSTOV) AS DOC_INDGED_FOR_REVRSL_IND,
--TO_CHAR(STODT,'YYYY-MM-DD')) AS PLANNED_REVERSAL_DT,
convert(char(10),STODT,120) as PLANNED_REVERSAL_DT,

RTRIM(XMWST) AS AUTO_TAX_CALCULATION_IND,
RTRIM(XSNET) AS GL_AMTS_EXCLUDES_TAX_IND,
RTRIM(LOTKZ) AS FUNDS_RESERVATION_LOT_NUM,
RTRIM(STGRD) AS REVERSAL_REASON_CD,
RTRIM(PPNAM) AS PARKED_BY_USERID,
RTRIM(ZZBATCHNO) AS RGI_BATCH_NBR,
RTRIM(ZSOURCE) AS RGI_SOURCE_CD,
--ZRUNDATE) AS RGI_RUN_DT,
CONVERT(DATE,ZRUNDATE) AS RGI_RUN_DT,
RTRIM(ZSTATUS) AS RGI_STATUS_CD,
--TO_CHAR(PSOBT,'YYYY-MM-DD')) AS PSO_POSTING_DT,
convert(char(10),PSOBT,120) as PSO_POSTING_DT,
RTRIM(PSOZL) AS PSO_ACTUAL_POSTING_DT,
--TO_CHAR(PSODT ,'YYYY-MM-DD')) AS PSO_LAST_UPDATE_DT,
convert(char(10),PSODT ,120) as PSO_LAST_UPDATE_DT,
--TO_DT(TO_CHAR(PSOTM) ,'HH24:MI:SS')) AS PSO_LAST_UPDATE_TIME,
RTRIM(convert(char,PSOTM,108)) AS PSO_LAST_UPDATE_TIME,

cast(getdate()as date) AS UPDATE_DT,
'FAS' AS SOURCE_ID,

  getdate() AS ETL_CREA_DT,
  getdate() AS ETL_UPDT_DT

FROM   "BKPF"

WHERE GJAHR >= 2018
```

```sql
-- Source query for OLEDB_SRC-BSEG (Data Flow in SEQC_30_2_SP_ACCOUNTING_DOC_LINE_ITEM)
SELECT
  RTRIM(BELNR) AS ACCOUNTING_DOCUMENT_NBR,
  RTRIM(GJAHR) AS FY ,
  RTRIM(BUZEI) AS ACCOUNTING_DOCUMENT_ITEM_NUM,
  convert(date,AUGDT) AS CLEARING_DT,
  convert(date,AUGCP) AS CLEARING_ENTRY_DT,
  RTRIM(AUGBL) AS CLEARING_DOCUMENT_NBR,
  RTRIM(BSCHL) AS POSTING_TYPE_KEY,
  RTRIM(KOART) AS ACCOUNT_TYPE_CD,
  --UMSKZ) AS SPECIAL_GL_TYPE_CD,
  CASE
  WHEN UMSKZ = ' ' then null
  ELSE RTRIM(UMSKZ)
  END  AS SPECIAL_GL_TYPE_CD,

  RTRIM(UMSKS) AS SPECIAL_GL_TRANSCTN_TYPE_CD,
  RTRIM(ZUMSK) AS TARGET_SPECIAL_GL_TYPE_CD,
  RTRIM(SHKZG) AS DEBIT_CREDIT_CD,
  RTRIM(MWSKZ) AS TAX_CD,
  RTRIM(QSSKZ) AS WITHHOLDING_TAX_CD,
  DMBTR AS LOCAL_CURRENCY_AMT,
  WRBTR AS  DOCUMENT_CURRENCY_AMT,
  KZBTR AS  ORIGINAL_REDUCTION_AMT,
  PSWBT AS  GL_UPDATE_AMT,
  RTRIM(PSWSL) AS  GL_AMT_CURRENCY_CD,
  TXBHW AS  ORGNL_LOCL_CURNCY_TAX_BASD_AMT,
  TXBFW AS  ORGNL_DOC_CURNCY_TAX_BASE_AMT,
  MWSTS AS  LOCAL_CURRENCY_TAX_AMT,
  WMWST AS  DOCUMENT_CURRENCY_TAX_AMT,
  HWBAS AS  LOCAL_CURRENCY_TAX_BASE_AMT,
  FWBAS AS  DOCUMENT_CURNCY_TAX_BASE_AMT,
  RTRIM(MWART) AS TAX_TYPE_CD,
  RTRIM(ZUONR) AS ALLOCATION_REFERENCE_NBR,
--  RTRIM(SGTXT) AS LINE_ITEM_TEXT,
  CASE
  WHEN SGTXT = ' ' or SGTXT='' then null
  --ELSE ltrim(rtrim(SGTXT,' '),' ')
  ELSE ltrim(rtrim(SGTXT))
  END  AS LINE_ITEM_TEXT,

  RTRIM(BEWAR) AS TRANSACTION_TYPE_CD,
  RTRIM(ALTKT) AS GL_ACCOUNT_GROUP_NBR,
  RTRIM(VORGN) AS GL_TRANSACTION_TYPE_CD,
  RTRIM(FKONT) AS FINANCIAL_BUDGET_ITEM_NBR,
  RTRIM(KOSTL) AS COST_CENTRE_NBR,
 -- AUFNR) AS ORDER_NBR,
  CASE
  WHEN AUFNR = ' ' then null
  ELSE RTRIM(AUFNR)
  END  AS ORDER_NBR,

  RTRIM(ANLN1) AS MAIN_ASSET_NBR,
  RTRIM(ANLN2) AS SUB_ASSET_NBR,
  RTRIM(ANBWA) AS  ASSET_TRANSACTION_TYPE_CD,
  convert(date,BZDAT) AS  ASSET_VALUE_DT,
  RTRIM(XSKST) AS STAT_POSTNG_2_COST_CENTR_IND,
  RTRIM(XSAUF) AS STAT_POSTING_TO_ORDER_IND,
  RTRIM(XSPRO) AS STAT_POSTING_PROJECT_IND,
  RTRIM(XSERG) AS STAT_POSTNG_2_PROFL_ANLYS_IND,
  RTRIM(XOPVW) AS OPEN_ITEM_MANAGEMENT_IND,
  RTRIM(XZAHL) AS PAYMENT_TRANSACTION_IND,
  RTRIM(HKONT) AS GL_ACCOUNT_NBR,
--  RTRIM(KUNNR) AS CUSTOMER_NBR,
  CASE
  WHEN KUNNR = ' ' then null
  ELSE RTRIM(KUNNR)
  END  AS CUSTOMER_NBR,

 -- LIFNR) AS VENDOR_NBR,
  CASE
  WHEN LIFNR = ' ' then null
  ELSE RTRIM(LIFNR)
  END  AS VENDOR_NBR,

  RTRIM(XBILK) AS BALANCE_SHEET_ACCOUNT_IND,
  RTRIM(GVTYP) AS PL_ACCOUNT_TYPE_CD,
  RTRIM(HZUON) AS SPECIAL_GL_ALLOCATION_NBR,
  RTRIM(REBZT) AS FOLLOWING_DOCUMENT_TYPE_CD,
  convert(char(10), ZFBDT, 120) AS BASELINE_PAYMENT_DT,
  --to_char(ZFBDT,'yyyy-mm-dd')) AS BASELINE_PAYMENT_DT,
  RTRIM(ZLSCH) AS PAYMENT_METHOD_CD,
  RTRIM(ZLSPR) AS PAYMENT_BLOCKING_KEY,
 -- EBELN) AS PO_DOCUMENT_NBR,
RTRIM(ISNULL(T8.FAS_EBELN, nullif(T1.EBELN,''))) AS PO_DOCUMENT_NBR,

  RTRIM(EBELP) AS PO_LINE_ITEM_NBR,
  RTRIM(ZEKKN) AS ACCOUNT_ASSIGNMENT_SERIAL_NUM,
  RTRIM(EGBLD) AS DESTINATION_COUNTRY_CD,
--  RTRIM(EGLLD) AS SUPPLYING_COUNTRY_CD,
 'a' AS SUPPLYING_COUNTRY_CD,
  RTRIM(XHKOM) AS MANUAL_GL_ACCOUNT_IND,
  RTRIM(FIPOS) AS COMMITMENT_ITEM_KEY,
  RTRIM(PROJK) AS WBS_NBR,
--  RTRIM(XRAGL) AS REVERSE_CLEARING_IND,
  CASE
  WHEN XRAGL = ' ' then null
  ELSE RTRIM(XRAGL)
  END  AS REVERSE_CLEARING_IND,

  RTRIM(UZAWE) AS PAYMENT_METHOD_SUPPLEMENT_CD,
--  RTRIM(FISTL) AS FUND_CENTRE_NBR,
  CASE
  WHEN FISTL = ' ' then null
  ELSE RTRIM(FISTL)
  END  AS FUND_CENTRE_NBR,

--  RTRIM(GEBER) AS FUND_NBR,
  CASE
  WHEN GEBER = ' ' then ''
  ELSE RTRIM(GEBER)
  END  AS FUND_NBR,

  --CASE
  --WHEN T2.GCS_GEBER is NULL then ' '
  --ELSE T2.GCS_GEBER
  RTRIM( ' ') AS "GCS_FUND_NBR",  -- The reverse lookup does not work because it produces duplicates.

--  RTRIM(KBLNR) AS FUNDS_RESERVATION_DOC_NUM,
  CASE
  WHEN KBLNR = ' ' then null
  ELSE RTRIM(KBLNR)
  END  AS FUNDS_RESERVATION_DOC_NUM,

  RTRIM(KBLPOS) AS FUNDS_RESERVATION_ITEM_NUM,
  RTRIM(EMPFB) AS PAYEE_KEY,
  RTRIM(ZZGWAC) AS PROGRAM_ACTIVITY_NBR,
  RTRIM(PERNR) AS PRI_NBR,
  cast(getdate() AS date) AS UPDATE_DT,
  RTRIM(VBUND) AS TRADING_PARTNER_COMPANY_NBR,
  RTRIM(FKBER) AS FUNCTIONAL_AREA_CD,
--  CASE
--  WHEN FKBER = ' ' then null
--  ELSE FKBER
--  END  AS FUNCTIONAL_AREA_CD,

 -- MEASURE) AS FUNDED_PROGRAM_CD
   CASE
  WHEN MEASURE = ' ' then null
  ELSE RTRIM(MEASURE)
  END  AS FUNDED_PROGRAM_CD,
'FAS' AS SOURCE_ID,

  getdate() AS ETL_CREA_DT,
  getdate() AS ETL_UPDT_DT

FROM BSEG T1

--LEFT JOIN ZOAT_GEBER_MAP T2 ON
--T1.GEBER=T2.FAS_GEBER  RTRIM(  RTRIM( -- This creates duplicates

LEFT JOIN ZOAT_PORD_MAP T8
ON T1.EBELN=T8.GCS_EBELN

WHERE T1.GJAHR >= 2018
```

```sql
-- Source query used in  DFT-Insert-S_GC_ACCOUNTING_DOC_LINE_ITEM_DEEMED_V_TEMP (Data Flow Task in SEQC_30_2_1-Update-S_GC_ACCOUNTING_DOC_LINE_ITEM_(DEEMED_VENDOR_NBR))
--Business logic taken from following.
--Project SSIS_SWS >>> Package DATA_HUB >>> Data Flow DFT-SAP_ACCOUNTING_DOCUMENT_LINE_ITEM
-- Option 1 : vR300_DEEMED_VENDOR,  VENDOR_NBR if FUND_NBR=R300 and VENDOR_NBR is not NULL
-- Option 2 : vTRADING_PARTNER_VENDOR, TRADING_PARTNER_COMPANY_NBR if it is not NULL
-- Finally, If Option 1 is not NULL, else Option 2

WITH
vR300_DEEMED_VENDOR as (
SELECT dv.ACCOUNTING_DOCUMENT_NBR, dv.FY, dv.VENDOR_NBR as DEEMED_VENDOR_NBR FROM (
