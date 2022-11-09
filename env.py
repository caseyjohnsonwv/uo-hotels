from dotenv import load_dotenv
load_dotenv('.env')

from os import getenv
FAMILY_AND_FRIENDS_PROMO = getenv('FAMILY_AND_FRIENDS_PROMO')
RED_CARPET_RATE_PROMO = getenv('RED_CARPET_RATE_PROMO')