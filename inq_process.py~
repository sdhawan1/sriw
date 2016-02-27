
#in this file, process the "inq_process" dictionary and reformat it.

import xlrd

inqbook = xlrd.open_workbook('inquirerbasic.xls')
sheet = inqbook.sheets()[0]
numrows = sheet.nrows
#[for debugging] print numrows

#now, read each row, and compile a list of positive and negative words

poswds = []
negwds = []
for i in range(1, numrows):
    #cell 0 in the row (should) correspond to the text value of the word
    val = sheet.cell(i, 0).value
    if (type(val) == type(0)):
        continue
    word = sheet.cell(i, 0).value.encode('utf8', 'ignore')

    #cell 2 should correspond to "positive" outlook
    p = sheet.cell(i, 2).value.encode('utf8', 'ignore')
    if not (p == ''): #if cell 2 in a row is nonempty, the word is positive.
        poswds += [word.lower()]

    #cell 3 should correspond to "negative" outlook
    
    n = sheet.cell(i, 3).value.encode('utf8', 'ignore')
    if not (p == ''):
        negwds += [word.lower()]

#print poswds

## NEXT, PRINT INTO FILE
fpos = open('hvd_poswds', 'w')
ftxt = ('\n').join(poswds)
fpos.write(ftxt)
fpos.close()

fneg = open('hvd_negwds', 'w')
ftxt = ('\n').join(negwds)
fneg.write(ftxt)
fneg.close()

## NEXT, TRY TO FIND SCORES OF NEG AND POS SENTIMENT (BETW 0&1) IF POSSIBLE...
