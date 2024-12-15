from rest_framework.pagination import LimitOffsetPagination, _positive_int


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom pagination class extending LimitOffsetPagination.

    Overrides the `paginate_queryset` method to return the full queryset
    when the limit query parameter is set to 0. This behavior differs from
    the default LimitOffsetPagination which returns an empty list for limit=0.

    Methods:
        paginate_queryset(queryset, request, view=None): Paginates the given queryset
            based on the request parameters, returning the full queryset if limit=0.
    """

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request, self.count)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])

    def get_limit(self, request, count):
        if self.limit_query_param:
            try:
                if int(request.query_params[self.limit_query_param]) == 0:
                    return count
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit,
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit
