from ckan.lib.cli import CkanCommand
import audit_db
import sys
import logging
log = logging.getLogger('ckanext')
log.setLevel(logging.DEBUG)


class AuditCmd(CkanCommand):
    """Init required vocabs
        Usage:
        audit-cmd initdb
        - creates necessery db tables
        audit-cmd uninstall
        - drop db tables
    """
    
    summary = __doc__.split('\n')[0]
    usage = __doc__
    #max_args = 3
    #min_args = 0
    
    def __init__(self, name):
        super(AuditCmd, self).__init__(name)
    def command(self):
        self._load_config()
              
        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'initdb':
            log.info('Starting db initialization')
            if not audit_db.revision_audit_table.exists():
                log.info("creating revision_audit table")
                audit_db.revision_audit_table.create()
                log.info("revision_audit table created successfully")
            else:
                log.info("revision_audit table already exists")
        if cmd == 'uninstall':
            log.info('Starting uninstall process')
            if audit_db.revision_audit_table.exists():
                log.info("droping revision_audit table")
                audit_db.revision_audit_table.drop()
                log.info("revision_audit table droped successfully")
            else:
                log.info("revision_audit table doesnt exists")
        if cmd == 'audit_log':
            import tasks
            log.info('count of args: %d', len(self.args))
            if len(self.args) == 8:
                tasks.audit_log(self.args[1], self.args[2], self.args[3], self.args[4], self.args[5], self.args[6], self.args[7])