# AI-Email-Sender-Crew
AI Agents work together using CrewAI to automate sending emails to known people, given a length of time.

Ensure you have Python >=3.10 <3.13 and CrewAI installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/gmail_testing_final/config/agents.yaml` to define your agents
- Modify `src/gmail_testing_final/config/tasks.yaml` to define your tasks (Including email structure, user's name, and unavailability time period)
- Modify `src/gmail_testing_final/crew.py` to add your own logic, tools and specific args
- Modify `src/gmail_testing_final/main.py` to add custom inputs for your agents and tasks (Including list of who to respond to)
- Modify `src/gmail_testing_final/credentials.json` with Google Cloud API services credentials

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the gmail-testing-final Crew, assembling the agents and assigning them tasks as defined in your configuration.
