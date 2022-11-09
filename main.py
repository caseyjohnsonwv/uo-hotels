from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import env


class Promos:
	FAMILY_AND_FRIENDS = env.FAMILY_AND_FRIENDS_PROMO
	RED_CARPET_RATE = env.RED_CARPET_RATE_PROMO


class HotelRate:

	def __init__(self, name, rate, check_in, nights, search_url):
		self.name = name
		self.rate = rate
		self.check_in = check_in
		self.nights = nights
		self.search_url = search_url

	def __repr__(self):
		return f"${self.rate*self.nights} ({self.check_in} - {datetime.strftime(datetime.strptime(self.check_in, '%m/%d/%Y') + timedelta(days=nights), '%m/%d/%Y')} @ ${self.rate}/night): {self.name}"


# configs
promo = Promos.RED_CARPET_RATE
nights = 2
check_in_range = ['2022-01-06', '2022-01-06']

# query rates for all hotels in this date range
deals = []
base_url = 'https://reservations.universalorlando.com/ibe/default.aspx?hgID=641'
earliest = datetime.fromisoformat(check_in_range[0])
latest = datetime.fromisoformat(check_in_range[1])
current_dt = earliest
while current_dt <= latest:
	current_dt_fmt = current_dt.strftime('%m/%d/%Y')
	print(f"Getting rates for {current_dt_fmt}")

	full_url = f"{base_url}&checkin={current_dt_fmt}&nights={nights}&promo={promo}"
	resp = requests.get(full_url)

	soup = BeautifulSoup(resp.text, 'html.parser')
	names = [r.text for r in soup.find_all('a', {'class': 'wsName'})]
	rates = [r.text for r in soup.find_all('span', {'class': 'ws-number'})]
	rates = [int(r[1:]) for r in rates]
	hotels = sorted(zip(names, rates), key=lambda x: x[1])
	for h in hotels:
		deal = HotelRate(*h, current_dt_fmt, nights, full_url)
		deals.append(deal)

	current_dt += timedelta(days=1)

# organize into meaningful results
deals.sort(key=lambda hr: hr.rate)
by_hotel = {}
by_date = {}
for d in deals:
	if d.name not in by_hotel.keys():
		by_hotel[d.name] = d
	if d.check_in not in by_date.keys():
		by_date[d.check_in] = d

print('---')
print('Cheapest stay for each hotel:')
[print(v) for v in by_hotel.values()]
print('---')
print('Cheapest stay for each check-in date:')
[print(v) for v in sorted(by_date.values(), key=lambda hr: hr.check_in)]
print('---')
print('Visit the UO reservations website to start booking:')
print(f"{base_url}&promo={promo}")
