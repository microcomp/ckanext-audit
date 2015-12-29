import uuid

import ckan.plugins as plugins
from audit_db import RevisionAudit
from ckan.lib.celery_app import celery
from pylons import config, session
import ckan.model as model

import logging
log = logging.getLogger(__name__)

def send_message_auditlog(context, data_dict):
    jar_path = config.get('ckan.auditlog_enabled', True)
    log.info('audit log send')
    event_name = data_dict.get('event_name', '')
    authorized_user = data_dict.get('authorized_user', '')
    subject = data_dict.get('subject','')
    description = data_dict.get('description', '')
    object_reference = data_dict.get('object_reference', '')
    debug_level = data_dict.get('debug_level', 0)
    error_code = data_dict.get('error_code', 0)
    log.info('creating celery task')
    jar_path = config.get('ckan.auditlog_client_path', None)
    actor_obj = model.User.get(authorized_user)
    if actor_obj and actor_obj.fullname:
        authorized_user += '/' + actor_obj.fullname
    subject_obj = model.User.get(subject)
    if subject_obj and subject_obj.fullname:
        subject += '/' + subject_obj.fullname
    celery.send_task("audit.log", args=[event_name, authorized_user, subject, description, object_reference, debug_level, error_code, jar_path], countdown=10, task_id=str(uuid.uuid4()))

def retrieve_revision_executor(context, data_dict):
    search = {'id' : data_dict['id']}
    revision = RevisionAudit.get(**search)
    log.info('revision result: %s', revision)
    if revision:
        return revision[0].actor_id
    return None
    

def insert_revision_executor_id(context, data_dict):
    revision_id = data_dict.get('revision_id', None)
    user_id = data_dict.get('user_id', None)
    log.info('user_id: %s', user_id)
    log.info('revision_id: %s', revision_id)
    if user_id and revision_id:
        search = {'revision_id' : revision_id}
        revisions = RevisionAudit.get(**search)
        if revisions:
            revisions[0].actor_id = user_id
            revisions[0].save()
            return
        revision = RevisionAudit(revision_id, user_id)
        revision.save()

class AuditPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions, inherit=False)
    plugins.implements(plugins.IMapper, inherit=True)
    
    def get_actions(self):
        return {'audit_revision' : insert_revision_executor_id,
                'revision_executor' : retrieve_revision_executor,
                'auditlog_send' : send_message_auditlog}
    
    def after_update(self, mapper, connection, instance):
        log.info("Updated: %r", instance)

    def after_insert(self, mapper, connection, instance):
        log.info("Inserted: %r", instance)