# mcp dev ./my_server.py
# MCP Inspector v0.12.0
# Command: python
# Arguments: ./my_server.py

# sse
# 1st command prompt: python my_server.py
# 2nd command prompt: fastmcp dev my_server.py

from fastmcp import FastMCP

# Instantiate the server, giving it a name
mcp = FastMCP(
   name="My First MCP Server",
   instructions="This server is meant to demonstrate the working of the Model Context Protocol.",
)

print("FastMCP server object created.")

# ------------------- Add tools

@mcp.tool()
def Greeting(name: str) -> str:
    """Returns a simple greeting."""
    return f"Hello, {name}!"

@mcp.tool()
def Add(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

@mcp.tool()
def Subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@mcp.tool()
def Multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def Divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

print("Tools 'Greeting', 'Add', 'Subtract', 'Divide' and 'Multiply' added.")

# ------------------- Add resources

APP_CONFIG = {"theme": "dark", "version": "1.1", "feature_flags": ["new_dashboard"]}

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return APP_CONFIG

print("Resource 'data://config' added.")

# ------------------- Add template
USER_PROFILES = {
    101: {"name": "Alice", "status": "active"},
    102: {"name": "Bob", "status": "inactive"},
}

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by their ID."""
    # The {user_id} from the URI is automatically passed as an argument
    return USER_PROFILES.get(user_id, {"error": "User not found"})

print("Resource template 'users://{user_id}/profile' added.")

# ------------------- Add Prompt

@mcp.prompt()
def Calculator_Prompt(a: float, b: float, operation: str) -> str:
    """Prompt for a calculation and return the result."""
    if operation == "Add":
        return f"The result of adding {a} and {b} is {Add(a, b)}"
    elif operation == "Subtract":
        return f"The result of subtracting {b} from {a} is {Subtract(a, b)}"
    elif operation == "Multiply":
        return f"The result of multiplying {a} and {b} is {Multiply(a, b)}"
    elif operation == "Divide":
        try:
            return f"The result of dividing {a} by {b} is {Divide(a, b)}"
        except ValueError as e:
            return str(e)
    else:
        return "Invalid operation. Please choose Add, Subtract, Multiply, or Divide."

print("Prompt 'Calculator' added.")

# --------- Python Execution: STDIO

if __name__ == "__main__":
    print("\n--- Starting FastMCP Server via __main__ ---")

   # according to Render documentation, the default value of PORT is 10000
   # https://render.com/docs/web-services#port-binding
    mcp.run(transport="sse", host="0.0.0.0", port=10000)

