# Code Formatting and Linting Documentation

This document describes the code formatting and linting setup for the quantum_patterns project.

## Tools Used

### Black - Code Formatter
- **Purpose**: Automatic code formatting for consistent style
- **Version**: >=24.0.0
- **Configuration**: Line length 88, Python 3.12 target

### Ruff - Linter
- **Purpose**: Fast Python linter with auto-fix capabilities
- **Version**: >=0.8.0
- **Configuration**: Comprehensive rule set with auto-fix support

## Configuration

### Black Configuration
```toml
[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | htmlcov
  | \.pytest_cache
  | \.ruff_cache
  # generated code folders
  | notebooks
  | converted_notebooks
  | target_github_projects
  | data
)/
'''
```

### Ruff Configuration
```toml
[tool.ruff]
target-version = "py312"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]
exclude = [
    ".eggs",
    ".git",
    ".hg",
    ".mypy_cache",
    ".tox",
    ".venv",
    "_build",
    "buck-out",
    "build",
    "dist",
    "htmlcov",
    ".pytest_cache",
    ".ruff_cache",
    # generated code folders
    "notebooks",
    "converted_notebooks", 
    "target_github_projects",
    "data",
]
```

## Available Commands

### Formatting Commands
```bash
# Format all Python files with Black
just format

# Format specific file or directory
just format-file src/core_concepts/

# Check formatting without making changes
just format-check

# Format and show diff
just format-diff
```

### Linting Commands
```bash
# Lint all Python files with Ruff
just lint

# Lint specific file or directory
just lint-file src/core_concepts/

# Lint and fix automatically
just lint-fix

# Lint and fix specific file
just lint-fix-file src/core_concepts/
```

### Combined Commands
```bash
# Run both formatting and linting
just format-lint

# Check formatting and linting without making changes
just check-all

# Format, lint, and run tests
just format-lint-test
```

## Excluded Directories

The following directories are excluded from formatting and linting as they contain generated code:

- `notebooks/` - Jupyter notebooks
- `converted_notebooks/` - Converted Python files from notebooks
- `target_github_projects/` - Cloned GitHub repositories
- `data/` - Data files and source snippets

## Current Status

### Formatting Status
- ✅ **All source files properly formatted**
- ✅ **Black configuration working correctly**
- ✅ **Generated code folders excluded**

### Linting Status
- ✅ **Ruff configuration working correctly**
- ✅ **Most issues auto-fixed**
- ⚠️ **9 remaining linting issues** (mostly minor):
  - Unnecessary `list()` calls in `sorted()`
  - Unused variables in tests
  - Whitespace in multiline strings
  - Missing import in test fixtures

### Files Processed
- **16 files reformatted** by Black
- **22 files checked** by Ruff
- **Generated code folders excluded** as requested

## Usage Examples

### Daily Development Workflow
```bash
# Before committing code
just format-lint

# Check if code needs formatting
just format-check

# Fix linting issues automatically
just lint-fix
```

### CI/CD Integration
```bash
# Check formatting and linting in CI
just check-all

# Full code quality pipeline
just format-lint-test
```

### Specific File Workflow
```bash
# Format specific file
just format-file src/core_concepts/identify_classiq_core_concepts.py

# Lint specific file
just lint-file tests/test_identify_classiq_core_concepts.py
```

## Best Practices

### Development
1. **Run formatting before committing**: `just format`
2. **Fix linting issues**: `just lint-fix`
3. **Check everything**: `just check-all`

### Code Review
1. **Ensure formatting is applied**: `just format-check`
2. **Verify no linting issues**: `just lint`
3. **Run full pipeline**: `just format-lint-test`

### Maintenance
1. **Regular formatting**: Run `just format` regularly
2. **Address linting issues**: Use `just lint-fix` for auto-fixable issues
3. **Manual fixes**: Address remaining issues manually

## Integration with IDE

### VS Code
- Install Black Formatter extension
- Install Ruff extension
- Configure to use project settings

### PyCharm
- Configure external tools for Black and Ruff
- Set up file watchers for automatic formatting

## Troubleshooting

### Common Issues
1. **Formatting conflicts**: Run `just format` to resolve
2. **Linting errors**: Use `just lint-fix` for auto-fixable issues
3. **Import sorting**: Ruff handles this automatically

### Configuration Updates
- Black settings in `[tool.black]` section of `pyproject.toml`
- Ruff settings in `[tool.ruff]` section of `pyproject.toml`
- Exclusions can be updated in both configurations

## Performance

### Black
- **Fast formatting**: Typically < 1 second for project
- **Incremental**: Only processes changed files
- **Consistent**: Same output regardless of input style

### Ruff
- **Very fast linting**: 10-100x faster than other linters
- **Auto-fix**: Automatically fixes many issues
- **Comprehensive**: Catches many code quality issues

## Future Improvements

### Potential Enhancements
1. **Pre-commit hooks**: Automatically run formatting/linting
2. **IDE integration**: Better editor integration
3. **Custom rules**: Project-specific linting rules
4. **Documentation**: Auto-generate formatting documentation

### Monitoring
- **Regular checks**: Run `just check-all` regularly
- **CI integration**: Include in automated testing
- **Team adoption**: Ensure all team members use the tools
