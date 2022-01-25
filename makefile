create_migrations:
	cd src && \
	alembic revision --autogenerate

migrate:
	cd src && \
	alembic upgrade head
