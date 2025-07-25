import subprocess
from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool



def invoke(command: str) -> str:
        """
        Executes a gcloud command.

        Args:
            command: The full gcloud command to execute (e.g., "gcloud compute instances list").

        Returns:
            The output of the gcloud command.
        """
        try:
            # We assume 'command' already includes 'gcloud' at the beginning.
            # If not, you might want to prepend 'gcloud ' to the command.
            result = subprocess.run(
                command.split(), # Split the command string into a list of arguments
                capture_output=True,
                text=True,
                check=True,
                shell=False # It's generally safer to not use shell=True for security reasons
            )
            result = "Status" + str(result.stdout.strip())
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing gcloud command: {e.stderr.strip()}"
        except FileNotFoundError:
            return "gcloud command not found. Please ensure Google Cloud SDK is installed and in your PATH."


root_agent = Agent(
   # A unique name for the agent.
   name="gcloud_command_executor",
   # The Large Language Model (LLM) that agent will use.
   # Please fill in the latest model id that supports live from
   # https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/#supported-models
   model="gemini-live-2.5-flash-preview",  # for example: model="gemini-2.0-flash-live-001" or model="gemini-2.0-flash-live-preview-04-09"
   
   # A short description of the agent's purpose.
   description="You are an agent that understand users instruction and perform gcloud command convert of the same so that the command is sytactically correct and executes correctly with correct parameters. You fact and syntax check the command and converse with user to get the required parameters before calling the invoke tool passing the command as parameter to it and returns its response back to the user",
   # Instructions to set the agent's behavior.
   instruction="You are GCLOUD command expert and always speak english. You capture and understand users instruction and  " \
   "perform gcloud command convert of the same so that the command is syntactically " \
   "correct and executes correctly with correct parameters. You fact check and syntax check with google search tool as well if required " \
   "the command and converse with user to get the required parameters before " \
   "calling the invoke tool passing the command as parameter to it and returns its response back to the user. Do not be repeatative and do not confirm the command with user. Make sure to use default values for parameters that might be configured with gcloud earlier",
   # Add google_search tool to perform grounding with Google search.
   tools=[invoke],

)






