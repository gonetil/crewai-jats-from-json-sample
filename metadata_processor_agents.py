from crewai import Agent
from tools.json_retriever_tool import JSonRetrieverTool
from crewai_tools import DOCXSearchTool




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
  
  def paper_analyzer(self):
     return Agent(
      role='Looks for bibliographic references in a paper',
      goal="""Return the list of bibliographic references in the Bibliography
             section of the paper. The paper could be written in any language, so 
             the bibliographic references might also be in any language""",
      backstory="""You are an expert in bibliographic analysis, and your work is to 
      generate lists of bibliographic refecences of every scientific paper you recieve.
      The papers you analyze can be written in Enlish, Spanish, French or any other language,
      and you are able to locate the Bibliography section of a scientific paper, no matter 
      its language""",
      verbose=False,
      llm = self.llm
    )
     
  def reference_generator(self):
    return Agent(
      role='Generates lists of bibliographic references in XML JATS format',
      goal="""For every bibliographic reference recieved, generates a ref item for the ref-list
      section of an XML JATS document""",
      backstory="""Your job is to extract bibliographic references from scientific papers,
       and to generate an XML JATS version of each reference, which will be added to the ref-list
        section of an XML JATS document""",
      verbose=False,
      llm = self.llm
    )
