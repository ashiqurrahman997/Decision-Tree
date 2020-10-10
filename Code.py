from math import *
class data:
    d_l = {}
    name = []
    tree = []
    try_tree = {}
    def __init__(self,l):
        self.l = l
    def display(self):
        for i in self.l:
            print(i,end = " ")
        #for i,j in data.d_l.items():
            #print(j ,end =" ")
        #print()
        #for i in data.name:
            #print(i,end = " ")
        print()

def display_data(l):
    for i in l:
        i.display()


def create_decision_tree():
    fn = 'Decision_tree'
    f1 = open(fn, 'r')
    l1 = []
    l2 = []
    lines = f1.readlines()
    for i in lines:
        i = i.strip()
        l1 = i.split(" ")
        d1 = data(l1)
        l2.append(d1)

    fn2 = 'Names.txt'
    f2 = open(fn2,'r')
    lines2 = f2.readlines()
    for i in lines2:
        i = i.strip()
        n = i.split(" ")
        data.name = n.copy()

    return l2


def find_total_distinct_values_for_every_situation(l):
    old = []
    temp = []
    for i in l[0].l:
        old.append([])

    for obj in l:
        temp = []
        for i in range(1,len(obj.l)-1,1):
            if (obj.l[i] in old[i]):
                pass
            else:
                temp = old[i].copy()
                temp.append(obj.l[i])
                old[i] = temp.copy()
                temp = []

    for i in range(len(l[0].l)):
        data.d_l[i] = old[i]
    return l

def find_total_positive_negetive(l,decision_index,positive_val):
    cnt = 0
    for i in l:
        if i.l[decision_index] == positive_val:
           cnt+=1
    return cnt,(len(l) - cnt)

def f_p_n(l,decision_index,positive_val,index2 = None, val = None):
    cnt = 0
    cnt2 = 0
    for i in l:
        if i.l[index2] == val:
            if i.l[decision_index] == positive_val :
                cnt+=1
            else:
                cnt2+=1

    return cnt,cnt2

def entropy(p,n):
    if p==n:
        return 1
    elif p==0 or n==0:
        return 0
    t = p+n
    res = (p/t) * log2(p/t)
    res2 = (n/t) * log2(n/t)

    r = -res - res2
    return r

def gain(l,index):
    decision_index = len(l[0].l) - 1
    p,n = find_total_positive_negetive(l,decision_index,"Yes")
    if p == 0 or n == 0:
        if p == 0 :
            return 10
        else :
            return 20

    e_s = entropy(p,n)

    total_data = len(l)
    condition_no = len(data.d_l[index])
    conditions = data.d_l[index]
    e_list = []
    e_list.append(e_s)
    i=0
    while i<condition_no:
        p, n = f_p_n(l, decision_index, "Yes", index, conditions[i])
        total = p + n
        e = entropy(p,n)
        e = e * total / total_data
        e = -e
        e_list.append(e)
        i+=1

    gain_result = sum(e_list)
    return gain_result

def gain_generation(l,except_index):

    n = len(l[0].l)
    already_done = data.tree.copy()
    except_list = []
    j = 0
    while j<len(already_done):
        r = data.name.index(already_done[j])
        except_index.append(r)
        j+=1
    g = []
    i = 1
    while i< n:
        if i in except_index:
            i+=1
            continue
        g1 = gain(l,i)
        g.append(g1)
        i+=1
    return g

def choose(g):
    break_point1 = 10
    break_point2 = 20
    if break_point1 in g:
        return -1
    if break_point2 in g:
        return -2

    m = max(g)
    i = g.index(m)
    lent1 = len(data.name)-2
    lent2 = len(g)
    if lent1 == lent2:
        return i+1
    else:
        return i+1+lent1-lent2

def generate_inner_list(l,index,condition):
    l2 = []
    for i in l:
        if i.l[index] == condition:
            l2.append(i)
    return l2

def new_list_generation(l,index_name):
    index = data.name.index(index_name)
    conditions = []
    conditions = data.d_l[index].copy()
    l2 = []
    for i in conditions:
        l2.append(generate_inner_list(l,index,i))

    return l2

def repeated_gain(l,except_index):
    total_new_list = len(l)
    cnt = 0
    conditions = data.tree[len(data.tree)-1]
    conditions = data.d_l[data.name.index(conditions)]
    i_s = len(data.tree)-1

    for i in range(total_new_list):
        g = gain_generation(l[i],except_index)
        index = choose(g)
        if index < 0 :
            if index == -1:
                string1 = data.tree[i_s] + ',' + conditions[cnt]
                data.try_tree[string1] = 'No'
            else:
                string1 = data.tree[i_s] + ',' + conditions[cnt]
                data.try_tree[string1] = 'Yes'
        else :
            string1 = data.tree[i_s] + ',' + conditions[cnt]
            data.try_tree[string1] = 'Check,' +data.name[index]
            data.tree.append(data.name[index])
            l2 = new_list_generation(l[i], data.tree[len(data.tree) - 1])
            repeated_gain(l2,except_index)

        cnt+=1

def predict():
    print('Enter Data To predict : ')
    s1 = data.tree[0]
    s2 = 'Check'
    s3 = 'Yes'
    s4 = 'No'
    while True:
        x = input(s1 + ' : ')
        x = s1 + ',' + x
        result = data.try_tree[x]
        result = result.strip()
        list = result.split(',')
        if s2 in list:
            s1 = list[1]
        if s3 in list:
            print('Yes')
            break
        if s4 in list:
            print('No')
            break


def main():
    l = create_decision_tree()
    l = find_total_distinct_values_for_every_situation(l)
    g = []
    except_index = [0,len(l[0].l)-1]
    g = gain_generation(l,except_index)
    index = choose(g)
    data.tree.append(data.name[index])
    l2 = new_list_generation(l,data.tree[len(data.tree)-1])
    repeated_gain(l2,except_index)
    print(data.tree)
    print(data.try_tree)
    predict()

main()


