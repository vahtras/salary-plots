
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
        elif ' in ' in kv:
            k, v = kv.split(' in ')
            values = v.split()
            df = df[df[k].isin(values)]
    return df
