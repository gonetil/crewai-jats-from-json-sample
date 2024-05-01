from configparser import ConfigParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class LocalOpenAI:
  def __init__(self,params):
    self.llm = ChatOpenAI(
         model = params['MODEL'],
         base_url = params['BASE_URL'],
         api_key=params['API_KEY']
    )
  def get_llm(self):
    return self.llm


class Groq:
  def __init__(self,params):
    self.llm = ChatGroq(
                  api_key=params['API_KEY'],
                  model=params['MODEL']
              )
  def get_llm(self):
    return self.llm



class LLM_Service:
  def __init__(self):
    self.__load_config()
    class_name = self.config['General']['LLM_FLAVOR']
    flavor = globals()[ class_name]
    llm_instance = flavor(self.config[class_name])
    self.llm = llm_instance.get_llm()

  def get_llm(self):
    return self.llm
  
  def __load_config(self):
    config = ConfigParser()
    
    config.read('.environment')
    self.config = config