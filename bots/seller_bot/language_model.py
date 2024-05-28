import together
import os
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from bots.client_bot.models import Category
import json

class TogetherLLM(LLM):

    model: str = "togethercomputer/llama-2-70b-chat"

    together_api_key: str = "67a96691fabefa1320d838470ca884833d0d99131c6d59d741609361e2141ee2"

    """Together API key"""

    temperature: float = 0.1

    max_tokens: int = 1000


    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key

        s =together.Models.start(self.model)
        print(s)
        print(prompt)

        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']

        s = together.Models.stop(self.model)
        print(s)


        return text

def all_base_categories(categories : [Category]):
    categories_parents = [category.parent for category in categories]
    return [{"id" : category.id, "name": category.name} for category in categories if category.id not in categories_parents]


system_prompt = (
"""\
You are a data generator. you generate data in a JSON format 
using the JSON schema provided below. you shall never deviate from 
the schema provided below and never go outside the context of the 
given prompt. 

Here is the schema you are going to use:

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "maxLength": 100,
    },
    "price": {
      "type": "number",
      "maximum": 9999999.99,
      "minimum": 0.00,
      "nullable": true
    },
    "category": {
      "type": "integer",
      "nullable": true
    },
    "sold": {
      "type": "boolean",
      "nullable": true
    },
    "description": {
      "type": "string",
      "nullable": true
    },
    "detailed_description": {
      "type": "object",
      "nullable": true,
      "additionalProperties" : {
        "type" : "string"
      }
    }
  },
  "required": ["name"],
  "additionalProperties": false
}

Further instructions for each property is given below

name - in this property, you will summarize the prompt into a very
short summary that tells what the product is. it is meant to be put as 
the headline and it should not be more than 1 line long.

price - in this property, you will search for anything explaining the price
of the product and put it here. if the price is not found or is ambigous put null.
category - in this property, you will categorize the product into one of the category lists
found below. if you cannot categorize it put null.
""" +
json.dumps(all_base_categories(Category.all().get("results")))

+

"""
sold - in this property, you will look for details showing the product is sold and put true if
it is. if not you put false. if there is nothing specifiying if it is sold or not or if there is
something ambigous then you put null
description - in this property you will put a longer description of the product in just a simple paragraph.
If you dont have enough content then put it as null.
detailed_description - in this property, you will put a json in which the properties explain the specifications of the prodcut
and are specific to a certain category. if you dont have enough content then put it as null. 
"""




)
prompt = PromptTemplate.from_template(
"""\
[/INST]
<<SYS>>
{system_prompt}    
<<SYS>>
{prompt}
[/INST]
"""
)


chain = LLMChain(llm=TogetherLLM(), prompt=prompt)


"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"