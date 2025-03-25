```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                                                                              | Purpose within Package                                                                                                                                                                                                                                                                  | Security Requirements                                           | Parameters/Variables | Source Part |
|---------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |-----------------------|-----------------------|-------------|
| MART_GC_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred], Authentication: [Assumed Windows Authentication or SQL Server Authentication based on CM]  | Destination connection for loading data into dimension tables.  This connection is the final destination of the data flow in the provided XML.                | Requires permissions to write to the specified database and tables. SQL Server Auth likely | None            | Part 1, 2, 3, 4                  |
| GC_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred], Authentication: [Assumed Windows Authentication or SQL Server Authentication based on CM]  | Source connection for extracting data from staging tables. Source for data extracted from `S_GC_CHANNEL` and `S_GC_FUND_CENTRE` tables. | Requires permissions to read from the specified database and tables. SQL Server Auth likely            |  None                  |  Part 1, 2, 3, 4                 |
| GC_STAGING_SOURCE           | OLE DB          | Server: [Inferred], Database: [Inferred], Authentication: [Assumed Windows Authentication or SQL Server Authentication based on CM]  | Source database for data extraction.             | Requires permissions to read from the specified database and tables. SQL Server Auth likely            |  None                  |  Part 2                 |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

- **Control Flow (General):** The package focuses on loading dimension tables related to GC (Global Commerce) data. It involves truncating tables, loading data from staging areas, and inserting default rows.
- **Error Handling:** Error rows are typically configured to `FailComponent`, causing the entire data flow to fail upon error. No explicit logging within snippets.

#### DFT- R_CHANNEL

*   **Source:** OLE DB Source (OLEDB\_SRC-S\_GC\_CHANNEL) extracts data from the `S_GC_CHANNEL` table in the `GC_STAGING` database.
*   **Destination:** OLE DB Destination (`OLEDB_DEST-R_CHANNEL`) loads data into the `R_CHANNEL` table in the `MART_GC_REPORTING` database.
*   **Transformations:** No explicit transformations are present within the data flow, indicating a direct data movement from source to destination, although the SQL query in the OLE DB source performs some transformations.

#### DFT-D_GC_FUND_CENTRE

*   **Source:** Multiple OLE DB Sources: LEVEL\_1\_DEPARTMENT, LEVEL\_2\_BRANCH, LEVEL\_3\_BUREAU, LEVEL\_4\_DIVISION, LEVEL\_5\_SECTION, LEVEL\_6\_UNIT\_1, LEVEL\_7\_UNIT\_2, each extracting data based on fund center levels from `S_GC_FUND_CENTRE`.
*   **Transformations:**
    *   `UNIONALL_TRFM`: Combines the output from all OLE DB Sources into a single data stream.
    *   `DCONV_TRFM`: Converts strings to shorter lengths.
    *   `DRVCOL_TRFM`: Creates `ETL_CREA_DT` and `ETL_UPDATE_DT` with `GETDATE()`.
*   **Destination:** OLE DB Destination (`OLEDB_DEST-D_GC_FUND_CENTRE`) loads data into the `D_GC_FUND_CENTRE` table in the `MART_GC_REPORTING` database.

#### DFT-D_GC_LOAN_GAC and DFT-D_GC_LOAN_NON_GAC

*   Loads data into `D_GC_LOAN` where `AGENCY_ID` = '3' and `AGENCY_ID` != '3' respectively.

#### DFT-D_GC_INITIATIVE

*   Loads data into the `D_GC_INITIATIVE` table.

#### DFT-D_GC_THEMATIC_PRIORITY

*   Loads data into the `D_GC_THEMATIC_PRIORITY` table.

#### DFT-D_GC_WBS_LEVEL_2

*   **Source:** `OLEDB_SRC-s_gc_project_wbs` extracts data from the `s_gc_project_wbs` table using the `GC_STAGING` connection.
*   **Transformation:** `DCONV_TRFM` converts string columns to `wstr` data types.
*   **Destination:** `OLEDB_DEST-D_GC_WBS_LEVEL_2` loads converted data into the `[dbo].[D_GC_WBS_LEVEL_2]` table using the `MART_GC_REPORTING` connection.

#### DFT-D_GC_WBS_LEVEL_3

*   **Source:** `OLEDB_SRC-S_GC_PROJECT_WBS` extracts WBS Level 3 data from the GC_STAGING database.
*   **Transformation:** `DCONV_TRFM` performs data conversions.
*   **Destination:** `OLEDB_DEST-D_GC_WBS_LEVEL_3` loads the transformed data into the `D_GC_WBS_LEVEL_3` table in the MART_GC_REPORTING database.

#### DFT- D_GC_GEOGRAPHIC_REGION

*   **Sources:** `OLEDB_SRC-Continent`, `OLEDB_SRC- Sub_continent`, `OLEDB_SRC- Sub_sub_continent`, `OLEDB_SRC- Country`
*   **Transformation:** `UNIONALL_TRFM`, `DCONV_TRFM`
*   **Destination:** `OLEDB_DEST-D_GC_GEOGRAPHIC_REGION` loads the transformed data into the `D_GC_GEOGRAPHIC_REGION` table in the MART_GC_REPORTING database.

#### DFT- Update_D_GC_WBS_LEVEL_2

*   **Source:** `OLEDB_SRC-S_D_GC_WBS_LEVEL_2_TMP`: Extract data from the temporary table.
*   **Destination:** `OLEDB_DEST-UPDATE_D_GC_WBS_LEVEL_2`: Loads the extracted data into the `D_GC_WBS_LEVEL_2` table.

#### DFT- Update_D_GC_WBS_LEVEL_2_By_Fact

*   **Source:** `OLEDB_SRC-F_GC_WBS_MILESTONE`: Extract data from the Fact table.
*   **Destination:** `OLEDB-DEST-UPDATE_D_GC_WBS_LEVEL_2`: Loads the extracted data into the `D_GC_WBS_LEVEL_2` table.

#### DFT- D_GC_EMPLOYEE

*   **Source:** `OLEDB_SRC-S_GC_EMPLOYEE` extracts data from the `S_GC_EMPLOYEE` table.

#### DFT- D_GC_IM_PROGRAM_POSITION

*   Data flow task to load data into the D_GC_IM_PROGRAM_POSITION dimension.

#### DFT- D_GC_INDIVIDUAL

*   Data flow task to load data into the D_GC_INDIVIDUAL dimension.

#### DFT- D_GC_ROLE

*   Data flow task to load data into the D_GC_ROLE dimension.

#### Sequence Containers
 * SEQC-1_D_GC_FUND_CENTRE is used to group the two data flow tasks (`DFT- R_CHANNEL` and `DFT-D_GC_FUND_CENTRE`).
 * `SEQC-2-D_GC_LOAN`, `SEQC-2-D_GC_SECTOR`, and `SEQC-3-D_GC_CROSS_CUTTING_THEME` organize and group related tasks.

## 4. Code Extraction

```sql
-- Source: OLEDB_SRC-S_GC_CHANNEL (DFT- R_CHANNEL)
SELECT
	T1.CHANNEL_CD AS CHANNEL_CD,
	T1.EN_NM AS CHANNEL_EN_NM,
	T1.EN_ACRONYM AS CHANNEL_EN_ACRONYM,
	T1.FR_NM AS CHANNEL_FR_NM,
	T1.FR_ACRONYM AS CHANNEL_FR_ACRONYM,
	T1.CHANNEL_SUB_CATEGORY_CD AS CHANNEL_SUB_CATEGORY_CD,
	CASE
		WHEN T2.CHANNEL_SUB_CATEGORY_EN_NM is NULL THEN 'Uncoded'
		ELSE T2.CHANNEL_SUB_CATEGORY_EN_NM
	END AS CHANNEL_SUB_CATEGORY_EN_NM,
	CASE
		WHEN T2.CHANNEL_SUB_CATEGORY_ACRONYM_EN_ is NULL THEN 'Uncoded'
		ELSE T2.CHANNEL_SUB_CATEGORY_ACRONYM_EN_
	END AS CHANNEL_SUB_CATEGORY_EN_ACRONYM,
	CASE
		WHEN T2.CHANNEL_SUB_CATEGORY_FR_NM is NULL THEN 'Non codé'
		ELSE T2.CHANNEL_SUB_CATEGORY_FR_NM
	END AS CHANNEL_SUB_CATEGORY_FR_NM,
	CASE
		WHEN T2.CHANNEL_SUB_CATEGORY_ACRONYM_FR_ is NULL THEN 'Non codé'
		ELSE T2.CHANNEL_SUB_CATEGORY_ACRONYM_FR_
	END AS CHANNEL_SUB_CATEGORY_FR_ACRONYM,
	T1.PARENT_CHANNEL_CD AS CHANNEL_CATEGORY_CD,
	CASE
		WHEN T3.CHANNEL_CATEGORY_EN_NM is NULL THEN 'Uncoded'
		ELSE T3.CHANNEL_CATEGORY_EN_NM
	END AS CHANNEL_CATEGORY_EN_NM,
	CASE
		WHEN T3.CHANNEL_CATEGORY_EN_ACRONYM is NULL THEN 'Uncoded'
		ELSE T3.CHANNEL_CATEGORY_EN_ACRONYM
	END AS CHANNEL_CATEGORY_EN_ACRONYM,
	CASE
		WHEN T3.CHANNEL_CATEGORY_FR_NM is NULL then 'Non codé'
		ELSE T3.CHANNEL_CATEGORY_FR_NM
	END AS CHANNEL_CATEGORY_FR_NM,
	CASE
		WHEN T3.CHANNEL_CATEGORY_FR_ACRONYM is NULL THEN 'Non codé'
		ELSE T3.CHANNEL_CATEGORY_FR_ACRONYM
	END AS CHANNEL_CATEGORY_FR_ACRONYM,
	T1.COEFFICIENT_PCT AS COEFFICIENT_PCT,
	GETDATE() AS UPDATE_DATE,
	T1.SOURCE_ID AS SOURCE_ID,
getdate() as ETL_CREA_DT,
getdate() as ETL_UPDT_DT
FROM "dbo"."S_GC_CHANNEL" T1
LEFT JOIN "dbo"."S_GC_CHANNEL_SUB_CATEGORY" T2 ON T1.CHANNEL_SUB_CATEGORY_CD = T2.CHANNEL_SUB_CATEGORY_CD
LEFT JOIN "dbo"."S_GC_CHANNEL_CATEGORY" T3 ON T1.PARENT_CHANNEL_CD = T3.CHANNEL_CATEGORY_CD
```

```sql
-- Source: OLEDB_SRC- LEVEL_2_BRANCH (DFT-D_GC_FUND_CENTRE)
SELECT DISTINCT

      T1.FUND_CENTER_NBR as [FUND_CENTRE_CD],
      T1.SOURCE_ID,
      NULL as[DEFAULT_CURRENCY_CODE],
      NULL as[BI_FC_SYMBOL_DESCR_EN],
      NULL as[BI_FC_SYMBOL_DESCR_FR],
      NULL as[FC_SYMBOL],
      NULL as [FC_SDESC_EN],
      NULL as[FC_SDESC_FR],
      T1.[EN_NM] as [FC_LDESC_EN],
      T1.[FR_NM] as [FC_LDESC_FR],
      NULL as[FC_SYMBOL_DESC_EN],
      NULL as[FC_SYMBOL_DESC_FR],
      NULL AS[FC_GROUPNAME],
      NULL AS[LEVEL1_FC_GROUP_NAME],
      NULL AS[LEVEL2_FC_GROUP_NAME],
      T1.FUND_CENTER_NBR as [LEVEL7_CD],
      NULL AS[LEVEL7_SYMBOL],
      NULL AS[LEVEL7_SDESC_EN],
      NULL AS[LEVEL7_SDESC_FR],
      T1.[EN_NM] as [LEVEL7_LDESC_EN],
      T1.[FR_NM] as [LEVEL7_LDESC_FR],
      NULL AS[LEVEL7_SYMBOL_DESC_EN],
      NULL AS[LEVEL7_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL6_CD],
      NULL AS[LEVEL6_SYMBOL],
      NULL AS[LEVEL6_SDESC_EN],
      NULL AS[LEVEL6_SDESC_FR],
      T1.[EN_NM] as [LEVEL6_LDESC_EN],
      T1.[FR_NM] as [LEVEL6_LDESC_FR],
      NULL AS[LEVEL6_SYMBOL_DESC_EN],
      NULL AS[LEVEL6_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL5_CD],
      NULL AS[LEVEL5_SYMBOL],
      NULL AS[LEVEL5_SDESC_EN],
      NULL AS[LEVEL5_SDESC_FR],
      T1.[EN_NM] as [LEVEL5_LDESC_EN],
      T1.[FR_NM] as [LEVEL5_LDESC_FR],
      NULL AS[LEVEL5_SYMBOL_DESC_EN],
      NULL AS[LEVEL5_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL4_CD],
      NULL AS[LEVEL4_SYMBOL],
      NULL AS[LEVEL4_SDESC_EN],
      NULL AS[LEVEL4_SDESC_FR],
      T1.[EN_NM] as [LEVEL4_LDESC_EN],
      T1.[FR_NM] as [LEVEL4_LDESC_FR],
      NULL AS[LEVEL4_SYMBOL_DESC_EN],
      NULL AS[LEVEL4_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL3_CD],
      NULL AS[LEVEL3_SYMBOL],
      NULL AS[LEVEL3_SDESC_EN],
      NULL AS[LEVEL3_SDESC_FR],
      T1.[EN_NM] as [LEVEL3_LDESC_EN],
      T1.[FR_NM] as [LEVEL3_LDESC_FR],
      NULL AS[LEVEL3_SYMBOL_DESC_EN],
      NULL AS[LEVEL3_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL2_CD],
      NULL AS[LEVEL2_SYMBOL],
      NULL AS[LEVEL2_SDESC_EN],
      NULL AS[LEVEL2_SDESC_FR],
      T1.[EN_NM] as [LEVEL2_LDESC_EN],
      T1.[FR_NM] as [LEVEL2_LDESC_FR],
      NULL AS[LEVEL2_SYMBOL_DESC_EN],
      NULL AS[LEVEL2_SYMBOL_DESC_FR],
      NULL AS[LEVEL1_SDESC_EN],
      NULL AS[LEVEL1_SDESC_FR],
      T2.FUND_CENTER_NBR as [LEVEL1_CD],
      T2.[EN_NM] as [LEVEL1_LDESC_EN],
      T2.[FR_NM] as [LEVEL1_LDESC_FR],
      NULL AS[REGION_CD],
      NULL AS[HR_REGION_CD],
      NULL AS[HQ_MISSION_CD],
      NULL AS[PROGRAM_ACTIVITY_CD],
      NULL AS[PAC_SDESC_EN],
      NULL AS[PAC_SDESC_FR],
      NULL AS[PAC_LDESC_EN],
      NULL AS[PAC_LDESC_FR],
      2 AS[LEVEL],
      NULL AS[COMPANY_CODE],
      T1.FUND_CENTER_NBR as[FC_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL7_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL6_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL5_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL4_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL3_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL2_MUN],
      T2.FUND_CENTER_NBR as [FC_LVL1_MUN],
      NULL AS[SYM_MUN],
      NULL AS[SYM_LVL7_MUN],
      NULL AS[SYM_LVL6_MUN],
      NULL AS[SYM_LVL5_MUN],
      NULL AS[SYM_LVL4_MUN],
      NULL AS[SYM_LVL3_MUN],
      NULL AS[SYM_LVL2_MUN],
      NULL AS[SYM_LVL1_MUN],
      NULL AS[DEPT_ID],
      NULL AS[PAC],
      T1. CREATION_DT AS[Create_Date],
      T1. [LAST_UPDATED_DT] AS[Last_Update_Date],
      NULL AS[Record_Identity],
      convert(date,getdate()) as ROW_INSERT_DT

  FROM [dbo].[S_GC_FUND_CENTRE] T1

  JOIN [dbo].[S_GC_FUND_CENTRE] T2
	  on T1.PARENT_FUND_CENTER_NBR = T2.FUND_CENTER_NBR

WHERE T2.FUND_CENTER_NBR = 'DFAIT'
```

```sql
-- Source: OLEDB_SRC- LEVEL_5_SECTION (DFT-D_GC_FUND_CENTRE)
SELECT DISTINCT

      T5.FUND_CENTER_NBR as [FUND_CENTRE_CD],
      T5.SOURCE_ID,
      NULL as[DEFAULT_CURRENCY_CODE],
      NULL as[BI_FC_SYMBOL_DESCR_EN],
      NULL as[BI_FC_SYMBOL_DESCR_FR],
      NULL as[FC_SYMBOL],
      NULL as [FC_SDESC_EN],
      NULL as[FC_SDESC_FR],
      T5.[EN_NM] as [FC_LDESC_EN],
      T5.[FR_NM] as [FC_LDESC_FR],
      NULL as[FC_SYMBOL_DESC_EN],
      NULL as[FC_SYMBOL_DESC_FR],
      NULL AS[FC_GROUPNAME],
      NULL AS[LEVEL1_FC_GROUP_NAME],
      NULL AS[LEVEL2_FC_GROUP_NAME],
      T5.FUND_CENTER_NBR as [LEVEL7_CD],
      NULL AS[LEVEL7_SYMBOL],
      NULL AS[LEVEL7_SDESC_EN],
      NULL AS[LEVEL7_SDESC_FR],
      T5.[EN_NM] as [LEVEL7_LDESC_EN],
      T5.[FR_NM] as [LEVEL7_LDESC_FR],
      NULL AS[LEVEL7_SYMBOL_DESC_EN],
      NULL AS[LEVEL7_SYMBOL_DESC_FR],
      T5.FUND_CENTER_NBR as [LEVEL6_CD],
      NULL AS[LEVEL6_SYMBOL],
      NULL AS[LEVEL6_SDESC_EN],
      NULL AS[LEVEL6_SDESC_FR],
      T5.[EN_NM] as [LEVEL6_LDESC_EN],
      T5.[FR_NM] as [LEVEL6_LDESC_FR],
      NULL AS[LEVEL6_SYMBOL_DESC_EN],
      NULL AS[LEVEL6_SYMBOL_DESC_FR],
      T5.FUND_CENTER_NBR as [LEVEL5_CD],
      NULL AS[LEVEL5_SYMBOL],
      NULL AS[LEVEL5_SDESC_EN],
      NULL AS[LEVEL5_SDESC_FR],
      T5.[EN_NM] as [LEVEL5_LDESC_EN],
      T5.[FR_NM] as [LEVEL5_LDESC_FR],
      NULL AS[LEVEL5_SYMBOL_DESC_EN],
      NULL AS[LEVEL5_SYMBOL_DESC_FR],
      T4.FUND_CENTER_NBR as [LEVEL4_CD],
      NULL AS[LEVEL4_SYMBOL],
      NULL AS[LEVEL4_SDESC_EN],
      NULL AS[LEVEL4_SDESC_FR],
      T4.[EN_NM] as [LEVEL4_LDESC_EN],
      T4.[FR_NM] as [LEVEL4_LDESC_FR],
      NULL AS[LEVEL4_SYMBOL_DESC_EN],
      NULL AS[LEVEL4_SYMBOL_DESC_FR],
      T3.FUND_CENTER_NBR as [LEVEL3_CD],
      NULL AS[LEVEL3_SYMBOL],
      NULL AS[LEVEL3_SDESC_EN],
      NULL AS[LEVEL3_SDESC_FR],
      T3.[EN_NM] as [LEVEL3_LDESC_EN],
      T3.[FR_NM] as [LEVEL3_LDESC_FR],
      NULL AS[LEVEL3_SYMBOL_DESC_EN],
      NULL AS[LEVEL3_SYMBOL_DESC_FR],
      T2.FUND_CENTER_NBR as [LEVEL2_CD],
      NULL AS[LEVEL2_SYMBOL],
      NULL AS[LEVEL2_SDESC_EN],
      NULL AS[LEVEL2_SDESC_FR],
      T2.[EN_NM] as [LEVEL2_LDESC_EN],
      T2.[FR_NM] as [LEVEL2_LDESC_FR],
      NULL AS[LEVEL2_SYMBOL_DESC_EN],
      NULL AS[LEVEL2_SYMBOL_DESC_FR],
      NULL AS[LEVEL1_SDESC_EN],
      NULL AS[LEVEL1_SDESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL1_CD],
      T1.[EN_NM] as [LEVEL1_LDESC_EN],
      T1.[FR_NM] as [LEVEL1_LDESC_FR],
      NULL AS[REGION_CD],
      NULL AS[HR_REGION_CD],
      NULL AS[HQ_MISSION_CD],
      NULL AS[PROGRAM_ACTIVITY_CD],
      NULL AS[PAC_SDESC_EN],
      NULL AS[PAC_SDESC_FR],
      5 AS[LEVEL],
      NULL AS[COMPANY_CODE],
      T5.FUND_CENTER_NBR as[FC_MUN],
      T5.FUND_CENTER_NBR as [FC_LVL7_MUN],
      T5.FUND_CENTER_NBR as [FC_LVL6_MUN],
      T5.FUND_CENTER_NBR as [FC_LVL5_MUN],
      T4.FUND_CENTER_NBR as [FC_LVL4_MUN],
      T3.FUND_CENTER_NBR as [FC_LVL3_MUN],
      T2.FUND_CENTER_NBR as [FC_LVL2_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL1_MUN],
      NULL AS[SYM_MUN],
      NULL AS[SYM_LVL7_MUN],
      NULL AS[SYM_LVL6_MUN],
      NULL AS[SYM_LVL5_MUN],
      NULL AS[SYM_LVL4_MUN],
      NULL AS[SYM_LVL3_MUN],
      NULL AS[SYM_LVL2_MUN],
      NULL AS[SYM_LVL1_MUN],
      NULL AS[DEPT_ID],
      NULL AS[PAC],
      T1. CREATION_DT AS[Create_Date],
      T1. [LAST_UPDATED_DT] AS[Last_Update_Date],
      NULL AS[Record_Identity],
      convert(date,getdate()) as ROW_INSERT_DT

  FROM [dbo].[S_GC_FUND_CENTRE] T5

  join [dbo].[S_GC_FUND_CENTRE] T4       --- DIVISION T4
  on T5.[PARENT_FUND_CENTER_NBR] = T4.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T3       --- BUREAU T3
  on T4.[PARENT_FUND_CENTER_NBR] = T3.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T2      --- BRANCH T2
  on T3.[PARENT_FUND_CENTER_NBR] = T2.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T1       --- DEPARTMENT T1
  on T2.[PARENT_FUND_CENTER_NBR] = T1.FUND_CENTER_NBR

WHERE T1.FUND_CENTER_NBR = 'DFAIT'
--AND T5.FUND_CENTER_NBR IN (SELECT PARENT_FUND_CENTER_NBR from [GC_Staging].[dbo].S_GC_FUND_CENTRE)  -- filter out Level 5s with no Children to eliminate duplicates with level 6
```

```sql
-- Source: OLEDB_SRC- LEVEL_7_UNIT_2 (DFT-D_GC_FUND_CENTRE)
SELECT DISTINCT

      T7.FUND_CENTER_NBR as [FUND_CENTRE_CD],
      T7.SOURCE_ID,
      NULL as[DEFAULT_CURRENCY_CODE],
      NULL as[BI_FC_SYMBOL_DESCR_EN],
      NULL as[BI_FC_SYMBOL_DESCR_FR],
      NULL as[FC_SYMBOL],
      NULL as [FC_SDESC_EN],
      NULL as[FC_SDESC_FR],
      T7.[EN_NM] as [FC_LDESC_EN],
      T7.[FR_NM] as [FC_LDESC_FR],
      NULL as[FC_SYMBOL_DESC_EN],
      NULL as[FC_SYMBOL_DESC_FR],
      NULL AS[FC_GROUPNAME],
      NULL AS[LEVEL1_FC_GROUP_NAME],
      NULL AS[LEVEL2_FC_GROUP_NAME],
      T6.FUND_CENTER_NBR as [LEVEL7_CD],
      NULL AS[LEVEL7_SYMBOL],
      NULL AS[LEVEL7_SDESC_EN],
      NULL AS[LEVEL7_SDESC_FR],
      T6.[EN_NM] as [LEVEL7_LDESC_EN],
      T6.[FR_NM] as [LEVEL7_LDESC_FR],
      NULL AS[LEVEL7_SYMBOL_DESC_EN],
      NULL AS[LEVEL7_SYMBOL_DESC_FR],
      T6.FUND_CENTER_NBR as [LEVEL6_CD],
      NULL AS[LEVEL6_SYMBOL],
      NULL AS[LEVEL6_SDESC_EN],
      NULL AS[LEVEL6_SDESC_FR],
      T6.[EN_NM] as [LEVEL6_LDESC_EN],
      T6.[FR_NM] as [LEVEL6_LDESC_FR],
      NULL AS[LEVEL6_SYMBOL_DESC_EN],
      NULL AS[LEVEL6_SYMBOL_DESC_FR],
      T5.FUND_CENTER_NBR as [LEVEL5_CD],
      NULL AS[LEVEL5_SYMBOL],
      NULL AS[LEVEL5_SDESC_EN],
      NULL AS[LEVEL5_SDESC_FR],
      T5.[EN_NM] as [LEVEL5_LDESC_EN],
      T5.[FR_NM] as [LEVEL5_LDESC_FR],
      NULL AS[LEVEL5_SYMBOL_DESC_EN],
      NULL AS[LEVEL5_SYMBOL_DESC_FR],
      T4.FUND_CENTER_NBR as [LEVEL4_CD],
      NULL AS[LEVEL4_SYMBOL],
      NULL AS[LEVEL4_SDESC_EN],
      NULL AS[LEVEL4_SDESC_FR],
      T4.[EN_NM] as [LEVEL4_LDESC_EN],
      T4.[FR_NM] as [LEVEL4_LDESC_FR],
      NULL AS[LEVEL4_SYMBOL_DESC_EN],
      NULL AS[LEVEL4_SYMBOL_DESC_FR],
      T3.FUND_CENTER_NBR as [LEVEL3_CD],
      NULL AS[LEVEL3_SYMBOL],
      NULL AS[LEVEL3_SDESC_EN],
      NULL AS[LEVEL3_SDESC_FR],
      T3.[EN_NM] as [LEVEL3_LDESC_EN],
      T3.[FR_NM] as [LEVEL3_LDESC_FR],
      NULL AS[LEVEL3_SYMBOL_DESC_EN],
      NULL AS[LEVEL3_SYMBOL_DESC_FR],
      T2.FUND_CENTER_NBR as [LEVEL2_CD],
      NULL AS[LEVEL2_SYMBOL],
      NULL AS[LEVEL2_SDESC_EN],
      NULL AS[LEVEL2_SDESC_FR],
      T2.[EN_NM] as [LEVEL2_LDESC_EN],
      T2.[FR_NM] as [LEVEL2_LDESC_FR],
      NULL AS[LEVEL2_SYMBOL_DESC_EN],
      NULL AS[LEVEL2_SYMBOL_DESC_FR],
      NULL AS[LEVEL1_SDESC_EN],
      NULL AS[LEVEL1_SDESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL1_CD],
      T1.[EN_NM] as [LEVEL1_LDESC_EN],
      T1.[FR_NM] as [LEVEL1_LDESC_FR],
      NULL AS[REGION_CD],
      NULL AS[HR_REGION_CD],
      NULL AS[HQ_MISSION_CD],
      NULL AS[PROGRAM_ACTIVITY_CD],
      NULL AS[PAC_SDESC_EN],
      NULL AS[PAC_LDESC_FR],
      7 AS[LEVEL],
      NULL AS[COMPANY_CODE],
      T7.FUND_CENTER_NBR as[FC_MUN],
      T7.FUND_CENTER_NBR as [FC_LVL7_MUN],
      T6.FUND_CENTER_NBR as [FC_LVL6_MUN],
      T5.FUND_CENTER_NBR as [FC_LVL5_MUN],
      T4.FUND_CENTER_NBR as [FC_LVL4_MUN],
      T3.FUND_CENTER_NBR as [FC_LVL3_MUN],
      T2.FUND_CENTER_NBR as [FC_LVL2_MUN],
      T1.FUND_CENTER_NBR as [FC_LVL1_MUN],
      NULL AS[SYM_MUN],
      NULL AS[SYM_LVL7_MUN],
      NULL AS[SYM_LVL6_MUN],
      NULL AS[SYM_LVL5_MUN],
      NULL AS[SYM_LVL4_MUN],
      NULL AS[SYM_LVL3_MUN],
      NULL AS[SYM_LVL2_MUN],
      NULL AS[SYM_LVL1_MUN],
      NULL AS[DEPT_ID],
      NULL AS[PAC],
      T1. CREATION_DT AS[Create_Date],
      T1. [LAST_UPDATED_DT] AS[Last_Update_Date],
      NULL AS[Record_Identity],
      convert(date,getdate()) as ROW_INSERT_DT

  FROM [dbo].[S_GC_FUND_CENTRE] T7

  join [dbo].[S_GC_FUND_CENTRE] T6       --- UNIT 1
  on T7.[PARENT_FUND_CENTER_NBR] = T6.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T5       --- SECTION T5
  on T6.[PARENT_FUND_CENTER_NBR] = T5.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T4       --- DIVISION T4
  on T5.[PARENT_FUND_CENTER_NBR] = T4.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T3       --- BUREAU T3
  on T4.[PARENT_FUND_CENTER_NBR] = T3.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T2      --- BRANCH T2
  on T3.[PARENT_FUND_CENTER_NBR] = T2.FUND_CENTER_NBR

  join [dbo].[S_GC_FUND_CENTRE] T1       --- DEPARTMENT T1
  on T2.[PARENT_FUND_CENTER_NBR] = T1.FUND_CENTER_NBR

WHERE T1.FUND_CENTER_NBR = 'DFAIT'
```

```sql
-- Source: OLEDB_SRC-LEVEL_1_DEPARTMENT (DFT-D_GC_FUND_CENTRE)
SELECT DISTINCT

      T1.FUND_CENTER_NBR as [FUND_CENTRE_CD],
      T1.SOURCE_ID,
      NULL as[DEFAULT_CURRENCY_CODE],
      NULL as[BI_FC_SYMBOL_DESCR_EN],
      NULL as[BI_FC_SYMBOL_DESCR_FR],
      NULL as[FC_SYMBOL],
      NULL as [FC_SDESC_EN],
      NULL as[FC_SDESC_FR],
      T1.[EN_NM] as [FC_LDESC_EN],
      T1.[FR_NM] as [FC_LDESC_FR],
      NULL as[FC_SYMBOL_DESC_EN],
      NULL as[FC_SYMBOL_DESC_FR],
      NULL AS[FC_GROUPNAME],
      NULL AS[LEVEL1_FC_GROUP_NAME],
      NULL AS[LEVEL2_FC_GROUP_NAME],
      T1.FUND_CENTER_NBR as [LEVEL7_CD],
      NULL AS[LEVEL7_SYMBOL],
      NULL AS[LEVEL7_SDESC_EN],
      NULL AS[LEVEL7_SDESC_FR],
      T1.[EN_NM] as [LEVEL7_LDESC_EN],
      T1.[FR_NM] as [LEVEL7_LDESC_FR],
      NULL AS[LEVEL7_SYMBOL_DESC_EN],
      NULL AS[LEVEL7_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL6_CD],
      NULL AS[LEVEL6_SYMBOL],
      NULL AS[LEVEL6_SDESC_EN],
      NULL AS[LEVEL6_SDESC_FR],
      T1.[EN_NM] as [LEVEL6_LDESC_EN],
      T1.[FR_NM] as [LEVEL6_LDESC_FR],
      NULL AS[LEVEL6_SYMBOL_DESC_EN],
      NULL AS[LEVEL6_SYMBOL_DESC_FR],
      T1.FUND_CENTER_NBR as [LEVEL5_CD],
      NULL AS[LEVEL5_SYMBOL],
      NULL AS[LEVEL5_SDESC_EN],
      NULL AS[LEVEL5_SDESC_FR],
      T1.[EN_NM] as [LEVEL5_LDESC_EN],
