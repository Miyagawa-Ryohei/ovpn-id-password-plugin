
from ovpn_idpass_plugin.entity import db, user
from . import auth

def initialize(database : db.Database) -> str:
    database.initialize()
    return create_admin(database)

def create_user(database : db.Database) -> (str, str):
    name = input("Input user name").strip()
    result = database.is_exist(name)
    if result:
        print(name + " has been already existing. please use other user name")
        return create_user(database)

    password = auth.create_password()
    salt = auth.get_random_str(16)
    hashed = auth.to_password_hash(password, salt)
    created = user.User()
    created.name = name
    created.password = hashed
    created.salt = salt
    created.administrator = False
    created.disabled = False
    try:
        database.create_user(created)
        return name, password
    except Exception as e:
        print(f'error has occurred : {e}')
        raise e


def create_admin(database : db.Database) -> str:
    admin = database.get_admin()
    if admin is not None:
        raise Exception("admin user is already exist")
    password = auth.create_password()
    salt = auth.get_random_str(16)
    hashed = auth.to_password_hash(password, salt)
    created = user.User()
    created.name = "admin"
    created.password = hashed
    created.salt = salt
    created.administrator = True
    created.disabled = False
    try:
        database.create_user(created)
        return password
    except Exception as e:
        print(f'error has occurred : {e}')
        raise e

def change_password(database : db.Database) -> (str):
    name = input("Input admin user name").strip()
    password = input("Input admin user password").strip()
    admin = _get_auth_user(name, password, database)
    if admin is None:
        return False

    if not admin.administrator:
        return False

    target = input("which user password is changing? (input user name)").strip()

    try:
        result = database.get_user(target)
        password = auth.create_password()
        salt = auth.get_random_str(16)
        hashed = auth.to_password_hash(password, salt)
        result.password = hashed
        result.salt = salt
        database.update_user(result)
        return password
    except IndexError as e:
        print(f'{target} is not registered')
        raise e


def _get_auth_user(name : str, password : str, database : db.Database) -> user.User | None:
    entry = database.get_user(name)
    hashed = auth.to_password_hash(password, entry.salt)
    if entry.password == hashed:
        return entry
    return None

def auth_user(name : str, password : str, database : db.Database) -> bool:
    entry = database.get_user(name)
    hashed = auth.to_password_hash(password, entry.salt)
    if entry.password == hashed:
        return True
    return False


def read_entry_file(path : str) -> (str, str):
    fp = open(path)
    data = fp.readlines()
    fp.close()
    return data[0].rstrip(), data[1].rstrip()
