import uuid


def generate_cache_task_key():
    return str(uuid.uuid1())
