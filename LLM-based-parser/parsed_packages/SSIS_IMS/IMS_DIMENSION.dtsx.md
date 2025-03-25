## 1. Input Connection Analysis

| Connection Manager Name | Connection Type | Connection String Details | Purpose within Package | Security Requirements | Parameters/Variables | Source Part |
|---|---|---|---|---|---|---|
| IMS_SSIS_DFAIT_REPORTING | OLE DB | Server: [Inferred], Database: [Inferred] | Destination for dimension data | SQL Server Auth likely | None | Part 1, 2, 3 |
| IMS_SSIS_DFAIT_STAGING | OLE DB | Server: [Inferred], Database: [Inferred] | Source for dimension data | SQL Server Auth likely | None | Part 1, 2, 3 |
| MART_COM | OLE DB | Server: [Inferred], Database: [Inferred] | Source for dimension data | SQL Server Auth likely | None | Part 1, 2, 3 |

## 2. Package Dependencies

| Dependent Package Name | Package Full Path | Parent-Child Relationship | Execution Conditions/Constraints | Notes | Source Part |
|---|---|---|---|---|---|
| None Found |  |  |  | No dependent SSIS packages tasks found | Part 1, 2, 3 |

## 3. Package Flow Analysis

The package "IMS_DIMENSION" appears to load various dimension tables in a data warehouse related to financial data, materials management, and other entities.

*   The package starts with an Expression Task named "Dimensions - Start Task" which evaluates the expression `1 == 1`, effectively doing nothing but acting as the starting point.
*   The bulk of the package consists of several `Sequence Container`s, each responsible for loading a specific dimension table. Each sequence container truncate table, insert unknown member and load dimension table

#### SEQC - D_FIN_DOCUMENT_TYPE

*   **Tasks:**
    *   `ESQLT-Truncate D_FIN_DOCUMENT_TYPE`: Truncates the `dbo.D_FIN_DOCUMENT_TYPE` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_DOCUMENT_TYPE`.
    *   `DFT - D_FIN_DOCUMENT_TYPE`: Loads data into the `dbo.D_FIN_DOCUMENT_TYPE` 

*   **`DFT - D_FIN_DOCUMENT_TYPE` Data Flow Analysis:**
    *   **Source:**  `OLEDB_SRC - S1_IMS_DOCUMENT_TYPE` extracts data from `dbo.S1_IMS_DOCUMENT_TYPE`.
    *   **Transformations:** `DRV - ETL Dates` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST - D_FIN_DOCUMENT_TYPE` loads data into `dbo.D_FIN_DOCUMENT_TYPE`.

#### SEQC - D_FIN_ECON_OBJECT

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_FIN_ECON_OBJECT` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_ECON_OBJECT`.
    *   `DFT - D_FIN_ECON_OBJECT`: Loads data into the `dbo.D_FIN_ECON_OBJECT` table.

*   **`DFT - D_FIN_ECON_OBJECT` Data Flow Analysis:**
    *   **Sources:** `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV1`,  `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV2`, `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV3`,`OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV4` extracts data from staging tables.
    *   **Transformations:**
        *   `SRT - LEVEL1_ID`, `SRT - LEVEL2_ID`: Sort transformations.
        *   `MGJN - LEVEL3_ID`, `MGJN - LEVEL2_ID`, `MGJN - LEVEL1_ID`: Merge Join transformations to join data from different level tables.
        *   `DRV - ETL DATES & LONG DESC`: Derived Column transformation to add ETL dates and derive long text descriptions.
    *   **Destination:** `OLEDB_DEST - D_FIN_ECON_OBJECT` loads data into `dbo.D_FIN_ECON_OBJECT`.

#### SEQC - D_FIN_GL

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_FIN_GL` table.
    *   `DFT - D_FIN_GL`: Loads data into the `dbo.D_FIN_GL` table.

*   **`DFT - D_FIN_GL` Data Flow Analysis:**
    *   **Sources:** `OLEDB_SRC - W1_FIN_GL` extracts data from `dbo.W1_FIN_GL` and `OLEDB_SRC - S1_EFR_BANK_RELATED_GL_ACCOUNTS - BANK` extracts data from `S1_EFR_BANK_RELATED_GL_ACCOUNTS`.
    *   **Transformations:**
        *   `SRT - MISSION_NAME_EN`: Sorts data by MISSION_NAME_EN.
        *   `MGJN - GL_ACCOUNT_INTERNAL`: Merge Join to combine `W1_FIN_GL` and `S1_EFR_BANK_RELATED_GL_ACCOUNTS`.
        *   `MGJN - MISSION_NAME_EN`: Merge Join to enrich data with mission name information.
        *   `DRV - ETL DATES`: Derived Column transformation to add ETL dates.
    *   **Destination:** `OLEDB_DEST - D_FIN_GL` loads data into `dbo.D_FIN_GL`.

#### SEQC - D_FIN_WBS_ELEMENT

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_FIN_WBS_ELEMENT` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_WBS_ELEMENT`.
    *   `DFT - D_FIN_WBS_ELEMENT`: Loads data into the `dbo.D_FIN_WBS_ELEMENT` table.

*   **`DFT - D_FIN_WBS_ELEMENT` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC - W2_FIN_WBS_ELEMENT` extracts data from `dbo.W2_FIN_WBS_ELEMENT`.
    *   **Transformations:** `DRV - ELT DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST - D_FIN_WBS_ELEMENT` loads data into `dbo.D_FIN_WBS_ELEMENT`.

#### SEQC - D_MM_AGREEMENT_TYPE (Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_AGREEMENT_TYPE` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_AGREEMENT_TYPE`.
    *   `DFT - D_MM_AGREEMENT_TYPE`: Loads data into the `dbo.D_MM_AGREEMENT_TYPE` table.

*   **`DFT - D_MM_AGREEMENT_TYPE` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_AGREEMENT_TYPE` extracts data from `dbo.S1_MM_AGREEMENT_TYPE`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_AGREEMENT_TYPE` loads data into `dbo.D_MM_AGREEMENT_TYPE`.

#### SEQC - D_MM_COMMODITY_TYPE (Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_COMMODITY_TYPE` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_COMMODITY_TYPE`.
    *   `DFT - D_MM_COMMODITY_TYPE`: Loads data into the `dbo.D_MM_COMMODITY_TYPE` table.

*   **`DFT - D_MM_COMMODITY_TYPE` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC-S_IMS_M_RATES_DAILY` extracts data from `dbo.S1_MM_COMMODITY_TYPE`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_COMMODITY_TYPE` loads data into `dbo.D_MM_COMMODITY_TYPE`.

#### SEQC - D_MM_INTELLECTUAL_PROPERTY (Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_INTELLECTUAL_PROPERTY` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_INTELLECTUAL_PROPERTY`.
    *   `DFT - D_MM_INTELLECTUAL_PROPERTY`: Loads data into the `dbo.D_MM_INTELLECTUAL_PROPERTY` table.

*   **`DFT - D_MM_INTELLECTUAL_PROPERTY` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_INTELLECTUAL_PROPERTY` extracts data from `dbo.S1_MM_INTELLECTUAL_PROPERTY`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_INTELLECTUAL_PROPERTY` loads data into `dbo.D_MM_INTELLECTUAL_PROPERTY`.

#### SEQC - D_MM_LIMITED_TENDERING (Sprint 7 - Zahra)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_LIMITED_TENDERING` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_LIMITED_TENDERING`.
    *   `DFT - D_MM_LIMITED_TENDERING`: Loads data into the `dbo.D_MM_LIMITED_TENDERING` table.

*   **`DFT - D_MM_LIMITED_TENDERING` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_LIMITED_TENDERING` extracts data from `dbo.S1_MM_LIMITED_TENDERING`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_LIMITED_TENDERING` loads data into `dbo.D_MM_LIMITED_TENDERING`.

#### SEQC - D_MM_PLANT (Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_PLANT` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_PLANT`.
    *   `DFT - D_MM_PLANT`: Loads data into the `dbo.D_MM_PLANT` table.

*   **`DFT - D_MM_PLANT` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_PLANT` extracts data from `dbo.S1_MM_PLANT`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_PLANT` loads data into `dbo.D_MM_PLANT`.

#### SEQC - D_MM_PURCHASING_GROUP (Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_PURCHASING_GROUP` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_PURCHASING_GROUP`.
    *   `DFT - D_MM_PURCHASING_GROUP`: Loads data into the `dbo.D_MM_PURCHASING_GROUP` table.

*   **`DFT - D_MM_PURCHASING_GROUP` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_PURCHASING_GROUP` extracts data from `dbo.S1_MM_PURCHASING_GROUP`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_PURCHASING_GROUP` loads data into `dbo.D_MM_PURCHASING_GROUP`.

#### SEQC - D_MM_SOLICITATION_PROCEDURE(Sprint 7)

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.D_MM_SOLICITATION_PROCEDURE` table.
    *   `ESQL-Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_MM_SOLICITATION_PROCEDURE`.
    *   `DFT - D_MM_SOLICITATION_PROCEDURE`: Loads data into the `dbo.D_MM_SOLICITATION_PROCEDURE` table.

*   **`DFT - D_MM_SOLICITATION_PROCEDURE` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- S1_MM_SOLICITATION_PROCEDURE` extracts data from `dbo.S1_MM_SOLICITATION_PROCEDURE`.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-D_MM_SOLICITATION_PROCEDURE` loads data into `dbo.D_MM_SOLICITATION_PROCEDURE`.

#### SEQC - R_FIN_PO_ADD_DATA (Sprint 8) - Zahra

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.R_FIN_PO_ADD_DATA` table.
    *   `DFT-R_FIN_PO_ADD_DATA`: Loads data into the `dbo.R_FIN_PO_ADD_DATA` table.

*   **`DFT-R_FIN_PO_ADD_DATA` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC- R_IMS_FIN_PO_ADD_DATA` extracts data from `dbo.R_IMS_FIN_PO_ADD_DATA` using the `BI_CONFORMED` connection.
    *   **Transformations:** `DRV-START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-R_FIN_PO_ADD_DATA` loads data into `dbo.R_FIN_PO_ADD_DATA`.

#### SEQC-D_FIN_CE_GROUP

*   **Tasks:**
    *   `ESQLT- Truncate Staging Tables`: Truncates the `dbo.D_FIN_CE_GROUP` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_CE_GROUP`.
    *   `DFT-D_FIN_CE_GROUP`: Loads data into the `dbo.D_FIN_CE_GROUP` table.

*   **`DFT-D_FIN_CE_GROUP` Data Flow Analysis:**
    *   **Source:** OLEDB_SRC-S1_IMS_COST_ELEMENT_TEXT extracts data from `dbo.S1_IMS_COST_ELEMENT_TEXT`
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_CE_GROUP` loads data into `dbo.D_FIN_CE_GROUP`.

#### SEQC-D_FIN_COMMITMENT

*   **Tasks:**
    *   `ESQLT- Truncate DIM Tables`: Truncates the `dbo.D_FIN_COMMITMENT` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_COMMITMENT`.
    *   `DFT-D_FIN_COMMITMENT`: Loads data into the `dbo.D_FIN_COMMITMENT` table.

*   **`DFT-D_FIN_COMMITMENT` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC-D_FIN_COMMITMENT` extracts data from `dbo.S1_IMS_CHART_OF_COMMITMENT_ITEMS`.
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_COMMITMENT` loads data into `dbo.D_FIN_COMMITMENT`.

#### SEQC-D_FIN_FISCAL_DATE

*   **Tasks:**
    *   `ESQLT- Truncate DIM Tables`: Truncates the `dbo.D_FIN_FISCAL_DATE` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_FISCAL_DATE`.
    *   `DFT-D_FIN_FISCAL_DATE`: Loads data into the `dbo.D_FIN_FISCAL_DATE` table.

*   **`DFT-D_FIN_FISCAL_DATE` Data Flow Analysis:**
    *   **Source:** `OLEDB_SRC-D_FIN_FISCAL_DATE` extracts data from `dbo.D_COM_DATE`.
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_FISCAL_DATE` loads data into `dbo.D_FIN_FISCAL_DATE`.

#### SEQC-D_FIN_FUND

*   **Tasks:**
    *   `ESQLT- Truncate Staging Tables`: Truncates the `dbo.D_FIN_FUND` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_FUND`.
    *   `DFT-D_FIN_FUND`: Loads data into the `dbo.D_FIN_FUND` table.

*   **`DFT-D_FIN_FUND` Data Flow Analysis:**
    *   **Source:**  `OLEDB_SRC-D_FIN_FUND` extracts data from `dbo.S1_IMS_FUND`.
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_FUND` loads data into `dbo.D_FIN_FUND`.

#### SEQC-D_FIN_OTHER

*   **Tasks:**
    *   `ESQLT- Truncate Staging Tables`: Truncates the `dbo.D_FIN_OTHER` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_OTHER`.
    *   `DFT-D_FIN_OTHER`: Loads data into the `dbo.D_FIN_OTHER` table.

*   **`DFT-D_FIN_OTHER` Data Flow Analysis:**
    *   **Source:**  `OLEDB_SRC-D_FIN_OTHER` extracts data from a complex SQL query combining various tables.
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_OTHER` loads data into `dbo.D_FIN_OTHER`.

#### SEQC-D_FIN_USER

*   **Tasks:**
    *   `ESQLT- Truncate Staging Tables`: Truncates the `dbo.D_FIN_USER` table.
    *   `ESQLT- Insert Unknown Members`: Inserts a default/unknown member into `dbo.D_FIN_USER`.
    *   `DFT-D_FIN_USER`: Loads data into the `dbo.D_FIN_USER` table.

*   **`DFT-D_FIN_USER` Data Flow Analysis:**
    *   **Source:**  `OLEDB_SRC-D_FIN_USER` extracts data using a UNION ALL query.
    *   **Transformations:** `DRV- START_END_DATES` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_TRG-D_FIN_USER` loads data into `dbo.D_FIN_USER`.

#### SEQC-GROUP1

*   **Tasks:**
    *   `ESQLT- Truncate Staging Tables`: Truncates the `dbo.R_IMS_M_RATES_DAILY` table.
    *   `DFT - R_IMS_M_RATES_DAILY`: Loads data into the `dbo.R_IMS_M_RATES_DAILY` table.

*   **`DFT - R_IMS_M_RATES_DAILY` Data Flow Analysis:**
    *   **Source:**  `OLEDB_SRC - W2_IMS_DAILY_RATES_M` extracts data with a SQL query.
    *   **Transformations:** `DRV - ETL Dates & Flag` adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST - R_IMS_M_RATES_DAILY` loads data into `dbo.R_IMS_M_RATES_DAILY`.

#### SEQC-SPRINT 8 - Venkata

*   **Tasks:**
    *   `ESQLT- Truncate Dimension Tables`: Truncates the `dbo.R_FIN_IO_FUND_CENTRE`, `dbo.R_IMS_M_RATES_MONTHLY`, and `dbo.R_FIN_EXPENDITURE_ADJUSTMENTS` tables.
    *   `DFT-R_FIN_IO_FUND_CENTRE`: Loads data into the `dbo.R_FIN_IO_FUND_CENTRE` table.
    *   `DFT-R_IMS_M_RATES_MONTHLY`: Loads data into the `dbo.R_IMS_M_RATES_MONTHLY` table.
    *   `DFT-R_FIN_EXPENDITURE_ADJUSTMENTS`: Loads data into the `dbo.R_FIN_EXPENDITURE_ADJUSTMENTS` table.

*   **`DFT-R_FIN_IO_FUND_CENTRE` Data Flow Analysis:**
    *   **Sources:** `OLEDB_SRC-D_COMMON_FUND_CENTRE` extracts data from staging tables.
    *   **Transformations:**
        *   `Merge Join` to combine data.
        *   `DRV - ETL Dates & Flag`: Derived Column transformation to add ETL dates.
    *   **Destination:** `OLEDB_DEST - R_FIN_IO_FUND_CENTRE` loads data into `dbo.R_FIN_IO_FUND_CENTRE`.
*   **`DFT-R_IMS_M_RATES_MONTHLY` Data Flow Analysis:**
    *   **Sources:** `OLEDB_SRC-S_IMS_M_RATES_DAILY` extracts data from staging tables.
    *   **Transformations:**
        *   `DRV - ETL Dates & Flag`: Derived Column transformation to add ETL dates.
    *   **Destination:** `OLEDB_DEST - R_IMS_M_RATES_MONTHLY` loads data into `dbo.R_IMS_M_RATES_MONTHLY`.
*   **`DFT-R_FIN_EXPENDITURE_ADJUSTMENTS` Data Flow Analysis:**
    *   **Sources:** `OLEDB_SRC-S1_IMS_ACCT_DOC_SEGMENT` extracts data from staging tables.
    *   **Transformations:**
        *   `LKP-FUND_CENTRE_CD`: Lookup  transformation.
        *   `DRV - ETL Dates & Flag`: Derived Column transformation to add ETL dates.
    *   **Destination:** `OLEDB_DEST - R_FIN_EXPENDITURE_ADJUSTMENTS` loads data into `dbo.R_FIN_EXPENDITURE_ADJUSTMENTS`.

## 4. Code Extraction

### SQL queries:

Context: The following SQL query is used in the OLE DB Source `OLEDB_SRC - S1_IMS_DOCUMENT_TYPE` to extract data from the `S1_IMS_DOCUMENT_TYPE` table.

```sql
SELECT distinct DOCUMENT_TYPE,
	MAX(DOCUMENT_TYPE_DESCR_EN) as DOCUMENT_TYPE_DESCR_EN,
	MAX(DOCUMENT_TYPE_DESCR_FR) as DOCUMENT_TYPE_DESCR_FR
FROM   dbo.S1_IMS_DOCUMENT_TYPE
WHERE (LEN(DOCUMENT_TYPE) > 1)
GROUP BY DOCUMENT_TYPE
ORDER BY 1
```

Context: The following SQL query is used in the OLE DB Source `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV1`:

```sql
SELECT  distinct   ECON_OBJ_ID as LEVEL1_ID, ECON_OBJ_CODE as LEVEL1_CD, ISNULL
                          ((SELECT     MAX(ECON_OBJ_ID)
                              FROM         dbo.S1_IMS_ECONOMIC_OBJECTS A
                              WHERE     x.ECON_OBJ_ID > ECON_OBJ_ID AND LEN(x.ECON_OBJ_CODE) > len(ECON_OBJ_CODE)), 11111)
                      AS PARENT_ID, ECON_OBJ_TXT_EN as LEVEL1_TXT_EN, ECON_OBJ_TXT_FR as LEVEL1_TXT_FR
FROM         dbo.S1_IMS_ECONOMIC_OBJECTS x

where LEN(ECON_OBJ_CODE) = 1
ORDER BY ECON_OBJ_ID
```

Context: The following SQL query is used in the OLE DB Source `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV2`:

```sql
SELECT  distinct   ECON_OBJ_ID as LEVEL2_ID, ECON_OBJ_CODE as LEVEL2_CD, ISNULL
                          ((SELECT     MAX(ECON_OBJ_ID)
                              FROM         dbo.S1_IMS_ECONOMIC_OBJECTS A
                              WHERE     x.ECON_OBJ_ID > ECON_OBJ_ID AND LEN(x.ECON_OBJ_CODE) > len(ECON_OBJ_CODE)), 11111)
                      AS LEVEL1_ID, ECON_OBJ_TXT_EN as LEVEL2_TXT_EN, ECON_OBJ_TXT_FR as LEVEL2_TXT_FR
FROM         dbo.S1_IMS_ECONOMIC_OBJECTS x

where LEN(ECON_OBJ_CODE) = 2
ORDER BY ECON_OBJ_ID
```

Context: The following SQL query is used in the OLE DB Source `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV3`:

```sql
SELECT  distinct   ECON_OBJ_ID as LEVEL3_ID, ECON_OBJ_CODE as LEVEL3_CD, ISNULL
                          ((SELECT     MAX(ECON_OBJ_ID)
                              FROM         dbo.S1_IMS_ECONOMIC_OBJECTS A
                              WHERE     x.ECON_OBJ_ID > ECON_OBJ_ID AND LEN(x.ECON_OBJ_CODE) > len(ECON_OBJ_CODE)), 11111)
                      AS LEVEL2_ID, ECON_OBJ_TXT_EN as LEVEL3_TXT_EN, ECON_OBJ_TXT_FR as LEVEL3_TXT_FR
FROM         dbo.S1_IMS_ECONOMIC_OBJECTS x

where LEN(ECON_OBJ_CODE) = 3
ORDER BY ECON_OBJ_ID
```

Context: The following SQL query is used in the OLE DB Source `OLEDB_SRC - S1_IMS_ECONOMIC_OBJECTS & S1_IMS_GL_MASTER - LEV4`:

```sql
SELECT  distinct   ECON_OBJ_ID as LEVEL4_ID, ECON_OBJ_CODE as LEVEL4_CD, ISNULL
                          ((SELECT     MAX(ECON_OBJ_ID)
                              FROM         dbo.S1_IMS_ECONOMIC_OBJECTS A
                              WHERE     x.ECON_OBJ_ID > ECON_OBJ_ID AND LEN(x.ECON_OBJ_CODE) > len(ECON_OBJ_CODE)), 11111)
                      AS LEVEL3_ID, ECON_OBJ_TXT_EN as LEVEL4_TXT_EN, ECON_OBJ_TXT_FR as LEVEL4_TXT_FR,
          GL_ACCOUNT_ID as ECON_OBJ_BKID
FROM         dbo.S1_IMS_ECONOMIC_OBJECTS x

INNER JOIN dbo.S1_IMS_GL_MASTER y ON CAST(x.ECON_OBJ_CODE AS INT) = CAST(y.GL_ACCOUNT_ALT_NBR AS INT)

where LEN(ECON_OBJ_CODE) = 4
AND ISNUMERIC(ECON_OBJ_CODE) = 1
```

Context: The following SQL query is used in the Execute SQL Task `ESQL-Insert Unknown Members` inside the Sequence Container `SEQC - D_FIN_ECON_OBJECT`:

```sql
/**************************D_FIN_ECON_OBJECT*************************/

DBCC CHECKIDENT ('dbo.D_FIN_ECON_OBJECT', RESEED, 0)

SET IDENTITY_INSERT dbo.D_FIN_ECON_OBJECT ON

INSERT INTO [dbo].[D_FIN_ECON_OBJECT]
           (ECON_OBJ_SID
 ,[ECON_OBJ_BKID]
      ,[LEVEL1_CD]
      ,[LEVEL1_TXT_EN]
      ,[LEVEL1_TXT_FR]
      ,[LEVEL1_LONG_TXT_EN]
      ,[LEVEL1_LONG_TXT_FR]
      ,[LEVEL2_CD]
      ,[LEVEL2_TXT_EN]
      ,[LEVEL2_TXT_FR]
      ,[LEVEL2_LONG_TXT_EN]
      ,[LEVEL2_LONG_TXT_FR]
      ,[LEVEL3_CD]
      ,[LEVEL3_TXT_EN]
      ,[LEVEL3_TXT_FR]
      ,[LEVEL3_LONG_TXT_EN]
      ,[LEVEL3_LONG_TXT_FR]
      ,[LEVEL4_CD]
      ,[LEVEL4_TXT_EN]
      ,[LEVEL4_TXT_FR]
      ,[LEVEL4_LONG_TXT_EN]
      ,[LEVEL4_LONG_TXT_FR]
      ,[ETL_CREA_DT]
      ,[ETL_UPDT_DT]         
     )
     VALUES
  (
  -3,
'-',
'-',
'N/A',
'N/A',
NULL,
NULL,
'-',
'N/A',
'N/A',
NULL,
NULL,
'-',
'N/A',
'N/A',
NULL,
NULL,
'-',
'N/A',
'N/A',
NULL,
NULL,
GETDATE(),
GETDATE()
)

 SET IDENTITY_INSERT dbo.D_FIN_ECON_OBJECT OFF
```

Context: The following SQL query is used in the Execute SQL Task `ESQLT- Truncate Dimension Tables` inside the Sequence Container `SEQC - D_FIN_ECON_OBJECT`:

```sql
TRUNCATE TABLE DBO.D_FIN_ECON_OBJECT;
```

Context: The following SQL query is used in the OLE DB Source component `OLEDB_SRC - W1_FIN_GL`:

```sql
SELECT	GL_ACCOUNT_KEY,
	GL_TXT_SHORT_EN,
	GL_TXT_LONG_EN,
	GL_TXT_EN,
	GL_TXT_SHORT_FR,
	GL_TXT_LONG_FR,
	GL_TXT_FR,
	GL_ACCOUNT_CD,
	GL_GROUP_LEVEL1_EN,
	GL_GROUP_LEVEL1_FR,
	GL_GROUP_LEVEL2_EN,
	GL_GROUP_LEVEL2_FR,
        GL_ACCOUNT_INTERNAL,
        CASE WHEN (SELECT GL_ACCOUNT FROM S1_EFR_BANK_RELATED_GL_ACCOUNTS WHERE BLOCKED <> 'X' AND GL_ACCOUNT = CAST(a.GL_ACCOUNT_KEY as INT)) IS NOT NULL THEN 'Y' ELSE 'N' END as EFR_GL
FROM   dbo.W1_FIN_GL a

--where GL_ACCOUNT_KEY <> '-'
order by GL_ACCOUNT_INTERNAL
```

Context: The following SQL query is used in the OLE DB Source component `OLEDB_SRC - S1_EFR_BANK_RELATED_GL_ACCOUNTS - LEV1`

```sql
SELECT  distinct   ECON_OBJ_ID as LEVEL1_ID, ECON_OBJ_CODE as LEVEL1_CD, ISNULL
                          ((SELECT     MAX(ECON_OBJ_ID)
                              FROM         dbo.S1_IMS_ECONOMIC_OBJECTS A
                              WHERE     x.ECON_OBJ_ID > ECON_OBJ_ID AND LEN(x.ECON_OBJ_CODE) > len(ECON_OBJ_CODE)), 11111)
                      AS PARENT_ID, ECON_OBJ_TXT_EN as LEVEL1_TXT_EN, ECON_OBJ_TXT_FR as LEVEL1_TXT_FR
FROM         dbo.S1_IMS_ECONOMIC_OBJECTS x

where LEN(ECON_OBJ_CODE) = 1
ORDER BY ECON_