from functools import partial


def _get_id(df, player_col, year_col):
    """Aggregate player column and year column."""
    return df[player_col] + '___' + df[year_col].astype(str)


def filter_df(df, team_col='team_id', player_col='player_url', year_col='year'):
    """If a player is present multiple times for the same year, get their TOT stats."""
    missing_cols = {team_col, player_col, year_col}.difference(df.columns)
    if missing_cols:
        raise ValueError('Missing columns: {}'.format(missing_cols))
    _partialed_get_id = partial(_get_id, player_col=player_col, year_col=year_col)
    vals = set(_partialed_get_id(df[df[team_col] == 'TOT']))
    return df[~(_partialed_get_id(df).isin(vals) & (df[team_col] != 'TOT'))].reset_index(drop=True)


def merge_with_prev_year(df, year_delta, year_col='year', player_col='player_url'):
    """Merge player stats from previous year."""
    if year_delta < 1:
        raise ValueError('year_delta must be >= 1, got {}!'.format(year_delta))
    prev_year_df = df.copy()
    prev_year_df[year_col] += year_delta
    merged_df = df.merge(
        prev_year_df,
        how='left',
        on=[player_col, year_col],
        suffixes=('', '___{}'.format(year_delta))
    )
    return merged_df
