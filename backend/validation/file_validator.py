from fastapi import HTTPException, UploadFile
import os

def validate_txt_file(file: UploadFile):
    """
    Validates that the uploaded file is a .txt file and less than 100MB
    """
    # Validate file extension
    if not file.filename.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    # Move to the end of the file to get its size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer to the beginning
    
    # Check if file size is greater than 100MB
    max_size = 100 * 1024 * 1024  # 100MB in bytes
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 100MB limit")
    
    return file