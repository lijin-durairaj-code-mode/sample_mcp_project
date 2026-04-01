from fastmcp import FastMCP


app = FastMCP("calculator")


@app.tool()
def addition(a: int, b: int):
    return a + b


@app.tool()
def subtraction(a: int, b: int):
    return a - b


@app.tool()
def multiplication(a: int, b: int):
    return a * b


@app.tool()
def division(a: int, b: int):
    return a / b


if __name__ == "__main":
    app.run(transport="http", host="0.0.0.0", port=8000)
