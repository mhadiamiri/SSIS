## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Purpose within Package                       | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager   | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=X:\ETL\COSMOS\R_COUNTRY_MAPPING-cosmosCountryCd.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";                                                                                                                                                                                                                                                                                                                                                                    | Read country mapping from Excel file     | File system access       | None                   | Part 1, 2, 3                  |
| Excel Connection Manager 1   | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=X:\ETL\COSMOS\CosmosCountryCd.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";                                                                                                                                                                                                                                                                                                                                                                                             | Read country mapping from Excel file     | File system access       | None                   | Part 1, 2, 3                  |
| Excel Connection Manager 2   | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=X:\ETL\COSMOS\R_COUNTRY_MAPPING-cosmosCountryCd.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";                                                                                                                                                                                                                                                                                                                                                                    | Read country mapping from Excel file     | File system access       | None                   | Part 1, 2, 3                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found               |                   |                              |                                     | No dependent SSIS packages tasks found | Part 1, 2, 3 |

## 3. Package Flow Analysis

The package `CCEM_Dimension` consists of a series of sequence containers and data flow tasks designed to populate dimension tables within a CCEM data warehouse. The package also begins with an expression task to determine which branches are used for the data flow.

*   **Initial Activity:**  `Dimensions - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` - Determines if data flow tasks should be run.

The rest of the tasks are sequence containers that contain data flow tasks and execute SQL tasks.

#### SEQC-D_CCEM_ACTIVITY

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_ACTIVITY`.  This task truncates table D_CCEM_ACTIVITY.
*   **Insert Unknown Members:** Inserts unknown members into the D_CCEM_ACTIVITY table.
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_ACTIVITY` reseeds the identity column of the D_CCEM_ACTIVITY table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_ACTIVITY` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC-CCEM_CASE_ACTIVITY` extracts data from the `CCEM_CASE_ACTIVITY` table in the staging database.
    *   **Destination:**  `OLEDB_DEST-D_CCEM_ACTIVITY` loads data into the `D_CCEM_ACTIVITY` table in the MART\_CCEM database.

#### SEQC-D_CCEM_ARREST_DETENTION

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_ARREST_DETENTION`.  This task truncates table D_CCEM_ARREST_DETENTION
*   **Insert Unknown Members:** Inserts unknown members into the D_CCEM_ARREST_DETENTION table.
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_ARREST_DETENTION` reseeds the identity column of the D_CCEM_ARREST_DETENTION table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_ARREST_DETENTION` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC_CCEM_ARREST_TRANSFER` extracts data from the `CCEM_ARREST_TRANSFER` table in the staging database.
    *   **Destination:**  `OLEDB_DEST_D_CCEM_ARREST_DETENTION` loads data into the `D_CCEM_ARREST_DETENTION` table in the MART\_CCEM database.

#### SEQC-D_CCEM_ARREST_DETENTION_FLAG

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_ARREST_DETENTION_FLAG`.  This task truncates table D_CCEM_ARREST_DETENTION_FLAG
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_ARREST_DETENTION_FLAG` reseeds the identity column of the D_CCEM_ARREST_DETENTION_FLAG table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_ARREST_DETENTION_FLAG` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC_D_CCEM_ARREST_DETENTION_FLAG` extracts data from a code table and creates flags.
    *   **Destination:**  `DFT-DIMENSION_D_CCEM_ARREST_DETENTION_FLAG` loads data into the `D_CCEM_ARREST_DETENTION_FLAG` table in the MART\_CCEM database.

#### SEQC-D_CCEM_ARREST_PRISON (DISABLED)

The data flow and SQL tasks are disabled for this sequence container. The steps are the same as the other sequence containers.

#### SEQC-D_CCEM_CASE

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_CASE`.  This task truncates table D_CCEM_CASE
*   **Insert Unknown Members:** Inserts unknown members into the D_CCEM_CASE table.
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_CASE` reseeds the identity column of the D_CCEM_CASE table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_CASE` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC_CCEM_CASE` extracts data from the `CCEM_CASE` table in the staging database.
    *   **Destination:**  `OLEDB_DEST_D_CCEM_CASE` loads data into the `D_CCEM_CASE` table in the MART\_CCEM database.

#### SEQC-D_CCEM_CASE_COUNTRY

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_CASE_COUNTRY`.  This task truncates table D_CCEM_CASE_COUNTRY
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_CASE_COUNTRY` reseeds the identity column of the D_CCEM_CASE_COUNTRY table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_COUNTRY` moves data from the staging database to the final dimension table.
    *   **Source:** `OLEDB_SRC_S_CCE_COUNTRY` extracts data from `dbo.CCEM_COUNTRY`.
    *   **Transformation:** Applies a `Data Conversion` and a `Lookup` from `[BI_Conformed].[dbo].[R_COUNTRY_MAPPING]` to enrich the data.
    *   **Destination:**  `OLEDB_DEST_D_CCEM_COUNTRY` loads data into the `D_CCEM_COUNTRY` table in the MART\_CCEM database.

#### SEQC-D_CCEM_CASE_EMPLOYEE

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_CASE_EMPLOYEE`.  This task truncates table D_CCEM_CASE_EMPLOYEE
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_CASE_EMPLOYEE` reseeds the identity column of the D_CCEM_CASE_EMPLOYEE table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_EMPLOYEE` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC_S_CCEM_EMPLOYEE` extracts data from the `CCEM_EMPLOYEE` table in the staging database.
    *   **Destination:**  `OLEDB_DEST_D_CCEM_EMPLOYEE` loads data into the `D_CCEM_EMPLOYEE` table in the MART\_CCEM database.

#### SEQC_D_CCEM_SLA

*   **Truncation of Table:**  `ESQLT- Truncate _D_CCEM_SLA`.  This task truncates table D_CCEM_SLA
*   **Insert Unknown Members:** Inserts unknown members into the D_CCEM_SLA table.
*   **Reseed Identity:**  `ESQLT- DBCC-D_CCEM_SLA` reseeds the identity column of the D_CCEM_SLA table.
*   **Data Flow:**  `DFT-DIMENSION_D_CCEM_SLA` moves data from the staging database to the final dimension table.
    *   **Source:**  `OLEDB_SRC_CCEM_SLA` extracts data from the `CCEM_SLA` table in the staging database.
    *   **Destination:**  `OLEDB_DEST-D_CCEM_SLA` loads data into the `D_CCEM_SLA` table in the MART\_CCEM database.

## 4. Code Extraction

The following code snippets were found in the package.

Truncate Table Statements:

```sql
TRUNCATE TABLE dbo.D_CCEM_ACTIVITY;
TRUNCATE TABLE dbo.D_CCEM_ARREST_DETENTION;
TRUNCATE TABLE dbo.D_CCEM_ARREST_DETENTION_FLAG;
TRUNCATE TABLE dbo.D_CCEM_ARREST_PRISON;
TRUNCATE TABLE dbo.D_CCEM_CASE;
TRUNCATE TABLE dbo.D_CCEM_CASE_COUNTRY;
TRUNCATE TABLE dbo.D_CCEM_CASE_EMPLOYEE;
TRUNCATE TABLE dbo.D_CCEM_SLA;
TRUNCATE TABLE dbo.D_CCEM_SUBCATEGORY;
TRUNCATE TABLE dbo.D_CCEM_REGISTRATION;
```

Insert Unknown Members:

```sql
SET IDENTITY_INSERT dbo.D_CCEM_ACTIVITY ON

INSERT INTO  dbo.D_CCEM_ACTIVITY(
[ACTIVITY_SID]
,[ACTIVITY_ID]
      ,[ACTIVITY_IDENTIFICATION]
      ,[ACTIVITY_SUBJECT_TXT]
     -- ,[ACTIVITY_DESCR]
      ,[ACTIVITY_TYPE_DESCR_EN]
      ,[ACTIVITY_TYPE_DESCR_FR]
      ,[ACTIVITY_CREATED_BY_EMPLOYEE_NM]
      ,[ACTIVITY_CREATED_ON_DT]
      ,[ACTIVITY_START_DT]
      ,[ACTIVITY_END_DT]
      ,[ACTIVITY_CONTACT_NM]
      ,[CASE_IDENTIFICATION]
      ,[LATEST_ACTIVITY_IND]
      ,[STATUS_DESCR_EN]
      ,[STATUS_DESCR_FR]
      ,[STATE_DESCR_EN]
      ,[STATE_DESCR_FR]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]

)  
VALUES 
  (-3,'-3','-3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,getdate(),getdate()
)

SET IDENTITY_INSERT dbo.D_CCEM_ACTIVITY OFF
```

```sql
SET IDENTITY_INSERT dbo.D_CCEM_ARREST_DETENTION ON

INSERT INTO dbo.D_CCEM_ARREST_DETENTION (

[ARREST_DETENTION_SID]
,[ARREST_TRANSFER_ID]
,[CASE_ID]
,[DETENTION_STATUS_NM_EN]
,[DETENTION_STATUS_NM_FR]
,[VERDICT_STATUS_NM_EN]
,[VERDICT_STATUS_NM_FR]
,[DETENTION_START_DT]
,[DETENTION_END_DT]
,[ETL_CREA_DT]
,[ETL_UPDT_DT]


)  
VALUES 
(-3,
-3,
-3,
null, 
null, 
null, 
null, 
null, 
null, 
getdate(), 
getdate()


)

SET IDENTITY_INSERT dbo.D_CCEM_ARREST_DETENTION OFF
```

```sql
SET IDENTITY_INSERT dbo.D_CCEM_ARREST_DETENTION ON

INSERT INTO dbo.D_CCEM_ARREST_DETENTION (

[ARREST_DETENTION_SID]
,[ARREST_TRANSFER_ID]
,[CASE_ID]
,[DETENTION_STATUS_NM_EN]
,[DETENTION_STATUS_NM_FR]
,[VERDICT_STATUS_NM_EN]
,[VERDICT_STATUS_NM_FR]
,[DETENTION_START_DT]
,[DETENTION_END_DT]
,[ETL_CREA_DT]
,[ETL_UPDT_DT]


)  
VALUES 
(-3,
-3,
-3,
null, 
null, 
null, 
null, 
null, 
null, 
getdate(), 
getdate()


)

SET IDENTITY_INSERT dbo.D_CCEM_ARREST_DETENTION OFF
```

```sql
SET IDENTITY_INSERT dbo.D_CCEM_ARREST_PRISON ON

INSERT INTO dbo.D_CCEM_ARREST_PRISON (

[PRISON_SID]
      ,[ACCOUNT_ID]
      ,[PRISON_LEVEL_NM]
      ,[PRISON_CITY_NM]
      ,[PRISON_SNU]
      ,[PRISON_PHONE_NBR]
      ,[PRISON_ADDRESS]
      ,[PRISON_DESCRIPTION]
      ,[PRISON_FAX_NBR]
      ,[PRISON_NAME]
      ,[PRISON_NOTE]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]


)  
VALUES 
(-3, -3, null,  null,  null,  null,  null,  null,  null,  null,  null,  getdate(),  getdate()


)

SET IDENTITY_INSERT dbo.D_CCEM_ARREST_PRISON OFF
```

```sql
SET IDENTITY_INSERT dbo.D_CCEM_CASE ON

INSERT INTO dbo.D_CCEM_CASE (

[CASE_SID] ,
[SUBCATEGORY_CASE_ID],
[CASE_ID],
[CASE_IDENTIFICATION],
[CATEGORY_ID],
[CATEGORY_DECSR],
[SUBCATEGORY_ID],
[SUBCATEGORY_DESCR],
[CREATED_BY_ID],
[CREATED_BY_NM],
[CREATED_ON_DT],
[MODIFIED_BY_ID],
[MODIFIED_BY_NM],
[MODIFIED_ON_DT],
[STATE_DESCR],
[STATUS_DESCR],
[COUNTRY_ID],
[COUNTRY_NM],
[COUNTRY_SUBDIVISION_ID],
[COUNTRY_SUBDIVISION_NM],
[SUMMARY_TXT],
[DUE_DT],
[COMPLETED_DT],
[READY_FOR_PROCESSING_DT],
[RECEIVED_DT],
[IRCC_RECEIVED_DT],
[IRCC_SUBMITTED_DT],
[PASSPORT_APPLIC_SUBMIT_DT],
[EMAIL],
[PHONE],
[GENERAL_ENQUIRIES_CATEGORY_CD],
[FIRST_NM],
[LAST_NM],
[AFFECTED_PERSON_ID],
[AFFECTED_PERSON_NM],
[TRIP_DESTINATION_ID],
[ATIP_ID],
[ATIP_NM],
[MEDICAL],
[SUB_CASE_IDENTIFICATION],
[SUB_CASE_NM],
[SUB_POLICE_REPORT_DT],
[SUB_POLICE_REPORT_TXT],
[SUB_CASE_KEYWORD_TXT],
[SUB_CASE_DETAILS_TXT],
[SUB_CASE_DT],
[SUB_CASE_START_DT],
[SUB_CASE_END_DT],
[ETL_CREA_DT],
[ETL_UPDT_DT]


)  
VALUES 
(-3,	'-3',	'-3',	'-3',	'-3',	null,	'-3',	null,	'-3',	null,	null,	null,	null,	null,	null,	null,	'-3',	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	-3,	null,	null,	null,	null,	null,	null,	null,	null,	getdate(),	getdate()
)

SET IDENTITY_INSERT dbo.D_CCEM_CASE OFF
```

```sql
  SET IDENTITY_INSERT dbo.[D_CCEM_CLIENT] ON

INSERT INTO dbo.[D_CCEM_CLIENT](
[CLIENT_SID]
      ,CONTACT_ID
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
)  
VALUES 
  (-3,'-3',getdate(),getdate()
)

SET IDENTITY_INSERT dbo.[D_CCEM_CLIENT] OFF
```

```sql
SET IDENTITY_INSERT dbo.D_CCEM_SUBCATEGORY ON

INSERT INTO dbo.D_CCEM_SUBCATEGORY(
[SUBCATEGORY_SID]
      ,[SUBCATEGORY_NBR]
      ,[CATEGORY_NBR]
      ,[SUBCATEGORY_DESCR_EN]
      ,[SUBCATEGORY_DESCR_FR]
      ,[CATEGORY_DESCR_EN]
      ,[CATEGORY_DESCR_FR]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]

)  
VALUES 
  (-3,'-3','-3',NULL,NULL,NULL,NULL,getdate(),getdate())

SET IDENTITY_INSERT dbo.D_CCEM_SUBCATEGORY OFF
```

DBCC CHECKIDENT Statements:

```sql
DBCC CHECKIDENT ('dbo.D_CCEM_ACTIVITY', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_ARREST_DETENTION', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_ARREST_DETENTION_FLAG', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_ARREST_PRISON', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_CASE', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_CASE_COUNTRY', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_CASE_EMPLOYEE', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_SLA', RESEED, 1)
DBCC CHECKIDENT ('dbo.D_CCEM_SUBCATEGORY', RESEED, 1)
```

Source SQL Queries:

```sql
SELECT  
     [ACTIVITY_ID]
      ,[CCEM_IDENTIFICATION]
      ,[CCEM_SUBJECT_TXT]
   --   ,[CCEM_DESCR]
      ,[CCEM_TYPE_NM_EN]
      ,[CCEM_TYPE_NM_FR]
      ,[CCEM_CASE_IDENTIFICATION]
      ,[CREATED_BY_NM]
      ,[CREATED_ON_DT]
      ,[CCEM_END_DT]
      ,[CCEM_START_DT]
      ,[CCEM_CASE_CONTACT_NM]
      ,[STATUS_DESCR_EN]
      ,[STATUS_DESCR_FR]
      ,[STATE_DESCR_EN]
      ,[STATE_DESCR_FR]
      ,[LATEST_ACTIVITY_IND]
      ,[STATE_CODE_ID]
      ,[STATUS_CODE_ID]
      ,[CCEM_ACTIVITY_TYPE_CD]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
  FROM [dbo].[CCEM_CASE_ACTIVITY]
-- Date: 2024-01-29.  Added this condition to avoid nightly failure.
-- There were empty records in the source.  So added the null 
---- condition. 
WHERE ACTIVITY_ID is not null
```

```sql
SELECT  distinct
      [ARREST_TRANSFER_ID]
      ,[CASE_ID]
      ,[DETENTION_STATUS_NM_EN]
      ,[DETENTION_STATUS_NM_FR]
      ,[VERDICT_STATUS_NM_EN]
      ,[VERDICT_STATUS_NM_FR]
      ,[DETENTION_START_DT]
      ,[DETENTION_END_DT]
      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
  FROM [dbo].[CCEM_ARREST_TRANSFER]
```

```sql
with arrestFlags as
(select 1 as flag_value
union all
select 0
union all
select -3)

select f1.flag_value as IS_CURRENT_DETENTION_IND
       ,f1.flag_value as IS_CURRENT_PRISON_IND
      ,f0.flag_value as IS_LAST_VISIT_IND
      ,getdate() as ETL_CREAT_DT
     ,getdate() as ETL_UPDT_DT


from arrestFlags f1
cross join arrestFlags f0
```

```sql
SELECT 

[ACCOUNTID]
   
      ,[ADDRESS1_COUNTY]
      ,[ADDRESS1_CITY]
      ,[ADDRESS1_STATEORPROVINCE]
      ,[ADDRESS1_COMPOSITE]
      ,[DESCRIPTION]
      ,[ADDRESS1_FAX]
      ,[NAME]
      ,[CCEM_ADDRESS1_ADDITIONALDETAILS]
      ,[ADDRESS1_TELEPHONE1]
      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]

  FROM [dbo].[CCEM_ARREST_PRISON]
```

```sql
select distinct

[CASE_ID] ,
[CASE_IDENTIFICATION],
[CATEGORY_ID],
[CATEGORY_DECSR],
[SUBCATEGORY_ID],
[SUBCATEGORY_DESCR],
[CREATED_BY_ID],
[CREATED_BY_NM],
[CREATED_ON_DT],
[MODIFIED_BY_ID],
[MODIFIED_BY_NM],
[MODIFIED_ON_DT],
[STATE_DESCR],
[STATUS_DESCR],
[COUNTRY_ID],
[COUNTRY_NM],
[COUNTRY_SUBDIVISION_ID],
[COUNTRY_SUBDIVISION_NM],
[SUMMARY_TXT],
[DUE_DT],
[COMPLETED_DT],
[READY_FOR_PROCESSING_DT],
[RECEIVED_DT],
[IRCC_RECEIVED_DT],
[IRCC_SUBMITTED_DT],
[PASSPORT_APPLIC_SUBMIT_DT],
[EMAIL],
[PHONE],
[GENERAL_ENQUIRIES_CATEGORY_CD],
[FIRST_NM],
[LAST_NM],
[AFFECTED_PERSON_ID],
[AFFECTED_PERSON_NM],
[TRIP_DESTINATION_ID],
[ATIP_ID],
[ATIP_NM],
[MEDICAL],
[SUBCATEGORY_CASE_ID],
[SUB_CASE_IDENTIFICATION],
[SUB_CASE_NM],
[SUB_POLICE_REPORT_DT],
[SUB_POLICE_REPORT_TXT],
[SUB_CASE_KEYWORD_TXT],
[SUB_CASE_DETAILS_TXT],
[SUB_CASE_DT],
[SUB_CASE_START_DT],
[SUB_CASE_END_DT],
getdate() as [ETL_CREA_DT],
getdate() as [ETL_UPDT_DT]

from dbo.CCEM_CASE
```

```sql
SELECT 
      [ALPHA_2_CD] COLLATE Latin1_General_CI_AS as ALPHA_2_CD
      ,[CNA_REGION_NAME_EN]
      ,[CNA_REGION_NAME_FR]
  
  FROM [BI_Conformed].[dbo].[R_COUNTRY_MAPPING]
```

```sql
SELECT 

[ACCOUNTID]
   
      ,[ADDRESS1_COUNTY]
      ,[ADDRESS1_CITY]
      ,[ADDRESS1_STATEORPROVINCE]
      ,[ADDRESS1_COMPOSITE]
      ,[DESCRIPTION]
      ,[ADDRESS1_FAX]
      ,[NAME]
      ,[CCEM_ADDRESS1_ADDITIONALDETAILS]
      ,[ADDRESS1_TELEPHONE1]
      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]

  FROM [dbo].[CCEM_ARREST_PRISON]
```

```sql
with arrestFlags as
(select 1 as flag_value
union all
select 0
union all
select -3)

select f1.flag_value as IS_CURRENT_DETENTION_IND
       ,f1.flag_value as IS_CURRENT_PRISON_IND
      ,f0.flag_value as IS_LAST_VISIT_IND
      ,getdate() as ETL_CREAT_DT
     ,getdate() as ETL_UPDT_DT


from arrestFlags f1
cross join arrestFlags f0
```

```sql
SELECT 

[CASE_ID] as [CASE_ID],
[ARREST_ID] as [ARREST_ID],
[ARREST_TRANSFER_ID] as [ARREST_TRANSFER_ID],
[ARREST_ACTIVITY_ID] as [ARREST_ACTIVITY_ID],
[APPEAL_DECISION] as [APPEAL_DT],
[CONSULAR_ASSIS_REFUSED] as [CLIENT_REFUSES_ACCESS],
[STATUS_CD_NM] as [CUSTODY_STATUS],
[DT_ARREST] as [DT_OF_ARREST],
[CAPITAL_PUNISHMENT_NM] as [DEATH_CHARGE],
[PREVIOUS_CONTACT_DT] as [LAST_CONTACT_DT],
[DETENTION_START_DT] as [PAROLE_DT],
[VISIT_START_DT] as [PLANNED_VISIT_DT],
[VISIT_TYPE_NM] as [PLANNED_VISIT_TYPE],
[CHARGE_PRIMARY_NM] as [PRIMARY_CHARGE_NM],
[PRISONER_NBR] as [PRISONER_NBR],
[CCEM_RELEASE] as [RELEASE_DT],
[ARREST_TRANSFER_ID] as [REQUIRE_TRANSFER],
[CHARGE_SECONDARY_NM] as [SECONDARY_CHARGE_NM],
[SENTENCE_DT] as [SENTENCE_DT],
[ITOO_REQUESTED] as [TRANSFER_REQUEST_DT],
[LATEST_DETENTION_INDICATOR] as [LATEST_DETENTION_STATUS],
[STATE_CD_NM] as [TRANSFER_STATUS],
[TRIAL_STATUS_NM] as [TRIAL_STATUS],
getdate() as [ETL_CREA_DT],
getdate() as [ETL_UPDT_DT]


  FROM [dbo].[CCEM_ARREST_DETENTION]
```

```sql
with arrestFlags as
(select 1 as flag_value
union all
select 0
union all
select -3)

select f1.flag_value as IS_CURRENT_DETENTION_IND
       ,f1.flag_value as IS_CURRENT_PRISON_IND
      ,f0.flag_value as IS_LAST_VISIT_IND
      ,getdate() as ETL_CREAT_DT
     ,getdate() as ETL_UPDT_DT


from arrestFlags f1
cross join arrestFlags f0
```

```sql
SELECT 

[CASE_ID] as [CASE_ID],
[ARREST_ID] as [ARREST_ID],
[ARREST_TRANSFER_ID] as [ARREST_TRANSFER_ID],
[ARREST_ACTIVITY_ID] as [ARREST_ACTIVITY_ID],
[APPEAL_DECISION] as [APPEAL_DT],
[CONSULAR_ASSIS_REFUSED] as [CLIENT_REFUSES_ACCESS],
[STATUS_CD_NM] as [CUSTODY_STATUS],
[DT_ARREST] as [DT_OF_ARREST],
[CAPITAL_PUNISHMENT_NM] as [DEATH_CHARGE],
[PREVIOUS_CONTACT_DT] as [LAST_CONTACT_DT],
[DETENTION_START_DT] as [PAROLE_DT],
[VISIT_START_DT] as [PLANNED_VISIT_DT],
[VISIT_TYPE_NM] as [PLANNED_VISIT_TYPE],
[CHARGE_PRIMARY_NM] as [PRIMARY_CHARGE_NM],
[PRISONER_NBR] as [PRISONER_NBR],
[CCEM_RELEASE] as [RELEASE_DT],
[ARREST_TRANSFER_ID] as [REQUIRE_TRANSFER],
[CHARGE_SECONDARY_NM] as [SECONDARY_CHARGE_NM],
[SENTENCE_DT] as [SENTENCE_DT],
[ITOO_REQUESTED] as [TRANSFER_REQUEST_DT],
[LATEST_DETENTION_INDICATOR] as [LATEST_DETENTION_STATUS],
[STATE_CD_NM] as [TRANSFER_STATUS],
[TRIAL_STATUS_NM] as [TRIAL_STATUS],
getdate() as [ETL_CREA_DT],
getdate() as [ETL_UPDT_DT]


  FROM [dbo].[CCEM_ARREST_DETENTION]
```

## 5. Output Analysis

| Destination Table                   | Description                                                                 | Source Part                                                                                                                                                                                        |
|------------------------------------|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dbo.D_CCEM_ACTIVITY               | Stores activity dimension data.                                             | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_ARREST_DETENTION         | Stores arrest and detention dimension data                                       | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_ARREST_DETENTION_FLAG       | Stores arrest and detention flag dimension data                                      | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_ARREST_PRISON       | Stores arrest and prison data.  This data flow is disabled.                                       | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_CASE                     | Stores case dimension data.                                                  | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_COUNTRY                  | Stores country dimension data.                                               | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_CASE_EMPLOYEE            | Stores case employee dimension data.                                       | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_SLA                      | Stores SLA (Service Level Agreement) dimension data.                               | Part 3                                                                                                                                                                                             |
| dbo.D_CCEM_SUBCATEGORY              | Stores subcategory dimension data.                                          | Part 3                                                                                                                                                                                             |

## 6. Package Summary

*   **Input Connections:** 5
    *   3 Excel connections for R_COUNTRY_MAPPING-cosmosCountryCd.xlsx and CosmosCountryCd.xlsx
    *   2 OLE DB Connections for CCEM_STAGING and BI_Conformed
    *   1 project connection for MART_CCEM
*   **Output Destinations:**  9 dimension tables
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 1
    *   Sequence Containers: 8
    *   Execute SQL Tasks: 24
    *   Data Flow Tasks: 9
    *   Lookup Transformations: 4
    *  Data Conversion: 1

*   **Overall package complexity assessment:** Medium.
*   **Potential performance bottlenecks:**  Lookup transformation from BI_Conformed database.  This database may be external to the staging database.
*   **Critical path analysis:**  The package follows a linear flow, with each sequence container dependent on the successful completion of the previous one.  Any failure in any sequence container will halt the package execution.
*   **Document error handling mechanisms:**  The package has an `OnError` event handler that updates the ETL process status to "Failed".  The source for this update is a variable `User::V_SQL_UPDATE_ON_ERROR`.
