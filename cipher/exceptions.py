# exceptions.py 
# Custom exception hierarchy for the toolkit 

# Using custom exceptions makes the toolkit easier to debug, test and extend 

from __future__ import annotations

class CipherError(Exception): 
    # Base exception for the entire toolkit 
    # Eevery custom exception inherits from this class 

    pass 


# Alphabet Exceptions

class InvalidAlphabetError(CipherError): 
    # Raised when an alphabet is invalid 

    pass 

class AlphabetNotFoundError(CipherError): 
    # Raised when requesting an alphabet that doesn't exist 

    pass 

# Shift Exceptions 

class InvalidShiftError(CipherError): 
    # Raised when a shift value is invalid 

    pass


# Text Exceptions

class EmptyTextError(CipherError):
    # Raised when an empty string is supplied where text is required 

    pass

class InvalidTextError(CipherError): 
    # Raised when text isn't a string 

    pass


# Encryption Exceptions

class EncryptionError(CipherError):
    # General encryption failure 

    pass


class DecryptionError(CipherError):
    # General decryption failure 

    pass


class UnsupportedCipherError(CipherError):
    # Raised when attempting to use a cipher that hasn't been implemented 

    pass


# Analysis Exceptions

class AnalysisError(CipherError): 
    # Base class for analysis-related failures 

    pass


class FrequencyAnalysisError(AnalysisError): 
    # Raised when frequency analysis fails 

    pass


class BruteForceError(AnalysisError): 
    # Raised when brute-force analysis fails 

    pass


class AutoCrackError(AnalysisError): 
    # Raised when automatic cracking cannot determine a suitable result 

    pass


# File Exceptions

class FileEncryptionError(CipherError): 
    # Raised when encrypting a file fails 

    pass


class FileDecryptionError(CipherError): 
    # Raised when decrypting a file fails 

    pass


class FileFormatError(CipherError): 
    # Raised when an unsupported file format is encountered 

    pass


# Configuration Exceptions

class ConfigurationError(CipherError): 
    # Raised when configuration values are invalid 

    pass


# Internal Exceptions

class InternalCipherError(CipherError): 
    # Indicates an unexpected internal error 

    pass 

