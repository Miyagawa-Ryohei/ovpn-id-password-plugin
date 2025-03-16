import contextlib

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ovpn_idpass_plugin.entity.user import User
from ovpn_idpass_plugin.entity.db import Database


class SqliteConnector(Database):
    engine: sqlalchemy.Engine
    def connect(self, location: str):
        self.engine = sqlalchemy.create_engine(f'sqlite:///{location}', echo=True)

    @contextlib.contextmanager
    def session(self):
        s = sessionmaker(bind=self.engine)()
        try:
            yield s
        finally:
            s.close()

    def initialize(self):
        User.metadata.create_all(bind=self.engine)

    def is_exist(self, name : str) -> bool:
        try:
            user = self.get_user(name)
            if user is None:
                return False
            else:
                return True
        except IndexError:
            return False

    def create_user(self, user : User) -> bool:
        with self.session() as session:
            try:
                session.add(instance = user)
                session.commit()
                return True
            except Exception as e:
                raise e

    def update_user(self, user : User) -> bool:
        with self.session() as session:
            try:
                u = session.query(User).filter_by(id=user.id).first()
                if u is not None:
                    u.password = user.password
                    u.salt = user.salt
                    session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                raise e

    def get_user(self, name : str) -> User:
        with self.session() as session:
            try:
                user = session.query(User).filter_by(name=name)
                return user[0]
            except:
                raise

    def get_admin(self) -> User | None:
        with self.session() as session:
            try:
                user = session.query(User).filter_by(administrator=True)
                if user.count() == 0:
                    return None
                else:
                    return user[0]
            except:
                raise
