import csv, argparse
from tabulate import tabulate


def parse_cli_args(args=None):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', help='Source file path. Required')
    argparser.add_argument('--where', help='Filter condition as field_name{=,<,>}value')
    argparser.add_argument('--aggregate', help='Aggregate function as field_name={avg,min,max}. Only numeric fields.')
    return argparser.parse_args(args)


def map_data(row):
    return {
        'name': row[0],
        'brand': row[1],
        'price': float(row[2]),
        'rating': float(row[3])
    }


def isfloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def filter_data(data, condition):
    greater = condition.split('>')
    less = condition.split('<')
    equal = condition.split('=')

    def do_filter_greater(data, field, match):
        match = float(match) if isfloat(match) else match
        return list(filter(lambda row: row[field] > match, data))

    def do_filter_less(data, field, match):
        match = float(match) if isfloat(match) else match
        return list(filter(lambda row: row[field] < match, data))

    def do_filter_equal(data, field, match):
        match = float(match) if isfloat(match) else match
        return list(filter(lambda row: row[field] == match, data))

    if len(greater) > 1:
        return do_filter_greater(data, greater[0], greater[1])

    if len(less) > 1:
        return do_filter_less(data, less[0], less[1])

    if len(equal) > 1:
        return do_filter_equal(data, equal[0], equal[1])


def aggregate_data(data, condition):
    function = condition.split('=')[1]
    field = condition.split('=')[0]

    if not isfloat(data[0][field]):
        raise ValueError('Only numeric fields allowed')

    def avg():
        avg = 0
        for row in data:
            avg += float(row[field])
        avg = avg / len(data)
        return [{'avg': avg}]

    def min():
        min = data[0][field]
        for row in data:
            min = row[field] if row[field] < min else min
        return [{'min': min}]

    def max():
        max = data[0][field]
        for row in data:
            max = row[field] if row[field] > max else max
        return [{'max': max}]

    return locals()[function]()


def read_data(filename):
    data = []
    with open(filename) as products:
        reader = csv.reader(products)
        next(reader)
        for row in reader:
            data.append(map_data(row))
    return data


def main(args=None):
    args = parse_cli_args(args)
    data = read_data(args.file)
    if args.where:
        data = filter_data(data, args.where)

    if args.aggregate:
        data = aggregate_data(data, args.aggregate)

    print(tabulate(data, headers='keys', tablefmt='grid'))

if __name__ == '__main__':
    main()
