from worker import worker
import random
from logging_config import configure_logger
list_of_names = ["Adrian","Mark","Greg","Kelly","Jessica","Liz","Rosa","Patricia","Julia","Kathy"]
openness_traits = ["sensitive","confident"]
# neuroticism_traits = ["confident"]

world_logger = configure_logger(name="world",log_file="world_log.txt")
class world():
    def __init__(self, no_workers, init_pants, no_days, current_date = None, manager = False, static = True):
        self.no_workers = no_workers
        self.init_pants = init_pants
        self.no_days = no_days
        self.current_date = current_date
        self.pants = 0
        self.shorts = 0
        self.worker_list = []
        self.pants_over_time = []
        self.manager = manager
        self.static = static

        if self.manager:
            manager = worker(1024,self,name="Michael",traits = random.choice(openness_traits),static=self.static)
            manager.clothes= "shorts"
            self.worker_list.append(manager)
            self.no_workers -=1
        for i in range(self.no_workers):
            # trait = [random.choice(openness_traits) , random.choice(neuroticism_traits)]
            office_worker = worker(i,self,name=list_of_names[i],traits=random.choice(openness_traits))

            if i<init_pants:
                office_worker.clothes = "pants"
            else:
                office_worker.clothes = "shorts"
            self.worker_list.append(office_worker)

    def set_clothes_info(self):
        for worker in self.worker_list:
            if worker.clothes == "pants":
                self.pants +=1
            elif worker.clothes == "shorts":
                self.shorts +=1
        self.pants_over_time.append(self.pants)
        if self.manager:
            m_info = f"\nThe manager, {self.worker_list[0].name} wore {self.worker_list[0].clothes} yesterday."
        else:
            m_info = ""
        info = f"Yesterday, {self.pants} people wore pants and {self.shorts} people wore shorts." +m_info
        # print("Info: ", info)
        self.pants = 0
        self.shorts = 0
        for worker in self.worker_list:
            worker.clothes_info = info

    def run(self):
        for i in range(self.no_days):
            self.set_clothes_info()
            world_logger.info(f"Yesterday on day {i}, {self.pants_over_time[-1]} of {self.no_workers} wore pants.")
            # print("Today's choices: ")
            for worker in self.worker_list:
                worker.step()