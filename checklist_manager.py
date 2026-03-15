"""
Checklist Manager - Tracks onboarding task completion and progress.
"""


def calculate_progress(completed_tasks: list[bool]) -> dict:
    """Calculate completion statistics."""
    total = len(completed_tasks)
    completed = sum(completed_tasks)
    remaining = total - completed
    percentage = int((completed / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "remaining": remaining,
        "percentage": percentage,
        "is_complete": completed == total and total > 0,
    }


def get_progress_label(percentage: int) -> str:
    """Return a motivational label based on progress percentage."""
    if percentage == 0:
        return "🚀 Let's get started!"
    elif percentage < 25:
        return "🌱 Just warming up..."
    elif percentage < 50:
        return "📈 Good momentum!"
    elif percentage < 75:
        return "⚡ Halfway there, keep going!"
    elif percentage < 100:
        return "🔥 Almost done, final stretch!"
    else:
        return "🎉 Onboarding Complete!"


def get_progress_color(percentage: int) -> str:
    """Return a color hex for the progress bar."""
    if percentage < 25:
        return "#ef4444"   # red
    elif percentage < 50:
        return "#f97316"   # orange
    elif percentage < 75:
        return "#eab308"   # yellow
    elif percentage < 100:
        return "#3b82f6"   # blue
    else:
        return "#22c55e"   # green


def get_next_task(tasks: list[str], completed_tasks: list[bool]) -> str | None:
    """Return the next uncompleted task."""
    for task, done in zip(tasks, completed_tasks):
        if not done:
            return task
    return None
