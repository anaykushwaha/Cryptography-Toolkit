# constants.py

# Shared Constants for the Entire Cryptography Toolkit

# Contains application-wide constants used throughout the project.
# Keeping shared values in one module prevents duplication and
# makes configuration and maintenance easier.


# Project Information

PROJECT_NAME = "Cryptography Toolkit"

PROJECT_VERSION = "1.0.0"

PROJECT_DESCRIPTION = (
    "A modular toolkit for classical cryptography, "
    "cryptanalysis, and text analysis."
)

PROJECT_AUTHOR = "Scaranker"

PROJECT_LICENSE = "MIT"


# Character Constants

LOWERCASE_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

UPPERCASE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DIGITS = "0123456789"

ALPHANUMERIC = (
    UPPERCASE_ALPHABET
    + LOWERCASE_ALPHABET
    + DIGITS
)

ASCII_LETTERS = (
    UPPERCASE_ALPHABET
    + LOWERCASE_ALPHABET
)

PRINTABLE_ASCII_START = 32

PRINTABLE_ASCII_END = 126

PRINTABLE_ASCII_LENGTH = (
    PRINTABLE_ASCII_END
    - PRINTABLE_ASCII_START
    + 1
)


# Cipher Constants

DEFAULT_SHIFT = 3

MIN_CAESAR_SHIFT = 0

MAX_CAESAR_SHIFT = 25

CAESAR_KEYSPACE_SIZE = 26

ROT13_SHIFT = 13

ROT5_SHIFT = 5

ROT47_SHIFT = 47


# Analysis Constants

ENGLISH_ALPHABET_SIZE = 26

DEFAULT_NGRAM_SIZE = 2

BIGRAM_SIZE = 2

TRIGRAM_SIZE = 3

DEFAULT_TOP_CANDIDATES = 10

DEFAULT_FREQUENCY_PRECISION = 4

DEFAULT_SCORE_PRECISION = 4

DEFAULT_ENTROPY_PRECISION = 4

DEFAULT_IOC_PRECISION = 4


# File Constants

DEFAULT_ENCODING = "utf-8"

DEFAULT_NEWLINE = "\n"

TEXT_FILE_EXTENSION = ".txt"

JSON_FILE_EXTENSION = ".json"

CSV_FILE_EXTENSION = ".csv"

MARKDOWN_FILE_EXTENSION = ".md"

REPORT_FILE_EXTENSION = ".txt"


# Directory Names

DATA_DIRECTORY = "data"

REPORTS_DIRECTORY = "reports"

HISTORY_DIRECTORY = "history"

DOCS_DIRECTORY = "docs"

EXAMPLES_DIRECTORY = "examples"

TESTS_DIRECTORY = "tests"


# Application Constants

DEFAULT_APPLICATION_NAME = (
    "Cryptography Toolkit"
)

DEFAULT_LANGUAGE = "en"

DEFAULT_THEME = "default"

DEFAULT_TIMEOUT = 30

DEFAULT_PROGRESS_WIDTH = 40

DEFAULT_TABLE_WIDTH = 80


# CLI Constants

CLI_PROMPT = "> "

CLI_CONTINUE_PROMPT = (
    "Press Enter to continue..."
)

CLI_YES_VALUES = (
    "y",
    "yes",
)

CLI_NO_VALUES = (
    "n",
    "no",
)

CLI_EXIT_COMMANDS = (
    "q",
    "quit",
    "exit",
)

CLI_CLEAR_COMMANDS = (
    "clear",
    "cls",
)


# Logging Constants

DEFAULT_LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s - "
    "%(name)s - "
    "%(levelname)s - "
    "%(message)s"
)

LOG_DATE_FORMAT = (
    "%Y-%m-%d %H:%M:%S"
)

DEFAULT_LOG_DIRECTORY = "logs"

DEFAULT_LOG_FILENAME = (
    "cryptography_toolkit.log"
)


# Validation Constants

MIN_TEXT_LENGTH = 0

MAX_TEXT_LENGTH = 1_000_000

MIN_KEY_LENGTH = 1

MAX_KEY_LENGTH = 1_000

MIN_ALPHABET_LENGTH = 2

MAX_ALPHABET_LENGTH = 256


# Streaming Constants

DEFAULT_CHUNK_SIZE = 4096

MIN_CHUNK_SIZE = 1

MAX_CHUNK_SIZE = 1_048_576


# Timing Constants

DEFAULT_TIMER_PRECISION = 6

MILLISECONDS_PER_SECOND = 1_000

MICROSECONDS_PER_SECOND = 1_000_000


# Boolean Constants

ENABLED = True

DISABLED = False


# Common Symbols

EMPTY_STRING = ""

SPACE = " "

TAB = "\t"

NEWLINE = "\n"

CARRIAGE_RETURN = "\r"

PERIOD = "."

COMMA = ","

COLON = ":"

SEMICOLON = ";"

HYPHEN = "-"

UNDERSCORE = "_"


# Result Status Constants

STATUS_SUCCESS = "success"

STATUS_FAILURE = "failure"

STATUS_WARNING = "warning"

STATUS_ERROR = "error"

STATUS_PENDING = "pending"


# Cipher Operation Constants

OPERATION_ENCRYPT = "encrypt"

OPERATION_DECRYPT = "decrypt"

OPERATION_ANALYZE = "analyze"

OPERATION_VERIFY = "verify"


# Supported Cipher Names

CIPHER_CAESAR = "caesar"

CIPHER_ROT13 = "rot13"

CIPHER_ROT5 = "rot5"

CIPHER_ROT18 = "rot18"

CIPHER_ROT47 = "rot47"

CIPHER_ATBASH = "atbash"

CIPHER_CHAIN = "chain"


# Supported Analysis Names

ANALYSIS_FREQUENCY = "frequency"

ANALYSIS_STATISTICS = "statistics"

ANALYSIS_ENTROPY = "entropy"

ANALYSIS_IOC = "ioc"

ANALYSIS_NGRAMS = "ngrams"

ANALYSIS_SCORER = "scorer"

ANALYSIS_BRUTE_FORCE = "brute_force"


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the constants module

    tests = [

        PROJECT_NAME
        == "Cryptography Toolkit",

        PROJECT_VERSION
        == "1.0.0",

        len(
            LOWERCASE_ALPHABET
        )
        == 26,

        len(
            UPPERCASE_ALPHABET
        )
        == 26,

        len(
            DIGITS
        )
        == 10,

        len(
            ASCII_LETTERS
        )
        == 52,

        CAESAR_KEYSPACE_SIZE
        == 26,

        ROT13_SHIFT
        == 13,

        ROT5_SHIFT
        == 5,

        BIGRAM_SIZE
        == 2,

        TRIGRAM_SIZE
        == 3,

        DEFAULT_ENCODING
        == "utf-8",

        DEFAULT_CHUNK_SIZE
        > 0,

        MIN_CHUNK_SIZE
        <= DEFAULT_CHUNK_SIZE,

        DEFAULT_CHUNK_SIZE
        <= MAX_CHUNK_SIZE,

        MIN_KEY_LENGTH
        <= MAX_KEY_LENGTH,

        MIN_ALPHABET_LENGTH
        <= MAX_ALPHABET_LENGTH,

        STATUS_SUCCESS
        == "success",

        STATUS_FAILURE
        == "failure",

        OPERATION_ENCRYPT
        == "encrypt",

        OPERATION_DECRYPT
        == "decrypt",

        CIPHER_CAESAR
        == "caesar",

        CIPHER_ATBASH
        == "atbash",

        ANALYSIS_FREQUENCY
        == "frequency",

        ANALYSIS_BRUTE_FORCE
        == "brute_force",
    ]

    return all(
        tests
    )


# Module Exports

__all__ = [

    # Project Information
    "PROJECT_NAME",
    "PROJECT_VERSION",
    "PROJECT_DESCRIPTION",
    "PROJECT_AUTHOR",
    "PROJECT_LICENSE",

    # Character Constants
    "LOWERCASE_ALPHABET",
    "UPPERCASE_ALPHABET",
    "DIGITS",
    "ALPHANUMERIC",
    "ASCII_LETTERS",
    "PRINTABLE_ASCII_START",
    "PRINTABLE_ASCII_END",
    "PRINTABLE_ASCII_LENGTH",

    # Cipher Constants
    "DEFAULT_SHIFT",
    "MIN_CAESAR_SHIFT",
    "MAX_CAESAR_SHIFT",
    "CAESAR_KEYSPACE_SIZE",
    "ROT13_SHIFT",
    "ROT5_SHIFT",
    "ROT47_SHIFT",

    # Analysis Constants
    "ENGLISH_ALPHABET_SIZE",
    "DEFAULT_NGRAM_SIZE",
    "BIGRAM_SIZE",
    "TRIGRAM_SIZE",
    "DEFAULT_TOP_CANDIDATES",
    "DEFAULT_FREQUENCY_PRECISION",
    "DEFAULT_SCORE_PRECISION",
    "DEFAULT_ENTROPY_PRECISION",
    "DEFAULT_IOC_PRECISION",

    # File Constants
    "DEFAULT_ENCODING",
    "DEFAULT_NEWLINE",
    "TEXT_FILE_EXTENSION",
    "JSON_FILE_EXTENSION",
    "CSV_FILE_EXTENSION",
    "MARKDOWN_FILE_EXTENSION",
    "REPORT_FILE_EXTENSION",

    # Directory Names
    "DATA_DIRECTORY",
    "REPORTS_DIRECTORY",
    "HISTORY_DIRECTORY",
    "DOCS_DIRECTORY",
    "EXAMPLES_DIRECTORY",
    "TESTS_DIRECTORY",

    # Application Constants
    "DEFAULT_APPLICATION_NAME",
    "DEFAULT_LANGUAGE",
    "DEFAULT_THEME",
    "DEFAULT_TIMEOUT",
    "DEFAULT_PROGRESS_WIDTH",
    "DEFAULT_TABLE_WIDTH",

    # CLI Constants
    "CLI_PROMPT",
    "CLI_CONTINUE_PROMPT",
    "CLI_YES_VALUES",
    "CLI_NO_VALUES",
    "CLI_EXIT_COMMANDS",
    "CLI_CLEAR_COMMANDS",

    # Logging Constants
    "DEFAULT_LOG_LEVEL",
    "LOG_FORMAT",
    "LOG_DATE_FORMAT",
    "DEFAULT_LOG_DIRECTORY",
    "DEFAULT_LOG_FILENAME",

    # Validation Constants
    "MIN_TEXT_LENGTH",
    "MAX_TEXT_LENGTH",
    "MIN_KEY_LENGTH",
    "MAX_KEY_LENGTH",
    "MIN_ALPHABET_LENGTH",
    "MAX_ALPHABET_LENGTH",

    # Streaming Constants
    "DEFAULT_CHUNK_SIZE",
    "MIN_CHUNK_SIZE",
    "MAX_CHUNK_SIZE",

    # Timing Constants
    "DEFAULT_TIMER_PRECISION",
    "MILLISECONDS_PER_SECOND",
    "MICROSECONDS_PER_SECOND",

    # Boolean Constants
    "ENABLED",
    "DISABLED",

    # Common Symbols
    "EMPTY_STRING",
    "SPACE",
    "TAB",
    "NEWLINE",
    "CARRIAGE_RETURN",
    "PERIOD",
    "COMMA",
    "COLON",
    "SEMICOLON",
    "HYPHEN",
    "UNDERSCORE",

    # Result Status
    "STATUS_SUCCESS",
    "STATUS_FAILURE",
    "STATUS_WARNING",
    "STATUS_ERROR",
    "STATUS_PENDING",

    # Cipher Operations
    "OPERATION_ENCRYPT",
    "OPERATION_DECRYPT",
    "OPERATION_ANALYZE",
    "OPERATION_VERIFY",

    # Cipher Names
    "CIPHER_CAESAR",
    "CIPHER_ROT13",
    "CIPHER_ROT5",
    "CIPHER_ROT18",
    "CIPHER_ROT47",
    "CIPHER_ATBASH",
    "CIPHER_CHAIN",

    # Analysis Names
    "ANALYSIS_FREQUENCY",
    "ANALYSIS_STATISTICS",
    "ANALYSIS_ENTROPY",
    "ANALYSIS_IOC",
    "ANALYSIS_NGRAMS",
    "ANALYSIS_SCORER",
    "ANALYSIS_BRUTE_FORCE",

    # Testing
    "self_test",
]

