## 1. Input Connection Analysis

| Connection Manager Name          | Connection Type | Connection String Details  | Purpose within Package                        | Security Requirements | Parameters/Variables | Source Part |
|------------------------------------|-----------------|---------------------------|-----------------------------------------------|-----------------------|-----------------------|-------------|
| FC_Staging_TRGT           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Target for staging tables                     | SQL Server Auth likely | None                  | All Parts   |
| BI_Conformed        | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for `BI_CONFORMED_SYMBOL_NAME` view      | SQL Server Auth likely | None                  | Part 1       |
| PS_Source_DB_FC        | OLE DB          | Server: [Inferred], Database: [Inferred]  | Target for `S_FC_FIN_HR_INACTIVE_SYMBOLS` table      | SQL Server Auth likely | None                  | Part 1       |
| PS_Source_DB          | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for views `PS_G9_FC_SYMBL_TBL` and `PS_G9_FC_SYMCD_TBL`     | SQL Server Auth likely | None                  | Part 1       |
| SAP_SOURCE_SRC          | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for tables `ZZGWACT, SETHEADER` and `SAP_SETLEAF_ALL`      | SQL Server Auth likely | None                  | Part 1       |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No execute SSIS packages tasks found   | All Parts|

## 3. Package Flow Analysis

The package begins with an `Expression Task` that evaluates a simple expression (1 == 1).

The package then executes two sequence containers based on an expression: `SEQC_1_S_FC_SETHEADER` and `SEQC-R_FC_BI_SYMBOL_MAPPINGS`.

The expression used to determine whether the `SEQC_1_S_FC_SETHEADER` sequence container is executed is `(UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "ALL") || (UPPER(TRIM(@[$Project::PRJ_PRM_PROCESS_NODE])) == "STAGING")`

#### SEQC-R_FC_BI_SYMBOL_MAPPINGS

1.  **Execute SQL Task:** `ESQLT-TRUNCATE_R_FC_BI_SYMBOL_MAPPINGS` truncates the `dbo.R_FC_BI_SYMBOL_MAPPINGS` table.
2.  **Data Flow Task:** `DFT-R_FC_BI_SYMBOL_MAPPINGS` loads data into the `dbo.R_FC_BI_SYMBOL_MAPPINGS` table.

    *   **Source:** `OLEDB_SRC-BI_CONFORMED_SYMBOL_NAME` extracts data from `dbo.BI_CONFORMED_SYMBOL_NAME`.
    *   **Transformations:**
        *   `Derived Column`: Adds `ETL_CREA_DT` and `ETL_UPDT_DT` using `GETDATE()`.
    *   **Destination:** `OLEDB_DEST-R_FC_BI_SYMBOL_MAPPINGS` loads data into `dbo.R_FC_BI_SYMBOL_MAPPINGS`.

#### SEQC_1_S_FC_SETHEADER:

1.  **Execute SQL Task:** `ESQLT-TRUNCATE_TABLES_In_Staging` truncates several staging tables, including `dbo.S_FC_SETHEADER`, `dbo.S_FC_SETLEAF`, `dbo.S_FC_SETNODE`, `dbo.S_FC_HIERARCHY_1`, `dbo.S_FC_HIERARCHY_2`, `dbo.S_FC_HIERARCHY_3`, `dbo.S_FC_GROUPS`, `dbo.S_FC_GROUPS_HIERARCHY`, `dbo.S_FC_GROUPS_LEVEL2`, `dbo.S_FC_FIN_HR_SYMBOLS`, `dbo.S_FC_PAC` and `dbo.S_FC_SETLEAF_PAC`.
2.  **Execute SQL Task:** `ESQLT-TRUNCATE_TABLES_In_PS_SOURCE_DB` truncates table `dbo.S_FC_FIN_HR_INACTIVE_SYMBOLS`.
3.  **Data Flow Task:** `DFT-S_FC_FIN_HR_INACTIVE_SYMBOLS` loads data into `dbo.S_FC_FIN_HR_INACTIVE_SYMBOLS`.

    *   **Source:** `OLEDB_SRC-PS_G9_FC_SYMBL_TBL` extracts data from a SELECT statement that joins tables `dbo.PS_G9_FC_SYMBL_TBL` and `dbo.PS_G9_FC_SYMCD_TBL` where `EFF_STATUS` is 'I'.
    *   **Destination:** `OLEDB_DEST_S_FC_FIN_HR_INACTIVE_SYMBOLS` loads data into `dbo.S_FC_FIN_HR_INACTIVE_SYMBOLS`.
4.  **Data Flow Task:** `DFT-S_FC_SETHEADER` loads data into `dbo.S_FC_SETHEADER`.

    *   **Source:** `OLEDB_SRC-SAP_SOURCE-SETHEADER` extracts data from a SELECT statement that filters data on `SETCLASS = '0312'` and `subclass = '0050'`
    *   **Destination:** `OLEDB_DEST-S_FC_SETHEADER` loads data into `dbo.S_FC_SETHEADER`.
5.  **Data Flow Task:** `DFT-S_FC_SETLEAF` loads data into `dbo.S_FC_SETLEAF`.

    *   **Source:** `OLEDB_SRC-SAP_SOURCE-SAP_SETLEAF_ALL` extracts data from `dbo.SAP_SETLEAF_ALL` based on specific filter criteria.
    *   **Destination:** `OLEDB_DEST-S_FC_SETLEAF` loads data into `dbo.S_FC_SETLEAF`.
6.  **Data Flow Task:** `DFT-S_FC_SETNODE` loads data into `dbo.S_FC_SETNODE`.

    *   **Source:** `OLEDB_SRC-SAP_SOURCE-SAP_SETNODE` extracts data from `dbo.SETNODE` based on specific filter criteria.
    *   **Destination:** `OLEDB_DEST-S_FC_SETNODE` loads data into `dbo.S_FC_SETNODE`.
7.  **Data Flow Task:** `DFT-S_FC_HIERARCHY_1` loads data into `dbo.S_FC_HIERARCHY_1`.

    *   **Source:** `OLEDB_SRC-S_FC_SETNODE` extracts data from `dbo.S_FC_SETNODE` based on specific filter criteria.
    *   **Destination:** `OLEDB_DEST-S_FC_HIERARCHY_1` loads data into `dbo.S_FC_HIERARCHY_1`.
8.  **Data Flow Task:** `DFT-S_FC_HIERARCHY_2` loads data into `dbo.S_FC_HIERARCHY_2`.

    *   **Source:** `OLEDB_SRC-S_FC_HIERARCHY_1_&_S_FC_SETLEAF` extracts data from a SELECT statement that joins `dbo.S_FC_HIERARCHY_1` and `dbo.S_FC_SETLEAF`.
    *   **Destination:** `OLEDB_DEST-S_FC_HIERARCHY_2` loads data into `dbo.S_FC_HIERARCHY_2`.
9.  **Data Flow Task:** `DFT-S_FC_HIERARCHY_3` loads data into `dbo.S_FC_HIERARCHY_3`.

    *   **Source:** `OLEDB_SRC-S_FC_HIERARCHY_2_&_S_FC_SETLEAF` extracts data from a SELECT statement that joins `dbo.S_FC_HIERARCHY_2` and `dbo.S_FC_SETLEAF`.
    *   **Destination:** `OLEDB_DEST-S_FC_HIERARCHY_3` loads data into `dbo.S_FC_HIERARCHY_3`.
10. **Data Flow Task:** `DFT-S_FC_GROUPS` loads data into `dbo.S_FC_GROUPS`.

    *   **Source:** `OLEDB_SRC-S_FC_SETHEADER_&_S_FC_SETNODE` extracts data by joining `dbo.S_FC_SETHEADER`, `dbo.S_FC_SETNODE` and `dbo.S_FC_SETLEAF`.
    *   **Destination:** `OLEDB_DEST-S_FC_GRROUPS` loads data into `dbo.S_FC_GROUPS`.
11. **Data Flow Task:** `DFT-S_FC_GROUPS_HIERARCHY` loads data into `dbo.S_FC_GROUPS_HIERARCHY`.

    *   **Source:** `OLEDB_SRC-S_FC_HIERARCHY_2_&_S_FC_SETLEAF_&_S_FC_SETNODE` extracts data from a UNION ALL of two SELECT statements against `dbo.S_FC_HIERARCHY_2`, `dbo.S_FC_SETLEAF` and `dbo.S_FC_SETNODE`.
    *   **Destination:** `OLEDB_DEST-S_FC_GROUPS_HIERARCHY` loads data into `dbo.S_FC_GROUPS_HIERARCHY`.
12. **Data Flow Task:** `DFT-S_FC_GROUPS_LEVEL2` loads data into `dbo.S_FC_GROUPS_LEVEL2`.

    *   **Source:** `OLEDB_SRC-S_FC_SETNODE` extracts data from `dbo.S_FC_SETNODE` based on specific filter criteria.
    *   **Destination:** `OLEDB_DEST-S_FC_GROUPS_LEVEL2` loads data into `dbo.S_FC_GROUPS_LEVEL2`.
13. **Data Flow Task:** `DFT-S_FC_FIN_HR_SYMBOLS` loads data into `dbo.S_FC_FIN_HR_SYMBOLS`.

    *   **Source:** `OLEDB_SRC-PS_SOURCE_DB__PS_G9_FC_SYMBL_TBL` extracts data from a SELECT statement that joins `dbo.PS_G9_FC_SYMBL_TBL` and `dbo.PS_G9_FC_SYMCD_TBL` where `EFF_STATUS = 'A'`.
    *   **Destination:** `OLEDB_DEST-S_FC_FIN_HR_SYMBOLS` loads data into `dbo.S_FC_FIN_HR_SYMBOLS`.
14. **Data Flow Task:** `DFT-S_FC_PAC` loads data into `dbo.S_FC_PAC`.

    *   **Source:** `OLEDB_SRC-SAP_SOURCE-ZZGWACT` extracts data from a SELECT statement against `dbo.ZZGWACT`
    *   **Destination:** `OLEDB_DEST-S_FC_PAC` loads data into `dbo.S_FC_PAC`.
15. **Data Flow Task:** `DFT-S_FC_SETLEAF_PAC` loads data into `dbo.S_FC_SETLEAF_PAC`.

    *   **Source:** `OLEDB_SRC-SAP_SOURCE-SAP_SETLEAF_ALL` extracts data from `dbo.SAP_SETLEAF_ALL` based on specific filter criteria.
    *   **Destination:** `OLEDB_DEST-S_FC_SETLEAF_PAC` loads data into `dbo.S_FC_SETLEAF_PAC`.

## 4. Code Extraction

```sql
SELECT	"FUND_CENTRE_CD",
	"BI_FC_DESC_EN",
	"BI_FC_DESC_FR"
FROM   "dbo"."BI_CONFORMED_SYMBOL_NAME"
```

Context: SQL query for the `OLEDB_SRC-BI_CONFORMED_SYMBOL_NAME` OLE DB Source

```sql
SELECT DISTINCT
       T1.G9_FC_SYMBOL_ID,
       T1.EFFDT,
       T1.EFF_STATUS,
       T1.DESCR, T1.DESCRSHORT,
       SUBSTRING(T1.DESCRSHORT, 1, CHARINDEX(' FC', T1.DESCRSHORT)) AS FC_SYMBOL,
       T2.G9_FUND_CENTER,
GETDATE() AS ETL_CREA_DT,
GETDATE() AS ETL_UPDT_DT
FROM   dbo.PS_G9_FC_SYMBL_TBL T1 INNER JOIN
       dbo.PS_G9_FC_SYMCD_TBL T2 ON T1.G9_FC_SYMBOL_ID = T2.G9_FC_SYMBOL_ID
WHERE  (T1.EFF_STATUS = 'I')

ORDER BY T2.G9_FUND_CENTER
```

Context: SQL query for the `OLEDB_SRC-PS_G9_FC_SYMBL_TBL` OLE DB Source.

```sql
SELECT DISTINCT
       TOP 100 PERCENT T1.SETID,
       T1.G9_FC_SYMBOL_ID,
       T1.EFFDT,
       T1.EFF_STATUS,
       T1.DESCR, T1.DESCRSHORT,
       SUBSTRING(T1.DESCRSHORT, 1, CHARINDEX(' FC', T1.DESCRSHORT)) AS FC_SYMBOL,
       T2.G9_FUND_CENTER,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM   dbo.PS_G9_FC_SYMBL_TBL T1 INNER JOIN
       dbo.PS_G9_FC_SYMCD_TBL T2 ON T1.G9_FC_SYMBOL_ID = T2.G9_FC_SYMBOL_ID
WHERE  (T1.EFF_STATUS = 'A') AND (T1.EFFDT = (SELECT TOP 1 MAX(T3.EFFDT)
                                              FROM dbo.PS_G9_FC_SYMBL_TBL T3,
                                                   dbo.PS_G9_FC_SYMCD_TBL T4
                                              WHERE T3.G9_FC_SYMBOL_ID = T4.G9_FC_SYMBOL_ID
                                              AND T2.G9_FUND_CENTER = T4.G9_FUND_CENTER
                                              AND EFF_STATUS = 'A'))
--and T2.G9_FUND_CENTER = 11210

ORDER BY T2.G9_FUND_CENTER
```

Context: SQL query for the `OLEDB_SRC-PS_SOURCE_DB__PS_G9_FC_SYMBL_TBL` OLE DB Source.

```sql
SELECT distinct
       T2."SETNAME" as NODE_SETNAME,
	T2."SUBSETNAME" as NODE_SUBSETNAME,
	T1."SETTYPE",
	T1."CREDATE",
	T1."UPDDATE",
	T1."SAPRL",
	T1."TABNAME",
	T1."FIELDNAME",
	T1."ROLLNAME",
	T2."LINEID",
	T2."SEQNR",
       t3."VALTO" as FC_CODE,

	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT

FROM   dbo."S_FC_SETHEADER" T1,
        dbo.S_FC_SETNODE T2,
       "dbo"."S_FC_SETLEAF" T3
WHERE T1.SETNAME = T2.sUBSETNAME
AND T2.SUBSETNAME = t3."SETNAME"
```

Context: SQL query for the `OLEDB_SRC-S_FC_SETHEADER_&_S_FC_SETNODE` OLE DB Source.

```sql
SELECT	DISTINCT T1."SETNAME",
	T1."SETNAME_LEVEL2",
	T1."SETNAME_LEVEL3",
       T2."VALFROM" AS SETNAME_LEVEL4,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM   "dbo"."S_FC_HIERARCHY_2" T1 LEFT OUTER JOIN
      "dbo"."S_FC_SETLEAF" T2
ON  T1.SETNAME_LEVEL3 = T2.SETNAME

UNION ALL

SELECT DISTINCT ST1.SETNAME,
       ST1."SETNAME_LEVEL2",
	ST1."SETNAME_LEVEL3",
       (ST2.SUBSETNAME)  AS SETNAME_LEVEL4,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM (SELECT	DISTINCT T1."SETNAME",
	T1."SETNAME_LEVEL2",
	T1."SETNAME_LEVEL3",
       T2."VALFROM" AS SETNAME_LEVEL4
FROM   "dbo"."S_FC_HIERARCHY_2" T1 LEFT OUTER JOIN
       "dbo"."S_FC_SETLEAF" T2
ON  T1.SETNAME_LEVEL3 = T2.SETNAME ) AS ST1 LEFT OUTER JOIN S_FC_SETNODE ST2
ON ST1.SETNAME_LEVEL3 = ST2.SETNAME
```

Context: SQL query for the `OLEDB_SRC-S_FC_HIERARCHY_2_&_S_FC_SETLEAF_&_S_FC_SETNODE` OLE DB Source.

```sql
SELECT	distinct
	"SETNAME",
	"SUBSETNAME",
       2 as LEVEL,

      getdate() as ETL_CREA_DT,
      getdate() as ETL_UPDT_DT

FROM   "dbo"."S_FC_SETNODE"
--where isnumeric(setname) = 0
--where setname like 'RRD%'
ORDER BY SUBSETNAME
```

Context: SQL query for the `OLEDB_SRC-S_FC_SETNODE` (for DFT-S_FC_GROUPS_LEVEL2) OLE DB Source.

```sql
SELECT	distinct
	"SETNAME",
        SUBSETNAME,
       1 as LEVEL,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM   "dbo"."S_FC_SETNODE"
where isnumeric(setname) = 0
and len(setname) - charindex('_',SETNAME) = 5
and charindex('_',SETNAME) > 0
--and SETNAME like 'RRD%'
```

Context: SQL query for the `OLEDB_SRC-S_FC_SETNODE` (for DFT-S_FC_HIERARCHY_1) OLE DB Source.

```sql
SELECT	DISTINCT T1."SETNAME",
	T1."SUBSETNAME" AS SETNAME_LEVEL2,
       COALESCE(COALESCE(T2.VALFROM,T3.SUBSETNAME),T1."SUBSETNAME") AS SETNAME_LEVEL3,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM   "dbo"."S_FC_HIERARCHY_1" T1 LEFT OUTER JOIN
       "dbo"."S_FC_SETLEAF" T2
ON  T1.SUBSETNAME = T2.SETNAME LEFT OUTER JOIN "dbo"."S_FC_SETNODE" T3 ON T1.SUBSETNAME = T3.SETNAME
--WHERE T2.SETNAME IS NOT NULL
--where  COALESCE(COALESCE(T2.VALFROM,T3.SUBSETNAME),T1."SUBSETNAME") = '30471'
order by 1, 2, 3
```

Context: SQL query for the `OLEDB_SRC-S_FC_HIERARCHY_1_&_S_FC_SETLEAF` OLE DB Source.

```sql
SELECT	DISTINCT T1."SETNAME",
	SETNAME_LEVEL2,
       SETNAME_LEVEL3,
       COALESCE(COALESCE(T2.VALFROM,T3.SUBSETNAME), SETNAME_LEVEL3) AS SETNAME_LEVEL4,

	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT

FROM   "dbo"."S_FC_HIERARCHY_2" T1 LEFT OUTER JOIN
       "dbo"."S_FC_SETLEAF" T2
ON  T1.SETNAME_LEVEL3 = T2.SETNAME LEFT OUTER JOIN "dbo"."S_FC_SETNODE" T3 ON T1.SETNAME_LEVEL3 = T3.SETNAME
--where COALESCE(COALESCE(T2.VALFROM,T3.SUBSETNAME), SETNAME_LEVEL3) = '30471'
--WHERE T1.SETNAME LIKE'RRD%'
order by 1, 2, 3
```

Context: SQL query for the `OLEDB_SRC-S_FC_HIERARCHY_2_&_S_FC_SETLEAF` OLE DB Source.

```sql
SELECT
	SUBSTRING("ZZGWAC",3,2) as PAC_CD,
       MAX(CASE
             WHEN SPRAS = 'E' THEN ZZGWACT
       END) as PAC_DESCR_EN,
       MAX(CASE
             WHEN SPRAS = 'F' THEN ZZGWACT
       END) as PAC_DESCR_FR,

       getdate() as ETL_CREA_DT,
       getdate() as ETL_UPDT_DT

FROM   "dbo"."ZZGWACT"
WHERE FIKRS = '0050'
AND SUBSTRING(ZZGWAC,1,2) = '00'
AND ZZGWAC not in ( '000')
AND SUBSTRING("ZZGWAC",3,2) <> '00'
GROUP BY ZZGWAC
```

Context: SQL query for the `OLEDB_SRC-SAP_SOURCE-ZZGWACT` OLE DB Source.

```sql
SELECT	"MANDT",
	"SETCLASS",
	"SUBCLASS",
	"SETNAME",
	"SETTYPE",
	"XDYNAMIC",
	"AUTHGR",
	"XUNIQ",
	"RVALUE",
	"CREUSER",
	"CREDATE",
	"CRETIME",
	"UPDUSER",
	"UPDDATE",
	"UPDTIME",
	"SAPRL",
	"TABNAME",
	"FIELDNAME",
	"ROLLNAME",
	"SET_OLANGU",
	"NO_RWSHEADER",
	"NO_RWSLINE",
	"NO_SETLINET",

	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT

FROM   "dbo"."SETHEADER"
where SETCLASS = '0312'
AND subclass = '0050'
--and setname like 'L%'
AND isnumeric(substring(setname, 1,1)) = 0
order by setname
```

Context: SQL query for the `OLEDB_SRC-SAP_SOURCE-SETHEADER` OLE DB Source.

```sql
SELECT	"MANDT",
	"SETCLASS",
	"SUBCLASS",
	"SETNAME",
	"LINEID",
	"VALSIGN",
	"VALOPTION",
	"VALFROM",
	"VALTO",
	"SEQNR",

	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT

FROM   "dbo"."SAP_SETLEAF_ALL"
where setclass = '0312'
and subclass = '0050'
and isnumeric(substring(setname, 1,1)) = 0
--and setname like '%_531'
```

Context: SQL query for the `OLEDB_SRC-SAP_SOURCE-SAP_SETLEAF_ALL` (for DFT-S_FC_SETLEAF) OLE DB Source.

```sql
SELECT	"MANDT",
	"SETCLASS",
	"SUBCLASS",
	"SETNAME",
	"LINEID",
	"VALSIGN",
	"VALOPTION",
	"VALFROM",
	"VALTO",
	"SEQNR",

	getdate() as ETL_CREA_DT,
	getdate() as ETL_UPDT_DT

FROM   "dbo"."SAP_SETLEAF_ALL"
where setname like 'Z-FC%'
```

Context: SQL query for the `OLEDB_SRC-SAP_SOURCE-SAP_SETLEAF_ALL` (for DFT-S_FC_SETLEAF_PAC) OLE DB Source.

```sql
TRUNCATE TABLE dbo.R_FC_BI_SYMBOL_MAPPINGS;
```

Context: SQL query for the `ESQLT-TRUNCATE_R_FC_BI_SYMBOL_MAPPINGS` Execute SQL Task.

```sql
TRUNCATE TABLE dbo.S_FC_SETHEADER;

TRUNCATE TABLE dbo.S_FC_SETLEAF;

TRUNCATE TABLE dbo.S_FC_SETNODE;

TRUNCATE TABLE dbo.S_FC_HIERARCHY_1;

TRUNCATE TABLE dbo.S_FC_HIERARCHY_2;
  
TRUNCATE TABLE dbo.S_FC_HIERARCHY_3;

TRUNCATE TABLE dbo.S_FC_GROUPS;

TRUNCATE TABLE dbo.S_FC_GROUPS_HIERARCHY;

TRUNCATE TABLE dbo.S_FC_GROUPS_LEVEL2;

TRUNCATE TABLE dbo.S_FC_FIN_HR_SYMBOLS;

TRUNCATE TABLE dbo.S_FC_PAC

TRUNCATE TABLE dbo.S_FC_SETLEAF_PAC
```

Context: SQL query for the `ESQLT-TRUNCATE_TABLES_In_Staging` Execute SQL Task.

```sql
TRUNCATE TABLE [dbo].[S_FC_FIN_HR_INACTIVE_SYMBOLS];
```

Context: SQL query for the `ESQLT-TRUNCATE_TABLES_In_PS_SOURCE_DB` Execute SQL Task.

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
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'FC_Master.dtsx' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'FC_Staging.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: SQL query for the `ESQLT- Update ETL Process Status to Failed` Execute SQL Task in `OnError` event handler.

```sql
UPDATE ETL_RUN_STATUS
 SET ETL_RUN_STATUS_DESC = 'SUCCEEDED'
    ,ETL_RUN_RECORD_UPDT_DT = GETDATE()
WHERE  ETL_RUN_STATUS.ETL_RUN_STATUS_ID in
(
select max(e.ETL_RUN_STATUS_ID)
from ETL_RUN_STATUS e
where (e.ETL_COMPONENT_ID +'-' + e.ETL_SUB_COMPONENT_ID) in 
(
 SELECT ETL_SUB_COMPONENT_ID  +'-' +ETL_COMPONENT.ETL_COMPONENT_ID 
  FROM    ETL_SUB_COMPONENT  INNER JOIN  ETL_COMPONENT  ON (ETL_SUB_COMPONENT.ETL_COMPONENT_ID = ETL_COMPONENT.ETL_COMPONENT_ID)
 WHERE 
   ETL_COMPONENT_NM = 'FC_Master.dtsx' 
   AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC' 
   AND ETL_SUB_COMPONENT.ETL_SUB_COMPONENT_NM = 'FC_Staging.DTSX'
)
 AND ETL_RUN_STATUS_DESC = 'RUNNING'
 AND ETL_RUN_MAIN_COMPONENT_IND = 0
)
;
```

Context: SQL query for the `ESQLT- Update ETL Process Status to Succeeded` Execute SQL Task in `OnPostExecute` event handler.

```sql
INSERT INTO [ETL_RUN_STATUS] 
	(
 [ETL_COMPONENT_ID]
 ,[ETL_SUB_COMPONENT_ID]
 ,[ETL_RUN_STATUS_DESC]
 ,[ETL_RUN_MAIN_COMPONENT_IND]
 ,[ETL_RUN_RECORD_CREA_DT]
 ,[ETL_RUN_RECORD_UPDT_DT]
 )

VALUES 
	(
 (
  SELECT ETL_COMPONENT_ID
  
		FROM ETL_COMPONENT
  
		WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'   -- 'STRATEGIA_MASTER.DTSX'
   
		AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC'   -- 'DataAnalytics/1- SICB Content Repository/SSIS/STRATEGIA'
  )
 
	,(
  SELECT ETL_SUB_COMPONENT_ID
  
		FROM ETL_SUB_COMPONENT
  
		WHERE ETL_COMPONENT_ID IN 
			(
    SELECT ETL_COMPONENT_ID
    
				FROM ETL_COMPONENT
    
				WHERE ETL_COMPONENT_NM = 'FC_Master.dtsx'
     
				AND ETL_REPOSITORY_FULL_PATH = 'DataAnalytics/1- SICB Content Repository/SSIS/FC' 
    )
   
			AND ETL_SUB_COMPONENT_NM = 'FC_Staging.DTSX'   --'STRATEGIA_STAGING.DTSX'
  )

	 ,'RUNNING'
 
	,0
 
	,GETDATE()
 	
	,GETDATE()

 )

;
```

Context: SQL query for the `ESQLT- Create Record  with Running Status` Execute SQL Task in `OnPreExecute` event handler.

## 5. Output Analysis

| Destination Table               | Description                                                                      | Source Part |
|-----------------------------------|----------------------------------------------------------------------------------|-------------|
| dbo.R_FC_BI_SYMBOL_MAPPINGS       | Stores BI symbol mappings data                                                   | Part 1, 2, 3|
| dbo.S_FC_FIN_HR_INACTIVE_SYMBOLS  | Stores inactive financial and HR symbols                                          | Part 1      |
| dbo.S_FC_SETHEADER                | Stores financial control set headers                                              | Part 1      |
| dbo.S_FC_SETLEAF                  | Stores financial control set leaves                                               | Part 1      |
| dbo.S_FC_SETNODE                  | Stores financial control set nodes                                                | Part 1      |
| dbo.S_FC_HIERARCHY_1              | Stores financial control hierarchy level 1 data                                   | Part 1      |
| dbo.S_FC_HIERARCHY_2              | Stores financial control hierarchy level 2 data                                   | Part 1      |
| dbo.S_FC_HIERARCHY_3              | Stores financial control hierarchy level 3 data                                   | Part 1      |
| dbo.S_FC_GROUPS                   | Stores financial control groups                                                   | Part 1      |
| dbo.S_FC_GROUPS_HIERARCHY         | Stores financial control group hierarchy data                                     | Part 1      |
| dbo.S_FC_GROUPS_LEVEL2            | Stores financial control groups level 2 data                                      | Part 1      |
| dbo.S_FC_FIN_HR_SYMBOLS           | Stores active financial and HR symbols                                            | Part 1      |
| dbo.S_FC_PAC                      | Stores Program Activity Codes                                                    | Part 1      |
| dbo.S_FC_SETLEAF_PAC              | Stores financial control set leaves for Program Activity Codes                    | Part 1      |

The package logs success/failure status to the `ETL_RUN_STATUS` table.

## 6. Package Summary

*   **Input Connections:** 5
*   **Output Destinations:** 14 staging tables + 1 ETL status table
*   **Package Dependencies:** 0
*   **Activities:**
    *   Expression Tasks: 2+
    *   Sequence Containers: 2
    *   Data Flow Tasks: 11
    *   Execute SQL Tasks: 4

*   Overall package complexity assessment: Medium.
*   Potential performance bottlenecks: The number of staging tables being truncated and loaded.
*   Critical path analysis: The sequence of data flow tasks within `SEQC_1_S_FC_SETHEADER`.
*   Error handling mechanisms: The `OnError` event handler updates the `ETL_RUN_STATUS` table with a "FAILED" status. The `OnPreExecute` and `OnPostExecute` event handlers also update the `ETL_RUN_STATUS` table.
