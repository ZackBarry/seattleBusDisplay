import csv


def get_csv_field_names(file_name):
    header = open(file_name).read().splitlines()[0]
    return header.split(',')


def col_is_digit(table, col):
    for row in table:
        if not row[col].isdigit():
            return False
    return True


def load_csv(file_name):
    cols = get_csv_field_names(file_name)
    rows = []

    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=cols)
        for row in reader:
            rows.append(row)
    
    # first row contains col names
    del rows[0]
    
    for col in cols:
        if col_is_digit(rows, col):
            for row in rows:
                row[col] = int(row[col])
    
    return rows
