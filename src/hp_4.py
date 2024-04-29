# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(old_date, "%Y-%m-%d").strftime('%d %b %Y') for old_date in old_dates]

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    date_objects = []
    strd = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        date_objects.append(strd + timedelta(days=i))
    return date_objects


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    values_list = len(values)
    range_dates = date_range(start_date, values_list)
    finalList = list(zip(range_dates, values))
    return finalList


def fees_report(infile, outfile):
    file_columns = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    fees = defaultdict(float)
    with open(infile, 'r') as f:
        lines = DictReader(f, fieldnames=file_columns)
        rows = [row for row in lines]
    rows.pop(0)
    for each_row in rows:
        patronID = each_row['patron_id']
        date_due = datetime.strptime(each_row['date_due'], "%m/%d/%Y")
        date_returned = datetime.strptime(each_row['date_returned'], "%m/%d/%Y")
        daysLate = (date_returned - date_due).days
        fees[patronID]+= 0.25 * daysLate if daysLate > 0 else 0.0
    outputData = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in fees.items()
    ]
    with open(outfile, 'w') as f:
        writer = DictWriter(f,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(outputData)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
