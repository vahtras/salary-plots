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
            elif '=' in kv:
                k, v = kv.split('=')
                if df[k].dtype == int:
                    try:
                        v = int(v)
                    except ValueError:
                        raise
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
                df = df[df[k].str.match(fr'.*{v}.*')]
    except KeyError:
        print('Available columns:', df.columns)
        exit(1)

    return df


def filter_values(s):
    regex = r'[/\s\w.]+[=>]([-\s\w()]+)'
    m = re.match(regex, s)
    if m:
        return m.groups(1)[0]
    return ""
