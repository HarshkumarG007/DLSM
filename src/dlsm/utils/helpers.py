import json
import logging
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict
import joblib
import numpy as np

def setup_logger(name: str = "DLSM", log_file: str = "artifacts/reports/dlsm.log", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
        
    return logger

def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

def save_json(data: Any, filepath: str | Path) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def load_json(filepath: str | Path) -> Any:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_pickle(obj: Any, filepath: str | Path) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)

def load_pickle(filepath: str | Path, verify_checksum: bool = True) -> Any:
    path = Path(filepath)
    if verify_checksum:
        checksums_file = path.parent / "checksums.json"
        if checksums_file.exists():
            import hashlib
            with open(checksums_file, "r", encoding="utf-8") as f:
                checksums = json.load(f)
            expected = checksums.get(path.name)
            if expected:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != expected:
                    raise ValueError(
                        f"Security Alert: Checksum mismatch for {path.name} (possible model tampering). "
                        f"Expected {expected}, got {actual}"
                    )
    return joblib.load(path)
