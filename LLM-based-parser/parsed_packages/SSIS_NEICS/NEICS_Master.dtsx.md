## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_NEICS | OLE DB | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR], Database: @[$Project::PRJ_PRM_TRGT_REPORTING_DB_NM] | Target for data transformations | Integrated Security (SSPI) | @[$Project::PRJ_PRM_TRGT_DB_SRVR], @[$Project::PRJ_PRM_TRGT_REPORTING_DB_NM] | Part 1, 2, 3 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| ODS_NEICS.dtsx |  | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") &#x007C;&#x007C; (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ODS") | Executes ODS package | Part 1, 2, 3|
| NEICS_Staging.dtsx |  | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") | Executes staging package | Part 1, 2, 3|
| NEICS_Dimension.dtsx |  | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "DIMENSION") | Executes dimension package | Part 1, 2, 3|
| NEICS_Fact.dtsx |  | Parent | (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "FACT") | Executes fact package | Part 1, 2, 3|

## 3. Package Flow Analysis

The package begins with an `EXPRESSIONT- Work Flow - Start Task - Each branch depends on value in Project Parameter - Process_Node` task, which evaluates the project parameter `[$Project::PRJ_PRM_PROCESS_NODE]`.  Based on the value of this parameter, different branches of the package are executed. The possible values and corresponding package parts are:

*   **ODS**: Executes `EPKGT-  <SubjectArea> ODS`
*   **STAGING**: Executes `EPKGT-  <SubjectArea> STAGING` with OnError and OnPostExecute event handlers.
*   **DIMENSION**: Executes `EPKGT-  <SubjectArea> DIMENSION`
*   **FACT**: Executes `EPKGT- <SubjectArea> FACT`
*   **MART_NEICS_LIVE**: Executes `MART_NEICS_LIVE`
*   **ALL**: Executes all the above in a sequence: ODS -> STAGING -> Create Staging index -> DIMENSION -> FACT -> MART_NEICS_LIVE -> Execute SQL Task Stored Proc ETL Monitoring

The package includes the following tasks:

*   **Execute Package Tasks (EPKTs)**: Executes child packages (ODS, Staging, Dimension, Fact).
*   **Execute SQL Tasks (ESQLTs)**: Executes SQL statements for creating indexes and executing stored procedures.
*   **Expression Tasks**: Used to evaluate expressions and start the workflow.

There are OnError and OnPostExecute event handlers at package level and for the "Staging" package execution task.

## 4. Code Extraction

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_MASTER_RUN_STATUS
INSERT INTO [ETL_RUN_STATUS]
           ([ETL_COMPONENT_ID]           
           ,[ETL_RUN_STATUS_DESC]
 
          ,[ETL_RUN_MAIN_COMPONENT_IND]
           ,[ETL_RUN_RECORD_CREA_DT]
           ,[ETL_RUN_RECORD_UPDT_DT])
    
 VALUES
           (
     (select ETL_COMPONENT_ID  from ETL_COMPONENT where ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX' and ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS') 
          
           ,'RUNNING'
           ,1
           ,GETDATE()
           ,GETDATE()
     )
;
```

Context: This SQL query inserts a record into the `ETL_RUN_STATUS` table to indicate that the master package is running.

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_MASTER
UPDATE ETL_RUN_STATUS 

    SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
, [ETL_RUN_RECORD_UPDT_DT] = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
  
    (
SELECT ETL_RUN_STATUS_ID
  
       FROM ETL_RUN_STATUS R
  
      WHERE R.ETL_COMPONENT_ID = 

            (
SELECT ETL_COMPONENT_ID

               FROM ETL_COMPONENT
                                
              WHERE 
ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'  
                AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS')
   
    AND ETL_RUN_STATUS_DESC = 'RUNNING'
   
    AND ETL_RUN_MAIN_COMPONENT_IND = 1
)
;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to mark any previous running instance of the master package as "TERMINATED BY RERUN".

```sql
-- From User::V_SQL_INSERT_ON_PRE_EXECUTE_TERMINATE_SUB_COMPONENTS

UPDATE ETL_RUN_STATUS

    SET ETL_RUN_STATUS_DESC = 'TERMINATED BY RERUN'
, ETL_RUN_RECORD_UPDT_DT = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
    

(-- First Bracket Start
                

      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
   
         SELECT ETL_SUB_COMPONENT_ID
                
           FROM ETL_SUB_COMPONENT
                
          WHERE ETL_COMPONENT_ID IN 

            (
SELECT ETL_COMPONENT_ID
        
               FROM ETL_COMPONENT
                
              WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'
                                                                                
                AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)

            AND ETL_SUB_COMPONENT_NM = 'ODS_NEICS.dtsx'    -- 'ODS_NEICS.DTSX'
			)
                                
            AND ETL_COMPONENT_ID IN 

                (
SELECT ETL_COMPONENT_ID
                
                   FROM ETL_COMPONENT
                                
                  WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'

                    AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)

            AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
            AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
UNION
              
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
       (SELECT ETL_SUB_COMPONENT_ID
                
          FROM ETL_SUB_COMPONENT
                                                
         WHERE ETL_COMPONENT_ID IN 
         
(
SELECT ETL_COMPONENT_ID
                
              FROM ETL_COMPONENT

             WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'

                       AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS')

           AND ETL_SUB_COMPONENT_NM = 'NEICS_Staging.dtsx'    -- 'NEICS_STAGING.DTSX'
		   )
-- Second Bracket
           AND ETL_COMPONENT_ID IN 

               (
SELECT ETL_COMPONENT_ID

                  FROM ETL_COMPONENT

                 WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'

                   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)

           AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
           AND ETL_RUN_MAIN_COMPONENT_IND = 0
  
 
UNION
                                
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
   
        SELECT ETL_SUB_COMPONENT_ID
                
          FROM ETL_SUB_COMPONENT
                
         WHERE ETL_COMPONENT_ID IN 

           (
SELECT ETL_COMPONENT_ID
        
              FROM ETL_COMPONENT
                
             WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'
                                                                                
               AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)

           AND ETL_SUB_COMPONENT_NM = 'NEICS_Dimension.dtsx'    -- 'NEICS_DIMENSION.DTSX'
		   )                -- Second Bracket             
           AND ETL_COMPONENT_ID IN 

                 (
SELECT ETL_COMPONENT_ID
                
                    FROM ETL_COMPONENT
                                
                   WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'

                     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS')

           AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
           AND ETL_RUN_MAIN_COMPONENT_IND = 0

                  
UNION

                
      SELECT ETL_RUN_STATUS_ID
                
        FROM ETL_RUN_STATUS
                
       WHERE ETL_SUB_COMPONENT_ID IN 
                                
       (-- Second Bracket Start
                                                
        SELECT ETL_SUB_COMPONENT_ID
                                                
          FROM ETL_SUB_COMPONENT
                                                
         WHERE ETL_COMPONENT_ID IN 

           (
SELECT ETL_COMPONENT_ID
                                                                                
              FROM ETL_COMPONENT
                                                                                
             WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'
                                                                                
               AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)
                                
               AND ETL_SUB_COMPONENT_NM = 'NEICS_Fact.dtsx'    -- 'NEICS_FACT.DTSX' 
)                -- Second Bracket End    
           AND ETL_COMPONENT_ID IN 

                                       (
SELECT ETL_COMPONENT_ID
                                
                                  FROM ETL_COMPONENT
                                
                                 WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'

                                   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)
                                
        AND ETL_RUN_STATUS_DESC = 'RUNNING'
                                
        AND ETL_RUN_MAIN_COMPONENT_IND = 0


    )   -- First Bracket End
;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to mark any running instances of the sub-components (child packages) as "TERMINATED BY RERUN".

```sql
-- From User::V_SQL_UPDATE_ON_ERROR
UPDATE ETL_RUN_STATUS
SET ETL_RUN_STATUS_DESC = 'FAILED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()
WHERE ETL_RUN_STATUS_ID IN (
  SELECT max(ETL_RUN_STATUS_ID)
  FROM ETL_RUN_STATUS R
  WHERE R.ETL_COMPONENT_ID = (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
    )
   AND ETL_RUN_STATUS_DESC = 'RUNNING'
   AND ETL_RUN_MAIN_COMPONENT_IND = 1
   AND ETL_SUB_COMPONENT_ID IS NULL
  )
  
  ;
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to mark the master package as "FAILED" in case of an error.

```sql
-- From User::V_SQL_UPDATE_ON_POST_EXECUTE
UPDATE ETL_RUN_STATUS

    SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,[ETL_RUN_RECORD_UPDT_DT] = GETDATE()

  WHERE ETL_RUN_STATUS_ID IN 
   (
SELECT max(etl_run_status_id)
  
      FROM ETL_RUN_STATUS R
  
     WHERE R.ETL_COMPONENT_ID = 
     (
SELECT ETL_COMPONENT_ID
    
        FROM ETL_COMPONENT
    
       WHERE ETL_COMPONENT_NM = 'NEICS_MASTER.DTSX'
    
         AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/NEICS'
)
   
       AND ETL_RUN_STATUS_DESC = 'RUNNING'
   
       AND ETL_RUN_MAIN_COMPONENT_IND = 1
   
       AND ETL_SUB_COMPONENT_ID IS NULL
);
```

Context: This SQL query updates the `ETL_RUN_STATUS` table to mark the master package as "SUCCEEDED" after successful execution.

```sql
-- From Execute SQL Task Create DIM Indexes
CREATE INDEX i_D_EICS_ACCOUNTS ON [MART_NEICS].[DBO].[D_EICS_ACCOUNTS]
(ACCT_ID, CONTROL_ITEM_ID, BUS_ID );

CREATE INDEX i_D_EICS_BUSINESS_PAYMENTS ON [MART_NEICS].[DBO].[D_EICS_BUSINESS_PAYMENTS]
(BUS_PYMNT_ID);

CREATE INDEX i_D_EICS_BUSINESSES ON [MART_NEICS].[DBO].[D_EICS_BUSINESSES]
(BUS_ID);

CREATE INDEX [i_D_EICS_BUSINESSES_2] ON [MART_NEICS].[DBO].[D_EICS_BUSINESSES]
(EICB_NO);

CREATE INDEX i_D_EICS_COMMODITY ON [MART_NEICS].[DBO].[D_EICS_COMMODITY]
(LVL6_CMDTY_ID);

CREATE INDEX i_D_EICS_CONTROL_ITEMS ON [MART_NEICS].[DBO].D_EICS_CONTROL_ITEMS
(LVL6_CONTROL_ITEM_ID, LVL6_LOCATION_ID, LVL6_CONTROL_ITEM_EFCTV_DT,  LVL6_CONTROL_ITEM_EXPIRY_DT);

CREATE INDEX [i_D_EICS_DATE_2] ON [MART_NEICS].[DBO].[D_EICS_DATE]
(DATE_ID);

CREATE INDEX i_D_EICS_DATE ON [MART_NEICS].[DBO].[D_EICS_DATE]
(DAY_ID);

CREATE INDEX i_D_EICS_EDI_TRANSACTION_ITEMS ON [MART_NEICS].[DBO].[D_EICS_EDI_TRANSACTION_ITEMS]
(EDI_TRANS_ID , PRMT_APLCTN_ID, PRMT_ID);

CREATE INDEX i_D_EICS_FINANCIAL_INVOICE_ITEMS ON [MART_NEICS].[DBO].[D_EICS_FINANCIAL_INVOICE_ITEMS]
(FIN_INVC_ID, PRMT_ITEM_ID , PRMT_APLCTN_ID);

CREATE INDEX i_D_EICS_FINANCIAL_INVOICES ON [MART_NEICS].[DBO].[D_EICS_FINANCIAL_INVOICES]
(FIN_INVC_ID, BUS_ID, FIN_INVC_DT );

CREATE INDEX i_D_EICS_LOCATIONS ON [MART_NEICS].[DBO].[D_EICS_LOCATIONS]
(LOCATION_ID );

CREATE INDEX i_D_EICS_PERMIT_APPLICATIONS ON [MART_NEICS].[DBO].[D_EICS_PERMIT_APPLICATIONS]
(PRMT_APLCTN_ID , CDN_ENTRY_EXIT_PORT_ID, EXP_IMP_ID , APLCNT_ID , CDN_ENTRY_EXIT_DT );

CREATE INDEX [i_D_EICS_PERMIT_APPLICATIONS_2] ON [MART_NEICS].[DBO].[D_EICS_PERMIT_APPLICATIONS]
(PRMT_APLCTN_ID, CDN_ENTRY_EXIT_DT , EXP_IMP_ID, BUS_PYMNT_ID, APLCNT_ID);

CREATE INDEX i_D_EICS_PERMIT_EXPORTS ON [MART_NEICS].[DBO].[D_EICS_PERMIT_EXPORTS]
(PRMT_ITEM_ID);

CREATE INDEX i_D_EICS_PERMIT_ITEMS ON [MART_NEICS].[DBO].[D_EICS_PERMIT_ITEMS]
(PRMT_ITEM_ID, PRMT_APLCTN_ID, COMMODITY_ID, CONTROL_ITEM_ID, THIRD_PARTY_LINK_ID, SHIPMENT_DATE);

CREATE INDEX i_D_EICS_PERMITS ON [MART_NEICS].[DBO].[D_EICS_PERMITS]
(PRMT_ID);

CREATE INDEX [i_D_EICS_PERMITS_2] ON [MART_NEICS].[DBO].[D_EICS_PERMITS]
(PRMT_APLCTN_ID, PRMT_EFCTV_DT , PRMT_EXPIRY_DT);

CREATE INDEX i_D_EICS_THIRD_PARTIES ON [MART_NEICS].[DBO].[D_EICS_THIRD_PARTIES]
(Third_Party_Link_Id);

CREATE INDEX i_D_EICS_TRANSFERS ON [MART_NEICS].[DBO].[D_EICS_TRANSFERS]
(TRANSFER_ID, SOURCE_ACCT_ID, TARGET_ACCT_ID, PRMT_ID,  PRMT_ITEM_ID, TRANSFER_EFCTV_DT);

CREATE INDEX i_D_EICS_User ON [MART_NEICS].[DBO].[D_EICS_User]
(User_Id);

CREATE INDEX i_D_EICS_USER_COMMODITIES_LOCATIONS ON [MART_NEICS].[DBO].[D_EICS_USER_COMMODITIES_LOCATIONS]
(User_Id, CMDTY_ID , LOCATION_ID);

CREATE INDEX i_D_EICS_WORKFLOW ON [MART_NEICS].[DBO].[D_EICS_WORKFLOW]
(Prmt_Aplctn_Id, Transfer_Id, EICB_No  );

CREATE INDEX i_D_EXCOL_ACTIVITY ON [MART_NEICS].[DBO].[D_EXCOL_ACTIVITY]
(ActivityID, EPEObjectID );

CREATE INDEX i_D_EXCOL_BCLogs_EP_SummaryOfScale_UNION ON [MART_NEICS].[DBO].[D_EXCOL_BCLogs_EP_SummaryOfScale_UNION]
(ItemAdvertiseBCLogsID, Item );

CREATE INDEX i_D_EXCOL_BCLogsEPSummaryOfScale ON [MART_NEICS].[DBO].[D_EXCOL_BCLogsEPSummaryOfScale]
(ItemAdvertiseBCLogsID, LogItemID, EPEObjectID );

CREATE INDEX i_D_EXCOL_CLIENT ON [MART_NEICS].[DBO].[D_EXCOL_CLIENT]
(ClientID );

CREATE INDEX i_D_EXCOL_CLIENT_USER_ASSIGNMENTROLE ON [MART_NEICS].[DBO].[D_EXCOL_CLIENT_USER_ASSIGNMENTROLE]
(ClientID, UserID );

CREATE INDEX i_D_EXCOL_CONSULTATIONS ON [MART_NEICS].[DBO].[D_EXCOL_CONSULTATIONS]
(ConsultationGroupID, EPEObjectID);

CREATE INDEX i_D_EXCOL_CONSULTEE ON [MART_NEICS].[DBO].[D_EXCOL_CONSULTEE]
(ConsultationGroupID);

CREATE INDEX i_D_EXCOL_COUNTRY ON [MART_NEICS].[DBO].[D_EXCOL_COUNTRY]
(CountryID);

CREATE INDEX i_D_EXCOL_DOCUMENT ON [MART_NEICS].[DBO].[D_EXCOL_DOCUMENT]
(EPEObjectID, ActivityID, SubmittedByUserID, DistributedDate , CreatedDate , ReceivedDate );

CREATE INDEX i_D_EXCOL_ECLASSESSMENT ON [MART_NEICS].[DBO].[D_EXCOL_ECLASSESSMENT]
(ECLAssessmentID, EPEObjectID);

CREATE INDEX [i_D_EXCOL_EPEOBJECT_2] ON [MART_NEICS].[DBO].[D_EXCOL_EPEOBJECT]
(ReviewAAID, EPEObjectDetailID, ItemAdvertiseBCLogsID);

CREATE INDEX i_D_EXCOL_EPEOBJECT ON [MART_NEICS].[DBO].[D_EXCOL_EPEOBJECT]
(EPEObjectID,  EPEObjectDetailID, ReviewID, ReviewAAID, ClientID, SubmitDate);

CREATE INDEX i_D_EXCOL_EPEOBJECT_CRITERIA_CONDITION ON [MART_NEICS].[DBO].[D_EXCOL_EPEOBJECT_CRITERIA_CONDITION]
(EPEObjectCriteriaConditionID);

CREATE INDEX i_D_EXCOL_EPEOBJECT_DETAILS ON [MART_NEICS].[DBO].[D_EXCOL_EPEOBJECT_DETAILS]
(EPEObjectDetailID);

CREATE INDEX i_D_EXCOL_EPEOBJECTCONTACT ON [MART_NEICS].[DBO].[D_EXCOL_EPEOBJECTCONTACT]
(EPEObjectID, EPEContactTypeCode, SeqNo);

CREATE INDEX i_D_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT ON [MART_NEICS].[DBO].[D_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT]
(FirearmItemECLSelfAssessmentID, ItemID);

CREATE INDEX i_D_EXCOL_ITEM ON [MART_NEICS].[DBO].[D_EXCOL_ITEM]
(ItemID, LogCorrespondingAAEPEObjectID, EPEObjectID);

CREATE INDEX [i_D_EXCOL_ITEM_2] ON [MART_NEICS].[DBO].[D_EXCOL_ITEM]
(ItemID, EPEObjectID, CountryOfOriginID);

CREATE INDEX i_D_EXCOL_ITEM_ADVERTISE_BCLogs ON [MART_NEICS].[DBO].[D_EXCOL_ITEM_ADVERTISE_BCLogs]
(ItemAdvertiseBCLogsID);

CREATE INDEX i_D_EXCOL_REVIEW ON [MART_NEICS].[DBO].[D_EXCOL_REVIEW]
(ReviewID);

CREATE INDEX i_D_EXCOL_REVIEWAA ON [MART_NEICS].[DBO].[D_EXCOL_REVIEWAA]
(ReviewAAID, AdvertiseListDate);

CREATE INDEX i_D_EXCOL_USER ON [MART_NEICS].[DBO].[D_EXCOL_USER]
(UserID);

CREATE INDEX i_D_EXCOL_WORKFLOW ON [MART_NEICS].[DBO].[D_EXCOL_WORKFLOW]
(EPE_Object_ID);
```

Context: This SQL script creates indexes on various dimension tables within the `MART_NEICS` database. This task is disabled.

```sql
-- From Execute SQL Task Create Staging Indexes

CREATE INDEX i_S_EICS_CONTROL_ITEMS ON [STG_NEICS].[DBO].[S_EICS_CONTROL_ITEMS]
(CONTROL_ITEM_ID);

CREATE INDEX i_S_EICS_PERMIT_APPLICATIONS ON [STG_NEICS].[DBO].[S_EICS_PERMIT_APPLICATIONS]
(PRMT_APLCTN_ID);

CREATE INDEX i_S_EICS_PERMIT_ITEMS ON [STG_NEICS].[DBO].[S_EICS_PERMIT_ITEMS]
(PRMT_ITEM_ID);

CREATE INDEX [i_S_EICS_PERMIT_ITEMS_2] ON [STG_NEICS].[DBO].[S_EICS_PERMIT_ITEMS]
(CONTROL_ITEM_ID);
```

Context: This SQL script creates indexes on various staging tables within the `STG_NEICS` database.

```sql
-- From Execute SQL Task Stored Proc ETL Monitoring
exec stg_neics.dbo.sp_qa_NEICS_etl;
```

Context: This SQL statement executes a stored procedure `sp_qa_NEICS_etl` within the `stg_neics.dbo` schema.

```sql
-- From MART_NEICS_LIVE
IF DB_ID( 'MART_NEICS_LIVE' ) IS NOT NULL
                DROP DATABASE [MART_NEICS_LIVE] 

CREATE DATABASE [MART_NEICS_LIVE] ON 
( NAME = N'NEICS_REPORTING', FILENAME = N'E:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\MART_NEICS_LIVE.ss1' ) 
                AS SNAPSHOT OF MART_NEICS
```

Context: This SQL statement creates a database snapshot of the `MART_NEICS` database named `MART_NEICS_LIVE`. This task is disabled.

## 5. Output Analysis

| Destination Table | Description | Source Part |
|--------------------------|------------------------------------|-------------|
| ETL_RUN_STATUS | Stores the status of ETL components (packages) | Event Handlers |

## 6. Package Summary

*   **Input Connections:** 1
*   **Output Destinations:** `ETL_RUN_STATUS`
*   **Package Dependencies:** 4
*   **Activities:**
    *   Execute Package Tasks: 4
    *   Execute SQL Tasks: 6
    *   Expression Tasks: 2
*   **Overall package complexity assessment:** Medium
*   **Potential performance bottlenecks:** The execution of child packages and index creation could be a bottleneck.
*   **Critical path analysis:** The critical path depends on the value of the `[$Project::PRJ_PRM_PROCESS_NODE]` parameter.
*   **Error handling mechanisms:** The package includes OnError event handlers at both the package level and for the staging package execution. Status updates to the ETL_RUN_STATUS table are used for logging. The package also has pre-execution event handlers to terminate hung jobs.
