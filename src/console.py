import sys


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
