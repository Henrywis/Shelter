from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7fca5826a079"
down_revision = "310a6eb3f12b"
branch_labels = None
depends_on = None

def upgrade():
    # Recreate table so SQLite can handle the type change
    with op.batch_alter_table("intake_requests", recreate="always") as batch_op:
        # add reason
        batch_op.add_column(sa.Column("reason", sa.String(), nullable=True))
        # change eta: String -> DateTime
        batch_op.alter_column(
            "eta",
            existing_type=sa.String(),     # what it used to be
            type_=sa.DateTime(),           # what we want
            existing_nullable=True
        )

def downgrade():
    with op.batch_alter_table("intake_requests", recreate="always") as batch_op:
        # revert eta: DateTime -> String
        batch_op.alter_column(
            "eta",
            existing_type=sa.DateTime(),
            type_=sa.String(),
            existing_nullable=True
        )
        # drop reason
        batch_op.drop_column("reason")
