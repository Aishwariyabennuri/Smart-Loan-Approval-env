import os
from openai import OpenAI
from env.loan_env import LoanEnv
from tasks.tasks import TASKS
from graders.grader import compute_score

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

if not API_BASE_URL or not API_KEY:
    raise ValueError("Missing API_BASE_URL or API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)

def get_action_from_llm(state):
    prompt = f"""
You are a loan approval agent.

Decide whether to APPROVE or REJECT the loan based on the user data.

State:
{state}

Answer strictly in one word:
approve or reject
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
    )

    action = response.choices[0].message.content.strip().lower()

    if action not in ["approve", "reject"]:
        action = "reject"

    return action

def run_task(task):
    env = LoanEnv(task)
    state = env.reset()

    rewards = []

    print(f"[START] task={task} env=loan-risk model={MODEL_NAME}")

    for step in range(1, 3):
        action = get_action_from_llm(state)

        state, reward, done, _ = env.step(action)
        rewards.append(reward)

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

        if done:
            break

    score = compute_score(rewards)
    success = score > 0.5
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    for t in TASKS:
        run_task(t)
