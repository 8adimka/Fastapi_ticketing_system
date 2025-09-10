from src.core.exceptions import TicketStatusNotAllowed


class TestExceptions:
    """Test cases for custom exceptions"""

    def test_ticket_status_not_allowed_exception(self):
        """Test TicketStatusNotAllowed exception"""
        expression = "Status Not Allowed"
        message = "From status open to closed Not Allowed"

        exception = TicketStatusNotAllowed(expression, message)

        assert exception.expression == expression
        assert exception.message == message
        assert str(exception) == message

    def test_ticket_status_not_allowed_inheritance(self):
        """Test that TicketStatusNotAllowed inherits from Error"""
        exception = TicketStatusNotAllowed("test", "test message")

        assert isinstance(exception, Exception)
