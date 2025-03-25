```markdown
## 1. Input Connection Analysis

| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| FC_Staging_TRGT           | OLE DB          | Server=[Inferred], Database: [Inferred], Integrated Security=SSPI  | Staging and destination for data from source | Integrated security | None            | Part 1, 2, 3                  |
| DFAIT_Staging_SRC           | OLE DB          | Server=[Inferred], Database: [Inferred], Integrated Security=SSPI  | Source for Currency Code | Integrated security | None            | Part 1, 2                  |
| SAP_SOURCE_SRC            | OLE DB          | Server=[Inferred], Database: [Inferred], Integrated Security=SSPI  | Source for region code and other data | Integrated security | None            | Part 1, 3                  |
| FC_Reporting           | OLE DB          | Server=[Inferred], Database: [Inferred]  | Used as a destination for transformed data.  It appears to be a reporting database. |  Requires appropriate database permissions (e.g., `INSERT`, `UPDATE`) for the user account used by the connection. | None apparent from the snippet. | Part 2                  |

## 2. Package Dependencies

| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|

## 3. Package Flow Analysis

The package starts by executing tasks in parallel, `SEQC_1_3_DFT-S3_FC_MASTER_NEW` and `SEQC_1_S_FC_HIERARCHY_NEW`. `SEQC_1_4_DFT-D_COMMON_FUND_CENTRE` executes after `EXPRESSIONT- Dimension - Start Task - Each branch depends on value in package parameter - ProcessDataFlowNode` and before `SEQC_1_3_DFT-S3_FC_MASTER_NEW`.

### SEQC_1_4_DFT-D_COMMON_FUND_CENTRE

*   Truncates tables `S_COMMON_FUND` and `R_COMMON_FUND` using `ESQLT-S_TRUNCATE_TABLE_COMMON_FUND` and `ESQLT-R_TRUNCATE_TABLE_COMMON_FUND` respectively.
*   Executes a data flow task `DFT-D_COMMON_FUND_CENTRE`.
*   Executes a sequence container `SEQC_1_5_DFT-S2_FC_GROUPS`

### DFT-D_COMMON_FUND_CENTRE

*(Details of this data flow are not provided in the snippet)*

### SEQC_1_5_DFT-S2_FC_GROUPS

*   Truncates tables `S2_FC_GROUPS` and `R_FC_GROUPS` using `ESQLT-S_TRUNCATE_TABLE_S2_FC_GROUPS` and `ESQLT-TRUNCATE_TABLE_R_FC_GROUPS` respectively.
*   Executes a data flow task `DFT-S2_FC_GROUPS` which extracts and transforms data from `dbo.S_FC_HIERARCHY_3` and loads it into `dbo.S2_FC_GROUPS`.
*   Executes a data flow task `DFT-R_FC_GROUPS` which *(details of this dataflow is missing in snippet)*

#### DFT-S2_FC_GROUPS

*   **Source:** `OLEDB_SRC-S3_HIERARCHY` extracts data from `dbo.S_FC_HIERARCHY_3` using this query:

    ```sql
    SELECT distinct
    "SETNAME" AS FC_GROUPNAME,
    "SETNAME_LEVEL2" AS SUBGROUP_LEVEL1,
    "SETNAME_LEVEL3" AS SUBGROUP_LEVEL2,
    "SETNAME_LEVEL4" AS FUND_CENTRE
     FROM "dbo"."S_FC_HIERARCHY_3"
     where isnumeric(substring("SETNAME_LEVEL2",1,1)) = 0
    ```

*   **Transformation:** A `Derived Column` transformation `DRVC-CREA_UPDT_DT` adds two new columns:
    *   `ETL_CREA_DT`:  `GETDATE()`
    *   `ETL_UPDT_DT`:  `GETDATE()`
*   **Destination:**  `OLEDB_DEST-S2_FC_GROUPS` loads the transformed data into the `[dbo].[S2_FC_GROUPS]` table.

### DFT-R_FC_GROUPS

*(Details of this data flow are not provided in the snippet)*

### SEQC_1_S_FC_HIERARCHY_NEW

*   Truncates tables using `ESQLT-TRUNCATE_TABLES`.
*   Executes data flow task `DFT-1_1_S_FC_HIERARCHY_NEW` which extracts and transforms data and loads it into `dbo.S_FC_HIERARCHY_NEW`.
*   Executes data flow task `DFT-1_3_S2_FC_MASTER_NEW` which extracts and transforms data and loads it into `dbo.S2_FC_MASTER_NEW`.
*   Executes sequence container `SEQC_1_2_DFT-S_FC_MASTER_NEW` which does additional processing on `S_FC_MASTER_NEW`.

#### DFT-1_1_S_FC_HIERARCHY_NEW

This data flow manages the FC Hierarchy data with multiple sources and transformations. It is structured to handle English and French descriptions for different levels.

*   **Sources:** `OLEDB_SRC-FC_LVL1_Source_En`, `OLEDB_SRC-FC_LVL1_Source_Fr`, `OLEDB_SRC-FC_LVL2_Source_En`, `OLEDB_SRC-FC_LVL2_Source_Fr`, `OLEDB_SRC-FC_LVL3_Source_En`, `OLEDB_SRC-FC_LVL3_Source_Fr`, `OLEDB_SRC-FC_LVL4_Source_En`, `OLEDB_SRC-FC_LVL4_Source_Fr`, `OLEDB_SRC-FC_LVL5_Source_En`, `OLEDB_SRC-FC_LVL5_Source_Fr` , `OLEDB_SRC-Level6_EN`, `OLEDB_SRC-Level6_FR`, `OLEDB_SRC-Level7_EN`, `OLEDB_SRC-Level7_FR` - all of these are used to extract data for different levels of FC Hierachy and in different languages
*   **Transformations:** `MRG_TRFM_Desc_En_Fr_Lvl1` through `MRG_TRFM_Desc_En_Fr_Lvl7` (Merge Join), `DRVC_TRFM_Lvl1` through `DRVC_TRFM_Lvl7` (Derived Column),  `MLTCAST_TRFM-Lvl1` through `MLTCAST_TRFM-Lvl6`, `SORT_TRFM_Lvl2` through `SORT_TRFM_Lvl7` and a `UNIONALL_TRFM` are used to merge and transform data.
*   **Destination:**  `OLEDB_DEST-S_FC_HIERARCHY_NEW` loads the transformed data into the `[dbo].[S_FC_HIERARCHY_NEW]` table.

The pattern involves extracting data for each level (1-7) in both English and French, merging the descriptions using `Merge Join` transformations, and then using a `Derived Column` transformation to create the final set of columns for the output table. Finally, the `Union All` transformation merges the data from all the levels and loads it into the destination table. The `Multicast` transforms are used to create copies of the data for different branches of the data flow.

#### DFT-1_3_S2_FC_MASTER_NEW

This data flow is used load data into `dbo.S2_FC_MASTER_NEW` table

*   **Source:** `OLEDB_SRC-S_FC_MASTER_NEW` extracts data from `dbo.S_FC_MASTER_NEW` using the following query:

    ```sql
    SELECT	cast(FUND_CENTRE_CD as int) as "FC_SID",
           FC_SYMBOL,
    	right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) as FUND_CENTRE_CD,
    	"DEFAULT_CURRENCY_CODE",
    	"FC_SDESC_EN",
    	"FC_SDESC_FR",
    	right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ' - ' + rtrim(coalesce(FC_SDESC_EN,'')) as FC_LDESC_EN,
    	right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ' - ' + rtrim(coalesce(FC_SDESC_FR,'')) as FC_LDESC_FR,
        CASE when FC_SYMBOL is NULL then '('+ right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ') ' + rtrim(coalesce(FC_SDESC_EN,'')) 
    		else FC_SYMBOL + '(' + right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ') ' + rtrim(coalesce(FC_SDESC_EN,'')) end as FC_SYMBOL_DESC_EN,
        CASE when FC_SYMBOL is NULL then '('+ right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ') ' + rtrim(coalesce(FC_SDESC_FR,'')) 
    		else FC_SYMBOL + '(' + right(rtrim(('00000' + "FUND_CENTRE_CD")), 5) + ') ' + rtrim(coalesce(FC_SDESC_FR,'')) end as FC_SYMBOL_DESC_FR,
           right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) as LEVEL7_CD,
    	"LEVEL7_SDESC_EN",
    	"LEVEL7_SDESC_FR",
    	CASE when LEVEL7_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL7_SDESC_EN,'')) end as LEVEL7_LDESC_EN,
       	CASE when LEVEL7_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL7_SDESC_FR,'')) end as LEVEL7_LDESC_FR,
        CASE when LEVEL7_CD is null then null
            when LEVEL7_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL7_SDESC_EN,''))
    		else LEVEL7_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL7_SDESC_EN,'')) end as LEVEL7_SYMBOL_DESC_EN,
        CASE when LEVEL7_CD is null then null
            when LEVEL7_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL7_SDESC_FR,''))
    		else LEVEL7_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL7_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL7_SDESC_FR,'')) end as LEVEL7_SYMBOL_DESC_FR,
           right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) as LEVEL6_CD,
    	"LEVEL6_SDESC_EN",
    	"LEVEL6_SDESC_FR",
    	CASE when LEVEL6_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL6_SDESC_EN,'')) end as LEVEL6_LDESC_EN,
       	CASE when LEVEL6_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL6_SDESC_FR,'')) end as LEVEL6_LDESC_FR,
        CASE when LEVEL6_CD is null then null
            when LEVEL6_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL6_SDESC_EN,''))
    		else LEVEL6_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL6_SDESC_EN,'')) end as LEVEL6_SYMBOL_DESC_EN,
        CASE when LEVEL6_CD is null then null
            when LEVEL6_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL6_SDESC_FR,''))
    		else LEVEL6_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL6_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL6_SDESC_FR,'')) end as LEVEL6_SYMBOL_DESC_FR,
           right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) as LEVEL5_CD,
    	"LEVEL5_SDESC_EN",
    	"LEVEL5_SDESC_FR",
    	CASE when LEVEL5_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL5_SDESC_EN,'')) end as LEVEL5_LDESC_EN,
       	CASE when LEVEL5_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL5_SDESC_FR,'')) end as LEVEL5_LDESC_FR,
        CASE when LEVEL5_CD is null then null
            when LEVEL5_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL5_SDESC_EN,''))
    		else LEVEL5_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL5_SDESC_EN,'')) end as LEVEL5_SYMBOL_DESC_EN,
        CASE when LEVEL5_CD is null then null
            when LEVEL5_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL5_SDESC_FR,''))
    		else LEVEL5_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL5_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL5_SDESC_FR,'')) end as LEVEL5_SYMBOL_DESC_FR,
    	right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) as LEVEL4_CD,
    	"LEVEL4_SDESC_EN",
    	"LEVEL4_SDESC_FR",
    	CASE when LEVEL4_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL4_SDESC_EN,'')) end as LEVEL4_LDESC_EN,
       	CASE when LEVEL4_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL4_SDESC_FR,'')) end as LEVEL4_LDESC_FR,
        CASE when LEVEL4_CD is null then null
            when LEVEL4_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL4_SDESC_EN,''))
    		else LEVEL4_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL4_SDESC_EN,'')) end as LEVEL4_SYMBOL_DESC_EN,
        CASE when LEVEL4_CD is null then null
            when LEVEL4_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL4_SDESC_FR,''))
    		else LEVEL4_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL4_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL4_SDESC_FR,'')) end as LEVEL4_SYMBOL_DESC_FR,
    	right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) as LEVEL3_CD,
    	"LEVEL3_SDESC_EN",
    	"LEVEL3_SDESC_FR",
    	CASE when LEVEL3_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL3_SDESC_EN,'')) end as LEVEL3_LDESC_EN,
       	CASE when LEVEL3_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL3_SDESC_FR,'')) end as LEVEL3_LDESC_FR,
        CASE when LEVEL3_CD is null then null
            when LEVEL3_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL3_SDESC_EN,''))
    		else LEVEL3_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL3_SDESC_EN,'')) end as LEVEL3_SYMBOL_DESC_EN,
        CASE when LEVEL3_CD is null then null
            when LEVEL3_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL3_SDESC_FR,''))
    		else LEVEL3_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL3_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL3_SDESC_FR,'')) end as LEVEL3_SYMBOL_DESC_FR,
    	right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) as LEVEL2_CD,
    	"LEVEL2_SDESC_EN",
    	"LEVEL2_SDESC_FR",
    	CASE when LEVEL2_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL2_SDESC_EN,'')) end as LEVEL2_LDESC_EN,
       	CASE when LEVEL2_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL2_SDESC_FR,'')) end as LEVEL2_LDESC_FR,
        CASE when LEVEL2_CD is null then null
            when LEVEL2_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL2_SDESC_EN,''))
    		else LEVEL2_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL2_SDESC_EN,'')) end as LEVEL2_SYMBOL_DESC_EN,
        CASE when LEVEL2_CD is null then null
            when LEVEL2_SYMBOL is null then '(' + right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL2_SDESC_FR,''))
    		else LEVEL2_SYMBOL + '(' + right(('00000' + RTRIM(LTRIM("LEVEL2_CD"))), 5) + ') ' + rtrim(coalesce(LEVEL2_SDESC_FR,'')) end as LEVEL2_SYMBOL_DESC_FR,
    	right(('00000' + RTRIM(LTRIM("LEVEL1_CD"))), 5) as LEVEL1_CD,
    	"LEVEL1_SDESC_EN",
    	"LEVEL1_SDESC_FR",
    	CASE when LEVEL1_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL1_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL1_SDESC_EN,'')) end as LEVEL1_LDESC_EN,
       	CASE when LEVEL1_CD is null then null
    		else right(('00000' + RTRIM(LTRIM("LEVEL1_CD"))), 5) + ' - ' + rtrim(coalesce(LEVEL1_SDESC_FR,'')) end as LEVEL1_LDESC_FR,
    	"LEVEL",
    	"COMPANY_CODE",
    "LEVEL7_SYMBOL",
    "LEVEL6_SYMBOL",
    "LEVEL5_SYMBOL",
    "LEVEL4_SYMBOL",
    "LEVEL3_SYMBOL",
    "LEVEL2_SYMBOL",
    RTRIM(LTRIM(REGION_CD)) as REGION_CD,
    HR_REGION as HR_REGION_CD,
    PAC,
    DEPT_ID,
    "PAC_SDESC_EN",
    "PAC_SDESC_FR",
    "PAC_LDESC_FR",
    "PAC_LDESC_EN",
    CASE when RTRIM(LTRIM(REGION_CD)) is null then 'H' 
    	when RTRIM(LTRIM(REGION_CD)) in ('ON','QC','') then 'H'
    	when RTRIM(LTRIM(REGION_CD)) = 'ZZ' then 'M'
    	else 'O' end as HQ_MISSION_CD,
    
    	"Create_Date",
    	"Last_Update_Date",
    	"Record_Identity"
    FROM   "dbo"."S_FC_MASTER_NEW"
    ```

*   **Transformation:** A `Derived Column` transformation adds two new columns:
    *   `ETL_CREA_DT`:  `GETDATE()`
    *   `ETL_UPDT_DT`:  `GETDATE()`
*   **Destination:**  `OLEDB_DEST-S2_FC_MASTER_NEW` loads the transformed data into the `[dbo].[S2_FC_MASTER_NEW]` table.

### SEQC_1_2_DFT-S_FC_MASTER_NEW

This sequence container performs additional transformations and data loading related to the S_FC_MASTER_NEW table.

*   Truncates the `S_FC_MASTER_NEW` table using `ESQLT-TRUNCATE_S_FC_MASTER_NEW`.
*   Executes data flow `DFT-S_FC_MASTER_NEW` which extracts and transforms data.

    #### DFT-S_FC_MASTER_NEW

    *   **Source:** `OLEDB_SRC-W1_HR_DEPT_FUND_CENTRE` extracts data using the following query:

        ```sql
        ;with Max_SYM as (
        SELECT
        	Max(g9_fc_symbol_id) over(partition by G9_FUND_CENTER order by G9_FUND_CENTER) as Max_symbol,
        	CAST("G9_FUND_CENTER" as INTEGER) as G9_FUND_CENTER,
        	"G9_FUND_CENTER" as FUND_CENTRE,
        	"FC_SYMBOL"
        FROM   dbo."S_FC_FIN_HR_SYMBOLS"
        )
        
        , HR_SYMBOL as (
        select distinct
        a.G9_FUND_CENTER,
        a.FC_SYMBOL
        FROM   dbo."S_FC_FIN_HR_SYMBOLS" a join Max_SYM b on a.G9_FUND_CENTER = b.fund_centre
        where a.g9_fc_symbol_id = b.Max_symbol
        )
        
        ,Max_HR_REG as (
        select distinct
        "G9_FUND_CENTRE",
        max("EFF_DT") over(partition by G9_FUND_CENTRE order by G9_FUND_CENTRE) as EFF_DT,
        max("DEPT_ID") over(partition by G9_FUND_CENTRE order by G9_FUND_CENTRE) as DEPT_ID
         FROM   "dbo"."W1_HR_DEPT_FUND_CENTRE"
        ) 
        
        
        ,HR_REGION as (
        SELECT	a."DEPT_ID",
        	a."EFF_DT",
        	"EFF_END_DT",
        	"DESCRSHORT",
        	"LOCATION_CD",
        	a."G9_FUND_CENTRE"
        FROM   "dbo"."W1_HR_DEPT_FUND_CENTRE" a join Max_HR_REG b on a.G9_FUND_CENTRE = b.G9_FUND_CENTRE and a.EFF_DT = b.EFF_DT and a.DEPT_ID = b.DEPT_ID
        where eff_end_dt is null or eff_end_dt >= getdate()
        )
        
        
        ,PAC_DIM as (
        SELECT CASE WHEN FC_InputLvl_Id='PPT' THEN '22222'
                    WHEN FC_InputLvl_Id='DFAIT' THEN '11111'
               ELSE  FC_InputLvl_Id END as Fund_Centre,
        
               substring(b."SETNAME",5,2) as "PAC",
               b."VALFROM",
               b."VALTO",
               "PAC_DESCR_EN",
               "PAC_DESCR_FR"
        
        FROM   "dbo"."S_FC_HIERARCHY" a,
               "dbo"."S_FC_SETLEAF_PAC" b,
               "dbo"."S_FC_PAC" c
        
        WHERE  a."FC_InputLvl_Id" >= b."VALFROM"
        and    a."FC_InputLvl_Id" <= b."VALTO"
        and substring(b."SETNAME",5,2) = c.PAC_CD
        )
        
        ,PAC_Distinct as (
        SELECT distinct FUND_CENTRE,
        MIN(PAC) over (partition by fund_centre order by PAC) as PAC
        from PAC_DIM
        )
        
        , PAC as (
        Select
        a.Fund_Centre,
        a.PAC,
        a.PAC_DESCR_EN,
        a.PAC_DESCR_FR
        from PAC_DIM a join PAC_Distinct b on a.Fund_Centre = b.Fund_Centre and a.PAC = b.PAC
        )
        
        
        SELECT DISTINCT
               CASE WHEN FC_InputLvl_Id='PPT' THEN '22222'
                         WHEN FC_InputLvl_Id='DFAIT' THEN '11111'
               ELSE  FC_InputLvl_Id END AS Fund_Centre,
        coalesce((SELECT top 1"Currency_Code" from "dbo"."M_MISSION_CURRENCY_CODES" T2 where "Fund_Centre" =
               CASE WHEN FC_InputLvl_Id='PPT' THEN '22222'
                         WHEN FC_InputLvl_Id='DFAIT' THEN '11111'
               ELSE  FC_InputLvl_Id END),'CAD') as DEFAULT_CURRENCY_CODE,
               "FC_SDESC_EN" as FC_SDESC_EN,
               "FC_SDESC_FR" as FC_SDESC_FR,
               "FC_Level5_Id" as LEVEL5_CD,
               "FC_Level5_Desc_En" as LEVEL5_SDESC_EN,
               "FC_Level5_Desc_Fr" as LEVEL5_SDESC_FR,
        	   "FC_Level4_Id" as LEVEL4_CD,
               "FC_Level4_Desc_En" as LEVEL4_SDESC_EN,
               "FC_Level4_Desc_Fr" as LEVEL4_SDESC_FR,
               "FC_Level3_Id" as LEVEL3_CD,
               "FC_Level3_Desc_En" as LEVEL3_SDESC_EN,
               "FC_Level3_Desc_Fr" as LEVEL3_SDESC_FR,
               "FC_Level2_Id" as LEVEL2_CD,
               "FC_Level2_Desc_En" as LEVEL2_SDESC_EN,
               "FC_Level2_Desc_Fr" as LEVEL2_SDESC_FR,
               "FC_Level1_Id" as LEVEL1_CD,
        	   "FC_Level1_Desc_En" as LEVEL1_SDESC_EN,
               "FC_Level1_Desc_Fr" as LEVEL1_SDESC_FR,
        	   (CASE WHEN FC_LEVEL3_ID IS NULL THEN 2 ELSE
                CASE WHEN  FC_LEVEL4_ID IS NULL THEN 3 ELSE
                CASE WHEN  FC_LEVEL5_ID IS NULL THEN 4 ELSE
                CASE WHEN  FC_LEVEL6_ID IS NULL THEN 5 ELSE
                CASE WHEN  FC_LEVEL7_ID IS NULL THEN 6 ELSE
        		7 END END END END END) AS LEVEL,
               '0050' as COMPANY_CODE,
        	    CASE WHEN FC_InputLvl_Id='PPT' THEN '22222'
                     WHEN FC_InputLvl_Id ='DFAIT' THEN 11111 else cast(FC_InputLvl_Id as int) end AS FC_Symbol,
        	   HR5.FC_SYMBOL as LEVEL5_SYMBOL,
               HR4.FC_SYMBOL as LEVEL4_SYMBOL,
               HR3.FC_SYMBOL as LEVEL3_SYMBOL,
               HR2.FC_SYMBOL as LEVEL2_SYMBOL,
        	   p.PAC as PAC,
        	   r.DESCRSHORT as HR_REGION,
        	    r.DEPT_ID as DEPT_ID,
        	   p.PAC_DESCR_EN as PAC_SDESC_EN,
        	   p.PAC_DESCR_FR as PAC_SDESC_FR,
        	   p.PAC + ' - ' + p.PAC_DESCR_EN as PAC_LDESC_EN,
        	   p.PAC + ' - ' + p.PAC_DESCR_FR as PAC_LDESC_FR,
        /*
        	   NULL as PAC, --p.PAC as PAC,
        	   NULL as HR_REGION, --r.DESCRSHORT as HR_REGION,
        	   NULL as DEPT_ID, -- r.DEPT_ID as DEPT_ID,
        	   NULL as PAC_SDESC_EN, --p.PAC_DESCR_EN as PAC_SDESC_EN,
        	   NULL as PAC_SDESC_FR, --p.PAC_DESCR_FR as PAC_SDESC_FR,
        	   NULL as PAC_LDESC_EN, --p.PAC + ' - ' + p.PAC_DESCR_EN as PAC_LDESC_EN,
        	   NULL as PAC_LDESC_FR,  --p.PAC + ' - ' + p.PAC_DESCR_FR as PAC_LDESC_FR,*/
        	   getdate() as Create_Date,
        	   getdate() as Last_Update_Date,
        	   ROW_NUMBER() over (order by FC_InputLvl_Id)  as Record_Identity,
        	   HR6.FC_SYMBOL as LEVEL6_SYMBOL,
               HR7.FC_SYMBOL as LEVEL7_SYMBOL,
        	   "FC_Level7_Id" as LEVEL7_CD,
               "FC_Level7_Desc_En" as LEVEL7_SDESC_EN,
               "FC_Level7_Desc_Fr" as LEVEL7_SDESC_FR,
               "FC_Level6_Id" as LEVEL6_CD,
               "FC_Level6_Desc_En" as LEVEL6_SDESC_EN,
               "FC_Level6_Desc_Fr" as LEVEL6_SDESC_FR	
        
        FROM   dbo.S_FC_HIERARCHY_NEW a 
        LEFT JOIN HR_SYMBOL as HR on CASE WHEN a.FC_InputLvl_Id='PPT' THEN 22222
                     WHEN a.FC_InputLvl_Id ='DFAIT' THEN 11111 else cast(a.FC_InputLvl_Id as int) end = cast(HR.G9_FUND_CENTER as int)
        LEFT JOIN HR_SYMBOL as HR2 on CASE WHEN a.FC_Level2_Id='PPT' THEN 22222
                     WHEN a.FC_Level2_Id ='