"""Houses the class representing a Figaro user"""

import argon2
from getpass import getpass
from typing import List, Union

from figaro import utils
from figaro.server import db

class User(object):
    """
    Represents a Figaro user

    ...

    Attributes
    ----------
    uid : int
        The user's unique id.
    uname : str
        The user's username.
    pwd : str
        The user's hashed password.
    """

    _ph: argon2.PasswordHasher = argon2.PasswordHasher()

    def __init__(self, uid: int, uname: str, pwd: str, check_store: bool = True):
        self.uid: int = uid
        self.uname: str = uname
        self.pwd: str = pwd
        if check_store:
            self.store()

    def store(self) -> None:
        """
        Stores the user in the server's database.
        """
        con, c = db.connect()
        res = db.fetchone('SELECT pass FROM users WHERE name = ?', self.uname)
        if not res:
            c.execute('INSERT INTO users (name, pass) VALUES (?, ?)', (self.uname, self.pwd, ))
            con.commit()
            self.uid = User.load(self.uname).uid
        elif res[0] != self.pwd:
            c.execute('UPDATE users SET pass = ? WHERE name = ?', (self.pwd, self.uname, ))
        db.close(con)

    def verify(self, pwd: str) -> bool:
        """
        Verify that the given password and the user's password match.
        """
        try:
            return User._ph.verify(self.pwd, pwd)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def __str__(self) -> str:
        return f'{self.uname}#{self.uid}'

    @classmethod
    def load(cls, uname: str) -> Union["User", None]:
        """
        Load the user with the given username from the db.
        """
        res = db.fetchone('SELECT uid, pass FROM users WHERE name = ?', uname)
        if not res:
            return None
        return User(res[0], uname, res[1], check_store=False)

    @classmethod
    def load_all(cls) -> List["User"]:
        """
        Load all users stored in the database.
        """
        return [User(*u, check_store=False) for u in db.fetchall('SELECT * FROM users')]

    @classmethod
    def hash(cls, pwd: str) -> str:
        """
        Hash the given password.
        """
        return User._ph.hash(pwd)

    @classmethod
    def create_prompt(cls) -> "User":
        """
        Create a new user by prompting to the CLI.
        """
        name = input('Enter new username: ')
        while True:
            pwd = getpass('Enter new password: ')
            if pwd == getpass('Confirm new password: '):
                break
            utils.printerr('Passwords don\'t match!')
        return User(-1, name, User.hash(pwd))