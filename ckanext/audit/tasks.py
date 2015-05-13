import os
import subprocess
import logging
from ckan.lib.celery_app import celery
from pylons import config

log=logging.getLogger(__name__)

@celery.task(name = "audit.log")
def audit_log(event_name, authorized_user, subject, description, object_reference, debug_level, error_code, jar_path=None):
    log.info('celery task audit log')
    if not jar_path:
        jar_path = config.get('ckan.auditlog_client_path', None)
    log.info('jar path: %s', jar_path)
    log.info('jar path type: %s', type(jar_path))
    try:
        status = subprocess.check_call(["java", "-jar", str(jar_path), str(event_name), str(authorized_user), str(subject), str(description), str(object_reference), str(debug_level), str(error_code)])
        return status
    except subprocess.CalledProcessError as e:
        log.exception(e)
        return -1