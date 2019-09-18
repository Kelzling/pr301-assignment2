from TIGr import AbstractParser
import re
import json

"""
Uses Regular Expressions in Parser, Parsed from Configurable Lookup Table
Written by Kelsey Vavasour and Thomas Baines
"""


class TigrParser(AbstractParser):
    def __init__(self, drawer):
        super().__init__(drawer)
        self.regex_pattern = r'(^[a-zA-Z]\b)\s+?(-?\b\d+\.?\d?\b)?\s*?([#|//].*)?$'
        self.__output_log = []
        self.current_line_number = None
        self.current_line = None
        self.current_args = None
        self.drawer_command = None
        try:
            with open("command_lookup.json", 'r') as json_file:
                # load configurable language reference from file
                self.language_commands = json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:  # This error is thrown to be caught further up the stack
            raise FileNotFoundError(f"Error loading commands from file: {e}")

    @property
    def output_log(self):
        # readonly
        return self.__output_log

    def parse(self, raw_source):
        if type(raw_source) == str:  # defensively handles edge case where a single command was passed as a string
            raw_source = [raw_source]
        self.source = raw_source
        for line_number in range(0, len(self.source)-1):
            self.current_line_number = line_number
            if not self._prepare_line():
                continue

            self._parse_line()

            self._prepare_command()

            try:
                self._execute_command()
            except Exception as e:  # intercept error thrown that wasn't caught and appending the line number
                # that caused it
                args = e.args
                if args:
                    arg0 = args[0]
                else:
                    arg0 = str()
                arg0 += f' at source line {self.current_line_number}'
                e.args = (arg0, *args[1:])
                raise

    def _prepare_line(self):
        trimmed_line = self.source[self.current_line_number].strip()
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
            # Raises SyntaxError to indicate that the line line_number didn't match the required pattern
            raise SyntaxError(
                f"line number {self.current_line_number} contains invalid syntax: \n\t{self.current_line}")

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
            raise SyntaxError(f"Command {self.command} on line {self.current_line_number} not recognized")

    def _execute_command(self):
        try:
            # explodes the created args array into the function that is being called
            # if there is nothing in the array, nothing will be passed! Nice and fancy.
            output = self.drawer.__getattribute__(self.drawer_command)(*self.current_args)
        except AttributeError as e:
            raise SyntaxError(
                f'Command {self.command} Not recognized by drawer - Command reference mismatch detected')
        else:
            self._log_drawer_output(output)

    def _log_drawer_output(self, output):
        self.__output_log.append(output)
