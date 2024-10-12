from gentopia.agent.base_agent import BaseAgent
from google_search import GoogleSearch
from pdf_reader import PDFReader
from pydantic import Field
from typing import List, Dict, Any

class LLMToolAgent(BaseAgent):
    """An LLM agent that can use Google Search and PDF reading tools."""

    # Required fields for BaseAgent (as per Pydantic validation)
    name: str = "LLM Tool Agent"
    type: str = "multi-tool"
    version: str = "1.0"
    description: str = "An agent that can perform Google searches and read PDF files."
    target_tasks: List[str] = Field(default_factory=lambda: ["google_search", "pdf_reader"])
    llm: str = "default-llm"
    prompt_template: str = "default-prompt-template"
    plugins: List[str] = Field(default_factory=list)
    
    # Adding `tools` as a field
    tools: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self):
        super().__init__()
        
        # Initialize the tools within the constructor
        self.tools = {
            "google_search": GoogleSearch(),
            "pdf_reader": PDFReader(),
        }

    def perform_task(self, tool_name, args):
        """Method to call the appropriate tool based on the task."""
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            result = tool._run(**args)
            return result
        else:
            return "Invalid tool requested."

    # Implementing the abstract method `run`
    def run(self, task_type, data):
        """This method runs the task based on the task_type."""
        return self.perform_task(task_type, data)

    # Implementing the abstract method `stream`
    async def stream(self, *args, **kwargs):
        """Asynchronous stream method to process tasks."""
        raise NotImplementedError("Stream functionality is not yet implemented in this agent.")

# if __name__ == "__main__":
#     agent = LLMToolAgent()

#     # Google search task
#     search_args = {"query": "Latest research on transformers"}
#     google_results = agent.run("google_search", search_args)
#     print("Google Search Results:\n", google_results)

#     # PDF reading task
#     pdf_args = {"file_path": "../../../../handout-3.pdf"}
#     pdf_content = agent.run("pdf_reader", pdf_args)
#     print("PDF Content:\n", pdf_content)
