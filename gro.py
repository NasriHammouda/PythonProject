def main():
    import shelve
    with shelve.open('drows.db') as allrows:  
        allrows['0'] = {1:'foo', 2:'bar', 3:'Lumberjack', 4:'Knights'}
        allrows['Hello'] = {'foo':'Hello', 'bar':'World', 'Lumberjack': '?', 'Knights':'?'}
        allrows['Spam'] = {'foo':'Spam', 'bar':'Eggs', 'Lumberjack': '?', 'Knights':'?'}
    
    allrows = shelve.open('drows.db')

    fargs = {}
    for item in allrows['0']:
        fname = allrows['0'][item]
        if fname in globals():
            fargs[fname] = {}
            from inspect import signature, _empty
            sig = signature(eval(fname))
            print("%s is a function with arguments %s" % (fname, sig))
            for param in sig.parameters.values():
                pname = param.name
                pdefault = param.default
                if pdefault is _empty:
                    fargs[fname][pname] = None
                    print('Required parameter: %s %s' % (fname, pname))
                else:
                    fargs[fname][pname] = pdefault
                    print('I have default value for: %s %s %s' % (fname, pname, pdefault))
    print(fargs)

    for item in allrows:
        if item != '0':
            print("%s: %s" % (item, allrows[item]))

def delrow(allrows, rowkey):
    try:
        del allrows[rowkey]
    except:
        pass

def Knights():
    return "Ni" 

def Lumberjack(job, play='', status='Okay'):
    return "I'm okay"        

if __name__ == "__main__":
    main() 