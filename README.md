## Instructions to the reproduce issue

1. Clone the repo.

2. Create a Python virutal env
```
python -m venv .venv
```

3. Activate the virutal env.
```
.venv/Scripts/Activate.ps1 # Windows
```

```
source .venv/bin/activate # MacOS/Linux
```

4. Install the requirements.
```
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory similar to the `.example.env` file and add your Google API key.

6. Run evaluations using either of the following commands.

```
pytest src/tests
```

```
adk eval .\src\agents\orchestrator_agent .\src\tests\agents\orchestrator_agent\evalset56f9a2.evalset.json --config_file_path .\src\tests\agents\orchestrator_agent\test_config.json --print_detailed_results
```

