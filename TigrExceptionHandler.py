import sys


class TigrExceptionHandler:
    def __init__(self, exit_message):
        self.exit_message = exit_message

    def display_and_exit(self, e, *messages, line_number=None, line=''):
        print(self.exit_message, file=sys.stderr)
        if messages:
            print(*messages, file=sys.stderr)
        if line_number is not None:
            line_message = f'Error on Line {line_number}: {line}'
            print(line_message, file=sys.stderr)
        print(e)
        exit(1)
