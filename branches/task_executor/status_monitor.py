def get_all_jobs():
    from .job_queue import _jobs
    return _jobs[-10:]
