from TIGr import AbstractParser
from CommandBuilder import CommandBuilder
import re

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
            self.command_builder = CommandBuilder()
        except Exception as e:
            self.exception_handler.display_and_exit(e)

    @property
    def output_log(self):
        # readonly
        return self.__output_log

    def parse(self, raw_source):
        if type(raw_source) == str:  # defensively handles edge case where a single command was passed as a string
            raw_source = [raw_source]

        for line_number in range(0, len(raw_source) - 1):
            current_line = self.__prepare_line(raw_source[line_number])
            if self.__is_line_blank(current_line):
                continue

            try:
                command, data = self.__parse_line(current_line)

                prepared_command = self.command_builder.prepare_command(command, data)

                output = prepared_command.execute(self.drawer)
                self._log_drawer_output(output)
            except Exception as e:
                self.exception_handler.display_and_exit(e, line_number=line_number, line=current_line)

    def __prepare_line(self, line):
        return line.strip()

    def __is_line_blank(self, line):
        return not line

    def __parse_line(self, line):
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

    def _log_drawer_output(self, output):
        self.__output_log.append(output)
