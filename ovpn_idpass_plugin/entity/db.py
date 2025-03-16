from abc import abstractmethod
from ovpn_idpass_plugin.entity.user import User


class Database:
    @abstractmethod
    def is_exist(self, user : str) -> bool:
        pass

    @abstractmethod
    def create_user(self, user : User) -> bool:
        pass

    @abstractmethod
    def update_user(self, user : User) -> bool:
        pass

    @abstractmethod
    def get_user(self, user : str) -> User:
        pass

    @abstractmethod
    def get_admin(self) -> User | None:
        pass

    @abstractmethod
    def initialize(self):
        pass
