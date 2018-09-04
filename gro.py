import globs

def main():
    for dbsource in ['gdocs', 'local']:
        dosheet(dbsource)

def dosheet(dbsource):
    allrows = ''
    if dbsource == 'local':
        import shelve, csv
        allrows = shelve.open('drows.db')
        with open('sample.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for globs.lastrow, row in enumerate(spamreader):
                allrows[str(globs.lastrow)] = row
            for row in spamreader:
                print(', '.join(row))
        allrows.close()       
        allrows = shelve.open('drows.db')
        for rowkey in allrows:
            print(allrows[rowkey])
    elif dbsource == 'gdocs':
        import pickle, gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('gropey_secret.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("use this").sheet1
        for globs.lastrow in range(1, wks.row_count):
            arow = wks.row_values(globs.lastrow)
            if arow:
                print(str(arow))
            else:
                break 
    else:
        pass

    return

    '''
    fargs = {}
    for item in allrows['0']:
        fname = allrows['0'][item]
        if fname in globals():
            fargs[fname] = {}
            from inspect import signature, _empty
            sig = signature(eval(fname))
            # print("%s is a function with arguments %s" % (fname, sig))
            for param in sig.parameters.values():
                pname = param.name
                pdefault = param.default
                if pdefault is _empty:
                    fargs[fname][pname] = None
                    #print('Required parameter: %s %s' % (fname, pname))
                else:
                    fargs[fname][pname] = pdefault
                    #print('I have default value for: %s %s %s' % (fname, pname, pdefault))
    # print(fargs)
    '''

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

