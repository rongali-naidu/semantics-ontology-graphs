"""Shared settings + SigV4 signing for Amazon Neptune.

Environment variables:
  NEPTUNE_ENDPOINT   cluster endpoint, e.g. my-db.cluster-abc.us-east-1.neptune.amazonaws.com
  NEPTUNE_PORT       default 8182
  AWS_REGION         default us-east-1
  NEPTUNE_IAM_AUTH   "true" if IAM database authentication is enabled
"""
import os

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

ENDPOINT = os.environ["NEPTUNE_ENDPOINT"]
PORT = int(os.environ.get("NEPTUNE_PORT", "8182"))
REGION = os.environ.get("AWS_REGION", "us-east-1")
IAM_AUTH = os.environ.get("NEPTUNE_IAM_AUTH", "false").lower() == "true"
HTTPS_URL = f"https://{ENDPOINT}:{PORT}"


def signed_headers(method: str, url: str, body: str | None = None,
                   headers: dict | None = None) -> dict:
    """Return headers for a request; adds SigV4 auth when IAM auth is on.
    Neptune's signing service name is 'neptune-db'."""
    headers = dict(headers or {})
    if not IAM_AUTH:
        return headers
    creds = boto3.Session().get_credentials().get_frozen_credentials()
    req = AWSRequest(method=method, url=url, data=body, headers=headers)
    SigV4Auth(creds, "neptune-db", REGION).add_auth(req)
    return dict(req.headers)


def neptunedata_client():
    """boto3 'neptunedata' client: signs requests itself, IAM or not."""
    return boto3.client("neptunedata", endpoint_url=HTTPS_URL, region_name=REGION)
