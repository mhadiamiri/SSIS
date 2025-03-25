```markdown
## 1. Input Connection Analysis

| Connection Manager Name                                  | Connection Type | Connection String Details                       | Purpose within Package                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Security Requirements                               | Parameters/Variables | Source Part |
| -------------------------------------------------------- | --------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | --------------------- |-------------|
| {4C44ACE1-34E1-4E07-AC7E-84014ECDC0B6}                   | Excel Source    | `invalid`                                     | Source for the "Data Flow Task" (Disabled).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Unknown due to invalid connection string. | None                  | Part 1                  |
| {FA3E2499-2C9B-4FF0-99D2-834F0DE08FF6}                   | OLE DB          | `Project.ConnectionManagers[ETL_STG_DATA_HUB]` | Destination for the "Data Flow Task" (Disabled).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Depends on connection manager configuration.      | None                  | Part 1                  |
| {87F21133-2B18-4979-A59D-C544A5799C22}                   | OLE DB          | `Project.ConnectionManagers[ODS_GC_SOURCE_DB]` | Source for several DFTs (e.g., "DFT-SAP_COST_CENTRE", "DFT-SAP_FUND_CENTRE", "DFT-SAP_PROJECT_FINANCE"). Extracts data from GC_SOURCE_DB database to populate tables in DATA_HUB. Source for extracting SAP data (tables like `zastk`, `ZAPS_CCMWBS`, `PRHI`, etc.). | Depends on connection manager configuration. Read Access to the source ODS.           | None                  | Part 1, 2, 3, 4                  |
| {452E16FA-100E-4B79-827B-54F46F5E0D8F}                   | OLE DB          | `Project.ConnectionManagers[DATA_HUB]`        | Destination for several DFTs (e.g., "DFT-SAP_COST_CENTRE", "DFT-SAP_FUND_CENTRE", "DFT-SAP_PROJECT_FINANCE"). Destination for loading transformed data into Data Hub tables.                                                                                                                                                                                                                                                                                | Depends on connection manager configuration. Access to data warehouse.          | None                  | Part 1, 2, 3, 4                  |
| DATA_HUB                                                | OLE DB          | Server, Database, Authentication Method (Implied) | Destination for loading data into tables like `SAP_MILESTONE`, `SAP_PROJECT`, `SAP_PROJECT_WBS`, `SAP_PROJECT_WBS_CHANGE_STATUS`, and `SAP_VENDOR`, `SAP_GEO_COUNTRY`, and `SAP_PROJECT_WBS_WORKPLAN_DESCRIPTION`.                                                                                                                                                                                                                                                                                                                | Requires appropriate database permissions (write access) on the DATA_HUB to insert/update data | Likely uses project level connection manager; Requires the `DATA_HUB` connection manager to be configured correctly in the SSIS project | Part 2, 4                  |
| ODS_GC_SOURCE_DB                                          | OLE DB          | Server, Database, Authentication Method (Implied) | Source for extracting data from GC_SOURCE_DB database to populate tables in DATA_HUB.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Requires appropriate database permissions (read access) on the ODS_GC_SOURCE_DB to extract data| Likely uses project level connection manager; Requires the `ODS_GC_SOURCE_DB` connection manager to be configured correctly in the SSIS project | Part 2, 4                  |
| ODS_SAP                                                   | OLE DB          | Server, Database, Authentication Method (not specified) | Lookup data from SAP (ZACEAAQCT, ZACEAAQAT, TJ30T)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Credentials to access the ODS_SAP database.          | None                  | Part 3                  |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes                                   | Source Part |
| ---------------------- | ----------------- | ------------------------- | --------------------------------- | --------------------------------------- |-------------|
| None Found            |                   |                           |                                   | No dependent SSIS packages tasks found. | Part 1, 2, 3, 4|

## 3. Package Flow Analysis

The control flow of the package consists of the following activities:

1.  **Data Flow Task**: `Data Flow Task` - Disabled
2.  **Expression Task**: `EXPRESSIONT_DATA_HUB_GCS_LOAD` - Expression: `1==1`
3.  **Sequence Container**: `SEQ-06`
    *   **Data Flow Task**: `DFT-SAP_COST_CENTRE`
    *   **Data Flow Task**: `DFT-SAP_FUND_CENTRE`
    *   **Data Flow Task**: `DFT-SAP_PROJECT_FINANCE`
    *   **Data Flow Task**: `DFT-SAP_PROJECT_FINANCE 1` - Disabled
    *   **Data Flow Task**: `DFT-SAP_PROJECT_FINANCE Before_2023-11-03` - Disabled
    *   **Data Flow Task**: `DFT-SAP_PROJECT_FINANCE_new_try` - Disabled
    *   **Data Flow Task**: `DFT-SAP_PROJECT_FINANCE_not_Used` - Disabled
    *   **Data Flow Task**: `DFT-SAP_PROJECT_WBS_CRS_ACTIVITY`
4.  **Sequence Container**: `SEQC-GCS-FAS_MERGE-STAGING TABLE`
    *   **Execute SQL Task**: `ESQLT-TRUNCATE - S_SAP_GCS_FAS_WBS_MAP`
    *   **Data Flow Task**: `DFT-S_SAP_GCS_FAS_WBS_MAP`
5.  **Sequence Container**: `SEQC-Initialize_Tables_For_GCS_loading`
    *   **Execute SQL Task**: `ESQL-Truncate_Tables_In_DATA_HUB_02_SAP`
    *   **Execute SQL Task**: `ESQLT-Truncate SAP_PROJECT_and_VENDOR`
    *   **Execute SQL Task**: `ESQLT-Drop_Index_On_Big_Tables`
6.  **Sequence Container**: `SEQC_01_Load_GCS`
    *   **Data Flow Task**: `DFT_SAP_PROJECT_POLICY_MARKER_GCS`
    *   **Data Flow Task**: `DFT_SAP_INVESTMENT_PROGRAM_POSITION_ASSIGNMENT_Before_05_01` - Disabled
    *   **Data Flow Task**: `DFT_SAP_INVESTMENT_PROGRAM_POSITION`
    *   **Data Flow Task**: `DFT_SAP_INVESTMENT_ALTERNATE_PROGRAM_POSITION_ASSIGNMENT`
7.  **Sequence Container**: `SEQC_02_Load_GCS`
    *   Contains multiple Data Flow Tasks for loading different SAP entities.
    *   **Parallel Execution:** The Data Flow Tasks within `SEQC_02_Load_GCS` appear to execute in parallel.
8.  **Sequence Container**: `SEQC_03_Load_GCS - Accounting Documents`
        *   **Task:** `ESQL_Load_SAP_ACCOUNTING_DOCUMENT from GCS`
        *   **Connection:** `ODS_GC_SOURCE_DB`
        *   **Task**: `ESQL_Load_SAP_ACCOUNTING_DOCUMENT_LINE_ITEM from GCS`
        *    **Connection**: `ODS_GC_SOURCE_DB`
9.  **Sequence Container**: `SEQC_04`
        *   **Task**: `DFT-SAP_GEO_COUNTRY`
        *   **Task**: `DFT-SAP_PROJECT_WBS_CFP`
        *   **Task**: `DFT-SAP_VENDOR_CONTACT_DETAIL`
10. **Sequence Container**: `SEQC_05`
    *   DFT-SAP\_DAC\_CONTINENT\_REGION\_GCS
    *   DFT-SAP\_FUND\_RESERVATION\_COMMITMENT\_LINE\_ITEM\_GCS (Disabled)
    *   DFT-SAP\_PROJECT\_HIERARCHY\_GCS (Disabled)
    *   DFT-SAP\_PROJECT\_WBS\_CEAA\_GCS
    *   DFT-SAP\_PROJECT\_WBS\_CHANGE\_STATUS\_HISTORY\_GCS
    *   DFT-SAP\_PROJECT\_WBS\_PROPOSAL\_CALL\_GCS
    *   DFT\_SAP\_REGION\_GCS
11. **Sequence Container**: `SEQC_07` containing multiple Data Flow Tasks (DFTs).

#### Precedence Constraints

-   The `EXPRESSIONT_DATA_HUB_GCS_LOAD` task always executes because its expression is `1==1`.
-   The subsequent tasks `SEQ-06`, `SEQC-GCS-FAS_MERGE-STAGING TABLE`, `SEQC-Initialize_Tables_For_GCS_loading` and `SEQC_01_Load_GCS` execute sequentially after the `EXPRESSIONT_DATA_HUB_GCS_LOAD` task.
-   Inside the `SEQ-06` container, the data flow tasks execute in sequence.
-   Inside the `SEQC_01_Load_GCS` container, the data flow tasks execute in sequence.
-   Inside the `SEQC-GCS-FAS_MERGE-STAGING TABLE` container, the tasks execute in sequence.
-   Inside the `SEQC-Initialize_Tables_For_GCS_loading` container, the tasks execute in sequence.
-   The DFTs in `SEQC_04`, `SEQC_05`, and `SEQC_07` execute sequentially based on precedence constraints (success/failure).

#### DFT- Data Flow Task (Disabled)

*   **Source:** `Excel Source` - Reads data from an Excel sheet named "page$". The connection manager is invalid.
*   **Transformations:**
    *   `Derived Column` - Adds new columns `ETL_CREA_DT` and `ETL_UPDT_DT` with the current date and time.
    *   `Data Conversion` - Converts `DAC Recipient (format)` and `Sector (format)` from `wstr` to `str`.
*   **Destination:** `OLE DB Destination` - Writes data to the table `[dbo].[S_RPT_GC_DAC_COEFF]` using connection `ETL_STG_DATA_HUB`.
*   **Error Handling:** Fails the component for any errors.

#### DFT-SAP_COST_CENTRE

*   **Source:** `OLE DB _SAP_KBLP` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_Load_Dhub_SAP_COST_CENTRE` - Loads transformed data into `[dbo].[SAP_COST_CENTRE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_FUND_CENTRE

*   **Source:** `OLE DB _SAP_FMHISV` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB _SAP_FUND_CENTRE` - Loads transformed data into `[dbo].[SAP_FUND_CENTRE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_FINANCE

*   **Source:** `OLE DB _SAP_RPSCO` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_Load_DHUB_SAP_PROJECT_FINANCE` - Loads transformed data into `[dbo].[SAP_PROJECT_FINANCE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_FINANCE 1 (Disabled)

*   **Source:** `OLE DB _SAP_RPSCO` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_Load_DHUB_SAP_PROJECT_FINANCE` - Loads transformed data into `[dbo].[SAP_PROJECT_FINANCE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_FINANCE Before_2023-11-03 (Disabled)

*   **Source:** `OLE DB _SAP_RPSCO` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_Load_DHUB_SAP_PROJECT_FINANCE` - Loads transformed data into `[dbo].[SAP_PROJECT_FINANCE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_FINANCE_new_try (Disabled)

*   **Source:** `OLE DB _SAP_RPSCO` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_Load_DHUB_SAP_PROJECT_FINANCE` - Loads transformed data into `[dbo].[SAP_PROJECT_FINANCE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_FINANCE_not_Used (Disabled)

*   **Source:** `OLE DB _SAP_RPSCO` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_Load_DHUB_SAP_PROJECT_FINANCE` - Loads transformed data into `[dbo].[SAP_PROJECT_FINANCE]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP_PROJECT_WBS_CRS_ACTIVITY

*   **Source:** `OLE DB _ZAPS_CRSACTIVIT` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLE DB_DEST_SAP_PROJECT_WBS_CRS_ACTIVITY` - Loads transformed data into `[dbo].[SAP_PROJECT_WBS_CRS_ACTIVITY]` using the `DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-S_SAP_GCS_FAS_WBS_MAP

*   **Source:** `OLEDB-SRC - GCS - PRPS DELTA` - Extracts data from the `ODS_GC_SOURCE_DB` connection using a complex SQL query (see Code Extraction section).
*   **Destination:** `OLEDB-DEST S_SAP_GCS_FAS_WBS_MAP` - Loads transformed data into `[dbo].[S_SAP_GCS_FAS_WBS_MAP]` using the `ETL_STG_DATA_HUB` connection.
*   **Error Handling**: Fails Component.

#### DFT-SAP\_MILESTONE from SEQC_MILESTONE

*   **Source**: `OLEDB_SRC-MLTX` (OLE DB Source) reading from table `MLTX`
*   **Destination**: `OLEDEB_DST-SAP_MILESTONE_SAP` (OLE DB Destination) writing to table `SAP_MILESTONE`
*   **Transformations**: Data type conversions are implied from the column mappings.
*   **Error Handling**: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_MILESTONE from SEQC_MILESTONE

*   **Source**: `OLEDB_SRC-MLST_GCS` (OLE DB Source) reading from table `MLST`
*   **Destination**: `OLEDEB_DST-SAP_PROJECT_MILESTONE` (OLE DB Destination) writing to table `SAP_PROJECT_WBS_MILESTONE`
*   **Transformations**: Data type conversions are implied from the column mappings.
*   **Error Handling**: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_WBS\_WORKPLAN\_DESCRIPTION from SEQC_MILESTONE

*   **Source**: `OLEDB_SRC-AFVU JOIN AFVV_GCS` (OLE DB Source) reading from table `AFVU` and `AFVV`
*   **Destination**: `OLEDEB_DST-SAP_PROJECT_WBS_WORKPLAN_DESCRIPTION_GCS` (OLE DB Destination) writing to table `SAP_PROJECT_WBS_WORKPLAN_DESCRIPTION`
*   **Transformations**: Data type conversions are implied from the column mappings.
*   **Error Handling**: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_WBS\_WORKPLAN from SEQC_MILESTONE

*   **Source**: `OLEDB_SRC-AFVC join PRPS_GCS` (OLE DB Source) reading from table `AFVC` and `PRPS`
*   **Destination**: `OLEDB_DST-SAP_PROJECT_WBS_WORKPLAN_GCS` (OLE DB Destination) writing to table `SAP_PROJECT_WBS_WORKPLAN`
*   **Transformations**: Data type conversions are implied from the column mappings.
*   **Error Handling**: Error output defined on both source and destination components.

#### DFT-SAP\_VENDOR\_CONTACT\_DETAIL within SEQC\_04

*   **Source**: `OLEDBSRC-zastk`
    *   Connection: `ODS_GC_SOURCE_DB`
    *   SQL Query: Extracts vendor contact details from the `zastk` table.
    *   Columns: `VENDOR_NBR`, `CONTACT_DETAIL_LANGUAGE_CD`, `OFFICIAL_LANGUAGE_CD`, `OPERATING_VENDOR_NAME_1_TXT`, etc.
*   **Destination**: `OLEDBDEST-SAP_VENDOR_CONTACT_DETAIL`
    *   Connection: The destination connection is not included in the XML
    *   Table: Target table is not included in the XML
    *   Data Flow: Moves data from `OLEDBSRC-zastk` directly to the destination.
*   **Transformations**: None.
*   **Error Handling**: Error outputs are defined for the source and destination, allowing for error redirection.

#### DFT\_SAP\_PROJECT\_WBS\_CROSS\_CUTTING\_SCORE within SEQC\_04

*   **Source**: `OLE DB_SRC_ZAPS_CCMWBS`
    *   Connection: `ODS_GC_SOURCE_DB`
    *   SQL Query: Extracts project WBS cross-cutting score from the ZAPS\_CCMWBS table.
    *   Columns: `WBS_NBR`, `MARKER_TYPE_CD`, `MARKER_CD`, `MARKER_SCORE_PCT`, `PROJECT_WBS_OBJECT_NBR`, `SOURCE_ID`, `ETL_CREA_DT`, `ETL_UPDT_DT`
*   **Destination**: `OLE DB DEST_SAP_PROJECT_WBS_CROSS_CUTTING_SCORE`
    *   Connection: `DATA_HUB`
    *   Table: `dbo.SAP_PROJECT_WBS_CROSS_CUTTING_SCORE`
    *   Data Flow: Moves data from `OLE DB_SRC_ZAPS_CCMWBS` directly to the destination.
*   **Transformations**: None.
*   **Error Handling**: Error outputs are defined for the source and destination, allowing for error redirection.

#### DFT\_SAP_PROJECT_WBS_SECTOR_CROSS_CUTTING\_SCORE within SEQC\_04

*   **Source**: `OLE DB_SRC_ZAPS_CCMWBSSECT`
    *   Connection: `ODS_GC_SOURCE_DB`
    *   SQL Query: Extracts project WBS sector cross-cutting score from the ZAPS\_CCMWBSSECT table.
    *   Columns: `WBS_NBR`, `CROSS_CUTTING_MARKER_TYPE_CD`, `SECTOR_CD`, `SECTOR_MARKER_SCORE_CD`, `ETL_CREA_DT`, `ETL_UPDT_DT`, `SOURCE_ID`
*   **Destination**: `OLE DB DEST_SAP_PROJECT_WBS_SECTOR_CROSS_CUTTING_SCORE`
    *   Connection: `DATA_HUB`
    *   Table: `dbo.SAP_PROJECT_WBS_SECTOR_CROSS_CUTTING_SCORE`
    *   Data Flow: Moves data from `OLE DB_SRC_ZAPS_CCMWBSSECT` directly to the destination.
*   **Transformations**: None.
*   **Error Handling**: Error outputs are defined for the source and destination, allowing for error redirection.

#### DFT-SAP\_DOMAIN\_FIXED\_VALUES (within SEQC\_07)

*   Source: `OLEDBSRC-DD07T` (OLE DB Source) reading potentially from tables `DD07T` and `SAP_SOURCE.dbo.DD07T`
*   Destination: `OLEDBDEST-SAP_DOMAIN_FIXED_VALUES` (OLE DB Destination) writing to table `SAP_DOMAIN_FIXED_VALUES`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_FUNCTIONAL\_AREA (within SEQC\_07)

*   Source: `OLEDBSRC-TFKB` (OLE DB Source) reading from potentially tables `TFKB` and `TFKBT`
*   Destination: `OLEDBDEST-SAP_FUNCTIONAL_AREA` (OLE DB Destination) writing to table `SAP_FUNCTIONAL_AREA`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_FUND\_RESERVATION\_COMMITMENT (Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-KBLK` (OLE DB Source) reading from table `KBLK`
*   Destination: `OLEDBDEST-SAP_FUND_RESERVATION_COMMITMENT` (OLE DB Destination) writing to table `SAP_FUND_RESERVATION_COMMITMENT`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_PDS\_ALLOCATION (Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-EKBE` (OLE DB Source) reading from tables  `ZAPS_PDS_CD` and `PRPS`
*   Destination: `OLEDBDEST-SAP_PROJECT_PDS_ALLOCATION` (OLE DB Destination) writing to table `SAP_PROJECT_PDS_ALLOCATION`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_PDS\_ALLOCATION\_Before2023\_11\_04 (Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-EKBE` (OLE DB Source) reading from tables  `ZAPS_PDS_CD` and `PRPS`
*   Destination: `OLEDBDEST-SAP_PROJECT_PDS_ALLOCATION` (OLE DB Destination) writing to table `SAP_PROJECT_PDS_ALLOCATION`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_PROJECT\_PDS\_ALLOCATION\_Not\_used (Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-EKBE` (OLE DB Source) reading from tables  `ZAPS_PDS_CD` and `PRPS`
*   Destination: `OLEDBDEST-SAP_PROJECT_PDS_ALLOCATION` (OLE DB Destination) writing to table `SAP_PROJECT_PDS_ALLOCATION`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_PURCHASE\_ORDER\_CONSUMPTION (Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-EKBE` (OLE DB Source) reading from table `KBLK`
*   Destination: `OLEDBDEST-SAP_PURCHASE_ORDER_CONSUMPTION` (OLE DB Destination) writing to table `SAP_PURCHASE_ORDER_CONSUMPTION`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_PURCHASE\_ORDER\_LINE\_ITEM(Disabled) (within SEQC\_07)

*   Source: `OLEDBSRC-EKPO` (OLE DB Source) reading from table `EKPO`
*   Destination: `OLEDBDEST-SAP_PURCHASE_ORDER_LINE_ITEM` (OLE DB Destination) writing to table `SAP_PURCHASE_ORDER_LINE_ITEM`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_VENDOR\_ACCOUNT\_GROUP 1 (within SEQC\_07)

*   Source: `OLEDB_SRC-T077Y_EN` (OLE DB Source) reading from table `T077Y` (English)
*   Source: `OLEDB_SRC-T077Y_FR` (OLE DB Source) reading from table `T077Y` (French)
*   Transformation: `Merge Join` joins the two sources on `KTOKK`
*   Transformation: `DRVCOL_TRFM-NEW-COLUMNS` creates the final table key and default values
*   Transformation: `Data Conversion` converts the `SAP_MERGE_SOURCE_CD` to its final form
*   Destination: `OLEDB_DEST-SAP_VENDOR_ACCOUNT_GROUP` (OLE DB Destination) writing to table `SAP_VENDOR_ACCOUNT_GROUP`
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_VENDOR\_CHANNEL(within SEQC\_07)

*   Source: `OLEDBSRC-zafi_cod` (OLE DB Source) reading from table `zafi_cod`
*   Destination: `OLEDBDEST-SAP_VENDOR_CHANNEL` (OLE DB Destination) writing to table `SAP_VENDOR_CHANNEL`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### DFT-SAP\_VENDOR\_NAME\_SWS (within SEQC\_07)

*   Source: `OLEDBSRC-lfa1` (OLE DB Source) reading from table `lfa1`
*   Destination: `OLEDBDEST-SAP_VENDOR_NAME_SWS` (OLE DB Destination) writing to table `SAP_VENDOR_NAME_SWS`
*   Transformations: None explicitly defined, but data type conversions are implied from the column mappings.
*   Error Handling: Error output defined on both source and destination components.

#### Sequence Containers

*   **`SEQ-06`**: This sequence container appears to be responsible for loading SAP-related tables into the Data Hub. It contains several Data Flow Tasks, each responsible for loading a specific SAP table/entity.
*   **`SEQC-GCS-FAS_MERGE-STAGING TABLE`**: This sequence container is responsible for truncating and loading the staging table `S_SAP_GCS_FAS_WBS_MAP`.
*   **`SEQC-Initialize_Tables_For_GCS_loading`**: This sequence container is responsible for truncating several tables in the Data Hub.
*   **`SEQC_01_Load_GCS`**: This sequence container appears to be responsible for loading SAP-related tables into the Data Hub. It contains several Data Flow Tasks, each responsible for loading a specific SAP table/entity.
*   **`SEQC_04`**: Loads SAP project and vendor data.
*   **`SEQC_05`**: Loads SAP Dimensions.
*   **`SEQC_07`**: Loads SAP Budget data.
*   **Sequence Container SEQC_MILESTONE**: Loads SAP Milestone data.

## 4. Code Extraction

```sql
-- OLEDBSRC-MLTX (DFT-SAP_MILESTONE) SQL Command
--use GC_SOURCE_DB;

SELECT T1.MLTX_ZAEHL AS MILESTONE_NBR
	,CASE 
		WHEN charindex('-', T1.KTEXT) > 0
			THEN CASE 
					WHEN T1.MLTX_ZAEHL = '000000043789'
						THEN NULL --temproary fix by hardcoding, re-runing MLST could be solution
					WHEN T1.MLTX_ZAEHL = '000000044005'
						THEN NULL
					WHEN T1.MLTX_ZAEHL = '000000044200'
						THEN NULL
					WHEN T1.MLTX_ZAEHL = '000000044369'
						THEN NULL
					WHEN T1.MLTX_ZAEHL = '000000044381'
						THEN NULL
					WHEN T1.MLTX_ZAEHL = '000000044482'
						THEN NULL
					WHEN T1.MLTX_ZAEHL = '000000044965'
						THEN NULL
					ELSE ltrim(substring(T1.KTEXT, charindex('-', T1.KTEXT) + 1, 120))
					END
		ELSE T1.KTEXT
		END AS MILESTONE_EN_NM
	,CASE 
		WHEN charindex('-', T1.KTEXT) > 0
			THEN CASE 
					WHEN substring(T1.KTEXT, 1, charindex('-', T1.KTEXT) - 1) = ' '
						THEN NULL
					ELSE substring(T1.KTEXT, 1, charindex('-', T1.KTEXT) - 1)
					END

		ELSE T1.KTEXT
		END AS MILESTONE_FR_NM
	,T1."KTEXT" AS MILESTONE_NM
	
	,'GCS' AS SAP_MERGE_SOURCE_CD
	,GETDATE() AS ETL_CREA_DT
	,GETDATE() AS ETL_UPDT_DT
FROM MLTX T1

LEFT JOIN SAP_SOURCE.DBO.MLTX T2
on T1.MLTX_ZAEHL=T2.MLTX_ZAEHL
where T2.MLTX_ZAEHL is null
```

```sql
-- OLEDBSRC-PROJ (DFT-SAP_PROJECT) SQL Command
SELECT --TOP (1000)
RTRIM(T1."PSPID") as WBS_NBR,
cast(getdate() as date) AS UPDATE_DT,
RTRIm(T1."POST1") as PROJECT_NM,
RTRIM(T1."ERNAM") as CREATED_BY_USERID,
T1."ERDAT" as CREATION_DT,
RTRIM(T1."AENAM") as LAST_UPDATED_BY_USERID,
T1."AEDAT" as LAST_UPDATED_DT,
T1."PLFAZ" as START_DT,
T1."PLSEZ" as END_DT,
T1."VERNR" as OFFICER_NBR,
T1."PSPNR" as INTERNAL_WBS_NBR,
--T1."LOEVM" as LOGICALLY_DELETED_IND,
   CASE
      WHEN T1.LOEVM = 'X' THEN 1
      ELSE 0
  END  AS "LOGICALLY_DELETED_IND",
T1.OBJNR as PROJ_INTERNAL_CD,
'GCS' as SOURCE_ID,
'GCS'    AS HK_SOURCE_ID,
  getdate() AS "ETL_CREA_DT",
  getdate() AS "ETL_UPDT_DT"  from dbo.PROJ T1
```

```sql
-- OLEDBSRC-PRPS (DFT-SAP_PROJECT_WBS) SQL Command
SELECT

T1."POSID" WBS_NBR,
--substring(T1."POSID",0,8) [PROJECT_NBR],
cast(Getdate() as date)   AS UPDATE_DT,
T1.objnr                  AS PROJECT_WBS_OBJECT_NBR,
T1."pspnr"                AS INTERNAL_WBS_NBR,
T1."post1"                AS WBS_NM,
Ltrim(T1.stufe)           AS WBS_LEVEL,
T1."vernr"                AS OFFICER_NBR,

ISNULL(FICTR.FAS_FICTR,
  CASE
  WHEN Len(T1."fkstl") = '0' THEN NULL
  WHEN T1."fkstl" = ' ' THEN NULL
 -- ELSE Substring('0000000000' + T1."fkstl", Len(T1."fkstl") + 1, 10)
  ELSE  replace(ltrim(replace(T1.[fkstl], '0', ' ')), ' ', '0') 
END    )                   AS FUND_CENTER_NBR,
T1."fkstl"               AS [FKSTL_SRC],
--T1."ernam"                AS CREATED_BY_USERID,
ISNULL(USNAM.FAS_USNAM,T1."ernam")         AS CREATED_BY_USERID,

T1."erdat"                AS CREATION_DT,
T1."aenam"                AS LAST_UPDATED_BY_USERID,
T1."aedat"                AS LAST_UPDATE_DT,
--CASE
--  WHEN rtrim(ltrim(T1.ZAFUND)) = '' THEN NULL
--  ELSE Ltrim(T1.ZAFUND)
--END                       AS FUND_NBR,
--NULL AS FUND_NBR,
ISNULL(GEBER.FAS_GEBER  ,
CASE
  WHEN T1.usr02 = ' ' THEN NULL
  ELSE Ltrim(T1.usr02)
END  )                     AS FUND_NBR,    

T1.psphi                  AS INTERNAL_PROJECT_NBR,
CASE
  WHEN T1."loevm" = 'X' THEN 1
  ELSE 0
END                       AS LOGIC