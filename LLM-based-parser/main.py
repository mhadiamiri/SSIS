from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os, json, re
from esxtract_prompts import *
from glob import glob
import logging

# Insert logger configuration after load_dotenv()
load_dotenv()
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

base_url = 'https://openrouter.ai/api/v1'
api_key = os.getenv('OPENROUTER_API_KEY')

llm = ChatOpenAI(model=os.getenv('EXTRACTION_MODEL'), base_url=base_url, api_key=api_key, )


def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def save_json(json_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_data, file)

def save_markdown(markdown_data, file_path):
    with open(file_path, 'w') as file:
        file.write(markdown_data)

def parse_json(json_string):
    return json.loads(json_string.replace("```json", "").replace("```", ""))

def parse_dtsx_file(package_path):
    logger.info(f"Parsing {package_path.split('/')[-1]}")
    xml_content = load_file(package_path)

    
    # TODO Sliding Window needs to be implemented
    # try to parse as a single file 
    try:
        logger.info("Parsing as single file")
        summary = llm.invoke(input=summarization_prompt_single_file.format(summary=xml_content))
    
    # if it fails, try to parse as a 3 part file
    except:
        logger.warning("Parsing as single file failed, parsing as a 5 part file")
        # split the file into 5 parts
        first_part = xml_content[:len(xml_content)//5]
        second_part = xml_content[len(xml_content)//5:2*len(xml_content)//5]
        third_part = xml_content[2*len(xml_content)//5:3*len(xml_content)//5]
        fourth_part = xml_content[3*len(xml_content)//5:4*len(xml_content)//5]
        fifth_part = xml_content[4*len(xml_content)//5:]

        first_part = llm.invoke(f"{partial_prompt}:\n {first_part}")
        logger.info(f"[1/5] Successfully parsed")

        second_part = llm.invoke(f"{partial_prompt}:\n {second_part}")
        logger.info(f"[2/5] Successfully parsed")

        third_part = llm.invoke(f"{partial_prompt}:\n {third_part}")
        logger.info(f"[3/5] Successfully parsed")

        fourth_part = llm.invoke(f"{partial_prompt}:\n {fourth_part}")
        logger.info(f"[4/5] Successfully parsed")

        fifth_part = llm.invoke(f"{partial_prompt}:\n {fifth_part}")
        logger.info(f"[5/5] Successfully parsed")

        summary = llm.invoke(input=summarization_prompt_by_parts.format(first_part=first_part, second_part=second_part, third_part=third_part, fourth_part=fourth_part, fifth_part=fifth_part))

    return summary.content

def build_conmgr_files(conmgr_file):

    with open(conmgr_file, 'r') as file:
        connection_string = file.read()
        structured_connection_manager = llm.invoke(connmgr_to_json_prompt + "\n\n" + connection_string)

        logger.info(f"Parsed structured connection manager for {conmgr_file.split('/')[-1]}")
        
        return parse_json(structured_connection_manager.content)['connectionManagers']
        

def workflow(packages_path, save_path):
    # save folder 
    os.makedirs(save_path, exist_ok=True)

    # subfolder
    os.makedirs(f'{save_path}/{packages_path.split("/")[-1]}', exist_ok=True)
    
    # Get all files in the folder
    all_files = glob(f'{packages_path}/*')
    logger.info(f"Found {len(all_files)} files")

    # Perpare connection manager schema
    aggregated_connection_managers = {"connectionManagers":[]}

    for pack_file in all_files:

        # check if file exists

        # if it is a dtsx file, parse it
        if pack_file.endswith('.dtsx'):
            if not os.path.exists(f'{save_path}/{packages_path.split("/")[-1]}/{pack_file.split("/")[-1]}.md'):
                try:
                    logger.info(f"Parsing {pack_file.split('/')[-1]}")
                    summary = parse_dtsx_file(pack_file)
                    save_markdown(summary, f'{save_path}/{packages_path.split("/")[-1]}/{pack_file.split("/")[-1]}.md')
                except Exception as e:
                    logger.error(f"Error parsing {pack_file.split('/')[-1]}: {e}")
            else:
                logger.info(f"File {pack_file.split('/')[-1]} already exists")  
        elif pack_file.endswith('.conmgr'):
            if not os.path.exists(f'{save_path}/{packages_path.split("/")[-1]}/connection_managers.json'):
                conmgr_files = build_conmgr_files(pack_file)
                aggregated_connection_managers['connectionManagers'].extend(conmgr_files)
            else:
                logger.info(f"File {pack_file.split('/')[-1]} already exists")  

        elif pack_file.endswith('.params'):
            pass

    save_json(aggregated_connection_managers, f'{save_path}/{packages_path.split("/")[-1]}/connection_managers.json')

if __name__ == "__main__":
    save_path = '/root/SSIS_Migration_Assistant/parsed_packages'
    
    packages = [
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_TRADE',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_ARD',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_CCEM',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_COSMOS',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_FC',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_GC',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_IMS',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_NEICS',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_PATHFINDER',
        '/root/SSIS_Migration_Assistant/SSISPacks/SSIS_SWS'
    ]

 
    for package in packages:
        try:
            logger.info(f"Processing {package.split('/')[-1]}")
            workflow(package, save_path)
        except Exception as e:
            logger.error(f"ERROR: {e}")
            continue