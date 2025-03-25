## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| COSMOS_STAGING_SSIS | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for staging tables | SQL Server Auth likely | None        | Part 1, 2, 3                  |
| BI_Conformed           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for lookup data and dimension tables | SQL Server Auth likely | None            | Part 1, 2, 3                  |
| COSMOS_LANDING_SSIS           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for landing tables             | SQL Server Auth likely            |  None                  | Part 1, 2, 3                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `COSMOS_Staging` is designed to load staging tables from various sources, likely as part of a larger ETL process. The primary flow is as follows:

*   Sets the `V_SQL_INSERT_ON_PRE_EXECUTE` variable to 'Running'.
*   Sets the `V_SQL_UPDATE_ON_POST_EXECUTE` variable to 'Succeeded'.
*   Sets the `V_SQL_UPDATE_ON_ERROR` variable to 'Failed'.

*   **EXPRESSIONT- Stage - Start Task**

    *   An Expression Task that evaluates the expression `1 == 1`.

*   **SEQC- Load Staging Tables 1**:

    *   Sequence Container designed to load staging tables. Contains the following data flows:

        #### DFT- S_CO_CASE_CATEGORY

        *   **Source:** `OLEDB_SRC-L_CO_CASE_CATEGORY` extracts data from the view `dbo.L_CO_CASE_CATEGORY` on the `BI_Conformed` connection.
        *   **Destination:** `OLEDB_DEST-S_CO_CASE_CATEGORY` loads data into the table `dbo.S_CO_CASE_CATEGORY` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_CASE_NOTE

        *   **Source:** `OLEDB_SRC_v_tCaseNote` extracts data from the view `dbo.v_tCaseNote` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tCaseNoteType`
        *   **Destination:** `OLEDB_DEST_S_CO_CASE_NOTE` loads data into the table `dbo.S_CO_CASE_NOTE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_CITIZENSHIP_SERVICE

        *   **Source:** `OLEDB_SRC_v_tCitizenshipService` extracts data from the view `dbo.v_tCitizenshipService` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tCitizenshipServiceType`.
        *   **Destination:** `OLEDB_DEST_S_CO_CITIZENSHIP_SERVICE` loads data into the table `dbo.S_CO_CITIZENSHIP_SERVICE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_CLIENT

        *   **Source:** `OLEDB_SRC_v_tClient` extracts data from the view `dbo.v_tClient` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tLanguage`, `dbo.v_tGender`, `dbo.v_tMaritalStatus`, `dbo.v_tCanadaStatus`, `dbo.v_tForeignCountryStatus`, `dbo.v_tOccupation`, and `dbo.v_tClientDocumentationType`
        *   **Transformations**:

        *   `LKP-L_CO_CASE_CATEGORY`: Lookup with join to `BI_Conformed` to `dbo.L_CO_CASE_CATEGORY`
        *   `DRVCOL_TRFM-Replace_Null_Value`: Derived column to handle null values.
        *   **Destination:** `OLEDB_DEST_S_CO_CLIENT` loads data into the table `dbo.S_CO_CLIENT` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_COMMON_CODE_TABLE

        *   **Source:** `OLEDB_SRC_R_COMMON_CODE_TABLE` extracts data from the table `dbo.R_COMMON_CODE_TABLE` on the `BI_Conformed` connection.
        *   **Destination:** `OLEDB_DEST_S_CO_COMMON_CODE_TABLE` loads data into the table `dbo.S_CO_COMMON_CODE_TABLE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_COUNTRY

        *   **Source:** `OLEDB_SRC_v_tCountry` extracts data from the view `dbo.v_tCountry` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tGeographicRegion` and `dbo.v_tcurrency`.
        *   **Destination:** `OLEDB_DEST_S_CO_COUNTRY` loads data into the table `dbo.S_CO_COUNTRY` using the `COSMOS_STAGING_SSIS` connection.

        #### SEQC_CASES-To-CASE_CLIENT
        *   Sequence Container designed to load staging tables. Contains the following data flows:
            *   **DFT_S_CO_CASES**:
                    *   **Source:** `OLEDB_SRC_v_tCase` extracts data from the view `dbo.v_tCase` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tCaseStatus` and `dbo.v_tSubNationalUnit`.
                    *   **Destination:** `OLEDB_DEST_S_CO_CASES` loads data into the table `dbo.S_CO_CASES` using the `COSMOS_STAGING_SSIS` connection.
            *   **DFT_S_CO_CASE_CLIENT**:
                    *   **Source:** `OLEDB_SRC_S_CO_CASES`: `S_CO_CASES`
                    *   **Source** `OLEDB_SRC_S_CO_CLIENT`: `dbo.S_CO_CLIENT`
                    *   **Destination:** `OLEDB_DEST_S_CO_CASE_CLIENT` loads data into the table `dbo.S_CO_CASE_CLIENT` using the `COSMOS_STAGING_SSIS` connection.

    *   **ESQLT- Truncate Staging Tables**:

        *   Truncates the following staging tables:
            *   `dbo.S_CO_CASE_CATEGORY`
            *   `dbo.S_CO_CASE_NOTE`
            *   `dbo.S_CO_CASES`
            *   `dbo.S_CO_CITIZENSHIP_SERVICE`
            *   `dbo.S_CO_CLIENT`
            *   `dbo.S_CO_COMMON_CODE_TABLE`
            *   `dbo.S_CO_COUNTRY`
            *   `dbo.S_CO_CASE_CLIENT`

*   **SEQC- Load Staging Tables 2**:

    *   Sequence Container designed to load staging tables. Contains the following data flows:

        #### DFT_S_CO_DATE

        *   **Source 1:** `OLEDB_SRC_DATE_DIM` extracts data from the table `dbo.DATE_DIM` on the `BI_Conformed` connection
        *   **Source 2:** `OLEDB_SRC_S_CO_DATE+20 Year` extracts data from the table `dbo.DATE_DIM` on the `BI_Conformed` connection, and adds 20 years to the date.
        *   **Transformations**:
            *   `DCONV_TRFM_String`: Derived column to handle null values.
            *   `UNIONALL_TRFM`: Combines data from the 2 sources.
            *   `DCONV_TRFM_Unicode`: Converts to unicode for `WEEK_DAY_FR` and `FISCAL_YEAR_NM`.

        *   **Destination:** `OLEDB_DEST_S_CO_DATE` loads data into the table `dbo.S_CO_DATE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_EMPLOYEE

        *   **Source:** `OLEDB_SRC_v_tEmployee` extracts data from the view `dbo.v_tEmployee` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tEmployeeCategory`.
        *   **Destination:** `OLEDB_DEST_S_CO_EMPLOYEE` loads data into the table `dbo.S_CO_EMPLOYEE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_GEOGRAPHIC_COORDINATES

        *   **Source:** `OLEDB_SRC_R_GEOGRAPHIC_COORDINATES` extracts data from the table `dbo.R_GEOGRAPHIC_COORDINATES` on the `BI_Conformed` connection.
        *   **Destination:** `OLEDB_DEST_S_CO_GEOGRAPHIC_COORDINATES` loads data into the table `dbo.S_CO_GEOGRAPHIC_COORDINATES` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_IBM_SUPPORTED_COUNTRY

        *   **Source:** `OLEDB_SRC_R_IBM_SUPPORTED_COUNTRY` extracts data from the table `dbo.R_IBM_SUPPORTED_COUNTRY` on the `BI_Conformed` connection.
        *   **Destination:** `OLEDB_DEST_S_CO_IBM_SUPPORTED_COUNTRY` loads data into the table `dbo.S_CO_IBM_SUPPORTED_COUNTRY` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_IMMIGRATION_SERVICE

        *   **Source:** `OLEDB_SRC_v_tImmigrationService` extracts data from the view `dbo.v_tImmigrationService` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tImmigrationServiceType` and `dbo.v_tYesNo`.
        *   **Destination:** `OLEDB_DEST_S_CO_IMMIGRATION_SERVICE` loads data into the table `dbo.S_CO_IMMIGRATION_SERVICE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_MISSION

        *   **Source:** `OLEDB_SRC_v_tMission` extracts data from the view `dbo.v_tMission` on the `COSMOS_LANDING_SSIS` connection, joining to `dbo.v_tMissionType`.
        *   **Destination:** `OLEDB_DEST_S_CO_MISSION` loads data into the table `dbo.S_CO_MISSION` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_PASSPORT_SERVICE

        *   **Source:** `OLEDB_SRC_v_tPassportService` extracts data from the view `dbo.v_tPassportService` on the `COSMOS_LANDING_SSIS` connection, joining multiple tables.
        *   **Transformations**:
            *   `DCONV_TRFM_DataType`: Data Conversion of SERVICE_FEE_EN_NM and SERVICE_FEE_FR_NM.
        *   **Destination:** `OLEDB_DEST_S_CO_PASSPORT_SERVICE` loads data into the table `dbo.S_CO_PASSPORT_SERVICE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_PASSPORT_SERVICE_ARCHIVE

        *   **Source:** `OLEDB_SRC_S_CO_PASSPORT_SERVICE_ARCHIVE` extracts data from the table `dbo.S_CO_PASSPORT_SERVICE_ARCHIVE` on the `COSMOS_LANDING_SSIS` connection.
        *   **Transformations**:
            *   `DCONV_TRFM-DataType`: Data Conversion of SERVICE_FEE_EN_NM and SERVICE_FEE_FR_NM.
        *   **Destination:** `OLEDB_DEST_S_CO_PASSPORT_SERVICE_ARCHIVE` loads data into the table `dbo.S_CO_PASSPORT_SERVICE_ARCHIVE` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_PPT_COMBINED_STATUS

        *   **Source:** `OLEDB_SRC_v_JPC_TS_CombinedStatus` extracts data from the view `dbo.v_JPC_TS_CombinedStatus` on the `COSMOS_LANDING_SSIS` connection.
        *   **Destination:** `OLEDB_DEST_S_CO_PPT_COMBINED_STATUS` loads data into the table `dbo.S_CO_PPT_COMBINED_STATUS` using the `COSMOS_STAGING_SSIS` connection.

        #### DFT_S_CO_PPT_WORKFLOW_STATUS

        *   **Source:** `OLEDB_SRC_v_tPassportService` extracts data from the view `dbo.v_tPassportService` on the `COSMOS_LANDING_SSIS` connection.
        *   **Destination:** `OLEDB_DEST_S_CO_PPT_WORKFLOW_STATUS` loads data into the table `dbo.S_CO_PPT_WORKFLOW_STATUS` using the `COSMOS_STAGING_SSIS` connection.

    *   **ESQLT- Truncate Staging Tables**:

        *   Truncates the following staging tables:

            *   `dbo.S_CO_DATE`
            *   `dbo.S_CO_EMPLOYEE`
            *   `dbo.S_CO_GEOGRAPHIC_COORDINATES`
            *   `dbo.S_CO_IBM_SUPPORTED_COUNTRY`
            *   `dbo.S_CO_IMMIGRATION_SERVICE`
            *   `dbo.S_CO_MISSION`
            *   `dbo.S_CO_PASSPORT_SERVICE`
            *   `dbo.S_CO_PASSPORT_SERVICE_ARCHIVE`
            *   `dbo.S_CO_PPT_COMBINED_STATUS`
            *   `dbo.S_CO_PPT_WORKFLOW_STATUS`

## 4. Code Extraction

```sql
SELECT     "TypeCode" AS TYPE_CAT_CD
	,"TypeNameE" AS TYPE_CAT_EN_NM
	,cast("TypeNameF" as nvarchar(50)) AS TYPE_CAT_FR_NM
	,"SubGroupCode" AS SUBGROUP_CAT_CD
	,"SubGroupNameE" AS SUBGROUP_CAT_EN_NM
	,cast("SubGroupNameF" as nvarchar(50)) AS SUBGROUP_CAT_FR_NM
	,"ServiceStandardGroupCode" AS SERVICE_STANDARD_GRP_CD
	,"ServiceStandardGroupE" AS SERVICE_STANDARD_GRP_EN_NM
	,cast("ServiceStandardGroupF" as nvarchar(50)) AS SERVICE_STANDARD_GRP_FR_NM
	,"CaseCategoryCode" AS CASE_CATEGORY_CD
	,"CaseCategoryNameE" AS CASE_CATEGORY_EN_NM
	,"CaseCategoryNameF" AS CASE_CATEGORY_FR_NM
	,"ComipCategoryCode" AS COMIP_CATEGORY_CD
	,"TimeStandardNew" AS TIME_STANDARD_NEW
	,"TimeStandardOngoing" AS TIME_STANDARD_ONGOING
	,"IsCurrent" AS IS_CURRENT_IND
	,"ComipCategoryCodePostCutoff" AS COMIPCATEGORY_POSTCUTOFF
	,getdate() AS ROW_INSERT_DTM
	,getdate() AS [ETL_CREA_DT]
	,getdate() AS [ETL_UPDT_DT]
FROM dbo.L_CO_CASE_CATEGORY
```

Context: SQL query for OLEDB_SRC-L_CO_CASE_CATEGORY in DFT- S_CO_CASE_CATEGORY

```sql
SELECT "CaseCode" AS CASE_CD
	,"SequenceNum" AS SEQUNCE_NBR
	,"FileNumber" AS FILE_NBR
	,"EmployeeCode" AS EMPLOYEE_CD
	,"EntryDate" AS ENTRY_DTM
	,"Subject" AS SUBJECT_DESCR
	,CASE 
		WHEN T1.NoteType IS NULL
			THEN - 3
		ELSE "NoteType"
		END AS NOTE_TYPE_CD
	,CASE 
		WHEN T2.Code IS NULL
			THEN 'Uncoded'
		ELSE "LabelE"
		END AS NOTE_TYPE_EN_NM
	,CASE 
		WHEN T2.Code IS NULL
			THEN 'Non codé'
		ELSE "LabelF"
		END AS NOTE_TYPE_FR_NM
	,getdate() AS ROW_INSERT_DTM
	,getdate() AS [ETL_CREA_DT]
	,getdate() AS [ETL_UPDT_DT]
FR 

Context: SQL query for OLEDB_SRC_v_tCaseNote in DFT_S_CO_CASE_NOTE

```sql
SELECT T1.PersonCode AS PERSON_CD
      ,T1.ApplicationDate AS APPLICATION_DTM

      ,CASE
      when T2.CitizenshipServTypeCode IS NULL then -3
      else T1.CitizenshipServTypeCode
	  END as CITIZENSHIP_SERV_TYPE_CD

	  ,CASE
      when T2.CitizenshipServTypeCode IS NULL then 'Uncoded'
      else T2.CitizenshipServTypeNameE
      END as CITIZENSHIP_SERV_TYPE_EN_NM

      ,CASE
      when T2.CitizenshipServTypeCode IS NULL then 'Non codé'
      else T2.CitizenshipServTypeNameF
      END as CITIZENSHIP_SERV_TYPE_FR_NM


      ,T1.ToProcessingDate AS TO_PROCESSING_DTM
      ,T1.FromProcessingDate AS FROM_PROCESSING_DTM
	  ,DATEDIFF(DD,T1.ApplicationDate,T1.ToProcessingDate)+1 AS PROCESSING_DAYS

      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT],
	   getdate() as [ETL_UPDT_DT]
FROM dbo.v_tCitizenshipService T1

left join dbo.v_tCitizenshipServiceType T2
on T1.CitizenshipServTypeCode=T2.CitizenshipServTypeCode
```

Context: SQL query for OLEDB_SRC_v_tCitizenshipService in DFT_S_CO_CITIZENSHIP_SERVICE

```sql
SELECT
T1."PersonCode" as CLIENT_CD,
T1."CaseCode" as CASE_CD,
T1."Birthdate" as BIRTHDATE_DTM,
CASE
    when T1."BirthCountryCode"  IS NULL then -3
    else T1."BirthCountryCode"
END as BIRTH_COUNTRY_CD,
CASE
    when T1."CitizenshipCode" IS NULL then -3
    else T1."CitizenshipCode"
END as CITIZENSHIP_CD,
CASE
    when T1."OtherCitizenshipCode" IS NULL then -3
    else T1."OtherCitizenshipCode"
END as OTHER_CITIZENSHIP_CD,

CASE
    when T2."LanguageCode" IS NULL then -3
    else T1."LanguageCode"
END as LANGUAGE_CD,

CASE
    when T2."LanguageCode" IS NULL then 'Uncoded'
    else T2."LanguageNameE"
END as LANGUAGE_EN_NM,

CASE
    when T2."LanguageCode" IS NULL then 'Non codé'
    else T2."LanguageNameF"
END as LANGUAGE_FR_NM,


CASE
    when T2."ISOCode" IS NULL then -3
    else T2."ISOCode"
END as ISO_CD,

CASE
    when T2."ISOLabel" IS NULL then 'Uncoded'
    else T2."ISOLabel"
END as ISO_LABEL_NM,


CASE
    when T3."GenderCode" IS NULL then -3
    else T1."GenderCode"
END as GENDER_CD,

CASE
    when T3."GenderCode" IS NULL then 'Uncoded'
    else T3."GenderNameE"
END as GENDER_EN_NM,

CASE
    when T3."GenderCode" IS NULL then 'Non codé'
    else T3."GenderNameF"
END as GENDER_FR_NM,

CASE
    when T4."MaritalStatusCode" IS NULL then -3
    else T1."MaritalStatusCode"
END as MARITAL_STATUS_CD,

CASE
    when T4."MaritalStatusCode" IS NULL then 'Uncoded'
    else T4."MaritalStatusNameE"
END as MARITAL_STATUS_EN_NM,

CASE
    when T4."MaritalStatusCode" IS NULL then 'Non codé'
    else T4."MaritalStatusNameF"
END as MARITAL_STATUS_FR_NM,

CASE
    when T5."StatusInCanadaCode" IS NULL then -3
    else T1."StatusInCanadaCode"
END as STATUS_IN_CANADA_CD,

CASE
    when T5."StatusInCanadaCode" IS NULL then 'Uncoded'
    else T5."StatusInCanadaNameE"
END as STATUS_IN_CANADA_EN_NM,

CASE
    when T5."StatusInCanadaCode" IS NULL then 'Non codé'
    else T5."StatusInCanadaNameF"
END as STATUS_IN_CANADA_FR_NM,

CASE
    when T6."StatusInCountryCode" IS NULL then -3
    else T1."StatusInCountryCode"
END as STATUS_IN_COUNTRY_CD,

CASE
    when T6."StatusInCountryCode" IS NULL then 'Uncoded'
    else T6."StatusInCountryNameE"
END as STATUS_IN_COUNTRY_EN_NM,

CASE
    when T6."StatusInCountryCode" IS NULL then 'Non codé'
    else T6."StatusInCountryNameF"
END as STATUS_IN_COUNTRY_FR_NM,

T1."CanDepartureDate" as CANADA_DEPARTURE_DTM,
T1."CurrentAddress" as CLIENT_CURRENT_ADDRESS_DESCR,
T1."PermanentAddress" as CLIENT_PERMANENT_ADDRESS_DESCR,
T1."MailAddress" as CLIENT_MAILING_ADDRESS_DESCR,

CASE
    when T7."OccupationCode" IS NULL then -3
    else T1."OccupationCode"
END as OCCUPATION_CD,

CASE
    when T7."OccupationCode" IS NULL then 'Uncoded'
    else T7."OccupationNameE"
END as OCCUPATION_EN_NM,

CASE
    when T7."OccupationCode" IS NULL then 'Non codé'
    else T7."OccupationNameF"
END as OCCUPATION_FR_NM,

T1."EmployerName" as EMPLOYER_NM,
T1."WorkPhone" as WORK_PHONE_NBR,
coalesce (cast(T1."ClientServiceTypeCode" as int), -3) as CLIENT_SERVICE_TYPE_CD,

/*
CASE
    when T8."CaseCategoryCode" IS NULL then -3
    else T1."ClientServiceTypeCode"
END as CLIENT_SERVICE_TYPE_CD,

CASE
    when T8."CaseCategoryCode" IS NULL then 'Uncoded'
    else T8."CaseCategoryNameE"
END as CLIENT_SERVICE_TYPE_EN_NM,

CASE
    when T8."CaseCategoryCode" IS NULL then 'Non codé'
    else T8."CaseCategoryNameF"
END as CLIENT_SERVICE_TYPE_FR_NM,
*/



CASE
    when T9."CaseRelationCode" IS NULL then -3
    else T1."CaseRelationCode"
END as CASE_RELATION_CD,

CASE
    when T9."CaseRelationCode" IS NULL then 'Uncoded'
    else T9."CaseRelationNameE"
END as CASE_RELATION_EN_NM,

CASE
    when T9."CaseRelationCode" IS NULL then 'Non codé'
    else T9."CaseRelationNameF"
END as CASE_RELATION_FR_NM,

CASE
    when T10."ClientDocTypeCode" IS NULL then -3
    else T1."DocTypeCode"
END as CLIENT_DOC_TYPE_CD,

CASE
    when T10."ClientDocTypeCode" IS NULL then 'Uncoded'
    else T10."ClientDocTypeNameE"
END as CLIENT_DOC_TYPE_EN_NM,

CASE
    when T10."ClientDocTypeCode" IS NULL then 'Non codé'
    else T10."ClientDocTypeNameF"
END as CLIENT_DOC_TYPE_FR_NM,

T1."DocIssueDate" as DOC_ISSUE_DTM,
T1."DocExpiryDate" as DOC_EXPIRY_DTM,
T1."DocCity" as DOC_ISSUING_CITY_NM,

coalesce(T1."DocCountryCode",-3) as DOC_ISSUING_COUNTRY_CD,  --- link to Country

coalesce(T1."CustodyCode",-3) AS CUSTODY_CD,  --- relates to what table


getdate() as ROW_INSERT_DTM
,getdate() as [ETL_CREA_DT],
getdate() as [ETL_UPDT_DT]

FROM "dbo"."v_tClient" T1

left join "dbo"."v_tLanguage" T2
on T1."LanguageCode" = T2."LanguageCode"

left join "dbo"."v_tGender" T3
on T1."GenderCode" = T3."GenderCode"

left join "dbo"."v_tMaritalStatus" T4
on T1."MaritalStatusCode" = T4."MaritalStatusCode"

left join "dbo"."v_tCanadaStatus" T5
on T1."StatusInCanadaCode" = T5."StatusInCanadaCode"

left join "dbo"."v_tForeignCountryStatus" T6
on T1."StatusInCountryCode" = T6."StatusInCountryCode"

left join "dbo"."v_tOccupation" T7
on T1."OccupationCode" = T7."OccupationCode"

--left join "BI_Conformed"."dbo"."L_CO_CASE_CATEGORY" T8
--on T1."ClientServiceTypeCode" = T8."CaseCategoryCode"

left join "dbo"."v_tCaseRelation" T9
on T1."CaseRelationCode" = T9."CaseRelationCode"

left join "dbo"."v_tClientDocumentationType" T10
on T1."DocTypeCode" = T10."ClientDocTypeCode"
```

Context: SQL query for OLEDB_SRC_v_tClient in DFT_S_CO_CLIENT

```sql
SELECT KEY_CD
      ,KEY_TYPE_NM
      ,NM_CD
      ,EN_NM
      ,FR_NM
      ,VALUE_NBR
      ,SOURCE_ID
      ,getdate() as ROW_INSERT_DTM
      ,getdate() as [ETL_CREA_DT],
       getdate() as [ETL_UPDT_DT]
  FROM dbo.R_COMMON_CODE_TABLE
```

Context: SQL query for OLEDB_SRC_R_COMMON_CODE_TABLE in DFT_S_CO_COMMON_CODE_TABLE

```sql
SELECT T1.PersonCode AS PERSON_CD
      ,T1.ApplicationDate AS APPLICATION_DTM

      ,CASE
      when T2.CitizenshipServTypeCode IS NULL then -3
      else T1.CitizenshipServTypeCode
	  END as CITIZENSHIP_SERV_TYPE_CD

	  ,CASE
      when T2.CitizenshipServTypeCode IS NULL then 'Uncoded'
      else T2.CitizenshipServTypeNameE
      END as CITIZENSHIP_SERV_TYPE_EN_NM

      ,CASE
      when T2.CitizenshipServTypeCode IS NULL then 'Non codé'
      else T2.CitizenshipServTypeNameF
      END as CITIZENSHIP_SERV_TYPE_FR_NM


      ,T1.ToProcessingDate AS TO_PROCESSING_DTM
      ,T1.FromProcessingDate AS FROM_PROCESSING_DTM
	  ,DATEDIFF(DD,T1.ApplicationDate,T1.ToProcessingDate)+1 AS PROCESSING_DAYS

      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT],
	   getdate() as [ETL_UPDT_DT]
FROM dbo.v_tCitizenshipService T1

left join dbo.v_tCitizenshipServiceType T2
on T1.CitizenshipServTypeCode=T2.CitizenshipServTypeCode
```

Context: SQL query for OLEDB_SRC_v_tCitizenshipService in DFT_S_CO_CITIZENSHIP_SERVICE

```sql
SELECT T1."CountryCode" as COUNTRY_CD
      ,T1."CountryNameE" as COUNTRY_EN_NM
      ,T1."CountryNameF" as COUNTRY_FR_NM
      ,T1."IsCurrentCountry" as CURRENT_COUNTRY_IND
      ,T1."GeoRegionCode" as GEOGRAPHIC_REGION_CD
      ,T2."GeoRegionNameE" as GEOGRAPHIC_REGION_EN_NM
      ,T2."GeoRegionNameF" as GEOGRAPHIC_REGION_FR_NM
      ,T1."RequiresTouristVisa" as REQUIRES_TOURIST_VISA_IND
      ,T1."RequiresBusinessVisa" as REQUIRES_BUSINESS_VISA_IND
      ,T1."RequiresStudentVisa" as REQUIRES_STUDENT_VISA_IND
      ,T1."VisaIssuingOffice" as VISA_ISSUING_OFFICE_CD
      ,CASE
          when T1."CurrencyCode" IS NULL then -3
          else T1."CurrencyCode"
      END as CURRENCY_CD

      ,CASE
          when T3."CurrencyCode" IS NULL then 'Uncoded'
          else T3."CurrencySymbol"
      END as CURRENCY_SYMBOL_DESCR

      ,T1."HagueDate" as HAGUE_DTM
      ,T1."IsHague" as HAGUE_IND
      ,T1."CountryAbbrev" as COUNTRY_ABBRV_DESCR
      ,T1."HagueNotes" as HAGUE_NOTES_DESCR
      ,T1."ConPlanMission" as CON_PLAN_MISSION_ID
      ,T1."TipDisplayNameE" as TIP_DISPLAY_EN_NM
      ,T1."TipDisplayNameF" as TIP_DISPLAY_FR_NM
      ,T1."IsLongCPTemplate" as LONG_CP_TEMPLATE_IND
      ,T1."IsConPlanBySNU" as CON_PLAN_BY_SNU_IND
      ,T1."AssignByPrimaryMission" as ASSIGN_BY_PRIMARY_MISSION_IND
      ,T1."AdvisorySiteName" as ADVISORY_SITE_NM

      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT],
	   getdate() as [ETL_UPDT_DT]
FROM dbo.v_tCountry T1

left join dbo.v_tGeographicRegion T2
on T1."GeoRegionCode" = T2."GeoRegionCode"

Left join "dbo"."v_tcurrency" T3
on T1."CurrencyCode" = T3."CurrencyCode"
```

Context: SQL query for OLEDB_SRC_v_tCountry in DFT_S_CO_COUNTRY

```sql
TRUNCATE TABLE   dbo.S_CO_CASE_CATEGORY;
TRUNCATE TABLE   dbo.S_CO_CASE_NOTE;
TRUNCATE TABLE   dbo.S_CO_CASES;
TRUNCATE TABLE   dbo.S_CO_CITIZENSHIP_SERVICE;
TRUNCATE TABLE   dbo.S_CO_CLIENT;
TRUNCATE TABLE   dbo.S_CO_COMMON_CODE_TABLE;
TRUNCATE TABLE   dbo.S_CO_COUNTRY;
TRUNCATE TABLE   dbo.S_CO_CASE_CLIENT;
```

Context: SQL query for ESQLT- Truncate Staging Tables in SEQC- Load Staging Tables 1

```sql
SELECT
T1."PersonCode" as CLIENT_CD,
T1."CaseCode" as CASE_CD,
T1."Birthdate" as BIRTHDATE_DTM,
CASE
    when T1."BirthCountryCode"  IS NULL then -3
    else T1."BirthCountryCode"
END as BIRTH_COUNTRY_CD,
CASE
    when T1."CitizenshipCode" IS NULL then -3
    else T1."CitizenshipCode"
END as CITIZENSHIP_CD,
CASE
    when T1."OtherCitizenshipCode" IS NULL then -3
    else T1."OtherCitizenshipCode"
END as OTHER_CITIZENSHIP_CD,

CASE
    when T2."LanguageCode" IS NULL then -3
    else T1."LanguageCode"
END as LANGUAGE_CD,

CASE
    when T2."LanguageCode" IS NULL then 'Uncoded'
    else T2."LanguageNameE"
END as LANGUAGE_EN_NM,

CASE
    when T2."LanguageCode" IS NULL then 'Non codé'
    else T2."LanguageNameF"
END as LANGUAGE_FR_NM,


CASE
    when T2."ISOCode" IS NULL then -3
    else T2."ISOCode"
END as ISO_CD,

CASE
    when T2."ISOLabel" IS NULL then 'Uncoded'
    else T2."ISOLabel"
END as ISO_LABEL_NM,


CASE
    when T3."GenderCode" IS NULL then -3
    else T1."GenderCode"
END as GENDER_CD,

CASE
    when T3."GenderCode" IS NULL then 'Uncoded'
    else T3."GenderNameE"
END as GENDER_EN_NM,

CASE
    when T3."GenderCode" IS NULL then 'Non codé'
    else T3."GenderNameF"
END as GENDER_FR_NM,

CASE
    when T4."MaritalStatusCode" IS NULL then -3
    else T1."MaritalStatusCode"
END as MARITAL_STATUS_CD,

CASE
    when T4."MaritalStatusCode" IS NULL then 'Uncoded'
    else T4."MaritalStatusNameE"
END as MARITAL_STATUS_EN_NM,

CASE
    when T4."MaritalStatusCode" IS NULL then 'Non codé'
    else T4."MaritalStatusName