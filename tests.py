from main import *

def test_filter_data_brand(cmdopt):
    data = read_data(cmdopt)
    filtered_data = filter_data(data, 'brand=Apple')
    assert len(filtered_data) > 0 and len(filtered_data) < len(data)
    filtered_data = filter_data(data, 'brand=apple')
    assert len(filtered_data) > 0 and len(filtered_data) < len(data)

def test_filter_data_rating(cmdopt):
    data = read_data(cmdopt)
    filtered_data = filter_data(data, 'rating>4.2')
    assert len(filtered_data) > 0 and len(filtered_data) < len(data)

def test_aggregate_data_rating(cmdopt):
    data = read_data(cmdopt)
    assert aggregate_data(data, 'rating=avg')

def test_aggregate_data_brand(cmdopt):
    data = read_data(cmdopt)
    assert aggregate_data(data, 'brand=avg')