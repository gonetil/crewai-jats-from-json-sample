from crewai import Agent
from tools.json_retriever_tool import JSonRetrieverTool



class ReferenceProcessorAgents():
  def __init__(self, llm):
    self.llm = llm

  def reference_parser(self):
      return Agent(
      role='Parse JSON metadata',
      goal="""Generates JATS XML data from metadata in JSON format""",
      backstory="""When building large JATS XML documents, all references 
      must be also included in JATS XML format. Everytime you recieve JSON 
      metadata from papers, you transform it to JATS XML format, ready to be put into
      any JATS XML document""",
      verbose=False,
 
      llm = self.llm
    )
