# Development and Repository Guidelines

## Implementation Requirements

- All implementations **must pass** the following checks:
  `ty check`, `ruff check --fix`, `ruff format`, and `pytest`.

## Implementation Order

- Implementation **must proceed from the innermost layer**.
  - After completing each layer, a **review must be conducted** before proceeding to the next layer.

## Dependency Rules

- Dependencies under `src` **must be strictly controlled**.
  - `common` must not depend on any other modules.
  - `system` may depend on `common`.
  - External libraries may be used only when their necessity and appropriateness are justified.
- **Do not export namespaces via `__init__.py`**. Always import directly from the module where the symbol is defined.

## Code and Commit Conventions

- When implementing code or creating commits, **review existing implementations** and keep notation, structure, and style consistent.  
  In particular, code should follow the conventions used by other implementations within the same layer.

## Directory Structure

- The directory structures of `src` and `test` **must be identical**.
  - Any change in `src` must be reflected in `test`.
  - In principle, a **one-to-one correspondence between files** should be maintained.

## Commit Message Formatting

- Commit message prefixes **must be one of the following**:
  - `add: ` — for adding new features or files
  - `modify: ` — for modifying existing functionality
  - `remove: ` — for removing features or files
  - `fix: ` — for bug fixes
- Identifiers in commit messages **must be enclosed in backticks (`)**:
  - Class names: `ClassName`
  - Functions / methods: `function_name()`, `ClassName.method_name()`
  - Variables / attributes: `variable_name`, `ClassName.attribute`
  - File names / paths: `file.py`, `path/to/file.py`
  - Commands: `command`

## Language Policy

- The **output language** must follow the language used in the **most recent user input**.
- **Regardless of the user's input or output language**, all file contents (including **source code**), and **any other resources managed within the repository** must be written **in English**.
  - **Exception**: Comments and commit messages may be written in Japanese.
- All **identifiers** (variable names, function names, class names, module names, etc.) **must use only English or ASCII characters**.

## Testing Guidelines

- Write tests to achieve **as close to 100% direct coverage as possible** for all files.
  - If the cost of writing tests is prohibitively high and the disadvantages/costs outweigh the benefits, it is not necessary to force 100% coverage.
- For code that clearly does not need to be included in coverage (e.g., `pass` or `raise NotImplementedError` in abstract classes), use `# pragma: no cover` to exclude it from coverage.
- **Only when a file has no implementation at all** (e.g., `config.py`), exclude the entire file from coverage in `./pyproject.toml`. However, if there is even a small amount of implementation, this exception does not apply.
- **Do not use `patch()` with string paths** as a general rule, as this significantly reduces maintainability. However, it may be used for external libraries. Even in such cases, strive to avoid writing paths as strings by using `patch.object` or similar approaches.
- For all system code, anything that needs to be patched during testing should be **injected via DI** so that mocks can be passed in tests.
- This project uses **Sentry** and **Logfire**, so make sure to use both appropriately.
