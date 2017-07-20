from app.celery_tasks.celery_init import celery


@celery.task(bind=True, name="celery_tasks.git_info")
def get_user_git(self, username, fork=False):
    pass
