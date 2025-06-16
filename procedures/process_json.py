#
# EarthCODE metadata DOI provvisioning
#
# Project: EarthCODE
#
# Center for Sensing Solutions (Eurac research)
#
# file: process_json.py
#

import json
from datetime import datetime
import os

def process_json(json_file_path):
    # Verifica se il file esiste
    if not os.path.exists(json_file_path):
        print(f"Error: file not found -> '{json_file_path}' ")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # check for field "sci:doi"
        if "sci:doi" in data and data["sci:doi"] is not None:
            print(f"doi field 'sci:doi' found: {data['sci:doi']}")
        else:
            print("doi field 'sci:doi' not found")

        # extract variables
        title = data.get("title")
        description = data.get("description")
        resource_type = "Dataset"
        publ_year = datetime.now().year

        creators = []
        publishers = []

        for provider in data.get("providers", []):
            roles = provider.get("roles", [])
            if "producer" in roles or "processor" in roles:
                creators.append(provider)
            if "host" in roles:
                publishers.append(provider)

        #print("Metadata fields: ")
        #print("Title:", title)
        #print("Description:", description)
        #print("Publication year:", publ_year)
        #print("Resource type:", resource_type)
        #print("Creators (producer/processor):", creators)
        #print("Publisher (host):", publishers)

        mtd_map =  {
            "title": title,
            "description": description,
            "publ_year": publ_year,
            "resource_type": resource_type,
            "producer": "Copernicus Land Monitoring Service",
            "publisher": "Eurac Research - Institute for Earth Observation"
        }

        if("sci:doi" in data and data['sci:doi'] != ""):
            mtd_map["doi"] = data['sci:doi']

        return mtd_map

    except json.JSONDecodeError:
        print("Error: not a valid metadata json file")
    except Exception as e:
        print(f"Error during execution {e}")

