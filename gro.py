import globs

def main():
    for dbsource in ['gdocs', 'local']:
        dosheet(dbsource)
        print(globs.fargs)
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
        dofuncs(arow)
    else:
        print(arow)

def dofuncs(arow):
    fargs = {}
    for rowdex, fname in enumerate(arow):
        rowdex += 1
        if fname in globals():
            fargs[rowdex] = {}
            from inspect import signature, _empty
            sig = signature(eval(fname))
            for param in sig.parameters.values():
                pname = param.name
                pdefault = param.default
                if pdefault is _empty:
                    fargs[rowdex][pname] = None
                else:
                    fargs[rowdex][pname] = pdefault
    globs.fargs = fargs

    

def Func1():
    return "Ni" 

def Func2(param1, param2='', status='Okay'):
    return "I'm okay"        

if __name__ == "__main__":
    main()

