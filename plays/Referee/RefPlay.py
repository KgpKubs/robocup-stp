from tactics import TStop
from tactics import TMark
from tactics import TPosition
from utils.robot_threads import robot_thread as thread

class RefPlay(object):
    tactic_mapping = {"TStop": TStop.TStop,
                      "TMark": TMark.TMark,
                      "TPosition": TPosition.TPosition}
    def __init__(self, state,  publisher):
        self.active_robots = 6
        self.role_list = [['' for i in range(2)] for j \
            in range(self.active_robots)]
        self.instances = []
        self.robots = []
        self.state = state
        self.publisher = publisher

    def tactic_instance(self, tactic, params):
        for i in range(self.active_robots):
            self.role_list[i][0] = tactic[i]
            self.role_list[i][1] = params[i]
        for i in range(self.active_robots):
            self.instances.append(RefPlay.tactic_mapping[self.role_list[i][0]]( \
                i, self.state, self.role_list[i][1]))

    def execute(self,gv):
        for i in range(self.active_robots):
            self.robots.append(thread(self.instances[i], self.state, \
                gv,self.publisher))
        for i in range(self.active_robots):
            self.robots[i].start()
        for i in range(self.active_robots):
            self.robots[i].join()