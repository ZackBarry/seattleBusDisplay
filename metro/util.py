def _filter_table(table, col, fn):
    new_table = []

    for row in table:
        if fn(row[col]):
            new_table.append(row)
    
    return new_table


def filter_table(table, col, value, comparison='equals'):
    if comparison not in ['equals', 'not_equals', 'is_one_of']:
        raise ValueError(f'Filter comparison not supported: {comparison}')
    
    if comparison == 'is_one_of' and type(value) != list:
        raise ValueError(f'Filter value must be type list if comparison is `is_one_of`')

    if comparison == 'equals':
        return _filter_table(table, col, lambda x: x == value)
    elif comparison == 'not_equals':
        return _filter_table(table, col, lambda x: x != value)
    elif comparison == 'is_one_of':
        return _filter_table(table, col, lambda x: x in value)