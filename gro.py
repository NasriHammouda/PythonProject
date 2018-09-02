import shelve
# Make our data persistent
with shelve.open('drows.db') as s:
    # Created first dict
    # And make a dict of dicts
    s['drows'] = {
        'foo':{1:'foo', 2:'bar', 3:'Lumberjack', 4:'I work all day'},
        'bar':{1:'foo', 2:'bar', 3:'Lumberjack', 4:'I work all day'}
    } 

with shelve.open('drows.db') as s:
    drow = s['drows']
    
for item in drow:
    print(drow[item])