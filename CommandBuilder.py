from TigrCommand import TigrCommand

import json


class CommandBuilder:
    def __init__(self, lookup_file_name="command_lookup.json"):
        self._language_commands = self._load_command_lookup(lookup_file_name)

    def _load_command_lookup(self, file_name):
        try:
            with open(file_name, 'r') as json_file:
                # load configurable language reference from file
                return json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:
            raise FileNotFoundError(f"Command Lookup {file_name} not found")

    def prepare_command(self, command_text, data=None):
        command_info = self._language_commands.get(command_text)
        if not command_info:
            raise SyntaxError(f"Command {command_text} not valid")

        drawer_command = command_info[0]
        args = []

        if len(command_info) > 1:
            args.append(*command_info[1])
        if data:
            args.append(data)

        return TigrCommand(drawer_command, args)
