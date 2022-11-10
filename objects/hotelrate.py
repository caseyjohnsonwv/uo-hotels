class HotelRate:
	def __init__(self, name, rate, check_in, check_out, nights, search_url, promo):
		self.name = name
		self.rate = rate
		self.check_in = check_in
		self.check_out = check_out
		self.nights = nights
		self.search_url = search_url
		self.promo = promo
		self.total = rate*nights

	def __repr__(self):
		return f"${self.total} ({self.check_in} - {self.check_out} @ ${self.rate}/night): {self.name}"

	def as_csv_row(self):
		return [self.total, self.rate, self.check_in, self.check_out, self.nights, self.name, self.promo, self.search_url]

	def csv_header_row():
		return ['Total', 'Rate', 'Check In', 'Check Out', 'Nights', 'Property', 'Promo', 'URL']