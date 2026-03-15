"""
Notification Service - Simulates HR notification when onboarding completes.
"""

from datetime import datetime


def send_hr_notification(developer_profile: dict, stats: dict) -> str:
    """
    Simulate sending an HR email notification.
    Prints to terminal and returns the notification message.
    """
    name = developer_profile.get("name", "Developer")
    role = developer_profile.get("role", "Backend")
    level = developer_profile.get("level", "Junior")
    tech_stack = developer_profile.get("tech_stack", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notification = f"""
╔══════════════════════════════════════════════════════════════╗
║              📧  HR NOTIFICATION EMAIL (SIMULATED)           ║
╠══════════════════════════════════════════════════════════════╣
║  To      : hr@company.com                                    ║
║  CC      : {name.lower().replace(" ", ".")+"@company.com":<52}║
║  Subject : Onboarding Complete — {name:<27}║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Dear HR Team,                                               ║
║                                                              ║
║  This is an automated notification from the AI Onboarding   ║
║  Agent confirming that the following developer has           ║
║  successfully completed their onboarding program.            ║
║                                                              ║
║  Developer  : {name:<47}║
║  Role       : {level} {role:<44}║
║  Tech Stack : {', '.join(tech_stack):<47}║
║  Tasks      : {stats['completed']}/{stats['total']} completed{' '*(43-len(str(stats['completed'])+'/'+str(stats['total'])))}║
║  Completed  : {timestamp:<47}║
║                                                              ║
║  ACTION REQUIRED: Please assign this developer to their      ║
║  team and schedule a sprint onboarding session.              ║
║                                                              ║
║  — AI Onboarding Agent 🤖                                    ║
╚══════════════════════════════════════════════════════════════╝
"""

    print(notification)

    short_msg = (
        f"HR Notification: Developer onboarding completed for {name} "
        f"({level} {role}). Ready for team assignment."
    )
    print(f"\n✅ {short_msg}\n")

    return short_msg
