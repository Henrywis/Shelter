from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7e9d02b961e8"
down_revision = "7fca5826a079"
branch_labels = None
depends_on = None

def upgrade():
    # Ensure any existing NULLs are set to 'pending' before making NOT NULL
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE intake_requests SET status = 'pending' WHERE status IS NULL"))

    # Recreate table so SQLite can apply NOT NULL and add a CHECK constraint
    with op.batch_alter_table("intake_requests", recreate="always") as batch_op:
        # enforce NOT NULL
        batch_op.alter_column(
            "status",
            existing_type=sa.String(),
            nullable=False,
            existing_nullable=True,
        )
        # optional: add a check constraint for allowed values
        batch_op.create_check_constraint(
            "ck_intake_status",
            "status in ('pending','fulfilled','cancelled')"
        )

def downgrade():
    # Remove constraint and relax NOT NULL by recreating table
    with op.batch_alter_table("intake_requests", recreate="always") as batch_op:
        # drop the check constraint (SQLite needs name match)
        batch_op.drop_constraint("ck_intake_status", type_="check")
        # allow NULL again
        batch_op.alter_column(
            "status",
            existing_type=sa.String(),
            nullable=True,
            existing_nullable=False,
        )
