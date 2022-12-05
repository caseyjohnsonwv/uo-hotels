from datetime import datetime, timedelta
from typing import List
from bs4 import BeautifulSoup
import requests
from objects.hotelrate import HotelRate


BASE_URL = 'https://reservations.universalorlando.com/ibe/default.aspx?hgID=641'


class UO:
    def get_deals(check_in:str, nights:int, promo:str) -> List[HotelRate]:
        deals = []
        check_out = datetime.strftime(datetime.strptime(check_in, '%m/%d/%Y') + timedelta(days=nights), '%m/%d/%Y')

        full_url = f"{BASE_URL}&checkin={check_in}&nights={nights}&promo={promo}"
        resp = requests.get(full_url)
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        names = [r.text for r in soup.find_all('a', {'class': 'wsName'})]
        rates = [r.text for r in soup.find_all('span', {'class': 'ws-number'})]
        rates = [int(r.encode().decode('ascii')[1:]) for r in rates]

        assert len(names) == len(rates)
        for i,rate in enumerate(rates):
            deal = HotelRate(names[i], rate, check_in, check_out, nights, full_url, promo)
            deals.append(deal)
        
        return deals