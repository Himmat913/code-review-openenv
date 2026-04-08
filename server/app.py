from fastapi import FastAPI
import uvicorn
from env.environment import CodeReviewEnv

app = FastAPI()
env = CodeReviewEnv()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/reset")
def reset(task: str = "easy"):
    return env.reset(task)

@app.post("/step")
def step(action: dict):
    return env.step(action)

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()