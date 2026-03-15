"""
Onboarding Agent - Core AI Logic
Handles knowledge retrieval and personalized onboarding path generation.
"""

from __future__ import annotations

import json
import os
from datetime import datetime


# ──────────────────────────────────────────────
# Knowledge Retrieval System
# ──────────────────────────────────────────────

def load_knowledge_base() -> dict:
    """Load the company knowledge base from JSON."""
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
    with open(kb_path, "r") as f:
        return json.load(f)


def search_knowledge_base(query: str, knowledge_base: dict) -> dict | None:
    """
    Search the knowledge base for a relevant answer.
    Uses keyword matching to find the best article.
    Returns the best matching article or None.
    """
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for topic, data in knowledge_base.items():
        score = sum(
            1 for keyword in data.get("keywords", [])
            if keyword.lower() in query_lower
        )
        if score > best_score:
            best_score = score
            best_match = data

    return best_match if best_score > 0 else None


def get_ai_response(user_message: str, developer_profile: dict, knowledge_base: dict) -> str:
    """
    Generate a contextual AI response to the developer's question.
    Blends profile context with knowledge base results.
    """
    name = developer_profile.get("name", "Developer")
    role = developer_profile.get("role", "")
    level = developer_profile.get("level", "")

    # Greetings
    greet_keywords = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]
    if any(g in user_message.lower() for g in greet_keywords):
        return (
            f"👋 Hi {name}! I'm your AI Onboarding Assistant. Great to have you onboard as a "
            f"**{level} {role}**!\n\n"
            "I can help you with:\n"
            "- 🛠️ Setting up your environment\n"
            "- 📁 Accessing repositories\n"
            "- 🏗️ Understanding system architecture\n"
            "- 📏 Coding standards & best practices\n"
            "- 🔒 Security policies\n"
            "- 🚀 Deployment & DevOps\n\n"
            "What would you like to know? Ask me anything!"
        )

    # Search knowledge base
    result = search_knowledge_base(user_message, knowledge_base)

    if result:
        response = f"### 📚 {result['title']}\n\n{result['content']}"
        # Add role-specific tip
        if role == "Backend" and "backend" not in result["title"].lower():
            response += f"\n\n> 💡 **Tip for {level} Backend Devs**: Start with the `platform-backend` repo and get the API running locally first."
        elif role == "Frontend" and "frontend" not in result["title"].lower():
            response += f"\n\n> 💡 **Tip for {level} Frontend Devs**: Make sure Node.js 18+ is installed before running `npm install`."
        elif role == "DevOps":
            response += f"\n\n> 💡 **DevOps Tip**: Check the `infra/` repo for all Terraform and Helm configurations."
        return response

    # Fallback with suggestions
    suggestions = [
        "How do I set up my development environment?",
        "What is the system architecture?",
        "Where can I find coding standards?",
        "How do I run the backend service?",
        "What are the security policies?",
    ]
    suggestions_str = "\n".join(f"- {s}" for s in suggestions)
    return (
        f"I don't have a specific answer for that yet, {name}. 🤔\n\n"
        "Here are some topics I *can* help with:\n"
        f"{suggestions_str}\n\n"
        "You can also reach out to your team lead or check the #engineering Slack channel!"
    )


# ──────────────────────────────────────────────
# Personalized Onboarding Path Generator
# ──────────────────────────────────────────────

ONBOARDING_PATHS = {
    "Backend": {
        "Intern": [
            "✅ Complete company security & compliance training",
            "🛠️ Set up Node environment",
            "📁 Clone repository",
            "🐳 Run local server",
            "📖 Review backend architecture doc",
            "📏 Read API standards",
            "🐛 Complete starter bug fix",
        ],
        "Junior": [
            "✅ Complete company security & compliance training",
            "🛠️ Set up full development environment",
            "📁 Clone and explore all backend repositories",
            "🏗️ Deep dive into system architecture & API design",
            "🐳 Run and debug backend services locally",
            "🧪 Write unit & integration tests for a new endpoint",
            "🔧 Implement a small feature end-to-end",
            "🚀 Deploy feature to staging environment",
            "👥 Lead your first sprint story",
        ],
        "Senior": [
            "✅ Complete company security & compliance training",
            "🏗️ Architecture deep-dive with principal engineer",
            "📁 Access and review all backend repositories",
            "🔒 Review security policies & data handling practices",
            "🛠️ Set up advanced local environment (includes Kafka, k8s)",
            "💡 Propose improvements to an existing microservice",
            "🔧 Lead implementation of a medium-complexity feature",
            "👥 Conduct code review for junior developers",
            "📊 Establish first technical initiatives with team lead",
        ],
    },
    "Frontend": {
        "Intern": [
            "✅ Complete company security & compliance training",
            "🛠️ Install Node.js 18+, npm, and Git",
            "📁 Clone platform-frontend repository",
            "📦 Run npm install and start the dev server",
            "🎨 Read UI component library documentation (Storybook)",
            "⚡ Build your first React component",
            "🧪 Write a Jest unit test for your component",
            "🐛 Fix a UI bug from the 'good-first-issue' list",
        ],
        "Junior": [
            "✅ Complete company security & compliance training",
            "🛠️ Set up frontend dev environment with all tools",
            "📁 Clone frontend repo and explore project structure",
            "🎨 Review design system in Figma",
            "🔗 Integrate a new API endpoint into the UI",
            "📱 Implement a responsive feature with mobile support",
            "🧪 Write component and integration tests",
            "🚀 Deploy feature to staging and verify",
            "👥 Present your first feature in team demo",
        ],
        "Senior": [
            "✅ Complete company security & compliance training",
            "🏗️ Review frontend architecture",
            "🎨 Access design system",
            "🚀 Understand deployment pipeline",
            "📖 Review PR guidelines",
        ],
    },
    "DevOps": {
        "Intern": [
            "✅ Complete company security & compliance training",
            "🐳 Set up Docker and Docker Compose",
            "☸️ Learn Kubernetes basics (pods, deployments, services)",
            "📁 Clone the infra repository",
            "⚙️ Read CI/CD pipeline documentation",
            "🔧 Run a local Kubernetes cluster with minikube",
            "🚀 Deploy a sample service to staging",
            "📊 Set up basic monitoring with Datadog",
        ],
        "Junior": [
            "✅ Complete company security & compliance training",
            "🛠️ Set up full local infra tooling (Terraform, kubectl, Helm)",
            "📁 Clone and understand infra & all service repos",
            "☸️ Deep-dive into Kubernetes cluster architecture",
            "🔧 Modify a Helm chart for a service",
            "⚙️ Add a new step to a GitHub Actions workflow",
            "🚀 Full deploy cycle: staging → production",
            "🔒 Review cloud security configurations (IAM, VPC)",
        ],
        "Senior": [
            "✅ Complete company security & compliance training",
            "🏗️ Infrastructure architecture review with principal SRE",
            "📁 Audit all infrastructure repositories",
            "🔒 Security posture review (AWS IAM, SIEM, compliance)",
            "☸️ Kubernetes cluster optimization assessment",
            "⚙️ Design improvement for CI/CD pipeline",
            "💡 Propose and implement an infrastructure initiative",
            "📊 Set up SLOs/SLAs with alerting runbooks",
            "👥 Lead incident response drill with the team",
        ],
    },
}


def generate_onboarding_path(profile: dict) -> list[str]:
    """Generate a personalized onboarding path based on developer profile."""
    role = profile.get("role", "Backend")
    level = profile.get("level", "Junior")

    path = ONBOARDING_PATHS.get(role, ONBOARDING_PATHS["Backend"])
    tasks = path.get(level, path["Junior"])

    return tasks


def generate_onboarding_summary(profile: dict, completed_tasks: list[bool]) -> str:
    """Generate an AI onboarding summary report."""
    name = profile.get("name", "Developer")
    role = profile.get("role", "Backend")
    level = profile.get("level", "Junior")
    tech_stack = profile.get("tech_stack", [])
    tasks = generate_onboarding_path(profile)

    total = len(tasks)
    completed = sum(completed_tasks)
    pct = int((completed / total) * 100) if total else 0
    status = "Completed ✅" if pct == 100 else f"In Progress ({pct}% done)"

    if pct == 100:
        recommendation = "Ready for sprint assignment. Excellent onboarding performance! 🚀"
    elif pct >= 75:
        recommendation = "Almost there! Complete remaining tasks to get sprint-ready."
    elif pct >= 50:
        recommendation = "Good progress. Focus on completing the technical setup tasks next."
    else:
        recommendation = "Just getting started. Prioritize environment setup and documentation reading."

    readiness_score = min(100, pct + (10 if len(tech_stack) >= 2 else 0))

    report = f"""
# 📋 Onboarding Report — {datetime.now().strftime('%B %d, %Y')}

| Field | Details |
|---|---|
| **Developer** | {name} |
| **Role** | {level} {role} |
| **Tech Stack** | {', '.join(tech_stack) if tech_stack else 'N/A'} |
| **Tasks Completed** | {completed}/{total} |
| **Onboarding Status** | {status} |
| **Developer Readiness Score** | {readiness_score}/100 |
| **Recommendation** | {recommendation} |

## Completed Tasks
{chr(10).join(f"- {t}" for t, c in zip(tasks, completed_tasks) if c)}

## Pending Tasks
{chr(10).join(f"- {t}" for t, c in zip(tasks, completed_tasks) if not c) or "None — all done! 🎉"}
"""
    return report.strip()
