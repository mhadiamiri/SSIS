## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---|---|---|---|---|---|---|
| DATA_HUB | OLE DB | Server: [Inferred], Database: [Inferred] | Destination for staging data | SQL Server Auth likely | None | Part 1, 2, 3 |
| ARD_OPERA_LANDING | OLE DB | Server: [Inferred], Database: [Inferred] | Source for staging data | SQL Server Auth likely | None | Part 1, 2, 3 |
| DFAIT_Reporting | OLE DB | Server: [Inferred], Database: [Inferred] | Source for user info | SQL Server Auth likely | None | Part 1, 2, 3 |
| ARD_STAGING | OLE DB | Server: [Inferred], Database: [Inferred] | Lookup for  data | SQL Server Auth likely | None | Part 1, 2, 3 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|---|---|---|---|---|---|
| None Found |  |  |  | No dependent SSIS packages tasks found | Part 1, 2, 3 |

## 3. Package Flow Analysis

The package `ARD_OPERA_STAGING` performs the following main actions:

*   **Sequence Containers:** The package is organized using several sequence containers to group related tasks.
*   **Data Flow Tasks:** The majority of the data transformation and loading happens inside Data Flow Tasks (DFTs).
*   **Execute SQL Tasks:** There are also Execute SQL Tasks to truncate staging tables.

#### EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode
Expression Task that evaluates `1 == 1`.

#### SEQC - load_Project_ActivityTypes
This sequence container loads data related to project activity types.

*   **DFT - OPRA_OPSW_ACTIVITIES:** Extracts data, transforms it, and loads it into `OPRA_OPSW_ACTIVITIES`.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLACTIVITIES` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblActivities`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_ACTIVITIES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_ACTIVITIES`.
*   **DFT - OPRA_RO_ACTIVITY_TYPES:** Extracts and loads activity type data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLACTIVITYTYPES` (from `ARD_OPERA_LANDING` connection) extracts data from `ro.tblActivityTypes`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_ACTIVITY_TYPES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_ACTIVITY_TYPES`.
*   **DFT - OPRA_OPSW_PROJECT_PHASES:** Loads project phase data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTPHASES` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectPhases`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_PHASES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_PHASES`.
*   **DFT - OPRA_OPSW_PROJECT_COSTING:** Loads project costing data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTCOSTING` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectCosting`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_COSTING` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_COSTING`.
*   **DFT - OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING:** Loads project WBS costing data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTWBSCOSTING` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectWBSCosting`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING`.
*   **DFT - OPRA_RO_PHASES:** Loads phase data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLPHASES` (from `ARD_OPERA_LANDING` connection) extracts data from `ro.tblPhases`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_PHASES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_PHASES`.
*   **DFT - OPRA_RO_PROJECT_LEVEL_ROLES:** Loads project level role data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLPROJECTLEVELROLES` (from `ARD_OPERA_LANDING` connection) extracts data from `ro.tblProjectLevelRoles`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_PROJECT_LEVEL_ROLES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_PROJECT_LEVEL_ROLES`.
*   **ESQLT- TRUNCATE ALL STAGING TABLES:** Execute SQL Task to truncate a number of tables in `DATA_HUB`.

#### SEQC - load_Project_Scope
This sequence container loads project scope-related data.

*   **DFT - OPRA_OPSW_PROJECT_SCOPE:** Extracts and loads project scope data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTSCOPE` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectScope`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_SCOPE` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_SCOPE`.
*  **DFT - OPRA_OPSW_PROJECT_FLAGGED_ISSUES:** Loads project flagged issues data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTFLAGGEDISSUES` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectFlaggedIssues`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_FLAGGED_ISSUES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_FLAGGED_ISSUES`.
*   **DFT - OPRA_OPSW_PROJECT_PRIORITY_HEADERS:** Loads project priority header data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTPRIORITYHEADERS` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectPriorityHeaders`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_PRIORITY_HEADERS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_PRIORITY_HEADERS`.
*   **DFT - OPRA_OPSW_PROJECT_PRIORITY_SECTIONS:** Loads project priority sections data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTPRIORITYSECTIONS` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectPrioritySections`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_PRIORITY_SECTIONS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_PRIORITY_SECTIONS`.
*   **DFT - OPRA_RO_PLANNING_CYCLE_STATUSES:** Loads planning cycle status data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLPLANNINGCYCLESTATUSES` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblPlanningCycleStatuses`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_PLANNING_CYCLE_STATUSES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_PLANNING_CYCLE_STATUSES`.
*   **ESQLT- TRUNCATE ALL STAGING TABLES:** Execute SQL Task to truncate a number of tables in `DATA_HUB`.

#### SEQC - load_Question_Answers
This sequence container loads data related to project questions and answers.

*   **DFT - OPRA_OPSW_PROJECT_PCRA_QUESTION_ANSWERS:** Loads project PCRA question answer data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTPCRAANSWERS` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectPCRAAnswers`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
        *  `LKP - tblPCRAQuestions`: Lookup to RO.tblPCRAQuestions
        *  `LKP - OPRA_OPSW_PROJECT_UPDATES_LKP`: Lookup to OPRA_OPSW_PROJECT_UPDATES_LKP
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_PCRA_QUESTION_ANSWERS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_PCRA_QUESTION_ANSWERS`.
*   **DFT - OPRA_RO_PCRA_QUESTIONS:** Loads PCRA question data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLPCRAQUESTIONS` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblPCRAQuestions`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_PCRA_QUESTIONS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_PCRA_QUESTIONS`.
*   **DFT - OPRA_OPSW_PROJECT_RESOURCES:** Loads project resources data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLPROJECTRESOURCES` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblProjectResources`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_PROJECT_RESOURCES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_RESOURCES`.
*   **DFT - OPRA_OPSW_TOKEN_OVERRIDES:** Loads token overrides data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLTOKENOVERRIDES` (from `ARD_OPERA_LANDING` connection) extracts data from `OPSW.tblTokenOverrides`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_OPSW_TOKEN_OVERRIDES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_TOKEN_OVERRIDES`.
*   **DFT - OPRA_RO_RECORD_STATE_ROLES:** Loads record state role data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLRECORDSTATEROLES` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblRecordStateRoles`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_RECORD_STATE_ROLES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_RECORD_STATE_ROLES`.
*   **DFT - OPRA_RO_QUESTIONNAIRES:** Loads questionnaire data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLQUESTIONNAIRES` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblQuestionnaires`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_QUESTIONNAIRES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_QUESTIONNAIRES`.
*   **DFT - OPRA_RO_ROM_ESTIMATES:** Loads ROM estimates data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLROMESTIMATES` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblROMEstimates`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_ROM_ESTIMATES` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_ROM_ESTIMATES`.
*   **DFT - OPRA_USERS:** Loads user data.
    *   **Source:** `OLEDB_SOURCE - D_AD_SIGNON` (from `DFAIT_Reporting` connection) extracts data from `dbo.D_AD_SIGNON`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_USERS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_USERS`.
*   **ESQLT- TRUNCATE ALL STAGING TABLES:** Execute SQL Task to truncate a number of tables in `DATA_HUB`.

#### SEQC - load_Release 23 tables
This sequence container loads data related to project funding.

*   **DFT - OPRA_OPSW_PROJECT_IWP_NUMBERS:** Loads project IWP numbers data.
    *   **Source:** `OLEDB_SOURCE - OPSW_TBLPROJECTIWPNUMBERS` (from `ARD_OPERA_LANDING` connection) extracts data from `OpsW.tblProjectIWPNumbers`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_PROJECT_IWP_NUMBERS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_OPSW_PROJECT_IWP_NUMBERS`.
*   **DFT - OPRA_RO_DEFAULT_WBS_WEIGHTS:** Loads default WBS weights data.
    *   **Source:** `OLEDB_SOURCE - RO_TBLDEFAULTWBSWEIGHTS` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblDefaultWBSWeights`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_DEFAULT_WBS_WEIGHTS` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_DEFAULT_WBS_WEIGHTS`.
*   **DFT - OPRA_RO_INTAKE_CATEGORY:** Loads intake category data.
    *   **Source:** `OLEDB_SOURCE - tblIntakeCategory` (from `ARD_OPERA_LANDING` connection) extracts data from `RO.tblIntakeCategory`.
    *   **Transformations:**
        *   `DRV_TRFM_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DEST - OPRA_RO_INTAKE_CATEGORY` (to `DATA_HUB` connection) loads data into `dbo.OPRA_RO_INTAKE_CATEGORY`.
*   **ESQLT- TRUNCATE ALL STAGING TABLES:** Execute SQL Task to truncate a number of tables in `DATA_HUB`.

#### Sequence Container
*   **DFT - SRSF_AREA:** Loads SRSF area data.
    *   **Source:** `OLEDB_SRC - Area` (from `ARD_OPERA_LANDING` connection) extracts data from `dbo.Area`.
    *   **Transformations:**
        *   `DRV_TRFM - DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DESC - SRSF_AREA` (to `DATA_HUB` connection) loads data into `dbo.SRSF_AREA`.
*   **DFT - SRSF_AREA_REGION:** Loads SRSF area region data.
    *   **Source:** `OLEDB_SRC - AreaRegion` (from `ARD_OPERA_LANDING` connection) extracts data from `AreaRegion`.
    *   **Transformations:**
        *   `DRV_TRFM - DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DESC - SRSF_AREA_REGION` (to `DATA_HUB` connection) loads data into `dbo.SRSF_AREA_REGION`.
*   **DFT - SRSF_REGION:** Loads region data.
    *   **Source:** `OLEDB_SRC - Region` (from `ARD_OPERA_LANDING` connection) extracts data from `dbo.Region`.
    *   **Transformations:**
        *   `DRV_TRFM - DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_DESC - SRSF_REGION` (to `DATA_HUB` connection) loads data into `dbo.SRSF_REGION`.
*   **DFT - SRSF_RMO:** Loads RMO data.
    *   **Source:** `OLEDB_SRC - RMO` (from `ARD_OPERA_LANDING` connection) extracts data from `dbo.RMO`.
    *   **Transformations:**
        *   `DRV_TRFM - DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns.
    *   **Destination:** `OLEDB_SRC - SRSF_RMO` (to `DATA_HUB` connection) loads data into `dbo.SRSF_RMO`.
*   **ESQLT- TRUNCATE ALL STAGING TABLES 1:** Execute SQL Task to truncate a number of tables in `DATA_HUB`.

## 4. Code Extraction
SQL queries used in OLE DB Sources:

```sql
-- From OLEDB_SOURCE - OPSW_TBLACTIVITIES inside DFT - OPRA_OPSW_ACTIVITIES
SELECT 
 act_ID AS ACTIVITY_ID 
, act_pph_ID AS ACTIVITY_PPH_ID
, act_att_ID AS ACTIVITY_ATT_ID
, case when act_Start = '0001-01-01' then null else cast(act_Start as datetime) end AS ACTIVITY_START_DT
, case when act_End = '0001-01-01' then null else cast(act_End as datetime) end AS ACTIVITY_END_DT

, act_Comment AS ACTIVITY_COMMENT_TXT
, convert(int, act_IsActive) AS ACTIVITY_ACTIVE_IND
, act_LastUpdated AS ACTIVITY_LAST_UPDATE_DTM
, act_UpdatedBy AS ACTIVITY_LAST_UPDATE_USER_NM

FROM [OpsW].[tblActivities]
```

```sql
-- From OLEDB_SOURCE - RO_TBLACTIVITYTYPES inside DFT - OPRA_RO_ACTIVITY_TYPES
SELECT 
 att_ID AS ACTIVITY_TYPE_ID
, att_pha_id AS ACTIVITY_TYPE_PHA_ID
, att_DescriptionE AS ACTIVITY_TYPE_EN_DESCR
, att_DescriptionF AS ACTIVITY_TYPE_FR_DESCR
, att_SortOrder AS ACTIVITY_TYPE_SORT_ORDER_NBR
, convert(int, att_IsActive) AS ACTIVITY_TYPE_ACTIVE_IND
, att_LastUpdated AS ACTIVITY_TYPE_LAST_UPDATED_DTM
, att_UpdatedBy AS ACTIVITY_TYPE_LAST_UPDATED_USER_NM
, att_EditableID AS ACTIVITY_TYPE_EDITIABLE_ID
, att_wbs_ID AS ACTIVITY_WBS_ID
, convert(int, att_IsSchedulable) AS ACTIVITY_TYPE_SCHEDULABLE_IND
FROM ro.tblActivityTypes
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTPHASES inside DFT - OPRA_OPSW_PROJECT_PHASES
SELECT 
 pph_id AS PROJECT_PHASE_ID
, pph_pup_id AS PROJECT_PHASE_PUP_ID
, pph_Phase_id AS PROJECT_PHASE_PPH_ID
, pph_Start AS PROJECT_PHASE_START_DT
, pph_End AS PROJECT_PHASE_END_DT
, pph_Comment AS PROJECT_PHASE_COMMENT_TXT
, CONVERT(INT, pph_IsActive) AS PROJECT_PHASE_ACTIVE_IND
, pph_LastUpdated AS PROJECT_PHASE_LAST_UPDATE_DTM
, pph_UpdatedBy AS PROJECT_PHASE_LAST_UPDATE_USER_NM

FROM OpsW.tblProjectPhases
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTCOSTING inside DFT - OPRA_OPSW_PROJECT_COSTING
SELECT 
 prc_id AS PROJECT_COSTING_ID
, prc_Value AS PROJECT_COSTING_VALUE_AMT
, prc_Comment AS PROJECT_COSTING_COMMENT_TXT
, convert(int, prc_IsActive) AS PROJECT_COSTING_ACTIVE_IND
, prc_LastUpdated AS PROJECT_COSTING_LAST_UPDATED_DTM
, prc_UpdatedBy AS PROJECT_COSTING_LAST_UPDATED_USER_NM
, prc_pup_ID AS PROJECT_COSTING_PROJECT_UPDATE_ID
, prc_Date AS PROJECT_COSTING_DTM
, prc_wbs_id AS PROJECT_COSTING_WORK_BREAKDOWN_STRUCTURE_ID
, prc_prg_id AS PROJECT_COSTING_PROGRAM_ID
, prc_fus_id AS PROJECT_COSTING_FUND_SOURCE_ID

FROM OpsW.tblProjectCosting
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTWBSCOSTING inside DFT - OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING
SELECT 
 pwc_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_ID
, pwc_pup_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_PROJECT_UPDATE_ID
, pwc_wbs_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_WORK_BREAKDOWN_STRUCTURE_ID
, pwc_Value AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_VALUE_AMT
, pwc_IsActive AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_ACTIVE_IND
, pwc_LastUpdated AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_LAST_UPDATED_DTM
, pwc_UpdatedBy AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_LAST_UPDATED_USER_NM
FROM OpsW.tblProjectWBSCosting
```

```sql
-- From OLEDB_SOURCE - RO_TBLPHASES inside DFT - OPRA_RO_PHASES
SELECT 
 pha_id AS PHASE_ID
, pha_EditableId AS PHASE_EDITIABLE_ID
, pha_DescriptionE AS PHASE_EN_DESCR
, pha_DescriptionF AS PHASE_FR_DESCR
--, pha_plr_id_Lead AS PHASE_PLR_ID
, pha_SortOrder AS PHASE_SORT_ORDER_NBR
, CONVERT(INT, pha_IsActive) AS PROJECT_PHASE_ACTIVE_IND
, pha_LastUpdated AS PROJECT_PHASE_LAST_UPDATE_DTM
, pha_UpdatedBy AS PHASE_LAST_UPDATE_USER_NM

FROM ro.tblPhases
```

```sql
-- From OLEDB_SOURCE - RO_TBLPROJECTLEVELROLES inside DFT - OPRA_RO_PROJECT_LEVEL_ROLES
SELECT 
 plr_id AS PROJECT_LEVEL_ROLE_ID
, plr_EditableId AS PROJECT_LEVEL_ROLE_EDITIABLE_ID
, plr_Code AS PROJECT_LEVEL_ROLE_CD
, plr_DescriptionE AS PROJECT_LEVEL_ROLE_EN_DESCR
, plr_DescriptionF AS PROJECT_LEVEL_ROLE_FR_DESCR
, plr_SortOrder AS PROJECT_LEVEL_ROLE_SORT_ORDER_NBR
, CONVERT(INT, plr_IsActive) AS PROJECT_LEVEL_ROLE_ACTIVE_IND
, plr_LastUpdated AS PROJECT_LEVEL_ROLE_LAST_UPDATE_DTM
, plr_UpdatedBy AS PROJECT_LEVEL_ROLE_LAST_UPDATE_USER_NM
--, plr_ApplicationRole AS PROJECT_LEVEL_ROLE_APPLICATION_NM
--, plr_ManagerApplicationRole AS PROJECT_LEVEL_ROLE_MANAGER_APPLICATION_NM

FROM ro.tblProjectLevelRoles
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTFLAGGEDISSUES inside DFT - OPRA_OPSW_PROJECT_FLAGGED_ISSUES
SELECT 
pfi_ID AS PROJECT_FLAGGED_ISSUES_ID 
,pfi_pup_id AS PROJECT_FLAGGED_ISSUES_PUP_ID
,pfi_pri_id AS PROJECT_FLAGGED_ISSUES_PRI_ID
,pfi_Severity_id AS PROJECT_FLAGGED_ISSUES_SEVERITY_ID
,convert(int, pfi_IsActive) AS PROJECT_FLAGGED_ISSUES_ACTIVE_IND
,pfi_LastUpdated AS PROJECT_FLAGGED_ISSUES_LAST_UPDATED_DTM
,pfi_UpdatedBy AS PROJECT_FLAGGED_ISSUES_LAST_UPDATED_USER_NM
,pfi_Description AS PROJECT_FLAGGED_ISSUES_DESCR

FROM OpsW.tblProjectFlaggedIssues
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTPRIORITYHEADERS inside DFT - OPRA_OPSW_PROJECT_PRIORITY_HEADERS
SELECT 
 pph_ID AS PROJECT_PRIORITY_HEADER_ID
,pph_pup_ID AS PROJECT_PRIORITY_HEADER_PUP_ID
--,pph_CompletionDate AS PROJECT_PRIORITY_HEADER_COMPLETION_DTM
,pph_LastUpdated AS PROJECT_PRIORITY_HEADER_LAST_UPDATED_DTM
,pph_UpdatedBy AS PROJECT_PRIORITY_HEADER_LAST_UPDATED_USER_NM
--,pph_IsCompletionDateRequired AS PROJECT_PRIORITY_HEADER_COMPLETION_DATE_IND
,pph_TotalScore AS PROJECT_PRIORITY_HEADER_TOTAL_SCORE_NBR
,pph_ImpactOfDelay AS PROJECT_PRIORITY_HEADER_IMPACT_OF_DELAY_TXT
,pph_roe_id AS PROJECT_PRIORITY_HEADER_ROE_ID
,pph_ProblemStatement AS PROJECT_PRIORITY_HEADER_PROBLEM_STATEMENT_DESCR
, pph_RomEstimate as PROJECT_PRIORITY_HEADER_ROM_ESTIMATE

FROM OpsW.tblProjectPriorityHeaders
```

```sql
-- From OLEDB_SOURCE - OPSW_TBLPROJECTWBSCOSTING inside DFT - OPRA_OPSW_PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING
SELECT 
 pwc_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_ID
, pwc_pup_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_PROJECT_UPDATE_ID
, pwc_wbs_ID AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_WORK_BREAKDOWN_STRUCTURE_ID
, pwc_Value AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_VALUE_AMT
, pwc_IsActive AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_ACTIVE_IND
, pwc_LastUpdated AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_LAST_UPDATED_DTM
, pwc_UpdatedBy AS PROJECT_WORK_BREAKDOWN_STRUCTURE_COSTING_LAST_UPDATED_USER_NM
FROM OpsW.tblProjectWBSCosting
```

```sql
-- From OLEDB_SOURCE - RO_TBLQUESTIONNAIRES inside DFT - OPRA_RO_ACTIVITY_TYPES
SELECT 
que_ID AS QUESTIONNAIRE_ID
,que_Key AS QUESTIONNAIRE_KEY_TXT
,que_NameE AS QUESTIONNAIRE_NAME_EN_DESCR
,que_NameF AS QUESTIONNAIRE_NAME_FR_DESCR
,CONVERT(INT, que_IsActive) AS QUESTIONNAIRE_ACTIVE_IND
,que_LastUpdated AS QUESTIONNAIRE_LAST_UPDATED_DTM
,que_UpdatedBy AS QUESTIONNAIRE__UPDATED_USER_NM

FROM ro.tblQuestionnaires
```

```sql
-- From OLEDB_SOURCE - RO_TBLRECORDSTATEROLES inside DFT - OPRA_RO_ACTIVITY_TYPES
SELECT 
rsr_ID AS RECORD_STATE_ROLE_ID
,rsr_rst_ID AS RECORD_STATE_ROLE_RST_ID
,rsr_plr_ID AS RECORD_STATE_ROLE_PLR_ID
,CONVERT(INT, rsr_IsActive) AS RECORD_STATE_ROLE_ACTIVE_IND
,rsr_LastUpdated AS RECORD_STATE_ROLE_LAST_UPDATE_DTM
,rsr_UpdatedBy AS PROJECT_PHASE_LAST_UPDATE_USER_NM

FROM RO.tblRecordStateRoles
```

```sql
-- From OLEDB_SOURCE - RO_TBLROMESTIMATES inside DFT - OPRA_RO_ACTIVITY_TYPES
SELECT 
roe_id AS ROM_ESTIMATE_ID
,roe_EditableId AS ROM_ESTIMATE_EDITIABLE_ID
,roe_DescriptionE AS ROM_ESTIMATE_EN_DESCR
,roe_DescriptionF AS ROM_ESTIMATE_FR_DESCR
,roe_SortOrder AS ROM_ESTIMATE_SORT_ORDER_NBR
,CONVERT(INT, roe_IsActive) AS ROM_ESTIMATE_ACTIVE_IND
,roe_LastUpdated AS ROM_ESTIMATE_LAST_UPDATED_DTM
,roe_UpdatedBy AS ROM_ESTIMATE_LAST_UPDATED_USER_NM

FROM RO.tblROMEstimates
```

```sql
-- From OLEDB_SOURCE - D_AD_SIGNON inside DFT - OPRA_USERS
SELECT [SIGNON] AS USER_ID
, cast(rtrim(ltrim([SURNAME])) + ', ' + rtrim(ltrim([GIVEN_NAME])) + ' -' + ltrim([DFAITORGCODE]) as Nvarchar(50))
AS USER_DISPLAY_NM
, CAST(rtrim(ltrim([DFAITORGCODE])) AS VARCHAR(50)) AS USER_ORG_ABBR_CD
, CAST( 
REPLACE(rtrim(ltrim([GIVEN_NAME]))+'.'+rtrim(ltrim([SURNAME])), ' ', '') + '@international.gc.ca '  
AS NVARCHAR(255)
)
AS USER_EMAIL_TXT
FROM [dbo].[D_AD_SIGNON]
```

```sql
-- From LKP - OPRA_OPSW_PROJECT_UPDATES_LKP inside DFT - OPRA_OPSW_ACTIVITIES_LKP
SELECT 
PROJECT_UPDATE_ID
, PROJECT_ID
, PROJECT_UPDATE_FINANCIAL_SNAPSHOT_DT_ID
, PROJECT_MISSION_ID
FROM dbo.OPRA_OPSW_PROJECT_UPDATES_LKP
```

```sql
-- From LKP - tblActivityTypes inside DFT - OPRA_OPSW_ACTIVITIES_LKP
SELECT 
att_ID
, att_pha_id AS ACTIVITY_TYPE_PHASE_ID
, att_wbs_ID ACTIVITY_WBS_ID
FROM RO.tblActivityTypes
```

```sql
-- From LKP - tblProjectPhases inside DFT - OPRA