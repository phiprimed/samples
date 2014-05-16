#!/usr/bin/env python

# Scheme Code;ISIN Div Payout/ ISIN Growth;ISIN Div Reinvestment;Scheme Name;Net Asset Value;Repurchase Price;Sale Price;Date

import urllib2

url = "http://portal.amfiindia.com/spages/NAV0.txt"
code_tab = {}
isin_tab = {}

data = urllib2.urlopen(url).readlines()

for line in data:
  line = line.strip()
  toks = line.split(';')
  if len(toks) == 8:
    #val = (toks[0], toks[1], toks[2], toks[3], toks[4], toks[5], toks[6], toks[7])
    val = toks
    code_tab[toks[0]] = val
    if toks[1] != None and toks[1] != '-' and toks[1] != '#N/A':
      isin_tab[toks[1]] = val

for k in code_tab.keys():
  if k != None:
    val_code = code_tab[k]
    if val_code[1] != None and val_code[1] != '-'  and val_code[1] != '#N/A': 
      val_isin = isin_tab[val_code[1]]
      if val_code != val_isin:
        print "Problem", val_code, val_isin

# Type,AccountNo,Owner(s),Company,Balance,Principal,Gain,ID,ISIN,NumUnits,Current NAV,Start date,End Date,Interest Rate,Notes

rfile = '~/Desktop/qFinances.csv'
total_balance = 0.0
total_gain = 0.0
with open(rfile, 'rU') as f:
  for line in f:
    line = line.strip();
    toks = line.split(',')
    if len(toks) == 15:
      if toks[0].strip() == 'MF' or toks[0].strip() == 'MF-RM':
        val = code_tab[toks[7]]
        #print val
        NAV = val[6]
        if NAV == "0" or NAV == "N.A." or float(NAV) == 0.0:
          NAV = val[4]
        toks[10] = NAV
        balance = float(toks[9])*float(NAV)
        toks[4] = str(balance)
        #print "Balance = ", balance
        gain = balance - float(toks[5])
        toks[6] = str(gain)
        total_balance = total_balance + balance
        total_gain = total_gain + gain
        print ','.join(toks)

print "Total Balance = ", total_balance
print "Total Gain = ", total_gain
