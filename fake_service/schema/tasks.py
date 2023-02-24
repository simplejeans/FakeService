from celery import shared_task
from django.core.cache import cache

from schema.services import FakeDataWrite


@shared_task()
def download_dataset_task(cache_task_key: str, schema_id: str, count: str, user_id: str):
    try:
        cache.set(cache_task_key, {"is_importing": False, "errors": []}, timeout=300)
        FakeDataWrite().write_data_to_db_and_remove_from_disk(schema_id=schema_id, count=count, user_id=user_id)
    except Exception as exc:
        cache.set(
            cache_task_key, {"is_importing": False, "errors": [exc.args]}, timeout=120
        )
    else:
        cache.set(cache_task_key, {"is_importing": True, "errors": []}, timeout=120)
