def json_structure_verification(json_obj, required_keys):
    missing = [key for key in required_keys if key not in json_obj]
    return missing