## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| TRADE_LANDING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for multiple data flows             | Credentials to write to `TRADE_LANDING` database | None Visible          | Part 1, 2, 3                  |
| TRIO_SOURCE         | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for multiple data flows             | Credentials to read from `TRIO_SOURCE` database   | None Visible          | Part 1, 2                 |
| WCMS_TCS | OLE DB | Server: [Inferred], Database: [Inferred] | Source for extracting data from view `vwSurveyResultAnswer_BI` and `vwSurveyResult_BI`. | Requires credentials to access the WCMS_TCS database. | None apparent from provided XML. | Part 2 |
| Strategia_IPRS_BI | OLE DB | Server: [Inferred], Database: [Inferred] | Source for extracting data from tables | Requires credentials to access the Strategia_IPRS_BI database. | None apparent from provided XML. | Part 2, 3 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package `TRADE_LANDING` has sequence containers executed sequentially.
*   Data flow tasks follow a pattern of extracting data from source views/tables and loading it into landing tables.
*   Several Data Conversion components are used to convert columns to different data types.
*   Error handling is often set to `FailComponent`, causing the entire task to fail upon any error.
*   Truncate statements are used to empty destination tables before loading data.

#### DFT- L-DFAIT\_CASE\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_CASE_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_CASE_VIEW`.

#### DFT- L-DFAIT\_CONTACT\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_CONTACT_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_CONTACT_VIEW`.

#### DFT- L-DFAIT\_LOV\_BUSINESS\_LINE (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_BUSINESS_LINE`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_BUSINESS_LINE`.

#### DFT- L-DFAIT\_LOV\_COUNTRY (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_COUNTRY`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_COUNTRY`.

#### DFT- L-DFAIT\_LOV\_OBJECTIVE (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_OBJECTIVE`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_OBJECTIVE`.

#### DFT- L-DFAIT\_LOV\_SECTOR (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_SECTOR`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_SECTOR`.

#### DFT- L-DFAIT\_LOV\_SERVICE\_STATUS (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_SERVICE_STATUS`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_SERVICE_STATUS`.

#### DFT- L-DFAIT\_LOV\_SERVICE\_TYPE (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_LOV_SERVICE_TYPE`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_LOV_SERVICE_TYPE`.

#### DFT- L-DFAIT\_FUNDING\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_FUNDING_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_FUNDING_VIEW`, converts the status column to a non-unicode format.

#### DFT- L-DFAIT\_ISSUES\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ISSUES_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ISSUES_VIEW`.

#### DFT- L-DFAIT\_OPPORTUNITY\_REFERRAL\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_OPPORTUNITY_REFERRAL_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_OPPORTUNITY_REFERRAL_VIEW`.

#### DFT- L-DFAIT\_OPPORTUNITY\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_OPPORTUNITY_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_OPPORTUNITY_VIEW`, converts the `OPPORTUNITY_DESCR` and `BUSINESS_LINE_TXT` columns to a non-unicode format.

#### DFT- L-DFAIT\_ORG\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ORG_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ORG_VIEW`, converts the `PROFILE` column to a non-unicode format.

#### DFT- L-DFAIT\_REFERRALS\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_REFERRALS_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_REFERRALS_VIEW`, converts the `ORIGINATING_OFFICER_LOGIN` column to a non-unicode format.

#### DFT- L-DFAIT\_SUCCESSES\_VIEW\_No\_Unused (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_SUCCESSES_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_SUCCESSES_VIEW`, converts the `SUBSIDIARY_NAME_TXT`, `LINKED_FUNDING_NBR`, `SUCCESS_NBR`, `RETURN_DESCR_TXT` columns to a non-unicode format, and truncates the `DETAILS_TXT` column.

#### DFT- L-DFAIT\_FDI\_PROJECTS\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_FDI_PROJECTS_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_FDI_PROJECTS_VIEW`.

#### DFT- L-DFAIT\_SERVICE\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_SERVICE_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_SERVICE_VIEW`.

#### DFT- L-DFAIT\_EMPLOYEE\_VIEW (Part 1)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_EMPLOYEE_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_EMPLOYEE_VIEW`, converts the `RESPONSIBILITY`, `DIVISION`, `USER_ID` columns to a non-unicode format.

#### DFT- L-DFAIT\_ORG\_LISTS\_VIEW (Part 1, 2)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ORG_LISTS_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ORG_LISTS_VIEW`, converts the `ORG_ID` column to a non-unicode format.

#### DFT- L-DFAIT\_ORG\_MARKETS\_INTEREST (Part 1, 2)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ORG_MARKETS_INTEREST`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ORG_MARKETS_INTEREST`, converts the `MARKETS_INTEREST_REGION` column to a non-unicode format.

#### DFT- L-DFAIT\_ORG\_SPC\_CHAR\_VIEW (Part 2)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ORG_SPC_CHAR_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ORG_SPC_CHAR_VIEW`.

#### DFT- L-DFAIT\_ORG\_REL\_VIEW (Part 2)

*   **Source:** Extracts data from `TRIO_SOURCE.dbo.DFAIT_ORG_REL_VIEW`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.DFAIT_ORG_REL_VIEW`.

#### DFT- L-WCMS\_vwSurveyResult\_BI (Part 2)

*   **Source:** Extracts data from `WCMS_TCS.dbo.vwSurveyResult_BI`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.WCMS_vwSurveyResult_BI`.

#### DFT- L-WCMS\_vwSurveyResultAnswer\_BI (Part 2)

*   **Source:** Extracts data from `WCMS_TCS.dbo.vwSurveyResultAnswer_BI`.
*   **Transformation:** Converts the `Value` column to `Value_Unicode`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.WCMS_vwSurveyResultAnswer_BI`.

#### DFT- L-FundedPosition (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundedPosition`.
*   **Transformation:** Converts the `PrioritySector` column to `Priority_Sector_ind`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundedPosition`.

#### DFT- L-MissionVersion (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.MissionVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.MissionVersion`.

#### DFT- L-MissionVersionFiscalYear (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.MissionVersionFiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.MissionVersionFiscalYear`.

#### DFT- L-MissionVersionFiscalYearProgram (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.MissionVersionFiscalYearProgram`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.MissionVersionFiscalYearProgram`.

#### DFT- L-ProgramPlan (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.ProgramPlan`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.ProgramPlan`.

#### DFT- L-Resource (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.Resource`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.Resource`.

#### DFT- L-ActionPlan (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.ActionPlan`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.ActionPlan`.

#### DFT- L-BaseFundingSourceType (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.BaseFundingSourceType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.BaseFundingSourceType`.

#### DFT- L-FiscalYear (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FiscalYear`.

#### DFT- L-FundingRequest (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundingRequest`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundingRequest`.

#### DFT- L-FundingSourceType (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundingSourceType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundingSourceType`.

#### DFT- L-FundingSourceVersion (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundingSourceVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundingSourceVersion`.

#### DFT- L-FundingSourceVersionFiscalYear (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundingSourceVersionFiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundingSourceVersionFiscalYear`.

#### DFT- L-Initiative (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.Initiative`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.Initiative`.

#### DFT- L-PartnerVersion (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PartnerVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PartnerVersion`.

#### DFT- L-SectorFunctionVersion (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.SectorFunctionVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.SectorFunctionVersion`.

#### DFT- L-CompletionStatus (Part 2, 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.CompletionStatus`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.CompletionStatus`.

#### DFT- L-Country (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.Country`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.Country`.

#### DFT- L-FundedPositionType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundedPositionType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundedPositionType`.

#### DFT- L-FundingSource (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.FundingSource`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.FundingSource`.

#### DFT- L-InitiativeLocation (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.InitiativeLocation`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.InitiativeLocation`.

#### DFT- L-InitiativePerformanceIndicator (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.InitiativePerformanceIndicator`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.InitiativePerformanceIndicator`.

#### DFT- L-InitiativeType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.InitiativeType`.
*   **Transformation:** Transforms the boolean column `IsFieldTypeOther` into an integer column  `IsFieldTypeOther_int`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.InitiativeType`.

#### DFT- L-MultiMissionType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.MultiMissionType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.MultiMissionType`.

#### DFT- L-PerformanceIndicator (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PerformanceIndicator`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PerformanceIndicator`.

#### DFT- L-PlanStatus (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PlanStatus`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PlanStatus`.

#### DFT- L-Position (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.Position`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.Position`.

#### DFT- L-PositionType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PositionType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PositionType`.

#### DFT- L-PositionVersion (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PositionVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PositionVersion`.

#### DFT- L-PositionVersionFiscalYear (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.PositionVersionFiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.PositionVersionFiscalYear`.

#### DFT- L-ProgramTemplate (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.ProgramTemplate`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.ProgramTemplate`.

#### DFT- L-Question (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.Question`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.Question`.

#### DFT- L-QuestionAnswer (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.QuestionAnswer`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.QuestionAnswer`.

#### DFT- L-QuestionType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.QuestionType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.QuestionType`.

#### DFT- L-QuestionValue (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.QuestionValue`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.QuestionValue`.

#### DFT- L-RegionVersion (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.RegionVersion`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.RegionVersion`.

#### DFT- L-RegionVersionFiscalYear (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.RegionVersionFiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.RegionVersionFiscalYear`.

#### DFT- L-SectorFunctionType (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.SectorFunctionType`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.SectorFunctionType`.

#### DFT- L-SectorFunctionVersionFiscalYear (Part 3)

*   **Source:** Extracts data from `Strategia_IPRS_BI.dbo.SectorFunctionVersionFiscalYear`.
*   **Destination:** Loads data into `TRADE_LANDING.dbo.SectorFunctionVersionFiscalYear`.

## 4. Code Extraction

```sql
-- Source query for DFT- L-DFAIT_CASE_VIEW
SELECT	"Case #" as CASE_NBR,
	"Case Name" as CASE_NAME_EN,
	"Description" as CASE_DESCR,
	"Status" as STATUS,
	"Business Line" as BUSINESS_LINE,
	"Owner Office" as OWNER_OFFICE,
	"Owner" as OWNER,
	"Created On" as CREATED_ON_DT,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM   "dbo"."DFAIT_CASE_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_CONTACT_VIEW
SELECT	distinct "Contact Id" as CONTACT_ID,
	"Contact First Name" as CONTACT_FIRST_NAME,
	"Contact Last Name" as CONTACT_LAST_NAME,
	"Contact Phone" as CONTACT_PHONE,
	"Contact Email" as CONTACT_EMAIL,
	"Org Id" as ORG_ID,
	"Exclusive Rep" as EXCLUSIVE_REP,
    "TRIO 1 ROW_ID" as TRIO1_ROW_ID,
    "Primary" as PRIMARY_CONTACT,
    "Created On Date" as CREATED_ON_DT,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM   "dbo"."DFAIT_CONTACT_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_LOV_BUSINESS_LINE
SELECT	"LIC" as LIC,
	"Value" as VALUE,
	"Parent LIC" as PARENT_LIC,
	"Order" as ORDER_ID,
	"LANG_ID" as LANG_ID,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM   "dbo"."DFAIT_LOV_BUSINESS_LINE"
```

```sql
-- Source query for DFT- L-DFAIT_LOV_COUNTRY
SELECT	"LIC" as LIC,
	"Value" as VALUE,
	"Parent LIC" as PARENT_LIC,
	"Order" as ORDER_ID,
	"LANG_ID" as LANG_ID,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM   "dbo"."DFAIT_LOV_COUNTRY"
```

```sql
-- Source query for DFT- L-DFAIT_LOV_OBJECTIVE
SELECT	"LIC" as LIC,
	"Value" as VALUE,
	"Parent LIC" as PARENT_LIC,
	"Order" as ORDER_ID,
	"LANG_ID" as LANG_ID,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM   "dbo"."DFAIT_LOV_OBJECTIVE"
```

```sql
-- Source query for DFT- L-DFAIT_LOV_SECTOR
SELECT	"LIC" as LIC,
	"Value" as VALUE,
	"Parent LIC" as PARENT_LIC,
	"Order" as ORDER_ID,
	"LANG_ID" as LANG_ID,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM  "dbo"."DFAIT_LOV_SECTOR"
```

```sql
-- Source query for DFT- L-DFAIT_LOV_SERVICE_STATUS
SELECT	"LIC" as LIC,
	"Value" as VALUE,
	"Parent LIC" as PARENT_LIC,
	"Order" as ORDER_ID,
	"LANG_ID" as LANG_ID,
	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT
FROM  "dbo"."DFAIT_LOV_SERVICE_STATUS"
```

```sql
-- Source query for DFT- L-DFAIT_FUNDING_VIEW
SELECT [Funding Number] as FUNDING_NBR
      ,[Funding Type] as FUNDING_TYPE
      ,[Target Country] as TARGET_COUNTRY
      ,[Target Sector] as TARGET_SECTOR
      ,[Status] as STATUS
      ,[Approved on Date] as APPROVED_ON_DT
      ,[Created by Office] as CREATED_BY_OFFICE
      ,[Agreement to Share Info] as AGREEMENT_TO_SHARE_INFO_IND
      ,[Summary] as SUMMARY_TXT
      ,[Created On Date] as CREATED_ON_DT
      ,[Org ID] as ORG_ID
	  ,getdate() as ETL_CREA_DT
	  ,getdate() as ETL_UPDT_DT
FROM [dbo].[DFAIT_FUNDING_VIEW]
```

```sql
-- Source query for DFT- L-DFAIT_ISSUES_VIEW
SELECT
"Issue #" as  "ISSUE_NBR",
"Country" as  "COUNTRY",
"Office" as  "OFFICE",
"Officer" as  "OFFICER",
"Policy Area" as  "POLICY_AREA",
"Type" as  "TYPE",
"Status" as  "STATUS",
"Title" as  "TITLE",
"Description of Issue" as  "DESCRIPTION_OF_ISSUE",
cast("Created On" as datetime) as CREATED_DT,
"Case #" as CASE_NUMBER,
getdate()  as  ETL_CREA_DT,
getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_ISSUES_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_OPPORTUNITY_REFERRAL_VIEW
SELECT	"Opportunity #" as OPPORTUNITY_NBR,
	"Opp Ref Created On" AS OPP_REF_CREATED_ON_DT,
    "Referred Date" AS REFERRED_DT,
	"Canadian Org" AS CANADIAN_ORG,
	"First Name" AS FRIST_NAME,
	"Last Name" AS LAST_NAME,
	"Referred By" AS REFERRED_BY,
	"Referred By Office" AS REFERRED_BY_POST,
	"Opportunity Referral #" AS OPPOURTINTY_REFERRAL_NBR,
	"Opp Ref Target Sector" AS OPP_REF_TARGET_SECTOR,
	"Opp Ref Status" AS OPP_REF_STATUS,
	"Business Line" as BUSINESS_LINE_TXT,
	"Case #" as CASE_NBR,
    "Org_ID" as ORG_ID,
    "Referred by Satellite"  as  REFERRED_BY_SATELLITE,
    "Contact ID"  as  CONTACT_ID,
	getdate()  as  ETL_CREA_DT,
	getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_OPPORTUNITY_REFERRAL_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_OPPORTUNITY_VIEW
SELECT	"Opportunity #" AS OPPORTUNITY_NBR,
	"Status" AS STATUS,
	"Local Organization" AS LOCAL_ORGANIZATION,
	"Local Contact" AS LOCAL_CONTACT,
	"Created On" AS CREATED_ON_DT,
	"Target Sector" AS TARGET_SECTOR,
	"Target Country" AS TARGET_COUNTRY,
	"Owner" AS OWNER,
	"Owner Office" AS OWNER_POST,
	"Sent to BON" AS SENT_TO_BON_DT,
	"BON Officer" AS BON_OFFICER,
	"Completed By BON" AS COMPLETED_BY_BON,
	"Case #" as CASE_NBR,
	"X_FDI_FLG" as X_FDI_FLAG,
	"FDI Project Title" as FDI_PROJECT_TITLE,
	"FDI Project Type" as FDI_PROJECT_TYPE_TXT,
	"Business Line" as BUSINESS_LINE_TXT,
    "Owner Satellite"  as  OWNER_SATELLITE,
    "Local Organization ID"  as  LOCAL_ORGANIZATION_ID,
    "Local Contact ID"  as  LOCAL_CONTACT_ID,
    cast("Description of Opportunity" as varchar(max)) as  OPPORTUNITY_DESCR,
    "Request HQ Assistance"  as  REQUEST_HQ_ASSISTANCE_IND,
	getdate()  as  ETL_CREA_DT,
	getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_OPPORTUNITY_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_REFERRALS_VIEW
SELECT	"Org Id" as ORG_ID,
    "TRIO 1 Org Id" as TRIO1_ORG_ID,
	"Organization Name" as ORG_NAME,
	"Service #" as SERVICE_NBR,
	"Service Type" as SERVICE_TYPE,
	"Assigned Office" as ASSIGNED_OFFICE,
	"Assigned To Last Name" as ASSIGNED_TO_LAST_NAME,
	"Assigned To First Name" as ASSIGNED_TO_FIRST_NAME,
    "SR Sector"  as SECTOR,
    "SR Sub Sector"  as SUB_SECTOR,
	"Org Sector" as ORG_SECTOR,
	"Org Sub Sector" as ORG_SUB_SECTOR,
	"Created Date" as CREATED_DT,
	"Delivered Date" as DELIVERED_DT,
	"Requested Date" as REQUESTED_DT,
	"Business Line" as BUSINESS_LINE,
	"Status" as STATUS,
	"Originating Officer Last Name" as ORIGINATING_OFFICER_LAST_NAME,
	"Originating Officer First Name" as ORIGINATING_OFFICER_FIRST_NAME,
    "Originating Officer Login" as ORIGINATING_OFFICER_LOGIN,
	"Originating Office" as ORIGINATING_OFFICE,
	"Connection Date" as CONNECTION_DT,
	"Follow-up" as FOLLOW_UP,
	"Follow-up Date" as FOLLOW_UP_DT,
	"Contact Id" as CONTACT_ID,
	"Contact Phone" as CONTACT_PHONE_NBR,
	"Contact Email" as CONTACT_EMAIL,
	getdate()  as  ETL_CREA_DT,
	getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_REFERRALS_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_SUCCESSES_VIEW_No_Unused
SELECT	"Success #" AS SUCCESS_NBR,
	"Linked Service #" AS LINKED_SERVICE_NBR,
	"Linked Opty Ref #" AS LINKED_OPTY_REF_NBR,
	"Type" AS TYPE_TXT,
	"Status" AS STATUS_TXT,
	"Organization" AS ORGANIZATION_TXT,
	"Business Line" AS BUSINESS_LINE_TXT,
	"Target Sector" AS TARGET_SECTOR_TXT,
	SUBSTRING("Details", 1, 4000) AS DETAILS_TXT,
	"Manager" AS MANAGER_NAME,
	"Owner" AS OWNER,
	"Owner Office" AS OWNER_POST,
	"Created On" AS CREATED_ON_DT,
	'' AS PARTICIPANT_NAME,
	"Participant Office" AS PARTICIPANT_POST,
	"Validated On" AS VALIDATED_ON_DT,
	"Return Reason" AS RETURN_REASON_TXT,
	"Return Description" AS RETURN_DESCR_TXT,
	"Linked FDI Project" as LINKED_FDI_PROJECT,
	"FDI Project Type" as FDI_PROJECT_TYPE_TXT,
	"FDI Project Title" as FDI_PROJECT_TITLE,
	"Value ($)" as VALUE_AMT,
	"# of Jobs" as NBR_JOBS,
	'DEPRECATED' as SUBSIDIARY_NAME_TXT,
	"Province" as PROVINCE_TXT,
	"City" as CITY_TXT,
	"Case #" as CASE_NBR,
    "Org ID" as ORG_ID,
    "Target Country" as TARGET_COUNTRY,
    "Linked Funding #" as LINKED_FUNDING_NBR,
    "Issue Number" as ISSUE_NUMBER,
    "Visit Date" as VISIT_DATE,
	getdate()  as  ETL_CREA_DT,
	getdate()  as  ETL_UPDT_DT
FROM   "dbo"."DFAIT_SUCCESS_VIEW"
```

```sql
-- Source query for DFT- L-DFAIT_FDI_PROJECTS_VIEW
SELECT [FDI Project #] as FDI_PROJECT_NUM
  	,[FDI Project Title] as FDI_PROJECT_TITLE
  	,[FDI Project Type] as FDI_PROJECT_TYPE
 	,[Status] as STATUS
  	,[Organization] as ORGANIZATION
  	,[Owner] as OWNER
  	,[Owner Office] as OWNER_OFFICE
  	,[Created On] as CREATED_ON
  	,[Closed Reason] as CLOSED_REASON
  	,[Target Sector] as TARGET_SECTOR
  	,[Target Country] as TARGET_COUNTRY
  	,[Value ($)] as VALUE
  	,[Number Of Jobs] as NUMBER_OF_JOBS
  	,[Est Start Date] as EST_START_DATE
  	,[Owner Satellite] as OWNER_SATELLITE
  	,[Org ID] as ORG_ID
	,getdate()  as  ETL_CREA_DT
    ,getdate()  as  ETL_UPDT_DT
FROM [dbo].[DFAIT_FDI_PROJECTS_VIEW]
```

```sql
-- Source query for DFT- L-DFAIT_SERVICE_VIEW
SELECT	"Org Id" as ORG_ID,
    "TRIO 1 Org Id" as TRIO1_ORG_ID,
	"Organization Name" as ORG_NAME,
	"Service #" as SERVICE_NBR,
	"Service Type" as SERVICE_TYPE,
	"Assigned Office" as ASSIGNED_OFFICE,
	"Assigned To Last Name" as ASSIGNED_TO_LAST_NAME,
	"Assigned To First Name" as ASSIGNED_TO_FIRST_NAME,
	"Assigned To Login" as ASSIGNED_TO_LOGIN,
    "SR Sector"  as SECTOR,