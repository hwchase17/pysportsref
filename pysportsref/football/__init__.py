from ..scraping import get_stats_for_year, get_stats_for_years
from .table_names import PASSING_TABLE_NAME, RUSHING_TABLE_NAME
from .url_formats import PASSING_URL_FORMATTER, RUSHING_URL_FORMATTER


def get_stats(stat, start_year, end_year):
    """Fetch NFL stats for given year range and specific stat types."""
    stat_types = {
        'passing': (PASSING_URL_FORMATTER, PASSING_TABLE_NAME),
        'rushing': (RUSHING_URL_FORMATTER, RUSHING_TABLE_NAME),
    }
    if stat not in stat_types:
        raise ValueError(
            'stat type {} is not supported currently. Only supported types are {}'.format(
                stat, stat_types.keys()
            )
        )
    url_formatter, table_name = stat_types[stat]
    return get_stats_for_years(url_formatter, start_year, end_year, table_name)
