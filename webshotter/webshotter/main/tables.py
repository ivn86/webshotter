import sqlalchemy as sa

from webshotter.migrations import metadata


screenshots_tbl = sa.Table(
    'screenshots', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('token', sa.String(200), nullable=False),
    sa.Column('url', sa.String(1024), nullable=False),
    sa.Column('picture_name', sa.String(200), nullable=True),


    # Indexes #
    sa.PrimaryKeyConstraint('id', name='screenshots_id_pkey'),
)