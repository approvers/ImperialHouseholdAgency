from opentelemetry import trace


def get_current_trace_id() -> str | None:
    """Get the current OpenTelemetry trace ID.

    Returns the trace ID as a 32-character lowercase hexadecimal string,
    or None if no valid span context exists.
    """
    current_span = trace.get_current_span()
    span_context = current_span.get_span_context()

    if span_context.is_valid:
        return format(span_context.trace_id, "032x")

    return None
