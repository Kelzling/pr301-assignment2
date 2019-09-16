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
        try:
            with open("command_lookup.json", 'r') as json_file:
                # load configurable language reference from file
                self.language_commands = json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:  # This error is thrown to be caught further up the stack
            raise FileNotFoundError(f"Error loading commands from file: {e}")

    def parse(self, raw_source):
        if type(raw_source) == str:  # defensively handles edge case where a single command was passed as a string
            raw_source = [raw_source]
        self.source = raw_source
        for line_number in range(0, len(self.source)-1):
            trimmed_line = self.source[line_number].strip()
            if not trimmed_line:
                continue
            match = re.findall(self.regex_pattern, trimmed_line)
            if match:
                groups = match[0]
                self.command = groups[0].upper()
                if groups[1]:
                    self.data = int(round(float(groups[1])))
                    """ Parser accepts decimals but silently rounds them in the background - all numbers passed are
                    stored as integers"""
                else:
                    self.data = None

                command_info = self.language_commands.get(self.command)
                if command_info:
                    args = []
                    if len(command_info) > 1:
                        args.append(*command_info[1])
                    if self.data:
                        args.append(self.data)

                    # explodes the created args array into the function that is being called
                    # if there is nothing in the array, nothing will be passed! Nice and fancy.
                    try:
                        self.drawer.__getattribute__(command_info[0])(*args)
                    except AttributeError as e:
                        raise SyntaxError(
                            f'Command {self.command} Not recognized by drawer - Command reference mismatch detected')
                    except Exception as e:  # intercept error thrown that wasn't caught and appending the line number
                        # that caused it
                        args = e.args
                        if args:
                            arg0 = args[0]
                        else:
                            arg0 = str()
                        arg0 += f' at source line {line_number}'
                        e.args = (arg0, *args[1:])
                        raise

                else:
                    raise SyntaxError(f"Command {self.command} on line {line_number} not recognized")
            else:
                # Raises SyntaxError to indicate that the line line_number didn't match the required pattern
                raise SyntaxError(f"line number {line_number} contains invalid syntax: \n\t{trimmed_line}")
