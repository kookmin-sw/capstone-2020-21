import six

from filters.schema import base_query_params_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ,    
)

user_query_schema = base_query_params_schema.extend(
    {
        "gender": IntegerLike,
        "min_age": IntegerLike,
        "max_age": IntegerLike,
    }
)