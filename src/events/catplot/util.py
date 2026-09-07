import re


def process_filters(df, filters):
    try:
        for kv in filters:
            if '!=' in kv:
                k, v = kv.split('!=')
                if df[k].dtype == int:
                    try:
                        v = int(v)
                    except ValueError:
                        raise
                else:
                    v = re.sub('_', ' ', v)
                df = df[df[k] != v]
            elif '<=' in kv:
                k, v = kv.split('<=')
                if df[k].dtype == int:
                    try:
                        v = int(v)
                    except ValueError:
                        raise
                df = df[df[k] <= v]
            elif '=' in kv:
                k, v = kv.split('=')
                if df[k].dtype == int:
                    try:
                        v = int(v)
                    except ValueError:
                        raise
                else:
                    v = re.sub('_', ' ', v)
                df = df[df[k] == v]
            elif '>' in kv:
                k, v = kv.split('>')
                try:
                    v = int(v)
                except ValueError:
                    pass
                df = df[df[k] > v]
            elif '<' in kv:
                k, v = kv.split('<')
                try:
                    v = int(v)
                except ValueError:
                    pass
                df = df[df[k] < v]
            elif '@' in kv:
                k, v = kv.split('@')
                values = v.split(':')
                values = [re.sub('_', ' ', v) for v in values]
                df = df[df[k].isin(values)]
            elif '.match.' in kv:
                k, v = kv.split('.match.')
                v = re.sub('_', ' ', v)
                df = df[df[k].notna() & df[k].str.match(fr'.*{v}.*')]
    except KeyError:
        print('Available columns:', df.columns)
        exit(1)

    return df


REGEX = r'([/\s\w.()]+)[=>@]([-\s\w():,]+)'


def filter_values(s: str) -> str:
    """
    Returns right-hand-side for defined filters

    >>> filter_values('Arbomr=19')
    '19'
    """

    s = re.sub('_', ' ', s)
    m = re.match(REGEX, s)
    if m:
        return m.groups(0)[1]
    return ""


def filter_keys(s: str) -> str:
    """
    Returns left-hand-side for defined filters

    >>> filter_keys('Arbomr=19')
    'Arbomr'
    """

    m = re.match(REGEX, s)
    if m:
        return m.groups(0)[0]
    return ""


def filter_dict(filters: list) -> dict:
    """
    Returns left-hand-side for defined filters

    >>> filter_dict('Arbomr=19')
    'Arbomr'
    """

    keys = [filter_keys(s) for s in filters]
    values = []
    for s in filters:
        value = filter_values(s)
        if ":" in value:
            values.append(value.split(':'))
        else:
            values.append(value)

    return {k: v for k, v in zip(keys, values)}
