# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Adapted From:
https://github.com/googleapis/python-tasks/blob/master/samples/snippets/create_http_task.py
"""

# def create_http_task(
#     project, queue, url, location='europe-west2', payload=None, in_seconds=None, task_name=None, credentials=None
# ):
# [START cloud_tasks_create_http_task]
"""Create a task for a given queue with an arbitrary payload."""

from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime
import json
import gva.logging
from google.oauth2 import service_account

logger = gva.logging.get_logger()

CREDENTIALS_FILE = "jon-deploy-project-150f60b0b3c3.json"

# credentials = service_account.Credentials.from_service_account_file(
#     CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"],
# )
# credentials=None
# # Create a client.
# if credentials:
#     client = tasks_v2.CloudTasksClient(credentials=credentials)
# else:
client = tasks_v2.CloudTasksClient()

location='europe-west2'

project = 'jon-deploy-project'
queue = 'my-queue'

# Construct the fully qualified queue name.
parent = client.queue_path(project, location, queue)
url = 'https://pls-nvd-post-3hipbvdnza-nw.a.run.app/ingest'
payload = 'Data is ingesting!'
timeout=1800
in_seconds=10

# Construct the request body.
task = {
    "http_request": {  # Specify the type of request.
        "http_method": tasks_v2.HttpMethod.POST,
        "url": url,  # The full url path that the task will be sent to.
    },
}
if payload is not None:
    if isinstance(payload, dict):
        # Convert dict to JSON string
        payload = json.dumps(payload)
        # specify http content-type to application/json
        task["http_request"]["headers"] = {"Content-type": "application/json"}
    # The API expects a payload of type bytes.
    converted_payload = payload.encode()
    task["http_request"]["body"] = converted_payload
if in_seconds is not None:
    # Convert "seconds from now" into an rfc3339 datetime string.
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
    # Create Timestamp protobuf.
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(d)
    # Add the timestamp to the tasks.
    task["schedule_time"] = timestamp
# if task_name is not None:
#     # Add the name to tasks.
#     task["name"] = task_name
# print (f'the task name is {task_name}')

# Use the client to build and send the task.
response = client.create_task(request={"parent": parent, "task": task})

logger.debug(F"[CREATE_TASK] Success - {queue} - {url} - {response.name}")
# return response
