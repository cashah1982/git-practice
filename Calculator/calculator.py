from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
import uvicorn
import os

app = FastAPI(title="Calculator API")

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))


class CalcRequest(BaseModel):
    num1: float
    num2: float
    op: str

    @field_validator("op")
    @classmethod
    def validate_op(cls, v: str) -> str:
        if v not in ("+", "-", "*", "/"):
            raise ValueError(f"Invalid operator: {v}")
        return v


OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


@app.post("/api/calc")
async def calculate(req: CalcRequest):
    if req.op == "/" and req.num2 == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    result = OPERATIONS[req.op](req.num1, req.num2)
    return {"result": result}


if __name__ == "__main__":
    uvicorn.run("calculator:app", host="127.0.0.1", port=8000, reload=True)
