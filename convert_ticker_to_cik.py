#!/usr/bin/python

import os, sys, re, json, urllib, urllib2
from   cPickle import dump
from   requests import get
from   BeautifulSoup import BeautifulSoup
 
# define this to your file:
TICKERS_FILE            = "data/all_tickers.txt"
OUTPUT_JSON_FILE_PATH   = "data/ticker_to_cik_mapping.json"
DEFAULT_TICKERS         = open(TICKERS_FILE).readlines()
URL                     = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
CIK_RE                  = re.compile(r'.*CIK=(\d{10}).*')
CNAME_RE                = re.compile(r'.*class="companyName">(.*) <acronym ')
HEADER_COLOR            = '\033[95m'
BLUE_COLOR              = '\033[94m'
GREEN_COLOR             = '\033[92m'
WARNING_COLOR           = '\033[93m'
FAIL_COLOR              = '\033[91m'
END_COLOR               = '\033[0m'
cik_dict                = { "Records"   : [] }
ticker_idx              = 0
num_tickers             = len(DEFAULT_TICKERS)


def announcement_print(msg):
    print "" + WARNING_COLOR + str(msg) + END_COLOR
    return None
# end of announcement_print
        

def green_print(msg):
    print "" + GREEN_COLOR + str(msg) + END_COLOR
    return None
# end of green_print
        
        
def red_print(msg):
    print "" + FAIL_COLOR + str(msg) + END_COLOR
    return None
# end of red_print


# Start Processing:

announcement_print("Finding CIK and Company Names for Tickers(" + str(num_tickers) + ")")

while ticker_idx < num_tickers:
    
    try:

        ticker  = str(DEFAULT_TICKERS[ticker_idx]).strip("\n")
        print "Finding(" + str(ticker_idx) + ") for Cik Stock Ticker(" + str(ticker) + ") Percent Done(" + str(float(ticker_idx)/float(num_tickers)*100.00) + ")"

        full_results    = get(URL.format(ticker)).content

        results         = CIK_RE.findall(full_results)
        if len(results):
            cik             = str(results[0])
            name_array      = CNAME_RE.findall(full_results)
            html_name       = str(name_array[0])
            company_name    = json.dumps(BeautifulSoup(html_name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents)[2:-2]

            if company_name != "":
                cik_dict["Records"].append({
                                                "CIK"       : cik.strip(),
                                                "Ticker"    : ticker.upper().strip(),
                                                "Name"      : company_name.upper()
                })
                green_print("   Stock(" + str(ticker) + ") CIK(" + str(cik) + ") Name(" + str(company_name) + ")")
            else:
                red_print("    No SEC Edgar Company Name for Stock Ticker(" + str(ticker) + ")")

            # end of valid stock ticker result
        else:
            red_print("    No SEC Edgar CIK and Name for Stock Ticker(" + str(ticker) + ")")

        # end of if there are results

    except Exception,e:

        red_print("ERROR: Failed to retrieve Stock Ticker Information from Ticker(" + str(ticker) + ") Ex(" + str(e) + ")")

    ticker_idx += 1

# end of for all Stock Tickers to find

announcement_print("Done Looking up All CIK and Company Names for Tickers(" + str(num_tickers) + ")")

output_json_dict    = json.dumps(cik_dict, sort_keys=True, indent=4, separators=(',', ': ')) + "\n"
output_file         = open(OUTPUT_JSON_FILE_PATH, 'w')
output_file.write(output_json_dict)
output_file.close()


sys.exit(0)


