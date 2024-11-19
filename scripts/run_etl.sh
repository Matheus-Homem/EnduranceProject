source .venv/bin/activate
python -c "from src.etl.orchestrator import orchestrate_etl_process; orchestrate_etl_process()"
deactivate