ARG PYTHON_VERSION=3.14
ARG PYTHON_BIN_PATH=/opt/python

ARG VENV_DIR=/opt/venv
ARG APP_DIR=/opt/app

# =================================================================
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder_without_dev

# Inherit Common environment variables
ARG PYTHON_VERSION
ARG PYTHON_BIN_PATH

ARG VENV_DIR
ARG APP_DIR

# Settings for uv to use in distroless
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=${PYTHON_BIN_PATH} \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PROJECT_ENVIRONMENT=${VENV_DIR}

# Install and create venv
RUN uv python install ${PYTHON_VERSION} && \
    uv venv ${VENV_DIR}

WORKDIR ${APP_DIR}

# Install dependencies
RUN --mount=type=cache,target=/tmp/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY ./ ${APP_DIR}

# =================================================================
FROM ubuntu:24.04 AS developer

# Inherit Common environment variables
ARG PYTHON_BIN_PATH

ARG VENV_DIR
ARG APP_DIR

ENV UV_PROJECT_ENVIRONMENT=${VENV_DIR}

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy built artifacts
COPY --from=builder_without_dev ${PYTHON_BIN_PATH} ${PYTHON_BIN_PATH}
COPY --from=builder_without_dev ${VENV_DIR} ${VENV_DIR}
COPY --from=builder_without_dev ${APP_DIR} ${APP_DIR}

ENV PATH="${VENV_DIR}/bin:$PATH"

WORKDIR ${APP_DIR}

# Install dev dependencies
RUN --mount=type=cache,target=/tmp/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --dev

CMD ["sleep", "infinity"]

# =================================================================
# Since Python requires glibc to run,
# we can't change the base image to static:nonroot.
FROM gcr.io/distroless/cc-debian12:nonroot AS runner

# Inherit Common environment variables
ARG PYTHON_BIN_PATH

ARG VENV_DIR
ARG APP_DIR

# Copy built artifacts
COPY --from=builder_without_dev --chown=nonroot:nonroot ${PYTHON_BIN_PATH} ${PYTHON_BIN_PATH}
COPY --from=builder_without_dev --chown=nonroot:nonroot ${VENV_DIR} ${VENV_DIR}
COPY --from=builder_without_dev --chown=nonroot:nonroot ${APP_DIR} ${APP_DIR}

ENV PATH="${VENV_DIR}/bin:$PATH"

WORKDIR ${APP_DIR}

CMD ["python", "main.py"]
