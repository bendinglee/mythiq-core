_jobs = []

def launch_task(payload):
    import time
    job_id = f"job-{int(time.time())}"
    _jobs.append({ "id": job_id, "status": "queued", "task": payload })
    return job_id

def get_job_status(job_id):
    for job in _jobs:
        if job["id"] == job_id:
            return job
    return { "error": "Job not found" }
