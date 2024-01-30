from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

class CustomQueryOperator(BaseOperator):
    @apply_defaults
    def __init__(self, sql, database_conn_id, *args, **kwargs):
        super(CustomQueryOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.database_conn_id = database_conn_id

    def execute(self, context):
        hook = BaseHook.get_hook(self.database_conn_id)
        records = hook.get_records(self.sql)
        for record in records:
            self.log.info(record)
