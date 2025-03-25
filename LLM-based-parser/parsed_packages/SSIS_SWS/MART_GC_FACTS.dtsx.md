```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details                                                                                                                                                                                                            | Purpose within Package                                                                                                                                                                                                                                                                                        | Security Requirements | Parameters/Variables                                                                                                                                                                                                                                                                         | Source Part |
|---------------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| MART_GC                   | OLE DB          | Server: [Inferred], Database: [Inferred]                                                                                                                                                                                             | Destination for fact tables `F_GC_INITIATIVE`, `F_GC_LOAN`, `F_GC_LOAN_GAC`, `F_GC_LOAN_NON_GAC`,  `F_GC_FINANCIAL_CFO_STATS`<br> Source for `D_LOAN` lookup within `DFT-F_GC_LOAN_GAC` and `DFT-F_GC_LOAN_NON_GAC`. <br>Used in Execute SQL Tasks to truncate the fact tables.                                                                                                                                     | SQL Server Auth likely | None                                                                                                                                                                                                                                                                                             | Part 1, 2, 3|
| DATA_HUB                  | OLE DB          | Server: [Inferred], Database: [Inferred]                                                                                                                                                                                             | Source for data from `SAP_OGD_EDC_LOAN`, `SAP_LOAN_PROFILE`, and  `SAP_CRS_OGD_LOAN_PROFILE` used in `DFT-F_GC_INITIATIVE` and `DFT-F_GC_LOAN_GAC` and `DFT-F_GC_LOAN_NON_GAC`.<br>Source for `SAP_RPT_GC_FINAN_CFO_STATS` to load `F_GC_FINANCIAL_CFO_STATS`.  Source for `SAP_LOAN_POLICY_MARKER` to load `F_GC_LOAN_POLICY_MARKER`.<br>Source for data flow `DFT-S_GC_PROJECT_WBS_BUDGET_TRANSACTION`   | SQL Server Auth likely | None                                                                                                                                                                                                                                                                                             | Part 1, 2, 3|
| ETL_STG_MART_GC | OLE DB | Server: [Inferred], Database: [Inferred] | Destination load staging table `S_PS_CFO_STATS_GC_FINAN`<br>Source for data flow `DFT-S_GC_PROJECT_WBS_BUDGET_TRANSACTION`   | SQL Server Auth likely | None | Part 1, 2, 3|

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints                                                                                                                                                                                                                                                                                                                             | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

*   The package starts with an `EXPRESSIONT_DMART` task that evaluates the expression `1 == 1`

*   It then proceeds to execute several sequence containers and data flow tasks in a specific order, as dictated by precedence constraints.

#### SEQC-F_LOAN_AND_INITITIVE

*   This Sequence Container truncates and loads data into `F_GC_LOAN` and `F_GC_INITIATIVE`.

*   It consists of the following:
    *   `ESQLT-Truncate_F_LOAN_AND_INITIATIVE`: Executes SQL to truncate the `F_GC_LOAN` and `F_GC_INITIATIVE` tables.
    *   `DFT-F_GC_LOAN_GAC`: Loads loan data from the `D_LOAN` and other SAP tables into `F_GC_LOAN`.
    *   `DFT-F_GC_LOAN_NON_GAC`: Loads loan data from the `D_LOAN` and other SAP tables into `F_GC_LOAN` for non-GAC loans.
    *   `DFT-F_GC_INITIATIVE`: Loads initiative data from `D_INITIATIVE` and other SAP tables into `F_GC_INITIATIVE`.

#### DFT-F_GC_LOAN_GAC

*   **Source:**  `OLEBD-src_D_LOAN` extracts data from `dbo.D_LOAN` joined with `DATA_HUB."dbo"."SAP_LOAN_PROFILE"` and `data_hub."dbo"."SAP_CRS_OGD_LOAN_PROFILE"`.
*   **Transformations:**
    *   `Data Conversion`: Converts string columns such as `ORIGINAL_AMT_DESCR` from str to wstr.
*   **Destinations:**
    *   `OLEDB_Dest_F_GC_LOAN_GAC` saves successfully mapped rows to `dbo.F_GC_LOAN`.

#### DFT-F_GC_LOAN_NON_GAC

*   **Source:**  `OLEDB-src_D_LOAN` extracts data from `dbo.D_LOAN` joined with `DATA_HUB."dbo"."SAP_LOAN_PROFILE"` and  `DATA_HUB.[dbo].[SAP_CRS_OGD_LOAN_PROFILE]`.
*   **Transformations:**
    *   `Data Conversion`: Converts string columns such as `ORIGINAL_AMT_DESCR` from str to wstr.
*   **Destinations:**
    *   `OLEDB-Dest_F_GC_LOAN_NON_GAC` saves successfully mapped rows to `dbo.F_GC_LOAN`.

#### DFT-F_GC_INITIATIVE

*   **Source:** `OLEDB-src_D_INITIATIVE` extracts data from `DBO.SAP_OGD_EDC_LOAN` and `MART_GC.DBO.D_INITIATIVE`
*   **Transformations:** None.
*   **Destinations:**
    *   `OLEDB-Dest_F_INITIATIVE` saves successfully mapped rows to `dbo.F_GC_INITIATIVE`.

#### SEQC_F_GC_FINANCIAL_CFO_STATS

*   This sequence container handles loading data into `F_GC_FINANCIAL_CFO_STATS`.

*   It consists of the following:
    *   `ESQLT-Truncate F_GC_FINANCIAL_CFO_STATS`: Executes SQL to truncate the `F_GC_FINANCIAL_CFO_STATS` table.
    *   `DFT-Save_Previous_Result_Snapshot`: Saves a snapshot of the previous data.
    *   `DFT-F_GC_FINANCIAL_CFO_STATS`: Loads data into the `F_GC_FINANCIAL_CFO_STATS` table.
    *   `ESQLT - UPD_INTL_COMMIT_AMT`: Updates `INTL_COMMIT_RPT_AMT` from `D_CFO_STATS_INTL_COMMIT` to `F_GC_FINANCIAL_CFO_STATS`.
    *   `ESQLT - UPD_FY_GC_FINAN_CFO_STATS_SID`:  Updates `FY_GC_FINAN_CFO_STATS_SID`.
    *   `ESQLT-UPDATE OGD VENDORS`: Updates vendor-related fields for OGD records.
    *   `ESQLT-UPDATE TRADING PARTNER NAMES`: Updates partner names from the `D_VENDOR` dimension.
    *   `CREATE_INDEX`: Creates a unique NONCLUSTERED index on `F_GC_FINANCIAL_CFO_STATS`.
    *   `ESQLT-Update_D_VENDOR`: update the `GC_IND` in the `D_VENDOR` table

#### DFT-F_GC_FINANCIAL_CFO_STATS

*   **Source:**  `OLEDB_SRC-SAP_RPT_GC_FINAN_CFO_STATS` extracts data from the SAP_RPT_GC_FINAN_CFO_STATS table.
*   **Transformations:**
    *   `LKP_TRFM_ D_COUNTRY`: Lookup transformation to retrieve country information.
    *   `LKP_TRFM_ D_FUND`: Lookup transformation to retrieve fund information.
    *   `LKP_TRFM_D_PROJECT_WBS`: Lookup transformation to retrieve project WBS information.
    *   `LKP_TRFM_D_FUND_CENTRE`: Lookup transformation to retrieve fund center information.
    *   `LKP_TRFM_SECTOR_LEVEL_3_SID`: Lookup transformation to retrieve sector level 3 information.
    *   `DRVCOL_TRFM - UNKNOWN MEMBERS`:  Derived Column transformation to handle unknown members.
*   **Destinations:**
    *   `OLEDB_DEST_F_GC_FINANCIAL_CFO_STATS` saves successfully mapped rows to `dbo.F_GC_FINANCIAL_CFO_STATS`.

#### DFT-Save_Previous_Result_Snapshot

*   **Source:**  `OLEDB_SRC_F_GC_FINANCIAL_CFO_STATS` extracts data from `[dbo].[F_GC_FINANCIAL_CFO_STATS]`.
*   **Transformations:** None.
*   **Destinations:**
    *   `OLE_DB_DEST_S_PS_CFO_STATS_GC_FINAN` saves the snapshot to `[dbo].[S_PS_CFO_STATS_GC_FINAN]`.

#### SEQC_F_WBS_IM_PROGRAM_ALLOCATION

*   This sequence container handles loading data into `F_WBS_IM_PROGRAM_ALLOCATION`.

*   It consists of the following:
    *   `ESQLT-Truncate F_WBS_IM_PROGRAM_ALLOCATION`: Executes SQL to truncate the `F_WBS_IM_PROGRAM_ALLOCATION` table.
    *   `DFT-F_WBS_IM_PROGRAM_ALLOCATION`: Loads data into the  `F_WBS_IM_PROGRAM_ALLOCATION` table.

#### DFT-F_WBS_IM_PROGRAM_ALLOCATION

*   **Source:**  `OLE DB SAP_LOAN_POLICY_MARKER` extracts data from `[dbo].[SAP_LOAN_POLICY_MARKER]`.
*   **Transformations:**
    *   `LKP_TRFM_D_PROJECT_WBS`: Lookup to get `PROJECT_WBS_SID`.
    *   `LKP_TRFM_ D_IM_PROGRAM_POSITION`: Lookup to get `IM_PROGRAM_POSITION_SID`.
    *   `DRVCOL_TRFM - UNKNOWN MEMBERS`: Derived column transformation to handle unknown members.

*   **Destinations:**
    *   `OLEDB_DEST_F_WBS_IM_PROGRAM_ALLOCATION` saves data to `[dbo].[F_WBS_IM_PROGRAM_ALLOCATION]`.

## 4. Code Extraction

```markdown
-- From OLEDB-src_D_INITIATIVE
SELECT	
 T2.INITIATIVE_SID,	
 ISNULL(T1.GEO_REGION_CD, '-3') AS DAC_REGION_CD,	
 T1.TIED_AID_AMT,	
 T1.UNTIED_AID_AMT,	
 T1.OUTSTANDING_AMT,	
 T1.FIRST_REPAYMENT_DT AS FIRST_PAYMENT_DT,	
 T1.FINAL_REPAYMENT_DT AS LAST_PAYMENT_DT,	
 T1.LOAN_START_DT AS START_DT,	
 T1.LOAN_END_DT AS END_DT,	
 T1.COMMITEMENT_AMT AS COMMITMENT_AMT,	
 T1.CAPITAL_EXPENDITURE_PER,	
 T1.COMMITMENT_DT,	
 T1.DISBURSEMENT_DT,	
 T1.INVESTMENT_RELATED_TECH_COOP_AMT,	
 T1.ARREARS_INTEREST_AMT,	
 T1.ARREARS_PRINCIPLE_AMT,	
 T1.DISBURESEMENT_AMT AS DISBURSEMENT_AMT,	
 T1.INTEREST_RATE_NBR AS INTEREST_RATE_AMT,	
 T1.INTEREST_RECEIVED_AMT,	
 T1.RECEIVED_AMT,	
 T1.SECOND_INTEREST_RATE_NBR AS SECOND_INTEREST_RATE_AMT,	
 CONVERT(DATE,GETDATE()) AS ROW_INSERT_DT,	
GETDATE() AS ETL_CREA_DT,	
GETDATE() AS ETL_UPDT_DT	
	
FROM DBO.SAP_OGD_EDC_LOAN T1 -- 2885	
	
JOIN MART_GC.DBO.D_INITIATIVE T2	
  ON T1.CRS_ID = T2.CRS_ID AND T1.CRS_ID_SUFFIX = T2.CRS_ID_SUFFIX AND T1.REPORTING_PERIOD = T2.REPORTING_PERIOD AND T1.OGD_YR = T2.YEAR	
	
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T3	
--	ON REPLICATE('0',5-LEN(T1.GEO_REGION_CD)) + T1.GEO_REGION_CD =  T3.DAC_GEOGRAPHIC_REGION_CD
--	AND T3.DAC_SID_IND = 1
```

SQL Query used to extract data from DBO.SAP_OGD_EDC_LOAN to load the F_GC_INITIATIVE table

```markdown
Select T1.LOAN_SID,		
       ISNULL(T2.GEO_REGION_CD, '-3') as DAC_REGION_CD,		
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,		
		
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],		
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],		
      crs.LOAN_START_DT as [LOAN_START_DT],		
      crs.LOAN_END_DT as [LOAN_END_DT],		
      crs.ORIGINAL_AMT_DESCR as [ORIGINAL_AMT_DESCR],		
      crs.BALANCE_AMT_DESCR as [BALANCE_AMT_DESCR],		
      crs.COVERING_PERIOD_DESCR as [COVERING_PERIOD_DESCR],		
      crs.PAYMENT_DUE_DT_DESCR as [PAYMENT_DUE_DT_DESCR],		
      crs.PRINCIPLE_BALANCE_AMT_DESCR as [PRINCIPLE_BALANCE_AMT_DESCR],		
      crs.INTEREST_BALANCE_AMT_DESCR as [INTEREST_BALANCE_AMT_DESCR],		
      T2.[INTEREST_RATE_NBR] as [INTEREST_RATE_NBR],		
      T2.[SECOND_INTEREST_RATE_NBR] as [SECOND_INTEREST_RATE_NBR],		
      NULL as [FIRST_PAYMENT_DT],		
      NULL as [LAST_PAYMENT_DT],		
		
       convert(date,getdate()) as ROW_INSERT_DT,		
GETDATE() AS ETL_CREA_DT,		
GETDATE() AS ETL_UPDT_DT		
		
		
from [dbo].[D_LOAN] T1		
		
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2		
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))		
		
left join data_hub."dbo"."SAP_CRS_OGD_LOAN_PROFILE" crs		
on T1.LOAN_PROJECT_NBR = crs.CUSTOMER_PROJECT_NBR		
		
Left Join [dbo].[D_SECTOR] T3		
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD		
		
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T4		
--	ON T2.GEO_REGION_CD =  T4.DAC_GEOGRAPHIC_REGION_CD	
--	AND T4.DAC_SID_IND = 1	
where T2.AGENCY_ID = 3
```

SQL Query used to extract data from multiple sources to load the F_GC_LOAN table

```markdown
Select T1.LOAN_SID,	
       ISNULL(T2.GEO_REGION_CD, '-3') as DAC_REGION_CD,	
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,	
	
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],	
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],	
      T4.[LOAN_START_DT],	
      T4.[LOAN_END_DT],	
      T4.[ORIGINAL_AMT_DESCR],	
      T4.[BALANCE_AMT_DESCR],	
      T4.[COVERING_PERIOD_DESCR],	
      T4.[PAYMENT_DUE_DT_DESCR],	
      T4.[PRINCIPLE_BALANCE_AMT_DESCR],	
      T4.[INTEREST_BALANCE_AMT_DESCR],	
      T2.[INTEREST_RATE_NBR],	
      T2.[SECOND_INTEREST_RATE_NBR],	
      T4.[FIRST_PAYMENT_DT],	
      T4.[LAST_PAYMENT_DT],	
	
       convert(date,getdate()) as ROW_INSERT_DT,	
GETDATE() AS ETL_CREA_DT,	
GETDATE() AS ETL_UPDT_DT	
	
	
from [dbo].[D_LOAN] T1	
	
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2	
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))	
	
Left Join [dbo].[D_SECTOR] T3	
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD	
	
left Join DATA_HUB.[dbo].[SAP_CRS_OGD_LOAN_PROFILE] T4	
on T1.LOAN_PROJECT_NBR = T4.CUSTOMER_PROJECT_NBR	
	
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T5	
--	ON T2.GEO_REGION_CD =  T5.DAC_GEOGRAPHIC_REGION_CD
--	AND T5.DAC_SID_IND = 1
	
where T2.AGENCY_ID != 3
```

SQL Query used to extract data from multiple sources to load the F_GC_LOAN table

```markdown
Select T1.LOAN_SID,		
       ISNULL(T2.GEO_REGION_CD,'-3') as DAC_REGION_CD,		
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,		
		
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],		
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],		
      crs.LOAN_START_DT as [LOAN_START_DT],		
      crs.LOAN_END_DT as [LOAN_END_DT],		
      crs.ORIGINAL_AMT_DESCR as [ORIGINAL_AMT_DESCR],		
      crs.BALANCE_AMT_DESCR as [BALANCE_AMT_DESCR],		
      crs.COVERING_PERIOD_DESCR as [COVERING_PERIOD_DESCR],		
      crs.PAYMENT_DUE_DT_DESCR as [PAYMENT_DUE_DT_DESCR],		
      crs.PRINCIPLE_BALANCE_AMT_DESCR as [PRINCIPLE_BALANCE_AMT_DESCR],		
      crs.INTEREST_BALANCE_AMT_DESCR as [INTEREST_BALANCE_AMT_DESCR],		
      T2.[INTEREST_RATE_NBR] as [INTEREST_RATE_NBR],		
      T2.[SECOND_INTEREST_RATE_NBR] as [SECOND_INTEREST_RATE_NBR],		
      NULL as [FIRST_PAYMENT_DT],		
      NULL as [LAST_PAYMENT_DT],		
		
       convert(date,getdate()) as ROW_INSERT_DT,		
GETDATE() AS ETL_CREA_DT,		
GETDATE() AS ETL_UPDT_DT		
		
		
from [dbo].[D_LOAN] T1		
		
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2		
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))		
		
left join data_hub."dbo"."SAP_CRS_OGD_LOAN_PROFILE" crs		
on T1.LOAN_PROJECT_NBR = crs.CUSTOMER_PROJECT_NBR		
		
Left Join [dbo].[D_SECTOR] T3		
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD		
		
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T4		
--	ON T2.GEO_REGION_CD =  T4.DAC_GEOGRAPHIC_REGION_CD	
--	AND T4.DAC_SID_IND = 1	
where T2.AGENCY_ID = 3
```

SQL Query used to extract data from multiple sources to load the F_GC_LOAN table

```markdown
Select T1.LOAN_SID,	
       ISNULL(T2.GEO_REGION_CD, '-3') as DAC_REGION_CD,	
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,	
	
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],	
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],	
      T4.[LOAN_START_DT],	
      T4.[LOAN_END_DT],	
      T4.[ORIGINAL_AMT_DESCR],	
      T4.[BALANCE_AMT_DESCR],	
      T4.[COVERING_PERIOD_DESCR],	
      T4.[PAYMENT_DUE_DT_DESCR],	
      T4.[PRINCIPLE_BALANCE_AMT_DESCR],	
      T4.[INTEREST_BALANCE_AMT_DESCR],	
      T2.[INTEREST_RATE_NBR],	
      T2.[SECOND_INTEREST_RATE_NBR],	
      T4.[FIRST_PAYMENT_DT],	
      T4.[LAST_PAYMENT_DT],	
	
       convert(date,getdate()) as ROW_INSERT_DT,	
GETDATE() AS ETL_CREA_DT,	
GETDATE() AS ETL_UPDT_DT	
	
	
from [dbo].[D_LOAN] T1	
	
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2	
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))	
	
Left Join [dbo].[D_SECTOR] T3	
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD	
	
left Join DATA_HUB.[dbo].[SAP_CRS_OGD_LOAN_PROFILE] T4	
on T1.LOAN_PROJECT_NBR = T4.CUSTOMER_PROJECT_NBR	
	
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T5	
--	ON T2.GEO_REGION_CD =  T5.DAC_GEOGRAPHIC_REGION_CD
--	AND T5.DAC_SID_IND = 1
	
where T2.AGENCY_ID != 3
```

SQL Query used to extract data from multiple sources to load the F_GC_LOAN table

```markdown
truncate table F_GC_LOAN;
truncate table F_GC_INITIATIVE;
```

SQL used in `ESQLT-Truncate_F_LOAN_AND_INITIATIVE`

```markdown
IF EXISTS(SELECT * FROM sys.indexes WHERE name = 'IDX_F_GC_FINANCIAL_CFO_STATS' AND object_id = OBJECT_ID('F_GC_FINANCIAL_CFO_STATS'))

DROP INDEX [IDX_F_GC_FINANCIAL_CFO_STATS] ON [dbo].[F_GC_FINANCIAL_CFO_STATS]
GO

/****** Object:  Index [IDX_F_GC_FINANCIAL_CFO_STATS]    Script Date: 2024-05-24 11:13:50 AM ******/
CREATE UNIQUE NONCLUSTERED INDEX [IDX_F_GC_FINANCIAL_CFO_STATS] ON [dbo].[F_GC_FINANCIAL_CFO_STATS]
(
	[FISCAL_YEAR] ASC,
	[FY_GC_FINAN_CFO_STATS_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

```

SQL used in `CREATE_INDEX` task

```markdown
Select T1.[LOAN_SID],		
       ISNULL(T2.GEO_REGION_CD, '-3') as DAC_REGION_CD,		
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,		
	
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],		
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],		
      T4.[LOAN_START_DT],		
      T4.[LOAN_END_DT],		
      T4.[ORIGINAL_AMT_DESCR],		
      T4.[BALANCE_AMT_DESCR],		
      T4.[COVERING_PERIOD_DESCR],		
      T4.[PAYMENT_DUE_DT_DESCR],		
      T4.[PRINCIPLE_BALANCE_AMT_DESCR],		
      T4.[INTEREST_BALANCE_AMT_DESCR],		
      T2.[INTEREST_RATE_NBR],		
      T2.[SECOND_INTEREST_RATE_NBR],		
      T4.[FIRST_PAYMENT_DT],		
      T4.[LAST_PAYMENT_DT],		
	
       convert(date,getdate()) as ROW_INSERT_DT,		
GETDATE() AS ETL_CREA_DT,		
GETDATE() AS ETL_UPDT_DT		
	
	
from [dbo].[D_LOAN] T1	
	
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2	
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))	
	
Left Join [dbo].[D_SECTOR] T3	
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD	
	
left Join DATA_HUB.[dbo].[SAP_CRS_OGD_LOAN_PROFILE] T4	
on T1.LOAN_PROJECT_NBR = T4.CUSTOMER_PROJECT_NBR	
	
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T5	
--	ON T2.GEO_REGION_CD =  T5.DAC_GEOGRAPHIC_REGION_CD
--	AND T5.DAC_SID_IND = 1
	
where T2.AGENCY_ID != 3
```

SQL query used in `OLEBD-src_D_LOAN`

```markdown
truncate table F_GC_LOAN;
truncate table F_GC_INITIATIVE;
```

SQL used in `ESQLT-Truncate_F_LOAN_AND_INITIATIVE`

```markdown
Select T1.LOAN_SID,		
       ISNULL(T2.GEO_REGION_CD,'-3') as DAC_REGION_CD,		
       ISNULL(T3.SECTOR_SID, '-3') as SECTOR_SID,		
		
      ISNULL(T2.TIED_AID_AMT, 0 ) as [TIED_AID_AMT],		
      ISNULL(T2.UNTIED_AID_AMT, 0 ) as [UNTIED_AID_AMT],		
      crs.LOAN_START_DT as [LOAN_START_DT],		
      crs.LOAN_END_DT as [LOAN_END_DT],		
      crs.ORIGINAL_AMT_DESCR as [ORIGINAL_AMT_DESCR],		
      crs.BALANCE_AMT_DESCR as [BALANCE_AMT_DESCR],		
      crs.COVERING_PERIOD_DESCR as [COVERING_PERIOD_DESCR],		
      crs.PAYMENT_DUE_DT_DESCR as [PAYMENT_DUE_DT_DESCR],		
      crs.PRINCIPLE_BALANCE_AMT_DESCR as [PRINCIPLE_BALANCE_AMT_DESCR],		
      crs.INTEREST_BALANCE_AMT_DESCR as [INTEREST_BALANCE_AMT_DESCR],		
      T2.[INTEREST_RATE_NBR] as [INTEREST_RATE_NBR],		
      T2.[SECOND_INTEREST_RATE_NBR] as [SECOND_INTEREST_RATE_NBR],		
      NULL as [FIRST_PAYMENT_DT],		
      NULL as [LAST_PAYMENT_DT],		
		
       convert(date,getdate()) as ROW_INSERT_DT,		
GETDATE() AS ETL_CREA_DT,		
GETDATE() AS ETL_UPDT_DT		
		
		
from [dbo].[D_LOAN] T1		
		
join DATA_HUB."dbo"."SAP_LOAN_PROFILE" T2		
on CAST(T1.LOAN_PROJECT_NBR as varbinary(100)) = CAST(T2.CRS_PROJECT_NBR as varbinary(100))		
		
left join data_hub."dbo"."SAP_CRS_OGD_LOAN_PROFILE" crs		
on T1.LOAN_PROJECT_NBR = crs.CUSTOMER_PROJECT_NBR		
		
Left Join [dbo].[D_SECTOR] T3		
on T2.SECTOR_CD = T3.DAC_SECTOR_LEVEL3_CD		
		
--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T4		
--	ON T2.GEO_REGION_CD =  T4.DAC_GEOGRAPHIC_REGION_CD	
--	AND T4.DAC_SID_IND = 1	
where T2.AGENCY_ID = 3
```

SQL query used in `OLEBD-src_D_LOAN`

```markdown
SELECT
 T2.INITIATIVE_SID,
 ISNULL(T1.GEO_REGION_CD, '-3') AS DAC_REGION_CD,
 T1.TIED_AID_AMT,
 T1.UNTIED_AID_AMT,
 T1.OUTSTANDING_AMT,
 T1.FIRST_REPAYMENT_DT AS FIRST_PAYMENT_DT,
 T1.FINAL_REPAYMENT_DT AS LAST_PAYMENT_DT,
 T1.LOAN_START_DT AS START_DT,
 T1.LOAN_END_DT AS END_DT,
 T1.COMMITEMENT_AMT AS COMMITMENT_AMT,
 T1.CAPITAL_EXPENDITURE_PER,
 T1.COMMITMENT_DT,
 T1.DISBURSEMENT_DT,
 T1.INVESTMENT_RELATED_TECH_COOP_AMT,
 T1.ARREARS_INTEREST_AMT,
 T1.ARREARS_PRINCIPLE_AMT,
 T1.DISBURESEMENT_AMT AS DISBURSEMENT_AMT,
 T1.INTEREST_RATE_NBR AS INTEREST_RATE_AMT,
 T1.INTEREST_RECEIVED_AMT,
 T1.RECEIVED_AMT,
 T1.SECOND_INTEREST_RATE_NBR AS SECOND_INTEREST_RATE_AMT,
 CONVERT(DATE,GETDATE()) AS ROW_INSERT_DT,
GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT

FROM DBO.SAP_OGD_EDC_LOAN T1 -- 2885

JOIN MART_GC.DBO.D_INITIATIVE T2
  ON T1.CRS_ID = T2.CRS_ID AND T1.CRS_ID_SUFFIX = T2.CRS_ID_SUFFIX AND T1.REPORTING_PERIOD = T2.REPORTING_PERIOD AND T1.OGD_YR = T2.YEAR

--LEFT JOIN DBO.D_GC_GEOGRAPHIC_REGION T3
-- ON REPLICATE('0',5-LEN(T1.GEO_REGION_CD)) + T1.GEO_REGION_CD = T3.DAC_GEOGRAPHIC_REGION_CD
-- AND T3.DAC_SID_IND = 1
```

SQL query used in `OLEDB-src_D_INITIATIVE`

```markdown
truncate table F_GC_LOAN;
truncate table F_GC_INITIATIVE;
```

SQL used in `ESQLT-Truncate_F_LOAN_AND_INITIATIVE`

```markdown
SELECT COUNTRY_SID  ,GAC_COUNTRY_CD  FROM dbo.D_COUNTRY
```

SQL query used in `LKP_TRFM_ D_COUNTRY`

```markdown
SELECT ACCOUNTING_FISCAL_PERIOD_SID AS FISCAL_YEAR_SID,ACCOUNTING_FISCAL_YEAR  FROM dbo.D_ACCOUNTING_FISCAL_PERIOD
WHERE [ACCOUNTING_FISCAL_PERIOD] = '00'
```

SQL query used in `LKP_TRFM_ FISCAL_YEAR_SID`

```markdown
SELECT FUND_SID,RTRIM(FUND_NBR) AS FUND_NBR  FROM dbo.D_FUND
```

SQL query used in `LKP_TRFM_D_FUND`

```markdown
SELECT FUND_CENTRE_SID as  FUND_CENTRE_SID ,FUND_CENTRE_CD FROM dbo.D_FUND_CENTRE
```

SQL query used in `LKP_TRFM_D_FUND_CENTRE`

```markdown
SELECT PROJECT_WBS_SID,WBS_NBR AS WBS_NBR  FROM