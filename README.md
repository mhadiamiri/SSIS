# SSIS_Migration_Assistant

## Description
This tool is used to analyze SSIS packages and generate a report for the same. The tool is divided into two parts:
1. SSIS Analyzer: This tool is used to analyze the SSIS packages and generate a detailed analysis of the same.
2. SSIS Report Generator: This tool is used to generate a report based on the analysis done by the SSIS Analyzer.
3. generate_summary: This tool is used to generate a summary report based on the analysis done by the SSIS Analyzer.

## Usage
```bash
python3 ssis_analyzer.py SSIS_PACKAGES_DIR
```
```bash
python3 generate_ssis_report.py Analysis_DIR SummaryDIR ReportTitle
```

## Example
```bash
python ssis_analyzer.py SSISPacks 
python generate_ssis_report.py SSISDetailedAnalysisOutput SSISSummaryReport "TEST Title"
```

# To Do 
- [ ] Clear all bugs listed in Asana project
- [ ] Load SSIS package as `XML` and extract the heirarchy of SQL queries
- [ ] Create an Agent to transform T-SQL queries to Spark SQL queries

**Note:** More items can be found in [OneNote]([TODO.md](https://dataplatforms.sharepoint.com/:o:/s/RDPManagedIPs2-SSISMigration/EsOKDze4nd5As2HP6inJTMwBuQZvJANoA_gLiKdCdsOWNw?e=7qsVBE)).