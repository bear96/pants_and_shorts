from utils import get_completion_from_messages
import numpy as np
import time
from logging_config import configure_logger

worker_logger = configure_logger(name = "workers", log_file="workers_log.txt")

class worker():
    def __init__(self, unique_id, model, name, traits, clothes = None, static = False):
        self.unique_id = unique_id
        self.clothes = clothes
        self.mem = np.array([],dtype="S")
        self.model = model
        self.clothes_info = None
        self.name = name
        self.traits = traits
        self.static = static

    def decide_clothes(self):
        reasoning, response = self.get_response()
        worker_logger.info(f"{self.name}'s reasoning: {reasoning}")
        worker_logger.info(f"{self.name}'s response: {response}")
        if response == "pants":
            self.clothes = "pants"
            self.mem = np.append(self.mem,f"You chose to wear pants yesterday.")
        elif response == "shorts":
            self.clothes = "shorts"
            self.mem = np.append(self.mem,f"You chose to wear shorts yesterday.")
        else:
            worker_logger.warning("Warning! Response was neither pants nor shorts. Defaulting with pants.")
            worker_logger.warning(f"Response was: {response}")
            self.clothes = "pants"
            self.mem = np.append(self.mem,f"You chose to wear pants yesterday.")

    def get_response(self):
        if len(self.mem) ==0:
            relevant_mems = f"You chose to wear {self.clothes} yesterday."
        else:
            relevant_mems = self.mem[-1]

        question_prompt = f"""
        You are {self.name}. You are a {self.traits} person.
        You work in an office with 9 other people. You have work today. You need to decide between wearing pants or shorts to work. The weather is appropriate for either pants or shorts.
        {relevant_mems}
        {self.clothes_info}
        Based on the above context, you need to choose whether to wear pants or shorts. You must provide your reasoning for your choice and then your response in one word.
        For example, if your answer is "pants", your response will be:
        Reasoning: [Your reason to choose to wear pants]
        Response: Pants
        If your answer is "shorts", then your response will be:
        Reasoning: [Your reason to choose to wear shorts]
        Response: Shorts
        Please make sure your response is in one word.
        """
        #You are {self.traits[0]} and {self.traits[1]}.
        
        messages =  [{'role':'system', 'content':question_prompt}]
        try:
            output = get_completion_from_messages(messages)
        except Exception as e:
            print(f"{e}\nProgram paused. Retrying after 60s...")
            time.sleep(60)
            output = get_completion_from_messages(messages)
        reasoning = ""
        response = ""
        try:
            intermediate  = output.split("Reasoning:",1)[1]
            reasoning, response = intermediate.split("Response:")
            response = response.strip().split(".",1)[0]
            reasoning = reasoning.strip()
            # print(reasoning, response)
        except:
            worker_logger.warning("Reasoning or response were not parsed correctly.")
            worker_logger.warning(f"Output: {output}")
            response = "pants"
            reasoning = None
        return reasoning.strip().lower(), response.strip().lower()

    def step(self):
        if not self.static:
            self.decide_clothes()
        else:
            pass


