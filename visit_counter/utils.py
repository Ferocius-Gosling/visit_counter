from datetime import datetime
from visit_counter.const import keys_meta


def get_date():
    now = datetime.now()
    return now.strftime("%H:%d.%W.%m.%Y")


def get_meta_dict(**meta_kwargs):
    meta = dict()
    meta['id'] = meta_kwargs['user_id']
    meta['date'] = meta_kwargs['date']
    meta['path'] = meta_kwargs['path']
    meta['domain'] = meta_kwargs['domain']
    meta['user_agent'] = meta_kwargs['user_agent']
    return meta


def check_in_keys_meta(name):
    for key in keys_meta:
        if key == name:
            return True
    return False
