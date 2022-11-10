import argparse
from datetime import datetime, timedelta
import xlsxwriter
from drivers.query import UO
from objects.promo import Promo
from objects.hotelrate import HotelRate

# accept and valdiate arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--check-in', help='Date in the form mm/dd/yyyy or date range in the form mm/dd/yyyy-mm/dd/yyyy', required=True)
parser.add_argument('-n', '--nights', help='Integer number of nights for the stay or integer range in the form X-Y', required=True)
parser.add_argument('--family-and-friends', action='store_true', default=False)
parser.add_argument('--red-carpet-rate', action='store_true', default=False)
ARGS = parser.parse_args()

check_in = str(ARGS.check_in).split('-')
earliest_check_in = datetime.strptime(check_in[0], '%m/%d/%Y')
latest_check_in = datetime.strptime(check_in[1], '%m/%d/%Y') if len(check_in) > 1 else earliest_check_in
if earliest_check_in > latest_check_in:
	earliest_check_in, latest_check_in = latest_check_in, earliest_check_in
del check_in

nights = str(ARGS.nights).split('-')
min_nights = int(nights[0])
max_nights = int(nights[1]) if len(nights) > 1 else min_nights
if min_nights > max_nights:
	min_nights, max_nights = max_nights, min_nights
del nights

truecount = sum([1 if arg else 0 for arg in [ARGS.family_and_friends, ARGS.red_carpet_rate]])
assert truecount <= 1
if ARGS.family_and_friends:
	promo = Promo.FAMILY_AND_FRIENDS
elif ARGS.red_carpet_rate:
	promo = Promo.RED_CARPET_RATE
else:
	promo = Promo.NONE


# do actual scraping work
deals = []
check_in = earliest_check_in
while check_in <= latest_check_in:
	check_in_fmt = datetime.strftime(check_in, '%m/%d/%Y')
	for night_count in range(min_nights, max_nights+1):
		print(f"Querying {night_count}-night stays with check-in on {check_in_fmt}")
		deals.extend(UO.get_deals(check_in_fmt, night_count, promo))
	check_in += timedelta(days=1)
deals.sort(key=lambda d:d.total)


# dump output to an excel sheet
workbook = xlsxwriter.Workbook('UO_Hotels.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write_row(0, 0, data=HotelRate.csv_header_row())
for i,d in enumerate(deals):
	worksheet.write_row(row=i+1, col=0, data=d.as_csv_row())

worksheet.autofilter(0, 0, len(deals), len(HotelRate.csv_header_row()))
workbook.close()
print('Saved results to UO_Hotels.xlsx')