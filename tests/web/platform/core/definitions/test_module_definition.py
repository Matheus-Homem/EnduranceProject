import pytest

from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    ModuleDefinition,
    SegmentDefinition,
)
from src.web.platform.core.functions import datetime_difference
from src.web.platform.core.types import FormattingType, InputType


class TestModuleDefinition:

    def test_module_definition_creation(self):
        module_test = ModuleDefinition(
            public_name="test_public_name",
            private_name="test_private_name",
            role="This module has the role to test the module definition creation",
            habit_description="About the habit of testing",
            inputs=[
                InputDefinition(
                    private_name="test_input1", type=InputType.TEXT, placeholder="Test"
                ),
                InputDefinition(
                    private_name="test_input1",
                    type=InputType.NUMBER,
                    min_length=1,
                    max_length=10,
                ),
            ],
        )

        expected_module_test = {
            "public_name": "test_public_name",
            "private_name": "test_private_name",
            "role": "This module has the role to test the module definition creation",
            "habit_description": "About the habit of testing",
            "inputs": [
                {
                    "private_name": "test_input1",
                    "type": "text",
                    "placeholder": "Test",
                    "options": None,
                    "min_length": None,
                    "max_length": None,
                    "label": None,
                    "public_name": None,
                    "output_formatting": None,
                },
                {
                    "private_name": "test_input1",
                    "type": "number",
                    "placeholder": None,
                    "options": None,
                    "min_length": 1,
                    "max_length": 10,
                    "label": None,
                    "public_name": None,
                    "output_formatting": None,
                },
            ],
            "outputs": None,
        }

        assert isinstance(module_test, ModuleDefinition)
        assert module_test.asdict() == expected_module_test

    def module_definition_full_name(self):
        pass
