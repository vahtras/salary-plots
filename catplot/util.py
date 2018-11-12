import re

def process_filters(df, filters):
    for kv in filters:
        if '!=' in kv:
            k, v = kv.split('!=')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] != v]
        elif '=' in kv:
            k, v = kv.split('=')
            try:
                v = int(v)
            except ValueError:
                pass
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
            values = v.split(',')
            values = [re.sub('_', ' ', v) for v in values]
            df = df[df[k].isin(values)]
    return df
