import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

ENV_URL = "http://127.0.0.1:7860"
TASKS = ["easy", "medium", "hard"]

def get_action(code):
    prompt = f"""
Analyze the following code and respond STRICTLY in this format:

issue: <short issue type>
impact: <what problem it causes>
fix: <how to fix it>

Code:
{code}
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150
    )

    text = res.choices[0].message.content.lower()

    # Default fallback
    action = {
        "issue": "unknown",
        "impact": "unknown",
        "fix": "unknown"
    }

    # Simple parsing
    for line in text.split("\n"):
        if "issue:" in line:
            action["issue"] = line.split("issue:")[-1].strip()
        elif "impact:" in line:
            action["impact"] = line.split("impact:")[-1].strip()
        elif "fix:" in line:
            action["fix"] = line.split("fix:")[-1].strip()

    return action


for task in TASKS:
    print(f"[START] task={task} env=code-review model={MODEL_NAME}")

    rewards = []
    steps = 0

    obs = requests.post(f"{ENV_URL}/reset", json={"task": task}).json()

    for step in range(1, 6):
        code = obs["code"]

        action = get_action(code)

        result = requests.post(f"{ENV_URL}/step", json=action).json()

        reward = result["reward"]
        done = result["done"]

        rewards.append(reward)
        steps = step

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

        if done:
            break

        obs = result["observation"]

    success = sum(rewards) > 1.5
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")