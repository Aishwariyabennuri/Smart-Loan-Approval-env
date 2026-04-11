# tasks.py
from enum import Enum

class Task(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

TASK_DESCRIPTIONS = {
    Task.EASY:   "Stable income, good credit, low loan amount",
    Task.MEDIUM: "Stable income, bad credit, high loan amount",
    Task.HARD:   "Unstable income, self-employed, very high loan amount"
}
