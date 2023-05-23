<%!
import re

%>"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


<%
    from flask import current_app
    bind_names = []
    if current_app.config.get('SQLALCHEMY_BINDS') is not None:
        bind_names = list(current_app.config['SQLALCHEMY_BINDS'].keys())

        ##  generating migration script for a single db bind
        migrating_db = current_app.config.get("migrating_db)

        if migrating_db:
            bind_names = [migrating_db]
            db_names = bind_names


    else:
        get_bind_names = getattr(current_app.extensions['migrate'].db, 'bind_names', None)
        if get_bind_names:
            bind_names = get_bind_names()
    db_names = [''] + bind_names
%>

## generate an "upgrade_<xyz>() / downgrade_<xyz>()" function
## for each database name in the ini file.

% for db_name in db_names:

def upgrade():
    ${context.get("%s_upgrades" % db_name, "pass")}


def downgrade():
    ${context.get("%s_downgrades" % db_name, "pass")}

% endfor
