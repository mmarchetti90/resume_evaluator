### ENV SETUP ------------------------------ ###

setup: requirements.txt
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

clean: .venv
	rm -r .venv

### TOOl RUN ------------------------------- ###

search_and_eval: setup
	.venv/bin/python3 -m src

eval: setup
	.venv/bin/python3 -m src --job_uri $(JOB)
