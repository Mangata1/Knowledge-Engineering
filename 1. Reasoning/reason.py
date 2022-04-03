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
    
    def backward(self,knows,rules):
        flag=False
        for rule in rules:
            allin=True
            for word in rule.knowledge:
                if(word not in knows):
                    allin=False
            if(allin==True ):
                knows.append(rule.result)
                flag=True
        if(flag):
            print('Reverse reasoning get result:',knows[-1])
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
        sel=int(input('Please enter the number of the reasoning strategy you want to implement, 1. Forward reasoning; 2. Reverse reasoning; 3. Mixture reasoning:'))
        if(sel==1):
            machine.forward(knows, rules1)
        elif(sel==2):
            machine.backward(knows, rules1)
        elif(sel==3):
        #knows=['有毛','黄褐色','暗斑点']
            machine.mixture(knows, rules1)
        else:
            print('input error!')

                    
                        
                    
        
        
            
        
        