"""Contains sqlite3 wrapper functions"""

import sqlite3
from typing import List, Tuple, Optional, Any, Union

from lib import params

def connect(db_path: str = params.DB_PATH) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Creates a connection to the sqlite db.
    
    Returns
    -------
    Tuple[sqlite3.Connection, sqlite3.Cursor]
        A tuple consisting of both the connection to the db and a cursor for the
        sqlite db.
    """
    con = sqlite3.connect(db_path)
    return (con, con.cursor())

def close(con: sqlite3.Connection) -> None:
    """
    Closes the connection to the sqlite db.

    Parameters
    ----------
    con : sqlite3.Connection
        The connection to the db.
    """
    con.commit()
    con.close()

def exec(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> None:
    """
    Opens a connection, executes the given query and closes the connection again.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters, i.e. '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    if arti:
        close(con)

def fetchone(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> Union[Tuple[Any], None]:
    """
    Opens a connection, executes the query and returns the first result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db. 
    
    Returns
    -------
    Union[Tuple[Any], None]
        Returns the first result (if any).
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchone()
    if arti:
        close(con)
    return res

def fetchall(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> List[Tuple[Any]]:
    """
    Opens a connection, executes the query and returns all results.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        The arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db.
    
    Returns
    -------
    List[Tuple[Any]]
        Returns resulting rows (or empty list)
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchall()
    if arti:
        close(con)
    return res

def exists(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> bool:
    """
    Checks whether or not the given query yields a result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters; '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    bool
        Whether or not the query has yielded a result.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = bool(c.fetchone())
    if arti:
        close(con)
    return res

def setup(db_path: str = params.DB_PATH) -> None:
    """
    Initializes the database: creates all tables, etc.
    """
    con, c = connect(db_path)
    c.execute('''CREATE TABLE users (
                    uid     INTEGER PRIMARY KEY,
                    name    VARCHAR(32) NOT NULL,
                    pass    VARCHAR(77) NOT NULL
                 )''')
    close(con)