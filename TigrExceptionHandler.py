import sys

class TigrExceptionHandler:
    def update_exception(self, e, line_number, line=""):
        args = e.args
        if args:
            arg0 = args[0]
        else:
            arg0 = str()
        arg0 = f'Error on Line {line_number}: {line}\n\t' + arg0
        e.args = (arg0, *args[1:])

        return e

    def display_and_exit(self, e):
        print("TIGr encountered an error and had to exit", file=sys.stderr)
        print(*e.args, file=sys.stderr)
        exit(1)