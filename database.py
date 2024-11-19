import sys


NULL = 'NULL'


class Database:
    def __init__(self):
        self.transaction_stack = []
        self.current_transaction = {}

    def set(self, key, value):
        self.current_transaction[key] = value

    def get(self, key):
        return self.current_transaction.get(key, NULL)

    def unset(self, key):
        self.current_transaction.pop(key, NULL)

    def counts(self, value):
        count = sum(1 for v in self.current_transaction.values() if v == value)
        return count

    def find(self, value):
        keys = [key for key, val in self.current_transaction.items()
                if val == value]
        return keys

    def begin(self):
        self.transaction_stack.append(self.current_transaction.copy())

    def rollback(self):
        self.current_transaction = self.transaction_stack.pop()

    def commit(self):
        self.transaction_stack.pop()


class Console():
    def __init__(self, db):
        self.db = db
        self.commands = {
            'SET': self.db.set,
            'GET': self.db.get,
            'UNSET': self.db.unset,
            'COUNTS': self.db.counts,
            'FIND': self.db.find,
            'BEGIN': self.db.begin,
            'ROLLBACK': self.db.rollback,
            'COMMIT': self.db.commit,
            'END': sys.exit,
        }

    def start_event_loop(self):
        while True:
            try:
                command, *args = input('> ').split()
            except EOFError:
                break

            try:
                result = self.commands[command.upper()](*args)
                if result is None:
                    continue
                print(result)
            except KeyError:
                print('Invalid command')
                continue
            except TypeError:
                print('Wrong number of arguments')
                continue
            except IndexError:
                print('ROLLBACK or COMMIT requires a started transaction')
                continue


def main():
    db = Database()
    console = Console(db)
    console.start_event_loop()


if __name__ == '__main__':
    main()
