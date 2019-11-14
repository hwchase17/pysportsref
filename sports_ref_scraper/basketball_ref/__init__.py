from ..scraping import get_stats_for_years, get_year_stats
from .table_names import ADVANCED_STATS_TABLE_NAME
from .url_formats import ADVANCED_STATS_URL_FORMATTER


def get_advanced_stats_for_year(year):
    """Fetch advanced NBA stats for given year."""
    return get_year_stats(ADVANCED_STATS_URL_FORMATTER, year, ADVANCED_STATS_TABLE_NAME)


def get_advanced_stats(start_year, end_year):
    """Fetch advanced NBA stats for given year range."""
    return get_stats_for_years(
        ADVANCED_STATS_URL_FORMATTER, start_year, end_year, ADVANCED_STATS_TABLE_NAME
    )
