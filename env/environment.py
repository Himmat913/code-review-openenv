from env.tasks import TASKS
from env.grader import grade
from env.models import Observation, StepResult

class CodeReviewEnv:

    def __init__(self):
        self.task = None
        self.done = False
        self.phase = "issue"

    def reset(self, task_name="easy"):
        self.task = TASKS[task_name]
        self.done = False
        self.phase = "issue"

        return Observation(
            code=self.task["code"],
            language=self.task["language"],
            step="identify_issue"
        ).dict()

    def step(self, action):
        reward = grade(self.task, action)

        # Progression logic
        if self.phase == "issue":
            self.phase = "impact"
        elif self.phase == "impact":
            self.phase = "fix"
        else:
            self.done = True

        obs = Observation(
            code=self.task["code"],
            language=self.task["language"],
            step=self.phase
        )

        return StepResult(
            observation=obs,
            reward=reward,
            done=self.done,
            info={"phase": self.phase}
        ).dict()

    def state(self):
        return {
            "task": self.task,
            "phase": self.phase
        }