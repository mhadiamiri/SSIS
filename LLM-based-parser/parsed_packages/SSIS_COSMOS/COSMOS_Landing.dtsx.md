## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| L_CO_CASE_CATEGORY           | Flat File          | File Path: [Inferred], Format: [Inferred]  | Source for `DFT_L_CO_CASE_CATEGORY` | File System Permissions likely | None            | Part 1                  |
| BI_Conformed           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for `DFT_L_CO_CASE_CATEGORY` | SQL Server Authentication likely | None            | Part 1                  |
| COSMOS_LANDING_SSIS           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for data flow tasks | SQL Server Authentication likely | None            | Part 1                  |
| COSMOS_SOURCE_SSIS           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for data flow tasks | SQL Server Authentication likely | None            | Part 1                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1|

## 3. Package Flow Analysis

The package executes tasks in sequence containers.  The main sequence appears to be:

1.  `EXPRESSIONT- Stage - Start Task`

The main ETL logic is segmented into subsequent Sequence Containers.
Each sequence container has its own truncate table task and data flow tasks.

#### SEQC-LANDING\_1

*   **Activities:**
    *   `ESQLT- TRUNCATE LANDING_1`: Truncates multiple tables: `dbo.v_JPC_TS_CombinedStatus`, `dbo.v_tCanadaStatus`, `dbo.v_tCase`, `dbo.v_tCaseNote`, `dbo.v_tCaseNoteTYpe`, `dbo.v_tCaseRelation`, `dbo.v_tCaseStatus`, `dbo.v_tCitizenshipService`, `dbo.v_tCitizenshipServiceType`, `dbo.v_tClient`, `dbo.v_tClientDocumentationType`
    *   `DFT_v_JPC_TS_CombinedStatus`: Data Flow Task loading data into `dbo.v_JPC_TS_CombinedStatus`
    *   `DFT_v_tCanadaStatus`: Data Flow Task loading data into `dbo.v_tCanadaStatus`
    *   `DFT_v_tCase`: Data Flow Task loading data into `dbo.v_tCase`
    *   `DFT_v_tCaseNote`: Data Flow Task loading data into `dbo.v_tCaseNote`
    *   `DFT_v_tCaseNoteTYpe`: Data Flow Task loading data into `dbo.v_tCaseNoteTYpe`
    *   `DFT_v_tCaseRelation`: Data Flow Task loading data into `dbo.v_tCaseRelation`
    *   `DFT_v_tCaseStatus`: Data Flow Task loading data into `dbo.v_tCaseStatus`
    *   `DFT_v_tCitizenshipService`: Data Flow Task loading data into `dbo.v_tCitizenshipService`
    *   `DFT_v_tCitizenshipServiceType`: Data Flow Task loading data into `dbo.v_tCitizenshipServiceType`
    *   `DFT_v_tClient`: Data Flow Task loading data into `dbo.v_tClient`
    *   `DFT_v_tClientDocumentationType`: Data Flow Task loading data into `dbo.v_tClientDocumentationType`
    *   `DFT_L_CO_CASE_CATEGORY`: Data Flow Task - disabled.

#### SEQC-LANDING\_2

*   **Activities:**
    *   `ESQLT- TRUNCATE LANDING_2`: Truncates multiple tables
    *   `DFT_v_tCountry`: Data Flow Task loading data into `dbo.v_tCountry`
    *   `DFT_v_tCurrency`: Data Flow Task loading data into `dbo.v_tCurrency`
    *   `DFT_v_tEmployee`: Data Flow Task loading data into `dbo.v_tEmployee`
    *   `DFT_v_tEmployeeCategory`: Data Flow Task loading data into `dbo.v_tEmployeeCategory`
    *   `DFT_v_tForeignCountryStatus`: Data Flow Task loading data into `dbo.v_tForeignCountryStatus`
    *   `DFT_v_tGender`: Data Flow Task loading data into `dbo.v_tGender`
    *   `DFT_v_tGeographicRegion`: Data Flow Task loading data into `dbo.v_tGeographicRegion`
    *   `DFT_v_tImmigrationService`: Data Flow Task loading data into `dbo.v_tImmigrationService`
    *   `DFT_v_tImmigrationServiceType`: Data Flow Task loading data into `dbo.v_tImmigrationServiceType`
    *   `DFT_v_tLanguage`: Data Flow Task loading data into `dbo.v_tLanguage`
    *   `DFT_v_JPC_TS_WorkFlowState_ARC`: Data Flow Task loading data into `dbo.v_JPC_TS_WorkFlowState_ARC`
    *   `DFT_v_JPC_TS_WorkFlowState`: Data Flow Task loading data into `dbo.v_JPC_TS_WorkFlowState`

#### SEQC-LANDING\_3

*   **Activities:**
    *   `ESQLT- TRUNCATE LANDING_3`: Truncates multiple tables listed above
    *   `DFT_v_tMaritalStatus`: Data Flow Task loading data into `dbo.v_tMaritalStatus`
    *   `DFT_v_tMission`: Data Flow Task loading data into `dbo.v_tMission`
    *   `DFT_v_tMissionType`: Data Flow Task loading data into `dbo.v_tMissionType`
    *   `DFT_v_tOccupation`: Data Flow Task loading data into `dbo.v_tOccupation`
    *   `DFT_v_tOtherGovDept`: Data Flow Task loading data into `dbo.v_tOtherGovDept`
    *   `DFT_v_tPassportDECProvince`: Data Flow Task loading data into `dbo.v_tPassportDECProvince`
    *   `DFT_v_tPassportReasonforIssuance`: Data Flow Task loading data into `dbo.v_tPassportReasonforIssuance`
    *   `DFT_v_tPassportService`: Data Flow Task loading data into `dbo.v_tPassportService`
    *   `DFT_v_tPassportService_ARC`: Data Flow Task loading data into `dbo.v_tPassportService_ARC`
    *   `DFT_v_tPassportServiceFee`: Data Flow Task loading data into `dbo.v_tPassportServiceFee`
    *   `DFT_v_tPMPPassportRole`: Data Flow Task loading data into `dbo.v_tPMPPassportRole`

#### SEQC-LANDING\_4

*   **Activities:**
    *   `ESQLT- TRUNCATE LANDING_4`: Truncates multiple tables listed above
    *   `DFT_v_tPassportServiceStatus`: Data Flow Task loading data into `dbo.v_tPassportServiceStatus`
    *   `DFT_v_tPassportStatus`: Data Flow Task loading data into `dbo.v_tPassportStatus`
    *   `DFT_v_tPassportTransactionType`: Data Flow Task loading data into `dbo.v_tPassportTransactionType`
    *   `DFT_v_tPassportTypeV2`: Data Flow Task loading data into `dbo.v_tPassportTypeV2`
    *   `DFT_v_tpikDecDocumenttype`: Data Flow Task loading data into `dbo.v_tpikDecDocumenttype`
    *   `DFT_v_tPMPCancelReason`: Data Flow Task loading data into `dbo.v_tPMPCancelReason`
    *   `DFT_v_tPMPDistributionType`: Data Flow Task loading data into `dbo.v_tPMPDistributionType`
    *   `DFT_v_tPMPServiceStream`: Data Flow Task loading data into `dbo.v_tPMPServiceStream`
    *   `DFT_v_tPMPWorkFlowStatus`: Data Flow Task loading data into `dbo.v_tPMPWorkFlowStatus`
    *   `DFT_v_tPrintStatus`: Data Flow Task loading data into `dbo.v_tPrintStatus`
    *   `DFT_v_tReceiptType`: Data Flow Task loading data into `dbo.v_tReceiptType`
    *   `DFT_v_tSubNationalUnit`: Data Flow Task loading data into `dbo.v_tSubNationalUnit`
    *   `DFT_v_tValidityPeriod`: Data Flow Task loading data into `dbo.v_tValidityPeriod`
    *   `DFT_v_tYesNo`: Data Flow Task loading data into `dbo.v_tYesNo`

**Data Flow Task Analysis Example:**

#### DFT_v_JPC_TS_CombinedStatus

*   **Source:** OLE DB Source (`OLEDB_SRC_v_JPC_TS_CombinedStatus`) extracts data from `dbo.v__JPC_TS_CombinedStatus` using the query:

```sql
select CombinedStatusCode
	  ,IRIS_StatusName
	  ,StatusNameE
	  ,StatusNameF
	  ,StatusDesc
	  ,IsPMP
	  ,IsIRIS
	  ,WorkPhase
	  ,PassportWorkFlowStatusCode
                  ,getdate() as EXTRACT_DT
                  ,getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]
from dbo.v__JPC_TS_CombinedStatus
```

*   **Destinations:** OLE DB Destination (`OLEDB_DEST_v_JPC_TS_CombinedStatus`) loads the data into `dbo.v_JPC_TS_CombinedStatus`

#### DFT_L_CO_CASE_CATEGORY

*   **Source:** Flat File Source (`Flat File Source_L_CO_CASE_CATEGORY`) reads data from a flat file connection `L_CO_CASE_CATEGORY`.
*   **Transformations:**
    *   `Derived Column`:  Calculates `ETL_CREA_DT`, `ETL_UPDT_DT`, and `EXTRACT_DT` using `GETDATE()`. Also uses  `REPLACENULL` function on `TimeStandardNew`, `TimeStandardOngoing`, `IsCurrent`, and `ComipCategoryCodePostCutoff` columns.
*   **Destination:** OLE DB Destination (`OLEDB_DEST_L_CO_CASE_CATEGORY`) loads data into `[dbo].[L_CO_CASE_CATEGORY]` using the connection `BI_Conformed`.

## 4. Code Extraction

```sql
-- From OLEDB_SRC_v_JPC_TS_CombinedStatus
select CombinedStatusCode
	  ,IRIS_StatusName
	  ,StatusNameE
	  ,StatusNameF
	  ,StatusDesc
	  ,IsPMP
	  ,IsIRIS
	  ,WorkPhase
	  ,PassportWorkFlowStatusCode
                  ,getdate() as EXTRACT_DT
                  ,getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]
from dbo.v__JPC_TS_CombinedStatus
```

This SQL query extracts data from  `dbo.v__JPC_TS_CombinedStatus` to load into `dbo.v_JPC_TS_CombinedStatus` in the Data Flow Task  `DFT_v_JPC_TS_CombinedStatus`.

```sql
SELECT StatusInCanadaCode
      ,StatusInCanadaNameE
      ,StatusInCanadaNameF
     ,getdate() as EXTRACT_DT
	,getdate() as [ETL_CREA_DT]
	,getdate() as [ETL_UPDT_DT]
    
  FROM dbo.v_tCanadaStatus
```

This SQL query extracts data from `dbo.v_tCanadaStatus` to load into  `dbo.v_tCanadaStatus` in the Data Flow Task  `DFT_v_tCanadaStatus`.

```sql
SELECT CaseCode
      ,Caseid
      ,CountryCode
      ,SNUCode
      ,OpenedDate
      ,CaseStatusCode
    ,'*** Protected B ***' as Subject  --- not found
      ,CaseCategoryCode
      ,MissionCode
      ,City
      ,MissionManagerCode
      ,HQManagerCode
      ,HQUnitCode
      ,IsCrisis
      ,FiledDate
      ,CaseReference
      ,CreatedBy
      ,CreationDate
      ,getdate() as EXTRACT_DT
	,getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]
  FROM dbo.v_tCase
```

This SQL query extracts data from `dbo.v_tCase` to load into `dbo.v_tCase` in the Data Flow Task `DFT_v_tCase`.

```sql
SELECT
    CaseCode,
    SequenceNum,
    FileNumber,
    EmployeeCode,
    EntryDate,
    Subject,
    NoteType,
    getdate() as EXTRACT_DT,
	getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]
  FROM dbo.v_tCaseNote
```

This SQL query extracts data from `dbo.v_tCaseNote` to load into `dbo.v_tCaseNote` in the Data Flow Task `DFT_v_tCaseNote`.

```sql
SELECT
 T1.Code,
 T1.Label as LabelE,
 T2.Label as LabelF
                   ,getdate() as EXTRACT_DT
	,getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]
FROM dbo.v_tpikCaseNoteType T1

Left join dbo.v_tpikCaseNoteType T2
on T1.Code = T2.Code
and T2.Language = '3084'

where T1.Language = '4105'
```

This SQL query extracts data from `dbo.v_tpikCaseNoteType` to load into `dbo.v_tCaseNoteTYpe` in the Data Flow Task `DFT_v_tCaseNoteTYpe`.

```sql
SELECT
CaseRelationCode
,CaseRelationNameE
,CaseRelationNameF
,getdate() as EXTRACT_DT
	,getdate() as [ETL_CREA_DT], 
	getdate() as [ETL_UPDT_DT]

FROM dbo.v_tCaseRelation
```

This SQL query extracts data from `dbo.v_tCaseRelation` to load into `dbo.v_tCaseRelation` in the Data Flow Task `DFT_v_tCaseRelation`.

```sql
SELECT

     CaseStatusCode
     ,CaseStatusNameE
     ,CaseStatusNameF
     ,getdate() as EXTRACT_DT
     ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]

  FROM dbo.v_tCaseStatus
```

This SQL query extracts data from `dbo.v_tCaseStatus` to load into `dbo.v_tCaseStatus` in the Data Flow Task `DFT_v_tCaseStatus`.

```sql
SELECT PersonCode
      ,ApplicationDate
      ,CitizenshipServTypeCode
      ,ToProcessingDate
      ,FromProcessingDate
     ,getdate() as EXTRACT_DT
	,getdate() as [ETL_CREA_DT]
	,getdate() as [ETL_UPDT_DT]
  FROM dbo.v_tCitizenshipService
```

This SQL 