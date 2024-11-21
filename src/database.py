import sys


class _NullType(object):
    def __repr__(self):
        return 'NULL'


NULL = _NullType()


class Database:
    def __init__(self):
        self.transaction_stack = []
        self.database = self.current_transaction = {}
        self.transaction_stack.append(self.database)

    def set(self, key, value):
        self.current_transaction[key] = value

    def get(self, key):
        for transaction in reversed(self.transaction_stack):
            if key not in transaction:
                continue
            return transaction[key]
        return NULL

    def unset(self, key):
        self.current_transaction[key] = NULL

    def counts(self, value):
        count = len(self.find(value))
        return count

    def find(self, value):
        found_keys = []
        changed_keys = []
        for transaction in reversed(self.transaction_stack):
            for key, val in transaction.items():
                if key in changed_keys:
                    continue
                if val == value:
                    found_keys.append(key)
                changed_keys.append(key)
        return found_keys

    def begin(self):
        self.current_transaction = {}
        self.transaction_stack.append(self.current_transaction)

    def rollback(self):
        self.transaction_stack.pop()
        self.current_transaction = self.transaction_stack[-1]

    def commit(self):
        self.transaction_stack[-2] = {
            **self.transaction_stack[-2],
            **self.transaction_stack[-1]
        }
        self.transaction_stack.pop()
        self.current_transaction = self.transaction_stack[-1]


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
            except ValueError:
                continue

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
