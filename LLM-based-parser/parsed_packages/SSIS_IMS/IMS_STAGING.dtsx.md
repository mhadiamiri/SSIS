```markdown
## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---|---|---|---|---|---|---|
| IMS_SSIS_DFAIT_STAGING | OLE DB | Server: [Inferred], Database: [Inferred], Authentication: [Inferred] | Used for reading data from source tables and writing data to destination staging tables, and source for lookup | Uses credentials specified in the connection manager. Secure storage of credentials is required. | None apparent in the provided XML. | Part 1, 2, 3, 4 |
| BI_CONFORMED | OLE DB | Server: [Inferred], Database: [Inferred], Authentication: [Inferred] | Used for lookup transformation and source for `S1_IMS_ECONOMIC_OBJECTS` Data Flow. | Uses credentials specified in the connection manager. Secure storage of credentials is required. | None apparent in the provided XML. | Part 1, 2, 3 |
| SAP_SOURCE | OLE DB | Server: [Inferred], Database: [Inferred], Authentication: [Inferred] | Used for source systems and source for `S1_IMS_FUNDS_MGMT_BUDGET_HEADER`, `S1_IMS_FUNDS_MGMT_BUDGET_LINES` and `S1_MM_VENDOR_MASTER` Data Flows. | Uses credentials specified in the connection manager. Secure storage of credentials is required. | None apparent in the provided XML. | Part 1, 2, 3 |
| MART_COM | OLE DB | Server: [Inferred], Database: [Inferred], Authentication: [Inferred] | Used for lookup transformation and Source for `S1_IMS_FISCAL_PERIOD_INFO` and `S1_IMS_FISCAL_YEAR_INFO` Data Flows. | Uses credentials specified in the connection manager. Secure storage of credentials is required. | None apparent in the provided XML. | Part 1, 2 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|---|---|---|---|---|---|
| DFT-S_IMS_P_RATES_YEARLY | Within the same package | Child of SEQC-STAGING TABLES SPRINT 7 - Venkata | Success of DFT-W_IMS_YEARLY_RATES_P | None apparent | Part 3 |
| DFT-W1_FIN_BUDGET | Within the same package | Child of SEQC-STAGING TABLES SPRINT 7 - Venkata | Success of DFT-S_IMS_P_RATES_YEARLY | None apparent | Part 3 |
| None Found | | | | No dependent SSIS packages tasks found | Part 1, 2, 4 |

## 3. Package Flow Analysis

*   The package's main control flow consists of a sequence of tasks to load staging tables from various sources. The main sequence is:

    1.  Expression Task - `EXPRESSIONT- Stage - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`
    2.  Sequence Container - `SEQC-STAGING TABLES GROUP 6`
    3.  Sequence Container - `SEQC-STAGING TABLES SPRINT 1`
    4.  Sequence Container - `SEQC-STAGING TABLES SPRINT 2`
    5.  Sequence Container - `SEQC-STAGING TABLES SPRINT 3`
    6.  Sequence Container - `SEQC-STAGING TABLES SPRINT 4`
    7.  Sequence Container - `SEQC-STAGING TABLES SPRINT 5`
    8.  Sequence Container - `SEQC-STAGING TABLES Sprint 6 - Zahra`
    9.  Sequence Container - `SEQC-STAGING TABLES SPRINT 6 Xiuxin`
    10. Sequence Container - `SEQC-STAGING TABLES SPRINT 7 - Venkata`
    11. Sequence Container - `SEQC-STAGING TABLES Sprint 7 - Zahra GROUP 2`
    12. Sequence Container - `SEQC-STAGING TABLES SPRINT 7 Xiuxin`
    13. Sequence Container - `SEQC-STAGING TABLES Sprint 8 - Venkata`
    14. Sequence Container - `SEQC-STAGING TABLES Sprint 8 - Zahra`

*   **`SEQC-STAGING TABLES GROUP 6`**:
    This sequence container truncates and loads several staging tables.

    *   `ESQLT- Truncate Staging Tables`: Executes SQL to truncate several staging tables.
    *   `DFT - W_IMS_DAILY_RATE_DATERANGES`: Data Flow Task to load table `W_IMS_DAILY_RATE_DATERANGES`.
    *   `DFT - W2_IMS_DAILY_RATES_M`: Data Flow Task to load table `W2_IMS_DAILY_RATES_M`.
    *   `DFT - S_IMS_M_RATES_DAILY`: Data Flow Task to load table `S_IMS_M_RATES_DAILY`.
    *   `DFT - W1_FIN_GL`: Data Flow Task to load table `W1_FIN_GL`.
    *   `DFT-S1_IMS_COMMITMENT_ITEMS`: Data Flow Task to load table `S1_IMS_COMMITMENT_ITEMS`.

*   **`SEQC-STAGING TABLES SPRINT 1`**:
    This sequence container truncates and loads several staging tables.

    *   `ESQLT- Truncate Staging Tables`: Executes SQL to truncate several staging tables.
    *   `DFT- R_FIN_MASTER_LOOKUP`: Data Flow Task to load table `R_FIN_MASTER_LOOKUP`.
    *   `DFT- S1_DEFAULT_MISSION_CURRENCY`: Data Flow Task to load table `S1_DEFAULT_MISSION_CURRENCY`.
    *   `DFT- S_IMS_TCURR`: Data Flow Task to load table `S_IMS_TCURR`.
    *   `DFT-S_IMS_TCURR_MAX_RATIO_DATES`: Data Flow Task to load table `S_IMS_TCURR_MAX_RATIO_DATES`.
    *   `DFT-S1_EFR_BANK_RELATED_GL_ACCOUNTS`: Data Flow Task to load table `S1_EFR_BANK_RELATED_GL_ACCOUNTS`.
    *   `DFT-S1_EFR_PERIODS`: Data Flow Task to load table `S1_EFR_PERIODS`.
    *   `DFT-S1_IMS_ACCT_DOC_HEADER`: Data Flow Task to load table `S1_IMS_ACCT_DOC_HEADER`
    *   `DFT-S1_IMS_ACCT_DOC_SEGMENT`: Data Flow Task to load table `S1_IMS_ACCT_DOC_SEGMENT`.
    *   `DFT-S1_IMS_BUDGET_TOTALS`: Data Flow Task to load table `S1_IMS_BUDGET_TOTALS`.

*   **`SEQC-STAGING TABLES SPRINT 2`**:
    This sequence container truncates and loads several staging tables.

    *   `ESQLT- Truncate Staging Tables`: Executes SQL to truncate several staging tables.
    *   `DFT- S1_IMS_CHART_OF_COMMITMENT_ITEMS`: Data Flow Task to load table `S1_IMS_CHART_OF_COMMITMENT_ITEMS`.
    *   `DFT- S1_IMS_COST_ELEMENT_CATEGORIES`: Data Flow Task to load table `S1_IMS_COST_ELEMENT_CATEGORIES`.
    *   `DFT-S1_IMS_COMMITMENT_DOC_MGMT`: Data Flow Task to load table `S1_IMS_COMMITMENT_DOC_MGMT`.
    *   `DFT-S1_IMS_COST_TOTALS`: Data Flow Task to load table `S1_IMS_COST_TOTALS`.
    *   `DFT-S1_IMS_DOCUMENT_HEADER`: Data Flow Task to load table `S1_IMS_DOCUMENT_HEADER`.
    *   `DFT-S1_IMS_DOCUMENT_TYPE`: Data Flow Task to load table `S1_IMS_DOCUMENT_TYPE`.
    *   `DFT-S1_IMS_FUND`: Data Flow Task to load table `S1_IMS_FUND`.
    *   `DFT-S1_IMS_GL_MASTER`: Data Flow Task to load table `S1_IMS_GL_MASTER`.
    *   `DFT-S1_IMS_LINE_ITEMS`: Data Flow Task to load table `S1_IMS_LINE_ITEMS`.

*   The package also contains two other sequence container `SEQC-STAGING TABLES SPRINT 5` and `SEQC-STAGING TABLES SPRINT 6 - Zahra` with multiple `Data Flow Task` and one `Execute SQL Task` each. The data flow tasks are executed sequentially based on the precedence constraints. The precedence constraints are set as `Success`.

*   The package also contains a sequence container `SEQC-STAGING TABLES SPRINT 6 Xiuxin` with two `Data Flow Task` and no `Execute SQL Task`. The data flow tasks are executed sequentially based on the precedence constraints. The precedence constraints are set as `Success`.

#### DFT - S_IMS_M_RATES_DAILY

*   **Source:** `OLEDB_SRC - W2_IMS_DAILY_RATES_M`: Extracts data from the `W2_IMS_DAILY_RATES_M` table using a SQL query.
*   **Transformation:** `DRV - ETL Dates & Flag`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` columns with the current date and time, and END_OF_MONTH_FLAG.
*   **Destination:** `OLEDB_DEST - S_IMS_M_RATES_DAILY`: Loads data into the `S_IMS_M_RATES_DAILY` table.

#### DFT-S1_IMS_ECONOMIC_OBJECTS

*   **Source:** `OLEDB_SRC-R_FIN_ECONOMIC_OBJECTS`
*   **Transformations:** `DRV-S1_IMS_ECONOMIC_OBJECTS`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_ECONOMIC_OBJECTS`

#### DFT-S1_IMS_FISCAL_PERIOD_INFO

*   **Source:** `OLEDB_SRC-DATE_DIM`
*   **Transformations:** `DRV-S1_IMS_FISCAL_PERIOD_INFO`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FISCAL_PERIOD_INFO`

#### DFT-S1_IMS_FISCAL_YEAR_INFO

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV-S1_IMS_FISCAL_YEAR_INFO`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FISCAL_YEAR_INFO`

#### DFT-S1_IMS_FUNDS_MGMT_BUDGET_HEADER

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_IMS_FUNDS_MGMT_BUDGET_LINES

*   **Source:** `OLEDB_SRC-FMBL`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_LINES`

#### DFT-S1_IMS_VALUE_TYPE

*   **Source:** `OLEDB_SRC-DD07T`
*   **Transformations:** `DRV-S1_IMS_VALUE_TYPE`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_VALUE_TYPE`

#### DFT-S1_IMS_VENDOR_MASTER

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_VENDOR_MASTER`

#### DFT-S1_IMS_WBS_ELEMENT_MASTER

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_WBS_ELEMENT_MASTER`

#### DFT-S1_IMS_WBS_HIER_POINTER

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_WBS_HIER_POINTER`

#### DFT-S2_IMS_WBS_ELEMENT_MASTER

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_WBS_HIER_POINTER`

#### DFT-S1_IMS_SET_LEAF

*   **Source:** `OLEDB_SRC-SETLEAF`
*   **Transformations:** `DRV-S1_IMS_SET_LEAF`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_SET_LEAF`

#### DFT-W1_FIN_ACTUALS

*   **Source:** `OLEDB_SRC-S1_IMS_LINE_ITEMS`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_VENDOR_MASTER

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_COMMITMENT_MASTER

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_IMS_PURCHASE_AQ_ACCT_ASGNM

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_IMS_PURCHASING_DOC_ITEM

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_IMS_MANUAL_DOC_ITEMS

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_IMS_DELIVERY_DATE

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_COMMODITY_TYPE

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_LIMITED_TENDERING

*   **Source:** `OLEDB_SRC-FMBH`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_PLANT

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_PURCHASING_ORG

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_PURCHASING_GROUP

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_MATERIAL_GROUP

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_AGREEMENT_TYPE

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_SOLICITATION_PROCEDURE

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_METHOD_OF_SUPPLY

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_PROCUREMENT

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_CONTRACT_DIVISION

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-S1_MM_INTELLECTUAL_PROPERTY

*   **Source:** `OLEDB_SRC-FMIFIIT`
*   **Transformations:** `DRV- START_END_DATES`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT`.
*   **Destination:** `OLEDB_DEST-S1_IMS_FUNDS_MGMT_BUDGET_HEADER`

#### DFT-W_IMS_DAILY_RATES_M

*   The `OLEDB_SRC - S_IMS_TCURR` and `OLEDB_SRC - S_IMS_TCURR_MAX_RATIO_DATES` are joined using `MGJN - RCURR_ID`. The output is sorted using `SRT - Multiple` and joined again with `OLEDB_SRC - S_IMS_TCURF` using `MGJN - Multiple`. The output is passed to `Conditional Split` activity and then to `DRV - ETL Dates` and finally to `OLEDB_DEST - W_IMS_DAILY_RATES_M`.

#### DFT-W1_MM_PROCUREMENT

*   **Source:** `OLEDB_SRC-S1_MM_PROCUREMENT`
*   **Lookup:** `LKP_TRFM-W1_MM_PROCUREMENT`
*   **Transformations:** `DCONV_TRFM-W1_MM_PROCUREMENT`: Contains data coversion transformation. Also, `DRV-W1_MM_PROCUREMENT`: Contains derived column transformation.
*   **Destination:** `OLEDB_DEST-W1_MM_PROCUREMENT`

#### DFT-W1_MM_PROCUREMENT_TOTALS

*   **Source:** `OLEDB_SRC-W2_MM_PROCUREMENT`
*   **Transformations:** `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
*   **Destination:** `OLEDB_DEST-W1_MM_PROCUREMENT_TOTALS`

#### DFT-W2_MM_PROCUREMENT

*   **Source:** `OLEDB_SRC-W1_MM-PROCUREMENT`
*   **Transformations:** `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT`, rounds `CONTRACT_VALUE` to two decimal places.
*   **Destination:** `OLEDB_DEST-W2_MM_PROCUREMENT`

#### DFT - W1_FIN_COMMITMENTS

*   **Source:** `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - 51`, `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - NOT 51`
*   **Transformations:** `DCONV_TRFM-TimeEntry`, `DRV - ETL Dates and Converted Amount`, `LKP - S_IMS_M_RATES_MONTHLY`
*   **Destination:** `OLEDB_DEST - W1_FIN_COMMITMENTS`

#### DFT - W1_FIN_FIFM_COMMITMENT_ITEM

*   **Source:** `OLEDB_SRC - S1_IMS_COMMITMENT_ITEMS`
*   **Transformations:** `DRV - ETL Dates`
*   **Destination:** `OLEDB_DEST - W1_FIN_FIFM_COMMITMENT_ITEM`

#### DFT - W1_FIN_ORDER_NUMBERS

*   **Source:** `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - 51`, `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - NOT 51`
*   **Transformations:** `DRV - ETL Dates`
*   **Destination:** `OLEDB_DEST - W1_FIN_ORDER_NUMBERS`

#### DFT - W1_FIN_ORDER_TYPE

*   **Source:** `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - 51`, `OLEDB_SRC - S1_IMS_COMMITMENT_DOC_MGMT - NOT 51`
*   **Transformations:** `DRV - ETL Dates`
*   **Destination:** `OLEDB_DEST - W1_FIN_ORDER_TYPE`

#### DFT-W1_MM_CORRECTIONS

*   **Source:** `OLEDB_SRC-S1_MM_CORRECTIONS`
*   **Transformations:** `DRV-W1_MM_PROCUREMENT`
*   **Destination:** `OLEDB_DEST-W1_MM_CORRECTIONS`

#### DFT-W2_MM_AMENDMENTS

*   **Source:** `OLEDB_SRC-W1_MM_AMENDMENTS 1`
*   **Transformations:** `DRV-START_END_DATES`
*   **Destination:** `OLEDB_DEST-W2_MM_AMENDMENTS`

#### DFT-S1_MM_ADJUSTMENT_OVERIDES

*   Source: `OLEDB_SRC-R_IMS_ADJUSTMENT_OVERIDES`
*   Destination: `OLEDB_DEST-S1_MM_ADJUSTMENT-OVERIDES`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S1_MM_AMMENDMENT

*   Source: `OLEDB_SRC-ZZPRPDAT`
*   Destination: `OLEDB_DEST-S1_MM_AMMENDMENT`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S1_MM_AMMENDMENT_CONTRACT_VALUES

*   Source: `OLEDB_SRC-ZZPRPDAT`
*   Destination: `OLEDB_DEST-S1_MM_AMMENDMENT_CONTRACT_VALUES`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S1_MM_CORRECTIONS

*   Source: `OLEDB_SRC-ZZPRPDAT`
*   Destination: `OLEDB_DEST-S1_MM_CORRECTIONS`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S1_MM_PROCUREMENT_LINE_NUMBERS

*   Source: `OLEDB_SRC-W2_MM_PROCUREMENT`
*   Destination: `OLEDB_DEST-S1_MM_PROCUREMENT_LINE_NUMBERS`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S2_MM_AMMENDMENT

*   Source: `OLEDB_SRC-ZZPRPDAT`
*   Destination: `OLEDB_DEST-S2_MM_AMMENDMENT`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S2_MM_PROCUREMENT_LINE_NUMBERS

*   Source: `OLEDB_SRC-S1_MM_PROCUREMENT_LINE_NUMBERS`
*   Destination: `OLEDB_DEST-S2_MM_PROCUREMENT_LINE_NUMBERS`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S3_MM_AMENDMENTS

*   Source: `OLEDB_SRC-S1_MM_AMMENDMENT`
*   Destination: `OLEDB_DEST-S3_MM_AMENDMENTS`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S4_MM_AMENDMENTS

*   Source: `OLEDB_SRC-S3_MM_AMENDMENTS`
*   Destination: `OLEDB_DEST-S4_MM_AMENDMENTS`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

#### DFT-S_IMS_M_RATES_MONTHLY

*   Source: `OLEDB_SRC-S_IMS_M_RATES_DAILY`
*   Destination: `OLEDB_DEST-S_IMS_M_RATES_MONTHLY`
*   Transformations: `DRV-START_END_DATES`: Creates new columns `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.

### Error Handling

*   The Data Flow Tasks primarily use `FailComponent` for error row disposition. This means that if an error occurs during data conversion or loading, the entire Data Flow Task will fail.
*   OLE DB Destinations contains error outputs
*   Error handling is limited to failing the component on error. More sophisticated logging may be implemented elsewhere (e.g., event handlers).

## 4. Code Extraction

### SQL Queries

#### OLEDB_SRC - W2_IMS_DAILY_RATES_M (Source for DFT - S_IMS_M_RATES_DAILY):

```sql
SELECT
IMS_RATE_DATE,
       MANDT,
       LAST_DAY_OF_MONTH,
	   CAST
	   (
		(CASE 
	    WHEN IMS_RATE_DATE  =  CAST(CAST (LAST_DAY_OF_MONTH AS DATE) AS CHAR(31)) THEN 'Y'
		WHEN IMS_RATE_DATE  = CAST(CAST (getdate() AS DATE) AS CHAR(31)) THEN 'Y' 
	    ELSE 'N'
        END)
		AS VARCHAR(1)) AS END_OF_MONTH_FLAG,
       FISCAL_MONTH,
       FISCAL_YEAR,
       M_RATE,
       CURRENCY_CD,
       RATIO
FROM
(
SELECT IMS_RATE_DATE,
       MANDT,
       LAST_DAY_OF_MONTH,
       FISCAL_MONTH,
       FISCAL_YEAR,
       M_RATE,
       FCURR AS CURRENCY_CD,
       RATIO
FROM    dbo.W2_IMS_DAILY_RATES_M
WHERE IMS_RATE_DATE IS NOT NULL
UNION
SELECT distinct IMS_RATE_DATE as IMS_RATE_DATE,
   MANDT,
   LAST_DAY_OF_MONTH,
   FISCAL_MONTH,
   FISCAL_YEAR,
   1 as M_RATE,
   'CAD' as CURRENCY_CD,
   1 as RATIO
FROM   dbo.W2_IMS_DAILY_RATES_M
WHERE IMS_RATE_DATE IS NOT NULL
) TB1
--WHERE IMS_RATE_DATE='2007-01-31'
```

#### User::V_SQL_INSERT_ON_PRE_EXECUTE Variable:

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
  WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'   -- 'STRATEGIA_MASTER.DTSX'
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
  )
 ,(
  SELECT ETL_SUB_COMPONENT_ID
  FROM ETL_SUB_COMPONENT
  WHERE ETL_COMPONENT_ID IN (
    SELECT ETL_COMPONENT_ID
    FROM ETL_COMPONENT
    WHERE ETL_COMPONENT_NM = 'IMS_MASTER.DTSX'
     AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/IMS' 
    )
   AND ETL_SUB_COMPONENT_NM = 'IMS_STAGING.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )
 ,'RUNNING'
 ,0
 ,GETDATE()
 ,GETDATE()
 )

;
```

#### User::V_SQL_UPDATE_ON_ERROR Variable:

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
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ET