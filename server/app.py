from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import uvicorn
from env.loan_env import LoanEnv

app = FastAPI()

class ActionRequest(BaseModel):
    action: str
    task: str = "easy"

    @validator("action")
    def validate_action(cls, v):
        if v not in ("approve", "reject"):
            raise ValueError("action must be 'approve' or 'reject'")
        return v

@app.post("/reset")
def reset(task:Task= Task.EASY):
    env = LoanEnv(task=task)      
    app.state.env = env            
    return {"state": env.reset()}

@app.post("/step")
def step(req: ActionRequest):
    env = getattr(app.state, "env", None)
    if env is None or env.current_state is None:
        raise HTTPException(status_code=400, detail="Call /reset first")
    state, reward, done, info = env.step(req.action)
    return {"state": state, "reward": reward, "done": done, "info": info}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860)  
