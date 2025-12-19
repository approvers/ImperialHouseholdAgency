# Development and Repository Guidelines

## Implementation Requirements

- All implementations **must pass** the following checks:  
  `mypy --strict`, `ty check`, `ruff check --fix`, `ruff format`, and `pytest`.

## Dependency Rules

- Dependencies under `src` **must be strictly controlled**.
  - `common` must not depend on any other modules.
  - `config` may depend **only** on `common`.
  - `system` may depend on `common` and `config`.
  - External libraries may be used only when their necessity and appropriateness are justified.

## Code and Commit Conventions

- When implementing code or creating commits, **review existing implementations** and keep notation, structure, and style consistent.  
  In particular, code should follow the conventions used by other implementations within the same layer.

## Directory Structure

- The directory structures of `src` and `test` **must be identical**.
  - Any change in `src` must be reflected in `test`.
  - In principle, a **one-to-one correspondence between files** should be maintained.

## Commit Message Formatting

- Identifiers in commit messages **must be enclosed in backticks (`)**:
  - Class names: `ClassName`
  - Functions / methods: `function_name()`, `ClassName.method_name()`
  - Variables / attributes: `variable_name`, `ClassName.attribute`
  - File names / paths: `file.py`, `path/to/file.py`
  - Commands: `command`

## Language Policy

- The **output language** must follow the language used in the **most recent user input**.
- **Regardless of the user’s input or output language**, all file contents (including **source code and comments**), **commit messages**, and **any other resources managed within the repository** must be written **in English**.
