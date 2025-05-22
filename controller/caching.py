from models import *
from schema import *
import json
import gzip
import base64
from typing import Tuple

# Set data compression threshold
COMPRESSION_SIZE_THRESHOLD = 1024  
MIN_COMPRESSION_REDUCTION = 0.1   

def compress_data(data: dict) -> Tuple[str, bool]:

    # Get original data size
    data_json = json.dumps(data, default=str)
    original_size = len(data_json.encode('utf-8'))
    
    # Check data size, if data size < COMPRESSION_SIZE_THRESHOLD store without compression
    if original_size < COMPRESSION_SIZE_THRESHOLD:
        return data_json, False
    
    # Data compression process
    try:
        # Compress data using gzip (binary)
        data_compressed = gzip.compress(data_json.encode('utf-8'))
        compressed_size = len(data_compressed)
        
        # Check compression size difference between original data
        compression_ratio = (1 - compressed_size / original_size)
        
        # Apply data compression if significant (size reduction ratio > 10%)
        if compression_ratio >= MIN_COMPRESSION_REDUCTION:
            
            compressed_b64 = base64.b64encode(data_compressed).decode('utf-8')
            print(f"({compression_ratio*100:.1f}% reduction)")
            
            return compressed_b64, True
        
        else:
            print(f"({compression_ratio*100:.1f}% reduction, no compression needed)")

            return data_json, False
            
    except Exception as e:
        print(f"Compression failed: {(e)}")
        
        return data_json, False

def decompress_data(cached_data: str, is_compressed: bool) -> dict:
    
    if not is_compressed:
        return json.loads(cached_data)
    
    # Decompress data to json format
    compressed = base64.b64decode(cached_data.encode('utf-8'))
    decompressed = gzip.decompress(compressed)
    return json.loads(decompressed.decode('utf-8'))