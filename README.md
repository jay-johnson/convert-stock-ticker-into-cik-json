The Python Sec Indexer Repository
------
Version 1.0

Using Python, take a list of Stock Ticker Symbols from a file and (if it exists) get the associated SEC CIK with the Company Name written into a JSON output file.  This uses python script uses the SEC Edgar website's searching functionality.


Setup
------

To run this have the python dependencies installed:
beautifulsoup
json
pickle
requests

Usage
------

Compile the latest Stock Ticker Symbols into a single file. For this build I used the NASDAQ csv's available here: http://www.nasdaq.com/screening/company-list.aspx

After copying and appending them into a single file I sorted and filtered one uniques 

    cat unsorted_single_entry_file | sort | uniq > data/newest_ticker_symbol_file.txt

Make sure to update the TICKERS_FILE line too in convert_ticker_to_cik.py

Defaults for reference assume the all_tickers and output file go in the ./data directory:

TICKERS_FILE            = "data/all_tickers.txt"

OUTPUT_JSON_FILE_PATH   = "data/ticker_to_cik_mapping.json"

To run:
./convert_ticker_to_cik.py


Credits
------

Doug van Kohorn for getting me started: https://gist.github.com/dougvk/8499335


Additional / License
------

This is free to use MIT LICENSE and all that fun.

Enjoy.






