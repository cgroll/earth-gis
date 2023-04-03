from pathlib import Path

class PPPaths:
    
    current_file_path = Path(__file__)
    data_path = current_file_path.parent.parent / "data"
    raw_data_path = data_path / "raw_data"
    processed_data_path = data_path / "processed_data"
