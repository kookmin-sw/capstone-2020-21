# This file saves constant list for choice fields options.
# 알파벳 순으로 정렬.
import json

GENDER_CHOICES = [
    (True, 'man'),
    (False, 'woman'),
]

with open('apps/api/locations/data.json') as json_file:
    data = json.load(json_file)
    
LOCATION_CHOICES = []
for row in data:
    LOCATION_CHOICES.append((int(row), data[row]['full_address']))

LOWER_CATEGORY_CHOICES = [
    ('short_sleeve', 'short_sleeve'),
    ('long_sleeve', 'long_sleeve'),
    ('short_sleeve_shirt', 'short_sleeve_shirt'),
    ('long_sleeve_shirt', 'long_sleeve_shirt'),
    ('sweatshirt', 'sweatshirt'),
    ('turtleneck', 'turtleneck'),
    ('hoodie', 'hoodie'),
    ('sweater', 'sweater'),
    ('blouse', 'blouse'),
    ('spaghetti_strap', 'spaghetti_strap'),
    ('sleeveless', 'sleeveless'),
    ('shorts', 'shorts'),
    ('hot_pants', 'hot_pants'),
    ('slacks', 'slacks'),
    ('jeans', 'jeans'),
    ('golden_pants', 'golden_pants'),
    ('sweatpants', 'sweatpants'),
    ('skirt', 'skirt'),
    ('long_skirt', 'long_skirt'),
    ('blazer', 'blazer'),
    ('short_padding', 'short_padding'),
    ('vest_padding', 'vest_padding'),
    ('long_padding', 'long_padding'),
    ('stadium_jacket', 'stadium_jacket'),
    ('coach_jacket', 'coach_jacket'),
    ('windbreaker', 'windbreaker'),
    ('field_jacket', 'field_jacket'),
    ('mustang', 'mustang'),
    ('coat', 'coat'),
    ('track_top', 'track_top'),
    ('leather_jacket', 'leather_jacket'),
    ('blue_jacket', 'blue_jacket'),
    ('cardigan', 'cardigan'),
    ('dress', 'dress')
]

REVIEW_CHOICES = [
    (1, 'cold'),
    (2, 'little_cold'),
    (3, 'nice'),
    (4, 'little_hot'),
    (5, 'hot'),
]
    
UPPER_CATEGORY_CHOICES = [
    ('bottom', 'bottom'),
    ('dress', 'dress'),
    ('outer', 'outer'),
    ('skirt', 'skirt'),
    ('top', 'top'),
]

STYLE_CHOICES = [
    ('simple', 'simple'),
    ('street', 'street'),
    ('suit', 'suit'),
    ('date', 'date'),
    ('splendor', 'splendor'),
]
