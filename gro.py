import shelve
with shelve.open('drows.db') as s:
    s['drows'] = {1:'foo', 2:'bar', 3:'Lumberjack', 4:'I work all day'}
with shelve.open('drows.db') as s:
    drow = s['drows']
for item in drow:
    print(drow[item])