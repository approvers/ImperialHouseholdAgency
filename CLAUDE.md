# Development and Repository Guidelines

> **Note**: This document must be kept in sync with the actual codebase.
> When making structural changes (adding layers, modules, or changing patterns), update this document accordingly.

## Project Structure

```
src/
├── common/                          # Common foundation (no dependencies on other modules)
│   ├── config/
│   │   └── interface.py             # ConfigIf: Base config interface
│   ├── di/
│   │   └── builder.py               # ModuleBase, BindEntry: DI module base
│   └── interface.py                 # Interface = ABC alias
│
└── system/                          # Main system (depends only on common)
    ├── domain/                      # Domain layer (business logic)
    │   ├── config.py                # DomainConfigIf, EnvironmentEnum
    │   ├── model/                   # Domain models
    │   │   ├── base.py              # DomainModelBase (Pydantic BaseModel + Interface)
    │   │   ├── user.py              # User
    │   │   ├── messenger.py         # Messenger
    │   │   └── nickname.py          # NicknameChangelog
    │   ├── value/                   # Value objects
    │   │   ├── base/
    │   │   │   ├── identifier.py    # ULIDBase (RootModel[ULID])
    │   │   │   └── time.py          # CreatedAtBase, UpdatedAtBase (RootModel[datetime])
    │   │   ├── user.py              # UserRecordID, UserID, UserCreatedAt, etc.
    │   │   ├── messenger.py         # MessengerRecordID, MessengerName, etc.
    │   │   └── nickname.py          # NicknameChangelogRecordID, Nickname, etc.
    │   └── interface/
    │       └── repository/          # Repository interfaces
    │           ├── common/
    │           │   ├── base.py      # RepositoryBase
    │           │   ├── response.py  # RepositoryResponse[T], RepositoryResultStatusEnum, etc.
    │           │   └── option.py    # SortOrder
    │           ├── user.py          # UserRepository
    │           ├── messenger.py     # MessengerRepository
    │           └── nickname.py      # NicknameChangelogRepository
    │
    ├── infrastructure/              # Infrastructure layer (external system integration)
    │   ├── repository/
    │   │   └── sqlalchemy/          # SQLAlchemy implementation
    │   │       ├── config.py        # SQLAlchemyConfigIf
    │   │       ├── model/           # SQLAlchemy models (ULIDMixin, CreatedAtMixin, etc.)
    │   │       ├── crud/            # Repository implementations (SAUserRepository, etc.)
    │   │       ├── translator/      # Domain <-> DB conversion (SAUserTranslator, etc.)
    │   │       └── type/            # Custom types (ULIDColumn)
    │   └── ext/                     # External services
    │       ├── sentry/              # Sentry error tracking
    │       └── logfire/             # Logfire observability
    │
    ├── usecase/                     # Usecase layer (application logic)
    │   └── base/
    │       ├── dto.py               # UsecaseRequest, UsecaseResponse (Pydantic BaseModel)
    │       └── interface.py         # UsecaseIf[RequestT, ResponseT].execute()
    │
    ├── ui/                          # UI layer (external interfaces)
    │   └── discord/
    │       └── config.py            # DiscordConfigIf
    │
    ├── di/                          # Dependency injection
    │   ├── container.py             # DIContainer (Injector)
    │   └── module/                  # DI module definitions
    │       ├── domain/config/       # PydanticDomainConfigModule
    │       ├── infrastructure/
    │       │   ├── repository/sqlalchemy/  # SARepositoryModule
    │       │   └── ext/             # Sentry, Logfire modules
    │       └── ui/discord/config/   # PydanticDiscordConfigModule
    │
    ├── util/                        # Utilities
    │   ├── id.py                    # generate_ulid()
    │   └── datetime.py              # utcnow()
    │
    └── config.py                    # Environment-specific config (BaseConfig, TestConfig, etc.)
```

## Architecture Patterns

### Layer Dependencies (Clean Architecture)

```
ui → usecase → domain ← infrastructure
         ↓
       common
```

- **common**: Common foundation. No dependencies on other modules
- **domain**: Business logic. Depends on common only
- **usecase**: Application logic. Depends on domain (and common)
- **infrastructure**: External system implementation. Implements domain interfaces (depends on domain and common)
- **ui**: User interface. Calls usecase (depends on usecase and common)

### Key Patterns

1. **Repository Pattern**
   - Interface: `src/system/domain/interface/repository/{entity}.py`
   - Implementation: `src/system/infrastructure/repository/sqlalchemy/crud/{entity}.py`
   - Response: `RepositoryResponse[T]` with `is_success`, `status`, `reason`, `message`

2. **Translator Pattern** (Domain ⇔ DB)
   - `BaseSADomainTranslator[DomainT, SAModelT]`
   - Static methods: `to_domain()`, `to_db_record()`
   - Lazy imports inside methods to avoid circular dependencies

3. **Value Object Pattern**
   - Wrap primitives with `RootModel[T]`
   - ULID identifiers extend `ULIDBase`
   - Timestamps extend `CreatedAtBase` / `UpdatedAtBase`

4. **Usecase Pattern**
   - Request/Response DTOs extend `UsecaseRequest` / `UsecaseResponse`
   - Interface: `UsecaseIf[RequestT, ResponseT]` with `async execute()`

5. **DI Pattern**
   - `injector` library with `Module`, `@provider`, `@singleton`
   - Config interfaces bound to Pydantic implementations
   - Repositories bound with `singleton` scope

### Naming Conventions

| Category | Pattern | Example |
|----------|---------|---------|
| Domain Model | `{Entity}` | `User`, `Messenger` |
| Value Object | `{Entity}{Field}` | `UserRecordID`, `UserCreatedAt` |
| Repository Interface | `{Entity}Repository` | `UserRepository` |
| SQLAlchemy Impl | `SA{Entity}Repository` | `SAUserRepository` |
| Translator | `SA{Entity}Translator` | `SAUserTranslator` |
| Config Interface | `{Component}ConfigIf` | `DiscordConfigIf` |
| Usecase Interface | `{Action}UsecaseIf` | (to be implemented) |

### Observability

- All meaningful operations in **usecase**, **repository**, and **ui** layers must be decorated with `@logfire.instrument(span_name="ClassName.method_name()")`
- Sentry for error tracking

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

- Test files are **colocated** with source files in `src/`.
  - Each source file `module.py` has a corresponding test file `test_module.py` in the same directory.
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
