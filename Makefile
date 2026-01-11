run:
	uvicorn app.main:app --reload

migrations:
	alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

%:
	@:

head:
	alembic upgrade head