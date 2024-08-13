from configparser import ConfigParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
#from antropic import Anthropic
import os

class LLM_Connector:
  def __init__(self,params):

    self.api_key = params['API_KEY']
    self.model_name = params['MODEL']
    self.base_url = ''  

  def get_llm(self):
    return self.llm  

class OpenAI(LLM_Connector):
  def __init__(self,params):
    super().__init__(params)
    self.llm = ChatOpenAI(
         model = self.model_name,
         api_key= self.api_key
    )

class LocalOpenAI(LLM_Connector):
  def __init__(self,params):
    super().__init__(params)
    self.llm = ChatOpenAI(
         model = self.model_name,
         base_url = self.base_url,
         api_key= self.api_key
    )

class PREBILLama(LLM_Connector):
  def __init__(self,params):
    super().__init__(params)
    self.llm = ChatOpenAI(
         model = self.model_name,
         base_url = self.base_url,
         api_key= self.api_key
    )



class Groq(LLM_Connector):
  def __init__(self,params):
    super().__init__(params)

    self.llm = ChatGroq(
                  api_key= self.api_key,
                  model=self.model_name
              )
 
class AnthropicClaude(LLM_Connector):
  def __init__(self,params):
    super().__init__(params)
    self.llm = Anthropic(
                  api_key=self.api_key,
                  model=self.model_name
                )
    

class LLM_Service:
  def __init__(self):
    self.__load_config()
    class_name = self.config['General']['LLM_FLAVOR']
    flavor = globals()[ class_name]
    llm_instance = flavor(self.config[class_name])
    self.llm = llm_instance.get_llm()
    self.set_environement_variables(llm_instance.api_key, llm_instance.model_name, llm_instance.base_url)

  def get_llm(self):
    return self.llm
  
  def __load_config(self):
    config = ConfigParser()
    
    config.read('.environment')
    self.config = config
  
  def set_environement_variables(self,model_name,api_key, base_url):
    os.environ["OPENAI_MODEL_NAME"] = model_name
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = base_url
   
