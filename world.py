from worker import worker
import random

list_of_names = ["Adrian","Mark","Greg","Kelly","Jessica","Liz","Rosa","Patricia","Julia","Kathy"]
openness_traits = ["curious", "cautious"]
neuroticism_traits = ["sensitive","confident"]

class world():
    def __init__(self, no_workers, init_pants, no_days, current_date = None):
        self.no_workers = no_workers
        self.init_pants = init_pants
        self.no_days = no_days
        self.current_date = current_date
        self.pants = 0
        self.shorts = 0
        self.worker_list = []
        self.pants_over_time = []


        for i in range(no_workers):
            trait = [random.choice(openness_traits) , random.choice(neuroticism_traits)]
            office_worker = worker(i,self,name=list_of_names[i],traits=trait)

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
        info = f"Yesterday, {self.pants} people wore pants and {self.shorts} people wore shorts."
        # print("Info: ", info)
        self.pants = 0
        self.shorts = 0
        for worker in self.worker_list:
            worker.clothes_info = info

    def run(self):
        for i in range(self.no_days):
            self.set_clothes_info()
            print(f"Yesterday on day {i}, {self.pants_over_time[-1]} of {self.no_workers} wore pants.")
            print("Today's choices: ")
            for worker in self.worker_list:
                worker.step()