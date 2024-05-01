import os
import requests
import json
from textwrap import dedent
from crewai import Crew
from tools.json_retriever_tool import JSonRetrieverTool
from metadata_processor_agents import ReferenceProcessorAgents
from metadata_processor_tasks import MetadataProcessorTasks
from llm_service import LLM_Service


class MetadataCrew:
  def __init__(self, doi):
    self.doi = doi
    llm_service = LLM_Service()
    self.llm = llm_service.get_llm() 


  def getMetadata(self):
    url = f"https://api.crossref.org/works/{self.doi}"
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    jsonData = requests.request("GET", url, headers=headers).json() 
    del jsonData['message']['reference']
    return jsonData

  def run(self):
    agents = ReferenceProcessorAgents(self.llm)
    tasks = MetadataProcessorTasks()

    processor_agent = agents.reference_parser()
    xml_generation_task = tasks.process_metadata(processor_agent, self.getMetadata()) # Agrega la metadata puto

    crew = Crew(
      agents=[
        processor_agent,
      ],
      tasks=[
        xml_generation_task,
      ],
      verbose=False
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## This is a simple JSON to JATS XML generator")
  print('-------------------------------')
  doi = input(
    dedent("""
      Please write the DOI of the paper in the format: prefix/sufix
          Example: 10.24215/23143738e132
      If you want to use the same DOI as the example, just press [ENTER]     
    """))
  if not doi:
    doi = "10.24215/23143738e132"
  
  metadata_crew = MetadataCrew(doi)
  result = metadata_crew.run()
  print(result)