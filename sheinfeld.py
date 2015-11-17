#!/usr/bin/env python3

import sys
import os.path

max_iterations = 1*1000*1000

def Usage():
    return "Usage: {} <file>".format(sys.argv[0])

def CheckInputArgumentsOrDie():
    if len(sys.argv) != 2:
        print(Usage())
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("File '{}' doesn't exist.".format(sys.argv[1]))

def DumpFileToArrayOfStrings(filename):
    with open (filename, "r") as my_file:
        return my_file.read().splitlines()

# Handy self-increasing list.
# Idea is shamelessly stolen from http://stackoverflow.com/a/8849909.
class rlist(list):
    def SetDefault(self, default):
        self.default_ = default
        return self
    def reserve(self, size):
        if size > len(self):
            self += [self.default_] * (size - len(self))
    def __setitem__(self, key, value):
        self.reserve(key + 1)
        super(rlist, self).__setitem__(key, value)
    def __getitem__(self, key):
        self.reserve(key + 1)
        return super(rlist, self).__getitem__(key)

def ConvertListOfStringsToListOfIntsOrDie(list_of_strings):
    try:
        return rlist(map(int, list_of_strings))
    except ValueError():
        print("There are non-integers on the first line")
        sys.exit(1)

class IncCommand:
    def __init__(self, register, command_number):
        self.register_index_ = register
        self.command_number_ = command_number

    # Returns index of the next command to run
    def ChangeRegisters(self, registers):
        registers[self.register_index_] += 1
        return self.command_number_ + 1

    def ToString(self):
        return "inc {}".format(self.register_index_)

class DecCommand:
    def __init__(self, register, next_command,command_number):
        self.register_index_ = register
        self.next_command_ = next_command
        self.command_number_ = command_number

    # Returns index of the next command to run
    def ChangeRegisters(self, registers):
        if (registers[self.register_index_] > 0):
            registers[self.register_index_] -= 1
            return self.next_command_
        else:
            return self.command_number_ + 1

    def ToString(self):
        return "dec {} {}".format(self.register_index_, self.next_command_)

if __name__ == "__main__":
    CheckInputArgumentsOrDie()
    lines = DumpFileToArrayOfStrings(sys.argv[1])

    registers = ConvertListOfStringsToListOfIntsOrDie(lines[0].split())
    registers.SetDefault(0)

    commands = rlist().SetDefault(0)
    for i in range(1, len(lines)):
        words = lines[i].split()
        if (words[0] == "inc"):
            if (len(words) != 2):
                print("Line {} does not look like a valid 'inc' command:"
                      .format(i + 1))
                print(lines[i])
                sys.exit(1)

            reg = 0
            try:
                reg = int(words[1])
            except ValueError():
                print("Line {}, not an int".format(i + 1))
                sys.exit(1)

            commands[i] = IncCommand(reg, i)
        elif (words[0] == "dec"):
            if (len(words) != 3):
                print("Line {} does not look like a valid 'dec' command:"
                      .format(i + 1))
                print(lines[i])
                sys.exit(1)

            reg = 0
            next_command = 0
            try:
                reg = int(words[1])
                next_command = int(words[2])
            except ValueError():
                print("Line {}, not an int".format(i + 1))
                sys.exit(1)

            commands[i] = DecCommand(reg, next_command, i)
        else:
            print("Something is not right at line {}".format(i + 1))

    # Main loop
    next_command = 1
    iterations_passed = max_iterations
    halted = 0
    for i in range(0, max_iterations):
        print(commands[next_command].ToString() + "\t" + str(registers))
        next_command = commands[next_command].ChangeRegisters(registers)
        if (next_command >= len(commands)):
            iterations_passed = i + 1
            halted = 1
            break

    print("\nIterations passed: {}".format(iterations_passed))
    if (not halted):
        print("Maximum number of iterations reached")
    print("Registers at the end: " + str(registers))
