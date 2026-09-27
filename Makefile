.PHONY: install audit run test dashboard clean

install:
	pip install -r requirements.txt

audit:
	python src/dlsm/data/audit_generator.py

run:
	python src/dlsm/pipeline_orchestrator.py

test:
	pytest tests/ -v

dashboard:
	streamlit run app/dashboard.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
