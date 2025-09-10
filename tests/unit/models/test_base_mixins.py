from unittest.mock import MagicMock

import pytest

from src.models.base_mixins import AuditMixin, BaseMixin, TimestampMixin


class TestBaseMixin:
    """Test cases for BaseMixin"""

    def test_base_mixin_tablename(self):
        """Test that BaseMixin generates correct table name"""

        class TestModel(BaseMixin):
            pass

        assert TestModel.__tablename__ == "testmodels"

    def test_base_mixin_id_column(self):
        """Test that BaseMixin has correct id column"""
        # Mock the column to avoid SQLAlchemy setup
        with pytest.MonkeyPatch().context() as m:
            m.setattr("sqlalchemy.Column", MagicMock())
            m.setattr("sqlalchemy.dialects.postgresql.UUID", MagicMock())

            class TestModel(BaseMixin):
                pass

            # Verify the mixin is applied
            assert hasattr(TestModel, "id")


class TestTimestampMixin:
    """Test cases for TimestampMixin"""

    def test_timestamp_mixin_columns(self):
        """Test that TimestampMixin has correct columns"""
        # Mock the columns to avoid SQLAlchemy setup
        with pytest.MonkeyPatch().context() as m:
            m.setattr("sqlalchemy.Column", MagicMock())
            m.setattr("sqlalchemy.DateTime", MagicMock())

            class TestModel(TimestampMixin):
                pass

            # Verify the mixin is applied
            assert hasattr(TestModel, "created_at")
            assert hasattr(TestModel, "updated_at")


class TestAuditMixin:
    """Test cases for AuditMixin"""

    def test_audit_mixin_columns(self):
        """Test that AuditMixin has correct columns"""
        # Mock the columns to avoid SQLAlchemy setup
        with pytest.MonkeyPatch().context() as m:
            m.setattr("sqlalchemy.Column", MagicMock())
            m.setattr("sqlalchemy.Text", MagicMock())

            class TestModel(AuditMixin):
                pass

            # Verify the mixin is applied
            assert hasattr(TestModel, "created_by")
            assert hasattr(TestModel, "updated_by")


class TestMixedMixins:
    """Test cases for combining multiple mixins"""

    def test_combined_mixins(self):
        """Test that multiple mixins can be combined"""
        # Mock the columns to avoid SQLAlchemy setup
        with pytest.MonkeyPatch().context() as m:
            m.setattr("sqlalchemy.Column", MagicMock())
            m.setattr("sqlalchemy.DateTime", MagicMock())
            m.setattr("sqlalchemy.Text", MagicMock())
            m.setattr("sqlalchemy.dialects.postgresql.UUID", MagicMock())

            class TestModel(BaseMixin, TimestampMixin, AuditMixin):
                pass

            # Verify all mixins are applied
            assert hasattr(TestModel, "id")
            assert hasattr(TestModel, "created_at")
            assert hasattr(TestModel, "updated_at")
            assert hasattr(TestModel, "created_by")
            assert hasattr(TestModel, "updated_by")
            assert TestModel.__tablename__ == "testmodels"
