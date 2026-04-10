from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from env.loan_env import LoanEnv

app = FastAPI()
env = LoanEnv()

class ActionRequest(BaseModel):
    action: str

@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    return {"state": env.current_state}


# ✅ ADD THIS MAIN FUNCTION (VERY IMPORTANT)
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ ADD THIS ENTRY POINT
if __name__ == "__main__":
    main()
