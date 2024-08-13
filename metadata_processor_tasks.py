from crewai import Task
from textwrap import dedent
from crewai_tools import DOCXSearchTool


class MetadataProcessorTasks():
  def process_metadata(self, agent, json_metadata):
    return Task(description=dedent(f"""
                Generates a ref item for the ref-list section in an XML JATS document for
                the paper for the following JSON obtained from CrossRef REST API: {json_metadata} 
      """),
      expected_output="A ref item in JATS XML format, with only the parts of the reference specified in XML JATS 1.2 standard",
      agent=agent
    )
  
  def look_for_references_in_paper(self,agent,llm,path_to_paper):
    docx_search_tool = DOCXSearchTool()
    return Task(
      description="""Analyze the content of a scientific paper, and retrieve all the 
      bibliographic refecences from the Bibliography section. The paper could be in any 
      language, so the Bibliography section could have any title, like References, Bibliografía,
      Referencias, among many
    """,
      agent=agent,
      llm = llm,
      expected_output="A list of bibliographic references",  
      tools=[docx_search_tool],
    )
  
  def transform_apa_reference_into_jats(self,agent,prev_task):
    return Task(
      description="""Process bibliographic references extracted from a paper, formated
      in APA7 style, and generate ref items for the ref-list section of an XML JATS document""",
      agent=agent,
      context=[prev_task],
      expected_output="""A list of ref item for the ref-list section in  XML JATS 1.2
        standard""",
    )
    
    
  def transform_docx_into_jats(sef,agent,prev_task):
    return Task(
      description="""Process an entire docx file for a scientific paper, identifying metadata, sections, citations, figures and tables, 
      and generate an XML JATS representation of the same document. The list of references have already been parsed into a ref-list section """,
      agent=agent,
      context=[prev_task],
      expected_output="""An XML JATS output for the given paper"""
    )  