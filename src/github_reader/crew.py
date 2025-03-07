import os
from crewai import Agent, Task, Crew, Process
from tools.github_tool import GitHubTool

# Load GitHub credentials from environment variables
GITHUB_OWNER = "ryanwkellss"
GITHUB_REPO = "eventhorizon"
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

# Initialize GitHub tool
github_tool = GitHubTool(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)

# Fetch PR files (Change PR number as needed)
pr_number = 123  # Replace with actual PR number
pr_files = github_tool.fetch_pull_request_files(pr_number)

if "error" in pr_files:
    print(pr_files["error"])
    exit()

# Create Agents
performance_agent = Agent(
    role="Performance Reviewer",
    goal="Analyze code performance issues",
    backstory="Expert in performance optimization.",
    verbose=True,
    tools=[github_tool]
)

security_agent = Agent(
    role="Security Auditor",
    goal="Identify security vulnerabilities",
    backstory="Specialist in secure coding practices.",
    verbose=True,
    tools=[github_tool]
)

efficiency_agent = Agent(
    role="Efficiency Specialist",
    goal="Optimize code for redundancy and efficiency",
    backstory="Focused on refactoring and clean code.",
    verbose=True,
    tools=[github_tool]
)

documentation_agent = Agent(
    role="Documentation Expert",
    goal="Improve code documentation and readability",
    backstory="Ensures proper commenting and documentation.",
    verbose=True,
    tools=[github_tool]
)

# Create Tasks
performance_task = Task(
    description="Review the PR for performance issues.",
    expected_output="A markdown report with performance suggestions.",
    agent=performance_agent
)

security_task = Task(
    description="Review the PR for security vulnerabilities.",
    expected_output="A markdown report with security concerns.",
    agent=security_agent
)

efficiency_task = Task(
    description="Review the PR for redundant code and improvements.",
    expected_output="A markdown report with redundancy fixes.",
    agent=efficiency_agent
)

documentation_task = Task(
    description="Review the PR for documentation and readability issues.",
    expected_output="A markdown report with documentation suggestions.",
    agent=documentation_agent
)

# Create Crew
crew = Crew(
    agents=[performance_agent, security_agent, efficiency_agent, documentation_agent],
    tasks=[performance_task, security_task, efficiency_task, documentation_task],
    process=Process.parallel  # Run agents simultaneously
)

# Execute Crew
results = crew.kickoff()

# Save Reports Locally
for agent, result in zip(
    ["performance", "security", "efficiency", "documentation"], results
):
    with open(f"{agent}_review.md", "w") as file:
        file.write(result)

print("Reviews completed. Reports saved locally.")
