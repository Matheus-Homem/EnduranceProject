import pytest

from src.web.platform.core.definitions import (
    BoxDefinition,
    InputCluster,
    InputDefinition,
    SectionDefinition,
)
from src.web.platform.core.enums import InputType, SectionType


class TestDefinition:

    def setup_method(self):
        self.test_input1 = InputDefinition(
            private_name="input1", type=InputType.TEXT, placeholder="Test"
        )

        self.test_input2 = InputDefinition(
            private_name="input2",
            type=InputType.NUMBER,
            min_length=1,
            max_length=10,
        )

        self.test_input3 = InputDefinition(private_name="input3", type=InputType.DATE)

        self.test_input4 = InputDefinition(
            private_name="input4",
            type=InputType.TEXTA_AREA,
        )

        self.test_box1 = BoxDefinition(
            public_name="Box 1",
            private_name="box1",
            role="This box has the role to test the first box definition creation",
            habit_description="About the habit of testing the box1",
            inputs=[
                self.test_input1,
                self.test_input2,
            ],
        )
        self.test_box2 = BoxDefinition(
            public_name="Box 2",
            private_name="box2",
            role="This box has the role to test the second box definition creation",
            habit_description="About the habit of testing the box2",
            inputs=InputCluster(
                is_recursive=True,
                inputs_list=[
                    self.test_input3,
                    self.test_input4,
                ],
            ),
        )

        self.test_section = SectionDefinition(
            type=SectionType.BASIC,
            header="Section 1",
            description="This section is the section responsible for testing the module definition",
            boxes=[self.test_box1, self.test_box2],
        )


class TestInputDefinition(TestDefinition):

    def test_input_definition_creation(self):
        expected_input1_test_dict = {
            "private_name": "input1",
            "type": "text",
            "options": None,
            "placeholder": "Test",
            "min_length": None,
            "max_length": None,
            "label": None,
            "public_name": None,
            "output_formatting": None,
            "box": "box1",
            "section": "basic",
            "input_fullname": "basic_box1_input1",
            "optional": False,
            "columns": None,
            "rows": None,
        }

        assert isinstance(self.test_input1, InputDefinition)
        assert self.test_input1.asdict() == expected_input1_test_dict


class TestBoxDefinition(TestDefinition):

    def test_box_definition_creation(self):
        expected_box1_test_dict = {
            "public_name": "Box 1",
            "private_name": "box1",
            "role": "This box has the role to test the first box definition creation",
            "habit_description": "About the habit of testing the box1",
            "inputs": [
                {
                    "private_name": "input1",
                    "type": "text",
                    "options": None,
                    "placeholder": "Test",
                    "min_length": None,
                    "max_length": None,
                    "label": None,
                    "public_name": None,
                    "output_formatting": None,
                    "box": "box1",
                    "section": "basic",
                    "input_fullname": "basic_box1_input1",
                    "optional": False,
                    "columns": None,
                    "rows": None,
                },
                {
                    "private_name": "input2",
                    "type": "number",
                    "options": None,
                    "placeholder": None,
                    "min_length": 1,
                    "max_length": 10,
                    "label": None,
                    "public_name": None,
                    "output_formatting": None,
                    "box": "box1",
                    "section": "basic",
                    "input_fullname": "basic_box1_input2",
                    "optional": False,
                    "columns": None,
                    "rows": None,
                },
            ],
            "outputs": None,
            "section": "basic",
            "box_fullname": "basic_box1",
        }

        assert isinstance(self.test_box1, BoxDefinition)
        assert self.test_box1.asdict() == expected_box1_test_dict

    def test_box_definition_fullname(self):
        assert self.test_box1.box_fullname == "basic_box1"

    def test_box_definition_inputs_list(self):
        assert isinstance(self.test_box1.inputs_list, list)
        assert all(
            isinstance(input, InputDefinition) for input in self.test_box1.inputs_list
        )

        assert isinstance(self.test_box2.inputs_list, list)
        assert all(
            isinstance(input, InputDefinition) for input in self.test_box2.inputs_list
        )

    def test_box_definition_map_input_definitions(self):
        # print(self.test_box1.map_input_definitions())
        pass


class TestSectionDefinition(TestDefinition):

    def test_set_box(self):
        assert self.test_input1.box == "box1"
        assert self.test_input2.box == "box1"
        assert self.test_input3.box == "box2"
        assert self.test_input4.box == "box2"

    def test_set_section(self):
        assert self.test_box1.section == "basic"
        assert self.test_box2.section == "basic"
        assert self.test_input1.section == "basic"
        assert self.test_input2.section == "basic"
        assert self.test_input3.section == "basic"
        assert self.test_input4.section == "basic"

    def test_set_fullname(self):
        assert self.test_box1.box_fullname == "basic_box1"
        assert self.test_box2.box_fullname == "basic_box2"
        assert self.test_input1.input_fullname == "basic_box1_input1"
        assert self.test_input2.input_fullname == "basic_box1_input2"
        assert self.test_input3.input_fullname == "basic_box2_input3"
        assert self.test_input4.input_fullname == "basic_box2_input4"
