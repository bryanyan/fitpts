from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
active = Table('active', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_id', Integer),
    Column('active_name', String(length=140)),
    Column('points', Integer),
)

group = Table('group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('group_name', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['active'].create()
    post_meta.tables['group'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['active'].drop()
    post_meta.tables['group'].drop()
