file = 'C10_sysinfo_20170909'

A = {}
with open(file,'r') as f:
    lists = [ line.split('|') for line in f.readlines()]
    for lis in lists:
        A[lis[0]] = lis[1]

    for key in A:
        print(key+':'+A[key])