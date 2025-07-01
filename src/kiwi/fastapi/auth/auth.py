from abc import ABC, abstractmethod


class AuthInterface(ABC):
    @abstractmethod
    def get_user(self, request) -> any:
        pass

    @abstractmethod
    def is_logged_in(self, user: any) -> bool:
        pass

    @abstractmethod
    def override_config_for_user(self, user: any, config: dict) -> dict:
        pass

    @abstractmethod
    def login_form(self) -> str:
        pass

    @abstractmethod
    def login_handler(self, request) -> str:
        pass

    @abstractmethod
    def callback_handler(self, request) -> str:
        pass

    @abstractmethod
    def logout_handler(self, request) -> str:
        pass

class NoAuth(AuthInterface):
    def get_user(self, request) -> any:
        return {}

    def is_logged_in(self, user: any) -> bool:
        return True

    def override_config_for_user(self, user: any, config: dict) -> dict:
        return config

    def login_form(self) -> str:
        return ''

    def login_handler(self, request) -> str:
        return 'No login required'

    def callback_handler(self, request) -> str:
        return 'No login required'

    def logout_handler(self, request) -> str:
        return 'No login required'
