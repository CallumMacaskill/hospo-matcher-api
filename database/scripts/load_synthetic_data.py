import argparse
import json

from hospo_matcher.utils.database import driver
from hospo_matcher.utils.logger import log
from hospo_matcher.utils.data_models import Venue

if __name__=="__main__":
    # Get inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-path")
    args = parser.parse_args()
    file_path = args.file_path

    # Load local data
    with open("database\synthetic_data.json", "r") as f:
        file_data = json.load(f)
    
    log.info(f"Loaded {len(file_data)} venues from file.")

    db_client = driver.get_db_client()
    venues_collection = db_client.venues

    # Validate against model
    for venue in file_data:
        Venue(**venue)

    # Upload documents
    insert_result = venues_collection.insert_many(file_data)
    log.info(f"Inserted {len(insert_result.inserted_ids)} venues.")
