import pandas as pd
class AprioriAlgorithm:
    def __init__(self,data,min_sup,min_conf):
        itemset=[]
        for line in data['Itemset']:
            item=line.split(', ')
            for i in item:
                if [i] not in itemset:
                    itemset.append([i])
        self.itemset=itemset
        self.min_conf=float(min_conf)
        self.min_sup=float(min_sup)
        new_data=[]
        for line in data["Itemset"]:
            list_str=line.split(', ')
            dict_item_line={}
            for item in list_str:
                dict_item_line[item]=True
            new_data.append(dict_item_line)
        self.data=new_data
    
    def sup_cal(self,list_itemset,loop_index):
        itemset_sup_list=[]
        for itemset in list_itemset:
            count_sup=0
            for line in self.data:
                count_item=0
                for item in itemset:
                    try:
                        if line[item]:
                            count_item+=1
                        if count_item == loop_index:
                            count_sup+=1
                    except:
                        continue
            itemset_sup_list.append(count_sup/len(self.data))
        return itemset_sup_list
    
    def generate_itemset(self,list_itemset,loop_index):
        list_item=[]
        itemset_first_list=[]
        for itemset in list_itemset:
            for item in itemset:
                if item not in list_item:
                    list_item.append(item)
        for itemset in list_itemset:
            dic={}
            for item in itemset:
                dic[item]=True
            itemset_first_list.append(dic)
        itemset_last_list=[]
        for itemset in itemset_first_list:
            for item in list_item:
                dic=itemset.copy()
                try:
                    if dic[item]:
                        continue
                except:
                    if len(dic)-1 < loop_index:
                        dic[item]=True
                        itemset_last_list.append(dic)
        leng_last_list=len(itemset_last_list)
        index=0
        while index < leng_last_list:
            if itemset_last_list.count(itemset_last_list[index]) !=1:
                itemset_last_list.remove(itemset_last_list[index])
                leng_last_list-=1
                continue
            if itemset_last_list.count(itemset_last_list[index])==1:
                index+=1
        itemset_new_list=[]
        for itemset in itemset_last_list:
            arr=[]
            for item in list_item:
                try:
                    if itemset[item]:
                        arr.append(item)
                    if len(arr) == loop_index:
                        itemset_new_list.append(arr)
                        break
                except:
                    index+=1
                    continue
        return itemset_new_list

    def conf_cal(self,last_list_itemset):
        list_rule=[]
        if len(last_list_itemset[0]) == 1:
            return []
        for itemset in last_list_itemset:
            key=[]
            value=itemset.copy()
            if len(itemset) <= 2:
                key=[itemset[0]]
                value.remove(itemset[0])
                list_rule.append([key,value])
                list_rule.append([value,key])
                continue
            while len(value) > 2:
                key.append(value[0])
                value.remove(value[0])
                list_rule.append([key,value])
                list_rule.append([value,key])
                for item in value:
                    key2=key.copy()
                    value2=value.copy()
                    key2.append(item)
                    value2.remove(item)
                    list_rule.append([key2,value2])
                    list_rule.append([value2,key2])
        list_conf_item=[]
        for rule in list_rule:
            count_first=0
            count_last=0
            for line in self.data:
                count_item_first=0
                for item in rule[0]:
                    try:
                        if line[item]:
                            count_item_first+=1
                    except:
                        continue
                    if count_item_first == len(rule[0]):
                        count_item_second=0
                        for item_second in rule[1]:
                            try:
                                if line[item_second]:
                                    count_item_second+=1
                                if count_item_second==len(rule[1]):
                                    count_last+=1
                            except:
                                break
                        count_first+=1
            list_conf_item.append((rule,count_last/count_first,count_last/len(self.data)))
        return list_conf_item

    def find_freq(self):
        final_itemset=[]
        l_index=1
        while self.itemset:
            itemset_sup_list=list(zip(self.itemset,self.sup_cal(self.itemset,l_index)))
            leng_sup_list=len(itemset_sup_list)
            count_item=0
            while count_item < leng_sup_list:
                if itemset_sup_list[count_item][1] < self.min_sup:
                    itemset_sup_list.remove(itemset_sup_list[count_item])
                    leng_sup_list=leng_sup_list-1
                    continue
                count_item+=1
            new_itemset=[]
            for item in itemset_sup_list:
                new_itemset.append(item[0])
            l_index+=1
            if new_itemset:
                final_itemset=new_itemset
            if len(itemset_sup_list) == 0:
                break
            self.itemset=self.generate_itemset(new_itemset,l_index)
        itemset_conf_list=self.conf_cal(final_itemset)
        index=0
        leng_itemset_conf_list=len(itemset_conf_list)
        while index < leng_itemset_conf_list:
            if itemset_conf_list[index][1] < self.min_conf:
                itemset_conf_list.remove(itemset_conf_list[index])
                leng_itemset_conf_list-=1
                continue
            index+=1
        print("ASSOCIATE RULE:")
        for list_itemset,conf,sup in itemset_conf_list:
            print(', '.join(list_itemset[0])+" =>> "+', '.join(list_itemset[1])+"(confidence:"+str(conf)+", sup:"+str(sup)+")")

min_sup=input("MIN SUP: ")
min_conf=input("MIN CONF: ")
xl=pd.ExcelFile("./data.xlsx")
df=pd.read_excel(xl)

apriori=AprioriAlgorithm(df,min_sup,min_conf)
apriori.find_freq()