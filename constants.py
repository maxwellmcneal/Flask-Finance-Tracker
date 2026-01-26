import os
import zoneinfo as zi

DEFAULT_TIMEZONE = zi.ZoneInfo('US/Pacific')

EXPENSE_CATEGORIES = [('', 'Select category'), ('Alcohol', 'Alcohol'), ('Automotive', 'Automotive'),
                      ('Clothes', 'Clothes'), ('Bills/Utilities', 'Bills/Utilities'),
                      ('Entertainment', 'Entertainment'), ('Food/Drink', 'Food/Drink'),
                      ('Gas', 'Gas'), ('Groceries', 'Groceries'), ('Health/Wellness', 'Health/Wellness'),
                      ('Home', 'Home'), ('Laundry', 'Laundry'), ('Miscellaneous', 'Miscellaneous'),
                      ('Rent', 'Rent'), ('Ride Sharing', 'Ride Sharing'), ('Travel', 'Travel')]

_payment_methods = os.environ.get(
    'PAYMENT_METHODS',
    'Credit Card, Debit Card, Cash, Check'
).split(',')
PAYMENT_METHOD_CHOICES = [('', 'Select payment method')] + [(m.strip(), m.strip()) for m in _payment_methods]