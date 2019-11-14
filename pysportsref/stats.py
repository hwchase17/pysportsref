def _calc_delta(df):
    df = df.dropna(subset=['weight_avg', 'diff'])
    return (df['diff'] * df['weight_avg']).sum() / df['weight_avg'].sum()


# TODO: add test
def calculate_aging_curve(df, stat_col, weight_col, age_col='age'):
    """Calculate an aging curve with the delta method."""
    prev_weight_col = '{}___1'.format(weight_col)
    prev_stat_col = '{}___1'.format(stat_col)
    df = df.copy()[[stat_col, weight_col, age_col, prev_stat_col, prev_weight_col]]
    df['diff'] = df[stat_col] - df[prev_stat_col]
    df['weight_avg'] = 2 / (1 / df[weight_col] + 1 / df[prev_weight_col])
    age_delta = df.groupby(age_col).apply(_calc_delta)
    return age_delta.fillna(0).cumsum()
