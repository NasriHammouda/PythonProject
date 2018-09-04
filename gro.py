import globs

class Credentials (object):
  def __init__ (self, access_token=None):
    self.access_token = access_token

  def refresh (self, http):
    # get new access_token
    # this only gets called if access_token is None
    return

def main():
    allrows = ''
    globs.DBSOURCE = 'gdocs'
    if globs.DBSOURCE == 'local':
        import shelve
        with shelve.open('drows.db') as allrows:  
            allrows['0'] = {1:'foo', 2:'bar', 3:'Lumberjack', 4:'Knights'}
            allrows['Hello'] = {'foo':'Hello', 'bar':'World', 'Lumberjack': '?', 'Knights':'?'}
            allrows['Spam'] = {'foo':'Spam', 'bar':'Eggs', 'Lumberjack': '?', 'Knights':'?'}
        allrows = shelve.open('drows.db')
    elif globs.DBSOURCE == 'gdocs':
        import pickle, gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('gropey_secret.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("use this").sheet1
        climit = wks.col_count
        rlimit = wks.row_count
        for i in range(1, rlimit):
            arow = wks.row_values(i)
            if arow:
                print(str(arow))
            else:
                break
        #for row in wks.row_values:
        #    print(str(row))
        #row = wks.get_all_values()
        #print(str(row))
        #wks.update_acell('B2', "it's down there somewhere, let me take another lookxxx.")
        #cell_list = wks.range('A1:B7')   
    else:
        pass

    return

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

