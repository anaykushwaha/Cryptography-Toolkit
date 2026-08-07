# streaming.py
# Streaming encryption utilities for the Cryptography Toolkit

# Contains utilities for processing large amounts of text
# without loading the entire input into memory


from __future__ import annotations

from collections.abc import Callable, Generator, Iterable, Iterator


# Type Definitions

TransformFunction = Callable[[str], str]


# Text Streaming

def encrypt_chunks(
    chunks: Iterable[str],
    transform: TransformFunction,
) -> Generator[str, None, None]:
    # Encrypts text chunks one at a time
    # Each chunk is passed directly to the supplied transformation function

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    for chunk in chunks:

        if not isinstance(
            chunk,
            str,
        ):
            raise TypeError(
                "Each chunk must be a string."
            )

        yield transform(
            chunk
        )


def decrypt_chunks(
    chunks: Iterable[str],
    transform: TransformFunction,
) -> Generator[str, None, None]:
    # Decrypts text chunks one at a time
    # The supplied transformation function should perform decryption

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    for chunk in chunks:

        if not isinstance(
            chunk,
            str,
        ):
            raise TypeError(
                "Each chunk must be a string."
            )

        yield transform(
            chunk
        )


# Text Generators

def encrypt_generator(
    text: str,
    transform: TransformFunction,
    chunk_size: int = 1024,
) -> Generator[str, None, None]:
    # Encrypts text incrementally using fixed-size chunks

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        chunk_size,
        int,
    ):
        raise TypeError(
            "Chunk size must be an integer."
        )

    if chunk_size <= 0:
        raise ValueError(
            "Chunk size must be greater than zero."
        )

    for start in range(
        0,
        len(text),
        chunk_size,
    ):

        chunk = text[
            start:start + chunk_size
        ]

        yield transform(
            chunk
        )


def decrypt_generator(
    text: str,
    transform: TransformFunction,
    chunk_size: int = 1024,
) -> Generator[str, None, None]:
    # Decrypts text incrementally using fixed-size chunks

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        chunk_size,
        int,
    ):
        raise TypeError(
            "Chunk size must be an integer."
        )

    if chunk_size <= 0:
        raise ValueError(
            "Chunk size must be greater than zero."
        )

    for start in range(
        0,
        len(text),
        chunk_size,
    ):

        chunk = text[
            start:start + chunk_size
        ]

        yield transform(
            chunk
        )


# Iterable Processing

def process_chunks(
    chunks: Iterable[str],
    transform: TransformFunction,
) -> Iterator[str]:
    # Applies a transformation to every chunk in an iterable

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    for chunk in chunks:

        if not isinstance(
            chunk,
            str,
        ):
            raise TypeError(
                "Each chunk must be a string."
            )

        yield transform(
            chunk
        ) 


# File Streaming


def encrypt_file(
    input_path: str,
    output_path: str,
    transform: TransformFunction,
    *,
    chunk_size: int = 4096,
    encoding: str = "utf-8",
) -> int:
    # Encrypts a file incrementally without loading the entire file into memory

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    if chunk_size <= 0:
        raise ValueError(
            "Chunk size must be greater than zero."
        )

    bytes_written = 0

    with open(
        input_path,
        "r",
        encoding=encoding,
    ) as source:

        with open(
            output_path,
            "w",
            encoding=encoding,
        ) as destination:

            while True:

                chunk = source.read(
                    chunk_size
                )

                if not chunk:
                    break

                transformed = transform(
                    chunk
                )

                destination.write(
                    transformed
                )

                bytes_written += len(
                    transformed.encode(
                        encoding
                    )
                )

    return bytes_written


def decrypt_file(
    input_path: str,
    output_path: str,
    transform: TransformFunction,
    *,
    chunk_size: int = 4096,
    encoding: str = "utf-8",
) -> int:
    # Decrypts a file incrementally without loading the entire file into memory

    return encrypt_file(
        input_path,
        output_path,
        transform,
        chunk_size=chunk_size,
        encoding=encoding,
    )


# Line Streaming


def encrypt_lines(
    lines: Iterable[str],
    transform: TransformFunction,
) -> Generator[str, None, None]:
    # Encrypts lines individually while preserving line endings

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    for line in lines:

        if not isinstance(
            line,
            str,
        ):
            raise TypeError(
                "Each line must be a string."
            )

        newline = ""

        if line.endswith("\n"):
            newline = "\n"
            content = line[:-1]

        else:
            content = line

        yield (
            transform(content)
            + newline
        )


def decrypt_lines(
    lines: Iterable[str],
    transform: TransformFunction,
) -> Generator[str, None, None]:
    # Decrypts lines individually while preserving line endings

    yield from encrypt_lines(
        lines,
        transform,
    )


# File Line Processing


def process_file_lines(
    input_path: str,
    output_path: str,
    transform: TransformFunction,
    *,
    encoding: str = "utf-8",
) -> int:
    # Processes a file one line at a time
    # Returns the number of lines processed

    if not callable(
        transform
    ):
        raise TypeError(
            "Transform must be callable."
        )

    line_count = 0

    with open(
        input_path,
        "r",
        encoding=encoding,
    ) as source:

        with open(
            output_path,
            "w",
            encoding=encoding,
        ) as destination:

            for line in source:

                transformed = next(
                    encrypt_lines(
                        [line],
                        transform,
                    )
                )

                destination.write(
                    transformed
                )

                line_count += 1

    return line_count 

# Validation Helpers

def validate_chunk_size(
    chunk_size: int,
) -> bool:
    # Determines whether a chunk size is valid

    if not isinstance(
        chunk_size,
        int,
    ):
        return False

    return chunk_size > 0


def validate_encoding(
    encoding: str,
) -> bool:
    # Determines whether a text encoding is supported

    if not isinstance(
        encoding,
        str,
    ):
        return False

    try:
        "".encode(
            encoding
        )

    except LookupError:
        return False

    return True


# Streaming Statistics

def count_chunks(
    text: str,
    chunk_size: int = 1024,
) -> int:
    # Calculates how many chunks are required to process the text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not validate_chunk_size(
        chunk_size
    ):
        raise ValueError(
            "Chunk size must be greater than zero."
        )

    if not text:
        return 0

    return (
        len(text)
        + chunk_size
        - 1
    ) // chunk_size


def count_lines(
    input_path: str,
    *,
    encoding: str = "utf-8",
) -> int:
    # Counts the number of lines in a file without loading it into memory

    if not validate_encoding(
        encoding
    ):
        raise ValueError(
            f"Unsupported encoding: {encoding}"
        )

    line_count = 0

    with open(
        input_path,
        "r",
        encoding=encoding,
    ) as source:

        for _ in source:
            line_count += 1

    return line_count


# Streaming Self Test

def self_test() -> bool:
    # Runs a quick internal test of the streaming utilities

    text = (
        "The quick brown fox "
        "jumps over the lazy dog."
    )

    transform = lambda value: value.upper()

    encrypted = "".join(
        encrypt_generator(
            text,
            transform,
            chunk_size=8,
        )
    )

    if encrypted != text.upper():
        return False

    chunks = list(
        encrypt_chunks(
            ["hello", " ", "world"],
            transform,
        )
    )

    if "".join(chunks) != "HELLO WORLD":
        return False

    if count_chunks(
        text,
        8,
    ) != 6:
        return False

    if not validate_chunk_size(
        1024
    ):
        return False

    if validate_chunk_size(
        0
    ):
        return False

    if not validate_encoding(
        "utf-8"
    ):
        return False

    return True


# Module Exports

__all__ = [
    "TransformFunction",
    "encrypt_chunks",
    "decrypt_chunks",
    "encrypt_generator",
    "decrypt_generator",
    "process_chunks",
    "encrypt_file",
    "decrypt_file",
    "encrypt_lines",
    "decrypt_lines",
    "process_file_lines",
    "validate_chunk_size",
    "validate_encoding",
    "count_chunks",
    "count_lines",
    "self_test",
] 

