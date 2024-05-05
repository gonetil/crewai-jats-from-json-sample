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
  def __init__(self, path_to_document):
    self.document = path_to_document
    self.doi = '10.7717/peerj.4375'
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

  #  processor_agent = agents.reference_parser()
  #  xml_generation_task = tasks.process_metadata(processor_agent, self.getMetadata()) # Agrega la metadata puto

    docx_analyzer_agent = agents.paper_analyzer()
    docx_analyze_task = tasks.look_for_references_in_paper(docx_analyzer_agent, self.llm, self.document)

    reference_generator_agent=agents.reference_generator()
    generate_references_task=tasks.transform_apa_reference_into_jats(reference_generator_agent,docx_analyze_task)

    crew = Crew(
      agents=[
        docx_analyzer_agent,
        reference_generator_agent
      ],
      tasks=[
        docx_analyze_task,
        generate_references_task
      ],
      verbose=False
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## DOCX reference analyzer ")
  print('-------------------------------')

  document='./sample/sample2_cadm.docx'  
  metadata_crew = MetadataCrew(document)
  result = metadata_crew.run()
  print(result)