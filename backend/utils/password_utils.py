import bcrypt
from typing import Union


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password as string
    """
    # Convert password to bytes if it's not already
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    
    # Return the hashed password as a string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to compare against
        
    Returns:
        True if passwords match, False otherwise
    """
    # Convert passwords to bytes if they're not already
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    # Verify the password
    return bcrypt.checkpw(plain_password, hashed_password)