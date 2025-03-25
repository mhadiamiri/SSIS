## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| STG_NEICS | OLE DB | Server: $(Project::PRJ_PRM_SRC_DB_SRVR), Database: $(Project::PRJ_PRM_TRGT_STAGING_DB_NM) | Destination connection for loading data into staging tables | Integrated Security (Windows Authentication likely) | Project Parameters: PRJ_PRM_SRC_DB_SRVR, PRJ_PRM_TRGT_STAGING_DB_NM | Part 1, Part 2, Part 3 |
| ODS_NEICS | OLE DB | Server: [Inferred], Database: [Inferred] | Source for data extraction into staging tables | Read access to source database | None | Part 2, Part 3 |
| EXCOL_Source | OLE DB | Server: EXCOL_Source | Source for `S_EXCOL_EVENTHISTORY` data flow. | Integrated Security (Windows Authentication) | None | Part 3 |
| Flat File Connection Manager | FLATFILE | `C:\\Users\\ADMMADNIK\\source\\Workspaces\\Workspace\\EICS BI Solution Modernization\\SSIS Developer\\Gerry\\NEICS\\Rejects\\EPEObjectContact_rejects.txt` | Reads data from a flat file, presumably containing rejected records | File system access | None | Part 1 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, Part 2, Part 3|

## 3. Package Flow Analysis

*   The control flow consists of a sequence of activities executed within a `SEQC- Load STAGING Tables` Sequence Container.
*   **Control Flow:**

    1.  `EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` (Expression Task): Likely initializes the staging process.
    2.  `SEQC- Load STAGING Tables` (Sequence Container): Encapsulates the data loading logic.

        *   `ESQLT- Truncate Staging Tables` (Execute SQL Task): Truncates all staging tables.
        *   Multiple Data Flow Tasks (DFTs) sequentially load data into staging tables.
        *   Common pattern: OLE DB Source (ODS_NEICS or EXCOL_Source) -> Transformations (minimal, if any) -> OLE DB Destination (STG_NEICS).
        *   Error handling: `errorRowDisposition="FailComponent"` often used.
*   **Data Flow Tasks (Examples):**

#### DFT- S_COMMODITIES_HIER

*   **Source:** `S_COMMODITIES Source` (OLE DB Source) connects to `ODS_NEICS` and executes a SQL query.
*   **Transformation:** `Data Conversion` converts `ROW_ID`, `LVL1_ROW_ID`, etc., from integer/unicode string to string types.
*   **Destination:** `S_COMMODITIES_HIER destination` (OLE DB Destination) connects to `STG_NEICS` and loads data into `dbo.S_EICS_COMMODITY_HIER`.
*   **Error Handling:** `Data Conversion` configured to "Fail Component" on errors.
*   **Data Flow Tasks (Examples):**

#### DFT- S_EXCOL_EVENTHISTORY

*   **Source:** OLE DB Source named `"S_EXCOL_EVENTHISTORY Source"` connects to `Project.ConnectionManagers[EXCOL_Source]` and extracts data using the provided SQL query.
*   **Destination:** OLE DB Destination named `"S_EXCOL_EVENTHISTORY Destination"` connects to `Package.ConnectionManagers[STG_NEICS]` and loads data into table `[dbo].[S_EXCOL_EVENTHISTORY]`.
*   **Data Movement:** Data moves directly from the OLE DB Source to the OLE DB Destination.
*   **Transformations:** No transformations are evident in the provided snippet
*   **Error Handling:** There are error outputs defined on both the Source and Destination components.

## 4. Code Extraction

```sql
-- ESQLT- Truncate Staging Tables
TRUNCATE TABLE  dbo.[S_EXCOL_LOCATION];
TRUNCATE TABLE  dbo.[S_EICS_COMMODITY_CONVERSION];
TRUNCATE TABLE  dbo.[S_EICS_BUSINESS_SUSPENSIONS];
TRUNCATE TABLE  dbo.[S_EICS_COMMODITY];
TRUNCATE TABLE  dbo.[S_EICS_COMMODITY_UNITS];
TRUNCATE TABLE  dbo.[S_EICS_PERMIT_ITEMS];
TRUNCATE TABLE  dbo.[S_EICS_SECTOR];
TRUNCATE TABLE  dbo.[S_EICS_CONTROL_ITEMS];
TRUNCATE TABLE  dbo.[S_EICS_COMMODITY_HIER];
TRUNCATE TABLE  dbo.[S_EICS_CONTROL_ITEMS_HIER];
TRUNCATE TABLE  dbo.[S_EICS_PERMIT_APPLICATIONS];
TRUNCATE TABLE  dbo.[S_EICS_TRANSFERS];
TRUNCATE TABLE  dbo.[S_EICS_PERMITS];
TRUNCATE TABLE  dbo.[S_EICS_BUSINESS_RIGHTS];
TRUNCATE TABLE  dbo.[S_EICS_BUSINESSES];
TRUNCATE TABLE  dbo.[S_EICS_ACCOUNTS];
TRUNCATE TABLE [dbo].[S_EICS_PERMIT_IMPORTS];
TRUNCATE TABLE [dbo].[S_EICS_PERMIT_EXPORTS];
TRUNCATE TABLE [dbo].[S_EICS_LOCATIONS];
TRUNCATE TABLE [dbo].[S_EICS_QUOTA_TRANSFERS];
TRUNCATE TABLE [dbo].[S_EICS_BUISNESS_PAYMENTS];
TRUNCATE TABLE [dbo].[S_EXCOL_EPEOBJECT];
TRUNCATE TABLE [dbo].[S_EXCOL_EPEOBJECT_DETAILS];
TRUNCATE TABLE [dbo].[S_EXCOL_EPEOBJECTCONTACT];
TRUNCATE TABLE [dbo].[S_EXCOL_ITEM];
TRUNCATE TABLE [dbo].[S_EXCOL_ECLASSESSMENT];
TRUNCATE TABLE [dbo].[S_EXCOL_ACTIVITY];
TRUNCATE TABLE [dbo].[S_EXCOL_CONSULTATIONS];
TRUNCATE TABLE [dbo].[S_EXCOL_REVIEW];
TRUNCATE TABLE [dbo].[S_EXCOL_WORKFLOW];
TRUNCATE TABLE [dbo].[S_EXCOL_COUNTRY];
TRUNCATE TABLE [dbo].[S_EXCOL_CLIENT];
TRUNCATE TABLE [dbo].[S_EXCOL_REVIEWAA];
TRUNCATE TABLE [dbo].[S_EXCOL_EPEOBJECT_CRITERIA_CONDITION];
TRUNCATE TABLE [dbo].[S_EXCOL_PERMIT_UTILIZATION];
TRUNCATE TABLE [dbo].[S_EXCOL_USER];
TRUNCATE TABLE [dbo].[S_EXCOL_ECL_SELF_ASSESSMENT];
TRUNCATE TABLE [dbo].[S_EXCOL_DOCUMENT];
TRUNCATE TABLE [dbo].[S_EXCOL_CLIENT_USER_ASSIGNMENTROLE];
TRUNCATE TABLE [dbo].[S_EXCOL_ITEM_ADVERTISE_BCLogs];
TRUNCATE TABLE [dbo].[S_EXCOL_BCLogs_EP_SummaryOfScale_UNION];
TRUNCATE TABLE [dbo].[S_EICS_BUSINESS_ADDRESSES];
TRUNCATE TABLE [dbo].[S_EICS_SWLSLA_DATA];
TRUNCATE TABLE [dbo].[S_EXCOL_USERROLE];
TRUNCATE TABLE [dbo].[S_EICS_WORKFLOW];
TRUNCATE TABLE [dbo].[S_EXCOL_BCLogsSurplusOfferToPurchase];
TRUNCATE TABLE [dbo].[S_EICS_FINANCIAL_INVOICES];
TRUNCATE TABLE [dbo].[S_EICS_FINANCIAL_INVOICE_ITEMS];
TRUNCATE TABLE [dbo].[S_EICS_THIRD_PARTIES];
TRUNCATE TABLE [dbo].[S_EICS_USER];
TRUNCATE TABLE [dbo].[S_EICS_USER_COMMODITIES_LOCATIONS];
TRUNCATE TABLE [dbo].[S_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT];
TRUNCATE TABLE [dbo].[S_EXCOL_EPEObject_Status_History];
TRUNCATE TABLE [dbo].[S_EICS_FOREIGN_LICENSES];
TRUNCATE TABLE [dbo].[S_EICS_BUSINESS_CONTACTS];
TRUNCATE TABLE [dbo].[S_EICS_EDI_TRANSACTION_ITEMS];
TRUNCATE TABLE [dbo].[S_EICS_EDI_TRANSACTIONS];
TRUNCATE TABLE [dbo].[S_EICS_BUSINESS_COMMENTS];
TRUNCATE TABLE [dbo].[S_EXCOL_BCLogsEPSummaryOfScale_Pass_One];
TRUNCATE TABLE [dbo].[S_EXCOL_BCLogsEPSummaryOfScale_Pass_Two];
TRUNCATE TABLE [dbo].[S_EXCOL_CONSULTEE];
TRUNCATE  TABLE [dbo].[S_EXCOL_EVENTHISTORY];
TRUNCATE  TABLE [dbo].[S_EXCOL_PRELIMINARY_ANALYSIS];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFCOUNTRYPROFILEANDBIRELATION];
TRUNCATE  TABLE [dbo].[S_EXCOL_USER_NOTIFICATION];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFDIVERSIONRISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFENDUSERVERIFICATION];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFGBVIOLENCEAGAINSTVGRISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFHRANDHUMANITARIANLAWRISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFNATIONALSECURITYRISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFOVERALLRISKASSESSMENT];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFPEACEANDSECURITYRISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFSANCTIONCOMPLIANCE];
TRUNCATE  TABLE [dbo].[S_EXCOL_RAFTERRORISMANDORGANIZEDCRIMERISK];
TRUNCATE  TABLE [dbo].[S_EXCOL_CBSA_DETENTION];
TRUNCATE  TABLE [dbo].[S_EXCOL_CBSA_DETENTION_ASSESSMENT];
TRUNCATE  TABLE [dbo].[S_EXCOL_CBSA_DETENTION_ECLICL_ASSESSMENT];
TRUNCATE  TABLE [dbo].[S_EXCOL_ICL_ASSESSMENT];
TRUNCATE  TABLE [dbo].[S_EXCOL_BADSTANDING];
TRUNCATE  TABLE [dbo].[S_EXCOL_WORST_OVERDUE_CONDITION];
TRUNCATE  TABLE [dbo].[S_EXCOL_MANAGEMENT_APPROVAL];
TRUNCATE  TABLE [dbo].[S_EICS_Commodity_Location_Conversions];

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'i_S_EICS_CONTROL_ITEMS' AND object_id = OBJECT_ID('[STG_NEICS].[dbo].[S_EICS_CONTROL_ITEMS]'))
    DROP INDEX [i_S_EICS_CONTROL_ITEMS] ON [STG_NEICS].[dbo].[S_EICS_CONTROL_ITEMS];

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'i_S_EICS_PERMIT_APPLICATIONS' AND object_id = OBJECT_ID('[STG_NEICS].[dbo].[S_EICS_PERMIT_APPLICATIONS]'))
    DROP INDEX [i_S_EICS_PERMIT_APPLICATIONS] ON [STG_NEICS].[dbo].[S_EICS_PERMIT_APPLICATIONS];

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'i_S_EICS_PERMIT_ITEMS' AND object_id = OBJECT_ID('[STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS]'))
    DROP INDEX [i_S_EICS_PERMIT_ITEMS] ON [STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS];

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'i_S_EICS_PERMIT_ITEMS_2' AND object_id = OBJECT_ID('[STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS]'))
    DROP INDEX [i_S_EICS_PERMIT_ITEMS_2] ON [STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS];
```

```sql
-- S_COMMODITIES Source
WITH Hierarchy ([Cmdty_Id], [Parent_Id], Parents)
AS
(
    --LVL1
	SELECT	[Cmdty_Id],
			[Parent_Id], CAST('' AS VARCHAR(MAX))
    FROM [dbo].[Commodities] AS LVL1
    WHERE [Parent_Id] IS NULL

 --LVL2
    UNION ALL
    SELECT	LVL2.[Cmdty_Id]
			,LVL2.[Cmdty_Id],
    CAST(CASE WHEN LVL1.Parents = ''
        THEN(CAST(LVL2.[Parent_Id] AS VARCHAR(MAX)))
        ELSE(LVL1.Parents + '.' + CAST(LVL2.[Parent_Id] AS VARCHAR(MAX)))
    END AS VARCHAR(MAX))
        FROM [dbo].[Commodities] AS LVL2
        INNER JOIN Hierarchy AS LVL1
		ON LVL2.[Parent_Id] = LVL1.[Cmdty_Id]
	--LVL3
    UNION ALL
    SELECT	LVL3.[Cmdty_Id]
			,LVL3.[Cmdty_Id],
    CAST(CASE WHEN LVL2.Parents = ''
        THEN(CAST(LVL3.[Parent_Id] AS VARCHAR(MAX)))
        ELSE(LVL2.Parents + '.' + CAST(LVL3.[Parent_Id] AS VARCHAR(MAX)))
    END AS VARCHAR(MAX))
        FROM [dbo].[Commodities] AS LVL3
        INNER JOIN Hierarchy AS LVL2
		ON LVL3.[Parent_Id] = LVL2.[Cmdty_Id]

	--LVL4
    UNION ALL
    SELECT	LVL4.[Cmdty_Id]
			,LVL4.[Cmdty_Id],
    CAST(CASE WHEN LVL3.Parents = ''
        THEN(CAST(LVL4.[Parent_Id] AS VARCHAR(MAX)))
        ELSE(LVL3.Parents + '.' + CAST(LVL4.[Parent_Id] AS VARCHAR(MAX)))
    END AS VARCHAR(MAX))
        FROM [dbo].[Commodities] AS LVL4
        INNER JOIN Hierarchy AS LVL3
		ON LVL4.[Parent_Id] = LVL3.[Cmdty_Id]

	--LVL5
    UNION ALL
    SELECT	LVL5.[Cmdty_Id],
			LVL5.[Cmdty_Id],
    CAST(CASE WHEN LVL4.Parents = ''
        THEN(CAST(LVL5.[Parent_Id] AS VARCHAR(MAX)))
        ELSE(LVL4.Parents + '.' + CAST(LVL5.[Parent_Id] AS VARCHAR(MAX)))
    END AS VARCHAR(MAX))
        FROM [dbo].[Commodities] AS LVL5
        INNER JOIN Hierarchy AS LVL4
		ON LVL5.[Parent_Id] = LVL4.[Cmdty_Id]

)
SELECT DISTINCT [Cmdty_Id] as ROW_ID
	,REVERSE(PARSENAME(REPLACE(REVERSE(Parents), ',', '.'), 1)) AS LVL1_ROW_ID
   , REVERSE(PARSENAME(REPLACE(REVERSE(Parents), ',', '.'), 2)) AS LVL2_ROW_ID
   , REVERSE(PARSENAME(REPLACE(REVERSE(Parents), ',', '.'), 3)) AS LVL3_ROW_ID
   , REVERSE(PARSENAME(REPLACE(REVERSE(Parents), ',', '.'), 4)) AS LVL4_ROW_ID
   , REVERSE(PARSENAME(REPLACE(REVERSE(Parents), ',', '.'), 5)) AS LVL5_ROW_ID
    FROM Hierarchy
ORDER BY 1
OPTION(MAXRECURSION 32767)
```

```sql
-- S_EICS_ACCOUNTS Source
SELECT acc.[Acct_Id]				as ACCT_ID
      ,acc.[Control_Item_Id]			as CONTROL_ITEM_ID
      ,acc.[Acct_Type_Cd]			as ACCT_TYPE_CD
	  ,acc_type.[Acct_Type_Eng_Desc]	as ACCT_TYPE_DESC_EN
	  ,acc_type.[Acct_Type_Fr_Desc]		as ACCT_TYPE_DESC_FR
      ,acc.[Acct_Desc]				as ACCT_DESC
      ,acc.[Acct_Qt]				as ACCT_QT
      ,acc.[Acct_Balance_Qt]		as ACCT_BALANCE_QT
      ,acc.[Bus_Id]					as BUS_ID
      ,acc.[Bus_Softwood_Type_Id]	as BUS_SOFTWARE_TYPE_ID
	  ,sst.Softwood_Sector_Type_Eng_Desc as SOFTWOOD_SECTOR_TYPE_DESC_EN
	  ,sst.Softwood_Sector_Type_Fr_Desc  as SOFTWOOD_SECTOR_TYPE_DESC_FR
      ,acc.[Interval_Rstrctn_Set_Ind]	as INTERVAL_RSTRCTN_SET_IND
      ,acc.[Parent_Id]				as PARENT_ID
      ,acc.[Node_Lvl]				as NODE_LVL
      ,acc.[Children_Ind]			as CHILDREN_IND
      ,acc.[Original_Acct_Qt]		as ORIGINAL_ACCT_QT
      ,acc.[Borrowed_Qt]			as BORROWED_QT
      ,acc.[Carry_Forward_Qt]		as CARRY_FORWARD_QT
      ,acc.[Acct_State]				as ACCT_STATE
      ,acc.[Pool_Acct_Type_Id]		as POOL_ACCT_TYPE_ID
	  ,pat.Pool_Acct_Type_Eng_Desc	as POOL_ACCT_TYPE_DESC_EN
	  ,pat.Pool_Acct_Type_Fr_Desc	as POOL_ACCT_TYPE_DESC_FR
      ,acc.[Audit_User_Id]			as AUDIT_USER_ID
      ,acc.[Audit_Tmstmp]			as AUDIT_TMSTMP
      ,getdate() as [ETL_CREA_DT]
      ,getdate() as [ETL_UPDT_DT]
FROM [dbo].[Accounts] acc
left outer join  [dbo].Ct_Account_Types acc_type
on acc.Acct_Type_Cd = acc_type.[Acct_Type_Cd]
left outer join  [dbo].[Business_Softwood_Types] bst
on acc.Bus_Softwood_Type_Id = bst.Bus_Softwood_Type_Id
left outer join [dbo].[Sys_Softwood_Sector_Types] sst
on bst.Softwood_Sector_Type_Cd = sst.Softwood_Sector_Type_Cd
left outer join  [dbo].[Pool_Account_Types] pat
on acc.[Pool_Acct_Type_Id]	 = pat.Pool_Acct_Type_Id
order by 1
```

```sql
-- S_EICS_BUSINESSES Source
SELECT
b.BUS_ID
,isnull(b.BUS_STTS_CD, -3) as BUS_STTS_CD
,bs.BUS_STTS_ENG_DESC as BUS_STTS_DESC_EN
,bs.BUS_STTS_FR_DESC as BUS_STTS_DESC_FR
,b.EICB_NO
,b.CCRA_BUS_NO
,b.RICS_NO
,b.CA_NO
,b.BUS_NM
,b.LANG_IND
,b.CDN_RES_DCLRTN_IND
,b.BRKR_IND
,b.EXP_IND
,b.IMP_IND
,b.EXCLUDED_SWL_BUSINESS_IND
,isnull(b.SWL_REGION_ID, -3) as SWL_REGION_ID
,loc.Location_Eng_Nm as SWL_REGION_DESC_EN
,loc.Location_Fr_Nm as SWL_REGION_DESC_FR
,type_nm.Softwood_Sector_Type_Eng_Desc as SWL_SECTOR_TYPE_DESC_EN
,type_nm.Softwood_Sector_Type_Fr_Desc as SWL_SECTOR_TYPE_DESC_FR
,isnull(b.RISK_LVL_CD, -3) as RISK_LVL_CD
,rl.RISK_LVL_ENG_DESC as RISK_LVL_DESC_EN
,rl.RISK_LVL_FR_DESC as RISK_LVL_DESC_FR
,b.APLCTN_CT
,b.ROUTE_APLCTN_NO
,b.DOC_LINK_ID
,b.ALLOW_EXP_APLCTN_IND
,b.ALLOW_IMP_APLCTN_IND
,b.REGULATE_TRANSFER_IN_IND
,b.PARENT_ID
,b.NODE_LVL
,b.CHILDREN_IND
,b.BUS_ALIAS_NM
,b.SUBSIDIARY_IND
,b.AUDIT_USER_ID
,b.AUDIT_TMSTMP
,b.GEP_IND
,getdate() as ETL_CREA_DT
,getdate() as ETL_UPDT_DT
FROM [dbo].[Businesses] b
left outer join [dbo].[Sys_Business_Statuses] bs
on b.BUS_STTS_CD = bs.BUS_STTS_CD
left outer join [dbo].[Ct_Risk_Levels] rl
on b.RISK_LVL_CD = rl.RISK_LVL_CD
left outer join [dbo].[Locations] loc
on b.SWL_Region_Id = loc.Location_Id
left outer join [dbo].[Business_Softwood_Types] type_cd
on b.Bus_Id = type_cd.Bus_Id
and type_cd.Softwood_Sector_Type_Cd = (select (min(sq1.Softwood_Sector_Type_Cd))--Prioritize 'Primary Mill' (type 1) over others when many
from [dbo].[Business_Softwood_Types] sq1
where type_cd.Bus_Id = sq1.Bus_Id)
left outer join [dbo].[Sys_Softwood_Sector_Types] type_nm
on type_cd.Softwood_Sector_Type_Cd = type_nm.Softwood_Sector_Type_Cd
order by 1
```

```sql
-- S_EICS_BUSINESS_ADDRESSES Source
SELECT Business_Addresses.[Bus_Adrs_Id]--new count after addr type join = 165,197 previous count = 151,570
      ,Business_Addresses.[Bus_Id]
      ,Business_Addresses.[Adrs_Line1_Txt]
      ,Business_Addresses.[Adrs_Line2_Txt]
      ,Business_Addresses.[Adrs_Line3_Txt]
      ,Business_Addresses.[City_Nm]
      ,isnull(Business_Addresses.[Prov_Id], -3)	as Prov_Id
	  ,Prov_Locations.Location_Eng_Nm	as Province_Desc_En
	  ,Prov_Locations.Location_Fr_Nm	as Province_Desc_Fr
      ,Business_Addresses.[Postal_Cd]
      ,Business_Addresses.[State_Id]
      ,Business_Addresses.[Zip_Cd]
      ,isnull(Business_Addresses.[Country_Id], -3)as Country_Id
	  ,Country_Locations.Location_Eng_Nm	as Country_Desc_En
	  ,Country_Locations.Location_Fr_Nm	as Country_Desc_Fr
      ,Business_Addresses.[Phn_No]
      ,Business_Addresses.[Fx_No]
      ,Business_Addresses.[Email_Txt]
      ,Business_Addresses.[URL_Txt]
      ,Business_Addresses.[Brkr_Outpost_No]
      ,Business_Addresses.[Audit_User_Id]
      ,Business_Addresses.[Audit_Tmstmp]
	  ,BAT.Adrs_Type_Cd as Adrs_Type_Cd
	  ,SYS_BAT.Adrs_Type_Eng_Desc as Adrs_Type_Eng_Desc
	  ,SYS_BAT.Adrs_Type_Fr_Desc  as Adrs_Type_Fr_Desc
      ,GETDATE()as [etl_crea_dt]
      ,GETDATE()as [etl_updt_dt]
FROM [dbo].[Business_Addresses] Business_Addresses
left outer join [dbo].[Locations] Prov_Locations
on Business_Addresses.Prov_Id = Prov_Locations.Location_Id
left outer join [dbo].[Locations] Country_Locations
on Business_Addresses.[Country_Id] = Country_Locations.Location_Id
	left outer join    [dbo].[Business_Address_Types] BAT
on Business_Addresses.[Bus_Adrs_Id] = BAT.[Bus_Adrs_Id]
left join [dbo].[Sys_Address_Types] SYS_BAT
on SYS_BAT.[Adrs_Type_Cd] = BAT.[Adrs_Type_Cd]
```

```sql
-- S_EICS_BUSINESS_COMMENTS Source
SELECT[Bus_Comment_Id]
      ,[Bus_Id]
      ,[Bus_Comment_Txt]
      ,[Audit_User_Id]
      ,[Audit_Tmstmp]
      ,getdate()as [etl_crea_dt]
      ,getdate()as [etl_updt_dt]
FROM [dbo].[Business_Comments]
```

```sql
-- S_EICS_BUSINESS_CONTACTS Source
SELECT bc.[BUS_CNTCT_ID]
      ,bc.[BUS_ID]
      ,bc.[CNTCT_FIRST_NM]
      ,bc.[CNTCT_LAST_NM]
      ,bc.[BUS_CNTCT_TXT]
	  ,bcr.Cntct_Role_Cd		as CONTACT_ROLE_CD
	  ,cr.Cntct_Role_Eng_Desc	as CONTACT_ROLE_DESC_EN
	  ,cr.Cntct_Role_Fr_Desc	as CONTACT_ROLE_DESC_FR
	  ,cr.Audit_Tmstmp			as CONTACT_ROLE_AUDIT_TIMESTAMP
      ,bc.AUDIT_USER_ID
      ,bc.AUDIT_TMSTMP
      ,getdate() 				as 	[ETL_CREA_DT]
      ,getdate() 				as 	[ETL_UPDT_DT]
from [dbo].[Business_Contacts] bc
left outer join [dbo].[Business_Contact_Roles] bcr
on bc.Bus_Cntct_Id = bcr.Bus_Cntct_Id
left outer join [dbo].[Ct_Contact_Roles] cr
on bcr.Cntct_Role_Cd = cr.Cntct_Role_Cd
```

```sql
-- S_EXCOL_EVENTHISTORY Source SQL Query
SELECT [EventHistoryID]
      ,[EPEObjectID]
      ,[Description]
      ,[Parameter]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
     ,getdate()		as 	[ETL_CREA_DT]
      ,getdate() 		as 	[ETL_UPDT_DT]
  FROM [dbo].[EventHistory]
```

```sql
-- S_EXCOL_FIREARM_ITEM_ECL_SELF_ASSESSMENT Source SQL Query
with cte
as
(
SELECT
	'ItemFirearmECLSelfAssessment' as ItemECLSelfAssessment_Type
	,ItemFirearmECLSelfAssessment.[ItemFirearmECLSelfAssessmentID] as FirearmItemECLSelfAssessmentID
    	,ItemFirearmECLSelfAssessment.[ItemID]
    	,isnull(ItemFirearmECLSelfAssessment.[FirearmECLID], -3) as [FirearmECLID]
	,null as [ECL]
    	,ItemFirearmECLSelfAssessment.[AuditConcurrencyDate]
    	,ItemFirearmECLSelfAssessment.[AuditUserID]
	,CT_FirearmECL.ECL			as FirearmECL_ECL
	,CT_FirearmECL.InactiveYN		as FirearmECL_InactiveYN
	,CT_FirearmECL.FirearmECL		as FirearmECL_FirearmECL
	,CT_FirearmECL.RelatedGoodsECL		as FirearmECL_RelatedGoodsECL
	,CT_FirearmECL.AmmoECL			as FirearmECL_AmmoECL
	,CT_FirearmECL.SortSequence		as FirearmECL_SortSequence
	,CT_FirearmECL.AuditConcurrencyDate as FirearmECL_AuditConcurrencyDate
	,CT_FirearmECL.AuditUserID		as FirearmECL_AuditUserID
	,getdate()				as [ETL_CREA_DT]
	,getdate()				as [ETL_UPDT_DT]
  FROM [dbo].[ItemFirearmECLSelfAssessment] ItemFirearmECLSelfAssessment
  left outer join  [dbo].[CT_FirearmECL] CT_FirearmECL
  on ItemFirearmECLSelfAssessment.FirearmECLID = CT_FirearmECL.FirearmECLID

union

SELECT
		'ItemECLSelfAssessment' as ItemECLSelfAssessment_Type
		,[ItemECLSelfAssessmentID] as FirearmItemECLSelfAssessmentID
		,isnull([ItemID], -3) as [ItemID]
		,null as [FirearmECLID]
		,[ECL]
		,[AuditConcurrencyDate]
		,[AuditUserID]
		,null as FirearmECL_ECL
		,null as FirearmECL_InactiveYN
		,null as FirearmECL_FirearmECL
		,null as FirearmECL_RelatedGoodsECL
		,null as FirearmECL_AmmoECL
		,null as FirearmECL_SortSequence
		,null as FirearmECL_AuditConcurrencyDate
		,null as FirearmECL_AuditUserID
		,getdate()		as [ETL_CREA_DT]
		,getdate()		as [ETL_UPDT_DT]
  FROM  [dbo].[ItemECLSelfAssessment]

  )
  select * from cte;
```

```sql
-- S_EXCOL_ICL_ASSESSMENT Source SQL Query
SELECT [ICLAssessmentID]
      ,[ICL]
      ,[Note]
      ,[AssessmentID]
      ,[AuditConcurrencyDate]
      ,[AuditUserID]
	  ,getdate() as [ETL_CREA_DT]
	  ,getdate() as [ETL_UPDT_DT]
  FROM [dbo].[ICLAssessment]
```

```sql
-- S_EXCOL_ITEM Source SQL Query
SELECT item.ItemID
      ,item.EPEObjectID
      ,item.SeqNo
      ,item.ModeCode
      ,item.ItemTypeCode
      ,item.ItemDesc
      ,item.QuantityTypeCode
      ,item.ReportPermitUtilizationYN
      ,item.Quantity
      ,item.UnitValue
      ,item.TotalValue
      ,item.USContent
      ,isnull(item.CountryOfOriginID, -3)as CountryOfOriginID
	  ,Country.NameEn					as Country_Desc_En
	  ,Country.NameFr					as Country_Desc_Fr
      ,isnull(item.GoodsDesignedForID, -3)  as GoodsDesignedForID
	  ,GoodsDesignedFor.NameEn			as GoodsDesignedFor_Desc_En
	  ,GoodsDesignedFor.NameFr			as GoodsDesignedFor_Desc_Fr
      ,item.GoodsDesignedForSpecifyDesc
      ,item.GoodUseCryptoYN
      ,item.LogCorrespondingAAEPEObjectID
      ,item.LogRaftBoomOrParcelNo
      ,item.LogFNo
      ,item.LogFNoApprovedYN
      ,item.LogNbrOfPieces
      ,isnull(item.LogQtyUnitOfMeasureID, -3) as LogQtyUnitOfMeasureID
	  ,LogUnitOfMeasure.NameEn			as LogUnitOfMeasure_Desc_En
	  ,LogUnitOfMeasure.NameFr			as LogUnitOfMeasure_Desc_Fr
      ,item.FirearmRegCertNo
      ,item.FirearmMake
      ,item.FirearmModel
      ,item.FirearmSerialNoOrFIN
      ,item.FirearmCalibre
      ,isnull(item.FirearmClassificationID, -3) as FirearmClassificationID
	  ,FirearmClassification.NameEn			as FirearmClassification_Desc_En
	  ,FirearmClassification.NameFr			as FirearmClassification_Desc_Fr
      ,item.FirearmAutomaticYN
      ,item.OICNo
      ,isnull(item.LogNativeProvSpeciesID, -3)  as LogNativeProvSpeciesID
	  ,LogSpecies.NameEn					as LogSpecies_desc_En
	  ,LogSpecies.NameFr					as LogSpecies_desc_Fr
	  ,isnull(isnull(item.LogSpeciesEndUseSortID,item.LogNativeProvSpeciesID), -3)  as LogSpeciesEndUseSortID
	  ,SpeciesEndUseSort.NameEn				as SpeciesEndUseSort_Desc_En
	  ,SpeciesEndUseSort.NameFr				as SpeciesEndUseSort_Desc_fr
      ,isnull(item.AuditConcurrencyDate, -1)   as AuditConcurrencyDate
      ,item.AuditUserID
      ,item.FRGItemType
      ,item.FRGLicenceType
      ,item.FRGLicenceHolderName
      ,item.FRGLicenceNo
      ,item.FRGFRTNo
      ,isnull(item.FRGMakeID, -3)			as FRGMakeID
	  ,FRGMake.NameEn						as FRGMake_Desc_En
	  ,FRGMake.NameFr						as FRGMake_Desc_Fr
      ,isnull(item.FRGModelID, -3)			as FRGModelID
	  ,FRGModel.NameEn						as FRGModel_Desc_En
      ,FRGModel.NameFr						as FRGModel_Desc_Fr
	  ,isnull(item.FRGTypeID, -3)			as FRGTypeID
	  ,FRGType.NameEn						as FRGType_Desc_En
	  ,FRGType.NameFr						as FRGType_Desc_Fr
      ,isnull(item.FRGActionID, -3)			as FRGActionID
	  ,FRGAction.NameEn						as FRGAction_Desc_En
	  ,FRGAction.NameFr						as FRGAction_Desc_fr
      ,isnull(item.FRGCalibreID, -3)		as FRGCalibreID