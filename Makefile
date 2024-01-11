run-docker:
	sudo docker compose up

# Here we cd to set the root
run-uvicorn:
	cd candidate_profiles && uvicorn main.main:app --reload

test:
	pytest

test-verbose:
	pytest -s
