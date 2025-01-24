import pandas as pd
import numpy as np
import matplotlib as mpl
import json
import math

f = open('rds.json','r')
relative_diffsets = json.load(f)
f.close()

print(f'read {len(relative_diffsets.keys())} data items\n')

# relative_diffsets is a python dictionary; each entry is the "name" of a set of parameters, e.g. "RDS(73,7,64,8)"
# the dictionary entries contain 
#          "status": either "All", "Yes", "Open" or "No", (all known, exist, open, or known not to exist),
#          "comment": information about how the status is known,
#          "sets": a list of known relative difference sets for these parameters

# these functions help to access the dictionary

#status of parameters
def get_status(D):
    if 'status' in relative_diffsets[D]:
        return relative_diffsets[D]['status']
    return None

def get_comment(D):
    if 'comment' in relative_diffsets[D]:
        return relative_diffsets[D]['comment']
    return None


# number of sets known for these parameters
def num_sets(D):
    if "sets" not in relative_diffsets[D]:
        return 0

    return len(relative_diffsets[D]["sets"])

# pull parameters out from name D
def get_m(D):
    S = D.split(',')
    return int(S[0].split('(')[1])

def get_n(D):
    S = D.split(',')
    return int(S[1])

def get_k(D):
    S = D.split(',')
    return int(S[2])

def get_lam(D):
    S = D.split(',')[3].split(')')[0]
    return int(S)

#get the ith set as a list
def get_set(D,i):
    if 'sets' not in relative_diffsets[D] or (len(relative_diffsets[D]['sets']) <= i):
        print('error: no such set')
        return
    return relative_diffsets[D]['sets'][i]

# print one set
def print_set(D,i):
    S = D.split(',')
    m = int(S[0].split('(')[1])
    n = int(S[1])
    k = int(S[2])
    lam = int(S[3].split(')')[0])
    print(f'\n{D}',end='')
    print(f'\n\tR={relative_diffsets[D]["sets"][i][0]}')
    

# get the ith (m,n,k,lambda) relative difference set, as a list
def get_rds(m,n,k,lam,i):
    rdsname = f'RDS({m},{n},{k},{lam})'.replace(' ','')
    if rdsname not in relative_diffsets:
        print(f'{rdsname} not in database')
        return

    D = relative_diffsets[rdsname]
    if ('sets' not in D) or (len(D['sets']) <= i):
        print('no such set')
        return

    return [m,n,k,lam,D['sets'][i]]


# get number of RDS(m,n,k,lam) sets, if any
# NOTE: this is different than num_sets() above in that its argument is the dictionary entry, not the RDS "name"
def set_count(rds):
    if 'sets' not in rds:
        return 0
    return len(rds['sets'])

# print out information about a given RDS
def get_rds_data(m,n,k,lam):
    rdsname = f'RDS({m},{n},{k},{lam})'.replace(' ','')
    if rdsname not in relative_diffsets:
        print(f'{rdsname} not in database')
        return

    D = relative_diffsets[rdsname]
    if D['status']=="All":
        if set_count(D)>1:
            print(f'There are exactly {set_count(D)} cyclic ({m},{n},{k},{lam})-RDS')
        else:
            print(f'There is exactly {set_count(D)} cyclic ({m},{n},{k},{lam})-RDS')

    if D['status']=="Yes":
        if set_count(D)>1:
            print(f'There are at least {set_count(D)} cyclic ({m},{n},{k},{lam})-RDS')
        else:
            if set_count(D)>0:
                print(f'There is at least {set_count(D)} cyclic ({m},{n},{k},{lam})-RDS')
            else:
                print(f'There is at least one cyclic ({m},{n},{k},{lam}), but it is not in this dataset')

    if D['status']=="No":
            print(f'No RDS({m},{n},{k},{lam}) exists')

    if 'comment' in D:
        print(f'Reference: {D["comment"]}\n')

    for i in range(set_count(D)):
        rds = D['sets'][i]
        if set_count(D) > 1:
            print(f'{i}:\t',end='')
        print(f'R = {rds}')


# code to create tables for showing a list of relative difference sets
def init_tab():
    T = {}
    T['m'] = []
    T['n'] = []
    T['k'] = []
    T['lambda'] = []
    T['status'] = []
    T['comment'] = []
    T['set'] = []
    return T

def add_tab_entry(T,D):
    m = int(D.split(',')[0].split('(')[1])
    n = int(D.split(',')[1])
    k = int(D.split(',')[2])
    lam = int(D.split(',')[3].split(')')[0])
    if num_sets(D) ==0:  # no set to show
        T['m'] += [m]
        T['n'] += [n]
        T['k'] += [k]
        T['lambda'] += [lam]
        T['status'] += [relative_diffsets[D]['status']]
        T['comment'] += [relative_diffsets[D]['comment']]
        T['set'] += ['RDS known to exist but not in database']
    else:
        for i in range(num_sets(D)):
            T['m'] += [m]
            T['n'] += [n]
            T['k'] += [k]
            T['lambda'] += [lam]
            T['status'] += [relative_diffsets[D]['status']]
            T['comment'] += [relative_diffsets[D]['comment']]
            T['set'] += [str(get_set(D,i))]

def show_tab(T):
    df = pd.DataFrame(T)
    df = df.style.hide(axis='index')
    return df


