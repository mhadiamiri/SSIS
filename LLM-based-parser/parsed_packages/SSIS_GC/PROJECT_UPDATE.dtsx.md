```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_GC_REPORTING          | OLE DB          | Server: [Inferred], Database: [Inferred]  | Destination and Source | SQL Server Auth likely | None            | Various                  |
| GC_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely            |  None                  | Part 2                |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2|

## 3. Package Flow Analysis

*   The package starts with an `Expression Task` named `EXPRESSIONT- Fact Tables - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode`.

*   The `Expression Task` is followed by two sequence containers running in parallel:
    *   `SEQC_WBS_LEVEL_2_DATE_UPDATES`
    *   `SEQC_Update_D_Vendor`

#### SEQC_WBS_LEVEL_2_DATE_UPDATES

1.  `ESQLT-Create_S_D_GC_WBS_LEVEL_2_TMP_Table`: Creates a temporary table `S_D_GC_WBS_LEVEL_2_TMP`.
2.  `DFT- Load_Tmp_Table_S_D_GC_WBS_LEVEL_2_TMP`: Loads data into the temporary table `S_D_GC_WBS_LEVEL_2_TMP`.
    *   **Source:** `OLEDB_SRC-s_gc_project_milestones` extracts data from `dbo.s_gc_project_milestones` in the `GC_STAGING` database. The query selects various milestone dates.
    *   **Destination:** `OLEDB_DEST-S_D_GC_WBS_LEVEL_2_TMP` inserts data into the `S_D_GC_WBS_LEVEL_2_TMP` table in the `MART_GC_REPORTING` database.
3.  `ESQLT-Create_Index`: Creates an index on the `S_D_GC_WBS_LEVEL_2_TMP` table.
4.  `DFT- Update_D_GC_WBS_LEVEL_2`: Updates the `D_GC_WBS_LEVEL_2` table with data from the temporary table.
    *   **Source:** `OLEDB_SRC-S_D_GC_WBS_LEVEL_2_TMP` extracts data from the `S_D_GC_WBS_LEVEL_2_TMP` table in the `MART_GC_REPORTING` database. The query performs logic to select dates and then joins to WBS table.
    *   **Destination:** `OLEDB_DEST-Update_D_GC_WBS_LEVEL_2` updates the `dbo.D_GC_WBS_LEVEL_2` table in the `MART_GC_REPORTING` database.
5.  `DFT- Update_D_GC_WBS_LEVEL_2_By_Fact`: Updates the `D_GC_WBS_LEVEL_2` table with data from `F_GC_WBS_MILESTONE`
    *   **Source:** `OLEDB_SRC-F_GC_WBS_MILESTONE` extracts data from the `F_GC_WBS_MILESTONE` table in the `MART_GC_REPORTING` database.
    *   **Destination:** `OLEDB-DEST-UPDATE_D_GC_WBS_LEVEL_2` updates the `dbo.D_GC_WBS_LEVEL_2` table in the `MART_GC_REPORTING` database.
6.  `ESQLT-Drop_Tmp_Table`: Drops the temporary table `S_D_GC_WBS_LEVEL_2_TMP`.

#### SEQC_Update_D_Vendor

1.  `DFT- Update_D_Vendor`: Updates the `D_GC_VENDOR` table.
    *   **Sources:**
        *   `OLEDB_SRC-EXECUTING_VENDOR_SID_W2` extracts data from `dbo.F_GC_WBS_LEVEL_2` to get `EXECUTING_VENDOR_SID`.
        *   `OLEDB_SRC- TARGETING_VENDOR_SID_W2` extracts data from `dbo.F_GC_WBS_LEVEL_2` to get `TARGETING_VENDOR_SID`.
        *   `OLEDB_SRC- F_GC_PURCHASE_ORDER` extracts data from `dbo.F_GC_PURCHASE_ORDER`.
    *   **Transformations:**
        *   `UNION ALL`: Combines the outputs from the three sources.
        *   `SORT_TRFM`: Sorts the data and removes duplicates.
        *   `DRVCOL_TRFM`: Adds the `ETL_UPDT_DT` column.
    *   **Destination:** `OLEDB_CMD_Update_GC_IND` updates the `DBO.D_GC_VENDOR` table in the `MART_GC_REPORTING` database.

*   **Event Handlers:**
    *   `OnError`: Updates the ETL process status to "Failed" in the `ETL_RUN_STATUS` table.
    *   `OnPostExecute`: Updates the ETL process status to "Succeeded" in the `ETL_RUN_STATUS` table.
    *   `OnPreExecute`: Creates a record with "Running" status in the `ETL_RUN_STATUS` table.

## 4. Code Extraction

```sql
-- From OLEDB_SRC- F_GC_PURCHASE_ORDER
SELECT DISTINCT
		poli.VENDOR_SID								AS VENDOR_SID
	FROM dbo.F_GC_PURCHASE_ORDER					po
	JOIN dbo.F_GC_PURCHASE_ORDER_LINE_ITEM			poli
		on poli.PURCHASE_ORDER_SID = po.PURCHASE_ORDER_SID
	JOIN DBO.F_GC_ACCOUNT_ASSIGNMENTS								aa
		on aa.PO_LINE_ITEM_SID = poli.PO_LINE_ITEM_SID
		and aa.WBS_LEVEL_2_SID <> -3
```

```sql
-- From OLEDB_SRC- TARGETING_VENDOR_SID_W2
SELECT DISTINCT
		w2.TARGETING_VENDOR_SID						AS VENDOR_SID
	FROM dbo.F_GC_WBS_LEVEL_2 w2
```

```sql
-- From OLEDB_SRC-EXECUTING_VENDOR_SID_W2
SELECT DISTINCT
		w2.EXECUTING_VENDOR_SID						AS VENDOR_SID
	FROM dbo.F_GC_WBS_LEVEL_2 w2
```

```sql
-- From OLEDB_CMD_Update_GC_IND
UPDATE DBO.D_GC_VENDOR
SET GC_IND =1
	  ,ETL_UPDT_DT = ?
WHERE VENDOR_SID = ?
```

```sql
-- From OLEDB_SRC-s_gc_project_milestones (inside SEQC_WBS_LEVEL_2_DATE_UPDATES)
SELECT rtrim(m.WBS_NBR) as WBS_NBR,
		max(case when m.STANDARD_MILESTONE_NBR='350' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_START_DT_1,
		max(case when lastm.milestoneID like '%Project Start Date' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_START_DT_2,

		max(case when m.STANDARD_MILESTONE_NBR='350' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_START_DT_1,
		max(case when lastm.milestoneID like '%Project Start Date' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_START_DT_2,

		max(case when m.STANDARD_MILESTONE_NBR='400' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_END_DT_1,
		max(case when lastm.milestoneID like '%End of Imp%' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_END_DT_2,
		max(case when lastm.milestoneID like '%Disb.completed' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_END_DT_3,

		max(case when m.STANDARD_MILESTONE_NBR='400' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_END_DT_1,
		max(case when lastm.milestoneID like '%End of Imp%' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_END_DT_2,
		max(case when lastm.milestoneID like '%Disb.completed' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_END_DT_3,

		max(case when m.STANDARD_MILESTONE_NBR='300' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS  PLANNED_APPROVAL_DATE_300,
		max(case when m.STANDARD_MILESTONE_NBR='300' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_APPROVAL_DATE_300,

		max(case when m.STANDARD_MILESTONE_NBR='330' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS  PLANNED_APPROVAL_DATE_330,
		max(case when m.STANDARD_MILESTONE_NBR='330' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_APPROVAL_DATE_330,

		max(case when lastm.milestoneID like '%Approval' and m.fixed_dt is not null then m.fixed_dt else '1900-01-01' end ) AS PLANNED_APPROVAL_DATE_2,
		max(case when lastm.milestoneID like '%Approval' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS ACTUAL_APPROVAL_DATE_2,

--------------------- NEW ---------------------

		max(case when m.STANDARD_MILESTONE_NBR='610' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS PUBLIC_ANNOUNCE_DATE_610,
		max(case when m.STANDARD_MILESTONE_NBR='620' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS PUBLICATION_DATE_620,
		max(case when m.STANDARD_MILESTONE_NBR='630' and m.actual_dt is not null then m.actual_dt else '1900-01-01' end ) AS PROACTIVE_DISCLOSURE_DATE_630

-- select *
FROM   [dbo].[s_gc_project_milestones] m
-- WHERE  M.STANDARD_MILESTONE_NBR = '610'
	INNER JOIN
		(SELECT WBS_NBR
				, rtrim(m1.standard_milestone_nbr)+ ms.EN_NM as milestoneID
				, max(case when m1.SOURCE_ID='FAS'then '2' else '1' end + m1.MILESTONE_NBR) as maxMS
			FROM   [dbo].[s_gc_project_milestones] m1
				JOIN [dbo].[s_gc_milestone] ms ON ms.milestone_nbr = m1.milestone_nbr and ms.SOURCE_ID=m1.SOURCE_ID
			group by m1.WBS_NBR, rtrim(m1.standard_milestone_nbr)+ ms.EN_NM
        ) lastm
		ON m.WBS_NBR=lastm.WBS_NBR and case when m.SOURCE_ID='FAS'then '2' else '1' end + m.MILESTONE_NBR = lastm.maxMS
group by m.WBS_NBR
```

```sql
-- From OLEDB_SRC-S_D_GC_WBS_LEVEL_2_TMP (inside SEQC_WBS_LEVEL_2_DATE_UPDATES)
select wbs.WBS_NBR ,
 case when PLANNED_START_DT_1 > '1900-01-01' then PLANNED_START_DT_1 else PLANNED_START_DT_2 end as PLANNED_START_DT ,
 case when ACTUAL_START_DT_1 > '1900-01-01' then ACTUAL_START_DT_1 else ACTUAL_START_DT_2 end as ACTUAL_START_DT ,

 case when PLANNED_END_DT_1 > '1900-01-01' then PLANNED_END_DT_1 when PLANNED_END_DT_2 > '1900-01-01' then PLANNED_END_DT_2 else PLANNED_END_DT_3 end as PLANNED_END_DT,
 case when ACTUAL_END_DT_1 > '1900-01-01' then ACTUAL_END_DT_1 when ACTUAL_END_DT_2 > '1900-01-01' then ACTUAL_END_DT_2 else ACTUAL_END_DT_3 end as ACTUAL_END_DT,

 case when PLANNED_APPROVAL_DATE_330 > '1900-01-01' and WBS.[select_mechanism_cd] = 'CIDA003'
		AND Upper(Substring(WBS.wbs_nbr, 8, 10)) <> 'CFP' THEN PLANNED_APPROVAL_DATE_330
	when  PLANNED_APPROVAL_DATE_300 > '1900-01-01' THEN  PLANNED_APPROVAL_DATE_300
	else PLANNED_APPROVAL_DATE_2 end as PLANNED_APPROVAL_DATE,

 case when ACTUAL_APPROVAL_DATE_330 > '1900-01-01' and WBS.[select_mechanism_cd] = 'CIDA003'
		AND Upper(Substring(WBS.wbs_nbr, 8, 10)) <> 'CFP' THEN ACTUAL_APPROVAL_DATE_330
	when  ACTUAL_APPROVAL_DATE_300 > '1900-01-01' THEN  ACTUAL_APPROVAL_DATE_300
	else ACTUAL_APPROVAL_DATE_2 end as ACTUAL_APPROVAL_DATE,

	PUBLIC_ANNOUNCE_DATE_610		as PUBLIC_ANNOUNCE_DT,
	PUBLICATION_DATE_620			as PUBLICATION_DT,
	PROACTIVE_DISCLOSURE_DATE_630	as PROACTIVE_DISCLOSURE_DT,
getdate() as ETL_UPDT_DT
FROM dbo.S_D_GC_WBS_LEVEL_2_TMP dt
	INNER JOIN [dbo].[d_gc_wbs_level_2] WBS on wbs.WBS_NBR = dt.WBS_NBR
```

```sql
-- From OLEDB_DEST-Update_D_GC_WBS_LEVEL_2 (inside SEQC_WBS_LEVEL_2_DATE_UPDATES)
UPDATE [dbo].[D_GC_WBS_LEVEL_2]
   SET [PLANNED_START_DT] = ?
      ,[ACTUAL_START_DT] = ?
      ,[PLANNED_END_DT] = ?
      ,[ACTUAL_END_DT] = ?
      ,[PLANNED_APPROVAL_DATE] = ?
      ,[ACTUAL_APPROVAL_DATE] = ?
      ,[PUBLIC_ANNOUNCE_DT] = ?
      ,[PUBLICATION_DT] = ?
      ,[PROACTIVE_DISCLOSURE_DT] = ?
	  ,ETL_UPDT_DT = ?
 WHERE [WBS_NBR] =?
```

```sql
-- From OLEDB_SRC-F_GC_WBS_MILESTONE (inside SEQC_WBS_LEVEL_2_DATE_UPDATES)
With
cde_MILESTONE as (
	SELECT distinct
		M.WBS_LEVEL_2_SID
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='100'
				then M.[ACTUAL_DT]
			 when M.[MILESTONE_EN_NM]='Initiation/received'
				then M.[ACTUAL_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])			as [100A]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='300'
				then M.[FORECAST_SCHEDULED_DT]
			 when M.[MILESTONE_EN_NM]='Approval'
				then M.[FORECAST_SCHEDULED_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])			as [300P]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='300'
				then M.[ACTUAL_DT]
			 when M.[MILESTONE_EN_NM]='Approval'
				then M.[ACTUAL_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])			as [300A]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='350'
				then M.[FORECAST_SCHEDULED_DT]
			 when M.[MILESTONE_EN_NM]='Début du projet / Project Start Date'
				then M.[FORECAST_SCHEDULED_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])			as [350P]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='350'
				then M.[ACTUAL_DT]
			 when M.[MILESTONE_EN_NM]='Début du projet / Project Start Date'
			 then M.[ACTUAL_DT]
			 else null
			end) over( partition by M.[WBS_LEVEL_2_SID])			as [350A]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='400'
				then M.[FORECAST_SCHEDULED_DT]
			 when M.[MILESTONE_EN_NM]='Proj/Disb.completed'
				then M.[FORECAST_SCHEDULED_DT]
			 else null
			end) over ( partition by M.[WBS_LEVEL_2_SID])				as [400P]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='400'
				then M.[ACTUAL_DT]
			 when M.[MILESTONE_EN_NM]='Proj/Disb.completed'
				then M.[ACTUAL_DT]
			 else null
			end) over (Partition by M.[WBS_LEVEL_2_SID])				as [400A]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='500'
				then M.[FORECAST_SCHEDULED_DT]
			 when M.[MILESTONE_EN_NM]='Final report/closing'
				then M.[FORECAST_SCHEDULED_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])				as [500P]
		,max(
			case
			 when M.[STANDARD_MILESTONE_NBR]='500'
				then M.[ACTUAL_DT]
			 when M.[MILESTONE_EN_NM]='Final report/closing'
				then M.[ACTUAL_DT]
			 else null
			end) over (partition by M.[WBS_LEVEL_2_SID])				as [500A]
	FROM F_GC_WBS_MILESTONE M
	WHERE M.WBS_LEVEL_2_SID is not null
) ,
cde_WORKPLAN as (
	SELECT distinct
		W.WBS_LEVEL_2_SID
		,max(case when W.[MILESTONE_NBR]='100'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[100A]
		,max(case when W.[MILESTONE_NBR]='300'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[300P]
		,max(case when W.[MILESTONE_NBR]='300'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[300A]
		,max(case when W.[MILESTONE_NBR]='330'
			then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[330Pp]
		,max(case when W.[MILESTONE_NBR]='330'
			then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[330Ap]
		,max(case when W.[MILESTONE_NBR]='350'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[350P]
		,max(case when W.[MILESTONE_NBR]='350'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[350A]
		,max(case when W.[MILESTONE_NBR]='310'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[310Pp]
		,max(case when W.[MILESTONE_NBR]='310'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[310Ap]
		,max(case when W.[MILESTONE_NBR]='400'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[400P]
		,max(case when W.[MILESTONE_NBR]='400'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[400A]
		,max(case when W.[MILESTONE_NBR]='500'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[500P]
		,max(case when W.[MILESTONE_NBR]='500'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[500A]
		,max(case when W.[MILESTONE_NBR]='501'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[501P]
		,max(case when W.[MILESTONE_NBR]='501'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[501A]
		,max(case when W.[MILESTONE_NBR]='335'
				then W.[SCHEDULED_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[335Pp]
		,max(case when W.[MILESTONE_NBR]='335'
				then W.[ACTUAL_END_DT]
			else null
			end) over (partition by W.[WBS_LEVEL_2_SID])			[335Ap]
	FROM F_GC_WBS_WORKPLAN W
	WHERE W.WBS_LEVEL_2_SID is not null
),
cde_STATUS as (
 SELECT distinct
	SH.WBS_LEVEL_2_SID
	,min(SH.[WBS_STATUS_DT]) OVER (Partition by SH.[WBS_LEVEL_2_SID])		TENT
	,min(case
		  when SH.[WBS_STATUS_CD]='E0004'
			then SH.[WBS_STATUS_DT]
		  else null
		  end) over (partition by SH.[WBS_LEVEL_2_SID])						OPER
	,min(case
		  when SH.[WBS_STATUS_CD]='E0006'
			then SH.[WBS_STATUS_DT]
		  else null
		  end) over (partition by SH.[WBS_LEVEL_2_SID])						TERM
	, min(case
		  when SH.[WBS_STATUS_CD]='E0005' then SH.[WBS_STATUS_DT]
		  else null
		  end) over (partition by SH.[WBS_LEVEL_2_SID])						CLOS
 FROM F_GC_WBS_STATUS_HISTORY SH
 ),
cde_DATES
as (
	SELECT distinct
		coalesce(W.[WBS_LEVEL_2_SID],M.[WBS_LEVEL_2_SID])				[WBS_LEVEL_2_SID]
		,Coalesce(W.[100A],M.[100A])									[100A]
		,Coalesce(W.[300P],M.[300P])									[300P]
		,Coalesce(W.[300A],M.[300A])									[300A]
		,W.[310Pp]														[310Pp]
		,W.[310Ap]														[310Ap]
		,W.[330Pp]														[330Pp]
		,W.[330Ap]														[330Ap]
		,W.[335Pp]														[335Pp]
		,W.[335Ap]														[335Ap]
		,Coalesce(W.[350P],M.[350P])									[350P]
		,Coalesce(W.[350A],M.[350A])									[350A]
		,Coalesce(W.[400P],M.[400P])									[400P]
		,Coalesce(W.[400A],M.[400A])									[400A]
		,Coalesce(W.[500P],M.[500P])									[500P]
		,Coalesce(W.[500A],M.[500A])									[500A]
		,W.[501P]														[501P]
		,W.[501A]														[501A]
		,W.[100A]														[W101A]
		,W.[300P]														[W300P]
		,W.[300A]														[W300A]
		,W.[350P]														[W350P]
		,W.[350A]														[W350A]
		,W.[400P]														[W400P]
		,W.[400A]														[W400A]
		,W.[500P]														[W500P]
		,W.[500A]														[W500A]
		--,S.TENT															[TENT]
		--,S.OPER															[OPER]
		--,S.TERM															[TERM]
		--,S.CLOS															[CLOS]
	FROM cde_MILESTONE M
	FULL OUTER JOIN cde_WORKPLAN W
		on W.WBS_LEVEL_2_SID = M.WBS_LEVEL_2_SID
	--JOIN cde_STATUS S
	--	on S.WBS_LEVEL_2_SID = W.WBS_LEVEL_2_SID
	--	or S.WBS_LEVEL_2_SID = M.WBS_LEVEL_2_SID
),
cde_DATE_STATUS
as (
	SELECT
		 D.*
		,S.TENT
		,S.OPER
		,S.TERM
		,S.CLOS
	FROM cde_DATES D
	JOIN cde_STATUS S
		on S.WBS_LEVEL_2_SID = D.WBS_LEVEL_2_SID
),
cde_CALL_FOR_PROPOSAL -- pre-calc
as (
SELECT
	 DS.*
	,WBS.WBS_NBR
	,WBS.GCS_WBS_NBR
	,WBS.WBS_STATUS_CD
	,WBS.WBS_STATUS_EN
	,WBS.SELECT_MECHANISM_CD
	,WBS.SELECT_MECHANISM_EN_NM
	,WBS.CFP_TYPE_CD
	--,WBS.WBS_CREATION_DT					-- this will be null at run time
	--,WBS.WBS_APPROVED_DT					-- this will be null at run time
	--,WBS.WBS_IMPLEMENTATION_START_DT		-- this will be null at run time
	--,WBS.WBS_IMPLEMENTATION_END_DT			-- this will be null at run time
	--,WBS.WBS_CLOSURE_DT						-- this will be null at run time
--	,coalesce(DS.[100A],DS.[TENT]) 										[SQL_Creation_Date]
	,case
		 when WBS.CFP_TYPE_CD='P' then DS.[330Pp]
		 else DS.[300P]
		end																[SQLsub Planned Approved Date]
	,coalesce(case
		when  WBS.CFP_TYPE_CD='P' then DS.[330Ap]
		else DS.[300A]
		end
		,
		/* OPER fail safe when workplan/milestone is inexistent when it should exist */
		CASE WHEN (WBS.WBS_STATUS_CD in ('E0004','E0006','E0005','E0023')) then(DS.[OPER])
		else(null)
		end
	)																	[SQLsub Actual Approved Date]
/*  original logic for Planned Implementation Start Date...to be changed Sept 19, 2024 per Guy instructions
	,case
		 when WBS.CFP_TYPE_CD='P'
			then DS.[310Pp]
			else DS.[350P]
		 end															[SQLsub Planned Implementation Start Date]
*/
	,case
		 when WBS.SELECT_MECHANISM_CD = 'CIDA003' and WBS.CFP_TYPE_CD='-3' then DS.[310Pp]
			else DS.[350P]
		 end															[SQLsub Planned Implementation Start Date]
	--,coalesce(case
	--	 when WBS.CFP_TYPE_CD='P'
	--		then DS.[310Ap]
	--	 else DS.[350A]
	--	end

	,coalesce(case
		 when WBS.SELECT_MECHANISM_CD = 'CIDA003' and WBS.CFP_TYPE_CD='-3' then DS.[310Ap]
		else DS.[350A]
		end
		,
		 /* OPER Status fail safe when Pre-APP doesn't have a milestone date for both Début du projet / Project Start Date */
		case when(WBS.WBS_STATUS_CD in ('E0004','E0006','E0005') and WBS.SELECT_MECHANISM_CD='CIDA001')
			then(DS.[OPER])
			else(null)
			end
		)																[SQLsub Actual Implementation Start Date]
		,DS.[400P]														[SQLsub Planned Implementation End Date]
		,/* TERM fail safe when the milestone/workplan doesn't exist for TERM and CLOS statuses */
		case when(DS.[400A] is null and WBS.WBS_STATUS_CD in ('E0006','E0005'))
				then(DS.[TERM])
				else(DS.[400A])
		end																[SQLsub Actual Implementation End Date]
		,case when WBS.CFP_TYPE_CD='P'
			then DS.[335