from crewai import Task
from textwrap import dedent

class MetadataProcessorTasks():
  def process_metadata(self, agent, json_metadata):
    return Task(description=dedent(f"""
                Generates a ref item for the ref-list section in an XML JATS document for
                the paper for the following JSON obtained from CrossRef REST API: {json_metadata} 
      """),
      expected_output="A ref item in JATS XML format, with only the parts of the reference specified in XML JATS 1.2 standard",
      agent=agent
    )