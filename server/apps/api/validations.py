import six

from filters.schema import base_query_params_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ,    
)

user_query_schema = base_query_params_schema.extend(
    {
        "gender": IntegerLike(),
        "min_age": IntegerLike(),
        "max_age": IntegerLike(),
    }
)

clothes_query_schema = base_query_params_schema.extend(
    {
        "upper_category": six.text_type,
        "lower_category": six.text_type,
    }
)

clothes_set_query_schema = base_query_params_schema.extend(
    {
        "style": six.text_type,
    }
)

clothes_set_review_query_schema = base_query_params_schema.extend(
    {
        'start_datetime': DatetimeWithTZ(),
        'end_datetime': DatetimeWithTZ(),
        'location' : six.text_type,
    }
)
