from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

# Serve static files at /static
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve index.html at root
from fastapi.responses import FileResponse
@app.get("/")
async def root():
	return FileResponse(os.path.join(static_dir, "index.html"))

class CalcRequest(BaseModel):
	num1: float
	num2: float
	op: str

@app.post("/api/clac")
async def calculate(req: CalcRequest):
	try:
		if req.op == "+":
			result = req.num1 + req.num2
		elif req.op == "-":
			result = req.num1 - req.num2
		elif req.op == "*":
			result = req.num1 * req.num2
		elif req.op == "/":
			if req.num2 == 0:
				raise HTTPException(status_code=400, detail="Division by zero")
			result = req.num1 / req.num2
		else:
			raise HTTPException(status_code=400, detail="Invalid operator")
		return {"result": result}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
	uvicorn.run("calculator:app", host="127.0.0.1", port=8000, reload=True)