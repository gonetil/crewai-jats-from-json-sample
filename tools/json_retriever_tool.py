import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
import pandas as pd


class JSonRetrieverTool():

  @tool("Retrieve JSON data")
  def retrieve_json_data(doi):
    """Useful to scrape and summarize a website content"""
    url = f"https://api.crossref.org/works/{doi}"
    
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    jsonData = requests.request("GET", url, headers=headers).json()
 
    return jsonData