from TIGr import AbstractParser
import re
import json

"""
Uses Regular Expressions in Parser, Parsed from Configurable Lookup Table
Written by Kelsey Vavasour and Thomas Baines
Refactored by Kelsey Vavasour
"""


class TigrParser(AbstractParser):
    def __init__(self, drawer, exception_handler):
        super().__init__(drawer)
        self.regex_pattern = r'(^[a-zA-Z]\b)\s+?(-?\b\d+\.?\d?\b)?\s*?([#|//].*)?$'
        self.__output_log = []
        self.exception_handler = exception_handler
        try:
            with open("command_lookup.json", 'r') as json_file:
                # load configurable language reference from file
                self.language_commands = json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:
            self.exception_handler.display_and_exit(e, "Error loading commands from file")

    @property
    def output_log(self):
        # readonly
        return self.__output_log

    def parse(self, raw_source):
        if type(raw_source) == str:  # defensively handles edge case where a single command was passed as a string
            raw_source = [raw_source]

        for line_number in range(0, len(raw_source) - 1):
            current_line = self._prepare_line(raw_source[line_number])
            if self._is_line_blank(current_line):
                continue

            try:
                command, data = self._parse_line(current_line)

                prepared_command = self._prepare_command(command, data)

                self._execute_command(prepared_command)
            except Exception as e:
                self.exception_handler.display_and_exit(e, line_number=line_number, line=current_line)

    def _prepare_line(self, line):
        return line.strip()

    def _is_line_blank(self, line):
        return not line

    def _parse_line(self, line):
        match = re.findall(self.regex_pattern, line)
        if match:
            groups = match[0]
            command = groups[0].upper()
            if groups[1]:
                data = int(round(float(groups[1])))
                """ Parser accepts decimals but silently rounds them in the background - all numbers passed are
                stored as integers"""
            else:
                data = None

            return command, data
        else:
            raise SyntaxError(
                f"Invalid Syntax")

    def _prepare_command(self, command, data):
        command_info = self.language_commands.get(command)
        self.current_args = []
        self.drawer_command = None

        if command_info:
            command = {'drawer_command': command_info[0], 'args': []}

            if len(command_info) > 1:
                command['args'].append(*command_info[1])
            if data:
                command['args'].append(data)
            # self.drawer_command = command_info[0]

            return command
        else:
            raise SyntaxError(f"Command {command} not valid")

    def _execute_command(self, prepared_command):
        try:
            # explodes the created args array into the function that is being called
            # if there is nothing in the array, nothing will be passed! Nice and fancy.
            output = self.drawer.__getattribute__(prepared_command['drawer_command'])(*prepared_command['args'])
        except AttributeError:
            raise SyntaxError(
                f'Command {prepared_command["drawer_command"]}' +
                'Not recognized by drawer - Command reference mismatch detected')
        else:
            self._log_drawer_output(output)

    def _log_drawer_output(self, output):
        self.__output_log.append(output)
