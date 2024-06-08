import pytest
from src.web.platform.core.types import FormattingType, InputType
from src.web.platform.core.functions import datetime_difference
from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    ModuleDefinition,
    SegmentDefinition,
)

class TestModuleDefinition:
    def setup_method(self):
        self.module_test = ModuleDefinition(
            public_name="test_public_name",
            private_name="test_private_name",
            role="This module has the role to test the module definition creation",
            habit_description="About the habit of testing",
            inputs=InputDefinition(
                private_name="test",
                type=InputType.TEXT,
                placeholder="Test"
            )
        )

    def test_module_definition_creation(self):
        assert isinstance(self.module_test, ModuleDefinition)

    def module_definition_full_name(self):
        pass