```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| GC_SOURCE_C                   | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source database for data extraction     | Database credentials  | None Explicitly defined, but likely exists as part of the Connection Manager                | Part 1, 2, 3, 4                  |
| GC_STAGING_CONVERTED_ARCHIVE_C | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination database for staging data    | Database credentials  | None Explicitly defined, but likely exists as part of the Connection Manager                 | Part 1, 2, 3, 4                  |
| F3C355AE-F196-4151-B245-806B060954C6  | OLE DB          | Server: [Inferred], Database: [Inferred] | Execute SQL Task     | Database credentials  | None                 | Part 1                  |
| 7901EA11-6732-4C40-BCA3-7069F6ADD75C  | OLE DB          | Server: [Inferred], Database: [Inferred] | OLE DB Destination (Truncate Tables)    | Database credentials  | None                 | Part 1, 2                  |
| BI_Conformed_C | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for data flow task `DFT- TMP_Table_BI_Country` to create a temp table.                                                                                         | Credentials to access the BI Conformed database; potentially encryption for data in transit. | None                 | Part 4 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

The package's control flow consists of multiple sequence containers and individual tasks. The execution order is determined by precedence constraints. Parallel execution is possible as different sequence containers can run in parallel.

*   **Overall Control Flow:**

    1.  `EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - 10 ProcessDataFlowNode`: This appears to be a starting point with an expression task.
    2.  Based on the outcome of the expression task, conditional branching occurs to Sequence Containers.
    3.  `SEQC-Load 10_GCS_Converted_Staging Branch_L` and `SEQC_Create_Common_TMP_Table` after the initial expression task.
    4. `ESQLT- drop_TMP_Table_BI_Country` after the sequence container `SEQC-Load 10_GCS_Converted_Staging Branch_L` and `SEQC-Load 10_GCS_Converted_Staging Branch_C`
*   **Sequence Container Analysis:**
    *   Each sequence container typically contains an Execute SQL Task (ESQLT) to truncate staging tables, followed by one or more Data Flow Tasks (DFT) to load data.
    *   Examples of Sequence Containers:
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_A`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_B`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_C`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_D`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_E`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_F`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_G`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_H`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_I`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_J`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_K`
        *   `SEQC-Load 10_GCS_Converted_Staging Branch_L`
        *   `SEQC_Create_Common_TMP_Table`
*   **Data Flow Task Analysis:**

#### DFT-S_GC_FUNDS_MANAGEMENT_ITEM

*   **Source:** OLE DB Source (OLEDB\_SRC_FMIOI T1) extracts data from `FMIOI` table
*   **Transformations:** `Data Conversion`
*   **Destination:** `OLEDB_DEST_S_GC_FUNDS_MANAGEMENT_ITEM`

#### DFT-S_GC_VENDOR

*   **Source:** OLE DB Source (OLEDB\_SRC_lfa1) extracts data from `lfa1` table
*   **Transformations:** `Data Conversion`
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR`

#### DFT-S_GC_VENDOR_ACCOUNT_GROUP

*   **Source:** OLE DB Source (OLEDB\_SRC-T077Y) extracts data from `T077Y` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST-S_GC_VENDOR_ACCOUNT_GROUP`

#### DFT-S_GC_TAX

*   **Source:** OLE DB Source (OLEDB\_SRC_T007S) extracts data from `T007S` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_TAX`

#### DFT-S_GC_TRADING_PARTNER

*   **Source:** OLE DB Source (OLEDB\_SRC_t880) extracts data from `t880` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_TRADING_PARTNER`

#### DFT-S_GC_TRANSACTION_EVENT_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC_DD07T) extracts data from `DD07T` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_TRANSACTION_EVENT_TYPE`

#### DFT-S_GC_UNITS_OF_MEASUREMENT

*   **Source:** OLE DB Source (OLEDB\_SRC_T006A) extracts data from `T006A` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_UNITS_OF_MEASUREMENT`

#### DFT-S_GC_ACCOUNT_ASSIGNMENTS

*   **Source:** OLE DB Source (OLEDB\_SRC_ekkn) extracts data from `ekkn` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_ACCOUNT_ASSIGNMENTS`

#### DFT-S_GC_VENDOR_CHRACTERISTIC_ALL

*   **Source:** OLE DB Source (OLEDB\_SRC_kssk) extracts data from `kssk` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_CHRACTERISTIC_ALL`

#### DFT-S_GC_VENDOR_CLASS

*   **Source:** OLE DB Source (OLEDB\_SRC_klah) extracts data from `klah` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_CLASS`

#### DFT-S_GC_VENDOR_MULTILINGUALISM

*   **Source:** OLE DB Source (OLEDB\_SRC_zastk) extracts data from `zastk` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_MULTILINGUALISM`

#### DFT-S_GC_HOLDBACK_RELEASE

*   **Source:** OLE DB Source (OLEDB\_SRC_BSIS) extracts data from `BSIS` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_HOLDBACK_RELEASE`

#### DFT-S_GC_PRIORITY_MARKET

*   **Source:** OLE DB Source (OLEDB\_SRC_ZAMM_PRI_MARKET) extracts data from `ZAMM_PRI_MARKET` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PRIORITY_MARKET`

#### DFT-S_GC_PRIORITY_SECTOR

*   **Source:** OLE DB Source (OLEDB\_SRC_ZAMM_PRI_SECTOR) extracts data from `ZAMM_PRI_SECTOR` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PRIORITY_SECTOR`

#### DFT-S_GC_PROPSL_PERFRM_MEASURMNT

*   **Source:** OLE DB Source (OLEDB\_SRC_ZAMM_PERF_MEASUR) extracts data from `ZAMM_PERF_MEASUR` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PROPSL_PERFRM_MEASURMNT`

#### DFT-S_GC_ACCT_ASSIGNMENT_CATEGORY

*   **Source:** OLE DB Source (OLEDB\_SRC_T163I) extracts data from `T163I` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_ACCT_ASSIGNMENT_CATEGORY`

#### DFT-S_GC_ADVANCE_JUSTIFICATION

*   **Source:** OLE DB Source (OLEDB\_SRC_ZZADVJUST) extracts data from `ZZADVJUST` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_ADVANCE_JUSTIFICATION`

#### DFT-S_GC_AGREEMENT_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC_ZZATT) extracts data from `ZZATT` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_AGREEMENT_TYPE`

#### DFT-S_GC_AMENDMENT

*   **Source:** OLE DB Source (OLEDB\_SRC_ZZPRPAME) extracts data from `ZZPRPAME` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_AMENDMENT`

#### DFT-S_GC_CHARACTERISTIC_VALUE

*   **Source:** OLE DB Source (OLEDB\_SRC_AUSP) extracts data from `AUSP` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_CHARACTERISTIC_VALUE`

#### DFT-S_GC_COMMODITY_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC_ZZCTT) extracts data from `ZZCTT` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_COMMODITY_TYPE`

#### DFT-S_GC_CONDITION_ITEM

*   **Source:** OLE DB Source (OLEDB\_SRC_KONV) extracts data from `KONV` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_CONDITION_ITEM`

#### DFT-S_GC_CONDITION_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC_T685T) extracts data from `T685T` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_CONDITION_TYPE`

#### DFT-S_GC_COST_CENTRE

*   **Source:** OLE DB Source (OLEDB\_SRC_csks) extracts data from `csks` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_COST_CENTRE`

#### DFT-S_GC_ENTRY_SHEET

*   **Source:** OLE DB Source (OLEDB\_SRC_ESSR) extracts data from `ESSR` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_ENTRY_SHEET`

#### DFT-S_GC_HISTORY_CATEGORY

*   **Source:** OLE DB Source (OLEDB\_SRC_T163C) extracts data from `T163C` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_HISTORY_CATEGORY`

#### DFT-S_GC_LIMITED_TENDERING_REASON

*   **Source:** OLE DB Source (OLEDB\_SRC_ZZLTT) extracts data from `ZZLTT` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_LIMITED_TENDERING_REASON`

#### DFT-S_GC_PAYMENT

*   **Source:** OLE DB Source (OLEDB\_SRC_EKBE) extracts data from `EKBE` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PAYMENT`

#### DFT-S_GC_PLANT

*   **Source:** OLE DB Source (OLEDB\_SRC_T001W) extracts data from `T001W` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PLANT`

#### DFT-S_GC_PO_DOCUMENT_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC_T161T) extracts data from `T161T` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PO_DOCUMENT_TYPE`

#### DFT-S_GC_PO_LINE_ITEM

*   **Source:** OLE DB Source (OLEDB\_SRC_ EKPO) extracts data from `EKPO` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PO_LINE_ITEM`

#### DFT-S_GC_PO_LINE_ITEM_SCHEDULE

*   **Source:** OLE DB Source (OLEDB\_SRC_ EKPO) extracts data from `EKPO` table.
*   **Transformations:** None
*   **Destination:** `OLEDB_DEST_S_GC_PO_LINE_ITEM_SCHEDULE`

#### DFT-S_GC_PO_VENDOR

*   **Source:** `OLEDB_SRC_EKPA`
*   **Destination:** `OLEDB_DEST_S_GC_PO_VENDOR`

#### DFT-S_GC_SERVICE

*   **Source:** `OLEDB_SRC_ASMDT`
*   **Destination:** `OLEDB_DEST_S_GC_SERVICE`

#### DFT-S_GC_SERVICE_ACCT_ASSIGNMENT

*   **Source:** `OLEDB_SRC_ESKN`
*   **Destination:** `OLEDB_DEST_S_GC_SERVICE_ACCT_ASSIGNMENT`

#### DFT-S_GC_SERVICE_LIMITS

*   **Source:** `OLEDB_SRC_ESUH`
*   **Destination:** `OLEDB_DEST_S_GC_SERVICE_LIMITS`

#### DFT-S_GC_SERVICE_PACKAGE_HEADER

*   **Source:** `OLEDB_SRC_ESLH`
*   **Destination:** `OLEDB_DEST_S_GC_SERVICE_PACKAGE_HEADER`

#### DFT-S_GC_SOLICITATION_PROCEDURE

*   **Source:** `OLEDB_SRC_ZZSPT`
*   **Destination:** `OLEDB_DEST_S_GC_SOLICITATION_PROCEDURE`

#### DFT-S_GC_SUBITEM

*   **Source:** `OLEDB_SRC_ESLL`
*   **Destination:** `OLEDB_DEST_S_GC_SUBITEM`

#### DFT-S_GC_VENDOR_CHARACTERISTIC

*   **Source:** `OLEDB_SRC_kssk`
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_CHARACTERISTIC`

#### DFT-S_GC_VENDOR_CHARACTERISTIC_VALUE

*   **Source:** `OLEDB_SRC_kssk`
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_CHARACTERISTIC_VALUE`

#### DFT-S_GC_VENDOR_OBJECT_CLASS

*   **Source:** `OLEDB_SRC_MARA`
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_OBJECT_CLASS`

#### DFT-S_GC_VENDOR_SUB_CLASS

*   **Source:** `OLEDB_SRC_kssk`
*   **Destination:** `OLEDB_DEST_S_GC_VENDOR_SUB_CLASS`

#### DFT-S_GC_ACTIVITY_TYPE

*   **Source:** `OLEDB_SRC_ZAMM_ACT_TYPE`
*   **Destination:** `OLEDB_DEST_S_GC_ACTIVITY_TYPE`

#### DFT-S_GC_COMPONENT_ACTIVITY_TYPE

*   **Source:** `OLEDB_SRC_ZAMM_CMP_ACT_TPL`
*   **Destination:** `OLEDB_DEST_S_GC_COMPONENT_ACTIVITY_TYPE`

#### DFT-S_GC_COMPONENT_DETAIL

*   **Source:** `OLEDB_SRC_ZAMM_CMP_DETAILS`
*   **Destination:** `OLEDB_DEST_S_GC_COMPONENT_DETAIL`

#### DFT-S_GC_COMPONENT_PRIORTY_MARKET

*   **Source:** `OLEDB_SRC_ZAMM_CMP_PRI_M_L`
*   **Destination:** `OLEDB_DEST_S_GC_COMPONENT_PRIORTY_MARKET`

#### DFT-S_GC_MATERIAL_GROUP

*   **Source:** `OLEDB_SRC_T023T`
*   **Destination:** `OLEDB_DEST_S_GC_MATERIAL_GROUP`

#### DFT-S_GC_MOVEMENT_TYPE

*   **Source:** `OLEDB_SRC_T156T`
*   **Destination:** `OLEDB_DEST_S_GC_MOVEMENT_TYPE`

#### DFT-S_GC_PARS_AUDIT_MESSAGE

*   **Source:** `OLEDB_SRC_ZAPAUD`
*   **Destination:** `OLEDB_DEST_S_GC_PARS_AUDIT_MESSAGE`

#### DFT-S_GC_PURCHASING_GROUP

*   **Source:** `OLEDB_SRC_T024`
*   **Destination:** `OLEDB_DEST_S_GC_PURCHASING_GROUP`

#### DFT-S_GC_PURCHASING_ORGANIZATION

*   **Source:** `OLEDB_SRC_T024E`
*   **Destination:** `OLEDB_DEST_S_GC_PURCHASING_ORGANIZATION`

#### DFT-S_GC_LINE_ITEM_CATEGORY

*   **Source:** `OLEDB_SRC_T163K`
*   **Destination:** `OLEDB_DEST_S_GC_LINE_ITEM_CATEGORY`

#### DFT-S_GC_REGION

*   **Source:** `OLEDB_SRC_TFKB`
*   **Destination:** `OLEDB_DEST_S_GC_REGION`

#### DFT-S_GC_PR_ACCOUNT_ASSIGNMENT

*   **Source:** `OLEDB_SRC_EBKN`
*   **Destination:** `OLEDB_DEST_S_GC_PR_ACCOUNT_ASSIGNMENT`

#### DFT-S_GC_PURCHASE_REQUISITION

*   **Source:** `OLEDB_SRC-EBAN`
*   **Destination:** `OLEDB_DEST_S_GC_PURCHASE_REQUISITION`

#### DFT-S_GC_PROGRAM_ACTIVITY

*   **Source:** `OLEDB_SRC_TFKB`
*   **Destination:** `OLEDB_DEST_S_GC_PROGRAM_ACTIVITY`

#### DFT-S_GC_PURCHASE_ORDER

*   **Source:** `OLEDB_SRC_ekko`
*   **Destination:** `OLEDB_DEST_S_GC_PURCHASE_ORDER`

#### DFT-TMP_Table_BI_Country

*   **Source:** `BI_Conformed_C`
*   **Destination:** `TMP_Table_BI_Country`

## 4. Code Extraction

```sql
-- Source Query for DFT-S_GC_FUNDS_MANAGEMENT_ITEM (OLEDB_SRC_FMIOI T1)
SELECT
	RTRIM(T1.BTART) AS AMOUNT_TYPE_CD
	,RTRIM(T1.BUKRS) AS COMPANY_CD
	,RTRIM(T1.FIKRS) AS fma_cd
	,RTRIM(T1.FIPEX) AS COMMITMENT_ITEM_NBR
	,RTRIM(T1.FISTL) AS FUND_CENTRE_NBR
	,RTRIM(T1.FKBTR) AS AREA_CURRENCY_AMT
	,RTRIM(T1.FONDS) AS FUND_NBR
	,RTRIM(T1.GJAHR) AS FISCAL_YR
--	,RTRIM(T1.HKONT) AS GL_ACCOUNT_NBR
       ,ISNULL(RTRIM(T8.FAS_SAKNR), RTRIM(T1.HKONT)) AS GL_ACCOUNT_NBR
	,RTRIM(T1.LIFNR) AS VENDOR_NBR
	,RTRIM(T1.PERIO) AS FISCAL_PERIOD
	,ISNULL(RTRIM(Z.FAS_EBELN),RTRIM(T1.REFBN)) AS REF_DOC_NBR
	,RTRIM(T1.REFBN) AS  GCS_REF_DOC_NBR
	,RTRIM(T1.RFETE) AS RFRNC_DOC_CLSSN_NBR
	,RTRIM(T1.RFKNT) AS RFRNC_DOC_ACCNT_ASSGN_NBR
	,RTRIM(T1.RFPOS) AS REF_DOC_ITEM_NBR
	,RTRIM(T1.SGTXT) AS ITEM_TEXT
	,T1.TRBTR AS TRANSACTION_CURRENCY_AMT
	,RTRIM(T1.TWAER) AS TRANSACTION_CURENCY_CD
	,RTRIM(T1.WRTTP) vt_cd
        ,'GCS'   AS SOURCE_ID
        ,getdate() AS ETL_CREA_DT
        ,getdate() AS ETL_UPDT_DT
FROM FMIOI T1
LEFT JOIN ZOAT_PORD_MAP Z
	ON T1.REFBN=Z.GCS_EBELN
LEFT JOIN ZOAT_SAKNR_MAP T8
     ON T1.HKONT = T8.GCS_SAKNR
WHERE T1.BTART = '0100'
```

```sql
-- Source Query for DFT-S_GC_VENDOR (OLEDB_SRC_ lfa1)
--use GC_SOURCE_DB
SELECT T1.lifnr,
       'GCS'                            AS SOURCE_ID,
       T2.altkn                         AS PREVIOUS_VENDOR_NBR,
 --      Ltrim(T1.name1)                  AS VENDOR_NM,
 --Change by JL Ticket number 9360

cast( isnull(Rtrim(T1.name1),'') +' '+  isnull(Rtrim(T1.name2),'')+' '+  isnull(Rtrim(T1.name3),'') +' '+  isnull(Rtrim(T1.name4),'')    as varchar(255) )   AS VENDOR_NM,
       Ltrim(Isnull(T3.za_acronym, '')) AS VENDOR_ACRONYM,
       CASE
         WHEN T1.name1 = ' '
               OR T1.name1 = '' THEN NULL
         ELSE Ltrim(T1.name1)
       END                              AS ADDRESS_LINE_1,
       CASE
         WHEN T1.name2 = ' '
               OR T1.name2 = '' THEN NULL
         ELSE Ltrim(T1.name2)
       END                              AS ADDRESS_LINE_2,
       CASE
         WHEN T1.name3 = ' '
               OR T1.name3 = '' THEN NULL
         ELSE T1.name3
       END                              AS ADDRESS_LINE_3,
       CASE
         WHEN T1.name4 = ' '
               OR T1.name4 = '' THEN NULL
         ELSE T1.name4
       END                              AS ADDRESS_LINE_4,
       Isnull(T7.alpha_2_cd, T1.land1)  AS COUNTRY_CD,
       CASE
         WHEN T1.regio = ''
               OR T1.regio = ' ' THEN NULL
         ELSE T1.regio
       END                              AS REGION_CD,
       T1.ort01                         AS CITY_NM,
       T1.ort02                         AS DISTRICT_NM,
       CASE
         WHEN T1.stras = ' '
               OR T1.stras = '' THEN NULL
         ELSE Ltrim(T1.stras)
       END                              AS STREET_ADDR,
       T1.pfach                         AS POSTAL_BOX_NBR,
       T1.pstlz                         AS POSTAL_CD,
       T1.telf1                         AS TELEPHONE_1,
       T1.telf2                         AS TELEPHONE_2,
       T1.telfx                         AS FAX_NBR,
       T1.ktokk                         AS VENDOR_ACCT_GRP,
       T1.konzs                         AS GROUP_KEY,
       T1.kunnr                         AS CUSTOMER_NBR,
       CASE
         WHEN T1.stcd1 = ''
               OR T1.stcd1 = ' ' THEN NULL
         ELSE Ltrim(T1.stcd1)
       END                              AS GST_NBR,
       CASE
         WHEN T2.altkn = ''
               OR T2.altkn = ' ' THEN NULL
         ELSE T2.altkn
       END                              AS AIDIS_REFERENCE_NBR,
       CASE
         WHEN T1.lnrza = ''
               OR T1.lnrza = ' ' THEN NULL
         ELSE T1.lnrza
       END                              AS ALTERNATE_PAYEE_NBR,
       Cast(Getdate() AS DATE)          AS UPDATE_DT,
       T1.lfurl                         AS INTERNET_ADDRESS_URL,
       CASE
         WHEN T2.intad = ''
               OR T2.intad = ' ' THEN NULL
         ELSE T2.intad
       END                              AS EMAIL_ADDRESS_URL,
       CASE
         WHEN T1.vbund = ''
               OR T1.vbund = ' ' THEN NULL
         ELSE T1.vbund
       END                              AS TRADING_PARTNER_COMPANY_NBR,
       CASE
         WHEN T1.loevm = 'X' THEN 1
         ELSE 0
       END                              AS LOGICALLY_DELETED_FL,
       T1.sperr                         AS POSTING_BLOCK_FL,
       T1.sperm                         AS PURCHASING_BLOCK_FL,
       T1.sperz                         AS PAYMENT_BLOCK_FL,
       T1.nodel                         AS DELETION_BLOCK_FL,
       T1.zafi_ch_code                  AS CHANNEL_CD,
       T1.sortl                         AS SEARCH_TERM,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM   lfa1 T1
       LEFT OUTER JOIN lfb1 T2
                    ON T1.lifnr COLLATE latin1_general_ci_as =
                       T2.lifnr COLLATE latin1_general_ci_as
       LEFT JOIN bi_conformed.dbo.bi_country_cd_update T7
              -- not really needed because all trading partners are Canadian
              ON T7.old_alpha_2_cd = T1.land1 COLLATE latin1_general_ci_ai
       LEFT JOIN zastk T3
              ON T3.za_lifnr = T1.lifnr  and ZA_LANG ='E'
--			  where T1.lifnr = '0001016044'
```

```sql
-- Source Query for DFT-S_GC_VENDOR_ACCOUNT_GROUP (OLEDB_SRC-T077Y)
SELECT
     T1.KTOKK as VENDOR_ACCOUNT_GROUP,
     CASE
         WHEN T1.TXT30=' ' or T1.TXT30='' or T1.TXT30 is null then 'UnCoded'
         ELSE T1.TXT30
     END as EN_NM,
     CASE
         WHEN T2.TXT30=' ' or T2.TXT30='' or T2.TXT30 is null then 'Non codé'
         ELSE T2.TXT30
     END as FR_NM,
--     MAX(CASE
--           WHEN T1.SPRAS = 'E' THEN T1.TXT30
--           ELSE ''
--      END) as VENDOR_ACCT_GRP_NM_DESCR_EN,
--     MAX(CASE
--           WHEN T2.SPRAS = 'F' THEN T2.TXT30
--           ELSE 'Non codé'
--     END) as VENDOR_ACCT_GRP_NM_DESCR_FR,
     getdate() as UPDATE_DT,
'GCS' as SOURCE_ID
	   ,getdate() as ETL_CREA_DT
	   ,getdate() as ETL_UPDT_DT
FROM T077Y T1 left join T077Y T2
on T1.KTOKK = T2.KTOKK
and T2.SPRAS = 'F'
Where T1.SPRAS = 'E'
```

```sql
-- Source Query for DFT-S_GC_TAX (OLEDB_SRC_T007S)
SELECT
     T1.MWSKZ as TAX_CD,
     T1.KALSM as PROCEDURE_CD,
     CASE
          WHEN T1.SPRAS = 'E' THEN T1.TEXT1
          ELSE ''
      END as EN_NM,
    CASE
          WHEN T2.SPRAS = 'F' THEN T2.TEXT1
          ELSE 'Non CD'
      END as FR_NM,
      getdate() as UPDATE_DT,
      getdate() as ETL_CREA_DT,
      getdate() as ETL_UPDT_DT,
'GCS' as SOURCE_ID
FROM T007S T1 left join T007S T2
on T1.MWSKZ = T2.MWSKZ
and T1.KALSM  = T2.KALSM
and T2.SPRAS='F'
WHERE T1.KALSM IN ( 'TAXCA' , 'TAXCAJ')
and T1.SPRAS ='E'
```

```sql
-- Source Query for DFT-S_GC_TRADING_PARTNER (OLEDB_SRC_t880)
/*
	USE GC_SOURCE_DB
*/
SELECT rcomp     AS TRADING_PARTNER_COMPANY_NBR,
       name1     AS NAME,
       cntry     AS COUNTRY_CD,
       stret     AS STREET,
       pstlc     AS POSTAL_CD,
       city      AS CITY,
       curr      AS CURRENCY_CD,
       Getdate() AS UPDATE_DT,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT,
'GCS' as SOURCE_ID
FROM   t880
		--LEFT JOIN BI_Conformed.dbo.BI_COUNTRY_CD_UPDATE T7  -- not really needed because all trading partners are Canadian
		--	  ON  T7.OLD_ALPHA_2_CD = cntry Collate Latin1_General_CI_AI
WHERE  rcomp <> 'E'
       AND rcomp <> 'I'

 --and cntry  = 'KV'  -- test should be converted to 'XK' -- Good -- does not exist
```

```sql
-- Source Query for DFT-S_GC_TRANSACTION_EVENT_TYPE (OLEDB_SRC_DD07T)
SELECT
     T1.DOMVALUE_L as TRANSACTION_EVENT_TYPE,
     CASE
         WHEN T1."DDTEXT" is null  THEN 'UnCoded'
         ELSE T1."DDTEXT"
     END as EN_NM,
     CASE
         WHEN T2."DDTEXT" is null THEN 'Non-Codé'
         ELSE T2."DDTEXT"
     END as FR_NM,
     getdate() as UPDATE_DT,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT,
'GCS' as SOURCE_ID
FROM DD07T T1 Left Join DD07T T2
on T1.DOMVALUE_L = T2.DOMVALUE_L
AND T2."DDLANGUAGE" = 'F'
AND T2.DOMNAME = 'VGABE'
WHERE T1."DDLANGUAGE"='E'
AND T1.DOMNAME = 'VGABE'
```

```sql
-- Source Query for DFT-S_GC_UNITS_OF_MEASUREMENT (OLEDB_SRC_T006A)
SELECT
     T1.MSEHI as UOM_ID,
 CASE
        WHEN T1.MSEH6=' ' or T1.MSEH6='' or T1.MSEH6 is null then 'UnCoded'
        ELSE T1.MSEH6
     END as EN_CD,
     CASE
        WHEN T1.MSEHL=' ' or T1.MSEH6='' or T1.MSEH6 is null then 'UnCoded'
        ELSE T1.MSEHL
     END en_num,
     CASE
        WHEN T2.MSEH6=' ' or T2.MSEH6='' or T2.MSEH6 is null  then 'Aucun'
        ELSE T2.MSEH6
     END as FR_CD,
     CASE
        WHEN T2.MSEHL=' ' or T2.MSEH6='' or T2.MSEH6 is null then 'Non codé'
        ELSE T2.MSEHL
     END fr_num,
     getdate() as UPDATE_DT,
     getdate() as ETL_CREA_DT,
     getdate() as ETL_UPDT_DT,
'GCS' as SOURCE_ID
FROM T006A T1 left join T006A T2
on T1.MSEHI=T