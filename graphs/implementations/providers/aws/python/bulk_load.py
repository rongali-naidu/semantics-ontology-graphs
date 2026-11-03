#!/usr/bin/env python3
"""Start a Neptune bulk-load job with boto3 and wait for it to finish.

    python bulk_load.py s3://my-bucket/retail/gremlin-csv/ csv
    python bulk_load.py s3://my-bucket/retail/opencypher-csv/ opencypher
    python bulk_load.py s3://my-bucket/retail/rdf/retail-data.nq nquads
    python bulk_load.py s3://my-bucket/retail/rdf/retail-data.ttl turtle

Env: LOADER_ROLE_ARN (IAM role attached to the cluster that can read the bucket)
"""
import os
import sys
import time

from common import REGION, neptunedata_client


def main(source: str, fmt: str) -> None:
    client = neptunedata_client()
    job = client.start_loader_job(
        source=source,
        format=fmt,                       # csv | opencypher | ntriples | nquads | rdfxml | turtle
        s3BucketRegion=REGION,
        iamRoleArn=os.environ["LOADER_ROLE_ARN"],
        failOnError=False,
        parallelism="MEDIUM",
        queueRequest=True,
    )
    load_id = job["payload"]["loadId"]
    print("loadId:", load_id)
    while True:
        status = client.get_loader_job_status(loadId=load_id, details=True, errors=True)
        overall = status["payload"]["overallStatus"]
        print(overall["status"], "records:", overall.get("totalRecords"))
        if overall["status"] not in ("LOAD_NOT_STARTED", "LOAD_IN_PROGRESS", "LOAD_IN_QUEUE"):
            print(status["payload"].get("errors", {}))
            break
        time.sleep(5)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
