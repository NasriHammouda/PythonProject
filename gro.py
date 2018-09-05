import globs

def main():
    globs.gfuncs = [x.lower() for x in globals().keys() if x[:2] != '__']
    for dbsource in ['gdocs', 'local']:
        dosheet(dbsource)
        print()

def dosheet(dbsource):
    allrows = ''
    if dbsource == 'local':
        import shelve, csv
        allrows = shelve.open('drows.db')
        with open('sample.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for rowdex, arow in enumerate(reader):
                allrows[str(rowdex + 1)] = arow
            #for row in spamreader:
                #print(', '.join(row))
        allrows.close()       
        allrows = shelve.open('drows.db')
        for rowkey in sorted(allrows):
            dorow(rowkey, allrows[rowkey])
    elif dbsource == 'gdocs':
        import pickle, gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('gropey_secret.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("use this").sheet1
        for rowdex in range(1, wks.row_count):
            arow = wks.row_values(rowdex)
            if arow:
                dorow(str(rowdex), arow)
            else:
                break 
    else:
        pass

def dorow(rownum, arow):
    if rownum == '1':
        globs.funcs = [x.lower() for x in arow]
        #print(globs.funcs)
        row1funcs(arow)
    else:
        for coldex, acell in enumerate(arow):
            if globs.funcs[coldex] in globs.gfuncs:
                if acell == '?':
                    evalfunc(coldex, arow)        


def evalfunc(coldex, arow):    
    fname = globs.funcs[coldex]
    #print(globs.fargs)
    #return
    fargs = globs.fargs[coldex]
    evalme = "%s(" % fname
    if fargs:
        #print(fname, fargs)
        for anarg in fargs:
            evalme = "%s%s='xxx', " % (evalme, anarg)
            # fargs[anarg] == None:
                #print(fname, anarg)
        evalme = evalme[:-2] + ')'
        print(evalme)


def row1funcs(arow):
    fargs = {}
    for coldex, fname in enumerate(arow):
        if fname.lower() in globs.gfuncs:
            fargs[coldex] = {}
            from inspect import signature, _empty
            sig = signature(eval(fname))
            for param in sig.parameters.values():
                pname = param.name
                pdefault = param.default
                if pdefault is _empty:
                    fargs[coldex][pname] = None
                else:
                    fargs[coldex][pname] = pdefault
    print(fargs)
    globs.fargs = fargs


                    


def Func1():
    return "No arguments here" 

def Func2(param1, param2='', status='Okay'):
    return "My params are: %s, %s" % (param1, param2)        

if __name__ == "__main__":
    main()

