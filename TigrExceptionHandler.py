class TigrExceptionHandler:
    def update_exception(self, e, line_number, line):
        args = e.args
        if args:
            arg0 = args[0]
        else:
            arg0 = str()
        arg0 = f'Error on Line {line_number}: {line}\n\t' + arg0
        e.args = (arg0, *args[1:])

        return e
