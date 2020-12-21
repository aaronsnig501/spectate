def filters(queryset, request):
    """Filtering function

    Check for the existance of the `sport` and `name` query strings and filter
    the queryset accordingly. This filter will look for exact matches.

    Args:
        queryset (Queryset): The dataset to be filtered
        request (Request): The request object provided by the client

    Returns:
        Queryset: The filtered data
    """
    # Get query strings
    sport = request.GET.get("sport", None)
    name = request.GET.get("name", None)

    # Query string filters
    if sport is not None:
        queryset = queryset.filter(sport__name__iexact=sport)
    if name is not None:
        queryset = queryset.filter(name__iexact=name)

    return queryset