import os.path
import sys
from ovpn_idpass_plugin.usecase import user
from ovpn_idpass_plugin.adapter.sqlite import SqliteConnector
def main():
    db = SqliteConnector()
    db.connect(os.path.join(os.path.dirname(__file__),"assets","db.sqlite"))
    arg = sys.argv[1]

    match arg:
        case "initialize":
            password = user.initialize(db)
            print(f'admin password : {password}')

        case "create_user":
            username, password = user.create_user(db)
            print(f'username : {username}')
            print(f'password : {password}')

        case "change_password":
            password = user.change_password(db)
            print(f'new password : {password}')

        case _:
            name, password = user.read_entry_file(arg)
            res = user.auth_user(name, password, db)
            if res:
                print("auth is success")
                sys.exit(0)
            else:
                print("auth is failed")
                sys.exit(1)

if __name__ == '__main__':
    main()
