from console import Console
from database import Database


def main():
    db = Database()
    console = Console(db)
    console.start_event_loop()


if __name__ == '__main__':
    main()
