## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| Excel Connection Manager         | EXCEL           | Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\Users\\admLIUJ6\\source\\Workspaces\\Workspace\\SWS Modernization\\Sprint_79\\D_WBS_LEVEL_2.xlsx;Extended Properties="EXCEL 12.0 XML;HDR=YES"; | Source data (Excel file)                                               | Access to the file system. Requires appropriate permissions to read the Excel file.                                                                | None                 | Part 1                  |
| Flat File Connection Manager      | FLATFILE        | C:\\Users\\admLIUJ6\\source\\Workspaces\\Workspace\\SWS Modernization\\Sprint_79\\d_proj_wbs_level_2.csv                                                                                       | Source data (CSV file)                                                  | Access to the file system. Requires appropriate permissions to read the CSV file.                                                                 | None                 | Part 1                  |
| Flat File Connection Manager 1  | FLATFILE        | C:\\Users\\admLIUJ6\\source\\Workspaces\\Workspace\\SWS Modernization\\Sprint_79\\d_proj_wbs_level_2.csv                                                                                       | Source data (CSV file) with column names in the first row.             | Access to the file system. Requires appropriate permissions to read the CSV file.                                                                 | None                 | Part 1                  |
| Flat File Connection Manager 2  | FLATFILE        | C:\\Users\\admLIUJ6\\source\\Workspaces\\Workspace\\SWS Modernization\\Sprint_79\\d_proj_wbs_level_2_1.txt                                                                                     | Source data (TXT file) with column names in the first row.             | Access to the file system. Requires appropriate permissions to read the TXT file.                                                                 | None                 | Part 1                  |
| DATA_HUB | OLE DB | Server=*; Database=DATA_HUB; Authentication=Windows Authentication (Implied) | Source database for dimension data. Source for SAP Project WBS data | Windows Authentication. Ensure the account has read permissions.  Credentials to access the DATA_HUB database  | None apparent| Part 2, 3                  |
| MART_GC | OLE DB | Server=*; Database=MART_GC; Authentication=Windows Authentication (Implied) | Destination database for dimension data, updating D_GEOGRAPHIC_REGION | Windows Authentication. Ensure the account has read/write permissions. Credentials to access the MART_GC database  | None apparent | Part 2, 3                  |
| ETL_STG_MART_GC | OLE DB | Server, Database | Source for S_PROJECT_BROWSER_STATUS data | Credentials to access the ETL_STG_MART_GC database | None apparent | Part 3                  |

## 2. Package Dependencies

```markdown
| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|
```

## 3. Package Flow Analysis

*   **Control Flow:**
    1.  `EXPRESSIONT_DMART- CD-Start Task Each branch depends on value in package parameter - ProcessDataFlowNode 1` : An expression task that evaluates the expression `1 == 1`. (Part 1)
    2.  `SEQC-Load_DATA_MART-CommonDims`: A sequence container that contains tasks for loading data into common dimensions. (Part 1)
        *   `SEQC_D_CFO_STATS_INTL_COMMIT`: Loads data into the `D_CFO_STATS_INTL_COMMIT` dimension table.
            *   `ESQLT-Truncate truncate table D_CFO_STATS_INTL_COMMIT`: Truncates the `D_CFO_STATS_INTL_COMMIT` table.
            *   `DFT-D_CFO_STATS_INTL_COMMIT`: Data flow task to load data into the table.
        *   `SEQC_D_COM_DATE_UPDT`: Updates the `D_COM_DATE` dimension table with current fiscal year information.
            *   `ESQLT-UPDATE_D_COM_DATE_CURRENT_FY`: Executes an SQL update statement.
        *   `SEQC_D_COUNTRY`: Loads data into the `D_COUNTRY` dimension table.
            *   `ESQLT-Truncate truncate table D_COUNTRY`: Truncates the table.
            *   `ESQLT - Insert Unknow Record to D_COUNTRY`: Inserts an "unknown" record into the `D_COUNTRY` table.
            *   `DFT-D_COUNTRY x`: Data flow task to load data into the table.
            *   `DFT-Insert_Region_As_Country_To_D_COUNTRY`: Data flow task to insert region data to D_COUNTRY table.
        *   `SEQC_D_COUNTRY_old`: *Disabled* Sequence Container (potentially an older implementation of the D\_COUNTRY load)
        *   `SEQC_D_FUND`: Loads data into the `D_FUND` dimension table.
            *   `ESQLT-Truncate truncate table D_FUND`: Truncates the table.
            *   `ESQLT_Insert_Unknow Record`: Inserts an "unknown" record into the `D_FUND` table.
            *   `DFT-D_FUND`: Data flow task to load data into the table.
        *   `SEQC_D_FUND_CENTRE`: Loads data into the `D_FUND_CENTRE` dimension table.
            *   `ESQLT-Truncate truncate table D_FUND_CENTRE`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_FUND_CENTRE`: Inserts an "unknown" record into the `D_FUND_CENTRE` table.
            *   `DFT-D_FUND_CENTRE`: Data flow task to load data into the table.
        *   `SEQC_D_GEO_REGION`: Loads data into the `D_GEO_REGION` dimension table.
            *   `ESQLT-Truncate truncate table D_GEOGRAPHIC_REGION`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_GEOGRAPHIC_REGION`: Inserts an "unknown" record.
            *   `DFT-D_GEOGRAPHIC_REGION`: Data flow task to load data into the table.
        *   `SEQC_D_PARTNER`: Loads data into the `D_PARTNER` dimension table.
            *   `ESQLT-Truncate truncate table D_PARTNER`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_PARTNER`: Inserts an "unknown" record.
            *   `DFT-D_PARTNER`: Data flow task to load data into the table.
        *   `SEQC_D_PROGRAM`: Loads data into the `D_PROGRAM` dimension table.
            *   `ESQLT-Truncate truncate table D_PROGRAM`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_PROGRAM`: Inserts an "unknown" record.
            *   `DFT-D_PROGRAM`: Data flow task to load data into the table.
        *   `SEQC_D_PROJECT`: Loads data into the `D_PROJECT` dimension table.
            *   `ESQLT-Truncate truncate table D_PROJECT`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_PROJECT`: Inserts an "unknown" record.
            *   `DFT-D_PROJECT`: Data flow task to load data into the table.
        *   `SEQC_D_RESP_ORG`: Loads data into the `D_RESP_ORG` dimension table.
            *   `ESQLT-Truncate truncate table D_RESP_ORG`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_RESP_ORG`: Inserts an "unknown" record.
            *   `DFT-D_RESP_ORG`: Data flow task to load data into the table.
        *   `SEQC_D_SUPPLIER`: Loads data into the `D_SUPPLIER` dimension table.
            *   `ESQLT-Truncate truncate table D_SUPPLIER`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_SUPPLIER`: Inserts an "unknown" record.
            *   `DFT-D_SUPPLIER`: Data flow task to load data into the table.
        *   `SEQC_D_WBS_L1`: Loads data into the `D_WBS_L1` dimension table.
            *   `ESQLT-Truncate truncate table D_WBS_L1`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_WBS_L1`: Inserts an "unknown" record.
            *   `DFT-D_WBS_L1`: Data flow task to load data into the table.
        *   `SEQC_D_WBS_L2`: Loads data into the `D_WBS_L2` dimension table.
            *   `ESQLT-Truncate truncate table D_WBS_L2`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_WBS_L2`: Inserts an "unknown" record.
            *   `DFT-D_WBS_L2`: Data flow task to load data into the table.
        *   `SEQC_D_GEO_REGION`: Loads data into the `D_GEO_REGION` dimension table.
            *   `ESQLT-Truncate truncate table D_GEOGRAPHIC_REGION`: Truncates the table.
            *   `ESQLT- Insert Unknow Record to D_GEOGRAPHIC_REGION`: Inserts an "unknown" record to the table.
            *   `DFT-D_GEOGRAPHIC_REGION`: Data flow task to load data into the table.
        *   `SEQC-Load_DATA_MART-CommonDims\\SEQC_D_IM_PROGRAM_POSITION`: Loads the `D_IM_PROGRAM_POSITION` dimension table. (Part 2)
            *   `ESQLT-Truncate truncate table D_IM_PROGRAM_POSITION`: Truncates the destination table.
            *   `ESQLT_Insert_Unknow Record_D_IM_PROGRAM_POSITION`: Inserts a default "Uncoded" or "Unknown" record.
            *   `DFT-D_IM_PROGRAM_POSITION`: Loads the table.
        *   `SEQC-Load_DATA_MART-CommonDims\\SEQC_D_LOAN`: Loads the `D_LOAN` dimension table. (Part 2)
            *   `ESQLT-Truncate_table_D_LOAN`: Truncates the destination table.
            *   `DFT-D_LOAN_GAC`: Loads the `D_LOAN` table for GAC.
            *   `DFT-D_LOAN_NON_GAC`: Loads the `D_LOAN` table for NON GAC.
            *   `ESQLT-Set_NULL_D_LOAN`: Inserts a default "Uncoded" or "Unknown" record.
    3.  `SEQC-Load_DATA_MART-CommonDims\\SEQC_D_PROJECT_WBS` (Part 3)
        *   `ESQLT-Truncate ETL_STG_MART_GC Tables` (Execute SQL Task)
        *   `DFT-S_PROJECT_BROWSER_STATUS` (Data Flow Task)
        *   `DFT-Insert_D_PROJECT_WBS` (Data Flow Task)
        *   `DFT-Insert_D_PROJECT_WBS_before_2024_09_17` (Data Flow Task, Disabled)

*   **Data Flow Tasks:**
    *   The data flow tasks (`DFT-*`) generally follow a pattern of (Part 1):
        1.  **Source:** OLE DB Source reading data from a view in the `DATA_HUB` database or other source.
        2.  **Transformation:** Data Conversion (if any).
        3.  **Destination:** OLE DB Destination writing data to a dimension table in the `MART_GC` database.

#### DFT-D_GEO_REGION (Part 2)
*   **Source:** Extracts data using a complex SQL query.
*   **Transformations:** Data Conversion
*   **Destination:** Loads data into the `D_GEOGRAPHIC_REGION` table.

#### DFT_UPDATE_D_GEO_REGION (Part 2)
*   **Source:** Extracts data using a SQL query
*   **Transformation:** None
*   **Destination:** Updates data into the `D_GEOGRAPHIC_REGION` table.

#### DFT-D_IM_PROGRAM_POSITION (Part 2)
*   **Source:** Extracts data using a SQL query.
*   **Transformation:** None
*   **Destination:** Loads data into the `D_IM_PROGRAM_POSITION` table.

#### DFT-D_LOAN_GAC (Part 2)
*   **Source:** Extracts data from `SAP_LOAN_PROFILE` using a SQL query.
*   **Transformations:** Data Conversion.
*   **Destination:** Loads data into the `D_LOAN` table.

#### DFT-D_LOAN_NON_GAC (Part 2)
*   **Source:** Extracts data from `SAP_LOAN_PROFILE` using a SQL query.
*   **Transformations:** Data Conversion.
*   **Destination:** Loads data into the `D_LOAN` table.

#### DFT-S_PROJECT_BROWSER_STATUS (Part 3)
*   **Source:** `OLEDB_SRC_SAP_PROJECT_WBS` (OLE DB Source) reading data from `SAP_PROJECT_WBS_CHANGE_STATUS` table in the `ETL_STG_MART_GC`
*   **Destination:** `OLEDB_DEST_S_PROJECT_BROWSER_STATUS` (OLE DB Destination).  Target table is `S_PROJECT_BROWSER_STATUS` in the `ETL_STG_MART_GC` database.
*   **Transformations:** No explicit transformations are present inside the data flow task.

#### DFT-Insert_D_PROJECT_WBS (Part 3)
*   **Source:** `OLE DB DATA_HUB_SAP_PROJECT_WBS` (OLE DB Source), reading data from a SQL query.
*   **Destination:** `OLE DB_Load_MART_GC_D_PROJECT_WBS` (OLE DB Destination). Target table is `D_PROJECT_WBS` in the `MART_GC` database.
*   **Transformations:**
    *   `TRSFM_LKPT_S_PROJECT_BROWSER_STATUS`: Lookup transformation to retrieve Project Browser Status information.
    *   `TRFM_DRV_WBS_BROWSER`: Derived Column transformation to handle null values for Project Browser Status.

#### DFT-Insert_D_PROJECT_WBS_before_2024_09_17 (Part 3)
*   **Status**: Disabled
*   **Source:** `OLE DB DATA_HUB_SAP_PROJECT_WBS` (OLE DB Source), reading data from a SQL query.
*   **Destination:** N/A
*   **Transformations:** N/A

#### Error Handling and Logging (Part 1, 2, 3):
*   Error handling is mostly configured at component level with `errorRowDisposition="FailComponent"`.
*   Each `OLE DB Destination` component has an "Error Output" configured to fail the component if errors occur during insertion.
*   Each `OLE DB Source` component has an "Error Output" configured to fail the component if errors occur during extraction.
*   `Execute SQL Task` has property `FailPackageOnFailure` set to `True`
*   SQL Tasks update the ETL\\_RUN\\_STATUS table with FAILED status.
*   The package utilizes variables to log the status of the ETL process.
    *   `V_SQL_INSERT_ON_PRE_EXECUTE`: SQL statement to insert a "RUNNING" status into the `ETL_RUN_STATUS` table before package execution.
    *   `V_SQL_UPDATE_ON_POST_EXECUTE`: SQL statement to update the `ETL_RUN_STATUS` table with a "SUCCEEDED" status after successful execution.
    *   `V_SQL_UPDATE_ON_ERROR`: SQL statement to update the `ETL_RUN_STATUS` table with a "FAILED" status if an error occurs.

#### Sequence Containers (Part 1, 2, 3):
*   Sequence containers (`SEQC-*`) are used to group related tasks, typically including a truncate task, "unknown record" insert, and a data flow task.
*   This pattern suggests a full load strategy where dimension tables are truncated and re-populated with data from the source.

## 4. Code Extraction

```sql
-- From OLE DB Source in DFT-D_CFO_STATS_INTL_COMMIT (Part 1)
SELECT  [APPROVAL_FY]
      ,[CCPM]
      ,[Partner Classification]
      ,[FISCAL_YR]
      ,[CONTINENT]
      ,cast([AMOUNT] as decimal (38,15)) as AMOUNT
      ,[AF_DEV_AMT]
      ,[AF_SEC_AMT]
      ,[AMAZON_FIRE_AMT]
      ,[BEIRUT_AMT]
      ,[CARE_WORK_AMT]
      ,[CARIB100_AMT]
      ,[CC_AMT]
      ,[CCPOST2020_AMT]
      ,[CL_ELECTION_AMT]
      ,[CL_TAP_AMT]
      ,[CL_CFLI_AMT]
      ,[CORE_AMT]
      ,[COVID_19P_AMT]
      ,cast([COVID_19R_AMT] as decimal (38,15)) as [COVID_19R_AMT]
      ,cast([ELSIE_AMT] as decimal (38,15)) as [ELSIE_AMT]
      ,[EQUALITY_AMT]
      ,cast([FAC_AMT] as decimal (38,15)) as [FAC_AMT]
      ,[G7ED_AMT]
      ,[G7OCEAN_AMT]
      ,[GAVI_AMT]
      ,[GFATM_AMT]
      ,cast([GH_HEALTH_AMT] as decimal (38,15)) as [GH_HEALTH_AMT]
      ,cast([GH_SRHR_AMT] as decimal (38,15)) as [GH_SRHR_AMT]
      ,[GPE_AMT]
      ,cast([GPEI_100_AMT] as decimal (38,15)) as [GPEI_100_AMT]
      ,cast([HAIYAN_RF_AMT] as decimal (38,15)) as [HAIYAN_RF_AMT]
      ,[HA_AMT]
      ,[IAIP_AMT]
      ,LGBTQ2_AND_INTERSEX_PERSONS_DEVELOPMENT
      ,LGBTQ2_AND_INTERSEX_PERSONS_SECURITY
      ,cast([MNCH2_AMT] as decimal (38,15)) as [MNCH2_AMT]
      ,cast([MES_IHA_AMT] as decimal (38,15)) as [MES_IHA_AMT]
      ,[MES_DEV_AMT]
      ,cast([MES_SEC_AMT] as decimal (38,15)) as [MES_SEC_AMT]
      ,cast([MES_DND_AMT] as decimal (38,15)) as [MES_DND_AMT]
      ,[NERF_AMT]
      ,[ROHINGYA_RF_AMT]
      ,[ROHINGYA300_AMT]
      ,[SMO_AMT]
      ,cast([SRHR_AMT] as decimal (38,15)) as [SRHR_AMT]
      ,[SRHRB_AMT]
      ,[SYRIA_AMT]
      ,[TUNISIA_AMT]
      ,[UKRAINE_AMT]
      ,[VE_AMT]
      ,[WBG_2019_AMT]
      ,[WBG_2009_AMT]
      ,cast([WVL_AMT]  as decimal (38,15)) as [WVL_AMT]
      ,cast([WVL2_AMT] as decimal (38,15)) as [WVL2_AMT]
      ,[ED10_AMT]
      ,[GE3_AMT]
      ,[TOTAL_INTL_COMMITMENT_AMT]
      ,[OVERLAP_AMT]
      ,[NON_COMMITMENT_AMT]
      ,cast([OUTSIDE_AMT] as decimal (38,15)) as [OUTSIDE_AMT]
      ,[SSA_AMT]
      ,[EMPOWER_AMT]
      ,cast([OUTSIDE_FIAP_AMT] as decimal (38,15)) as [OUTSIDE_FIAP_AMT]
      ,[DISBURSED_PCT]
      ,[FUND_TYPE_NM]
      ,[TFUND_NM]
      ,[GPEI_AMT]
      ,[NUTRITION_AMT]
      ,[PAKISTAN_FLOODS_AMT]
      ,[SLP_AMT]
      ,[UKRAINE_DEV_AMT]
      ,[SSA_HUNGER_CRISIS_AMT]
      ,[TURKIYE_AMT]
      ,[GC_FINAN_CFO_STATS_SID] ,
      INDOPAC_AMT,
    BIODIVERSITY_AMT,
GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT
from DBO.SAP_CFO_STATS_INTL_COMMIT_VW
```

```sql
-- From Execute SQL Task in SEQC_D_CFO_STATS_INTL_COMMIT (Part 1)
truncate table D_CFO_STATS_INTL_COMMIT ;
```

```sql
-- From Execute SQL Task in SEQC_D_COM_DATE_UPDT (Part 1)
  Update [MART_GC].[dbo].[D_COM_DATE]
  SET
       [ETL_CREA_DT] =getdate()
      ,[ETL_UPDT_DT] = getdate()
      ,[CURRENT_CALENDAR_YR] =  cast(YEAR(GETDATE()) as int)
   ,[CURRENT_FISCAL_YR] = CASE
                          when MONTH(GETDATE()) >= 4 and MONTH(GETDATE()) <= 12
             THEN  cast(YEAR(GETDATE()) as int) + 1
        when  MONTH(GETDATE()) in (1, 2, 3)
              THEN  cast(YEAR(GETDATE()) as int)
        END
  FROM [MART_GC].[dbo].[D_COM_DATE]
```

```sql
-- From OLE DB Source in DFT-D_COUNTRY x (Part 1)
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT  CAST([GAC_COUNTRY_CD] AS NVARCHAR(30)) AS [GAC_COUNTRY_CD]
      ,CAST([ISO3_COUNTRY_CD] AS NVARCHAR(30)) AS [ISO3_COUNTRY_CD]
      ,[COUNTRY_EN_NM]
      ,[COUNTRY_FR_NM]
      ,CAST([COUNTRY_LEVEL_CD] AS NVARCHAR(30)) AS [COUNTRY_LEVEL_CD]
      ,CAST([COUNTRY_INTERVENTION_CD] AS NVARCHAR(30)) AS [COUNTRY_INTERVENTION_CD]
      ,CAST([COUNTRY_ODA_CD] AS NVARCHAR(30)) AS [COUNTRY_ODA_CD]
      ,CAST([COUNTRY_ACTIVE_CD] AS NVARCHAR(30)) AS[COUNTRY_ACTIVE_CD]
      ,[COUNTRY_LONG_EN_NM]
      ,[COUNTRY_LONG_FR_NM]
      ,[COUNTRY_COMMON_EN_NM]
      ,[COUNTRY_COMMON_FR_NM]
      ,CAST([DAC_COUNTRY_CD] AS NVARCHAR(30)) AS [DAC_COUNTRY_CD]
      ,CAST([GEO_REGION_PARENT_CD] AS NVARCHAR(30)) AS [GEO_REGION_PARENT_CD]
      ,CAST([COUNTRY_LEVEL_EN_DESCR] AS NVARCHAR(120)) AS [COUNTRY_LEVEL_EN_DESCR]
      ,CAST([COUNTRY_LEVEL_FR_DESCR] AS NVARCHAR(120)) AS [COUNTRY_LEVEL_FR_DESCR]
      ,CAST([COUNTRY_INTERVENTION_EN_DESCR] AS NVARCHAR(120)) AS [COUNTRY_INTERVENTION_EN_DESCR]
      ,CAST([COUNTRY_INTERVENTION_FR_DESCR] AS NVARCHAR(120)) AS [COUNTRY_INTERVENTION_FR_DESCR]
      ,CAST([COUNTRY_ACTIVE_EN_DESCR] AS NVARCHAR(120)) AS [COUNTRY_ACTIVE_EN_DESCR]
      ,CAST([COUNTRY_ACTIVE_FR_DESC] AS NVARCHAR(120)) AS [COUNTRY_ACTIVE_FR_DESC]
      ,CAST([COUNTRY_ODA_EN_DESCR] AS NVARCHAR(120)) AS [COUNTRY_ODA_EN_DESCR]
      ,CAST([COUNTRY_ODA_FR_DESCR] AS NVARCHAR(120)) AS [COUNTRY_ODA_FR_DESCR]
      ,GETDATE() AS [ETL_CREA_DT]
      ,GETDATE() AS [ETL_UPDT_DT]
  FROM [dbo].[SAP_GEO_COUNTRY]
```

```sql
-- From OLE DB Source in DFT-Insert_Region_As_Country_To_D_COUNTRY (Part 1)
SELECT  CAST([GEO_REGION_CD] AS NVARCHAR(30))  AS GAC_COUNTRY_CD
      ,CAST([GEO_REGION_EN_NM] AS NVARCHAR(80)) AS COUNTRY_EN_NM
      ,CAST([GEO_REGION_FR_NM]  AS NVARCHAR(80)) AS COUNTRY_FR_NM
	  ,CAST([GEO_REGION_PARENT_CD] AS NVARCHAR(30)) as  [GEO_REGION_PARENT_CD]

	  ---To replace the 00380 value to 01031 value in DAC_COUNTRY_CD under client request ,
	  ---by Julian 2023-09-29
	  ,CASE
		WHEN  CAST(LTRIM(RTRIM([DAC_REGION_CD])) AS NVARCHAR(30)) = '00380' then '01031'
		ELSE  CAST(LTRIM(RTRIM([DAC_REGION_CD])) AS NVARCHAR(30))
		END as [DAC_COUNTRY_CD]
      ,GETDATE() AS [ETL_CREA_DT]
      ,GETDATE() AS [ETL_UPDT_DT]
  FROM [dbo].[SAP_GEO_REGION]
```

```sql
-- From Execute SQL Task in SEQC_D_COUNTRY (Part 1)
 SET IDENTITY_INSERT DBO.[D_COUNTRY] ON;

  DELETE FROM DBO.[D_COUNTRY] WHERE [COUNTRY_SID] = -3;

INSERT INTO DBO.[D_COUNTRY]
( [COUNTRY_SID]
      ,[GAC_COUNTRY_CD]
      ,[ISO3_COUNTRY_CD]
      ,[DAC_COUNTRY_CD]
      ,[COUNTRY_EN_NM]
      ,[COUNTRY_FR_NM]
      ,[GEO_REGION_PARENT_CD]
      ,[COUNTRY_ACTIVE_CD]
      ,[COUNTRY_ACTIVE_EN_DESCR]
      ,[COUNTRY_ACTIVE_FR_DESC]
      ,[COUNTRY_COMMON_EN_NM]
      ,[COUNTRY_COMMON_FR_NM]
      ,[COUNTRY_LEVEL_CD]
      ,[COUNTRY_LEVEL_EN_DESCR]
      ,[COUNTRY_LEVEL_FR_DESCR]
      ,[COUNTRY_INTERVENTION_CD]
      ,[COUNTRY_INTERVENTION_EN_DESCR]
      ,[COUNTRY_INTERVENTION_FR_DESCR]
      ,[COUNTRY_LONG_EN_NM]
      ,[COUNTRY_LONG_FR_NM]
      ,[COUNTRY_ODA_CD]
      ,[COUNTRY_ODA_EN_DESCR]
      ,[COUNTRY_ODA_FR_DESCR]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT])
SELECT  -3 as [COUNTRY_SID]
      ,'-3' as [GAC_COUNTRY_CD]
      ,'-3' as [ISO3_COUNTRY_CD]
      ,'-3' as [DAC_COUNTRY_CD]
      ,'Uncode' as [COUNTRY_EN_NM]
      ,'Non codé' as [COUNTRY_FR_NM]
      ,'-3' as [GEO_REGION_PARENT_CD]
      ,'-3' as [COUNTRY_ACTIVE_CD]
      ,'Uncode' as [COUNTRY_ACTIVE_EN_DESCR]
      ,'Non codé' as [COUNTRY_ACTIVE_FR_DESC]
      ,'Uncode' as [COUNTRY_COMMON_EN_NM]
      ,'Non codé' as [COUNTRY_COMMON_FR_NM]
      ,'-3' as [COUNTRY_LEVEL_CD]
      ,'Uncode' as [COUNTRY_LEVEL_EN_DESCR]
      ,'Non codé' as [COUNTRY_LEVEL_FR_DESCR]
      ,'-3' as [COUNTRY_INTERVENTION_CD]
      ,'Uncode' as [COUNTRY_INTERVENTION_EN_DESCR]
      ,'Non codé' as [COUNTRY_INTERVENTION_FR_DESCR]
      ,'Uncode' as [COUNTRY_LONG_EN_NM]
      ,'' as [COUNTRY_LONG_FR_NM]
      ,'-3' as [COUNTRY_ODA_CD]
      ,'Uncode' as [COUNTRY_ODA_EN_DESCR]
      ,'Non codé' as [COUNTRY_ODA_FR_DESCR]
      ,'' as [ETL_CREA_DT]
      ,'' as [ETL_UPDT_DT];

    SET IDENTITY_INSERT DBO.[D_COUNTRY] OFF;
```

```sql
-- From Execute SQL Task in SEQC_D_COUNTRY (Part 1)
truncate table D_COUNTRY;
```

```sql
-- OLE DB Source - DFT-D_GEO_REGION - Extracts data for D_GEOGRAPHIC_REGION (Part 2)
USE DATA_HUB;


---Union Part1 SRC_Continent

SELECT
	-- GEOGRAPHIC_REGION_SID			System Generated
	CASE
		WHEN ROW_NUMBER() OVER (
				PARTITION BY CONTINENT.DAC_REGION_CD ORDER BY CONTINENT.GEO_REGION_CD
				) = 1
			THEN 1
		ELSE 0
		END AS DAC_SID_IND
	,CONTINENT.GEO_REGION_CD AS GAC_GEOGRAPHIC_REGION_CD
	,CONTINENT.DAC_REGION_CD AS DAC_GEOGRAPHIC_REGION_CD
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS GAC_GEOGRAPHIC_REGION_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS GAC_GEOGRAPHIC_REGION_FR_NM
	,LTRIM(RTRIM(dacreg.DAC_CONTINENT_REGION_EN_NM)) AS DAC_GEOGRAPHIC_REGION_EN_NM
	,LTRIM(RTRIM(dacreg.DAC_CONTINENT_REGION_FR_NM)) AS DAC_GEOGRAPHIC_REGION_FR_NM


	,'10' AS GEOGRAPHIC_REGION_LEVEL_CD
	,1 AS GEOGRAPHIC_REGION_LEVEL_NBR
	,'Continent' AS GEOGRAPHIC_REGION_LEVEL_EN_NM
	,'Continent' AS GEOGRAPHIC_REGION_LEVEL_FR_NM


	--	 CONTINENT...
	,CONTINENT.GEO_REGION_CD AS GAC_CONTINENT_CD
	,CONTINENT.DAC_REGION_CD AS DAC_CONTINENT_CD


	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS GAC_CONTINENT_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS GAC_CONTINENT_FR_NM
	,LTRIM(RTRIM(dacreg.DAC_CONTINENT_REGION_EN_NM)) AS DAC_CONTINENT_EN_NM
	,LTRIM(RTRIM(dacreg.DAC_CONTINENT_REGION_FR_NM)) AS DAC_CONTINENT_FR_NM


	--	 SUB_CONTINENT...
	,CONTINENT.GEO_REGION_CD GAC_SUB_CONTINENT_CD
	,CONTINENT.DAC_REGION_CD DAC_SUB_CONTINENT_CD

	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) GAC_SUB_CONTINENT_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) GAC_SUB_CONTINENT_FR_NM
	,LTRIM(RTRIM(dacREG.DAC_CONTINENT_REGION_EN_NM)) AS DAC_SUB_CONTINENT_EN_NM
	,LTRIM(RTRIM(dacREG.DAC_CONTINENT_REGION_FR_NM)) AS DAC_SUB_CONTINENT_FR_NM

	--	 SUB_SUB_CONTINENT...
	,CONTINENT.GEO_REGION_CD GAC_SUB_SUB_CONTINENT_CD
	,CONTINENT.DAC_REGION_CD DAC_SUB_SUB_CONTINENT_CD

	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS GAC_SUB_SUB_CONTINENT_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS GAC_SUB_SUB_CONTINENT_FR_NM
	,LTRIM(RTRIM(dacREG.DAC_CONTINENT_REGION_EN_NM)) AS DAC_SUB_SUB_CONTINENT_EN_NM
	,LTRIM(RTRIM(dacREG.DAC_CONTINENT_REGION_FR_NM)) AS DAC_SUB_SUB_CONTINENT_FR_NM

	--	 COUNTRY...
	,CONTINENT.GEO_REGION_CD AS GAC_COUNTRY_CD
	,NULL ISO3_COUNTRY_CD
	,CONTINENT.DAC_REGION_CD AS DAC_COUNTRY_CD


	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS COUNTRY_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS COUNTRY_FR_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS COUNTRY_COMMON_EN_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS COUNTRY_COMMON_FR_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_EN_NM)) AS COUNTRY_EN_LONG_NM
	,LTRIM(RTRIM(CONTINENT.GEO_REGION_FR_NM)) AS COUNTRY_FR_LONG_NM

	,'-3' COUNTRY_GNP_LEVEL_CD
	,'Uncoded' COUNTRY_GNP_LEVEL_EN_NM
	,'Non-codé' COUNTRY_GNP_LEVEL_FR_NM
	,'0' AS DAC_