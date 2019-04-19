
from tools.command_line_tools import CLIArgument



def example_callback(arg):
    print(f"You called me with arg: {arg}")

def print_help():
    print(f"Help message or something")


test_arg = CLIArgument("parent")
def initialize():
    help = test_arg.add_argument("help", print_help)
    test = test_arg.add_argument("test", example_callback)

def start_cli_tool():

    while True:
        try:
            cmd = input("Enter a command> ")
            print(f"Command Entered: {cmd}")
            test_arg.parse_argument(cmd)
        except Exception as e:
            print(f"An exception occurred in cli tool: {e}")

if __name__ == "__main__":
    initialize()
    start_cli_tool()
    # Examples:
    # > test foobar
    # > help