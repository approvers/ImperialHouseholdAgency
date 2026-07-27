from unittest.mock import MagicMock, patch

from src.system.infrastructure.ext.logfire.trace import get_current_trace_id


class TestGetCurrentTraceId:
    def test_returns_trace_id_when_span_is_valid(self) -> None:
        with patch(
            "src.system.infrastructure.ext.logfire.trace.trace"
        ) as mock_trace_module:
            mock_span_context = MagicMock()
            mock_span_context.is_valid = True
            mock_span_context.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace_module.get_current_span.return_value = mock_span

            result = get_current_trace_id()

        assert result == "1234567890abcdef1234567890abcdef"

    def test_returns_none_when_span_is_invalid(self) -> None:
        with patch(
            "src.system.infrastructure.ext.logfire.trace.trace"
        ) as mock_trace_module:
            mock_span_context = MagicMock()
            mock_span_context.is_valid = False
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace_module.get_current_span.return_value = mock_span

            result = get_current_trace_id()

        assert result is None
