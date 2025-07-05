# Setup Guide for **clinical-ai-scribe-prompt-library**

> This document walks you through cloning the repo, installing dependencies, configuring environment variables, and running your first evaluation. It complements `README.md` by giving **step‑by‑step** instructions to get the project running locally or in CI.

---

## 1  Prerequisites

| Requirement | Recommended Version | Notes |
|-------------|---------------------|-------|
| **Python**  | 3.10 or newer | Tested on CPython 3.10/3.11. Older versions may miss security fixes. |
| **Git**     | Any recent | To clone & contribute. |
| **pip / venv** | Latest pip (≥ 24.0) | We use a virtual‑env to isolate deps. |
| **LLM API keys** | e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_GEMINI_API_KEY` | Needed to call GPT‑4, Claude, Gemini. |
| *(Optional)* **CUDA‑enabled GPU** | CUDA 12.x | Only required if you plan to run local GPU models. |

> **Tip:** Check Python version ➜ `python --version`. If < 3.10, install a newer Python or use **pyenv**.

---

## 2  Clone & Create Virtual Environment

```bash
# 1. Clone
$ git clone https://github.com/<your‑org>/clinical-ai-scribe-prompt-library.git
$ cd clinical-ai-scribe-prompt-library

# 2. Create & activate a virtual env
$ python -m venv .venv
$ source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

---

## 3  Install Dependencies

All mandatory Python packages are pinned in **`requirements.txt`**. A minimal list looks like:

```text
# requirements.txt
langchain>=0.2.0           # core prompt/chain helpers citeturn0search0
langsmith>=0.1.6           # eval & tracing client citeturn0search1
openai>=1.93.0             # OpenAI API wrapper citeturn0search2
pyyaml>=6.0
rich>=13.7
pytest>=8.0                # optional: run unit tests
```

```bash
$ pip install -r requirements.txt
```

**Optional extras** (GPU inference, dataset tooling, etc.) live in `requirements-dev.txt`.

---

## 4  Configure Environment Variables

Create (and never commit) a **`.env`** or export variables in your shell:

```bash
# LLM providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="claude-..."   # Claude models
export GOOGLE_GEMINI_API_KEY="AIza..."  # Gemini models

# LangSmith (optional)
export LANGSMITH_API_KEY="ls_..."  # get from https://smith.langchain.com
export LANGSMITH_PROJECT="clinical-ai-scribe-tests"
```

> **Security**: Add `.env` and any file called `*key*` or `*secret*` to `.gitignore`.

---

## 5  Project Layout After Setup

```
clinical-ai-scribe-prompt-library/
├── prompts/         # YAML prompt definitions
├── evaluations/     # YAML eval configs &/or Python checkers
├── examples/        # Sample LLM outputs & annotations
├── tools/           # Helper scripts (run cli / notebooks)
├── tests/           # pytest cases (optional)
├── requirements.txt
├── README.md
└── SETUP.md         # this file
```

You can add your own sub‑folders, but try to keep prompts & evals under their respective directories.

---

## 6  Running a Sample Evaluation

We ship a thin CLI wrapper in **`tools/run_all_evaluations.py`**. By default it:
1. Scans `prompts/` for `*.prompt.yaml` files.
2. Invokes the chosen LLM (configurable via `--model`).
3. Runs associated checks defined in `evaluations/`.
4. Prints a JSON summary and exits non‑zero if any test fails (CI‑friendly).

```bash
# Dry‑run with GPT‑4o
$ python tools/run_all_evaluations.py --model gpt-4o

# Use Claude 3.5‑Sonnet, restrict to medication tests
$ python tools/run_all_evaluations.py \
      --model claude-3.5-sonnet \
      --tag medication_logic
```

> **Note:** Set `OPENAI_API_BASE` or `ANTHROPIC_API` env vars if you use a proxy or on‑prem gateway.

### LangSmith Quick‑Start (optional)

```bash
# Enable tracing so every prompt/response flows to LangSmith
export LANGSMITH_TRACING="true"

# Run the script again – results appear in https://smith.langchain.com/projects/<project-id>
$ python tools/run_all_evaluations.py --model gpt-4o
```

LangSmith gives you diff views, histograms of failures, and regression dashboards. See **examples/langsmith_dashboard.png** for a preview.

---

## 7  Adding New Prompts / Evaluations

1. Copy the template from `prompts/_TEMPLATE.prompt.yaml` into the right specialty sub‑folder.
2. Fill in the metadata (`name`, `specialty`, `description`, `tags`).
3. Write the `system` & `user` blocks (multiple turns allowed).
4. State the **expected outcome** or **evaluation criteria**.
5. (Optionally) add a file in `evaluations/` if you need advanced programmatic checks.
6. Create an example run (`examples/your_prompt_example.md`) showing at least one model’s output.
7. Open a Pull Request following `CONTRIBUTING.md`.

> New prompts **must** include at least one safety or accuracy criterion – e.g., a flag for omissions, hallucinations, dosage errors, or guideline drift.

---

## 8  Running Tests (pytest)

We treat evaluation scripts as test cases:

```bash
$ pytest tests/  # runs any unit tests plus sample eval regressions
```

You can wire this into GitHub Actions so every PR triggers a lightweight smoke test (see `.github/workflows/ci.yaml`).

---

## 9  Troubleshooting & FAQ

| Symptom | Possible Fix |
|---------|--------------|
| "ImportError: langchain" | `pip install -r requirements.txt` (did you activate your venv?) |
| LLM returns 401/invalid API key | Check env variable spelling and token region restrictions |
| GPU out‑of‑memory errors | Lower the context window / use CPU / change model type |
| YAML parsing errors | Ensure indentation is 2 spaces, not tabs. Validate with `yamllint`. |

For more, open an issue or start a discussion.

---

## 10  License & Acknowledgements

This repository is released under the **MIT License** (see `LICENSE`). By contributing, you agree your contribution will be licensed under MIT. Thank you to all clinicians, researchers, and developers who help make clinical AI safer!

