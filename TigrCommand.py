class TigrCommand:
    def __init__(self, drawer_command, args):
        self.drawer_command = drawer_command
        self.args = args

    def execute(self, drawer):
        try:
            return drawer.__getattribute__(self.drawer_command)(*self.args)
        except AttributeError:
            raise SyntaxError(f'Command {self.drawer_command} not recognised by drawer')
