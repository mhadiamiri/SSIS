```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| ARD_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination for dimension tables | SQL Server Auth likely | None            | Part 1, 2, 3                  |
| MART_COM           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for common date dimension             | SQL Server Auth likely            |  None                  | Part 2                 |
| DATA_HUB           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for dimension tables             | SQL Server Auth likely            |  None                  | Part 2, 3                |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package `ARD_OPERA_DIMENSION.dtsx` performs the following tasks:

*   **Control Flow:**
    1.  `Dimensions - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` (Expression Task)
    2.  `SEQC - TRUNCATE TABLES & INSERT UNKNOWN MEMBER` Sequence Container
        *   `ESQLT- DIMENSION TRUNCATE TABLES` (Execute SQL Task)
        *   `DFT - INSERT UNKNOWN MEMBERS` (Data Flow Task)
    3.  `SEQC-LOAD DIMENSION TABLES1` Sequence Container
        *   `DFT - D_OPRA_DATE` (Data Flow Task)
        *   `DFT - D_OPRA_PROGRAM` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT` (Data Flow Task)
        *    `DFT - D_OPRA_PROJECT_UPDATE` (Data Flow Task)
        *    `DFT - D_OPRA_WORK_BREAKDOWN_STRUCTURE` (Data Flow Task)
    4.  `SEQC-LOAD DIMENSION TABLES2` Sequence Container
        *   `DFT - D_OPRA_FUND_SOURCE` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_ACTIVITY` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_COSTING` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_ACTIVITY_TYPE` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_PHASE` (Data Flow Task)
    5.  `SEQC-LOAD DIMENSION TABLES3` Sequence Container
        *   `DFT - D_OPRA_PCRA_SECTION` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_FLAGGED_ISSUE` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_ISSUE` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_PRIORITY_SECTION` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_PRIORITY_HEADER` (Data Flow Task)
    6.   `SEQC-LOAD DIMENSION TABLES4` Sequence Container
        *   `DFT - D_OPRA_PROJECT_PCRA_QUESTION` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_PCRA_VALID_ANSWER` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_PCRA_QUESTION_ANSWER` (Data Flow Task)
        *   `DFT - D_OPRA_PROJECT_RESOURCE` (Data Flow Task)
        *   `DFT - D_OPRA_SYSTEM_USER` (Data Flow Task)

#### DFT - INSERT UNKNOWN MEMBERS

*   **Source:** Several OLE DB Sources (Uncoded)
*   **Transformations:** Several Derived Column Transformations (DATES)
*   **Destinations:** Several OLE DB Destinations (Uncoded) to dimension tables

#### DFT - D_OPRA_DATE

*   **Source:** OLE DB Source (OLEDB\_SRC - D\_COM_DATE) from `dbo.D_COM_DATE`
*   **Transformations:**
    *   `Derived Column`: Adds current year information.
*   **Destinations:** OLE DB Destination (OLEDB\_DEST - D\_OPRA\_DATE) to `dbo.D_OPRA_DATE`

#### DFT - D_OPRA_PROGRAM

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_RO\_PROGRAM) from `dbo.OPRA_RO_PROGRAMS`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROGRAM) to `dbo.D_OPRA_PROGRAM`

#### DFT - D_OPRA_PROJECT

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPR\_PROJECT) from `dbo.OPRA_OPR_PROJECT`
*   **Transformations:**
    *   `Lookup`: Retrieves project type, mission, and accommodation information from related tables.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT) to `dbo.D_OPRA_PROJECT`

#### DFT - D_OPRA_PROJECT_UPDATE

*   **Source:** OLE DB Source (OLEDB\_SRC - D-OPRA\_PROJECT_UPDATE) from `dbo.OPRA_OPSW_PROJECT_UPDATES`
*   **Transformations:**
     *   `Lookup`: Retrieves record state information.
     *   `Lookup`: Retrieves funding source information.
     *   `Lookup`: Retrieves project scope information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID and cutoff date.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_UPDATE) to `dbo.D_OPRA_PROJECT_UPDATE`

#### DFT - D_OPRA_WORK_BREAKDOWN_STRUCTURE

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_RO\_WORK_BREAKDOWN_STRUCTURCE) from `dbo.OPRA_RO_WORK_BREAKDOWN_STRUCTURE`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_WORK_BREAKDOWN_STRUCTURE) to `dbo.D_OPRA_WORK_BREAKDOWN_STRUCTURE`

#### DFT - D_OPRA_FUND_SOURCE

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPR_FUNDING_SOURCE) from `dbo.OPRA_OPR_FUNDING_SOURCE`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_FUND_SOURCE) to `dbo.D_OPRA_FUND_SOURCE`

#### DFT - D_OPRA_PROJECT_ACTIVITY

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_ACTIVITIES) from `dbo.OPRA_OPSW_ACTIVITIES`
*   **Transformations:**
    *    `Lookup`: Retrieves project activity type information.
    *    `Lookup`: Retrieves work breakdown structure information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_ACTIVITY) to `dbo.D_OPRA_PROJECT_ACTIVITY`

#### DFT - D_OPRA_PROJECT_COSTING

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_COSTING) from `dbo.OPRA_OPSW_PROJECT_COSTING`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_COSTING) to `dbo.D_OPRA_PROJECT_COSTING`

#### DFT - D_OPRA_PROJECT_ACTIVITY_TYPE

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_RO\_ACTIVITY_TYPES) from `dbo.OPRA_RO_ACTIVITY_TYPES`
*   **Transformations:**
    *   `Lookup`: Retrieves phase information.
    *   `Lookup`: Retrieves work breakdown structure information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_ACTIVITY_TYPE) to `dbo.D_OPRA_PROJECT_ACTIVITY_TYPE`

#### DFT - D_OPRA_PROJECT_PHASE

*   **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_PHASES) from `dbo.OPRA_OPSW_PROJECT_PHASES`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_PHASE) to `dbo.D_OPRA_PROJECT_PHASE`

#### DFT - D_OPRA_PCRA_SECTION

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_RO\_PCRA\_SECTIONS) from `dbo.OPRA_RO_PCRA_SECTIONS`
*   **Transformations:**
    *   `Lookup`: Retrieves questionnaire information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PCRA_SECTION) to `dbo.D_OPRA_PCRA_SECTION`

#### DFT - D_OPRA_PROJECT_FLAGGED_ISSUE

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_FLAGGED_ISSUES) from `dbo.OPRA_OPSW_PROJECT_FLAGGED_ISSUES`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_FLAGGED_ISSUE) to `dbo.D_OPRA_PROJECT_FLAGGED_ISSUE`

#### DFT - D_OPRA_PROJECT_ISSUE

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_ISSUES) from `dbo.OPRA_OPSW_PROJECT_ISSUES`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_ISSUE) to `dbo.D_OPRA_PROJECT_ISSUE`

#### DFT - D_OPRA_PROJECT_PRIORITY_SECTION

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_PRIORITY_SECTIONS) from `dbo.OPRA_OPSW_PROJECT_PRIORITY_SECTIONS`
*   **Transformations:**
    *    `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_PRIORITY_SECTION) to `dbo.D_OPRA_PROJECT_PRIORITY_SECTION`

#### DFT - D_OPRA_PROJECT_PRIORITY_HEADER

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_PRIORITY_HEADERS) from `dbo.OPRA_OPSW_PROJECT_PRIORITY_HEADERS`
*   **Transformations:**
    *   `Lookup`: Retrieves ROM estimate information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_PRIORITY_HEADER) to `dbo.D_OPRA_PROJECT_PRIORITY_HEADER`

#### DFT - D_OPRA_PROJECT_PCRA_QUESTION

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_RO\_PCRA\_QUESTIONS) from `dbo.OPRA_RO_PCRA_QUESTIONS`
*   **Transformations:**
    *    `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA\_PROJECT_PCRA_QUESTION) to `dbo.D_OPRA_PROJECT_PCRA_QUESTION`

#### DFT - D_OPRA_PROJECT_PCRA_VALID_ANSWER

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_PCRA_VALID_ANSWERS) from `dbo.OPRA_OPSW_PROJECT_PCRA_VALID_ANSWERS`
*   **Transformations:**
    *    `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_PCRA_VALID_ANSWER) to `dbo.D_OPRA_PROJECT_PCRA_VALID_ANSWER`

#### DFT - D_OPRA_PROJECT_PCRA_QUESTION_ANSWER

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_PCRA_QUESTION_ANSWERS) from `dbo.OPRA_OPSW_PROJECT_PCRA_QUESTION_ANSWERS`
*   **Transformations:**
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_PCRA_QUESTION_ANSWER) to `dbo.D_OPRA_PROJECT_PCRA_QUESTION_ANSWER`

#### DFT - D_OPRA_PROJECT_RESOURCE

*    **Source:** OLE DB Source (OLEDB\_SRC - OPRA\_OPSW\_PROJECT_RESOURCES) from `dbo.OPRA_OPSW_PROJECT_RESOURCES`
*    **Transformations:**
    *   `Lookup`: Retrieves project level role information.
    *   `Lookup`: Retrieves record state information.
    *   `Derived Column`: Adds ETL creation and update dates and dimension ID.
*   **Destinations:** OLE DB Destination (OLEDB\_DESC - D\_OPRA_PROJECT_RESOURCE) to `dbo.D_OPRA_PROJECT_RESOURCE`

## 4. Code Extraction

The code below is used for data extraction:

```sql
SELECT -3 AS [FUND_SOURCE_SID]
      ,-3 AS [FUND_SOURCE_ID]
      ,NULL AS [FUND_SOURCE_CD]
      ,NULL AS [FUND_SOURCE_EN_DESCR]
      ,NULL AS [FUND_SOURCE_FR_DESCR]
      ,NULL AS [FUND_SOURCE_ACTIVE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_FUND_SOURCE - Uncoded` to insert an unknown member.

```sql
SELECT -3 AS [PCRA_SECTION_SID]
      ,-3 AS [PCRA_SECTION_ID]
      ,CONVERT(NVARCHAR(255), 'Uncoded') AS [PCRA_SECTION_NUMBER_TXT]
      ,NULL AS [PCRA_SECTION_CATEGORY_EN_NM]
      ,NULL AS [PCRA_SECTION_NOTES_EN_TXT]
      ,NULL AS [PCRA_SECTION_SORT_ORDER_NBR]
      ,NULL AS [PCRA_SECTION_ACTIVE_IND]
      ,NULL AS [PCRA_SECTION_LAST_UPDATE_USER_NM]
      ,NULL AS [PCRA_SECTION_LAST_UPDATE_DT]
      ,NULL AS [PCRA_SECTION_CATEGORY_FR_NM]
      ,NULL AS [PCRA_SECTION_NOTES_FR_TXT]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_ID]
      ,NULL AS [PCRA_SECTION_SCREENING_IND]
      ,NULL AS [PCRA_SECTION_SCORING_EN_DESCR]
      ,NULL AS [PCRA_SECTION_SCORING_FR_DESCR]
      ,NULL AS [PCRA_SECTION_WEIGHT_NBR]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_KEY_NM]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_EN_NM]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_FR_NM]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_ACTIVE_IND]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_LAST_UPDATE_DT]
      ,NULL AS [PCRA_SECTION_QUESTIONAIRE_LAST_UPDATE_USER_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PCRA_SECTION - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_SID]
      ,'-3' AS [DIM_ID]
      ,-3 AS [PROJECT_ID]
      ,NULL AS [PROJECT_TYPE_ID]
      ,NULL AS [PROJECT_MISSION_ID]
      ,NULL AS [PROJECT_FACILITY_TYPE_ID]
      ,NULL AS [PROJECT_ACCOMMODATION_ID]
--      ,NULL AS [PROJECT_SERIAL_NBR]
      ,NULL AS [PROJECT_DESCR]
      ,NULL AS [PROJECT_ACTIVE_IND]
      ,NULL AS [PROJECT_LAST_UPDATE_DTM]
      ,NULL AS [PROJECT_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_POST_ROM_IND]
      ,NULL AS [PROJECT_TITLE]
      ,NULL AS [PROJECT_FIT_UP_IND]
      ,NULL AS [PROJECT_FROZEN_IND]
   --   ,NULL AS [PROJECT_OLD_SERIAL_NBR]
      ,NULL AS [MISSION_CD]
      ,NULL AS [MISSION_EN_NM]
      ,NULL AS [MISSION_FR_NM]
      ,NULL AS [ACCOMMODATION_PRID]
      --,NULL AS [FACILITY_TYPE_ID]
      ,NULL AS [FACILITY_TYPE_EN_DESCR]
      ,NULL AS [FACILITY_TYPE_FR_DESCR]
      ,NULL AS [PROJECT_TYPE_EN_DESCR]
      ,NULL AS [PROJECT_TYPE_FR_DESCR]
      ,NULL AS [LATEST_PROJECT_UPDATE_ID]
, NULL AS [PROJECT_CODE] 
, NULL AS [PROJECT_PRE_ROM_CODE]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT - Uncoded` to insert an unknown member.

```sql
SELECT  
      -3 AS [PROJECT_ACTIVITY_SID]
      ,-3 AS [PROJECT_ACTIVITY_ID]
      ,NULL AS [PROJECT_ACTIVITY_COMMENT_TXT]
      ,NULL AS [PROJECT_ACTIVITY_ACTIVE_IND]
      ,NULL AS [PROJECT_ACTIVITY_START_DT]
      ,NULL AS [PROJECT_ACTIVITY_END_DT]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_EN_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_FR_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_CD]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_EN_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_FR_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_ACTIVE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_ACTIVITY - Uncoded` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_COSTING_SID]
      ,-3 AS [PROJECT_COSTING_ID]
      ,NULL AS [PROJECT_COSTING_COMMENT_TXT]
      ,NULL AS [PROJECT_COSTING_DT]
      ,NULL AS [PROJECT_COSTING_ACTIVE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_COSTING - Uncoded` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_ACTIVITY_TYPE_SID]
      ,-3 AS [PROJECT_ACTIVITY_TYPE_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_EN_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_FR_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_ACTIVE_IND]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_LAST_UPDATED_DTM]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_LAST_UPDATED_USER_NM]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_EDITIABLE_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_PHASE_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_PHASE_EN_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_PHASE_FR_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_ID]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_CD]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_EN_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_WBS_FR_DESCR]
      ,NULL AS [PROJECT_ACTIVITY_TYPE_SCHEDULABLE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_ACTIVITY_TYPE - Uncoded` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_PHASE_SID]
      ,-3 AS [PROJECT_PHASE_ID]
      ,NULL AS [PROJECT_PHASE_EN_NM]
      ,NULL AS [PROJECT_PHASE_FR_NM]
      ,NULL AS [PROJECT_PHASE_START_DT]
      ,NULL AS [PROJECT_PHASE_END_DT]
      ,NULL AS [PROJECT_PHASE_ACTIVE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PHASE - Uncoded` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_FLAGGED_ISSUE_SID]
      ,-3 AS [PROJECT_FLAGGED_ISSUE_ID]
      ,NULL AS [PROJECT_FLAGGED_ISSUE_SEVERITY_ID]
      ,NULL AS [PROJECT_FLAGGED_ISSUE_ACTIVE_IND]
      ,NULL AS [PROJECT_FLAGGED_ISSUE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_FLAGGED_ISSUE_LAST_UPDATE_USER_NM]
      ,CONVERT(NVARCHAR(MAX), 'Uncoded') AS [PROJECT_FLAGGED_ISSUE_UPDATED_DESCR]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_FLAGGED_ISSUE - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_ISSUE_SID]
      ,-3 AS [PROJECT_ISSUE_ID]
      ,NULL AS [PROJECT_ISSUE_FLAGGED_DT]
      ,NULL AS [PROJECT_ISSUE_RESOLVED_DT]
      ,NULL AS [PROJECT_ISSUE_ACTIVE_IND]
      ,NULL AS [PROJECT_ISSUE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_ISSUE_UPDATED_USER_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_ISSUE - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_PRIORITY_SECTION_SID]
      ,-3 AS [PROJECT_PRIORITY_SECTION_ID]
      ,NULL AS [PROJECT_PRIORITY_SECTION_COMMENT_TXT]
      ,NULL AS [PROJECT_PRIORITY_SECTION_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PRIORITY_SECTION_LAST_UPDATED_USER_NM]
      ,NULL AS [PROJECT_PRIORITY_SECTION_ACTIVE_IND]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PRIORITY_SECTION - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_PRIORITY_HEADER_SID]
      ,-3 AS [PROJECT_PRIORITY_HEADER_ID]
      ,NULL AS [PROJECT_PRIORITY_HEADER_TOTAL_SCORE_NBR]
      ,NULL AS [PROJECT_PRIORITY_HEADER_IMPACT_OF_DELAY_TXT]
      ,NULL AS [PROJECT_PRIORITY_HEADER_PROBLEM_STATEMENT_TXT]
      ,NULL AS [PROJECT_PRIORITY_HEADER_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PRIORITY_HEADER_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_ID]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_EN_DESCR]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_FR_DESCR]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_ACTIVE_IND]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_PRIORITY_HEADER_ROM_ESTIMATE_EDITABLE_ID]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PRIORITY_HEADER - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_PCRA_QUESTION_SID]
      ,-3 AS [PROJECT_PCRA_QUESTION_ID]
      ,NULL AS [PROJECT_PCRA_QUESTION_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_PCRA_QUESTION_EN_DESCR]
      ,NULL AS [PROJECT_PCRA_QUESTION_FR_DESCR]
      ,NULL AS [PROJECT_PCRA_QUESTION_DEFAULT_COMMENT_EN_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_DEFAULT_COMMENT_FR_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_PLACEHOLDER_EN_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_PLACEHOLDER_FR_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_WEIGHT_NBR]
      ,NULL AS [PROJECT_PCRA_QUESTION_REQUIRED_IND]
      ,NULL AS [PROJECT_PCRA_QUESTION_ACTIVE_IND]
      ,NULL AS [PROJECT_PCRA_QUESTION_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PCRA_QUESTION_LAST_UPDATE_USER_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PCRA_QUESTION - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_PCRA_QUESTION_ANSWER_SID]
      ,-3 AS [PROJECT_PCRA_QUESTION_ANSWER_ID]
      ,NULL AS [PROJECT_PCRA_QUESTION_ANSWER_COMMENT]
      ,NULL AS [PROJECT_PCRA_QUESTION_ANSWER_ACTIVE_IND]
      ,NULL AS [PROJECT_PCRA_QUESTION_ANSWER_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PCRA_QUESTION_ANSWER_LAST_UPDATE_USER_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PCRA_QUESTION_ANSWER - Unknown` to insert an unknown member.

```sql
SELECT -3 AS [PROJECT_RESOURCE_SID]
      ,-3 AS [PROJECT_RESOURCE_ID]
      ,NULL AS [PROJECT_RESOURCE_ACTIVE_IND]
      ,NULL AS [PROJECT_RESOURCE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_RESOURCE_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_ID]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_EDITABLE_ID]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_EN_DESCR]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_FR_DESCR]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_ACTIVE_IND]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_TOKEN_HOLDER_TITLE_EN_NM]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_TOKEN_HOLDER_FR_NM]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_EDITABLE_IND]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_APPROVED_IND]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_VALID_BASELINE_IND]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_VALID_GOVERNANCE_IND]
      ,NULL AS [PROJECT_RESOURCE_RECORD_STATE_KEY_TXT]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_ID]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_EDITABLE_ID]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_CD]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_EN_DESCR]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_FR_DESCR]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_ACTIVE_IND]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_LAST_UPDATE_USER_NM]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_APPLICATION_ROLE_NM]
      ,NULL AS [PROJECT_RESOURCE_PROJECT_LEVEL_ROLE_MANAGER_APPLICATION_ROLE_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_RESOURCE - Unknown` to insert an unknown member.

```sql
TRUNCATE TABLE dbo.D_OPRA_PROGRAM;

TRUNCATE TABLE dbo.D_OPRA_PROJECT;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_UPDATE;

TRUNCATE TABLE dbo.D_OPRA_WORK_BREAKDOWN_STRUCTURE;

TRUNCATE TABLE dbo.D_OPRA_DATE

TRUNCATE TABLE dbo.D_OPRA_FUND_SOURCE;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_ACTIVITY;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_COSTING;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_ACTIVITY_TYPE;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PHASE;


TRUNCATE TABLE dbo.D_OPRA_PROJECT_FLAGGED_ISSUE;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_ISSUE;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PRIORITY_SECTION;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PRIORITY_HEADER;

TRUNCATE TABLE dbo.D_OPRA_PCRA_SECTION;


TRUNCATE TABLE dbo.D_OPRA_SYSTEM_USER;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_RESOURCE;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PCRA_QUESTION;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PCRA_VALID_ANSWER;

TRUNCATE TABLE dbo.D_OPRA_PROJECT_PCRA_QUESTION_ANSWER;

--TRUNCATE TABLE dbo.D_OPRA_DATE;
```

This SQL statement is used in `ESQLT- DIMENSION TRUNCATE TABLES` to truncate the dimension tables.

```sql
SELECT -3 AS [PROJECT_PCRA_QUESTION_SID]
      ,-3 AS [PROJECT_PCRA_QUESTION_ID]
      ,NULL AS [PROJECT_PCRA_QUESTION_SORT_ORDER_NBR]
      ,NULL AS [PROJECT_PCRA_QUESTION_EN_DESCR]
      ,NULL AS [PROJECT_PCRA_QUESTION_FR_DESCR]
      ,NULL AS [PROJECT_PCRA_QUESTION_DEFAULT_COMMENT_EN_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_DEFAULT_COMMENT_FR_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_PLACEHOLDER_EN_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_PLACEHOLDER_FR_TXT]
      ,NULL AS [PROJECT_PCRA_QUESTION_WEIGHT_NBR]
      ,NULL AS [PROJECT_PCRA_QUESTION_REQUIRED_IND]
      ,NULL AS [PROJECT_PCRA_QUESTION_ACTIVE_IND]
      ,NULL AS [PROJECT_PCRA_QUESTION_LAST_UPDATE_DT]
      ,NULL AS [PROJECT_PCRA_QUESTION_LAST_UPDATE_USER_NM]
      ,'-3' AS [DIM_ID]
```

This SQL statement is used in `OLEDB_SRC - D_OPRA_PROJECT_PCRA_QUESTION - Unknown` to insert an unknown member.

The following SQL statement is used to find the last project update ID:

```sql
SELECT PROJECT_ID, MAX(PROJECT_UPDATE_ID) AS LATEST_PROJECT_UPDATE_ID FROM DBO.OPRA_OPSW_PROJECT_UPDATES
GROUP BY PROJECT_ID
```

The Derived Column Transformation uses the following expressions:

```
[GETDATE]()
MONTH([GETDATE]()) < 4 ? [YEAR]([GETDATE]()) : ([YEAR]([GETDATE]()) + 1)
(DT_STR,100,1252)PROJECT_ACTIVITY_TYPE_