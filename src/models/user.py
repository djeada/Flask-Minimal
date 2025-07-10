"""
This module defines the LibraryUser data class which represents a user of the
library.
"""

from dataclasses import dataclass


@dataclass
class LibraryUser:
    """
    A LibraryUser object represents a user of a library system and has the
    following attributes:

    :ivar id: the user's unique identifier
    :ivar name: the user's name
    :ivar email: the user's email
    :ivar password: the user's password
    """

    id: int
    name: str
    email: str
    password: str

    @classmethod
    def from_dict(cls, user_dict: dict) -> "LibraryUser":
        """
        Create a `LibraryUser` object from a dictionary.

        :param user_dict: A dictionary with the following keys:
                - `id` (int): the user's unique identifier
                - `name` (str): the user's name
                - `email` (str): the user's email
                - `password` (str): the user's password

        :returns: A `LibraryUser` object with the attributes specified in the
        dictionary.
        """
        return cls(
            id=int(user_dict["id"]),
            name=str(user_dict["name"]),
            email=str(user_dict["email"]),
            password=str(user_dict["password"]),
        )
