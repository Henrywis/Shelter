from alembic import op

# revision identifiers, used by Alembic.
revision = "8285fbf7b7f4"
down_revision = "ddb326bf0f71"  # last one from Marker 7
branch_labels = None
depends_on = None

def upgrade() -> None:
    # These work on SQLite & Postgres
    op.create_index("ix_intake_requests_created_at", "intake_requests", ["created_at"])
    op.create_index("ix_intake_requests_status", "intake_requests", ["status"])

def downgrade() -> None:
    op.drop_index("ix_intake_requests_status", table_name="intake_requests")
    op.drop_index("ix_intake_requests_created_at", table_name="intake_requests")
