#!/usr/bin/env bash

conf_print_gitignore() {
  cat <<-'EOF'
		__pycache__/
		*.py[cod]
		*$py.class
		*.so
		.Python
		build/
		develop-eggs/
		dist/
		downloads/
		eggs/
		.eggs/
		lib/
		lib64/
		parts/
		sdist/
		var/
		wheels/
		share/python-wheels/
		*.egg-info/
		.installed.cfg
		*.egg
		MANIFEST
		
		# Virtual Environments & Package Managers
		.venv/
		env/
		venv/
		ENV/
		env.bak/
		venv.bak/
		.uv/
		
		# Mise Local Environment / Overrides
		.mise/
		.mise.toml
	
		# IDEs and Editors
		.vscode/
		.idea/
		*.swp
		*.swo
		.DS_Store
		
		# Logs and Testing
		*.log
		logs/
		htmlcov/
		.tox/
		.nox/
		.coverage
		.coverage.*
		.cache
		nosetests.xml
		coverage.xml
		*.cover
		*.py,cover
		.hypothesis/
		.pytest_cache/
		.ruff_cache/
	EOF
}
conf_print_gitignore | tee .gitignore

conf_print_dockerignore() {
  cat <<-'EOF'
	  # Version Control
		.git
		.gitignore

		# Virtual Environments & Package Managers (Docker will build its own fresh .venv)
		.venv/
		env/
		venv/
		.uv/

		# Mise
		.mise/
		.mise.toml

		# Python Cache & Build Artifacts
		__pycache__/
		*.py[cod]
		*.so
		build/
		dist/
		*.egg-info/
		
		# IDEs & OS Files
		.vscode/
		.idea/
		.DS_Store
		
		# Documentation & Logs
		docs/
		*.log
	EOF
}
conf_print_gitignore | tee .dockerignore

conf_print_mise_toml() {
  cat <<-'EOF'
		[tools]
		python = "3.12"  # or whichever Python version you prefer
		uv = "latest"

		[settings]
		python.uv_venv_auto = "create|source"
	EOF
}
conf_print_mise_toml | tee mise.toml

mise trust
mise install

uv init --app
uv add libephemeris
