## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| MART_NEICS           | OLE DB          | Server: @[$Project::PRJ_PRM_TRGT_DB_SRVR], Database: @[$Project::PRJ_PRM_TRGT_REPORTING_DB_NM]  | Source and Destination | Integrated Security=SSPI | @[$Project::PRJ_PRM_TRGT_DB_SRVR], @[$Project::PRJ_PRM_TRGT_REPORTING_DB_NM]            | All                  |
| MART_NEICS 1 | OLE DB |  Server: [Inferred], Database: [Inferred]  | Source for many data flows | Integrated Security=SSPI | None | F_EICS_CTRL_PIT_APP_1A, F_EICS_CTRL_PIT_APP_2/3 and F_EICS_PERMIT_ITEM |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | All|

## 3. Package Flow Analysis

The package `NEICS_Fact.dtsx` is designed to load fact tables within the MART_NEICS database. It truncates existing fact tables and then populates them using data flow tasks. The package also logs ETL status to a table called ETL_RUN_STATUS.

*   **Expression Task:** `EXPRESSIONT- Fact Tables - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` acts as a starting point

*   **Sequence Container:** `SEQC-F_<Fact Table>` which contains the truncate and load operations for each fact table.

#### ESQLT- Truncate &lt;Fact Tables&gt;

This Execute SQL Task truncates a series of fact tables.

*   **SQL Statement:** The task contains a large SQL statement with multiple `TRUNCATE TABLE` commands.

####  DFT- F_EICS_CONTROL_ITEMS

*   **Source:**  `D_EICS_CONTROL_ITEMS Source` extracts data using an embedded SQL query.
*   **Destination:** `F_EICS_CONTROL_ITEMS Destination` loads data into the `dbo.F_EICS_CONTROL_ITEMS` table.

SQL Source Query from D_EICS_CONTROL_ITEMS Source:

```sql
;with cte_control_items -- Testing SourceControl
as  
(
select 
		 ci_stg.CONTROL_ITEM_ID					as CONTROL_ITEM_ID
		 ,ci.CTRL_ITEM_SID						as CONTROL_ITEM_SID	
		 ,c.COMMODITY_SID						as COMMODITY_SID
		 ,loc.LOCATION_SID						as LOCATION_SID
		,isnull(effdate.[DATE_SID], -3)			as CONTROL_ITEM_EFFECTIVE_DATE_SID
		,isnull(expirydate.[DATE_SID], -3)		as CONTROL_ITEM_EXPIRY_DATE_SID

		,isnull(ci_stg.[UTILIZED_LVL], 0)		as UTILIZED_LVL
		,isnull(ci_stg.[TPL_UTILIZED_LVL], 0)	as TPL_UTILIZED_LVL

		,isnull(pi_stg.[PRMT_QTY],0)			as PRMT_QTY
		,isnull(pi_stg.[ALTRNT_QTY],0)			as ALTRNT_QTY
		,isnull(pi_stg.[TRANSFER_QTY],0)		as TRANSFER_QTY
		,isnull(pi_stg.[TPL_TRANSFER_QTY],0) 	as TPL_TRANSFER_QTY
		,isnull(pi_stg.[TOTAL_AMT],0)			as TOTAL_AMT
		,isnull(q1.LAST_YTD_TRANSFER_QTY,0)		as LAST_YTD_TRANSFER_QTY 
		,isnull(LAST_YTD_TPL_TRANSFER_QTY, 0)	as LAST_YTD_TPL_TRANSFER_QTY
FROM [STG_NEICS].[dbo].[S_EICS_CONTROL_ITEMS] ci_stg 
left outer join 
(
	SELECT [CONTROL_ITEM_ID]
		  ,sum([PRMT_QTY])			as [PRMT_QTY]
		  ,sum([ALTRNT_QTY])		as [ALTRNT_QTY]
		  ,sum([TRANSFER_QTY])		as [TRANSFER_QTY]
		  ,sum([TPL_TRANSFER_QTY])	as [TPL_TRANSFER_QTY]
		  ,sum([TOTAL_AMT])			as [TOTAL_AMT]
 	  FROM [STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS] 
	  group by [CONTROL_ITEM_ID]
 )   pi_stg

  	on ci_stg.[CONTROL_ITEM_ID] = pi_stg.[CONTROL_ITEM_ID]


inner join [dbo].[D_EICS_CONTROL_ITEMS]  ci
		on ci.LVL6_CONTROL_ITEM_ID = ci_stg.CONTROL_ITEM_ID
left outer join [dbo].[D_EICS_DATE] effdate 
		on ci.LVL6_CONTROL_ITEM_EFCTV_DT = effdate.DATE_ID
left outer join [dbo].[D_EICS_DATE] expirydate 
		on ci.LVL6_CONTROL_ITEM_EXPIRY_DT = expirydate.DATE_ID
inner join [dbo].[D_EICS_COMMODITY] c 
		on c.[LVL6_CMDTY_ID] = ci.[LVL6_CMDTY_ID]
				and		c.COMMODITY_SID = 					
						(
							Select MAX (c2.COMMODITY_SID)
							from [dbo].[D_EICS_COMMODITY] c2
							WHERE c.[LVL6_CMDTY_ID] = c2.[LVL6_CMDTY_ID]

						)

inner join [dbo].[D_EICS_LOCATIONS] loc on ci.[LVL6_LOCATION_ID] = loc.LOCATION_ID
 
left outer join 
(
SELECT 
	a.[CONTROL_ITEM_ID]
	 ,[LAST_YTD_TRANSFER_QTY] = sum( case 
									  when c.CDN_ENTRY_EXIT_DT 
									  between convert(date,convert(char(4),year(a.CONTROL_ITEM_EFCTV_DT)-1)+'-01-01' )
									  and convert(date,DATEADD(YEAR, -1, getdate())) 
									  then b.[TRANSFER_QTY] 
									  else 0 end )
	 ,[LAST_YTD_TPL_TRANSFER_QTY] = sum( case 
									  when c.CDN_ENTRY_EXIT_DT 
									  between convert(date,convert(char(4),year(a.CONTROL_ITEM_EFCTV_DT)-1)+'-01-01' )
									  and convert(date,DATEADD(YEAR, -1, getdate())) 
									  then b.[TPL_TRANSFER_QTY] 
									  else 0 end )
	FROM [STG_NEICS].[dbo].[S_EICS_CONTROL_ITEMS] a
	join [STG_NEICS].[dbo].[S_EICS_PERMIT_ITEMS] b on a.CONTROL_ITEM_ID = b.CONTROL_ITEM_ID
	join [STG_NEICS].[dbo].[S_EICS_PERMIT_APPLICATIONS] c on b.PRMT_APLCTN_ID = c.PRMT_APLCTN_ID
	group by  a.[CONTROL_ITEM_ID] ) q1
 
on q1.[CONTROL_ITEM_ID] = pi_stg.[CONTROL_ITEM_ID]
--where c.[LVL6_CMDTY_ID] = 5671
)

select  
		cte.CONTROL_ITEM_SID 
		,cte.COMMODITY_SID
		,cte.LOCATION_SID
		,cte.CONTROL_ITEM_EFFECTIVE_DATE_SID
		,cte.CONTROL_ITEM_EXPIRY_DATE_SID
		,cte.UTILIZED_LVL
		,cte.TPL_UTILIZED_LVL
		,cte.PRMT_QTY
		,cte.ALTRNT_QTY
		,cte.TRANSFER_QTY
		,cte.TPL_TRANSFER_QTY
		,cte.TOTAL_AMT
		,cte.LAST_YTD_TRANSFER_QTY
		,LAST_YTD_TPL_TRANSFER_QTY
		,getdate() as [ETL_CREA_DT]
        ,getdate() as [ETL_UPDT_DT]
from cte_control_items cte;
```

#### DFT- F_EICS_CTRL_PIT_APP_1

*   **Source:** `F_EICS_CTRL_PIT_APP_1 Source` extracts data using an embedded SQL query.
*   **Destination:** `F_EICS_CTRL_PIT_APP_1  Destination` loads data into the `dbo.F_EICS_CTRL_PIT_APP_1` table.

SQL Source Query from F_EICS_CTRL_PIT_APP_1 Source:

```sql
--PASS 1

--F_EICS_CTRL_PIT_APP_1 Source dataflow on 29July2024_KR


select  -- select  -- 6,027,689 records inserted in 4 minutes 12 seconds
       CTRL_PIT_APP_SID = 
        concat(
convert(varchar,isnull(PA.[PRMT_APLCTN_SID], -3)), 
convert(varchar,isnull(CI.[CTRL_ITEM_SID], -3)), 
convert(varchar,isnull(P.[PERMIT_SID], -3)), 
convert(varchar,isnull(PIT.[PRMT_ITEM_SID], -3)),
convert(varchar,isnull(CO.COMMODITY_SID,-3))
       )
       ,ISNULL(CI.CTRL_ITEM_SID,-3)                     as [CTRL_ITEM_SID] -- 37 316 distinct records
       ,ISNULL(CO.COMMODITY_SID,-3)                     as CONTROL_COMMODITY_SID  -- changed from CO2.COMMODITY_SID to CO.COMMODITY_SID
       ,isnull(CO2.COMMODITY_SID,-3)                    as [PRMT_ITEM_COMMODITY_SID] -- Changed from CO.COMMODITY_SID to CO2.COMMODITY_SID

-- ADD COLUMN:  COMMODITY_SID  = isnull(CO.COMMODITY_SID,-3)
, isnull(CO.COMMODITY_SID,-3)                                                         as COMMODITY_SID 
       ,isnull(ci.[LVL6_UTILIZED_LVL], 0)                      as UTILIZED_LVL
       ,isnull(ci.[LVL6_TPL_UTILIZED_LVL], 0)                  as  TPL_UTILIZED_LVL

       ,isnull(PIT.[PRMT_ITEM_SID] , -3)                       as [PRMT_ITEM_SID]
       ,isnull(P.[PERMIT_SID], -3)                                    as [PERMIT_SID]
       ,isnull(PA.[PRMT_APLCTN_SID], -3)                       as [PRMT_APLCTN_SID]

       ,isnull(exp_imp_loc.[LOCATION_SID], -3)                 as [EXP_IMP_LOCATION_SID]

       ,isnull(bu_exp_imp.[BUSINESS_SID], -3)                  as [BUSINESS_EXPORT_IMPORT_SID]
       ,isnull(bu_applicant.[BUSINESS_SID], -3)        as [BUSINESS_APPLICANT_SID]
       ,isnull(bu_payment.[BUSINESS_PAYMENTS_SID], -3) as [BUSINESS_PAYMENT_SID]
       ,isnull(pe.PERMIT_EXPORTS_SID, -3)                             as [PERMIT_EXPORTS_SID]
       ,isnull(tp.THIRD_PARTIES_SID, -3)                       as [THIRD_PARTIES_SID]

       ,isnull(CDN_ENTRY_EXIT_DATE.DATE_SID, -3)       as [CDN_ENTRY_EXIT_DATE_SID]
       ,isnull(PERMIT_EFFECTIVE_DATE.DATE_SID, -3)     as [PERMIT_EFFECTIVE_DATE_SID]
       ,isnull(PERMIT_EXPIRY_DATE.DATE_SID, -3)     as [PERMIT_EXPIRY_DATE_SID]
       ,isnull(SHIPMENT_DATE.DATE_SID            , -3)         as [SHIPMENT_DATE_SID]
       ,isnull(PERMIT_DATE.DATE_SID              , -3)         as [PERMIT_DATE_SID]    
       ,isnull(PRMT_APLCTN_SUBMIT.DATE_SID              , -3)  as [PRMT_APLCTN_SUBMIT_DATE_SID] 

       ,isnull(PIT.[PRMT_QTY], 0)                              as [PERMIT_QTY]
       ,isnull(PIT.[ALTRNT_QTY], 0)                            as [PERMIT_ALTRNT_QTY]
       ,isnull(PIT.[TRANSFER_QTY], 0)                          as [PERMIT_TRANSFER_QTY]
       ,isnull(PIT.[TPL_TRANSFER_QTY], 0)               as [PERMIT_TPL_TRANSFER_QTY]
       ,isnull(PIT.[TOTAL_AMT],0)                       as [PERMIT_TOTAL_AMT]
       ,1                                                                              as [ROW_COUNT]
       ,getdate() as [ETL_CREA_DT]
    ,getdate() as [ETL_UPDT_DT] 

from    [dbo].[D_EICS_COMMODITY] CO -- 37 316
inner JOIN [dbo].D_EICS_PERMIT_ITEMS PIT -- changed to Inner Join (no need to return Commoditys with no Permits) 20June2024_KR
-- can we add the qty to the dim and we can hide at reporting?
              -- -- 5,309,552
ON PIT.[COMMODITY_ID] = CO.[LVL6_CMDTY_ID]

-- SQL below removed from F_EICS_CTRL_PIT_APP_1 Source dataflow on 29July2024_KR

                             --and         CO.COMMODITY_SID =                                
                             --            (
                             --                    Select MAX (CO2.COMMODITY_SID)
                             --                    from [dbo].[D_EICS_COMMODITY] Co2
                             --                    WHERE CO.[LVL6_CMDTY_ID] = CO2.[LVL6_CMDTY_ID]

                             --            )
-- SQL above removed from F_EICS_CTRL_PIT_APP_1 Source dataflow on 29July2024_KR


LEFT JOIN  [D_EICS_CONTROL_ITEMS] ci
       on ci.LVL6_CONTROL_ITEM_ID = PIT.[CONTROL_ITEM_ID]
                 AND PIT.[COMMODITY_ID] = CI.[LVL6_CMDTY_ID]

LEFT JOIN [dbo].[D_EICS_COMMODITY] CO2
ON CO2.[LVL6_CMDTY_ID] = CI.[LVL6_CMDTY_ID]

-- SQL below removed from F_EICS_CTRL_PIT_APP_1 Source dataflow on 29July2024_KR
                             --and         CO2.COMMODITY_SID =                              
                             --            (
                             --                    Select MAX (CO2_2.COMMODITY_SID)
                             --                    from [dbo].[D_EICS_COMMODITY] CO2_2
                             --                    WHERE CO2.[LVL6_CMDTY_ID] = CO2_2.[LVL6_CMDTY_ID]

                             --            )
-- SQL above removed from F_EICS_CTRL_PIT_APP_1 Source dataflow on 29July2024_KR


left join            [dbo].[D_EICS_PERMIT_APPLICATIONS] PA -- -- 5,339,553
              on PA.PRMT_APLCTN_ID = PIT.[PRMT_APLCTN_ID]

left join  [dbo].[D_EICS_PERMITS] P  -- 5,339,553
              on P.[PRMT_APLCTN_ID] = PIT.[PRMT_APLCTN_ID]    

----------------------------------------------------------
left outer join [dbo].[D_EICS_LOCATIONS] exp_imp_loc
              on pa.[CDN_ENTRY_EXIT_PORT_ID] = exp_imp_loc.LOCATION_ID
left outer join [dbo].[D_EICS_BUSINESSES] bu_exp_imp
              on pa.EXP_IMP_ID = bu_exp_imp.BUS_ID
left outer join [dbo].[D_EICS_BUSINESS_PAYMENTS] bu_payment
              on pa.[BUS_PYMNT_ID] = bu_payment.[BUS_PYMNT_ID]
left outer join [dbo].[D_EICS_BUSINESSES] bu_applicant
              on pa.[APLCNT_ID] = bu_applicant.[BUS_ID]

left outer join [dbo].[D_EICS_PERMIT_EXPORTS] pe
              on PIT.PRMT_ITEM_ID = pe.PRMT_ITEM_ID
left outer join [dbo].[D_EICS_THIRD_PARTIES] tp
              on PIT.[THIRD_PARTY_LINK_ID] = tp.[Third_Party_Link_Id]

left outer join [dbo].[D_EICS_DATE] CDN_ENTRY_EXIT_DATE
              on cast(PA.CDN_ENTRY_EXIT_DT as date)    = CDN_ENTRY_EXIT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_EFFECTIVE_DATE
              on CAST(P.[PRMT_EFCTV_DT] as date)               = PERMIT_EFFECTIVE_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_EXPIRY_DATE
              on cast(P.[PRMT_EXPIRY_DT] as date)              = PERMIT_EXPIRY_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] SHIPMENT_DATE
              on cast(PIT.[SHIPMENT_DATE] as date)= SHIPMENT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_DATE
              on cast(P.[PRMT_DT] as date)= PERMIT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PRMT_APLCTN_SUBMIT
              on cast(PA.PRMT_APLCTN_SUBMIT_DT as date)= PRMT_APLCTN_SUBMIT.DATE_ID
--where co.LVL6_CMDTY_ID in (15049, 19122)
       --     where PRMT_ITEM_SID = 2720951

          --where co.COMMODITY_SID in (214, 215) – test record
```

#### DFT- F_EICS_CTRL_PIT_APP_1A

*   **Source:** `F_EICS_CTRL_PIT_APP_1A Source` extracts data using an embedded SQL query.
*   **Destination:** `F_EICS_CTRL_PIT_APP_1A Destination` loads data into the `dbo.F_EICS_CTRL_PIT_APP_1A` table.

SQL Source Query from F_EICS_CTRL_PIT_APP_1A Source:

```sql
---PASS  2

select -- 1 084 317 rows inserted in 38 seconds
                CTRL_PIT_APP_SID = 
                             concat(
                             convert(varchar,isnull(PA.[PRMT_APLCTN_SID], -3)), 
                             convert(varchar,isnull(DCI.[CTRL_ITEM_SID], -3)), 
                             convert(varchar,isnull(P.[PERMIT_SID], -3)), 
                             convert(varchar,isnull(PI.[PRMT_ITEM_SID], -3)),
                                                                           convert(varchar,isnull(CO.COMMODITY_SID, -3))
                             )
                ,[CTRL_ITEM_SID] = isnull(DCI.CTRL_ITEM_SID, -3)
                ,[CONTROL_COMMODITY_SID] = isnull(CO.COMMODITY_SID, -3)
                ,[PRMT_ITEM_COMMODITY_SID] =  isnull(CO2.COMMODITY_SID,-3)

                ,COMMODITY_SID                           =   isnull(CO.COMMODITY_SID,-3)         

           
                ,isnull(DCI.[LVL6_UTILIZED_LVL], 0)                  as UTILIZED_LVL
                             ,isnull(DCI.[LVL6_TPL_UTILIZED_LVL], 0)              as  TPL_UTILIZED_LVL


                ,[PRMT_ITEM_SID]= isnull(PI.[PRMT_ITEM_SID], -3)
                ,[PERMIT_SID]= isnull(p.[PERMIT_SID], -3)
                ,[PRMT_APLCTN_SID] = isnull(pa.[PRMT_APLCTN_SID], -3)


                ,[EXP_IMP_LOCATION_SID] =isnull(exp_imp_loc.[LOCATION_SID], -3)

                ,[BUSINESS_EXPORT_IMPORT_SID] = isnull(bu_exp_imp.[BUSINESS_SID], -3)
                ,[BUSINESS_APPLICANT_SID] = isnull(bu_applicant.[BUSINESS_SID], -3)
                ,[BUSINESS_PAYMENT_SID] = isnull(bu_payment.[BUSINESS_PAYMENTS_SID], -3)
                ,[PERMIT_EXPORTS_SID] = isnull(pe.PERMIT_EXPORTS_SID, -3)
                ,[THIRD_PARTIES_SID] = isnull(tp.THIRD_PARTIES_SID, -3)

                ,[CDN_ENTRY_EXIT_DATE_SID] = isnull(CDN_ENTRY_EXIT_DATE.DATE_SID, -3)
                ,[PERMIT_EFFECTIVE_DATE_SID] = isnull(PERMIT_EFFECTIVE_DATE.DATE_SID, -3)
                ,[PERMIT_EXPIRY_DATE_SID] = isnull(PERMIT_EXPIRY_DATE.DATE_SID, -3)
                ,[SHIPMENT_DATE_SID] = isnull(SHIPMENT_DATE.DATE_SID, -3)
                ,[PERMIT_DATE_SID] = isnull(PERMIT_DATE.DATE_SID, -3)        
                ,[PRMT_APLCTN_SUBMIT_DATE_SID] = isnull(PRMT_APLCTN_SUBMIT.DATE_SID, -3)                        

                ,[PERMIT_QTY]  = isnull(PI.[PRMT_QTY], 0)
                ,[PERMIT_ALTRNT_QTY] = isnull(PI.[ALTRNT_QTY], 0)
                ,[PERMIT_TRANSFER_QTY] = isnull(PI.[TRANSFER_QTY], 0)
                ,[PERMIT_TPL_TRANSFER_QTY] = isnull(PI.[TPL_TRANSFER_QTY], 0)
                ,[PERMIT_TOTAL_AMT] =isnull(PI.[TOTAL_AMT],0)

                ,[ROW_COUNT] = 1
                ,[ETL_CREA_DT] = getdate()
                ,[ETL_UPDT_DT] = getdate()

FROM [dbo].[D_EICS_COMMODITY] CO                   --37,316

LEFT JOIN [dbo].[D_EICS_CONTROL_ITEMS] DCI    --386,250         
ON co.LVL6_CMDTY_ID = DCI.[LVL6_CMDTY_ID]

-- SQL below removed from F_EICS_CTRL_PIT_APP_1A Source dataflow on 29July2024_KR
                             --and         CO.COMMODITY_SID =                                
                             --            (
                             --                    Select MAX (CO2.COMMODITY_SID)
                             --                    from [dbo].[D_EICS_COMMODITY] CO2
                             --                    WHERE CO.[LVL6_CMDTY_ID] = CO2.[LVL6_CMDTY_ID]

                             --            )

LEFT JOIN [dbo].[D_EICS_PERMIT_ITEMS] PI          -- 878,081           
ON DCI.LVL6_CONTROL_ITEM_ID = PI.CONTROL_ITEM_ID
and DCI.LVL6_CMDTY_ID = pi.COMMODITY_ID

LEFT JOIN [dbo].[D_EICS_COMMODITY] CO2
ON PI.COMMODITY_ID =  co2.LVL6_CMDTY_ID

-- SQL below removed from F_EICS_CTRL_PIT_APP_1A Source dataflow on 29July2024_KR
                             --and         CO2.COMMODITY_SID =                              
                             --            (
                             --                    Select MAX (CO2_2.COMMODITY_SID)
                             --                    from [dbo].[D_EICS_COMMODITY] CO2_2
                             --                    WHERE CO2.[LVL6_CMDTY_ID] = CO2_2.[LVL6_CMDTY_ID]

                             --            )

LEFT JOIN [dbo].[D_EICS_PERMIT_APPLICATIONS] PA     --  878,081 
ON PI.[PRMT_APLCTN_ID] =  PA.[PRMT_APLCTN_ID]

LEFT JOIN [dbo].[D_EICS_PERMITS] P                  --  878,081 
ON P.[PRMT_APLCTN_ID] = PA.PRMT_APLCTN_ID

-------------------------------------------------------------
left outer join [dbo].[D_EICS_LOCATIONS] exp_imp_loc
                                on pa.[CDN_ENTRY_EXIT_PORT_ID] = exp_imp_loc.LOCATION_ID
left outer join [dbo].[D_EICS_PERMIT_EXPORTS] pe
                                on PI.PRMT_ITEM_ID = pe.PRMT_ITEM_ID
left outer join [dbo].[D_EICS_THIRD_PARTIES] tp
                                on PI.[THIRD_PARTY_LINK_ID] = tp.[Third_Party_Link_Id]
left outer join [dbo].[D_EICS_BUSINESSES] bu_exp_imp

                                on pa.EXP_IMP_ID = bu_exp_imp.BUS_ID
left outer join [dbo].[D_EICS_BUSINESS_PAYMENTS] bu_payment
              on pa.[BUS_PYMNT_ID] = bu_payment.[BUS_PYMNT_ID]

left outer join [dbo].[D_EICS_BUSINESSES] bu_applicant
                                on pa.[APLCNT_ID] = bu_applicant.[BUS_ID]

left outer join [dbo].[D_EICS_DATE] CDN_ENTRY_EXIT_DATE
                                on cast(pa.CDN_ENTRY_EXIT_DT as date)              = CDN_ENTRY_EXIT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_EFFECTIVE_DATE
                                on CAST(p.[PRMT_EFCTV_DT] as date)                    = PERMIT_EFFECTIVE_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_EXPIRY_DATE
                                on cast(p.[PRMT_EXPIRY_DT] as date)    = PERMIT_EXPIRY_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] SHIPMENT_DATE
                                on cast(PI.[SHIPMENT_DATE] as date)= SHIPMENT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PERMIT_DATE
                                on cast(p.[PRMT_DT] as date)= PERMIT_DATE.DATE_ID
left outer join [dbo].[D_EICS_DATE] PRMT_APLCTN_SUBMIT
                                on cast(pa.PRMT_APLCTN_SUBMIT_DT as date)= PRMT_APLCTN_SUBMIT.DATE_ID
```

#### DFT- F_EICS_CTRL_PIT_APP_2

*   **Source:** `F_EICS_CTRL_PIT_APP_2 Source` extracts data using an embedded SQL query.
*   **Destination:** `F_EICS_CTRL_PIT_APP_2 Destination` loads data into the `dbo.F_EICS_CTRL_PIT_APP_2` table

SQL Source Query from F_EICS_CTRL_PIT_APP_2 Source:

```sql
---PASS  2

select *
from [dbo].[F_EICS_CTRL_PIT_APP_1A] cte
	WHERE not exists (
 		SELECT * FROM [dbo].[F_EICS_CTRL_PIT_APP_1] one
			where cte.CTRL_ITEM_SID = one.CTRL_ITEM_SID
			)
;
```

#### DFT- F_EICS_CTRL_PIT_APP_3

*   **Source:** `F_EICS_CTRL_PIT_APP_3 Source` extracts data using an embedded SQL query.
*   **Destination:** `F_EICS_CTRL_PIT_APP_3 Destination` loads data into the `dbo.F_EICS_CTRL_PIT_APP_3` table.

SQL Source Query from F_EICS_CTRL_PIT_APP_3 Source:

```sql
--PASS 3

with cte
as
(
select --count(*)    1114 rows inserted in 20 seconds
	 CTRL_PIT_APP_SID = 
	 concat(
		convert(varchar,isnull(PA.[PRMT_APLCTN_SID], -3)), 
		convert(varchar,isnull(DCI.[CTRL_ITEM_SID], -3)), 
		convert(varchar,isnull(P.[PERMIT_SID], -3)), 
		convert(varchar,isnull(PIT.[PRMT_ITEM_SID], -3)),
                                     convert(varchar,isnull(CO.COMMODITY_SID, -3))
	)
	,-3								as [CTRL_ITEM_SID]
	,-3								as CONTROL_COMMODITY_SID
	,isnull(CO.COMMODITY_SID,-3)	as [PRMT_ITEM_COMMODITY_SID]


                   , isnull(CO.COMMODITY_SID,-3)  as COMMODITY_SID  

	, 0				as UTILIZED_LVL
	, 0			                  as TPL_UTILIZED_LVL

	,isnull(PIT.[PRMT_ITEM_SID] , -3)				as [PRMT_ITEM_SID]
	,isnull(P.[PERMIT_SID], -3)						as [PERMIT_SID]
	,isnull(PA.[PRMT_APLCTN_SID], -3) 				as [PRMT_APLCTN_SID]


	,[EXP_IMP_LOCATION_SID] = isnull(exp_imp_loc.[LOCATION_SID], -3)

	,[BUSINESS_EXPORT_IMPORT_SID] = isnull(bu_exp_imp.[BUSINESS_SID], -3)
	,[BUSINESS_APPLICANT_SID] = isnull(bu_applicant.[BUSINESS_SID], -3)
	,[BUSINESS_PAYMENT_SID] = isnull(bu_payment.[BUSINESS_PAYMENTS_SID], -3)
	,[PERMIT_EXPORTS_SID] = isnull(pe.PERMIT_EXPORTS_SID, -3)
	,[THIRD_PARTIES_SID] = isnull(tp.THIRD_PARTIES_SID, -3)

	,[CDN_ENTRY_EXIT_DATE_SID] = isnull(CDN_ENTRY_EXIT_DATE.DATE_SID, -3)
	,[PERMIT_EFFECTIVE_DATE_SID] = isnull(PERMIT_EFFECTIVE_DATE.DATE_SID, -3)
	,[PERMIT_EXPIRY_DATE_SID] = isnull(PERMIT_EXPIRY_DATE.DATE_SID, -3)
	,[SHIPMENT_DATE_SID] = isnull(SHIPMENT_DATE.DATE_SID, -3)
	,[PERMIT_DATE_SID] = isnull(PERMIT_DATE.DATE_SID, -3)		
	,[PRMT_APLCTN_SUBMIT_DATE_SID] = isnull(PRMT_APLCTN_SUBMIT.DATE_SID, -3)                        

	,[PERMIT_QTY]  = isnull(PI.[PRMT_QTY], 0)
	,[PERMIT_ALTRNT_QTY] = isnull(PI.[ALTRNT_QTY], 0)
	,[PERMIT_TRANSFER_QTY] = isnull(PI.[TRANSFER_QTY], 0)
	,[PERMIT_TPL_TRANSFER_QTY] = isnull(PI.[TPL_TRANSFER_QTY], 0)
	,[PERMIT_TOTAL_AMT] = isnull(PI.[TOTAL_AMT],0)

	,[ROW_COUNT] = 1
	,[ETL_CREA_DT] = getdate()
	,[ETL_UPDT_DT] = getdate()

FROM [dbo].[D_EICS_PERMIT_APPLICATIONS] PA
		
left join [dbo].[D_EICS_PERMITS] P
		on PA.PRMT_APLCTN_ID = P.[PRMT_APLCTN_ID]
		and P.PERMIT_SID  &lt;&gt; -3
		and PA.PRMT_APLCTN_SID  &lt;&gt; -3

left join [dbo].D_EICS_PERMIT_ITEMS PIT 
		on P.[PRMT_APLCTN_ID] = PIT.[PRMT_APLCTN_ID]
		and PIT.PRMT_ITEM_SID  &lt;&gt; -3 

LEFT JOIN [dbo].[D_EICS_COMMODITY] CO
ON PIT.[COMMODITY_ID] = CO.[LVL6_CMDTY_ID]
				and		CO.COMMODITY_SID = 					
						(
							Select MAX (CO2.COMMODITY_SID)
							from [dbo].[D_EICS_COMMODITY] Co2
							WHERE CO.[LVL6_CMDTY_ID] = CO2.[LVL6_CMDTY_ID]
						)
----------------------------------------------------------
left outer join [dbo].[D_EICS_LOCATIONS] exp_imp_loc
                                on pa.[CDN_ENTRY_EXIT_PORT_ID] = exp_imp_loc.LOCATION_ID
left outer join [dbo].[D_EICS_PERMIT_EXPORTS] pe
                                on PI.PRMT_ITEM_ID