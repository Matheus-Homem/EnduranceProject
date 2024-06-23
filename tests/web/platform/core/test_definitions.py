import pytest

from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
    SectionDefinition,
)
from src.web.platform.core.enums import InputType


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

        self.test_persona1 = PersonaDefinition(
            public_name="Persona 1",
            private_name="persona1",
            role="This persona has the role to test the first persona definition creation",
            habit_description="About the habit of testing the persona1",
            inputs=[
                self.test_input1,
                self.test_input2,
            ],
        )
        self.test_persona2 = PersonaDefinition(
            public_name="Persona 2",
            private_name="persona2",
            role="This persona has the role to test the second persona definition creation",
            habit_description="About the habit of testing the persona2",
            inputs=InputCluster(
                is_recursive=True,
                inputs_list=[
                    self.test_input3,
                    self.test_input4,
                ],
            ),
        )

        self.test_section = SectionDefinition(
            public_name="section 1",
            private_name="section1",
            description="This section is the section responsible for testing the module definition",
            personas=[self.test_persona1, self.test_persona2],
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
            "persona": "persona1",
            "section": "section1",
            "input_fullname": "section1_persona1_input1",
            "optional": False,
            "columns": None,
            "rows": None,
        }

        assert isinstance(self.test_input1, InputDefinition)
        assert self.test_input1.asdict() == expected_input1_test_dict


class TestPersonaDefinition(TestDefinition):

    def test_persona_definition_creation(self):
        expected_persona1_test_dict = {
            "public_name": "Persona 1",
            "private_name": "persona1",
            "role": "This persona has the role to test the first persona definition creation",
            "habit_description": "About the habit of testing the persona1",
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
                    "persona": "persona1",
                    "section": "section1",
                    "input_fullname": "section1_persona1_input1",
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
                    "persona": "persona1",
                    "section": "section1",
                    "input_fullname": "section1_persona1_input2",
                    "optional": False,
                    "columns": None,
                    "rows": None,
                },
            ],
            "outputs": None,
            "section": "section1",
            "persona_fullname": "section1_persona1",
        }

        assert isinstance(self.test_persona1, PersonaDefinition)
        assert self.test_persona1.asdict() == expected_persona1_test_dict

    def test_persona_definition_fullname(self):
        assert self.test_persona1.persona_fullname == "section1_persona1"

    def test_persona_definition_inputs_list(self):
        assert isinstance(self.test_persona1.inputs_list, list)
        assert all(
            isinstance(input, InputDefinition)
            for input in self.test_persona1.inputs_list
        )

        assert isinstance(self.test_persona2.inputs_list, list)
        assert all(
            isinstance(input, InputDefinition)
            for input in self.test_persona2.inputs_list
        )

    def test_persona_definition_map_input_definitions(self):
        #print(self.test_persona1.map_input_definitions())
        pass


class TestSectionDefinition(TestDefinition):

    def test_set_persona(self):
        assert self.test_input1.persona == "persona1"
        assert self.test_input2.persona == "persona1"
        assert self.test_input3.persona == "persona2"
        assert self.test_input4.persona == "persona2"

    def test_set_section(self):
        assert self.test_persona1.section == "section1"
        assert self.test_persona2.section == "section1"
        assert self.test_input1.section == "section1"
        assert self.test_input2.section == "section1"
        assert self.test_input3.section == "section1"
        assert self.test_input4.section == "section1"

    def test_set_fullname(self):
        assert self.test_persona1.persona_fullname == "section1_persona1"
        assert self.test_persona2.persona_fullname == "section1_persona2"
        assert self.test_input1.input_fullname == "section1_persona1_input1"
        assert self.test_input2.input_fullname == "section1_persona1_input2"
        assert self.test_input3.input_fullname == "section1_persona2_input3"
        assert self.test_input4.input_fullname == "section1_persona2_input4"
