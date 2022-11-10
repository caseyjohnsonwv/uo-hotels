import argparse
from datetime import datetime, timedelta
from drivers.query import UO
from objects.promo import Promo

# accept and valdiate arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--check-in', help='Date string in the form yyyy-mm-dd')
parser.add_argument('-o', '--check-out', help='Date string in the form yyyy-mm-dd')
parser.add_argument('-n', '--nights', help='Number of nights for the stay')
parser.add_argument('--family-and-friends', action='store_true', default=False)
parser.add_argument('--red-carpet-rate', action='store_true', default=False)
ARGS = parser.parse_args()

nullcount = sum([1 if arg is None else 0 for arg in [ARGS.check_in, ARGS.check_out, ARGS.nights]])
assert nullcount <= 1
nights = (datetime.fromisoformat(ARGS.check_out) - datetime.fromisoformat(ARGS.check_in)).days if ARGS.nights is None else int(ARGS.nights)
check_in = datetime.fromisoformat(ARGS.check_out) - timedelta(days=nights) if ARGS.check_in is None else datetime.fromisoformat(ARGS.check_in)
check_out = datetime.fromisoformat(ARGS.check_in) + timedelta(days=nights) if ARGS.check_out is None else datetime.fromisoformat(ARGS.check_out)
if nullcount == 0:
	assert (check_in - check_out).days == nights

truecount = sum([1 if arg else 0 for arg in [ARGS.family_and_friends, ARGS.red_carpet_rate]])
assert truecount <= 1
if ARGS.family_and_friends is not None:
	promo = Promo.FAMILY_AND_FRIENDS
elif ARGS.red_carpet_rate is not None:
	promo = Promo.RED_CARPET_RATE
else:
	promo = Promo.NONE


# start actually doing things
check_in_fmt = datetime.strftime(check_in, '%m/%d/%Y')
check_out_fmt = datetime.strftime(check_out, '%m/%d/%Y')
deals = UO.get_deals(check_in_fmt, nights, promo)

for d in sorted(deals, key=lambda d:d.rate):
	print(d)
