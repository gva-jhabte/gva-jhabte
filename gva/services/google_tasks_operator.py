from gva.data.flows import BaseOperator
from .create_http_task import create_http_task


class GoogleTaskOperator(BaseOperator):

    def __init__(self, credentials_file='creds.json'):
        super().__init__()
        from google.oauth2 import service_account
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    def execute(self, data={}, context={}):
        my_context = context.copy()
        my_context.pop('execution_trace') # remove this item from the context
        job_name = context.get('job_name', '').lower()
        create_http_task(
            project='vulnerability-analytics',
            queue='reply',
            url=F'https://dispatcher.flows.gva.services/{job_name}',
            payload=my_context,
            credentials=self.credentials)
        return data, my_context