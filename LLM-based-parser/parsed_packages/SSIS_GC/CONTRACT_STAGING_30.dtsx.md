## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| GC_STAGING_C           | OLE DB          | Server=?, Database=?, Authentication=?  | Destination for staging data, source for lookups, and temporary tables.  | Requires access to the GC_STAGING_C database. Permissions for writing to the target tables (S_GC_VENDOR_OBJECT_CLASS, S_GC_VENDOR_CLASS, S_GC_VENDOR_MULTILINGUALISM, S_GC_FUNDS_MANAGEMENT_ITEM, etc.). Proper database permissions for read/write operations. Sensitive information such as passwords needs to be securely stored. | None            | Part 1, 2, 3, 4                  |
| SAP_SOURCE           | OLE DB          | Server=?, Database=?, Authentication=?  | Source for extracting data from SAP system. | Requires access to the SAP_SOURCE database. SELECT permissions on tables like KSSK, KLAH, SWOR, ZASTK, EBAN, T024, T024E, CAWN, AUSP, CABNT, T163Y, T023T, MARA, T156T, FMIOI, ZOAT_PORD_MAP, lfm1, ZZADVJUST, T163I, ZAMM_PRI_SECTOR, csks, cskt, KONV, ZZLTT, kssk, klah, swor, ksml, ausp, cabnt, cawn, ESSR, T163C,T685T, EKKN, lfa1, T007Y, ZZPRPAME, T007S, t880, DD07T. Sensitive information such as passwords needs to be securely stored.            |  None                  | Part 1, 2, 3, 4                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

*   The package `CONTRACT_STAGING_30.DTSX` performs the following operations:

1.  **EXPRESSIONT- Stage 30 - Start Task -- Process Data Flow Node:** An Expression Task with the expression "1 == 1".  This task likely serves as a starting point or a placeholder. It doesn't perform any actual data manipulation.

2.  Several Sequence Containers, each loading data into staging tables. Common pattern: Extract, Lookup, Transform (Merge Join, Conditional Split), Load (Insert or Update).
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_A`
        *   `DFT-S_GC_VENDOR_OBJECT_CLASS`
        *   `DFT-S_SP_VENDOR_CLASS`
        *   `DFT-S_SP_VENDOR_MULTILINGUISM`
        *   `DFT_Insert_S_GC_FUNDS_MANAGEMENT_ITEM`
        *   `DFT_UpdateDelete_S_GC_FUNDS_MANAGEMENT_ITEM`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_B`
        *   `DFT-S_SP_VENDOR_PURCHASING_ORG`
        *   `DFT_Insert- S_GC_ADVANCE_JUSTIFICATION`
        *   `DFT_Upsert-S_GC_ACCT_ASSIGNMENT_CATEGORY`
        *   `DFT_Upsert-S_GC_PRIORITY_SECTOR`
        *   `DFT_S_SP_VENDOR_PURCHASING_ORG`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_C`
        *   `DFT-S_SP_VENDOR_CHARACTERISTIC_ALL`
        *   `DFT_Upsert-S_GC_HOLDBACK_RELEASE`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_D`
        *   `DFT-S_SP_COST_CENTRE`
        *   `DFT_Insert-S_GC_CONDITION_ITEM 1 1`
        *   `DFT_S_GC_LIMITED_TENDERING_REASON`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_I`
        *   `DFT-S_SP_VENDOR_CHARACTERISTIC`
        *   `DFT-S_SP_VENDOR_CHARACTERISTIC_VALUE`
        *   `DFT-S_SP_VENDOR_SUB_CLASS`
        *   `DFT_Upsert_ S_GC_ACTIVITY_TYPE`
        *   `ESQLT- Truncate S_SP_ AUTHORITY`
        *   `DFT-S_SP_ AUTHORITY`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_J`
        *   `DFT_Upsert-S_GC_COMPONENT_ACTIVITY_TYPE`
        *   `DFT_Upsert-S_GC_COMPONENT_DETAIL`
        *   `DFT_Upsert-S_GC_COMPONENT_PRIORTY_MARKET`
        *   `DFT_Upsert-S_GC_COMPONENT_QUANTITY_RESULT`
        *   `DFT_Upsert-S_GC_EXPENSE_TYPE`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_K`
        *   `DFT_Upsert-S_GC_LINE_ITEM_CATEGORY`
        *   `DFT_Upsert-S_GC_MATERIAL_GROUP`
        *   `DFT_Upsert-S_GC_MATERIAL_MASTER`
        *   `DFT_upsert-S_GC_MOVEMENT_TYPE`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_L`
        *   `DFT_Upsert-S_GC_PURCHASE_REQUISITION`
        *   `DFT_Upsert-S_GC_PURCHASING_GROUP`
        *   `DFT_Upsert-S_GC_PURCHASING_ORGANIZATION`
        *   `DFT_Upsert-S_GC_REGION`
        *   `ESQL-Create_tmp_Table`
        *   `DFT-Insert_S_GC_PR_ACCOUNT_ASSIGNMENT_TMP`
        *   `ESQL-Delete \_Duplicate\_Rows\_From\_Tmp\_Table`
        *   `DFT_Upsert-S_GC_PR_ACCOUNT_ASSIGNMENT`
        *   `ESQL-Drop\_tmp\_Table`
    *   `SEQC-Load 30_GCS_Converted_Staging Branch_M`
        *   `DFT-Insert_S_GC_ACCOUNT_ASSIGNMENTS_TMP`
        *   `DFT-S_SP_VENTOR`
        *   `DFT-S_SP_VENDOR_ACCOUNT_GROUP`
        *   `DFT_Upsert-S_GC_ACCOUNT_ASSIGNMENTS`
        *   `DFT_Upsert-S_GC_AMENDMENT`
        *   `DFT_Upsert-S_GC_TAX`
        *   `DFT_Upsert-S_GC_TRADING_PARTNER`
        *   `DFT_Upsert-S_GC_TRANSACTION_EVENT_TYPE`

#### DFT\\_Upsert-S_GC_CONDITION_TYPE

*   **Source:** OLE DB Source (OLEDB\\_SRC_T685T) - Extracts data from the `T685T` table in the SAP system.
*   **Source:** OLE DB Source (OLEDB\\_SRC\\_S_GC_CONDITION_TYPE) - Extracts data from the `S_GC_CONDITION_TYPE` table in the staging database.
*   **Transformation:** Merge Join (MRGJOIN_TRFM-Left_Outer) - Performs a left outer join between the data from the two OLE DB sources, matching on `CONDITION_TYPE_CD` and `APPLICATION_CD`.
*   **Transformation:** Conditional Split (CSPLIT_TRFM) - Routes the data based on whether a match was found in the staging database:
    *   **Insert:** If no match is found (new record), the data is routed to the insert destination.
    *   **Update:** If an existing record is found, the data is routed to the update command.
    *   **Default Output:** Route is not defined
*   **Destination:** OLE DB Destination (OLEDB\\_DEST_Insert-S\\_GC_CONDITION_TYPE) - Inserts new records into the `S_GC_CONDITION_TYPE` table.
*   **Destination:** OLE DB Command (OLEDBCMD\\_TRFM-Update_S_GC_CONDITION_TYPE) - Updates existing records in the `S_GC_CONDITION_TYPE` table.

#### DFT_Upsert_ S_GC_ACTIVITY_TYPE
*   **Source:** OLEDB_SRC_ZAMM_ACT_TYPE (SAP_SOURCE)
    *   Extracts data from the `ZAMM_ACT_TYPE` table in SAP.
*   **Destination:** OLEDBCMD_TRFM-Update_S_GC_ACTIVITY_TYPE (GC_STAGING_C) and OLEDB_DEST_Insert-S_GC_ACTIVITY_TYPE (GC_STAGING_C)
    *   The data flow performs an "upsert" operation, updating existing records and inserting new ones into the `[dbo].[S_GC_ACTIVITY_TYPE]` table.
    *   Transformation:
        *   Merge Join Transformation, Join Type = Left Outer
        *   Conditional Split Transformation, route data for either an update or an insert based on if the target exist.
        *   OLE DB Command Transformation, update S_GC_ACTIVITY_TYPE if target exist.
        *   OLE DB Destination Transformation, insert S_GC_ACTIVITY_TYPE if target doesn\'t exist.

## 4. Code Extraction

```sql
-- Source query for OLEDB_SRC-KSSK
SELECT
     OBJEK as VENDOR_NBR,
     KLART as VENDOR_CLASS_TYPE_CD,
     CLINT as VENDOR_CLASS_NBR,
     GETDATE() as UPDATE_DT,
     'FAS' as SOURCE_ID,
GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT
FROM KSSK
WHERE KLART = '010'
```

```sql
-- Source query for OLEDB_SRC_S_GC_VENDOR_CLASS
SELECT
     T1.CLINT	VENDOR_CLASS_NBR,
     T1.KLART	VENDOR_CLASS_TYPE_CD,
CASE
      WHEN T2."KSCHL" is null  THEN 'UnCoded'
      ELSE T2."KSCHL"
END as EN_NM,
CASE
      WHEN T3."KSCHL" is null THEN 'Non-Codé'
      ELSE T3."KSCHL"
END as FR_NM,
     NULL as CREATED_BY_USERID,
     NULL as CREATION_DT,
     NULL as LAST_UPDATED_BY_USERID,
     NULL as LAST_UPDATE_DT,
     getdate() as UPDATE_DT,
     'FAS' as SOURCE_ID,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM "KLAH" T1 join "SWOR" T2
on T1."CLINT" = T2."CLINT"
left join "SWOR" T3
on T1."CLINT" = T3."CLINT"
AND T3."SPRAS" = 'F'
WHERE T2."SPRAS"='E'
AND T1.KLART = '010'
```

```sql
-- Source query for OLEDB_SRC_S_SP_VENDOR_MULTILINGUISM
SELECT T1."za_lifnr"
       + Space(10 - Len(T1."za_lifnr")) AS VENDOR_NBR,
       T1.za_lang                       AS DETAIL_LANGUAGE_CD,
       T1.za_off_lang                   AS OFFICIAL_LANGUAGE_CD,
       T1.za_name1                      AS VENDOR_OPERATING_NM_LINE_1,
       T1.za_name2                      AS VENDOR_OPERATING_NM_LINE_2,
       T1.za_acronym                    AS VENDOR_ACRONYM,
       T1.za_url                        AS INTERNET_ADDRESS_URL,
       T1."za_url_lang"                 AS URL_LANGUAGE_CD,
       T1.za_addr1                      AS MAILING_ADDRESS_LINE_1,
       T1.za_addr2                      AS MAILING_ADDRESS_LINE_2,
       T1.za_city                       AS MAILING_CITY_NM,
       T1.za_region_cd                  AS MAILING_REGION_CD,
       T1.za_postal_cd                  AS MAILING_POSTAL_CD,
       isnull(cast(T7.ALPHA_2_CD as varchar(3)), T1.za_cntry_cd) AS MAILING_COUNTRY_CD,
       T1.za_pa_addr1                   AS PHYSICAL_ADDRESS_LINE_1,
       T1.za_pa_addr2                   AS PHYSICAL_ADDRESS_LINE_2,
       T1.za_pa_city                    AS PHYSICAL_CITY_NM,
       T1.za_pa_region_cd               AS PHYSICAL_REGION_CD,
       T1.za_pa_postal_cd               AS PHYSICAL_POSTAL_CD,
       T1.za_pa_cntry_cd                AS PHYSICAL_COUNTRY_CD,
       T1.za_email                      AS EMAIL_ADDRESS_URL,
       T1.za_telphn                     AS MAIN_TELEPHONE_NBR,
       T1.za_fax                        AS MAIN_FAX_NBR,
       T1.za_create_dt                  AS CREATION_DT,
       T1.za_update_dt                  AS LAST_UPDATED_DT,
       T1.za_userid                     AS CREATED_BY_USER_ID,
       T1.za_search_term                AS SEARCH_TERM,
       Getdate()                        AS UPDATE_DT,
       'FAS'                            AS SOURCE_ID,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM   zastk T1
	   LEFT JOIN BI_Conformed.dbo.BI_COUNTRY_CD_UPDATE T7
			  ON  T7.OLD_ALPHA_2_CD = T1.za_cntry_cd Collate Latin1_General_CI_AI
```

```sql
-- Source query for OLEDB_SRC_FMIOI
SELECT
	RTRIM(T1.BTART) AS AMOUNT_TYPE_CD
	,RTRIM(T1.BUKRS) AS COMPANY_CD
	,RTRIM(T1.FIKRS) AS FIN_MANAGEMENT_AREA_CD
	,RTRIM(T1.FIPEX) AS COMMITMENT_ITEM_NBR
	,RTRIM(T1.FISTL) AS FUND_CENTRE_NBR
	,RTRIM(T1.FKBTR) AS AREA_CURRENCY_AMT
	,RTRIM(T1.FONDS) AS FUND_NBR
	,RTRIM(T1.GJAHR) AS FISCAL_YR
	,RTRIM(T1.HKONT) AS GL_ACCOUNT_NBR
	,RTRIM(T1.LIFNR) AS VENDOR_NBR
	,RTRIM(T1.PERIO) AS FISCAL_PERIOD
	,RTRIM(T1.REFBN) AS REF_DOC_NBR
	,ISNULL(RTRIM(Z.GCS_EBELN),' ') AS GCS_REF_DOC_NBR
	,RTRIM(T1.RFETE) AS RFRNC_DOC_CLSSN_NBR
	,RTRIM(T1.RFKNT) AS RFRNC_DOC_ACCNT_ASSGN_NBR
	,RTRIM(T1.RFPOS) AS REF_DOC_ITEM_NBR
	,RTRIM(T1.SGTXT) AS ITEM_TEXT
	,T1.TRBTR AS TRANSACTION_CURRENCY_AMT
	,RTRIM(T1.TWAER) AS TRANSACTION_CURENCY_CD
	,RTRIM(T1.WRTTP) AS VALUE_TYPE_CD
	,'FAS' AS SOURCE_ID
	   ,getdate() AS ETL_CREA_DT
	   ,getdate() AS ETL_UPDT_DT
FROM FMIOI T1
LEFT JOIN ZOAT_PORD_MAP Z ON
T1.REFBN=Z.FAS_EBELN
WHERE T1.BTART = '0100'
AND T1.REFBN IS NOT NULL
```

```sql
-- Delete statement for OLEDB_CMD_Update_S_GC_FUNDS_MANAGEMENT_ITEM
DELETE FROM  dbo.S_GC_FUNDS_MANAGEMENT_ITEM
 	  where  	[REF_DOC_NBR]  = ? and
	[REF_DOC_ITEM_NBR]  = ? and
	[RFRNC_DOC_ACCNT_ASSGN_NBR]  = ? and
	[RFRNC_DOC_CLSSN_NBR]  = ? and
	[FISCAL_YR]  = ? and
	[FISCAL_PERIOD]  = ? and
	[AMOUNT_TYPE_CD] = ?
```

```sql
-- Source query for OLEDB_SRC_FMIOI (used in DFT_UpdateDelete_S_GC_FUNDS_MANAGEMENT_ITEM)
SELECT
RTRIM(T1.REFBN) AS REF_DOC_NBR
	,RTRIM(T1.RFPOS) AS REF_DOC_ITEM_NBR
	,RTRIM(T1.RFKNT) AS RFRNC_DOC_ACCNT_ASSGN_NBR
	,RTRIM(T1.RFETE) AS RFRNC_DOC_CLSSN_NBR
	,RTRIM(T1.GJAHR) AS FISCAL_YR
	,RTRIM(T1.PERIO) AS FISCAL_PERIOD
	,RTRIM(T1.BTART) AS AMOUNT_TYPE_CD
FROM FMIOI T1
LEFT JOIN ZOAT_PORD_MAP Z ON
T1.REFBN=Z.FAS_EBELN
WHERE T1.BTART = '0100'
AND T1.REFBN IS NOT NULL
order by RTRIM(T1.REFBN) ASC,
	RTRIM(T1.RFPOS) ASC,
	RTRIM(T1.RFKNT ) ASC,
	RTRIM(T1.RFETE) ASC,
	RTRIM(T1.GJAHR ) ASC,
	RTRIM(T1.PERIO) ASC,
	RTRIM(T1.BTART ) ASC
```

```sql
-- Source query for OLEDB_SRC_S_GC_FUNDS_MANAGEMENT_ITEM (used in DFT_UpdateDelete_S_GC_FUNDS_MANAGEMENT_ITEM)
select 	[REF_DOC_NBR]  ,
	[REF_DOC_ITEM_NBR]  ,
	[RFRNC_DOC_ACCNT_ASSGN_NBR]  ,
	[RFRNC_DOC_CLSSN_NBR]  ,
	[FISCAL_YR]  ,
	[FISCAL_PERIOD]  ,
	[AMOUNT_TYPE_CD]
from "dbo"."S_GC_FUNDS_MANAGEMENT_ITEM"
WHERE AMOUNT_TYPE_CD = '0100'
ORDER BY 	[REF_DOC_NBR]  ,
	[REF_DOC_ITEM_NBR]  ,
	[RFRNC_DOC_ACCNT_ASSGN_NBR]  ,
	[RFRNC_DOC_CLSSN_NBR]  ,
	[FISCAL_YR]  ,
	[FISCAL_PERIOD]  ,
	[AMOUNT_TYPE_CD]
```

```sql
-- Source query for OLEDB_SRC_ZZATT
SELECT "lifnr"   AS VENDOR_NBR,
       "ekorg"   AS PURCHASING_ORG_NBR,
       "erdat"   AS CREATED_DT,
       "ernam"   AS CREATED_BY_USER_ID,
       CASE
         WHEN "loevm" = 'X' THEN '1'
         ELSE "loevm"
       END       AS LOGICALLY_DELETED_IND,
       "ekgrp"   AS PURRCHSING_GROUP_CD,
       CASE
         WHEN "sperm" = 'X' THEN '1'
         ELSE"sperm"
       END       AS BLOCKING_IND,
       Getdate() AS UPDATE_DT,
       'FAS'     AS SOURCE_ID,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM   sap_source."dbo"."lfm1"
```

```sql
-- Source query for OLEDB_SRC_ZZADVJUST
SELECT T1."za_lifnr"
       + Space(10 - Len(T1."za_lifnr")) AS VENDOR_NBR,
       T1.za_lang                       AS DETAIL_LANGUAGE_CD,
       T1.za_off_lang                   AS OFFICIAL_LANGUAGE_CD,
       T1.za_name1                      AS VENDOR_OPERATING_NM_LINE_1,
       T1.za_name2                      AS VENDOR_OPERATING_NM_LINE_2,
       T1.za_acronym                    AS VENDOR_ACRONYM,
       T1.za_url                        AS INTERNET_ADDRESS_URL,
       T1."za_url_lang"                 AS URL_LANGUAGE_CD,
       T1.za_addr1                      AS MAILING_ADDRESS_LINE_1,
       T1.za_addr2                      AS MAILING_ADDRESS_LINE_2,
       T1.za_city                       AS MAILING_CITY_NM,
       T1.za_region_cd                  AS MAILING_REGION_CD,
       T1.za_postal_cd                  AS MAILING_POSTAL_CD,
       isnull(cast(T7.ALPHA_2_CD as varchar(3)), T1.za_cntry_cd) AS MAILING_COUNTRY_CD,
       T1.za_pa_addr1                   AS PHYSICAL_ADDRESS_LINE_1,
       T1.za_pa_addr2                   AS PHYSICAL_ADDRESS_LINE_2,
       T1.za_pa_city                    AS PHYSICAL_CITY_NM,
       T1.za_pa_region_cd               AS PHYSICAL_REGION_CD,
       T1.za_pa_postal_cd               AS PHYSICAL_POSTAL_CD,
       T1.za_pa_cntry_cd                AS PHYSICAL_COUNTRY_CD,
       T1.za_email                      AS EMAIL_ADDRESS_URL,
       T1.za_telphn                     AS MAIN_TELEPHONE_NBR,
       T1.za_fax                        AS MAIN_FAX_NBR,
       T1.za_create_dt                  AS CREATION_DT,
       T1.za_update_dt                  AS LAST_UPDATED_DT,
       T1.za_userid                     AS CREATED_BY_USER_ID,
       T1.za_search_term                AS SEARCH_TERM,
       Getdate()                        AS UPDATE_DT,
       'FAS'                            AS SOURCE_ID,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM   zastk T1
	   LEFT JOIN BI_Conformed.dbo.BI_COUNTRY_CD_UPDATE T7
			  ON  T7.OLD_ALPHA_2_CD = T1.za_cntry_cd Collate Latin1_General_CI_AI
```

```sql
-- SQL Query for OLEDB_SRC_S_GC_CONDITION_ITEM
SELECT  CONDITION_TYPE_CD,
     APPLICATION_CD FROM DBO.S_GC_CONDITION_TYPE
ORDER BY CONDITION_TYPE_CD,
     APPLICATION_CD
```

```sql
-- SQL Query for OLEDB_SRC_T685T
SELECT
     T1.KSCHL as CONDITION_TYPE_CD,
     T1.KAPPL as APPLICATION_CD,

CASE
      WHEN T1."VTEXT" is null  THEN 'UnCoded'
      ELSE T1."VTEXT"
END as EN_NM,

CASE
      WHEN T2."VTEXT" is null THEN 'Non-Codé'
      ELSE T2."VTEXT"
END as FR_NM,
getdate() as UPDATE_DT,
'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM T685T T1 Left Join T685T T2
on T1.KSCHL = T2.KSCHL
AND T1.KAPPL = T2.KAPPL
AND T2."SPRAS" = 'F'
WHERE T1.KAPPL IN ('M','TX')
AND T1."SPRAS"='E'
AND T2.KAPPL IN ('M','TX')
ORDER BY T1.KSCHL ,
     T1.KAPPL
```

```sql
-- SQL Update Statement for OLEDBCMD_TRFM-Update_S_GC_CONDITION_TYPE
UPDATE [dbo].[S_GC_CONDITION_TYPE]
   SET [EN_NM] = ?
      ,[FR_NM] = ?
      ,[UPDATE_DT] = ?
      ,[SOURCE_ID] = ?
      ,[ETL_UPDT_DT] = ?
 WHERE  [CONDITION_TYPE_CD] = ?
      and [APPLICATION_CD] = ?
```

```sql
--SQL Query for OLEDB_SRC_ESSR
SELECT
     LBLNI as ENTRY_SHEET_NBR,
     PACKNO as PACKAGE_NBR,
     EBELN as PO_DOCUMENT_NBR,
     EBELP as PO_LINE_ITEM_NBR,
   CASE
      WHEN LOEKZ = 'X' THEN 1
      ELSE 0
  END  AS LOGICALLY_DELETED_FLAG,
     ERNAM as CREATED_BY_USERID,
     ERDAT as CREATION_DT,
     AENAM as LAST_UPDATED_BY_USERID,
     AEDAT as LAST_UPDATE_DT,
getdate() as UPDATE_DT,
LBLNE as EXTERNAL_ENTRY_SHEET_NBR,
LBLDT as REFERENCE_DT,
LWERT as SERVICE_AMT,
'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM ESSR
"LBLNI"
ORDER BY  LBLNI
```

```sql
--SQL Update statement for OLEDBCMD_TRFM-Update_S_GC_ENTRY_SHEET
UPDATE [dbo].[S_GC_ENTRY_SHEET]
   SET [PACKAGE_NBR] = ?
      ,[PO_DOCUMENT_NBR] = ?
      ,[PO_LINE_ITEM_NBR] = ?
      ,[LOGICALLY_DELETED_FLAG] = ?
      ,[CREATED_BY_USERID] = ?
      ,[CREATION_DT] = ?
      ,[LAST_UPDATED_BY_USERID] = ?
      ,[LAST_UPDATE_DT] = ?
      ,[UPDATE_DT] = ?
      ,[EXTERNAL_ENTRY_SHEET_NBR] = ?
      ,[REFERENCE_DT] = ?
      ,[SERVICE_AMT] = ?
      ,[SOURCE_ID] = ?
      ,[ETL_UPDT_DT] = ?
 WHERE [ENTRY_SHEET_NBR] = ?
```

```sql
--SQL Query for OLEDB_SRC_S_GC_ENTRY_SHEET
SELECT ENTRY_SHEET_NBR FROM DBO.S_GC_ENTRY_SHEET
ORDER BY ENTRY_SHEET_NBR
```

```sql
--SQL Query for OLEDB_SRC_T163C
SELECT
     T1.KSCHL as CONDITION_TYPE_CD,
     T1.KAPPL as APPLICATION_CD,

CASE
      WHEN T1."VTEXT" is null  THEN 'UnCoded'
      ELSE T1."VTEXT"
END as EN_NM,

CASE
      WHEN T2."VTEXT" is null THEN 'Non-Codé'
      ELSE T2."VTEXT"
END as FR_NM,
getdate() as UPDATE_DT,
'FAS' as SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM T685T T1 Left Join T685T T2
on T1.KSCHL = T2.KSCHL
AND T1.KAPPL = T2.KAPPL
AND T2."SPRAS" = 'F'
WHERE T1.KAPPL IN ('M','TX')
AND T1."SPRAS"='E'
AND T2.KAPPL IN ('M','TX')
ORDER BY T1.KSCHL ,
     T1.KAPPL
```

```sql
--SQL Update Statement for OLEDBCMD_TRFM-Update_S_GC_HISTORY_CATEGORY
UPDATE [dbo].[S_GC_HISTORY_CATEGORY]
   SET [EN_CD] = ?
      ,[EN_NM] = ?
      ,[FR_CD] = ?
      ,[FR_NM] = ?
      ,[UPDATE_DT] = ?
      ,[SOURCE_ID] = ?
      ,[ETL_UPDT_DT] = ?
 WHERE  [HISTORY_CATEGORY_KEY] = ?
```

```sql
--SQL Query for OLEDB_SRC_S_GC_HISTORY_CATEGORY
SELECT HISTORY_CATEGORY_KEY FROM DBO.S_GC_HISTORY_CATEGORY
ORDER BY HISTORY_CATEGORY_KEY
```

```sql
--SQL for ESQL_Create_PK_S_GC_CONDITION_ITEM
IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM]') AND name = N'PK_S_GC_CONDITION_ITEM')
DROP INDEX [PK_S_GC_CONDITION_ITEM] ON [dbo].S_GC_CONDITION_ITEM WITH ( ONLINE = OFF );

CREATE UNIQUE CLUSTERED INDEX [PK_S_GC_CONDITION_ITEM] ON [dbo].[S_GC_CONDITION_ITEM]
(
[CONDITION_DOCUMENT_NBR] ASC,
[CONDITION_ITEM_NBR] ASC,
[STEP_NBR] ASC,
[CONDITION_COUNTER] ASC,
[SOURCE_ID] ASC
) ON [PRIMARY];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM_TMP]') AND type in (N'U'))
drop table dbo.[S_GC_CONDITION_ITEM_TMP];

IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM]') AND name = N'IDX_S_GC_CONDITION_ITEM')
DROP INDEX [IDX_S_GC_CONDITION_ITEM] ON [dbo].S_GC_CONDITION_ITEM WITH ( ONLINE = OFF );

CREATE UNIQUE NONCLUSTERED INDEX [IDX_S_GC_CONDITION_ITEM] ON [dbo].[S_GC_CONDITION_ITEM]
(
[STEP_NBR] ASC,
[CONDITION_COUNTER] ASC,
[PO_DOCUMENT_NBR] ASC,
[GCS_PO_DOCUMENT_NBR] ASC,
[PO_LINE_ITEM_NBR] ASC,
[CONDITION_TYPE_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
```

```sql
--SQL for ESQL_Ctreat_S_GC_CONDITION_ITEM_TMP
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM_TMP]') AND type in (N'U'))
DROP TABLE [dbo].[S_GC_CONDITION_ITEM_TMP]

select * into [dbo].[S_GC_CONDITION_ITEM_TMP]
FROM [dbo].[S_GC_CONDITION_ITEM];

IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM_TMP]') AND name = N'IDX_S_GC_CONDITION_ITEM')
DROP INDEX [IDX_S_GC_CONDITION_ITEM_TMP] ON [dbo].[S_GC_CONDITION_ITEM_TMP] WITH ( ONLINE = OFF );

CREATE UNIQUE NONCLUSTERED INDEX [IDX_S_GC_CONDITION_ITEM_TMP] ON [dbo].[S_GC_CONDITION_ITEM_TMP]
(
[STEP_NBR] ASC,
[CONDITION_COUNTER] ASC,
[PO_DOCUMENT_NBR] ASC,
[GCS_PO_DOCUMENT_NBR] ASC,
[PO_LINE_ITEM_NBR] ASC,
[CONDITION_TYPE_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];

GO
```

```sql
--SQL FOR ESQL_Drop_PK_S_GC_CONDITION_ITEM
IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_CONDITION_ITEM]') AND name = N'PK_S_GC_CONDITION_ITEM')
DROP INDEX [PK_S_GC_CONDITION_ITEM] ON [dbo].S_GC_CONDITION_ITEM WITH ( ONLINE = OFF );
```

```sql
--SQL for Add_Index_S_GC_PAYMENT 1
IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_PAYMENT]') AND name = N'ix6S_GC_PAYMENT')

DROP INDEX [ix6S_GC_PAYMENT] ON [dbo].[S_GC_PAYMENT]
GO
IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[S_GC_PAYMENT]') AND name = N'ix5S_GC_PAYMENT')
DROP INDEX [ix5S_GC_PAYMENT] ON [dbo].[S_GC_PAYMENT]
GO

IF  EXISTS (SELECT * FROM sys.