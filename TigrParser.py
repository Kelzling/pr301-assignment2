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
        self.current_line = None
        self.current_args = None
        self.drawer_command = None
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
        self.source = raw_source
        for line_number in range(0, len(self.source) - 1):

            try:
                if not self._prepare_line(line_number):
                    continue

                self._parse_line()

                self._prepare_command()

                self._execute_command()
            except Exception as e:
                self.exception_handler.display_and_exit(e, line_number=line_number, line=self.current_line)

    def _prepare_line(self, line_number):
        trimmed_line = self.source[line_number].strip()
        if self._is_line_blank(trimmed_line):
            return False
        else:
            self.current_line = trimmed_line
            return True

    def _is_line_blank(self, line):
        return not line

    def _parse_line(self):
        match = re.findall(self.regex_pattern, self.current_line)
        if match:
            groups = match[0]
            self.command = groups[0].upper()
            if groups[1]:
                self.data = int(round(float(groups[1])))
                """ Parser accepts decimals but silently rounds them in the background - all numbers passed are
                stored as integers"""
            else:
                self.data = None
        else:
            raise SyntaxError(
                f"Invalid Syntax")

    def _prepare_command(self):
        command_info = self.language_commands.get(self.command)
        self.current_args = []
        self.drawer_command = None

        if command_info:
            if len(command_info) > 1:
                self.current_args.append(*command_info[1])
            if self.data:
                self.current_args.append(self.data)
            self.drawer_command = command_info[0]
        else:
            raise SyntaxError(f"Command {self.command} not valid")

    def _execute_command(self):
        try:
            # explodes the created args array into the function that is being called
            # if there is nothing in the array, nothing will be passed! Nice and fancy.
            output = self.drawer.__getattribute__(self.drawer_command)(*self.current_args)
        except AttributeError:
            raise SyntaxError(
                f'Command {self.command} Not recognized by drawer - Command reference mismatch detected')
        else:
            self._log_drawer_output(output)

    def _log_drawer_output(self, output):
        self.__output_log.append(output)
