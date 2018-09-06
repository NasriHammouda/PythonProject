""" Pipulate lets you collect data straight off of the Web into spreadsheets

______ _             _       _                            
| ___ (_)           | |     | |                           
| |_/ /_ _ __  _   _| | __ _| |_ ___   ___ ___  _ __ ___  
|  __/| | '_ \| | | | |/ _` | __/ _ \ / __/ _ \| '_ ` _ \ 
| |   | | |_) | |_| | | (_| | ||  __/| (_| (_) | | | | | |
\_|   |_| .__/ \__,_|_|\__,_|\__\___(_\___\___/|_| |_| |_|
        | |                                               
        |_|                                               


Got a list that you need to look up something for eveyr item - like grabbing
litle tags for a list of URLs? Well, then Pipulate is your answer! For example,
for any given URL. you will be able to:
    
    1. Record the number of times that URL has appeared in a Tweet
    2. Record the number of times that URL was liked or shared in Facebook
    3. Record the number if times that URL was +1'd in Google Plus
    4. Figure out what keyword the page is trying to target for search traffic
    5. See how well that URL is doing for that keyword (position tracking)

And it all accumulates on a spreadsheet where you can do trending and keep track
of progress - all for free! But Pipulate is so much more, able to do such
lookups using any source data (addresseds, keywords, etc.) against any Web or data API
source (you have access to), allowing you to write your own Python functions to extend
system. And what system is that? You can learn it well, because almost every line of code
accompanied by a Youtube video. Playlist in mikelevinseo youtube channel. 
"""

import globs #Create objects that don't have to be passed as arguments

def main():
    """Allows processing of multiple worksheets

    The purpose of this function is to feed Python lists representing rows
    of a worksheet into the processrow function, which handles question mark
    replacement. This is the outer loop of that process representing the entire
    worksheet. In the first case, data can be loaded into a shelve object from
    csv and other sources for processing large datasets and scheduled tasks, or
    in the second case, from Google Spreadsheets for smaller datasets, but a more
    interactive approach."""
    funcs = [x for x in globals().keys() if x[:2] != '__'] #list all functions
    globs.funcslc = [x.lower() for x in funcs] #lower-case all function names
    globs.transfunc = dict(zip(globs.funcslc, funcs)) #Keep translation table
    for dbsource in ['gdocs', 'local']: #Each dbsource represents one worksheet
        dbmethod = {'local': dblocal, 'gdocs': dbgdocs}
        dbmethod[dbsource]()
        print()

def dblocal():
    #This is the "shelve" route, necessary for big data sets, useful for csv's
    import shelve, csv
    allrows = shelve.open('drows.db')
    with open('sample.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for rowdex, arow in enumerate(reader): #Dump entire csv into shelve.
            allrows[str(rowdex + 1)] = arow
    allrows.close()
    #We can add support for much more than csv here through "shove" module       
    allrows = shelve.open('drows.db')
    for rowkey in sorted(allrows): #Process each row (list) from the shelve
        processrow(rowkey, allrows[rowkey])

def dbgdocs():
    #This is the Google Spreadsheet route for smaller interactive sessions.
    import pickle, gspread
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gropey_secret.json', scope)
    gc = gspread.authorize(credentials)
    try:
        wks = gc.open("use this").sheet1 #HTTP connections errors happen here.
    except:
        print("Couldn't reach Google Docs")
        return
    for rowdex in range(1, wks.row_count): #Start stepping through every row
        arow = wks.row_values(rowdex)
        if arow: #But only process it if it does not come back as empty list
            processrow(str(rowdex), arow)
        else:
            break #Stop grabbing new rows at the first empty one encoutered

def processrow(rownum, arow):
    """Separates row-1 handling from question mark dection on all other row.

    Called on each row of a worksheet and either initializes functions when it's row 1
    or steps cell by cell along each subsequent (fed-in) row and when encountering a 
    question mark, it determines whether to invoke the functionindicated by 
    the column label, using values from the active row as parameter values
    if available, parameter defaults if not, and None if not found."""
    if rownum == '1':
        #Row 1 is always specially handled because it contains functions names.
        globs.row1 = [x.lower() for x in arow]
        row1funcs(arow)
    else:
        #All subsequent rows are checked for question mark replacement requests.
        for coldex, acell in enumerate(arow):
            if globs.row1[coldex] in globs.funcslc:
                if acell == '?':
                    evalfunc(coldex, arow)        

def row1funcs(arow):
    """Scans row-1 for names of global functions and builds dict of requirements

    This is only invoked on row 1 of a worksheet, where the names of functions
    and parameters are excepted to be discovered. By the end, we've created a
    dictionary of dictionaries called globs.fargs which plays an important role
    in building the code necessary for question mark replacement."""
    fargs = {}
    for coldex, fname in enumerate(arow):
        if fname.lower() in globs.funcslc: #Detect if column name is a function
            fargs[coldex] = {}
            from inspect import signature, _empty
            sig = signature(eval(fname))
            for param in sig.parameters.values(): #Build dict of function requirements
                pname = param.name
                pdefault = param.default
                if pdefault is _empty: #Catch when an argument has no default value
                    fargs[coldex][pname] = None
                else:
                    fargs[coldex][pname] = pdefault
    globs.fargs = fargs #Make dict global so we don't have to pass it around

def evalfunc(coldex, arow):
    """Build string to execute to get values to replace question mark with.
    
    Once a question mark is found in a cell belonging to a fuction-name
    colum, the exact invocation that's needed must be built, keeping in mind
    default values provide by function itself, as well as parameter values
    provided in the provided row. Because rows are being handled as lists, order is
    important, and the column index allows functions name lookup."""    
    fname = globs.transfunc[globs.row1[coldex]]
    fargs = globs.fargs[coldex]
    evalme = "%s(" % fname #Begin building string that will eventually be eval'd
    if fargs:
        #The function we're looking at DOES have required arguments
        for anarg in fargs:
            #Add on arg=value to string for each required argument.
            anarg = anarg.lower()
            argval = getargval(anarg, fargs[anarg], arow)
            evalme = "%s%s=%s, " % (evalme, anarg, argval)
        evalme = evalme[:-2] + ')' #Finish building string for the eval statement.
    else:
        #No arguments required, so just immediately close the parenthesis.    
        evalme = evalme + ')'
    print('%s: %s' % (evalme, eval(evalme)))


def getargval(anarg, defargval, arow):
    """Returns value to set argument equal-to in fuction invocation string.

    This function returns which value should be used as the arguments to the
    function invocation string being built. The value found on the row always
    beats the default provided by the function. Lacking values on the row and a
    default, the Python value of None will be returned."""
    for coldex, acol in enumerate(globs.row1):
        if acol == anarg: #Found column named same thing a required argument.
            if arow[coldex]: #The cell in that column has a non-zero/empty value.
                return adq(arow[coldex]) #So, we got what we need. return it.
    #Oops, no required argument were found on the row.
    if defargval:
        return adq(defargval) #So, if it's got a default value, return that.
    else:
        return None #We ALWAYS have to return at least None, least errors ensue.

def adq(aval):
    """Conditionally builds quotes on arg-value for function invocation string.

    This handles the value quoting details when building argument part of the
    function invocation string when replacing a question mark. For example, the
    keyword None must not become quoted. Typically, numbers shouldn't be quoted
    either, but we're feeding everything but None around as strings for now."""
    if not aval:
        return None #None-in/None-out. This special keyword shouldn't be quoted.
    else:    
        return "'%s'" % (aval) #ALMOST everything else should be quoted



def Func1():
    return "No arguments here" 

def Func2(param1, param2='', status='Okay'):
    return "My params are: %s, %s" % (param1, param2)        

if __name__ == "__main__":
    main()
