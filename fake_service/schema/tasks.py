from celery import shared_task
from django.core.cache import cache
from schema.services import FakeDataWrite
from schema.utils import generate_cache_task_key


@shared_task()
def download_dataset_task(cache_task_key: str, schema_id: str, row_nums: str, user_id: str):
    try:
        cache.set(cache_task_key, {"is_importing": False, "errors": []}, timeout=300)
        FakeDataWrite().write_data_to_db_and_remove_from_disk(schema_id=schema_id, row_nums=row_nums, user_id=user_id)
    except Exception as exc:
        cache.set(
            cache_task_key, {"in_process": False, "errors": [exc.args]}, timeout=120
        )
    else:
        cache.set(cache_task_key, {"done": True, "errors": []}, timeout=120)


def start_download_dataset_task(schema_id: str, row_nums: str, user_id: str) -> str:
    cache_task_key = generate_cache_task_key()
    download_dataset_task(
        cache_task_key, schema_id=schema_id, row_nums=row_nums, user_id=user_id
    )
    return cache_task_key
