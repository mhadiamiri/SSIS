## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| TRADE_REPORTING           | OLE DB          | Server: [Inferred], Database: TRADE_REPORTING  | Lookup data and destination | SQL Server Auth likely | Various SqlCommandParam references input column lineage ID            | Part 1, 2, 3                  |
| TRADE_STAGING           | OLE DB          | Server: [Inferred], Database: TRADE_STAGING  | Source for fact tables             | SQL Server Auth likely            |  None                  | Part 1, 2, 3                 |
| {EAD46801-DF7E-4A66-8392-A332378304A0} | OLE DB          | Server: [Inferred]  | Data source/destination, Truncate table, select statements | SQL Server Auth likely | ErrorDescription for error logging | Part 1, 3 |
| {FF0865AB-8993-4DEC-A8B5-2E067FE20155} | OLE DB          | Server: [Inferred]  | OLE DB runtime connection             | SQL Server Auth likely            |  None                  | Part 1, 3|

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| SEQC-F_TRADE_FINANCIALS_SP14|  [Inferred] | Parent | Executes after ESQLT- F_TRADE_FINANCIALS is successful.  |  | Part 2|
| SEQC-F_TRADE_FUNDING_SP11| [Inferred] | Parent | Executes after ESQLT- Truncate F_TRADE_FUNDING is successful.  |  | Part 2|
| SEQC-F_TRADE_HR_SP14| [Inferred] | Parent| Executes after ESQLT- F_TRADE_HR is successful. |  | Part 2|
| SEQC-F_TRADE_ISSUES_SP13| [Inferred] | Parent| Executes after ESQLT- F_TRADE_ISSUES is successful. |  | Part 2|
| SEQC-F_TRADE_LISTS_SP13| [Inferred] | Parent| Executes after ESQLT- F_TRADE_LISTS is successful. |  | Part 2|
| SEQC-F_TRADE_OPPORTUNITY_REFERRAL_SP13| [Inferred] | Parent| Executes after ESQLT- F_TRADE_OPPORTUNITY_REFERRAL is successful. |  | Part 2|
| SEQC-F_TRADE_OPPORTUNITY_SP9| [Inferred] | Parent| Executes after ESQLT- Truncate F_TRADE_OPPORTUNITY is successful. |  | Part 2|
| SEQC-F_TRADE_ORG_MARKETS_INTEREST_SP13| [Inferred] | Parent| Executes after ESQLT- F_TRADE_ORG_MARKETS_INTEREST is successful. |  | Part 2|
| SEQC-F_TRADE_ORG_SPC_CHAR_SP13| [Inferred] | Parent| Executes after ESQLT- F_TRADE_ORG_SPC_CHAR is successful. |  | Part 2|
| SEQC-F_TRADE_OUTCALL_SP11| [Inferred] | Parent| Executes after ESQLT- Truncate F_TRADE_OUTCALL is successful. |  | Part 2|
| SEQC-F_TRADE_SERVICE_CREATED_SP12| [Inferred] | Parent| Executes after ESQLT- F_TRADE_SERVICE_CREATED is successful. |  | Part 2|

## 3. Package Flow Analysis

#### DFT- F_TRADE_FINANCIALS

*   **Source:** `OLEDB_SRC-S_TRADE_FINANCIALS` reads data from the `S_TRADE_FINANCIALS` staging table.
*   **Transformations:**
    *   `LKPT-D_TRADE_FIN_DATE`: Lookup Transformation using `D_TRADE_FIN_DATE` dimension table.
    *   `LKPT-D_TRADE_POST_HIERARCHY`: Lookup Transformation using `D_TRADE_POST_HIERARCHY` dimension table.
    *   `UNIONALL_TRFM_LKP_NO_MATCH`: Union All transformation to combine unmatched rows from the lookups.
    *   `DRV_TRFM-REJECT_MASTER_TABLE`: Derived Column transformation to create `REASON`
*   **Destinations:**
    *   `OLEDB_DEST-F_TRADE_FINANCIALS`:  Writes successfully transformed data to the `dbo.F_TRADE_FINANCIALS` fact table.
    *   `OLEDB_DEST-REJECT_TRADE_MASTER`: Writes rejected data (due to lookup failures) to the `dbo.REJECT_TRADE_MASTER` table.

#### DFT- F_TRADE_FUNDING

*   **Source:** `OLEDB_SRC-F_TRADE_FUNDING` reads data from the `dbo.S_TRADE_FUNDING_VIEW` staging view.
*   **Transformations:**
    *   `Data Conversion`: Converts `ACTIVITY_SUBTYPE_LU` from `wstr` to `str`
    *   `LKP_D_TRADE_FUNDING`: Lookup transformation using the `dbo.D_TRADE_FUNDING` dimension table
    *   `LKP-D_TRADE_SECTOR`: Lookup transformation using the `dbo.D_TRADE_SECTOR` dimension table
    *   `LKP-D_TRADE_STATUS`: Lookup transformation using the `dbo.D_TRADE_STATUS` dimension table
    *   `LKP-D_TRADE_POST_HIERARCHY`: Lookup transformation using the `dbo.D_TRADE_POST_HIERARCHY` dimension table
    *   `LKP-D_TRADE_ORGANIZATION`: Lookup transformation using the `dbo.D_TRADE_ORGANIZATION` dimension table
    *   `LKP-D_TRADE_FIN_DATE`: Lookup transformation using the `dbo.D_TRADE_FIN_DATE` dimension table
    *   `LKP-D_TRADE_ACTIVITY_SUBTYPE`: Lookup transformation using the `dbo.D_TRADE_ACTIVITY_SUBTYPE` dimension table
    *   `UNIONALL_TRFM-LKP_NO_MATCH`: Union All transformation to combine unmatched rows from the lookups
    *   `DRV_TRFM-D_TRADE_ORGANIZATION`: Derived Column to create `REASON` column
    *   `DRV_TRFM-D_TRADE_POST_HIERARCHY`: Derived Column to create `REASON` column
    *   `DRV_TRFM-D_TRADE_STATUS`: Derived Column to create `REASON` column
    *   `DRV_TRFM-D_TRADE_SECTOR`: Derived Column to create `REASON` column
    *   `DRV_TRFM-D_TRADE_FIN_DATE`: Derived Column to create `REASON` column
    *   `DRV_TRFM-D_TRADE_ACTIVITY_SUBTYPE`: Derived Column to create `REASON` column
    *   `DRV_TRFM-F_TRADE_FUNDING`: Derived Column to create `ETL_CREA_DT1` and `ETL_UPDT_DT1` columns
    *   `DRV_TRFM-REJECT_TRADE_MASTER`: Derived Column to create `ETL_CREA_DT1`, `ETL_UPDT_DT1`, and `FACT_TABLE_NAME` columns
    *   `DCONV_TRFM-REJECT_TRADE_MASTER`: Data Conversion to convert columns to `str` for writing to REJECT_TRADE_MASTER table
*   **Destinations:**
    *   `OLEDB_DEST-F_TRADE_FUNDING`:  Writes successfully transformed data to the `dbo.F_TRADE_FUNDING` fact table.
    *   `OLEDB_DEST-REJECT_TRADE_MASTER`: Writes rejected data (due to lookup failures) to the `dbo.REJECT_TRADE_MASTER` table.

#### DFT- F_TRADE_SERVICE_CREATED

*   **Source:** `OLEDB SRC-S_W_TRADE_SERVICE_VIEW_CREATED` - OLE DB Source reading from a view `dbo.S_W_TRADE_SERVICE_VIEW_CREATED`
*   **Data Flow (Partial):**
    *   Data flows from the OLE DB source to a series of `Lookup` transformations (e.g., `LKP-D_TRADE_FIN_DATE`, `LKP-D_TRADE_ORGANIZATION`, `LKP-D_TRADE_SECTOR`, etc.).
    *   Rows that *do not match* in the Lookup transformations are sent to `Derived Column` transformations (e.g., `DRV_TRFM-D_TRADE_FIN_DATE1`, `DRV_TRFM-D_TRADE_SECTOR1`, etc.) to create "REASON" codes indicating why the lookup failed. These are then combined with the main flow using a `UNIONALL_TRFM_LKP_NO_MATCH` component
    *   The main flow (from the `Lookup Match Output` path) goes through conversion transformations (`DCONV_TRFM-ACTIVITY_SUBTYPE`, `DCONV_TRFM-DT_String`)\
    *   The converted data is loaded into the destination `OLEDB_Dest-F_TRADE_SERVICE_CREATED`
    *   Error rows (REJECT_TRADE_MASTER) are derived and converted before being written to another destination.
*   **Transformations:**
    *   **Lookup Transformations:** Used extensively to enrich the data with dimension information (e.g., joining `DATE_LU` to `D_TRADE_FIN_DATE` to get the `DATE_SID`). The `NoMatchBehavior` is set to "Send rows with no matching entries to the no match output."
    *   **Derived Column Transformations:** Used to create new columns (most notably `REASON` codes) based on the outcome of the Lookup transformations.
    *   **Data Conversion Transformations:** Used to convert data types (e.g., string to date).
    *   **Union All Transformations:** Used to combine data streams, specifically to re-integrate rows that did not match in the Lookup transformations.

## 4. Code Extraction

```sql
-- From OLEDB_SRC-F_TRADE_FINANCIALS in DFT- F_TRADE_FINANCIALS
SELECT
       coalesce(ORG_ID,'-3') as ORG_ID_LU
      ,coalesce(cast(FISCAL_DT as varchar),'-3') as FISCAL_DT_LU
      ,coalesce(CREATED_BY_POST,'-3') as CREATED_BY_POST_LU
      ,1 as FINANCIALS_COUNT
FROM dbo.S_TRADE_FINANCIALS_VIEW

-- From LKP-D_TRADE_FIN_DATE in DFT- F_TRADE_FINANCIALS
SELECT case when DATE_SID < 0 THEN '-3'
       else CONVERT(VARCHAR(10),"MONTH_END_DT",121) end AS INPUT_CD,
       DATE_SID AS OUTPUT_SID
FROM   dbo.D_TRADE_FIN_DATE
WHERE FISCAL_QUARTER IS NOT NULL

-- From LKP-D_TRADE_POST_HIERARCHY in DFT- F_TRADE_FINANCIALS
SELECT	case when "POST_SID"=-3 then '-3'
        else "POST_CD" end as POST_CD,
	    "POST_SID" as POST_SID
FROM   "dbo"."D_TRADE_POST_HIERARCHY"
ORDER BY 2

-- From ESQLT- F_TRADE_FINANCIALS in SEQC-F_TRADE_FINANCIALS_SP14
TRUNCATE TABLE dbo.F_TRADE_FINANCIALS;

-- From OLEDB_SRC-F_TRADE_FUNDING in DFT- F_TRADE_FUNDING
SELECT distinct
       coalesce(FUNDING_NBR,'-3') as FUNDING_LU
      ,coalesce(TARGET_SECTOR,'-3') as TARGET_SECTOR_LU
      ,coalesce(UPPER(STATUS),'-3') as STATUS_LU
      ,coalesce(CREATED_BY_POST,'-3') as CREATED_BY_POST_LU
	  ,coalesce(ORG_ID,'-3') as ORG_ID_LU
	  ,coalesce(cast(FISCAL_DT as varchar),'-3') as FISCAL_DT_LU
,coalesce(FUNDING_TYPE,'-3') as ACTIVITY_SUBTYPE_LU
      ,1 as FUNDING_COUNT
FROM dbo.S_TRADE_FUNDING_VIEW

-- From LKP-D_TRADE_ACTIVITY_SUBTYPE in DFT- F_TRADE_FUNDING
SELECT	case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
        else "ACTIVITY_SUBTYPE_EN_NM" end as INPUT_CD,
	   "ACTIVITY_SUBTYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_ACTIVITY_SUBTYPE"

-- From LKP-D_TRADE_FIN_DATE in DFT- F_TRADE_FUNDING
SELECT case when DATE_SID < 0 THEN '-3'
       else CONVERT(VARCHAR(10),"MONTH_END_DT",121) end AS INPUT_CD,
       DATE_SID AS OUTPUT_SID
FROM   dbo.D_TRADE_FIN_DATE
WHERE FISCAL_QUARTER IS NOT NULL

-- From LKP-D_TRADE_ORGANIZATION in DFT- F_TRADE_FUNDING
SELECT	case when "ORG_SID"=-3 then '-3'
        else "ORG_ID" end as INPUT_CD,
	"ORG_SID" OUTPUT_SID
FROM   "dbo"."D_TRADE_ORGANIZATION"

-- From LKP-D_TRADE_POST_HIERARCHY in DFT- F_TRADE_FUNDING
SELECT	case when "POST_SID"=-3 then '-3'
        else "POST_CD" end as POST_CD,
	    "POST_SID" as POST_SID
FROM   "dbo"."D_TRADE_POST_HIERARCHY"
ORDER BY 2

-- From LKP-D_TRADE_SECTOR in DFT- F_TRADE_FUNDING
SELECT	case when "SECTOR_SID"=-3 then '-3'
        else "SECTOR_DESCR_EN" end as INPUT_CD,
	"SECTOR_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_SECTOR"

-- From LKP-D_TRADE_STATUS in DFT- F_TRADE_FUNDING
SELECT	case when "STATUS_TYPE_SID" = -3 then '-3'
        else UPPER("STATUS_TYPE_DESCR_EN") end as INPUT_CD,
	"STATUS_TYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_STATUS"

-- From LKP_D_TRADE_FUNDING in DFT- F_TRADE_FUNDING
SELECT	case when "FUNDING_SID"=-3 then '-3'
        else "FUNDING_NBR" end as INPUT_CD,
	   "FUNDING_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_FUNDING"

-- From ESQLT- Truncate F_TRADE_FUNDING in SEQC-F_TRADE_FUNDING_SP11
TRUNCATE TABLE dbo.F_TRADE_FUNDING;

-- From OLEDB_SRC-W1_TRADE_HR in DFT- F_TRADE_HR
SELECT distinct DATE_SID,
        FUND_CENTRE_SID,
       LOCATION_SID,
	"LOCATION_TXT_EN",
       ISNULL(POST_ID,0) as POST_ID,
	"POSITION_STREAM_SID",
	"MEMBER_TYPE_SID",
	"CLASS_SID",
	"FILLED_SID",
	"POSITION_SID",
       POSITION_NBR,
       NAME,
	"POSITION_TOTAL",
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM   "dbo"."W1_TRADE_HR" T1,
       "TRADE_REPORTING".dbo."D_TRADE_POST_HIERARCHY" T2
WHERE T1.LOCATION_TXT_EN = T2."PS_POST_EN"
AND POSITION_TOTAL >= 1
--and country_en = 'USA'
--and DATE_SID = 175
--and post_id in (321)
--and date_sid = 175
--and position_stream_sid = 175
order by 4

-- From ESQLT- F_TRADE_HR in SEQC-F_TRADE_HR_SP14
TRUNCATE TABLE dbo.F_TRADE_HR;

-- From OLEDB_SRC-F_TRADE_ISSUES in DFT- F_TRADE_ISSUES
select distinct
       coalesce(ISSUE_NBR,'-3') as ISSUE_LU
      ,coalesce(ALPHA_2_CD,'-3')  as TARGET_COUNTRY_LU
      ,coalesce(OFFICE,'-3')  as POST_LU
      ,coalesce(UPPER(STATUS),'-3') as STATUS_LU
      ,coalesce(cast(FISCAL_DT as varchar),'-3') as FISCAL_DT_LU
      ,coalesce("TYPE",'-3') as ACTIVITY_SUBTYPE_LU
      ,coalesce(CASE_NUMBER,'-3') as CASE_LU
      ,1 as ISSUE_COUNT
      ,getdate() as ETL_CREA_DT
      ,getdate() as ETL_UPDT_DT
from dbo.S_TRADE_ISSUES_VIEW

-- From ESQLT- F_TRADE_ISSUES in SEQC-F_TRADE_ISSUES_SP13
TRUNCATE TABLE dbo.F_TRADE_ISSUES;

-- From OLEDB_SRC-S_TRADE_ORG_LISTS_VIEW in
SELECT coalesce(ORG_ID,'-3') as ORG_ID_LU
       ,LIST_NBR
      ,LIST_NAME
      ,LIST_DESCR
      ,CREATED_BY_USER
      ,CREATED_BY_OFFICE
      ,CREATED_ON_DT
      ,UPDATED_ON_DT
      ,getdate() as ETL_CREA_DT
      ,getdate() as ETL_UPDT_DT
  FROM dbo.S_TRADE_ORG_LISTS_VIEW

-- From ESQLT- F_TRADE_LISTS in SEQC-F_TRADE_LISTS_SP13
TRUNCATE TABLE dbo.F_TRADE_LISTS;

-- From OLEDB_SRC-F_TRADE_OPPORTUNITY in DFT- F_TRADE_OPPORTUNITY
SELECT distinct

coalesce(OPPORTUNITY_NBR,'-3') as OPPORTUNITY_NBR_LU,
coalesce("CONTACT_ID",'-3') as CONTACT_ID_LU,
coalesce(ALPHA_2_CD,'-3') as ALPHA_2_CD_LU,
1 as OPPORTUNITY_COUNT,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT

FROM   "dbo"."S_TRADE_OPPORTUNITY_VIEW"

-- From ESQLT- Truncate F_TRADE_OPPORTUNITY in SEQC-F_TRADE_OPPORTUNITY_SP9
TRUNCATE TABLE dbo.F_TRADE_OPPORTUNITY;

-- From OLEDB_SRC-S_TRADE_ORG_MARKETS_INTERES in DFT- F_TRADE_ORG_MARKETS_INTEREST
SELECT distinct

coalesce(T1."ORG_ID", '-3') as ORG_ID_LU,
      T1."ORG_ID",
      "MARKET_INTEREST_EN",
      "MARKET_INTEREST_FR",
      coalesce("ALPHA_2_CD",'-3') as ALPHA_2_CD,
      "COUNTRY_EN",
      "COUNTRY_FR",
      "REGION_NAME_EN",
      "REGION_NAME_FR",
      getdate()  as  ETL_CREA_DT
	,getdate()  as  ETL_UPDT_DT

FROM   "dbo"."S_TRADE_ORG_MARKETS_INTEREST" T1

-- From ESQLT- F_TRADE_ORG_MARKETS_INTEREST in SEQC-F_TRADE_ORG_MARKETS_INTEREST_SP13
TRUNCATE TABLE dbo.F_TRADE_ORG_MARKETS_INTEREST;

-- From OLEDB_SRC-S_TRADE_ORG_SPC_CHAR in DFT- F_TRADE_ORG_SPC_CHAR
SELECT distinct

coalesce(T1."ORG_ID", '-3') as ORG_ID_LU,
T1."ORG_ID",
coalesce(ORG_SPECIAL_CHARACTERISTICS,'Uncoded') as ORG_SPC_CHAR,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT

FROM   "dbo"."S_TRADE_ORG_SPC_CHAR" T1

-- From ESQLT- F_TRADE_ORG_SPC_CHAR in SEQC-F_TRADE_ORG_SPC_CHAR_SP13
TRUNCATE TABLE dbo.F_TRADE_ORG_SPC_CHAR;

-- From OLEDB_SRC-S_TRADE_OUTCALL in DFT- F_TRADE_OUTCALL
SELECT distinct

OUTCALL_DT,
       coalesce(cast(convert(varchar(10),(CASE WHEN MONTH("OUTCALL_DT") > 3 THEN CONVERT(DATETIME, '3/31/' + CONVERT(VARCHAR(4), YEAR("OUTCALL_DT") + 1))
            ELSE CONVERT(DATETIME, '3/31/' + CONVERT(VARCHAR(4), YEAR("OUTCALL_DT")))\
       END),121) as varchar),'-3') as DATE_LU,
	case when ORG_LU = '-' then '-3' else
	coalesce("ORG_LU",'-3') end as ORG_LU,
	case when SECTOR_LU='-' then '-3' else
	coalesce("SECTOR_LU",'-3') end as SECTOR_LU,
    case when OBJECTIVE_LU = '-' then '-3' else
	coalesce("OBJECTIVE_LU",'-3') end as OBJECTIVE_LU,
	'-3' AS ACTIVITY_SUBTYPE_LU,
	case when STATUS_LU  = '-' then '-3' else
	coalesce(UPPER("STATUS_LU"),'-3') end as STATUS_LU,
	case when CONTACT_LU='-' then '-3' else
	coalesce("CONTACT_LU",'-3') end as CONTACT_LU,
	case when CREATED_BY_LU='-' then '-3' else
	coalesce("CREATED_BY_LU",'-3') end as CREATED_BY_LU,
	case when ASSIGNED_TO_LU='-' then '-3' else
	coalesce("ASSIGNED_TO_LU",'-3') end as ASSIGNED_TO_LU,
	case when POST_LU='-' then '-3' else
	coalesce("POST_LU",'-3') end as POST_LU,
	'-3' as "OUTCALL_NUMBER",
       1 as "OUTCALL_COUNT",
       '-3' as CASE_LU,
	'-3' as BUSINESS_LINE_LU
       ,'-3' as ALPHA_2_CD_LU
       ,'-3' as OUTCALL_NUMBER_LU
       ,null as CREATED_DT

FROM   "dbo"."W1_TRADE_OUTCALL_TRIO1"

union

SELECT DISTINCT  OUTCALL_DT
	,coalesce(cast(FISCAL_DT AS VARCHAR), '-3') AS DATE_LU
	,coalesce("ORG_ID", '-3') AS ORG_LU
	,coalesce("SECTOR_EN", '-3') AS SECTOR_LU
	,coalesce("OBJECTIVE", '-3') AS OBJECTIVE_LU
    ,coalesce(cast("OBJECTIVE" as varchar(100)), '-3') AS ACTIVITY_SUBTYPE_LU
	,UPPER(coalesce("STATUS", '-3')) AS STATUS_LU
	,coalesce("CONTACT_ID", '-3') AS CONTACT_LU
	,coalesce("OFFICER_CREATED_BY", '-3') AS CREATED_BY_LU
	,coalesce("ASSIGNED_TO", '-3') AS ASSIGNED_TO_LU
	,coalesce("ASSIGNED_OFFICE", '-3') AS POST_LU
	,OUTCALL_NUMBER
	,1 AS OUTCALL_COUNT
	,coalesce("CASE_NBR", '-3') AS CASE_LU
	,coalesce("BUSINESS_LINE", '-3' ) as BUSINESS_LINE_LU
       ,coalesce("ALPHA_2_CD", '-3' ) as ALPHA_2_CD_LU
       ,coalesce("OUTCALL_NUMBER", '-3' ) as OUTCALL_NUMBER_LU
	,substring(CAST("CREATED_DT" AS VARCHAR(10)), 1, 10) AS CREATED_DT


FROM "dbo"."S_TRADE_OUTCALL_VIEW"

-- From ESQLT- Truncate F_TRADE_OUTCALL in SEQC-F_TRADE_OUTCALL_SP11
TRUNCATE TABLE dbo.F_TRADE_OUTCALL;

-- From LKP-D_TRADE_ACTIVITY_SUBTYPE in DFT- F_TRADE_OUTCALL
SELECT	case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
        else "ACTIVITY_SUBTYPE_EN_NM" end as INPUT_CD,
	   "ACTIVITY_SUBTYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_ACTIVITY_SUBTYPE"

-- From LKP-D_TRADE_BUSINESS_LINE in DFT- F_TRADE_OUTCALL
SELECT	case when BL_SID=-3 then '-3'
       else "BL_DESCR_EN" end as INPUT_CD,
	"BL_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_BUSINESS_LINE"

-- From LKP-D_TRADE_CASE in DFT- F_TRADE_OUTCALL
SELECT	cast(case when "CASE_SID"=-3 then '-3'
        else "CASE_NBR" end as nvarchar(30)) as INPUT_CD,
	   "CASE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_CASE"

-- From LKP-D_TRADE_CONTACT in DFT- F_TRADE_OUTCALL
SELECT	case when CONTACT_SID = -3  then '-3'
        else "CONTACT_ID" end as INPUT_CD,
	"CONTACT_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_CONTACT"

-- From LKP-D_TRADE_COUNTRY in DFT- F_TRADE_OUTCALL
SELECT	case when COUNTRY_SID=-3 then '-3'
        else ALPHA_2_CD end as INPUT_CD,
	    "COUNTRY_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_COUNTRY"

-- From LKP-D_TRADE_FIN_DATE in DFT- F_TRADE_OUTCALL
SELECT case when DATE_SID < 0 THEN '-3'
       else CONVERT(VARCHAR(10),"MONTH_END_DT",121) end AS INPUT_CD,
       DATE_SID AS OUTPUT_SID

FROM   D_TRADE_FIN_DATE
WHERE FISCAL_QUARTER IS NOT NULL

-- From OLEDB_SRC-S_W_TRADE_SERVICE_VIEW_CREATED in DFT- F_TRADE_OUTCALL
SELECT
       substring(CAST("CREATED_DT" as varchar(10)),1,10) as CREATED_DT,
       substring(CAST(DELIVERED_DT as varchar(10)),1,10) as DELIVERED_DT,
       substring(CAST("REQUESTED_DT" as varchar(10)),1,10) as REQUESTED_DT,
       substring(CAST("FOLLOW_UP_DT" as varchar(10)),1,10) as FOLLOW_UP_DT,
       substring(CAST("CONNECTION_DT" as varchar(10)),1,10) as CONNECTION_DT,
       coalesce(cast(FISCAL_DT as varchar),'-3') as DATE_LU,       coalesce("ORG_ID", '-3') as ORG_LU,
       coalesce("SECTOR_EN", '-3') as SECTOR_LU,
       coalesce(UPPER("SERVICE_TYPE"), '-3') as SERVICE_TYPE_LU,
	UPPER(coalesce("STATUS", '-3')) as STATUS_LU,
	coalesce("CONTACT_ID", '-3') as CONTACT_LU,
	coalesce("BUSINESS_LINE", '-3') as BL_LU,
	coalesce("OFFICER_CREATED_BY", '-3') as CREATED_BY_LU,
       coalesce("ASSIGNED_TO_LOGIN", '-3')  as ASSIGNED_TO_LU,
	coalesce("ASSIGNED_OFFICE", '-3') as POST_LU,
	coalesce("CASE_NBR", '-3') as CASE_LU,
       coalesce("SERVICE_NBR",'-3') as SERVICE_LU,
       coalesce("ALPHA_2_CD",'-3') as ALPHA_2_CD_LU,
       coalesce("SERVICE_TYPE", '-3') as ACTIVITY_SUBTYPE_LU,
       COUNT(DISTINCT "SERVICE_NBR") as SERVICE_COUNT,
       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT
FROM   "dbo"."S_TRADE_SERVICE_VIEW_CREATED"
GROUP BY
	substring(CAST("CREATED_DT" as varchar(10)),1,10),\
       substring(CAST(DELIVERED_DT as varchar(10)),1,10) ,\
       substring(CAST("REQUESTED_DT" as varchar(10)),1,10) ,\
       substring(CAST("FOLLOW_UP_DT" as varchar(10)),1,10),\
       substring(CAST("CONNECTION_DT" as varchar(10)),1,10) ,\
       FISCAL_DT ,\
       coalesce("ORG_ID", '-3') ,\
       coalesce("SECTOR_EN", '-3'),\
       coalesce(UPPER("SERVICE_TYPE"), '-3') ,\
	UPPER(coalesce("STATUS", '-3')) ,\
	coalesce("CONTACT_ID", '-3') ,\
	coalesce("BUSINESS_LINE", '-3'),\
	coalesce("OFFICER_CREATED_BY", '-3') ,\
       coalesce("ASSIGNED_TO_LOGIN", '-3'),\
	coalesce("ASSIGNED_OFFICE", '-3'),\
	coalesce("CASE_NBR", '-3'),\
       coalesce("SERVICE_NBR",'-3'),\
       coalesce("ALPHA_2_CD",'-3'),\
       coalesce("SERVICE_TYPE", '-3')
union all
SELECT	"CREATED_DT",
       substring(CAST(DELIVERED_DT as varchar(10)),1,10) as DELIVERED_DT,\
	"REQUESTED_DT",\
	"FOLLOW_UP_DT",\
	"CONNECTION_DT",
       coalesce(cast(convert(varchar(10),(CASE WHEN MONTH(DELIVERED_DT) > 3 THEN CONVERT(DATETIME, '3/31/' + CONVERT(VARCHAR(4), YEAR("DELIVERED_DT") + 1))\
            ELSE CONVERT(DATETIME, '3/31/' + CONVERT(VARCHAR(4), YEAR("DELIVERED_DT")))\
       END),121) as varchar),'-3') as DATE_LU,\tcase when ORG_LU='-' then '-3' else\
	coalesce("ORG_LU",'-3') end as ORG_LU,\
	case when SECTOR_LU='-' then '-3' else\
	coalesce("SECTOR_LU",'-3') end as SECTOR_LU,\
	case when SERVICE_TYPE_LU='-' then '-3' else\
	coalesce(UPPER("SERVICE_TYPE_LU"),'-3') end as SERVICE_TYPE_LU,\
	case when STATUS_LU='-' then '-3' else\
	coalesce(UPPER("STATUS_LU"),'-3') end as STATUS_LU,\
	case when CONTACT_LU='-' then '-3' else\
	coalesce("CONTACT_LU",'-3') end as CONTACT_LU,\
	case when BL_LU='-' then '-3' else\
	coalesce("BL_LU",'-3') end as BL_LU,\
	case when CREATED_BY_LU='-' then '-3' else\
	coalesce("CREATED_BY_LU",'-3') end as CREATED_BY_LU,\
	case when ASSIGNED_TO_LU='-' then '-3' else\
	coalesce("ASSIGNED_TO_LU",'-3') end as ASSIGNED_TO_LU,\
	case when POST_LU='-' then '-3' else\
	coalesce("POST_LU",'-3') end as POST_LU,\
       '-3' as CASE_LU,\
	case when SERVICE_LU='-' then '-3' else\
	coalesce("SERVICE_LU",'-3') end as SERVICE_LU,\
       '-3' as "ALPHA_2_CD_LU",\
       '-3' as ACTIVITY_SUBTYPE_LU,\
	"SERVICE_COUNT",\
       getdate() as ETL_CREA_DT,\
       getdate() as ETL_UPDT_DT\
FROM   "dbo"."W1_TRADE_SERVICE_TRIO1"

-- From ESQLT- F_TRADE_SERVICE_CREATED in SEQC-F_TRADE_SERVICE_CREATED_SP12
TRUNCATE TABLE dbo.F_TRADE_SERVICE_CREATED;

-- From LKP-D_TRADE_ACTIVITY_SUBTYPE in DFT- F_TRADE_SERVICE_CREATED
SELECT	case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
        else "ACTIVITY_SUBTYPE_EN_NM" end as INPUTC_D,
	   "ACTIVITY_SUBTYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_ACTIVITY_SUBTYPE"

-- From LKP-D_TRADE_BUSINESS_LINE in DFT- F_TRADE_SERVICE_CREATED
SELECT	case when BL_SID=-3 then '-3'
       else "BL_DESCR_EN" end as INPUT_CD,
	"BL_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_BUSINESS_LINE"

-- From LKP-D_TRADE_CASE in DFT- F_TRADE_SERVICE_CREATED
select * from (SELECT	case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
        else "ACTIVITY_SUBTYPE_EN_NM" end as INPUT_CD,