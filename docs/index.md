---
title: Quantum Software Analysis Project
description: Automated framework for analyzing quantum software to identify recurring software patterns across quantum frameworks.
permalink: /
---

# Quantum Software Analysis Project (QPA)

A reproducible, open-source framework and toolchain for analyzing the source code of popular quantum computing libraries to identify recurring software patterns.

This project automates discovery, preprocessing, semantic analysis, and reporting so researchers and engineers can study how quantum software concepts are used across frameworks such as Qiskit, PennyLane, and Classiq.

## Key Features

- Dynamic discovery of target repositories via the GitHub API
- Automated preprocessing of code and Jupyter notebooks
- Semantic concept extraction and pattern matching against the PlanQK Pattern Atlas
- Reproducible experimental data exports and comprehensive reports

## Quick Start

Prerequisites:

- Python 3.12+
- Git
- `just` (command runner)
- A GitHub Personal Access Token (set `GITHUB_TOKEN` in a `.env` file)

Core commands:

```bash
just install            # setup environment, clone targets, install deps
just identify-concepts  # extract framework concepts
just run_main           # run the main semantic analysis
just report             # generate final reports
just experimental-data  # export full experimental datasets
```

## Documentation & Data

- Experimental datasets and reproducibility notes: [docs/experimental_data.md](experimental_data.md)
- Final report: [docs/final_pattern_report.md](final_pattern_report.md)
- Generated CSV & JSON data: see the `data/` directory in the repository

## Citation

If you use this work in research, please cite:

```text
Leite Ramalho, Neilson C.; da Silva, Érico A.; Amario de Souza, H.; Chaim, Marcos. "qpq: Quantum Pattern Analysis", 2026. DOI: 10.5281/zenodo.18342945
```

## Contributing

We welcome contributions. The project follows strict reproducibility and testing practices: please run formatting, linting and tests before submitting PRs:

```bash
just format-lint-test
just test-coverage
```

See the repository `README.md` for full setup and the complete workflow.

## License

This project is open source — see the repository `LICENSE` file for details.
