from null_type import NULL


class Database:
    def __init__(self):
        self.transaction_stack = []
        self.current_transaction = {}
        self.transaction_stack.append(self.current_transaction)

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
                if transaction is not self.transaction_stack[0]:
                    changed_keys.append(key)
        return found_keys

    def begin(self):
        self.current_transaction = {}
        self.transaction_stack.append(self.current_transaction)

    def rollback(self):
        self.current_transaction = self.transaction_stack[-2]
        self.transaction_stack.pop()

    def commit(self):
        self.transaction_stack[-2] = {
            **self.transaction_stack[-2],
            **self.transaction_stack[-1]
        }
        self.transaction_stack.pop()
        self.current_transaction = self.transaction_stack[-1]
