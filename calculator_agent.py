from fastmcp import FastMCP


app = FastMCP("calculator")


@app.tool()
def addition(a: int, b: int):
    """
    this function is used to add two variables
    """
    return a + b


@app.tool()
def subtraction(a: int, b: int):
    """
    this function is used to subtract two variables
    """
    return a - b


@app.tool()
def multiplication(a: int, b: int):
    """
    this function is used to multiply two variables
    """
    return a * b


@app.tool()
def division(a: int, b: int):
    """
    this function is used to divide two variables
    """
    return a / b


if __name__ == "__main__":
    # app.run(transport="http", host="0.0.0.0", port=8000)
    app.run()
