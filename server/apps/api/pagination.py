from rest_framework.pagination import LimitOffsetPagination

# Pagination with small max limit.
class SmallLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


# Pagination with medium max limit.
class MediumLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


# Pagination with large max limit.
class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 10000
    
