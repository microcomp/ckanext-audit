from ckan.model.meta import metadata, Session, mapper
from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from ckan.model import domain_object
import ckan.model as model

revision_audit_table = Table('revision_audit', metadata,
                            #Column('revision_id',  types.UnicodeText, ForeignKey('revision.id'), primary_key=True, nullable=False),
                            Column('revision_id',  types.UnicodeText, primary_key=True, nullable=False),
                            Column('actor_id', types.UnicodeText, nullable=False)
                        )

class RevisionAudit(domain_object.DomainObject):
        
    def __init__(self, revision_id, actor_id):
        assert revision_id
        assert actor_id
        self.revision_id = revision_id
        self.actor_id = actor_id

    @classmethod
    def get(cls, **kw):
        '''Finds a single entity in the register.'''
        query = Session.query(cls).autoflush(False)
        return query.filter_by(**kw).all()
    
    @classmethod
    def delete(cls, **kw):
        query = Session.query(cls).autoflush(False).filter_by(**kw).all()
        for i in query:
            Session.delete(i)
        return

mapper(RevisionAudit, revision_audit_table)        
#mapper(RevisionAudit, revision_audit_table, properties={
# "revision": relationship(model.Revision, single_parent=True, backref=backref('revision_audited', cascade="all, delete, delete-orphan"))})