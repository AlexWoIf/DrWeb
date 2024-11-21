import sys
from io import StringIO

from console import Console
from database import Database
from null_type import NULL


def test_console_set_get():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('SET KEY VALUE\nGET KEY\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert 'VALUE' in output


def test_console_unset():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('SET KEY VALUE\nUNSET key\nGET key\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert str(NULL) in output


def test_console_counts():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('SET key1 value\nSET key2 value\nCOUNTS value\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert '2' in output


def test_console_find():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('SET key1 value\nSET key2 value\nFIND value\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert 'key1' in output and 'key2' in output


def test_console_begin_rollback_commit():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('BEGIN\nSET key value1\nROLLBACK\nGET key\nBEGIN\n'
                         'SET key value2\nCOMMIT\nGET key\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert (str(NULL) in output and 
            'value1' not in output and 
            'value2' in output)


def test_console_begin_commit_rollback():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('BEGIN\nSET key value1\nCOMMIT\nGET key\nBEGIN\n'
                         'SET key value2\nROLLBACK\nGET key\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert (str(NULL) not in output and 
            'value1' in output and 
            'value2' not in output)


def test_console_begin_rollback_rollback():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('BEGIN\nSET key value1\nROLLBACK\nGET key\nBEGIN\n'
                         'SET key value2\nROLLBACK\nGET key\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert (str(NULL) in output and 
            'value1' not in output and 
            'value2' not in output)


def test_console_invalid_command():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('INVALID_COMMAND\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert 'Invalid command' in output


def test_console_wrong_number_of_arguments():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('SET key\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert 'Wrong number of arguments' in output


def test_console_rollback_or_commit_without_begin():
    db = Database()
    console = Console(db)
    # Mock input and output
    sys.stdin = StringIO('ROLLBACK\n')
    sys.stdout = StringIO()
    console.start_event_loop()
    sys.stdout.seek(0)
    output = sys.stdout.read()
    assert 'ROLLBACK or COMMIT requires a started transaction' in output
