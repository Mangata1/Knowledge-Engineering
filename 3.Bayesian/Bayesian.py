import sys


class node:
    def __init__(self, name, p):
        self.name = name
        self.p = p  
        self.o = None
        self.calculate_self_O()  
        self.e = []  
        self.e_o = None  
        self.e_p = None 
        self.e_c = None  
        self.cal_complete = False
        self.list = []

    def calculate_self_O(self):
        self.o = self.p / (1 - self.p)

    def calculate_self_O_post(self):
        self.e_o = self.e_p / (1 - self.e_p)

    def calculate_self_O_post_updata(self, p_h):
        o_temp = p_h / (1 - p_h)
        self.e_o = (self.e_o / self.o) * (o_temp / self.o) * self.o


    def calculate_self_e_p_h(self):
        if self.e_c >= 0:
            self.e_p = self.p + self.e_c / 5 * (1 - self.p)
        elif self.e_c < 0:
            self.e_p = self.p + self.e_c / 5 * self.p
        else:
            print("error when calculate init_e_p_h")

    def calculate_self_e_p_update(self):
        self.e_p = self.e_o / (1 + self.e_o)



class R:
    def __init__(self, LHS, RHS, LS, LN, attr='INFER'):
        self.LHS = LHS  
        self.RHS = RHS  
        self.LS = LS
        self.LN = LN
        self.attr = attr  
        self.relu_use = False  


class cal_engine():
    def __init__(self):
        self.node_dict = {}  
        self.r_list = [] 
        self.load_node_relu()  
        self.load_init_C_or_P()  
        self.nodes_set = set()  


    def load_node_relu(self):
        for i in range(len(node_data)):
            self.node_dict[node_data[i]['name']] = node(node_data[i]['name'], node_data[i]['p'])
        for i in range(len(relu)):
            self.r_list.append(R(relu[i]['LHS'], relu[i]['RHS'], relu[i]['LS'], relu[i]['LN'], relu[i]['ATTR']))


    def load_init_C_or_P(self):
        for j in range(len(c_init)):
            if c_init[j]['H'] in self.node_dict:
                self.node_dict[c_init[j]['H']].e.append(c_init[j]['E'])
                self.node_dict[c_init[j]['H']].e_p = c_init[j]['C']
                self.node_dict[c_init[j]['H']].cal_complete = True
            else:
                print("error" + c_init[j]['H'] + "is not a node!!")


    def engine_processing(self):

        for i in range(len(self.r_list)):
            if self.r_list[i].relu_use:
                continue

            bool_cal = True
            for node1 in self.r_list[i].LHS:
                if not self.node_dict[node1].cal_complete:
                    bool_cal = False
                pass
            if bool_cal:  

                self.r_list[i].relu_use = True

 
                if self.r_list[i].attr == 'INFER':
                    p_H_E = 0
                    p_H_E_ = 0
                    if self.node_dict[self.r_list[i].LHS[0]].e_c:  
                        if self.node_dict[self.r_list[i].LHS[0]].e_c > 0:
                            p_H_E = (self.r_list[i].LS * self.node_dict[self.r_list[i].RHS[0]].o) / (
                                    1 + self.r_list[i].LS * self.node_dict[self.r_list[i].RHS[0]].o)
                            p_H_E_ = self.node_dict[self.r_list[i].RHS[0]].p + (
                                    p_H_E - self.node_dict[self.r_list[i].RHS[0]].p) * self.node_dict[
                                         self.r_list[i].LHS[0]].e_c / 5
                        else:
                        
                            p_H_E = (self.r_list[i].LN * self.node_dict[self.r_list[i].RHS[0]].o) / (
                                    1 + self.r_list[i].LN * self.node_dict[self.r_list[i].RHS[0]].o)
                          
                            p_H_E_ = p_H_E + (self.node_dict[self.r_list[i].RHS[0]].p - p_H_E) * (
                                    self.node_dict[self.r_list[i].LHS[0]].e_c / 5 + 1)

                    elif self.node_dict[self.r_list[i].LHS[0]].e_p:
                        if self.node_dict[self.r_list[i].LHS[0]].e_p > self.node_dict[self.r_list[i].LHS[0]].p:
                            p_H_E = (self.r_list[i].LS * self.node_dict[self.r_list[i].RHS[0]].o) / (
                                    1 + self.r_list[i].LS * self.node_dict[self.r_list[i].RHS[0]].o)

                            p_H_E_ = self.node_dict[self.r_list[i].RHS[0]].p + (
                                    p_H_E - self.node_dict[self.r_list[i].RHS[0]].p) / (
                                             1 - self.node_dict[self.r_list[i].LHS[0]].p) * (
                                             self.node_dict[self.r_list[i].LHS[0]].e_p - self.node_dict[
                                         self.r_list[i].LHS[0]].p)
                        else:
                            p_H_E = (self.r_list[i].LN * self.node_dict[self.r_list[i].RHS[0]].o) / (
                                    1 + self.r_list[i].LN * self.node_dict[self.r_list[i].RHS[0]].o)
                            p_H_E_ = p_H_E + (self.node_dict[self.r_list[i].RHS[0]].p - p_H_E) / self.node_dict[
                                self.r_list[i].LHS[0]].p * self.node_dict[self.r_list[i].LHS[0]].e_p

                  
                    self.node_dict[self.r_list[i].RHS[0]].list.append(p_H_E_)
                    if self.node_dict[self.r_list[i].RHS[0]].e == []:  # 证据集空
                        self.node_dict[self.r_list[i].RHS[0]].e_p = p_H_E_
                        self.node_dict[self.r_list[i].RHS[0]].calculate_self_O_post()
                    else: 
                        self.node_dict[self.r_list[i].RHS[0]].calculate_self_O_post_updata(p_H_E_)
                        self.node_dict[self.r_list[i].RHS[0]].calculate_self_e_p_update()
                 
                    for k in range(len(self.node_dict[self.r_list[i].LHS[0]].e)):
                        if self.node_dict[self.r_list[i].LHS[0]].e[k] not in self.node_dict[self.r_list[i].RHS[0]].e:
                            self.node_dict[self.r_list[i].RHS[0]].e.append(self.node_dict[self.r_list[i].LHS[0]].e[k])

                elif self.r_list[i].attr == 'AND':
                    self.node_dict[self.r_list[i].RHS[0]].e_p = 1
                    for node2 in self.r_list[i].LHS:
                        for ei in range(len(self.node_dict[node2].e)):
                            self.node_dict[self.r_list[i].RHS[0]].e.append(self.node_dict[node2].e[ei])
                        if self.node_dict[self.r_list[i].RHS[0]].e_p > self.node_dict[node2].e_p:
                            self.node_dict[self.r_list[i].RHS[0]].e_p = self.node_dict[node2].e_p
                elif self.r_list[i].attr == 'OR':
                    self.node_dict[self.r_list[i].RHS[0]].e_p = 0
                    for node2 in self.r_list[i].LHS:
                        for ei in range(len(self.node_dict[node2].e)):
                            self.node_dict[self.r_list[i].RHS[0]].e.append(self.node_dict[node2].e[ei])
                        if self.node_dict[self.r_list[i].RHS[0]].e_p < self.node_dict[node2].e_p:
                            self.node_dict[self.r_list[i].RHS[0]].e_p = self.node_dict[node2].e_p
                    pass
                else:
                    print("error!")
    
        self.nodes_set.clear()  # 清空集合
        for relu in self.r_list:
            if not relu.relu_use:
                self.nodes_set.add(relu.RHS[0])
        for node3 in self.node_dict.values():
            if node3.name not in self.nodes_set:
                node3.cal_complete = True

    def engine(self):
        self.engine_processing()
        while len(self.nodes_set) > 0:
            self.engine_processing()
relu = [
    {'LHS': ['RCS', 'RCAD', 'RCIB', 'RCVP'], 'RHS': ['SMIRA'], 'ATTR': 'OR', 'LS': None, 'LN': None},
    {'LHS': ['RCS'], 'RHS': ['SMIR'], 'ATTR': 'INFER', 'LS': 300, 'LN': 1},
    {'LHS': ['RCAD'], 'RHS': ['SMIR'], 'ATTR': 'INFER', 'LS': 75, 'LN': 1},
    {'LHS': ['RCIB'], 'RHS': ['SMIR'], 'ATTR': 'INFER', 'LS': 20, 'LN': 1},
    {'LHS': ['RCVP'], 'RHS': ['SMIR'], 'ATTR': 'INFER', 'LS': 4, 'LN': 1},
    {'LHS': ['SMIRA'], 'RHS': ['SMIR'], 'ATTR': 'INFER', 'LS': 1, 'LN': 0.0002},
    {'LHS': ['SMIR'], 'RHS': ['HYPE'], 'ATTR': 'INFER', 'LS': 300, 'LN': 0.0001},
    {'LHS': ['FMGS'], 'RHS': ['STIR'], 'ATTR': 'INFER', 'LS': 2, 'LN': 0.000001},
    {'LHS': ['FMGS', 'PT'], 'RHS': ['FMGS&PT'], 'ATTR': 'AND', 'LS': None, 'LN': None},
    {'LHS': ['FMGS&PT'], 'RHS': ['STIR'], 'ATTR': 'INFER', 'LS': 100, 'LN': 0.000001},
    {'LHS': ['STIR'], 'RHS': ['HYPE'], 'ATTR': 'INFER', 'LS': 65, 'LN': 0.01},
    {'LHS': ['HYPE'], 'RHS': ['FLE'], 'ATTR': 'INFER', 'LS': 200, 'LN': 0.0002},
    {'LHS': ['CVR'], 'RHS': ['FLE'], 'ATTR': 'INFER', 'LS': 800, 'LN': 1},
    {'LHS': ['FLE'], 'RHS': ['FRE'], 'ATTR': 'INFER', 'LS': 5700, 'LN': 0.0001},
    {'LHS': ['OTFS'], 'RHS': ['FRE'], 'ATTR': 'INFER', 'LS': 5, 'LN': 0.7},
]

node_data = [
    {'name': 'RCS', 'p': 0.001, },
    {'name': 'RCAD', 'p': 0.001, },
    {'name': 'RCIB', 'p': 0.001, },
    {'name': 'RCVP', 'p': 0.001, },
    {'name': 'SMIRA', 'p': 0.001, },
    {'name': 'SMIR', 'p': 0.03, },
    {'name': 'HYPE', 'p': 0.01, },
    {'name': 'FMGS', 'p': 0.01, },
    {'name': 'PT', 'p': 0.01, },
    {'name': 'FMGS&PT', 'p': 0.01, },
    {'name': 'STIR', 'p': 0.1, },
    {'name': 'CVR', 'p': 0.001, },
    {'name': 'FLE', 'p': 0.005, },
    {'name': 'OTFS', 'p': 0.1, },
    {'name': 'FRE', 'p': 0.001, },
    # {'name': '', 'p': , },
]

# 给定8个初始节点的合适可信度值
c_init = [
    {'H': 'RCS', 'E': 'E1', 'C': 5},
    {'H': 'RCAD', 'E': 'E1', 'C': -1},
    {'H': 'RCIB', 'E': 'E1', 'C': -1},
    {'H': 'RCVP', 'E': 'E1', 'C': -2},
    {'H': 'FMGS', 'E': 'E2', 'C': -1},
    {'H': 'PT', 'E': 'E2', 'C': -1},
    {'H': 'CVR', 'E': 'E3', 'C': -5},
    {'H': 'OTFS', 'E': 'E4', 'C': 1},
]

if __name__ == '__main__':
    eng = cal_engine()
    eng.engine()

    print("Posterior probability：", eng.node_dict['FRE'].e_p)
    print("后验几率：", eng.node_dict['FRE'].e_o)
