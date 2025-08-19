from pathlib import Path

import yaml

def load_yaml_file(file_path):
    """
    Reads a YAML file and returns its contents as a Python dictionary.
    
    Args:
        file_path (str): The path to the YAML file.
        
    Returns:
        dict: The contents of the YAML file as a Python dictionary.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

