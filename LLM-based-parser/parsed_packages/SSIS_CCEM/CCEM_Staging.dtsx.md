```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                                                                                                                                                                               | Purpose within Package                                                                                                                                                                                                                                                                                                                                   | Security Requirements                                                                                                                                                                                                                                                                  | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|-------------|
| Excel Connection Manager | EXCEL           | `Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\Documents\\Project\\Financial Sample.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES";`                                                                                                                             | Potentially used as a lookup table or source data, but not directly used in the provided code. Likely for testing or a different configuration.                                                                                                                                                                                             | Requires access to the specified file path. The account running the SSIS package needs read access to the file system.  Potentially sensitive data in the Excel file itself.  Consider encrypting the file or limiting access.                                                | None                 | Part 1                  |
| CCEM_STAGING             | OLEDB           | Server=...;Database=...;Integrated Security=SSPI;Persist Security Info=False / *Details are not provided in the package XML, assumed to be external connection*                                                                                                                                    | Destination for several Data Flow Tasks.  Used to write transformed data to staging tables.  It is also used for all the Lookup Transformations                                                                                                                                                                                                  | Integrated Security (Windows Authentication) is being used. The account running the SSIS package needs to have access to the CCEM_STAGING database / Connection details (server, database, authentication) need to be secured. Credentials should not be hardcoded in the package.  Use Windows Authentication or a secure credential store.  Access to staging tables must be restricted. | None                 | Part 1, 4                  |
| ODS_CCEM                 | OLEDB           | Server= [ODS_CCEM Server Details]; Database= [ODS_CCEM Database Name]; Authentication Method= [Likely Windows or SQL Authentication, need full XML to confirm] / Server=...;Database=...;Integrated Security=SSPI;Persist Security Info=False / *Details are not provided in the package XML, assumed to be external connection*                                                                                                                                    | Source for several Data Flow Tasks.  Extracts data from source tables in the ODS.  Used as source for all Data Flow Tasks. Used as source for all the Lookup Transformations                                                                                                                                                                                          | Requires access to the ODS_CCEM database. Proper authentication and authorization are needed / Integrated Security (Windows Authentication) is being used. The account running the SSIS package needs to have access to the ODS_CCEM database / Connection details (server, database, authentication) need to be secured. Credentials should not be hardcoded in the package.  Use Windows Authentication or a secure credential store.  Access to source tables must be restricted. | None                 | Part 1, 3, 4                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

The package consists of the following activities in execution order:

1.  **EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode:** An Expression Task that evaluates `1 == 1`. This serves as a starting point and likely represents a basic check or placeholder.
2.  **SEQC- Load Staging\_1\_SP1:** A Sequence Container that encapsulates multiple Data Flow Tasks.
    *   **DFT- S\_CCEM\_ARREST:** Data Flow Task to load data from the `ccem_arrest` table in the `ODS_CCEM` database to the `CCEM_ARREST` table in the `CCEM_STAGING` database.
        *   **Source:** `OLEDB_SRC_S_CCEM_ARREEST` - Extracts data from `[dbo].[ccem_arrest]` in the `ODS_CCEM` database using the SQL query (see section 4).\
        *   **Transformation:** `DCONV_TRFM_DataType` - Converts data types of several columns. Specifically, `ccem_case` and `ccem_arrestid` are converted to string with length 255.
        *   **Destination:** `OLEDB_DEST_CCEM_ARREST` - Loads the transformed data into `[dbo].[CCEM_ARREST]` in the `CCEM_STAGING` database.
    *   **DFT- S\_CCEM\_ARREST\_DETENTION:** Data Flow Task to load data into the `CCEM_ARREST_DETENTION` table in the `CCEM_STAGING` database.
        *   **Source 1:** `OLEDB_SRC_ccem_arrest_activity_AND_Other_tables` - Extracts data using a complex SQL query joining various tables (see section 4) from `ODS_CCEM` database.
        *   **Source 2:** `OLEDB_S_CCEM_ARREST_ACTIVITY_VISIT` - Extracts data using a complex SQL query from ccem_arrest_activity and ccem_arrest_transfer tables
        *   **Transformation:** `Merge Join` - Performs a `FULL` join based on `ccem_case`, `ccem_arrestid`, `ccem_arrest_activityid`, and `ccem_arrest_transferid` from the two sources.
        *   **Transformation:** `DRVCOL_TRFM` - Creates new columns `Latest_Detention_Ind` and `Latest_visit_Ind` based on `LATEST_DETENTION_ROW` and `LATEST_VISIT_ROW`.
        *   **Transformation:** `DCONV_TRFM-DataType` - Converts data types of columns `VISIT_TYPE_FR`, `CREATED_BY_ID_ACTIV`, and `CREATED_BY_ID_TRANS`.
        *   **Destination:** `DFT- S_CCEM_ARREST_DETENTION` - Loads the transformed data into `[dbo].[CCEM_ARREST_DETENTION]` in the `CCEM_STAGING` database.
    *   **DFT- S\_CCEM\_ARREST\_PRISON:** *(DISABLED)* Data Flow Task, likely intended to load data into a `CCEM_ARREST_PRISON` table. Disabled in the code.
    *   **DFT- S\_CCEM\_ARREST\_TRANSFER:** Data Flow Task to load data into `CCEM_ARREST_TRANSFER` table in the `CCEM_STAGING` database.
        *   **Source:** `OLEDB_SRC_ccem_arrest_transfer` - Extracts data from `[dbo].[ccem_arrest_transfer]` in `ODS_CCEM` database using the SQL query (see section 4).
        *   **Transformation:** `DCONV_TRFM` - Converts  `PRISONER_NBR`, `VERDICT_STATUS_NM_FR`, and `DETENTION_STATUS_NM_FR` to strings.
        *   **Destination:** `OLEDB_DEST_CCEM_ARREST_TRANSFER` - Loads the transformed data into `[dbo].[CCEM_ARREST_TRANSFER]` in the `CCEM_STAGING` database.
    *   **DFT- S\_CCEM\_CASE:** Data Flow Task to load data into the `CCEM_CASE` table in the `CCEM_STAGING` database.
        *   **Source 1:** `OLEDB_SRC_ccem_case` - Extracts data from `[dbo].[ccem_case]` in `ODS_CCEM` database using the SQL query (see section 4).
        *   **Source 2:** `OLEDB_SRC_S_CCEM_SUB_CASE` - Extracts data using a complex SQL query from ccem_sub_case table
        *   **Transformation:** `Data Conversion` - Converts data types of columns `SUBCATEGORY_CASE_ID`, `CASE_ID`, `SUB_CONTACT_ID`, and `SUB_CASE_OWER_ID`.
        *   **Transformation:** `Sort1` and `Sort2` - Sort the data.
        *   **Transformation:** `Merge Join` - Performs a `FULL` join based on `CASE_ID`
        *   **Destination:** `OLEDB_DEST_S_CCEM_CASE` - Loads the transformed data into `[dbo].[CCEM_CASE]` in the `CCEM_STAGING` database.
    *   **DFT- S\_CCEM\_CASE\_EMPLOYEE:** Data Flow Task to load data into the `CCEM_EMPLOYEE` table in the `CCEM_STAGING` database.
        *   **Source:** `OLEDB_SRC_systemuser1` - Extracts data from  `dbo.systemuser` in `ODS_CCEM` database using the SQL query (see section 4).
        *   **Destination:** `OLEDB_DEST_CCEM_CASE_EMPLOYEE` - Loads the transformed data into `[dbo].[CCEM_EMPLOYEE]` in the `CCEM_STAGING` database.
    *   **DFT- S\_CCEM\_MISSION:** Data Flow Task to load data into `CCEM_MISSION` table in the `CCEM_STAGING` database.
        *   **Source:** `OLEDB_SRC_ccem_mission` - Extracts data from `[dbo].[ccem_mission]` in `ODS_CCEM` database using the SQL query (see section 4).
        *   **Destination:** `OLEDB_DEST_CCEM_MISSION` - Loads the transformed data into `[dbo].[CCEM_MISSION]` in the `CCEM_STAGING` database.
3.  **DFT_CCEM_COUNTRY**: Extracts data from `ccem_country` and `ccem_region_country` and loads into `CCEM_COUNTRY`.
4.  **DFT-CCEM\_CLIENT**: Extracts data from a source table and transforms it using multiple `Lookup` transformations.
    *   **Transformations:** Multiple `Lookup` transformations are used to enrich the data by joining with other tables based on codes (e.g., `ccem_contactcategory`, `gendercode`,  `address1_addresstypecode`).
    *   **Destination:**  `OLEDB_Dest-CCEM_CLIENT` inserts the transformed data into a destination table named `[dbo].[CCEM_CLIENT]`.
5.  **DFT_CCEM_TRIPDESTINATION**: Extracts data from `ccem_tripdestination` and loads into `CCEM_TRIPDESTINATION`.
6.  **DFT_CCEM_REGISTRATION**: Extracts data from `ccem_trip` and loads into `CCEM_REGISTRATION`.
7.  **DFT_CCEM_ORGANIZATION**: Extracts data from `account` and loads into `CCEM_ORGANIZATION`.
8.  **DFT-CCEM\_CRISIS**: Extracts data from `ccem_crisis` and loads into `CCEM_CRISIS`.
9. **DFT_CCEM_DEPARTURE**: Extracts data from `ccem_departure` and loads into `CCEM_DEPARTURE`.
10. **DFT_CCEM_DEPARTURE_ACTIVITY**: Extracts data from `ccem_departure_activity` and loads into `CCEM_DEPARTURE_ACTIVITY`.
11.  **DFT- S\_CCEM\_\_SUB\_CASE**: Extracts data using a UNION ALL query from multiple tables within the `ODS_CCEM` database and loads into `CCEM_SUB_CASE`.
    *   **Transformations:** `DRVCOL_TRFM-ETL_DATE` - Derived Column. Adds two new timestamp columns: `ETL_CREAT_DT` and `ETL_UPDT_DT`, both populated with the current date and time using the `GETDATE()` function.
12.  **DFT_CCEM_SLA**: Extracts data from the `dbo.ccem_sla` table in the `ODS_CCEM` database, performs lookups, and loads into the `dbo.CCEM_SLA` table within the `CCEM_STAGING` database.
    *   **Transformations:** Several Lookups join data from: `CCEM_CODE_TABLE` to retrieve descriptions.
13. **DFT_CASE_ACTIVITY**: Reads the `S_CCEM_CASE_ACTIVITY` table at the staging database, performs lookups, and writes to the `CCEM_CASE_ACTIVITY` table at the staging database.
    *   **Transformations:**\
        *   `LKP-ACTIVITY_TYPE_CODE` - Lookup. Looks up the description (`DESCR_EN`, `DESCR_FR`) of the `ccem_type` based on the `ATTRIBUTE_VALUE_NBR` in the `CCEM_CODE_TABLE`.

**Precedence Constraints and Conditions:**

*   The Data Flow Tasks within the `SEQC- Load Staging_1_SP1` Sequence Container will execute sequentially, one after the other. No specific constraints are defined, so they will likely execute upon successful completion of the previous task.

**Parallel Execution Paths:**

*   No explicit parallel execution paths are defined within the provided XML. All tasks within the Sequence Container will execute in a serial manner.

**Sequence Containers and Purpose:**

*   `SEQC- Load Staging_1_SP1`: This sequence container groups together the different Data Flow Tasks involved in loading data into the staging tables. It provides a logical grouping and allows for easier management of the loading process.
*   `SEQC_Staging_SLA` - This sequence container only contains the `DFT_CCEM_SLA` and an Execute SQL Task to truncate the `CCEM_SLA` table.
*   `Sequence Container_2_SP1` - This sequence container is responsible to load the `CCEM_CODE_TABLE` and `CCEM_SUBCATEGORY` tables.
*   `Sequence Container_3_SP1` acts as a container to organize the data flow and other tasks.

## 4. Code Extraction

```markdown
### SQL Queries

```

```sql
-- OLEDB_SRC_S_CCEM_ARREEST (DFT- S_CCEM_ARREST)
SELECT  distinct
       [ccem_case]
      ,[ccem_arrestid]
      ,[ccem_capitalpunishment]
      ,[ccem_capitalpunishmentname]
      ,[ccem_casename]
      ,[ccem_contact]
      ,[ccem_charge_primary]
      ,[ccem_charge_primaryname]
      ,[ccem_sentence]
      ,[ccem_trialstatus]
      ,[ccem_trialstatusname]
      ,[ccem_detentionstatus]
      ,[ccem_dateofarrest]

      ,getdate() as [etl_crea_dt]
      ,getdate() as [etl_updt_dt]
  FROM  [dbo].[ccem_arrest]
```

```sql
-- OLEDB_SRC_ccem_arrest_activity_AND_Other_tables (DFT- S_CCEM_ARREST_DETENTION)
SELECT DISTINCT 

	 cast(ar.[ccem_case] AS VARCHAR(255)) AS [ccem_case]
	 ,cast(ar.[ccem_casename] as varchar(255)) as [ccem_case_name]
                   ,cast(ar.[ccem_arrestid] AS VARCHAR(255)) AS [ccem_arrestid]
	,cast(tr.[ccem_arrest_transferid] AS VARCHAR(255)) AS [ccem_arrest_transferid]
	,cast(act.ccem_arrest_activityid AS VARCHAR(255)) AS [ccem_arrest_activityid]

	
	,ar.[ccem_capitalpunishment]
	,ar.[ccem_capitalpunishmentname]
	,cast(ar.[ccem_contact] AS VARCHAR(255)) AS [ar_ccem_contact]
	,ar.[ccem_charge_primary]
	,ar.[ccem_charge_primaryname]
                  ,ar.[ccem_charge_secondaryname]
	,ar. [ccem_sentence]
	,ar.[ccem_trialstatus]
	,ar.[ccem_trialstatusname]
	,ar.[ccem_dateofarrest]
	
	
	,tr.[ccem_date_end]
	,tr.[ccem_date_start]
	,cast(tr.[ccem_prison] AS VARCHAR(255)) AS [ccem_prison]
	,cast(tr.[ccem_prisonernumber] as varchar(255)) as [ccem_prisonernumber]
	,tr.[ccem_prisonname]
	,tr.[statecode]
	,tr.[statecodename]
	,tr.[statuscode]
	,tr.[statuscodename]
	,tr.[ccem_status_detention]
	,tr.[ccem_status_detentionname]
	,cast(tr.[ccem_identification] AS VARCHAR(255)) AS [arrest_transfer_id]

                 
	
	
	,cast(act.ccem_case_contact AS VARCHAR(255)) AS [act_ccem_contact]
	,act.ccem_start
	,act.ccem_typename as [VISIT_TYPE_EN]
	,cast(str_map.[value] as nvarchar(255)) as [VISIT_TYPE_FR]
	,act.ccem_prisonvisitname
	,act.ccem_consularassistancere_fused
	,act.ccem_appealdecision
	,act.ccem_previouscontact_date
	,act.ccem_release
	,act.ccem_itoo_requested
	,act.ccem_itoo_informed
	,cast(act.[ccem_identification] AS VARCHAR(255)) AS [arrest_detention_id]

                   ,cast( act.createdby as varchar(255)) as [CREATED_BY_ID_ACTIV]
                   ,cast( tr.createdby as varchar(255)) as [CREATED_BY_ID_TRANS]

                      ,CASE
                    when act.ccem_start IS NOT NULL and act.ccem_typename ='Prison Visit' then 1 ELSE 0
                    END as VISIT_CNT
	
	,ctc.[ccem_othercitizenship1name]
	,null as [distinct_prisoner_cnt]
	,getdate() AS [etl_crea_dt]
	,getdate() AS [etl_updt_dt]
	



FROM [dbo].[ccem_arrest_activity] act
full join  [dbo].[ccem_arrest_transfer] tr 
	ON act.[ccem_case] = tr.[ccem_case] 
		and act.ccem_start between coalesce(tr.ccem_date_start,cast('1900-01-01' as date)) and coalesce(tr.ccem_date_end,cast('2100-01-01' as date))
LEFT JOIN [dbo].[ccem_arrest] ar 
    ON coalesce (act.[ccem_case], tr.[ccem_case]) = ar.[ccem_case] 
LEFT JOIN [dbo].[contact] ctc ON ctc.[contactid] = ar.[ccem_contact]
 
LEFT JOIN 
  (
	  select distinct *
	  from  [ODS_CCEM].[dbo].[stringmap]
	  where [attributename]='ccem_type' and [objecttypecode]='ccem_arrest_activity' and [langid]=1036
  ) str_map
  ON act.[ccem_type]=str_map.[attributevalue]

order by [ccem_case], [ccem_arrestid],  [ccem_arrest_activityid] ,   [ccem_arrest_transferid]
```

```sql
-- OLEDB_S_CCEM_ARREST_ACTIVITY_VISIT (DFT- S_CCEM_ARREST_DETENTION)
SELECT DISTINCT 

	 cast(ar.[ccem_case] AS VARCHAR(255)) AS [ccem_case]
                   , cast(ar.[ccem_arrestid] AS VARCHAR(255)) AS [ccem_arrestid]
	,cast(act.[ccem_arrest_activityid] AS VARCHAR(255)) AS [ccem_arrest_activityid]
	,cast(tr.[ccem_arrest_transferid] AS VARCHAR(255)) AS [ccem_arrest_transferid]

	--,tr.[ccem_prisonernumber]
	--,tr.[ccem_date_start]
                  -- ,act.[ccem_start]

	, Row_number () OVER (PARTITION BY ar.[ccem_case] order by tr.[ccem_date_start] DESC)  as LATEST_DETENTION_ROW 
                  ,  Row_number () OVER (PARTITION BY ar.[ccem_case] order by act.[ccem_start] DESC)  as LATEST_VISIT_ROW 



FROM [dbo].[ccem_arrest_activity] act
full join  [dbo].[ccem_arrest_transfer] tr 
	ON act.[ccem_case] = tr.[ccem_case] 
		and act.ccem_start between coalesce(tr.ccem_date_start,cast('1900-01-01' as date)) and coalesce(tr.ccem_date_end,cast('2100-01-01' as date))
LEFT JOIN [dbo].[ccem_arrest] ar 
    ON coalesce (act.[ccem_case], tr.[ccem_case]) = ar.[ccem_case] 

    
order by [ccem_case], [ccem_arrestid], [ccem_arrest_activityid],[ccem_arrest_transferid]
```

```sql
-- OLEDB_SRC_ccem_arrest_transfer (DFT- S_CCEM_ARREST_TRANSFER)
SELECT DISTINCT cast(tra.[ccem_arrest] AS VARCHAR(255)) AS [ARREST_ID]
	,cast(tra.[ccem_arrest_transferid] AS VARCHAR(255)) AS [ARREST_TRANSFER_ID]
	,cast(tra.[ccem_identification] AS VARCHAR(255)) AS [IDENTIFICATION]
	,cast(tra.[ccem_case] AS VARCHAR(255)) AS [CASE_ID]
	,tra.[ccem_casename] AS [CASE_NM]
	,cast(tra.[ccem_prison] AS VARCHAR(255)) AS [PRISON]
	,tra.[ccem_prisonernumber] AS [PRISONER_NBR]
	,tra.[ccem_prisonname] AS [PRISON_NM]
	,[ccem_date_start]  AS [DETENTION_START_DT]
	,[ccem_date_end]  AS [DETENTION_END_DT]
	,[ccem_status_detentionname] AS [DETENTION_STATUS_NM_EN]
	,[ccem_status_verdictname] AS [VERDICT_STATUS_NM_EN]
	,sta_det.value AS [DETENTION_STATUS_NM_FR]
	,sta_ver.value AS [VERDICT_STATUS_NM_FR]
	,getdate() AS [etl_crea_dt]
	,getdate() AS [etl_updt_dt]
FROM [dbo].[ccem_arrest_transfer] tra
LEFT JOIN (
	SELECT DISTINCT *
	FROM [dbo].[stringmap]
	WHERE objecttypecode = 'ccem_arrest_transfer'
		AND [attributename] = 'ccem_status_detention'
		AND [langid] = 1036
	) sta_det ON tra.[ccem_status_detention] = sta_det.[attributevalue]
LEFT JOIN (
	SELECT DISTINCT *
	FROM [dbo].[stringmap]
	WHERE objecttypecode = 'ccem_arrest_transfer'
		AND [attributename] = 'ccem_status_verdict'
		AND [langid] = 1036
	) sta_ver ON tra.[ccem_status_verdict] = sta_ver.[attributevalue]
```

```sql
-- OLEDB_SRC_ccem_case (DFT- S_CCEM_CASE)
select distinct 

c.[name] as ORGANIZATION_NM
, c.[description] as ORGANIZATION_DESCR
, cast(c.[accountid] as varchar(255) ) as [ORGANIZATION_ID]
, c.[address1_composite] as COMPOSITE_ADDRESS_TXT
, cast(c.[ccem_address1country] as varchar(255) ) as [COUNTRY_ID]
, cast(c.[ccem_mission] as varchar(255) ) as [MISSION_ID]
, c.[ccem_organizationcategory] as [CATEGORY_NBR]
, c.[ccem_organizationtype] as [TYPE_NBR]
  ,case 
      when isnumeric(c.[ccem_subcategories]) = 1 then 
              cast(c.[ccem_subcategories] AS int)
      else  NULL
  End as SUB_CATEGORY_NBR
, c.[statecode] as [STATE_NBR]
, c.[statuscode] as [STATUS_NBR]
--from prison
      ,cast ([ccem_caseid] as varchar(255) ) as [CASE_ID]
	  ,cast ([address1_addressid] as varchar(255)) as [address1_addressid]    
--	  ,[address1_country]
       ,[address1_county]
      ,[address1_city]
      ,[address1_stateorprovince]
      ,[address1_telephone1]
      ,[address1_composite]
	  ,[description]
                    ,[address1_fax]
--	  ,[name]
	  ,[address1_name]
      ,[address1_postalcode]
      ,[ccem_address1_additionaldetails]
     ,[address1_latitude]
      ,[address1_longitude]
      ,[address1_line1]
      ,[address1_line2]
      ,[address1_line3]
--      ,cast ( [ccem_address1country]as varchar(255)) as  [ccem_address1country]
      ,[ccem_address1countryname]     
--      ,cast ( [ccem_mission] as varchar(255)) as  [ccem_mission]	
      ,[ccem_missionname]
   --   ,[ccem_subcategories]
, getdate() as ETL_CREA_DT
, getdate() as ETL_UPDT_DT
,coalesce(f.ccem_requested,0.0 ) as CCEM_REQUESTED
from dbo.ccem_case  c
left outer join dbo.ccem_fund f
on c.ccem_caseid = f.ccem_case
where [ccem_caseid]   is not NULL
```

```sql
-- OLEDB_SRC_S_CCEM_SUB_CASE (DFT- S_CCEM_CASE)
WITH derivedTable
AS
(
    SELECT  [SUBCATEGORY_CASE_ID]
      ,[CASE_ID]
      ,[SUB_CASE_IDENTIFICATION]
      ,[SUB_CASE_NM]
      ,[SUB_CONTACT_ID]
      ,[SUB_CASE_COUNTER_VALUE]
      ,[POLICE_REPORT_DT]
      ,[POLICE_REPORT_TXT]
      ,[SUB_CASE_KEYWORD_TXT]
      ,[SUB_CASE_DETAILES_TXT]
      ,[SUB_CASE_DT]
      ,[SUB_CASE_START_DT]
      ,[SUB_CASE_END_DT]
      ,[SUB_CASE_OWER_ID]
      ,[SUB_CASE_INPUT_TABLE]
      ,[SUB_CREAT_BY_ID]
      ,[SUB_CREAT_ON_DT]
      ,[SUB_MODIFIED_BY_ID]
      ,[SUB_MODIFIED_ON_DT]
      ,ROW_NUMBER() OVER (Partition By [CASE_ID] ORDER BY [SUB_MODIFIED_ON_DT] DESC) rn
    FROM    dbo.CCEM_SUB_CASE
)
SELECT  [SUBCATEGORY_CASE_ID]
      ,[CASE_ID]
      ,[SUB_CASE_IDENTIFICATION]
      ,[SUB_CASE_NM]
      ,[SUB_CONTACT_ID]
      ,[SUB_CASE_COUNTER_VALUE]
      ,[POLICE_REPORT_DT] as [SUB_POLICE_REPORT_DT]
      ,[POLICE_REPORT_TXT] as [SUB_POLICE_REPORT_TXT]
      ,[SUB_CASE_KEYWORD_TXT]
      ,[SUB_CASE_DETAILES_TXT] as [SUB_CASE_DETAILS_TXT]
      ,[SUB_CASE_DT]
      ,[SUB_CASE_START_DT]
      ,[SUB_CASE_END_DT]
      ,[SUB_CASE_OWER_ID]
      ,[SUB_CASE_INPUT_TABLE]
      ,[SUB_CREAT_BY_ID]
      ,[SUB_CREAT_ON_DT]
      ,[SUB_MODIFIED_BY_ID]
      ,[SUB_MODIFIED_ON_DT] 
FROM    derivedTable
WHERE   derivedTable.rn = 1
```

```sql
-- OLEDB_SRC_systemuser1 (DFT- S_CCEM_CASE_EMPLOYEE)
SELECT DISTINCT 

cast ([systemuserid] as varchar(255) ) as [EMPLOYEE_ID]
,[yomifullname] as [YOMI_FULL_NM]
,cast ([address1_addressid]as varchar(255) ) as [ADDRESS]
,cast ([address2_addressid]as varchar(255) ) as [ADDRESS_2]
,[address1_telephone1] as [OTHER_PHONE]
,cast ([calendarid]as varchar(255) ) as [CALENDAR_ID]
,cast ([ccem_mission]as varchar(255) ) as [MISSION_ID]
,[ccem_missionname] as [MISSION_NM]
,cast ([createdby]as varchar(255) ) as [CREATED_BY_ID]
,[createdbyname] as [CREATED_BY]
,[createdon] as [CREATED_ON]
,[defaultmailboxname] as [MAILBOX_NM]
,[domainname] as [USER_NM]
,[firstname] as [FIRST_NM]
,[fullname] as [FULL_NM]
,[internalemailaddress] as [PRIMARY_EMAIL]
,[lastname] as [LAST_NM]
,cast ([modifiedby]as varchar(255) ) as [MODIFIED_BY_ID]
,[modifiedbyname] as [MODIFIED_BY]
,[accessmodename] as [ACCESS_MODE]
,[businessunitidname] as [BUSINESS_UNIT]
,[ccem_callorder] as [CALL_ORDER]
,[createdonbehalfbyname] as [CREATED_BY_DELEGATE]
,[preferredaddresscodename] as [PREFERRED_ADDRESS]
,[homephone] as [HOME_PHONE]
,[userlicensetype] as [LICENSE_TYPE]
,[preferredphonecodename] as [PREFERRED_PHONE]
,[middlename] as [MIDDLE_NM]
,[mobilealertemail] as [MOBILE_ALERT_EMAIL]
,[mobilephone] as [MOBILE_PHONE]
,[modifiedonbehalfbyname] as [MODIFIED_BY_DELEGATE]
,[modifiedon] as [MODIFIED_ON]
,[organizationidname] as [ORGANIZATION_NM]
,[siteidname] as [ORG_SITE]
,[territoryidname] as [ORG_TERRITORY]
,[positionidname] as [POSITION]
,[title] as [TITLE]
,getdate()  as  ETL_CREA_DT
,getdate()  as  ETL_UPDT_DT

from dbo.systemuser
```

```sql
-- OLEDB_SRC_ccem_mission (DFT- S_CCEM_MISSION)
select distinct 

cast ([ccem_missionid] as varchar(255) ) as [MISSION_ID],
[ccem_missiontype] as [MISSION_TYPE_ID],
[ccem_missiontypename] as [MISSION_TYPE_NM],
[ccem_abbreviation] as [ABBREVIATION],
[ccem_address_city] as [ADDR_CITY],
cast ( [ccem_address_country] as varchar(255) ) as [ADDR_COUNTRY_ID],
[ccem_address_countryname] as [ADDR_COUNTRY_NM],
[ccem_address_line1] as [ADDR_LINE1],
[ccem_address_postalcode] as [ADDR_POSTAL_CD],
cast ( [ccem_addresscountrysubdivision] as varchar(255) ) as [ADDR_COUNTRY_SUBDIVISION_ID],
[ccem_addresscountrysubdivisionname] as [ADDR_COUNTRY_SUBDIVISION_NM],
[ccem_directions] as [DIRECTIONS_TXT],
[ccem_email] as [EMAIL],
[ccem_fax] as [FAX],
[ccem_identification] as [IDENTIFICATION],
[ccem_identificationenglish] as [IDENTIFICATION_EN],
[ccem_identificationfrench] as [IDENTIFICATION_FR],
[ccem_mailing_city] as [MAILING_CITY],
cast ( [ccem_mailing_country] as varchar(255) ) as [MAILING_COUNTRY_ID],
[ccem_mailing_countryname] as [MAILING_COUNTRY_NM],
[ccem_mailing_line1] as [MAILING_LINE1],
[ccem_mailing_postalcode] as [MAILING_POSTAL_CD],
cast ( [ccem_mailingcountrysubdivision] as varchar(255) ) as [MAILING_COUNTRY_SUBDIVISION_ID],
[ccem_mailingcountrysubdivisionname] as [MAILING_COUNTRY_SUBDIVISION_NM],
[ccem_oldid] as [OLD_ID],
[ccem_phone] as [PHONE],
[ccem_specialinstructions] as [SPECIAL_INSTRUCTIONS_TXT],
cast ( [ccem_supervisingmission] as varchar(255) ) as [SUPERVISING_MISSION_ID],
[ccem_supervisingmissionname] as [SUPERVISING_MISSION_NM],
cast ( [ccem_team] as varchar(255) ) as [TEAM_ID],
[ccem_teamname] as [TEAM_NM],
cast ( [createdby] as varchar(255) ) as [CREATED_BY_ID],
[createdbyname] as [CREATED_BY_NM],
[createdon] as [CREATED_ON_DT],
cast ( [modifiedby] as varchar(255) ) as [MODIFIED_BY],
[modifiedbyname] as [MODIFIED_BY_NM],
[modifiedon] as [MODIFIED_ON_DT],
cast ( [organizationid] as varchar(255) ) as [ORGANIZATION_ID],
[organizationidname] as [ORGAN