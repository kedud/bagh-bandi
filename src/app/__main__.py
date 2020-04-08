import os, sys
sys.path.insert(0, os.getcwd())

from src.app.network_user_interface import NetworkUserInterface


def main():
    ui = NetworkUserInterface()
    ui.play()


# main
if __name__ == '__main__':
    main()