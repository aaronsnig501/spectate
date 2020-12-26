def parse_query_params(request):
    sport = request.GET.get("sport", None)
    name = request.GET.get("name", None)
    ordering = request.GET.get("ordering", None)

    return sport, name, ordering


def filter_by_params(queryset, params):
    """Filtering function

    Check for the existance of the `sport` and `name` query strings and filter
    the queryset accordingly. This filter will look for exact matches.

    Args:
        queryset (Queryset): The dataset to be filtered
        request (Request): The request object provided by the client

    Returns:
        Queryset: The filtered data
    """
    sport = params[0]
    name = params[1]

    # Query string filters
    if sport is not None:
        queryset = queryset.filter(sport__name__iexact=sport)
    if name is not None:
        queryset = queryset.filter(name__iexact=name)

    return queryset