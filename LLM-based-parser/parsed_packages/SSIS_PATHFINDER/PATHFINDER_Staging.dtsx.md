```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| ODS_PATHFINDER            | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source connection for all staging data flows  | SQL Server Auth likely | None            | All Data Flow Tasks                  |
| STG_PATHFINDER            | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination connection for all staging data flows             | SQL Server Auth likely            |  All Data Flow Tasks                  |
| Project.ConnectionManagers[ODS_PATHFINDER] | OLE DB | Server: [Inferred], Database: [Inferred] | Source connection for all staging data flows | SQL Server Auth likely | None | All Data Flow Tasks |
| Project.ConnectionManagers[STG_PATHFINDER] | OLE DB | Server: [Inferred], Database: [Inferred] | Destination connection for all staging data flows | SQL Server Auth likely | None | All Data Flow Tasks |
| {3653D0A0-E512-4269-94C0-866616C4F312} | OLE DB | Server: [Inferred], Database: [Inferred] | Used in Execute SQL Tasks for ETL Status updates | SQL Server Auth likely | User::V_SQL_INSERT_ON_PRE_EXECUTE, User::V_SQL_UPDATE_ON_ERROR, User::V_SQL_UPDATE_ON_POST_EXECUTE | Event Handlers and Expression Task |
| {347E8B01-4F97-43D9-98BC-39CEE8A43223} | OLE DB | Server: [Inferred], Database: [Inferred] | Destination connection for all staging data flows | SQL Server Auth likely | None | Sequence Container - Load STAGING Tables |
| {5B56212A-CCCD-48FA-94DD-1C928AC74B40} | OLE DB | Server: [Inferred], Database: [Inferred] | Source connection for all staging data flows | SQL Server Auth likely | None | Sequence Container - Load STAGING Tables |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All|

## 3. Package Flow Analysis

*   The package begins with an `EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` Expression Task.
*   It then proceeds to a `SEQC- Load STAGING Tables` Sequence Container.
*   The package has `OnError` and `OnPostExecute` event handlers to manage failures and successes.

#### SEQC- Load STAGING Tables

*   Begins by executing `ESQLT- Truncate Staging Tables` which truncates six staging tables: `S_PATHFINDER_CBSA_STEEL_CLASSIFICATION`, `S_PATHFINDER_CBSA_STEEL_COMMODITIES`, `S_PATHFINDER_CBSA_STEEL_DATA`, `S_PATHFINDER_CBSA_WHEAT_DATA`, `S_PATHFINDER_CT_PORTS`, and `S_PATHFINDER_CT_STEEL_INDUSTRIES`.
*   The sequence container then loads the aforementioned tables using Data Flow Tasks, each loading one table.
*   Each Data Flow Task extracts data from a source table in the `ODS_PATHFINDER` database and loads it into a staging table in the `STG_PATHFINDER` database.
*   Each Data Flow Task has an OLE DB Source and an OLE DB Destination.

#### DFT- S_PATHFINDER_CBSA_STEEL_CLASSIFICATION

*   **Source:** OLE DB Source extracts data from `dbo.Ct_Pathfinder_Steel_Industries` and `dbo.Ct_Steel_Classifications` joined together.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CBSA_STEEL_CLASSIFICATION`.

#### DFT- S_PATHFINDER_CBSA_STEEL_COMMODITIES

*   **Source:** OLE DB Source extracts data from `dbo.post_2012_Steel_Commodities`.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CBSA_STEEL_COMMODITIES`.

#### DFT- S_PATHFINDER_CBSA_STEEL_DATA

*   **Source:** OLE DB Source extracts data from `dbo.CBSA_STEEL_DATA`, `dbo.CBSA_STEEL_DATA_EXT` and `dbo.ct_Countries` joined together.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CBSA_STEEL_DATA`.

#### DFT- S_PATHFINDER_CBSA_WHEAT_DATA

*   **Source:** OLE DB Source extracts data from `dbo.CBSA_WHEAT_DATA`, `dbo.ct_Countries1` and `dbo.CBSA_WHEAT_DATA_EXT` joined together.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CBSA_WHEAT_DATA`.

#### DFT- S_PATHFINDER_CT_PORTS

*   **Source:** OLE DB Source extracts data from `dbo.Ct_Ports`.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CT_PORTS`.

#### DFT- S_PATHFINDER_CT_STEEL_INDUSTRIES

*   **Source:** OLE DB Source extracts data from `dbo.Ct_pathfinder_Steel_Industries`.
*   **Destination:** OLE DB Destination loads data into `dbo.S_PATHFINDER_CT_STEEL_INDUSTRIES`.

#### Event Handlers

*   `OnError` event handler updates the ETL process status to Failed.
*   `OnPostExecute` event handler updates the ETL process status to Succeeded.
*   `OnPreExecute` event handler creates a record with running status

## 4. Code Extraction

```markdown
-- From ESQLT- Truncate Staging Tables
TRUNCATE TABLE  dbo.[S_PATHFINDER_CBSA_STEEL_CLASSIFICATION];
TRUNCATE TABLE  dbo.[S_PATHFINDER_CBSA_STEEL_COMMODITIES];
TRUNCATE TABLE  dbo.[S_PATHFINDER_CBSA_STEEL_DATA];
TRUNCATE TABLE  dbo.[S_PATHFINDER_CBSA_WHEAT_DATA];
TRUNCATE TABLE  dbo.[S_PATHFINDER_CT_PORTS];
TRUNCATE TABLE  dbo.[S_PATHFINDER_CT_STEEL_INDUSTRIES];
```

Context: This SQL code truncates the staging tables.

```sql
-- From PATHFINDER_CBSA_STEEL_CLASSIFICATION Source
SELECT distinct 
Ct_Steel_Classifications.HS_Code 		AS HS_Code, 
Ct_Steel_Classifications.Cmdty_Eng_Desc AS Cmdty_Eng_Desc, 
Ct_Steel_Classifications.Cmdty_Efctv_Dt AS Cmdty_Efctv_Dt, 
Ct_Steel_Classifications.Cmdty_Expiry_Dt AS Cmdty_Expiry_Dt, 
Ct_Steel_Classifications.Steel_Ind_Cd AS Steel_Ind_Cd, 
Ct_Pathfinder_Steel_Industries.Steel_Ind_Eng_Desc AS Steel_Ind_Eng_Desc, 
Ct_Pathfinder_Steel_Industries.Steel_Ind_Fr_Desc AS Steel_Ind_Fr_Desc, 
Ct_Pathfinder_Steel_Industries.Steel_Ind_Efctv_Dt AS Steel_Ind_Efctv_Dt, 
Ct_Pathfinder_Steel_Industries.Steel_Ind_Expiry_Dt AS Steel_Ind_Expiry_Dt,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT

FROM dbo.Ct_Pathfinder_Steel_Industries Ct_Pathfinder_Steel_Industries 
INNER JOIN dbo.Ct_Steel_Classifications Ct_Steel_Classifications 
ON Ct_Pathfinder_Steel_Industries.Steel_Ind_Cd = Ct_Steel_Classifications.Steel_Ind_Cd
```

Context: This SQL code extracts data for `S_PATHFINDER_CBSA_STEEL_CLASSIFICATION` from the ODS database.

```sql
-- From PATHFINDER_CBSA_STEEL_COMMODITIES Source
SELECT distinct 
post_2012_Steel_Commodities.Cmdty_Cd AS Cmdty_Cd, SUBSTRING(post_2012_Steel_Commodities.Cmdty_Cd,1,10) AS HS_10_Code, post_2012_Steel_Commodities.Cmdty_Eng_Desc AS Cmdty_Eng_Desc, post_2012_Steel_Commodities.Cmdty_Fr_Desc AS Cmdty_Fr_Desc, post_2012_Steel_Commodities.Cmdty_Efctv_Dt AS Cmdty_Efctv_Dt, post_2012_Steel_Commodities.Cmdty_Expiry_Dt AS Cmdty_Expiry_Dt 
 ,getdate() as [ETL_CREA_DT]
  ,getdate() as [ETL_UPDT_DT]
FROM dbo.post_2012_Steel_Commodities
```

Context: This SQL code extracts data for `S_PATHFINDER_CBSA_STEEL_COMMODITIES` from the ODS database.

```sql
-- From PATHFINDER_CBSA_STEEL_DATA Source
SELECT
CBSA_STEEL_DATA_EXT.Ext_ID AS Ext_ID, CBSA_STEEL_DATA_EXT.Service_Option AS Service_Option, CBSA_STEEL_DATA_EXT.Importer_BN AS Importer_BN, CBSA_STEEL_DATA_EXT.Release_Office AS Release_Office, CBSA_STEEL_DATA_EXT.Importer_Name AS Importer_Name, CBSA_STEEL_DATA_EXT.Exporter_Name AS Exporter_Name, CBSA_STEEL_DATA_EXT.Vendor_Name AS Vendor_Name, CBSA_STEEL_DATA.Broker_ID AS Broker_ID, CBSA_STEEL_DATA.Broker_Name AS Broker_Name, CBSA_STEEL_DATA_EXT.Net_Weight AS Net_Weight, CBSA_STEEL_DATA_EXT.Net_Weight_UOM AS Net_Weight_UOM, CBSA_STEEL_DATA_EXT.Gross_Weight AS Gross_Weight, CBSA_STEEL_DATA_EXT.Gross_Weight_UOM AS Gross_Weight_UOM, CBSA_STEEL_DATA_EXT.GIP AS GIP, CBSA_STEEL_DATA.ID AS ID, CBSA_STEEL_DATA.Date_Inserted AS Date_Inserted, CBSA_STEEL_DATA.Transaction_Number AS Transaction_Number, CBSA_STEEL_DATA.Country_Of_Origin AS Country_Of_Origin, ct_Countries.Location_Eng_Nm AS Location_Eng_Nm, ct_Countries.Location_Fr_Nm AS Location_Fr_Nm, CBSA_STEEL_DATA.Release_Date AS Release_Date, CBSA_STEEL_DATA.HS_Code AS HS_Code, CBSA_STEEL_DATA.HS_Price AS HS_Price, CBSA_STEEL_DATA.HS_Weight AS HS_Weight, CBSA_STEEL_DATA.HS_UOM AS HS_UOM, CBSA_STEEL_DATA.ActiveYN AS ActiveYN, CBSA_STEEL_DATA.Updated AS Updated, CBSA_STEEL_DATA.Date_Updated AS Date_Updated, CBSA_STEEL_DATA.Note AS Note, CBSA_STEEL_DATA.Country_Of_Export AS Country_Of_Export, CBSA_STEEL_DATA.State_Of_Export AS State_Of_Export 
 ,getdate() as [ETL_CREA_DT]
  ,getdate() as [ETL_UPDT_DT]
, CBSA_STEEL_DATA.Cntry_melt_pour as Cntry_melt_pour 
FROM dbo.CBSA_STEEL_DATA CBSA_STEEL_DATA 
INNER JOIN dbo.CBSA_STEEL_DATA_EXT CBSA_STEEL_DATA_EXT 
	ON CBSA_STEEL_DATA.Ext_ID = CBSA_STEEL_DATA_EXT.Ext_ID 
INNER JOIN dbo.ct_Countries ct_Countries 
	ON CBSA_STEEL_DATA.Country_Of_Origin = ct_Countries.ISO_Cd
```

Context: This SQL code extracts data for `S_PATHFINDER_CBSA_STEEL_DATA` from the ODS database.

```sql
-- From PATHFINDER_CBSA_WHEAT_DATA Source
SELECT distinct
CBSA_WHEAT_DATA.ID AS ID, CBSA_WHEAT_DATA.Ext_ID AS Ext_ID, CBSA_WHEAT_DATA.Date_Inserted AS Date_Inserted, CBSA_WHEAT_DATA.Transaction_Number AS Transaction_Number, CBSA_WHEAT_DATA.Country_Of_Origin AS Country_Of_Origin, CBSA_WHEAT_DATA.HS_Code AS HS_Code, CBSA_WHEAT_DATA.HS_Price AS HS_Price, CBSA_WHEAT_DATA.HS_Weight AS HS_Weight, CBSA_WHEAT_DATA.HS_UOM AS HS_UOM, CBSA_WHEAT_DATA.Release_Date AS Release_Date, CBSA_WHEAT_DATA.ActiveYN AS ActiveYN, CBSA_WHEAT_DATA.Updated AS Updated, CBSA_WHEAT_DATA.Date_Updated AS Date_Updated, CBSA_WHEAT_DATA.Note AS Note, CBSA_WHEAT_DATA_EXT.Service_Option AS Service_Option, CBSA_WHEAT_DATA_EXT.Importer_BN AS Importer_BN, CBSA_WHEAT_DATA_EXT.Release_Office AS Release_Office, CBSA_WHEAT_DATA_EXT.Importer_Name AS Importer_Name, CBSA_WHEAT_DATA_EXT.Exporter_Name AS Exporter_Name, CBSA_WHEAT_DATA_EXT.Vendor_Name AS Vendor_Name, CBSA_WHEAT_DATA_EXT.Net_Weight AS Net_Weight, CBSA_WHEAT_DATA_EXT.Net_Weight_UOM AS Net_Weight_UOM, CBSA_WHEAT_DATA_EXT.Gross_Weight AS Gross_Weight, CBSA_WHEAT_DATA_EXT.Gross_Weight_UOM AS Gross_Weight_UOM, CBSA_WHEAT_DATA_EXT.GIP AS GIP, ct_Countries1.Location_Id AS Location_Id, ct_Countries1.Location_Eng_Nm AS Location_Eng_Nm, ct_Countries1.Location_Fr_Nm AS Location_Fr_Nm, ct_Countries1.ISO_Cd AS ISO_Cd 
 ,getdate() as [ETL_CREA_DT]
  ,getdate() as [ETL_UPDT_DT]
FROM dbo.CBSA_WHEAT_DATA CBSA_WHEAT_DATA 
INNER JOIN dbo.ct_Countries ct_Countries1 
	ON CBSA_WHEAT_DATA.Country_Of_Origin = ct_Countries1.ISO_Cd 
INNER JOIN dbo.CBSA_WHEAT_DATA_EXT CBSA_WHEAT_DATA_EXT 
	ON CBSA_WHEAT_DATA_EXT.Ext_ID = CBSA_WHEAT_DATA.Ext_ID
```

Context: This SQL code extracts data for `S_PATHFINDER_CBSA_WHEAT_DATA` from the ODS database.

```sql
-- From PATHFINDER_CT_PORTS Source
SELECT [Release_Office]
      ,[Port_Eng_Desc]
      ,[Port_Fr_Desc]
      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT] 
 FROM [dbo].[Ct_Ports]
```

Context: This SQL code extracts data for `S_PATHFINDER_CT_PORTS` from the ODS database.

```sql
-- From PATHFINDER_CT_STEEL_INDUSTRIES Source
SELECT [Steel_Ind_Cd]
      ,[Steel_Ind_Eng_Desc]
      ,[Steel_Ind_Fr_Desc]
      ,[Steel_Ind_Efctv_Dt]
      ,[Steel_Ind_Expiry_Dt]
  ,getdate() as [ETL_CREA_DT]
  ,getdate() as [ETL_UPDT_DT]
  FROM [dbo].[Ct_pathfinder_Steel_Industries]
```

Context: This SQL code extracts data for `S_PATHFINDER_CT_STEEL_INDUSTRIES` from the ODS database.

```sql
-- From ESQLT- Update ETL Process Status to Failed
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PATHFINDER_Staging.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL code updates the ETL process status to FAILED in case of an error.

```sql
-- From ESQLT- Update ETL Process Status to Succeeded
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PATHFINDER_Staging.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL code updates the ETL process status to SUCCEEDED after successful execution.

```sql
-- From ESQLT- Create Record  with Running Status
INSERT INTO [ETL_RUN_STATUS] (
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )
VALUES (
 (
  SELECT ETL_COMPONENT_ID
  FROM ETL_COMPONENT
  WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'   -- 'NEICS_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'PATHFINDER_Master.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/PATHFINDER' 
    )
   AND ETL_SUB_COMPONENT_NM = 'PATHFINDER_Staging.DTSX'   --'NEICS_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

Context: This SQL code inserts a new record into the ETL_RUN_STATUS table with a 'RUNNING' status.

## 5. Output Analysis

| Destination Table                            | Description                                                                | Source Part                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dbo.S_PATHFINDER_CBSA_STEEL_CLASSIFICATION | Stores CBSA Steel Classification data                                     | Data Flow Task: S_PATHFINDER_CBSA_STEEL_CLASSIFICATION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| dbo.S_PATHFINDER_CBSA_STEEL_COMMODITIES    | Stores CBSA Steel Commodities data                                        | Data Flow Task: S_PATHFINDER_CBSA_STEEL_COMMODITIES                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| dbo.S_PATHFINDER_CBSA_STEEL_DATA           | Stores CBSA Steel data                                                    | Data Flow Task: S_PATHFINDER_CBSA_STEEL_DATA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| dbo.S_PATHFINDER_CBSA_WHEAT_DATA           | Stores CBSA Wheat data                                                    | Data Flow Task: S_PATHFINDER_CBSA_WHEAT_DATA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| dbo.S_PATHFINDER_CT_PORTS                  | Stores CT Ports data                                                      | Data Flow Task: S_PATHFINDER_CT_PORTS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| dbo.S_PATHFINDER_CT_STEEL_INDUSTRIES       | Stores CT Steel Industries data                                           | Data Flow Task: S_PATHFINDER_CT_STEEL_INDUSTRIES                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ETL_RUN_STATUS                             | Stores the status of the ETL process (RUNNING, SUCCEEDED, FAILED) | Execute SQL Tasks in Event Handlers.  The tasks insert records before execution and then update them after execution or in the event of an error. |

## 6. Package Summary

*   **Input Connections:** 2 or 3
*   **Output Destinations:** 6 staging tables + `ETL_RUN_STATUS`
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 1
    *   Data Flow Tasks: 6
    *   Execute SQL Tasks: 4+
    *   Expression Task: 2+
*   Overall package complexity assessment: medium.
*   Potential performance bottlenecks: The truncation of the staging tables might be slow if the tables are very large.
    * Data flow tasks performance may depend on data volume.
*   Critical path analysis: The critical path is through the sequence container and the data flow tasks, since the source data needs to be available, and the destinations need to be available.
*   Error handling mechanisms: The package uses `OnError` event handlers to update the ETL process status to FAILED.
```