# base.py
# Base interface for all ciphers in the Cryptography Toolkit

# Defines the common structure that cipher implementations should follow
# Future ciphers can inherit from this base class


from __future__ import annotations
from abc import ABC, abstractmethod


# Base Cipher Class

class Cipher(ABC):
    # Abstract base class for encryption algorithms

    @abstractmethod
    def encrypt(
        self,
        text: str,
    ) -> str:
        # Encrypts the supplied text
        # Each cipher must provide its own implementation

        raise NotImplementedError


    @abstractmethod
    def decrypt(
        self,
        text: str,
    ) -> str:
        # Decrypts the supplied text
        # Each cipher must provide its own implementation

        raise NotImplementedError


    def verify(
        self,
        plaintext: str,
        ciphertext: str,
    ) -> bool:
        # Verifies that encrypting the plaintext produces the ciphertext

        return self.encrypt(
            plaintext
        ) == ciphertext


    def summary(
        self,
        text: str,
    ) -> dict:
        # Returns basic information about a cipher transformation

        encrypted = self.encrypt(
            text
        )

        return {
            "original": text,
            "transformed": encrypted,
            "length": len(text),
        }


    def self_test(self) -> bool:
        # Runs a basic reversible encryption test
        # Subclasses can override this with more detailed tests

        test_text = "Cryptography Toolkit"

        encrypted = self.encrypt(
            test_text
        )

        decrypted = self.decrypt(
            encrypted
        )

        return decrypted == test_text


# Cipher Information

    @property
    def name(self) -> str:
        # Returns the name of the cipher

        return self.__class__.__name__


    def __str__(self) -> str:
        # Returns a readable representation of the cipher

        return self.name


# Module Exports

__all__ = [
    "Cipher",
] 

