## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_PATHFINDER           | OLE DB          | Server: [Inferred], Database: [Inferred] | Destination for dimension data | SQL Server Auth likely | None  | All Data Flow Tasks                 |
| STG_PATHFINDER           | OLE DB          | Server: [Inferred], Database: [Inferred] | Source for dimension data | SQL Server Auth likely | None  | All Data Flow Tasks                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All|

## 3. Package Flow Analysis

The package begins with an `ExpressionTask` that always evaluates to true.  This task serves as a starting point for subsequent branches.

*   A `Sequence Container` named `SEQC-Truncate Dimension Tables` is executed when `@[$Project::PRJ_PRM_PROCESS_NODE]` is either "ALL" or "DIMENSION".

The `SEQC-Truncate Dimension Tables` Sequence Container contains the following Data Flow Tasks and one Execute SQL Task:

*   `D_PATHFINDER_CBSA_STEEL_CLASSIFICATION`
*   `D_PATHFINDER_CBSA_STEEL_COMMODITIES`
*   `D_PATHFINDER_CBSA_STEEL_DATA`
*   `D_PATHFINDER_CBSA_WHEAT_DATA`
*   `D_PATHFINDER_CT_PORTS`
*   `D_PATHFINDER_CT_STEEL_INDUSTRIES`
*   `ESQLT- Truncate And Seed PathFinder Dimensions`

#### DFT- D_PATHFINDER_CBSA_STEEL_CLASSIFICATION

*   **Source:** OLE DB Source (S\_PATHFINDER\_CBSA\_STEEL\_CLASSIFICATION Source) extracts data from `dbo.S_PATHFINDER_CBSA_STEEL_CLASSIFICATION` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CBSA\_STEEL\_CLASSIFICATION Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CBSA_STEEL_CLASSIFICATION` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### DFT- D_PATHFINDER_CBSA_STEEL_COMMODITIES

*   **Source:** OLE DB Source (S\_PATHFINDER\_CBSA\_STEEL\_COMMODITIES Source) extracts data from `dbo.S_PATHFINDER_CBSA_STEEL_COMMODITIES` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CBSA\_STEEL\_COMMODITIES Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CBSA_STEEL_COMMODITIES` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### DFT- D_PATHFINDER_CBSA_STEEL_DATA

*   **Source:** OLE DB Source (S\_PATHFINDER\_CBSA\_STEEL\_DATA Source) extracts data from `dbo.S_PATHFINDER_CBSA_STEEL_DATA` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CBSA\_STEEL\_DATA Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CBSA_STEEL_DATA` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### DFT- D_PATHFINDER_CBSA_WHEAT_DATA

*   **Source:** OLE DB Source (S\_PATHFINDER\_CBSA\_WHEAT\_DATAD\_PATHFINDER\_CBSA\_WHEAT\_DATA Source) extracts data from `dbo.S_PATHFINDER_CBSA_WHEAT_DATA` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CBSA\_WHEAT\_DATA Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CBSA_WHEAT_DATA` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### DFT- D_PATHFINDER_CT_PORTS

*   **Source:** OLE DB Source (S\_PATHFINDER\_CT\_PORTS Source) extracts data from `dbo.S_PATHFINDER_CT_PORTS` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CT\_PORTS Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CT_PORTS` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### DFT- D_PATHFINDER_CT_STEEL_INDUSTRIES

*   **Source:** OLE DB Source (S\_PATHFINDER\_CT\_STEEL\_INDUSTRIES Source) extracts data from `dbo.S_PATHFINDER_CT_STEEL_INDUSTRIES` from `STG_PATHFINDER` connection.
*   **Transformations:** None.
*   **Destinations:** OLE DB Destination (D\_PATHFINDER\_CT\_STEEL\_INDUSTRIES Destination) saves successfully mapped rows to `dbo.D_PATHFINDER_CT_STEEL_INDUSTRIES` using the `MART_PATHFINDER` connection.  Error rows are handled by failing the component.

#### ESTL- Truncate And Seed PathFinder Dimensions

*   This task truncates and reseeds the identity of the dimension tables within MART_PATHFINDER.

## 4. Code Extraction

```sql
TRUNCATE TABLE  dbo.[D_PATHFINDER_CBSA_STEEL_CLASSIFICATION];
TRUNCATE TABLE  dbo.[D_PATHFINDER_CBSA_STEEL_COMMODITIES];
TRUNCATE TABLE  dbo.[D_PATHFINDER_CBSA_STEEL_DATA];
TRUNCATE TABLE  dbo.[D_PATHFINDER_CBSA_WHEAT_DATA];
TRUNCATE TABLE  dbo.[D_PATHFINDER_CT_PORTS];
TRUNCATE TABLE  dbo.[D_PATHFINDER_CT_STEEL_INDUSTRIES];


DBCC CHECKIDENT ('dbo.D_PATHFINDER_CBSA_STEEL_CLASSIFICATION', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_CLASSIFICATION ON

insert into [dbo].[D_PATHFINDER_CBSA_STEEL_CLASSIFICATION]	
    (   
		   [CBSA_STEEL_CLASSIFICATION_SID]
      ,[HS_Code]
      ,[Cmdty_Eng_Desc]
      ,[Cmdty_Efctv_Dt]
      ,[Cmdty_Expiry_Dt]
      ,[Steel_Ind_Cd]
      ,[Steel_Ind_Eng_Desc]
      ,[Steel_Ind_Fr_Desc]
      ,[Steel_Ind_Efctv_Dt]
      ,[Steel_Ind_Expiry_Dt]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
    )
VALUES
(
	-3,
	'Uncoded',
	'Uncoded',
	'9999-12-31',
	'9999-12-31',
	-3,
	'Uncoded',
	'Non-codé',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31'
	)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_CLASSIFICATION OFF

DBCC CHECKIDENT ('dbo.D_PATHFINDER_CBSA_STEEL_COMMODITIES', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_COMMODITIES ON

insert into [dbo].[D_PATHFINDER_CBSA_STEEL_COMMODITIES]	
    ( 
	 [CBSA_STEEL_COMMODITIES_SID]
      ,[Cmdty_Cd]
      ,[HS_10_Code]
      ,[Cmdty_Eng_Desc]
      ,[Cmdty_Fr_Desc]
      ,[Cmdty_Efctv_Dt]
      ,[Cmdty_Expiry_Dt]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
)
VALUES
(
	-3,
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Non-codé',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31'
	)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_COMMODITIES OFF

DBCC CHECKIDENT ('dbo.D_PATHFINDER_CBSA_STEEL_DATA', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_DATA ON

insert into [dbo].[D_PATHFINDER_CBSA_STEEL_DATA]	
    ( 
			[CBSA_STEEL_DATA_SID]
      ,[Ext_ID]
      ,[Service_Option]
      ,[Importer_BN]
      ,[Release_Office]
      ,[Importer_Name]
      ,[Exporter_Name]
      ,[Vendor_Name]
      ,[Broker_ID]
      ,[Broker_Name]
      ,[Net_Weight]
      ,[Net_Weight_UOM]
      ,[Gross_Weight]
      ,[Gross_Weight_UOM]
      ,[GIP]
      ,[ID]
      ,[Date_Inserted]
      ,[Transaction_Number]
      ,[Country_Of_Origin]
      ,[Location_Eng_Nm]
      ,[Location_Fr_Nm]
      ,[Release_Date]
      ,[HS_Code]
      ,[HS_Price]
      ,[HS_Weight]
      ,[HS_UOM]
      ,[ActiveYN]
      ,[Updated]
      ,[Date_Updated]
      ,[Note]
      ,[Country_Of_Export]
      ,[State_Of_Export]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
)
VALUES
	(
		-3,
		-3,
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	-3,
	'Uncoded',
	-3,
	'Uncoded',
	-3,
	'Uncoded',
	'z',
	-3,
	'9999-12-31',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'9999-12-31',
	'Uncoded',
	-3,
	-3,
	-3,
	'z',
	'z',
	'9999-12-31',
	'Uncoded',
	'-3',
	'-3',
	'9999-12-31',
	'9999-12-31'
)

SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_STEEL_DATA OFF

DBCC CHECKIDENT ('dbo.D_PATHFINDER_CBSA_WHEAT_DATA', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_WHEAT_DATA ON

insert into [dbo].[D_PATHFINDER_CBSA_WHEAT_DATA]	
    (
			[CBSA_WHEAT_DATA_SID]
      ,[ID]
      ,[Ext_ID]
      ,[Date_Inserted]
      ,[Transaction_Number]
      ,[Country_Of_Origin]
      ,[HS_Code]
      ,[HS_Price]
      ,[HS_Weight]
      ,[HS_UOM]
      ,[Release_Date]
      ,[ActiveYN]
      ,[Updated]
      ,[Date_Updated]
      ,[Note]
      ,[Service_Option]
      ,[Importer_BN]
      ,[Release_Office]
      ,[Importer_Name]
      ,[Exporter_Name]
      ,[Vendor_Name]
      ,[Net_Weight]
      ,[Net_Weight_UOM]
      ,[Gross_Weight]
      ,[Gross_Weight_UOM]
      ,[GIP]
      ,[Location_Id]
      ,[Location_Eng_Nm]
      ,[Location_Fr_Nm]
      ,[ISO_Cd]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
)

VALUES
(
	-3,
	-3,
	-3,
	'9999-12-31',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	-3,
	-3,
	'Uncoded',
	'9999-12-31',
	'z',
	'z',
	'9999-12-31',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	'Uncoded',
	-3,
	'Uncoded',
	-3,
	'Uncoded',
	'z',
	-3,
	'Uncoded',
	'Uncoded',
	'Uncd',
	'9999-12-31',
	'9999-12-31'
)

SET IDENTITY_INSERT dbo.D_PATHFINDER_CBSA_WHEAT_DATA OFF

DBCC CHECKIDENT ('dbo.D_PATHFINDER_CT_PORTS', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CT_PORTS ON

insert into [dbo].[D_PATHFINDER_CT_PORTS]	
    ( [CT_PORTS_SID]
      ,[Release_Office]
      ,[Port_Eng_Desc]
      ,[Port_Fr_Desc]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
	)
VALUES
(
	-3,
	'Uncd',
	'Uncoded',
	'Non-codé',
	'9999-12-31',
	'9999-12-31'
)

SET IDENTITY_INSERT dbo.D_PATHFINDER_CT_PORTS OFF

DBCC CHECKIDENT ('dbo.D_PATHFINDER_CT_STEEL_INDUSTRIES', RESEED, 1)
SET IDENTITY_INSERT dbo.D_PATHFINDER_CT_STEEL_INDUSTRIES ON

insert into [dbo].[D_PATHFINDER_CT_STEEL_INDUSTRIES]	
    ( [STEEL_INDUSTRIES_SID]
      ,[Steel_Ind_Cd]
      ,[Steel_Ind_Eng_Desc]
      ,[Steel_Ind_Fr_Desc]
      ,[Steel_Ind_Efctv_Dt]
      ,[Steel_Ind_Expiry_Dt]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
)

VALUES
(
	-3,
	-3,
	'Uncoded',
	'Non-codé',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31',
	'9999-12-31'
)

SET IDENTITY_INSERT dbo.D_PATHFINDER_CT_STEEL_INDUSTRIES OFF
```

Context: This SQL code is executed in task `ESQLT- Truncate And Seed PathFinder Dimensions` to truncate the dimension tables and insert a default "uncoded" record, which uses surrogate key =-3 and 9999-12-31 as the effecitve and expiry dates.

```sql
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PATHFINDER_Dimension.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: This SQL code is used in the `OnError` event handler to update the ETL run status to 'FAILED'.  It uses subqueries and joins to identify the correct record to update in `ETL_RUN_STATUS`.

```sql
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
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'PATHFINDER_Dimension.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)


;
```

Context: This SQL code is used in the `OnPostExecute` event handler to update the ETL run status to 'SUCCEEDED'. Similar to the `OnError` handler, it uses subqueries and joins to identify the correct record to update in `ETL_RUN_STATUS`.

```sql
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
   AND ETL_SUB_COMPONENT_NM = 'PATHFINDER_Dimension.DTSX'   --'NEICS_Dimension.DTSX'
  )