
from werkzeug.exceptions import BadRequest
from datetime import datetime


def get_sort_type_by_fields(fields):
    sort_types = []
    for field in fields:
        sort_types.append('{}_asc'.format(field))
        sort_types.append('{}_desc'.format(field))
    return sort_types


def get_sort_from_args(args, fields):
    # Sorting result
    if 'sort' in args and args['sort']:
        sort_by = args['sort'].lower()
        sorted_fields = get_sort_type_by_fields(fields)
        if sort_by not in sorted_fields:
            raise BadRequest(message='Sort is not valid')
        index = sort_by.rindex('_')
        sort = [sort_by[:index], sort_by[index + 1:]]
    else:
        sort = ['id', 'desc']
    return sort


def get_page_from_args(args):
    if 'page' in args and args['page']:
        try:
            page = int(args['page'])
        except ValueError:
            raise BadRequest(message='Page is not valid')
    else:
        page = 1
    return page


def get_size_from_args(args):
    if 'per_page' in args and args['per_page']:
        try:
            size = int(args['per_page'])
        except ValueError:
            raise BadRequest(message='per_page is not valid')
    else:
        size = 10
    return size


def get_fields_from_args(args):
    if 'filter' in args and args['filter']:
        fields = args['filter'].split()
    else:
        fields = None
    return fields


def filter_by_fields(item, fields):
    return {k: v for k, v in item.items() if k in fields}


def datetime_from_timestamp(timestamp, tz=None):
    return datetime.fromtimestamp(timestamp / 1000, tz)


def timestamp_from_datetime(_datetime):
    return int(datetime.timestamp(_datetime) * 1000)
