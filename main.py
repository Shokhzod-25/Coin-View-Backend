import uvicorn
from src import create_app

app = create_app()

if __name__ == "__main__":
	uvicorn.run("main:app", reload=True, host="0.0.0.0", port=9000)
