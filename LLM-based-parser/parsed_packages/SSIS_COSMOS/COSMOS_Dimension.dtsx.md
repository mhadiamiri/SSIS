## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| COSMOS_REPORTING_SSIS     | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for Dimension data | SQL Server Authentication likely | None                  | Part 1, 2, 3                  |
| COSMOS_STAGING_SSIS       | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source data for Dimensions           | SQL Server Authentication likely            |  None                  | Part 1, 2, 3                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package `COSMOS_Dimension.dtsx` is a dimension loading package.
*   It truncates, loads, and performs DBCC checkident operations on multiple dimension tables.
*   The package inserts unknown members into the tables.
*   The package utilizes `S_CO_*` tables in staging schema as sources.
*   The target schema is `dbo` in the reporting database.
*   No Script Tasks found

#### DFT-DIMENSION_D_CO_CASES
*   **Source:** OLE DB Source (OLEDB_S_CO_CASES) extracts data from `dbo.S_CO_CASES`. The SQL query selects distinct case-related data from the source table.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_CASES) loads the data into `dbo.D_CO_CASES`.

#### DFT-DIMENSION_D_CO_CASE_CATEGORY
*   **Source:** OLE DB Source (OLEDB_S_CO_CASE_CATEGORY) extracts data from `dbo.S_CO_CASE_CATEGORY`. The SQL query selects various category-related data from the source table.
*   **Transformations:**
    *   `Data Conversion`: Converts `TYPE_CAT_FR_NM`, `SUBGROUP_CAT_FR_NM`, and `SERVICE_STANDARD_GRP_FR_NM` from wstr to str.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_CASE_CATEGORY) loads the transformed data into `dbo.D_CO_CASE_CATEGORY`.

#### DFT-DIMENSION_D_CO_CITIZENSHIP_SERVICE
*   **Source:** OLE DB Source (OLEDB_S_CO_CITIZENSHIP_SERVICE) extracts data from `dbo.S_CO_CITIZENSHIP_SERVICE`. The SQL query selects various citizenship service-related data from the source table.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_CITIZENSHIP_SERVICE) loads the data into `dbo.D_CO_CITIZENSHIP_SERVICE`.

#### DFT-DIMENSION_D_CO_DATE
*   **Source:** OLE DB Source (OLEDB_S_CO_DATE) extracts data from `dbo.S_CO_DATE`. The SQL query selects date dimension related data from the source table.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_DATE) loads the data into `dbo.D_CO_DATE`.

#### DFT-DIMENSION_D_CO_CLIENT
*   **Source:** OLE DB Source (OLEDB_S_CO_CLIENT) extracts data from `dbo.S_CO_CLIENT`. The SQL query selects client-related data from the source table.
*   **Transformations:**
    *   Lookup: LKP-D_CO_GEO_COUNTRY_BIRTH_COUNTRY retrieves `BIRTH_COUNTRY_SID`, `BIRTH_COUNTRY_EN_NM`, and `BIRTH_COUNTRY_FR_NM` from `dbo.D_CO_GEO_COUNTRY` based on `BIRTH_COUNTRY_CD`.
    *   Lookup: LKP-D_CO_GEO_COUNTRY_CITIZENSHIP_COUNTRY retrieves `CITIZENSHIP_COUNTRY_SID`, `CITIZENSHIP_COUNTRY_EN_NM`, and `CITIZENSHIP_COUNTRY_FR_NM` from `dbo.D_CO_GEO_COUNTRY` based on `CITIZENSHIP_CD`.
    *   Lookup: LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP retrieves `OTHER_CITIZENSHIP_SID`, `OTHER_CITIZENSHIP_COUNTRY_EN_NM`, and `OTHER_CITIZENSHIP_COUNTRY_FR_NM` from `dbo.D_CO_GEO_COUNTRY` based on `OTHER_CITIZENSHIP_CD`.
    *   DRVCOL_TRFM-Replace_Null_Values replaces null values in `BIRTH_COUNTRY_EN_NM`, `BIRTH_COUNTRY_FR_NM`, `CITIZENSHIP_COUNTRY_EN_NM`, and `OTHER_CITIZENSHIP_COUNTRY_FR_NM` with "Uncoded" or "Non codé".
    *   DCONV_TRFM-DataType converts `CLIENT_DOC_TYPE_EN_NM` and `CLIENT_DOC_TYPE_FR_NM` data types.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_CLIENT) loads the data into `dbo.D_CO_CLIENT`.

#### DFT-DIMENSION_D_CO_EMPLOYEE
*   **Source:** OLE DB Source (OLEDB_S_CO_EMPLOYEE) extracts data from `dbo.S_CO_EMPLOYEE`. The SQL query selects employee-related data from the source table.
*   **Transformations:**
    *   Lookup: LKP-D_CO_MISSION retrieves `MISSION_SID` from `dbo.D_CO_MISSION` based on `MISSION_CD`.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_EMPLOYEE) loads the data into `dbo.D_CO_EMPLOYEE`.

#### DFT-DIMENSION_D_CO_MISSION_GEO_COUNTRY
*   **Source:** OLE DB Source (OLEDB_D_CO_MISSION) extracts data from `dbo.D_CO_MISSION`. The SQL query selects mission-related data from the dimension table.
*   **Source:** OLE DB Source (OLEDB_S_CO_COUNTRY) extracts data from `dbo.S_CO_COUNTRY`. The SQL query selects country-related data from the source table.
*   **Transformations:**
    *   Merge Join: Merge Join combines the data from the two source components based on `DEFAULT_COUNTRY_CD` from `OLEDB_D_CO_MISSION` and `COUNTRY_CD` from `OLEDB_S_CO_COUNTRY`.
    *   Lookup: LKP-S_CO_COMMON_CODE_TABLE RC retrieves additional region information from `dbo.S_CO_COMMON_CODE_TABLE`.
    *   DCONV_TRFM-DataType converts `CNA_REGION_EN_NM` and `CNA_REGION_FR_NM` data types.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_MISSION_GEO_COUNTRY) loads the data into `dbo.D_CO_MISSION_GEO_COUNTRY`.

#### DFT-DIMENSION_D_CO_PPT_WORKFLOW_STATUS
*   **Source:** OLE DB Source (OLEDB_S_CO_PPT_WORKFLOW_STATUS) extracts data from `dbo.S_CO_PPT_WORKFLOW_STATUS`. The SQL query selects workflow status-related data from the source table.
*   **Transformations:**
    *   `Data Conversion`: Converts `WORKFLOW_STATUS_GROUP_EN_NM` and `WORKFLOW_STATUS_GROUP_FR_NM` from str to wstr.
*   **Destinations:** OLE DB Destination (OLEDB_DEST-D_CO_PPT_WORKFLOW_STATUS) loads the data into `dbo.D_CO_PPT_WORKFLOW_STATUS`.

## 4. Code Extraction

```sql
SELECT distinct CASE_CD,
	   CASE_ID,
	   CASE_REFERENCE_ID,
	   CASE_STATUS_CD,
	   CASE_STATUS_EN_NM,
	   CASE_STATUS_FR_NM,
	   SUBJECT_DESCR,
	   CITY_NM,
	   CRISIS_IND,
	   CASE_CREATION_DTM,
	   OPENED_DTM,
	   FILED_DTM,
       getdate() as ROW_INSERT_DTM,
	   getdate() as [ETL_CREA_DT],
       getdate() as [ETL_UPDT_DT]
FROM dbo.S_CO_CASES
```

Context: This SQL query is used in OLEDB_S_CO_CASES to extract data from the source table.

```sql
SELECT TYPE_CAT_CD
      ,TYPE_CAT_EN_NM
      ,TYPE_CAT_FR_NM
      ,SUBGROUP_CAT_CD
      ,SUBGROUP_CAT_EN_NM
      ,SUBGROUP_CAT_FR_NM
	  ,SERVICE_STANDARD_GRP_CD
	  ,SERVICE_STANDARD_GRP_EN_NM
	  ,SERVICE_STANDARD_GRP_FR_NM
      ,CASE_CATEGORY_CD
      ,CASE_CATEGORY_EN_NM
      ,CASE_CATEGORY_FR_NM
      ,COMIP_CATEGORY_CD
      ,TIME_STANDARD_NEW
      ,TIME_STANDARD_ONGOING
      ,IS_CURRENT_IND
      ,COMIPCATEGORY_POSTCUTOFF
      ,getdate() as ROW_INSERT_DTM
,getdate() as [ETL_CREA_DT]
,getdate() as [ETL_UPDT_DT]

  FROM dbo.S_CO_CASE_CATEGORY
```

Context: This SQL query is used in OLEDB_S_CO_CASE_CATEGORY to extract data from the source table.

```sql
SELECT PERSON_CD
      ,CITIZENSHIP_SERV_TYPE_CD
	  ,CITIZENSHIP_SERV_TYPE_EN_NM
      ,CITIZENSHIP_SERV_TYPE_FR_NM
      ,cast(APPLICATION_DTM as date) as APPLICATION_DT
	  ,APPLICATION_DTM as APPLICATION_DTM
      ,cast(FROM_PROCESSING_DTM as date) as FROM_PROCESSING_DT
	  ,FROM_PROCESSING_DTM as FROM_PROCESSING_DTM
	  ,cast(TO_PROCESSING_DTM as date) as TO_PROCESSING_DT
      ,TO_PROCESSING_DTM as TO_PROCESSING_DTM
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
FROM dbo.S_CO_CITIZENSHIP_SERVICE
```

Context: This SQL query is used in OLEDB_S_CO_CITIZENSHIP_SERVICE to extract data from the source table.

```sql
SELECT DATE_SID
      ,REC_TYPE
      ,DAY_ID
	  ,YEAR_ID
	  ,MONTH_ID
	  ,QUARTER_ID
	  ,QUARTER_NBR
	  ,WEEK_DAY_NBR
	  ,WEEK_DAY_EN
	  ,WEEK_DAY_FR
	  ,CALENDAR_YYYYMM
	  ,FISCAL_YEAR
	  ,FISCAL_YEAR_NM
	  ,FISCAL_MONTH
	  ,FISCAL_QUARTER
	  ,FISCAL_QUARTER_NM
	  ,FISCAL_YYYYMM
	  ,WORKING_DAY
	  ,MONTH_EN
	  ,MONTH_FR
	  ,MONTH_START_DT
	  ,MONTH_END_DT
	  ,MONTH_NBR
	  ,PERIOD
	  ,year(DATEADD(month,9,getdate())) as CURRENT_FY
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT],
	   getdate() as [ETL_UPDT_DT]
from dbo.S_CO_DATE
```

Context: This SQL query is used in OLEDB_S_CO_DATE to extract data from the source table.

```sql
SELECT 


      C.CLIENT_CD
      ,C.CASE_CD
      ,CAST(C.BIRTHDATE_DTM AS DATE) AS BIRTHDATE_DT

	  --++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	  ,CASE
	   WHEN C.BIRTHDATE_DTM <= getdate()
	   THEN convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25)
	   END as CLIENT_AGE
	  ,CASE
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 0 and 17
	   THEN '0-17'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 18 and 25
	   THEN '18-25'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 26 and 34
	   THEN '26-34'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 35 and 45
	   THEN '35-45'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 46 and 54
	   THEN '46-54'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) between 55 and 64
	   THEN '55-64'
	   WHEN C.BIRTHDATE_DTM <= getdate() and convert(int,datediff(DD,C.BIRTHDATE_DTM,getdate())/365.25) > 64
	   THEN '65+'
	   ELSE
	   'Uncoded/Non codé'
	   END as CLIENT_AGE_GROUP

	  --++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      ,C.BIRTH_COUNTRY_CD
      ,C.CITIZENSHIP_CD
      ,C.OTHER_CITIZENSHIP_CD
      ,C.LANGUAGE_CD
      ,C.LANGUAGE_EN_NM
      ,C.LANGUAGE_FR_NM
      ,C.ISO_CD
      ,C.ISO_LABEL_NM
      ,C.GENDER_CD
      ,C.GENDER_EN_NM
      ,C.GENDER_FR_NM
      ,C.MARITAL_STATUS_CD
      ,C.MARITAL_STATUS_EN_NM
      ,C.MARITAL_STATUS_FR_NM
      ,C.STATUS_IN_CANADA_CD
      ,C.STATUS_IN_CANADA_EN_NM
      ,C.STATUS_IN_CANADA_FR_NM
      ,C.STATUS_IN_COUNTRY_CD
      ,C.STATUS_IN_COUNTRY_EN_NM
      ,C.STATUS_IN_COUNTRY_FR_NM
      ,CAST(C.CANADA_DEPARTURE_DTM AS DATE) AS CANADA_DEPARTURE_DT
      ,C.CLIENT_CURRENT_ADDRESS_DESCR
      ,C.CLIENT_PERMANENT_ADDRESS_DESCR
      ,C.CLIENT_MAILING_ADDRESS_DESCR
      ,C.OCCUPATION_CD
      ,C.OCCUPATION_EN_NM
      ,C.OCCUPATION_FR_NM
      ,C.EMPLOYER_NM
      ,C.WORK_ADDRESS_DESCR
      ,C.WORK_PHONE_NBR
      ,C.CLIENT_SERVICE_TYPE_CD
      ,C.CLIENT_SERVICE_TYPE_EN_NM
      ,C.CLIENT_SERVICE_TYPE_FR_NM
      ,C.CASE_RELATION_CD
      ,C.CASE_RELATION_EN_NM
      ,C.CASE_RELATION_FR_NM
      ,C.CLIENT_DOC_TYPE_CD
      ,C.CLIENT_DOC_TYPE_EN_NM
	  ,C.CLIENT_DOC_TYPE_FR_NM
      ,CAST(C.DOC_ISSUE_DTM AS DATE) AS DOC_ISSUE_DT
      ,CAST(C.DOC_EXPIRY_DTM AS DATE) AS DOC_EXPIRY_DT
      ,C.DOC_ISSUING_CITY_NM
      ,C.DOC_ISSUING_COUNTRY_CD
      ,C.CUSTODY_CD
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
  FROM S_CO_CLIENT AS C
```

Context: This SQL query is used in OLEDB_S_CO_CLIENT to extract data from the source table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT PERSON_CD
      ,CITIZENSHIP_SERV_TYPE_CD
	  ,CITIZENSHIP_SERV_TYPE_EN_NM
      ,CITIZENSHIP_SERV_TYPE_FR_NM
      ,cast(APPLICATION_DTM as date) as APPLICATION_DT
	  ,APPLICATION_DTM as APPLICATION_DTM
      ,cast(FROM_PROCESSING_DTM as date) as FROM_PROCESSING_DT
	  ,FROM_PROCESSING_DTM as FROM_PROCESSING_DTM
	  ,cast(TO_PROCESSING_DTM as date) as TO_PROCESSING_DT
      ,TO_PROCESSING_DTM as TO_PROCESSING_DTM
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]

FROM dbo.S_CO_CITIZENSHIP_SERVICE
```

Context: This SQL query is used in OLEDB_S_CO_CITIZENSHIP_SERVICE to extract data from the source table.

```sql
SELECT DATE_SID
      ,REC_TYPE
      ,DAY_ID
	  ,YEAR_ID
	  ,MONTH_ID
	  ,QUARTER_ID
	  ,QUARTER_NBR
	  ,WEEK_DAY_NBR
	  ,WEEK_DAY_EN
	  ,WEEK_DAY_FR
	  ,CALENDAR_YYYYMM
	  ,FISCAL_YEAR
	  ,FISCAL_YEAR_NM
	  ,FISCAL_MONTH
	  ,FISCAL_QUARTER
	  ,FISCAL_QUARTER_NM
	  ,FISCAL_YYYYMM
	  ,WORKING_DAY
	  ,MONTH_EN
	  ,MONTH_FR
	  ,MONTH_START_DT
	  ,MONTH_END_DT
	  ,MONTH_NBR
	  ,PERIOD
	  ,year(DATEADD(month,9,getdate())) as CURRENT_FY
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT],
	   getdate() as [ETL_UPDT_DT]
from dbo.S_CO_DATE
```

Context: This SQL query is used in OLEDB_S_CO_DATE to extract data from the source table.

```sql
SELECT 
      COUNTRY_CD
      ,COALESCE(BD_C.GEO_COUNTRY_SID, -3) AS BIRTH_COUNTRY_SID
      ,COALESCE(BD_C.COUNTRY_EN_NM,'Uncoded') AS BIRTH_COUNTRY_EN_NM
      ,COALESCE(BD_C.COUNTRY_FR_NM,'Non codé') AS BIRTH_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS BD_C
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_BIRTH_COUNTRY to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZ.GEO_COUNTRY_SID, -3) AS CITIZENSHIP_COUNTRY_SID
      ,COALESCE(CTZ.COUNTRY_EN_NM,'Uncoded') AS CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZ.COUNTRY_FR_NM,'Non codé') AS CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZ
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_CITIZENSHIP_COUNTRY to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZO.GEO_COUNTRY_SID, -3) AS OTHER_CITIZENSHIP_SID
      ,COALESCE(CTZO.COUNTRY_EN_NM,'Uncoded') AS OTHER_CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZO.COUNTRY_FR_NM,'Non codé') AS OTHER_CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZO
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP to lookup data from the dimension table.

```sql
SELECT PERSON_CD
      ,CITIZENSHIP_SERV_TYPE_CD
	  ,CITIZENSHIP_SERV_TYPE_EN_NM
      ,CITIZENSHIP_SERV_TYPE_FR_NM
      ,cast(APPLICATION_DTM as date) as APPLICATION_DT
	  ,APPLICATION_DTM as APPLICATION_DTM
      ,cast(FROM_PROCESSING_DTM as date) as FROM_PROCESSING_DT
	  ,FROM_PROCESSING_DTM as FROM_PROCESSING_DTM
	  ,cast(TO_PROCESSING_DTM as date) as TO_PROCESSING_DT
      ,TO_PROCESSING_DTM as TO_PROCESSING_DTM
      ,getdate() as ROW_INSERT_DTM
	  ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]

FROM dbo.S_CO_CITIZENSHIP_SERVICE
```

Context: This SQL query is used in OLEDB_S_CO_CITIZENSHIP_SERVICE to extract data from the source table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZO.GEO_COUNTRY_SID, -3) AS OTHER_CITIZENSHIP_SID
      ,COALESCE(CTZO.COUNTRY_EN_NM,'Uncoded') AS OTHER_CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZO.COUNTRY_FR_NM,'Non codé') AS OTHER_CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZO
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP to lookup data from the dimension table.

```sql
SELECT 
      
	  coalesce(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZO.GEO_COUNTRY_SID, -3) AS OTHER_CITIZENSHIP_SID
      ,COALESCE(CTZO.COUNTRY_EN_NM,'Uncoded') AS OTHER_CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZO.COUNTRY_FR_NM,'Non codé') AS OTHER_CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZO
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZO.GEO_COUNTRY_SID, -3) AS OTHER_CITIZENSHIP_SID
      ,COALESCE(CTZO.COUNTRY_EN_NM,'Uncoded') AS OTHER_CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZO.COUNTRY_FR_NM,'Non codé') AS OTHER_CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZO
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZO.GEO_COUNTRY_SID, -3) AS OTHER_CITIZENSHIP_SID
      ,COALESCE(CTZO.COUNTRY_EN_NM,'Uncoded') AS OTHER_CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZO.COUNTRY_FR_NM,'Non codé') AS OTHER_CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZO
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_OTHER_CITIZENSHIP to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 
      
	  COALESCE(M.MISSION_SID, -3) AS MISSION_SID,
	  M.MISSION_CD
	  
	  
FROM dbo.D_CO_MISSION AS M
```

Context: This SQL query is used in LKP-D_CO_MISSION to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZ.GEO_COUNTRY_SID, -3) AS CITIZENSHIP_COUNTRY_SID
      ,COALESCE(CTZ.COUNTRY_EN_NM,'Uncoded') AS CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZ.COUNTRY_FR_NM,'Non codé') AS CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZ
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_CITIZENSHIP_COUNTRY to lookup data from the dimension table.

```sql
SELECT 

      COUNTRY_CD
      ,COALESCE(CTZ.GEO_COUNTRY_SID, -3) AS CITIZENSHIP_COUNTRY_SID
      ,COALESCE(CTZ.COUNTRY_EN_NM,'Uncoded') AS CITIZENSHIP_COUNTRY_EN_NM
      ,COALESCE(CTZ.COUNTRY_FR_NM,'Non codé') AS CITIZENSHIP_COUNTRY_FR_NM
	  
FROM dbo.D_CO_GEO_COUNTRY AS CTZ
```

Context: This SQL query is used in LKP-D_CO_GEO_COUNTRY_CIT