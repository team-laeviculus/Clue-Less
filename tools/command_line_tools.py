import pprint
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


"""
Command Line Tools: Helper classes for easily creating command line options.
Uses the Builder Design pattern.
"""

# class Director(object):
#     """
#     Creates a new Command Line argument using the builder interface.
#     """
#
#     def __init__(self):
#         self.__builder = None
#     def construct(self, builder):
#         self.__builder = builder
#         self.__builder.
class CLIArgument(object):
    """
    CLIArgument: Because I couldnt find a good library to do this I have to
    implement command line parsing from scratch. Hopefully this ends up better
    then a ton of 'if', 'else' statements.
    """

    def __init__(self, argname):
        self.__argname = argname
        self.__argdata = dict()

    def add_argument(self, argname, action_type=None):
        '''
        :param argname: a name for the argument in the argument map
        :param action_type: A function or whatever you want to store in the argument name
        :return : The current command line parser object

        Adds an argument to the argument table of the class along with a callback
        function or something you want the argument to do
        '''
        #TODO better action types
        self.__argdata[argname] = action_type
        return self

    def parse_argument(self, args):
        args = args.split()
        print(f"Args passed: {args}")
        if len(args) >= 1:
            if args[0] in self.__argdata:
                print(f"Argument {args[0]} Found!")
                # How tf do I handle data???
                if len(args) == 1:
                    self.__argdata[args[0]]()
                elif len(args) > 1:
                    #TODO This will only work for one argument
                    self.__argdata[args[0]](args[1])
                else:
                    print("Unhandled")
            else:
                print(f"Argument {args[0]} NOT Found")

    def __str__(self):
        out = io.StringIO()
        out.writelines(f"{self.__argname}:\n")
        pprint.pprint(self.__argdata, out)
        return out.getvalue()
    # def __repr__(self):
    #     return

    def __getitem__(self, item):
        return self.__argdata[item]


if __name__ == "__main__":
    print("Starting test")
    # Example usage

    test = CLIArgument("test")
    a = test.add_argument("a", lambda : print("call to a"))
    b = test.add_argument("b", lambda x: print(f"call to b: {x}"))
    b.add_argument("b_a", lambda : print("Call to sub function on b_a"))
    print(f"Done: {test}")
    test["a"]()
    test["b"]("Hello world")
    test["b_a"]()


