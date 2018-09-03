def main():
    import shelve
    # Make our data persistent
    # Created first dict
    # And make a dict of dicts
    with shelve.open('drows.db') as s:
        
        s['foo'] = {1:'foo', 2:'bar', 3:'Lumberjack', 4:'I work all day'}
        s['bar'] = {1:'foo', 2:'bar', 3:'Lumberjack', 4:'I work all day'}

    s = shelve.open('drows.db')

    for item in s:
        # print(item + ": " + str(s[item]))
        print("%s: %s" % (item, s[item])) # this is a tuple

def delrow(s, rowkey):
    try:
        del s[rowkey]
    except:
        pass
        
if __name__ == "__main__":
    main() 