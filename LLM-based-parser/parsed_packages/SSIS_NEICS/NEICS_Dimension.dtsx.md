## Consolidated SSIS Package Analysis Report

## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                               | Purpose                                                                                                                                | Security Requirements                                                                                                                            | Parameters/Variables                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Source Part |
|---------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| MART_NEICS                | OLE DB          | `Data Source=[Project::PRJ_PRM_TRGT_DB_SRVR];Initial Catalog=[Project::PRM_TRGT_REPORTING_DB_NM];...` or  `Server=*; Database=[dbo]` or `Server=<*MART Server*>;Database=<*MART Database*>; Integrated Security=SSPI` | Target database for dimension tables (D_*).                                                                                                | Integrated Security (SSPI) implies Windows Authentication. The user executing the package needs access to the target SQL Server instance. Credentials for accessing MART_NEICS.  | `[Project::PRJ_PRM_TRGT_DB_SRVR]`, `[Project::PRJ_PRM_TRGT_REPORTING_DB_NM]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Part 1, 2, 3 |
| STG_NEICS                 | OLE DB          | `Data Source=[Project::PRJ_PRM_SRC_DB_SRVR];Initial Catalog=[Project::PRM_TRGT_STAGING_DB_NM];...` or `Server=*; Database=[dbo]` or `Server=<*STG Server*>;Database=<*STG Database*>; Integrated Security=SSPI` | Staging database for source data (S_*).                                                                                                 | Integrated Security (SSPI) implies Windows Authentication. The user executing the package needs access to the staging SQL Server instance. Credentials for accessing STG_NEICS. | `[Project::PRJ_PRM_SRC_DB_SRVR]`, `[Project::PRM_TRGT_STAGING_DB_NM]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Part 1, 2, 3 |
| STG_NEICS 1               | OLE DB          | `Data Source=[Project::PRM_SRC_DB_SRVR];Initial Catalog=[Project::PRM_TRGT_STAGING_DB_NM];...`                               | Likely another connection to the staging database. Possible use in lookup or other transformation.                                        | Integrated Security (SSPI) implies Windows Authentication. The user executing the package needs access to the staging SQL Server instance.  | `[Project::PRJ_PRM_SRC_DB_SRVR]`, `[Project::PRM_TRGT_STAGING_DB_NM]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Part 1         |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes                               | Source Part |
|-----------------------|-------------------|--------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found           |                   |                          |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3 |

## 3. Package Flow Analysis

The overall package flow truncates and loads dimension tables from staging to the data warehouse.

*   The package starts with an `Expression Task` named `Dimensions - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` which always succeeds.
*   The core logic resides within the `SEQC-Truncate Dimension Tables` Sequence Container, which contains numerous Data Flow Tasks.
*   A second Sequence Container `Load D_EXCOL_BAD_STANDING after ITEMS and EPEObject DIMS are loaded` loads data into `D_EXCOL_BADSTANDING`.

#### SEQC-Truncate Dimension Tables

*   This sequence container truncates and loads dimensions into the MART_NEICS database.

#### Data Flow Tasks within `SEQC-Truncate Dimension Tables`

*   Each DFT generally follows a pattern: OLE DB Source (STG_NEICS) extracts data from `dbo.S_*` staging table, and OLE DB Destination (MART_NEICS) loads data into `dbo.D_*` dimension table.
*   Examples include: `D_EICS_ BUSINESS_PAYMENTS`, `D_EICS_ PERMIT_EXPORTS`, `D_EICS_ PERMIT_IMPORTS`, `D_EICS_ACCOUNTS`, `D_EICS_BUSINESSES`, `D_EICS_BUSINESS_ADDRESSES`, `D_EICS_BUSINESS_COMMENTS`, `D_EICS_BUSINESS_CONTACTS`, `D_EICS_BUSINESS_RIGHTS`, `D_EICS_BUSINESS_SUSPENSIONS`, `D_EICS_COMMODITY`, `D_EICS_COMMODITY_CONVERSION`, `D_EICS_Commodity_Location_Conversions`, `D_EICS_COMMODITY_UNITS`, `D_EICS_EDI_TRANSACTIONS`, `D_EICS_EDI_TRANSACTION_ITEMS`, `D_EICS_FINANCIAL_INVOICES`, `D_EICS_FINANCIAL_INVOICE_ITEMS`, `D_EICS_FOREIGN_LICENSES`, `D_EICS_LOCATIONS`, `D_EICS_PERMITS`, `D_EICS_PERMIT_APPLICATIONS`, `D_EICS_PERMIT_ITEMS`, `D_EICS_SECTOR`, `D_EICS_SWLSLA_DATA`, `D_EICS_THIRD_PARTIES`, `D_EICS_USER`, `D_EICS_USER_COMMODITIES_LOCATIONS`, `D_EXCOL_ACTIVITY`, `D_EXCOL_ASSESSMENT`, `D_EXCOL_BADSTANDING_PRE_LOAD`, `D_EXCOL_BCLogsEPSummaryOfScale`, `D_EXCOL_BCLogsSurplusOfferToPurchase`, `D_EXCOL_BCLogs_EP_SummaryOfScale_UNION`, `D_EXCOL_CLIENT`, `D_EXCOL_CLIENT_USER_ASSIGNMENTROLE`, `D_EXCOL_Consultations`, `D_EXCOL_ECLASSESSMENT`, `D_EXCOL_ECL_SELF_ASSESSMENT`, `D_EXCOL_EPEOBJECT`, `D_EXCOL_EPEOBJECTCONTACT`, `D_EXCOL_EPEOBJECT_CRITERIA_CONDITION`, `D_EXCOL_EPEOBJECT_DETAILS`,  `D_EXCOL_EPEOBJECT_STATUS_HISTORY`, `D_EXCOL_EVENTHISTORY`,  `D_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT`, `D_EXCOL_ITEM`, `D_EXCOL_ITEM_ADVERTISE_BCLogs`, `D_EXCOL_LOCATION`, `D_EXCOL_MANAGEMENT_APPROVAL`, `D_EXCOL_PERMIT_UTILIZATION`, `D_EXCOL_PRELIMINARY_ANALYSIS`, `D_EXCOL_RAFCOUNTRYPROFILEANDBIRELATION`, `D_EXCOL_RAFDIVERSIONRISK`, `D_EXCOL_RAFENDUSERVERIFICATION`, `D_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT`, `D_EXCOL_RAFGBVIOLENCEAGAINSTVGRISK`, `D_EXCOL_RAFHRANDHUMANITARIANLAWRISK`, `D_EXCOL_RAFNATIONALSECURITYRISK`, `D_EXCOL_RAFOVERALLRISKASSESSMENT`, `D_EXCOL_RAFPEACEANDSECURITYRISK`, `D_EXCOL_RAFSANCTIONCOMPLIANCE`, `D_EXCOL_RAFTERRORISMANDORGANIZEDCRIMERISK`, `D_EXCOL_REVIEW`, `D_EXCOL_REVIEWAA`, `D_EXCOL_TRANSFERS`, `D_EXCOL_USER`, `D_EXCOL_USERROLE`, `D_EXCOL_USER_NOTIFICATION`, `D_EXCOL_WORST_OVERDUE_CONDITION`.
*   Most data flows involve a direct data movement from source to destination with minimal transformations.
*   `D_EXCOL_ASSESSMENT` contains an explicit "Data Conversion" component to change data types of columns `DRV_ECL_List` and `RANKED_ECL_GROUP` to string (DT_STR).
*   Some queries for the source use the STUFF and FOR XML PATH to concatenate rows into a single column.

#### Load D_EXCOL_BAD_STANDING after ITEMS and EPEObject DIMS are loaded

*   **Truncate And Seed BadStanding Dimension:** Executes a SQL script to truncate the `[dbo].[D_EXCOL_BADSTANDING]` table and seed it with a default "Uncoded" row.
*   **D_EXCOL_BADSTANDING:** A `Data Flow Task` that loads data into `[dbo].[D_EXCOL_BADSTANDING]` from `[dbo].[D_EXCOL_BADSTANDING_PRE_DIM_LOAD]`.

#### Precedence Constraints

*   Inside the `Load D_EXCOL_BAD_STANDING after ITEMS and EPEObject DIMS are loaded` Sequence Container, the `D_EXCOL_BADSTANDING` Data Flow Task executes after the successful completion of the `Truncate And Seed BadStanding Dimension` task.

#### Error Handling

*   OLE DB Source and Destination components have error outputs configured, but the handling of these outputs is not clear from the provided XML snippets.  The default behavior is to fail the component.

## 4. Code Extraction

```sql
-- SQL Query for D_EICS_FINANCIAL_INVOICES Source
SELECT
       [Fin_Invc_Id]
      ,[Bus_Id]
      ,[Fin_Invc_Dt]
      ,[SWL_Ind]
      ,[Audit_User_Id]
      ,[Audit_Tmstmp]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
  FROM [dbo].[S_EICS_FINANCIAL_INVOICES]
```

```sql
-- SQL Query for D_EXCOL_EPEOBJECT Source

with cte
as
(
SELECT -- 389251
      [EPEObjectID]
      ,[RootEPEObjectID]
      ,[ParentEPEObjectID]
      ,[EPEObjectRefNo]
      ,[EPEObjectTypeID]
      ,[EPEObjectType_Desc_En]
      ,[EPEObjectType_Desc_Fr]
      ,[EPEObjectStatusID]
      ,[EPEObjectStatus_Desc_En]
      ,[EPEObjectStatus_Desc_Fr]
      ,[EPEObjectNewStatusID]
      ,[EPEObjectNewStatus_Desc_En]
      ,[EPEObjectNewStatus_Desc_Fr]
      ,[EPEObjectStatusChangedDate]
      ,[EPEObjectStatusChangedReasonID]
      ,[EPEObjectStatusChangedComment]
      ,[SavedOnceYN]
      ,[EditableYN]
      ,[PermitRequiedYN]
      ,[IssueDate]
      ,[ReIssueDate]
      ,[ExpiryDate]
      ,[EffectiveDate]
      ,[SubmitDate]
      ,[CreatedDate]
      ,[CreatedUserID]
      ,[SubmittedByUserName]
      ,[SessionID]
      ,[VersionNo]
      ,[AmendmentVersionNo]
      ,[ClientID]
      ,[ReviewID]
      ,[ReviewAAID]
      ,[ItemAdvertiseBCLogsID]
      ,[PermitCertificateNo]
      ,[EPEObjectDetailID]
      ,[DistributionID]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
      ,[InternalOpenRead]
      ,[ExternalOpenRead]
      ,[IsActiveObject]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
	  ,[PRELIMINARYANALYSISID]
	  ,[Duration]
	  ,[DecisionNotificationDate]
	   ,[CBSADetentionID]
	  ,[CBSADetentionAssessmentID]
	  ,[MessageToApplicant]
                  ,[OriginalExpiryDate]
  FROM [dbo].[S_EXCOL_EPEOBJECT]
  ),
  cte2
  as 
  (SELECT distinct 
		EPepeobject.[EPEObjectID]
		,DRV_Permit_Certificates_AtoA = STUFF ((Select distinct ',' +  PermitCertificateNo 
				from [dbo].[S_EXCOL_EPEOBJECT] as EPepeobject2
				where EPepeobject2.EPEObjectID = EPepeobject.EPEObjectID 
				FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')

FROM [dbo].[S_EXCOL_EPEOBJECT] AAepeobject
inner join [dbo].[S_EXCOL_ITEM] item -- AA object to its corresponding Permit items
              on AAepeobject.EPEObjectID = item.LogCorrespondingAAEPEObjectID 
inner join [dbo].[S_EXCOL_EPEOBJECT] EPepeobject -- Permit Items to their Permit object
              on item.EPEObjectID = EPepeobject.EPEObjectID
inner join [dbo].[S_EXCOL_ITEM_ADVERTISE_BCLogs] advertiseBClogs
             on AAepeobject.ItemAdvertiseBCLogsID = advertiseBClogs.ItemAdvertiseBCLogsID
	)
  select cte.     [EPEObjectID]
      ,[RootEPEObjectID]
      ,[ParentEPEObjectID]
      ,[EPEObjectRefNo]
      ,[EPEObjectTypeID]
      ,[EPEObjectType_Desc_En]
      ,[EPEObjectType_Desc_Fr]
      ,[EPEObjectStatusID]
      ,[EPEObjectStatus_Desc_En]
      ,[EPEObjectStatus_Desc_Fr]
      ,[EPEObjectNewStatusID]
      ,[EPEObjectNewStatus_Desc_En]
      ,[EPEObjectNewStatus_Desc_Fr]
      ,[EPEObjectStatusChangedDate]
      ,[EPEObjectStatusChangedReasonID]
      ,[EPEObjectStatusChangedComment]
      ,[SavedOnceYN]
      ,[EditableYN]
      ,[PermitRequiedYN]
      ,[IssueDate]
      ,[ReIssueDate]
      ,[ExpiryDate]
      ,[EffectiveDate]
      ,[SubmitDate]
      ,[CreatedDate]
      ,[CreatedUserID]
      ,[SubmittedByUserName]
      ,[SessionID]
      ,[VersionNo]
      ,[AmendmentVersionNo]
      ,[ClientID]
      ,[ReviewID]
      ,[ReviewAAID]
      ,[ItemAdvertiseBCLogsID]
      ,[PermitCertificateNo]
      ,[EPEObjectDetailID]
      ,[DistributionID]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
      ,[InternalOpenRead]
      ,[ExternalOpenRead]
      ,[IsActiveObject]
	  ,DRV_Permit_Certificates_AtoA
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
	  ,[PRELIMINARYANALYSISID]
	  ,[Duration]
	  ,[DecisionNotificationDate]
	  ,[CBSADetentionID]
	  ,[CBSADetentionAssessmentID]
	  ,[MessageToApplicant]
                  ,[OriginalExpiryDate]
  from cte
  left outer join cte2 on cte.EPEObjectID = cte2.EPEObjectID ;
```

```sql
-- SQL Query for D_EICS_PERMIT_APPLICATIONS Source

SELECT p.[PRMT_APLCTN_ID]
      ,isnull(p.[CDN_ENTRY_EXIT_PORT_ID], -3) as CDN_ENTRY_EXIT_PORT_ID
      ,p.[CDN_ENTRY_EXIT_DT]
      ,p.[APLCNT_ID]
      ,p.[EXP_IMP_ID]
      ,p.[PYMNT_TYPE_CD] as BUS_PYMNT_ID
      ,p.[PRMT_APLCTN_SUBMIT_DT]
      ,p.[APLCNT_REF_NO]
      ,p.[APLCTN_STTS_CD]
      ,p.[APLCTN_STTS_DESC_EN]
      ,p.[APLCTN_STTS_DESC_FR]
      ,p.[PRMT_DLVRY_TARGET_CD]
      ,p.[DISTR_MODE_CD]
	  ,p.DISTR_MODE_DESC_EN
	  ,p.DISTR_MODE_DESC_FR
	  ,p.DISTR_MODE_EFFECTIVE_DT
	  ,p.DISTR_MODE_EXPIRY_DT
      ,p.[DISTR_DETAILS_TXT]
      ,p.[BRKR_OUTPOST_NO]
      ,p.[CCRA_TRANS_NO]
      ,p.[APLCNT_COMMENT_TXT]
      ,p.[PRINT_APLCNT_COMMENT_IND]
      ,p.[EXP_IMP_IND]
      ,p.[LANG_IND]
      ,p.[RETROACTIVE_IND]
      ,p.[DOC_LINK_ID]
      ,p.[REASON_LINK_ID]
      ,p.[LAST_PREFDEFINED_REASON_ID]
      ,p.[LAST_PREFDEFINED_REASON_DESC_EN]
      ,p.[LAST_PREFDEFINED_REASON_DESC_FR]
      ,p.[THIRD_PARTY_LINK_ID]
      ,p.[ORIGINAL_PRMT_APLCTN_ID]
      ,p.[SENSITIVE_GOODS_IND]
      ,p.[EPE_MULTIPLE_SHPMNT_IND]
      ,p.[EPE_TEMP_EXP_IND]
      ,p.[PRMT_EFCTV_DT]
      ,p.[PRMT_EXPIRY_DT]
      ,p.[AUDIT_USER_ID]
      ,p.[AUDIT_TMSTMP]
      ,p.[APLCTN_USER_ID]
	  ,Case when W.[Prmt_Aplctn_Id] is NULL Then 0 
			Else 1 
			End AS ROUTED_APPLICATION_IND 
      ,p.[ETL_CREA_DT]
      ,p.[ETL_UPDT_DT]
FROM [dbo].[S_EICS_PERMIT_APPLICATIONS] p
left outer join dbo.S_EICS_WORKFLOW W 
on P.[PRMT_APLCTN_ID] = W.[Prmt_Aplctn_Id]
and w.[Workflow_Id]  = (
			select MAX(w2.[Workflow_Id])
                	from [dbo].[S_EICS_WORKFLOW] w2
			WHERE w.[PRMT_APLCTN_ID] = w2.[PRMT_APLCTN_ID]
			)
```

```sql
-- SQL Query for D_EXCOL_SWLSLA_DATA Source

SELECT [PeriodId], [Period_Start_Date], [Period_End_Date], [priceVl]
     , MAX(CASE WHEN [OPTA_IND] = 1 THEN [euscVl]  END) EUSC
     , MAX(CASE WHEN [OPTA_IND] = 0 THEN [euscVl]  END) AEUSC
	 ,[ETL_CREA_DT]
	,[ETL_UPDT_DT]
  FROM  [dbo].[S_EICS_SWLSLA_DATA]
  group by [PeriodId],[Period_Start_Date], [Period_End_Date], [priceVl]
			,[ETL_CREA_DT] ,[ETL_UPDT_DT]
```

```sql
-- SQL Query for D_EXCOL_ECLASSESSMENT Source

with cte
as
(
SELECT 
		ecl1.[ECLAssessmentID]
      ,ecl1.[AssessmentID]
      ,ecl1.[EPEObjectID]
      ,ecl1.[Assessment_ECL]
      ,ecl1.[Assessment_Note]
      ,ecl1.[Assessment_ECL_Srch_Cd]
      ,ecl1.[Control_Group]
      ,ecl1.[Control_Level]
      ,ecl1.[Control_Level_Destination_Desc_En]
      ,ecl1.[Control_Level_Destination_Desc_Fr]
      ,ecl1.[Control_Level_Abbrev]
      ,ecl1.[Control_Level_ID]
      ,ecl1.[ControlLevelECL_Desc_En]
      ,ecl1.[ControlLevelECL_Desc_Fr]
      ,ecl1.[PermitRequiredYN]
      ,ecl1.[CommentDesc]
      ,ecl1.[ReassessYN]
      ,ecl1.[ReassessCommentDesc]
      ,ecl1.[AssessmentDate]
	  ,ecl1.[Firearm_ECL]
	  ,ecl1.[ECL_Description_EN]
	  ,ecl1.[ECL_Description_FR]
      ,[DRV_Firearm_ECL_List] =
                      STUFF ((Select distinct ', ' +  isnull([Assessment_ECL], '') 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')
      ,[DRV_ECL_Description_EN_List] = 
				     STUFF ((Select distinct ', ' +  [ECL_Description_EN] 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')
      ,[DRV_ECL_Description_FR_List] =
				             STUFF ((Select distinct ', ' +  [ECL_Description_FR] 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')

      ,[DRV_Control_Level_ECL_List] =
                      STUFF ((Select distinct ', ' +  isnull([Control_Level], '') 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')

      ,[DRV_Control_Level_ECL_Description_EN_List] = 
				     STUFF ((Select distinct ', ' +  [ControlLevelECL_Desc_EN] 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')
      ,[DRV_Control_Level_ECL_Description_FR_List] =
				             STUFF ((Select distinct ', ' +  [ControlLevelECL_Desc_FR] 
                                    from S_EXCOL_ECLASSESSMENT as ecl2
                    where ecl2.EPEObjectID = ecl1.EPEObjectID 
                    FOR XML PATH (''), TYPE ).value('.', 'varchar(max)'), 1,1,'')


      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
  FROM [dbo].[S_EXCOL_ECLASSESSMENT] ecl1,
    (Select [EPEObjectID], MAX(ECLAssessmentID) as max_ecl 
                                FROM [dbo].[S_EXCOL_ECLASSESSMENT] 
                                                        group by EPEObjectID) ecl2
                                where ecl1.[EPEObjectID] = ecl2.[EPEObjectID]
                                and ecl1.ECLAssessmentID = ecl2.max_ecl
  and ecl1.[ItemECLSelfAssessmentID] <> -3

 )

  SELECT  
		[ItemFirearmECLSelfAssessmentID]
      ,[ItemECLSelfAssessmentID]
      ,[ItemID]
	  ,ECLSelfAssessment_ECL
      ,[FirearmECLID]
      ,[ECL]
      ,[FirearmECL]
      ,[RelatedGoodsECL]
      ,[AmmoECL]
      ,[SortSequence]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]

	  ,DRV_ECL_List 
 	  ,substring([DRV_ECL_Description_EN_List], 1, 8000)  as DRV_ECL_Description_EN_List
	  ,substring([DRV_ECL_Description_FR_List], 1, 8000) as DRV_ECL_Description_FR_List
	   
      ,[DRV_Control_Level_ECL_List]
      ,substring([DRV_Control_Level_ECL_Description_EN_List], 1, 8000)  as DRV_Control_Level_ECL_Description_EN_List
      ,substring([DRV_Control_Level_ECL_Description_FR_List], 1, 8000)  as DRV_Control_Level_ECL_Description_FR_List
	   
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT] from cte;
  --and  ecl1.itemID = 1018389
```

```sql
-- SQL Query for D_EXCOL_EPEOBJECT_DETAILS Source

SELECT
      [EPEObjectID]
      ,[RootEPEObjectID]
      ,[ParentEPEObjectID]
      ,[EPEObjectRefNo]
      ,[EPEObjectTypeID]
      ,[EPEObjectType_Desc_En]
      ,[EPEObjectType_Desc_Fr]
      ,[EPEObjectStatusID]
      ,[EPEObjectStatus_Desc_En]
      ,[EPEObjectStatus_Desc_Fr]
      ,[EPEObjectNewStatusID]
      ,[EPEObjectNewStatus_Desc_En]
      ,[EPEObjectNewStatus_Desc_Fr]
      ,[EPEObjectStatusChangedDate]
      ,[EPEObjectStatusChangedReasonID]
      ,[EPEObjectStatusChangedComment]
      ,[SavedOnceYN]
      ,[EditableYN]
      ,[PermitRequiedYN]
      ,[IssueDate]
      ,[ReIssueDate]
      ,[ExpiryDate]
      ,[EffectiveDate]
      ,[SubmitDate]
      ,[CreatedDate]
      ,[CreatedUserID]
      ,[SubmittedByUserName]
      ,[SessionID]
      ,[VersionNo]
      ,[AmendmentVersionNo]
      ,[ClientID]
      ,[ReviewID]
      ,[ReviewAAID]
      ,[ItemAdvertiseBCLogsID]
      ,[PermitCertificateNo]
      ,[EPEObjectDetailID]
      ,[DistributionID]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
      ,[InternalOpenRead]
      ,[ExternalOpenRead]
      ,[IsActiveObject]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
	  ,[PRELIMINARYANALYSISID]
	  ,[Duration]
	  ,[DecisionNotificationDate]
	  ,[CBSADetentionID]
	  ,[CBSADetentionAssessmentID]
	  ,[MessageToApplicant]
                  ,[OriginalExpiryDate]
  FROM [dbo].[S_EXCOL_EPEOBJECT]
```

```sql
-- SQL Query for D_EXCOL_EPEOBJECT_CRITERIA_CONDITION Source

SELECT
      L[LOCATION_ID]
      ,[LOCATION_ENG_NM] 
      ,[LOCATION_FR_NM]
      ,[CDA_COUNTRY_IND]
      ,[USA_COUNTRY_IND]
      ,[OTHER_COUNTRY_IND]
      ,[ISO_CD]
      ,[COUNTRY_EN]
      ,[COUNTRY_FR]
      ,[COUNTRY_CURRENCY_NM]
      ,[ALTERNATE_PORT_CD]
      ,[AREA_CONTROL_LIST_IND]
      ,[UN_EMBARGO_LIST_IND]
      ,[AFCCL_IND]
      ,[AREA_IND]
      ,[COUNTRY_IND]
      ,[PROV_IND]
      ,[STATE_IND]
      ,[SWL_REGION_IND]
      ,[CITY_IND]
      ,[PORT_IND]
      ,[PORT_AUTO_PROCESS_IND]
      ,[NAFTA_IND]
      ,[CCFTA_IND]
      ,[CCRFTA_IND]
      ,[NON_FTA_IND]
      ,[EU_IND]
      ,[THIRD_COUNTRY_IND]
      ,[LOCATION_EFCTV_DT]
      ,[LOCATION_EXPIRY_DT]
      ,[PARENT_ID]
      ,[NODE_LVL]
      ,[CHILDREN_IND]
      ,[NATO_IND]
      ,[LOCATION_STTS_CD]
      ,[LOCATION_STTS_DESC_EN]
      ,[LOCATION_STTS_DESC_FR]
      ,[MOST_FAVOURED_NATION_IND]
      ,[SUB_MFN_IND]
      ,[CETA_IND]
      ,[AUDIT_USER_ID]
      ,[AUDIT_TMSTMP]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
  FROM [dbo].[S_EICS_LOCATIONS] L
```

```sql
-- SQL Query for D_EXCOL_BCLogs_EP_SummaryOfScale_UNION Source

SELECT [PeriodId], [Period_Start_Date], [Period_End_Date], [priceVl]
     , MAX(CASE WHEN [OPTA_IND] = 1 THEN [euscVl]  END) EUSC
     , MAX(CASE WHEN [OPTA_IND] = 0 THEN [euscVl]  END) AEUSC
	 ,[ETL_CREA_DT]
	,[ETL_UPDT_DT]
  FROM  [dbo].[S_EICS_SWLSLA_DATA]
  group by [PeriodId],[Period_Start_Date], [Period_End_Date], [priceVl]
			,[ETL_CREA_DT] ,[ETL_UPDT_DT]
```

```sql
-- SQL Query (Source: D_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT)

SELECT  [ItemECLSelfAssessment_Type]
      ,[FirearmItemECLSelfAssessmentID]
      ,[ItemID]
      ,[FirearmECLID]
      ,[ECL]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
      ,[FirearmECL_ECL]
      ,[FirearmECL_InactiveYN]
      ,[FirearmECL_FirearmECL]
      ,[FirearmECL_RelatedGoodsECL]
      ,[FirearmECL_AmmoECL]
      ,[FirearmECL_SortSequence]
      ,[FirearmECL_AuditConcurrencyDate]
      ,[FirearmECL_AuditUserID]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]
  FROM [dbo].[S_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT]
  where ItemECLSelfAssessment_Type = 'ItemFirearmECLSelfAssessment'
```

```sql
-- SQL Script (ESQLT- Truncate And Seed Dimensions)
Truncate Table [dbo].[D_EICS_BUSINESSES]; 
Truncate Table [dbo].[D_EICS_BUSINESS_PAYMENTS]; 
Truncate Table [dbo].[D_EICS_PERMIT_EXPORTS];
Truncate Table [dbo].[D_EICS_PERMIT_IMPORTS];
Truncate Table [dbo].[D_EICS_ACCOUNTS]; 
Truncate Table [dbo].[D_EICS_BUSINESS_RIGHTS];
Truncate Table [dbo].[D_EICS_SECTOR];
Truncate Table [dbo].[D_EICS_COMMODITY];
Truncate Table [dbo].[D_EICS_PERMIT_APPLICATIONS];
Truncate Table [dbo].[D_EICS_PERMIT_ITEMS];
Truncate Table [dbo].[D_EICS_PERMITS];
Truncate Table [dbo].[D_EICS_LOCATIONS]; 
Truncate Table [dbo].[D_EICS_CONTROL_ITEMS];
Truncate Table [dbo].[D_EXCOL_EPEOBJECT_DETAILS];

DBCC CHECKIDENT ('dbo.D_EICS_BUSINESSES', RESEED, 1)
SET IDENTITY_INSERT dbo.D_EICS_BUSINESSES ON

insert  into D_EICS_BUSINESSES
(
BUSINESS_SID,
BUS_ID,
BUS_STTS_CD,
BUS_STTS_DESC_EN,
BUS_STTS_DESC_FR,
EICB_NO,
CCRA_BUS_NO,
RICS_NO,
CA_NO,
BUS_NM,
LANG_IND,
CDN_RES_DCLRTN_IND,
BRKR_IND,
EXP_IND,
IMP_IND,
EXCLUDED_SWL_BUSINESS_IND,
SWL_REGION_ID,
RISK_LVL_CD,
RISK_LVL_DESC_EN,
RISK_LVL_DESC_FR,
APLCTN_CT,
ROUTE_APLCTN_NO,
DOC_LINK_ID,
ALLOW_EXP_APLCTN_IND,
ALLOW_IMP_APLCTN_IND,
REGULATE_TRANSFER_IN_IND,
PARENT_ID,
NODE_LVL,
CHILDREN_IND,
BUS_ALIAS_NM,
SUBSIDIARY_IND,
AUDIT_USER_ID,
AUDIT_TMSTMP,
GEP_IND,
SWL_REGION_DESC_EN,
SWL_REGION_DESC_FR,
SWL_SECTOR_TYPE_DESC_EN,
SWL_SECTOR_TYPE_DESC_FR,
ETL_CREA_DT,
ETL_UPDT_DT,
LATEST_ACTIVITY_DATE
)
VALUES
(
-3,
-3,
-3,
'Uncoded',
'Non-codé',
-3,
-3,
-3,
-3,
'Uncoded',
0,
0,
0,
0,
0,
0,
-3,
-3,
'Uncoded',
'Non-codé',
0,
-3,
-3,
0,
0,
0,
-3,
0,
0,
'Uncoded',
0,
-3,
'9999-12-31',
0,
'Uncoded',
'Non-codé',
'Uncoded',
'Non-codé',
'9999-12-31',
'9999-12-31',
'9999-12-31'
)

SET IDENTITY_INSERT dbo.D_EICS_BUSINESSES OFF



DBCC CHECKIDENT ('