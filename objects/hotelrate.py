class HotelRate:
	def __init__(self, name, rate, check_in, check_out, nights, search_url, promo):
		self.name = name
		self.rate = rate
		self.check_in = check_in
		self.check_out = check_out
		self.nights = nights
		self.search_url = search_url
		self.promo = promo

	def __repr__(self):
		return f"${self.rate*self.nights} ({self.check_in} - {self.check_out} @ ${self.rate}/night): {self.name}"

	def as_csv_row(self):
		return [self.rate, self.check_in, self.check_out, self.nights, self.name, self.search_url, self.promo]