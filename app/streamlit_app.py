from utils.theme import apply_theme
from state.session_manager import SessionManager
from navigation.router import AppRouter


def initialize():

    apply_theme()

    SessionManager.initialize()


def main():

    initialize()

    router = AppRouter()

    router.render()


if __name__ == "__main__":

    main()