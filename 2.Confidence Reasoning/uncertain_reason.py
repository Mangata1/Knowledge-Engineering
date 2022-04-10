# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 20:15:33 2022

@author: 11877
"""
import copy
class Rule():
    def __init__(self,knowledge,res):
        self.knowledge=knowledge
        self.result=res
        
class Reason():
    def __init__(self):
        self.CF = [0.9, 0.8, 0.9, 0.9, 0.9, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.9, 0.9, 0.8]
        #置信度的值
        
    def load(self,path):
        rules=[]
        with open(path, 'r', encoding='utf-8') as f:
            lines=f.readlines()
        for line in lines:
            words=line.strip().split(' ')
            rules.append(Rule(words[:-1],words[-1]))
        return rules
      
    def solve(self,rule,type=1):
        if (type == 1):
            return max(rule, key=lambda x: len(x.knowledge))
        elif(type== 2):
            return rule[0]
        elif(type == 3):
            return rule[-1]
        else:
            exit(0)
    
    def forward(self,knows,rules):
        candidate_rules=[]
        used_rules=[]
        flag=False
        while True:
            candidate_rules=[]
            for rule in rules:
                allin=True
                for word in rule.knowledge:
                    if(word not in knows):
                        allin=False
                if(allin==True and rule not in used_rules):
                    candidate_rules.append(rule)
                    used_rules.append(rule)
            if(len(candidate_rules)!=0):
                target_rule= self.solve(candidate_rules,1)
                knows.append(target_rule.result)
                flag=True
            else:
                break
        if(flag):
            print('Forward reasoning get result:',knows[-1])
        else:
            print('reason fault!')
                
    def toposort(self,rules):
        topo_rules = []
        P_list = [rule.knowledge for rule in rules]
        Q_list = [rule.result for rule in rules]
        ind_list = []
        for i in P_list:
            sum = 0
            for x in i:
                if Q_list.count(x) > 0:
                    sum += Q_list.count(x)
            ind_list.append(sum)
        while True:
            if ind_list.count(-1) == len(ind_list):
                break
    
            for i, ind in enumerate(ind_list):
                if ind == 0:
                    topo_rules.append(Rule(P_list[i], Q_list[i]))
                    ind_list[i] = -1
                    for j, P in enumerate(P_list):
                        if Q_list[i] in P:
                            ind_list[j] -= 1
        return topo_rules
    
    def calculate_confidence(self,x,y):
        if(x>=0 and y>=0):
            return x+y-x*y
        elif(x<=0 and y<=0):
            return x+y+x*y
        elif(x*y<=0 and abs(x*y)==1):
            return 0
        elif(x*y<=0 and abs(x*y)!=1):
            return (x+y)/(1-min(abs(x),abs(y)))

                          
    def backward(self,knows,rules,cf):
        cf1=copy.deepcopy(cf)
        knows1=copy.deepcopy(knows)
        flag=False
        used_rule=[]
        for idx,rule in enumerate(rules):
            allin=True
            for word in rule.knowledge:
                if(word not in knows):
                    allin=False
            if(allin==True ):
                knows.append(rule.result)
                used_rule.append(idx)
                flag=True
        if(flag):
            print('Reverse reasoning get result:',knows[-1])
            print('Start calculate confidence! \n')
            print('used Rules:')
            for idx in used_rule:
                print(rules[idx].knowledge,'->',rules[idx].result)
            print('**********************************************')
            for idx in used_rule:
                print('Current rule：',rules[idx].knowledge,'->',rules[idx].result)
                cal_rules=[]
                for forward_idx in range(idx):
                    if(rules[forward_idx].result in rules[idx].result):
                        cal_rules.append(forward_idx)
                if(len(cal_rules)==0):
                    #print('test')
                    if(rules[idx].result not in knows1):
                        knows1.append(rules[idx].result)
                    cmp=cf1[knows1.index(rules[idx].knowledge[0])]
                    for kg in rules[idx].knowledge:
                        #print(kg)
                        #print(knows1)
                        if(cmp>cf1[knows1.index(kg)]):# and语句选择min
                            cmp=cf1[knows1.index(kg)]
                    cf1.append(float(self.CF[idx])*float(cmp))
                    print(rules[idx].result,'confidence:',cf1[-1])
                else:
                    cmp=cf1[knows1.index(rules[idx].knowledge[0])]
                    for kg in rules[idx].knowledge:

                        if(cmp>cf1[knows1.index(kg)]):# and语句选择min
                            cmp=cf1[knows1.index(kg)]
                    for idx1 in cal_rules:

                        res=self.calculate_confidence(float(cf1[knows1.index(rules[idx].result)]),float(self.CF[idx])*float(cmp))
                        #float(cf1[knows1.index(rules[idx].result)])+float(self.CF[idx])*float(cmp)-float(cf1[knows1.index(rules[idx].result)])*float(self.CF[idx])*float(cmp)
                        cf1[knows1.index(rules[idx].result)]=res
                    print(rules[idx].result,'confidence:',cf1[-1])
            print('**********************************************')
            print('Confidence result:',cf1[-1])
                #rules[idx]
            
        else:
            print('reason fault!')

    def mixture(self,knows,rules):
        candidate_rules=[]
        used_rules=[]
        flag=False
        i=0
        ii=0
        num=len(rules)
        backknow=[]
        flag1=False
        while True:
            if(flag1==True):
                break
            if (i%2==0):
                candidate_rules=[]
                for rule in rules:
                    allin=True
                    for word in rule.knowledge:
                        if(word not in knows):
                            allin=False
                    if(allin==True and rule not in used_rules):
                        candidate_rules.append(rule)
                        used_rules.append(rule)
                if(len(candidate_rules)!=0):
                    target_rule= self.solve(candidate_rules,1)
                    knows.append(target_rule.result)
                    flag=True
                else:
                    break
            else:
                reverserules=copy.deepcopy(rules)
                reverserules.reverse()
                while(ii<num):# 修改
                    allin=True
                    for word in reverserules[ii].knowledge:
                        if(word not in knows):
                            allin=False
                    if(allin==True ):
                        if(rule.result in knows):
                            falg1=True
                            break
                        else:
                            knows.append(reverserules[ii].result)
                            backknow.append(reverserules[ii].result)
                    ii+=1
            i+=1
                
        if(flag1):
            print('Mixture reasoning get result:',knows[-1])
        elif(flag):
            print('Mixture reasoning get result:',knows[-1])
        else:
            print('reason fault!')            
        
if __name__ == '__main__': 
    machine=Reason()
    rules=machine.load('data.txt')
    rules1=machine.toposort(rules)
    while(True):
        knows=input('Please enter known evidence：').strip().split(' ')
        cf=input('Please enter evidence confidence：').strip().split(' ')
        cf=[float(i) for i in cf]
        sel=int(input('Please enter the number of the reasoning strategy you want to implement, 1. Forward reasoning; 2. Reverse reasoning; 3. Mixture reasoning:'))
        if(sel==1):
            machine.forward(knows, rules1)
        elif(sel==2):
            machine.backward(knows, rules1,cf)
        elif(sel==3):
        #knows=['有毛','黄褐色','暗斑点']
            machine.mixture(knows, rules1)
        else:
            print('input error!')

                    
                        
                    
        
        
            
        
        