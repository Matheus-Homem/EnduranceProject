import pytest

from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
    PillarDefinition,
)
from src.web.platform.core.enums import InputType
from src.web.platform.core.builders import InputBuilder, PersonaBuilder, PillarBuilder


class TestInputBuilder:

    def test_text_input_builder(self):

        input_builder = InputBuilder()

        text_input_definition = InputDefinition(
            private_name="text_input_test",
            type=InputType.TEXT,
        )

        input_builder.get_definition(definition=text_input_definition)

        input_builder.build()

        print(text_input_definition.asdict())
        assert isinstance(input_builder, InputBuilder)


# class TestDefinition:

#     def setup_method(self):
#         self.text_input = InputDefinition(
#             private_name="text_input_test",
#             type=InputType.TEXT,

#             )

#         self.date_input = InputDefinition(
#             private_name="date_input_test",
#             type=InputType.DATE,

#             )

#         self.range_input = InputDefinition(
#             private_name="range_input_test",
#             type=InputType.RANGE,

#             )

#         self.number_input = InputDefinition(
#             private_name="number_input_test",
#             type=InputType.NUMBER,

#             )

#         self.toggle_input = InputDefinition(
#             private_name="toggle_input_test",
#             type=InputType.TOGGLE,

#             )

#         self.multiple_alternative_input = InputDefinition(
#             private_name="multiple_alternative_input_test",
#             type=InputType.MULTI,

#             )

#         self.single_alternative_input = InputDefinition(
#             private_name="single_alternative_input_test",
#             type=InputType.SINGLE,

#             )

#         self.text_area_input = InputDefinition(
#             private_name="text_area_input_test",
#             type=InputType.TEXTA_AREA,

#             )

#         self.datetime_input = InputDefinition(
#             private_name="datetime_input_test",
#             type=InputType.DATETIME,

#             )


#         self.test_input1 = InputDefinition(
#             private_name="input1", type=InputType.TEXT, placeholder="Test"
#         )

#         self.test_input2 = InputDefinition(
#             private_name="input2",
#             type=InputType.NUMBER,
#             min_length=1,
#             max_length=10,
#         )

#         self.test_input3 = InputDefinition(private_name="input3", type=InputType.DATE)

#         self.test_input4 = InputDefinition(
#             private_name="input4",
#             type=InputType.TEXTA_AREA,
#         )

#         self.test_persona1 = PersonaDefinition(
#             public_name="Persona 1",
#             private_name="persona1",
#             role="This persona has the role to test the first persona definition creation",
#             habit_description="About the habit of testing the persona1",
#             inputs=[
#                 self.test_input1,
#                 self.test_input2,
#             ],
#         )
#         self.test_persona2 = PersonaDefinition(
#             public_name="Persona 2",
#             private_name="persona2",
#             role="This persona has the role to test the second persona definition creation",
#             habit_description="About the habit of testing the persona2",
#             inputs=InputCluster(
#                 is_recursive=True,
#                 inputs_list=[
#                     self.test_input3,
#                     self.test_input4,
#                 ],
#             ),
#         )

#         self.test_pillar = PillarDefinition(
#             public_name="Pillar 1",
#             private_name="pillar1",
#             description="This pillar is the pillar responsible for testing the module definition",
#             personas=[self.test_persona1, self.test_persona2],
#         )


# class TestInputDefinition(TestDefinition):

#     def test_input_definition_creation(self):
#         expected_input1_test_dict = {
#             "private_name": "input1",
#             "type": "text",
#             "options": None,
#             "placeholder": "Test",
#             "min_length": None,
#             "max_length": None,
#             "label": None,
#             "public_name": None,
#             "output_formatting": None,
#             "persona": "persona1",
#             "pillar": "pillar1",
#             "input_fullname": "pillar1_persona1_input1",
#             "optional": False,
#             "columns": None,
#             "rows": None,
#         }

#         assert isinstance(self.test_input1, InputDefinition)
#         assert self.test_input1.asdict() == expected_input1_test_dict


# class TestPersonaDefinition(TestDefinition):

#     def test_persona_definition_creation(self):
#         expected_persona1_test_dict = {
#             "public_name": "Persona 1",
#             "private_name": "persona1",
#             "role": "This persona has the role to test the first persona definition creation",
#             "habit_description": "About the habit of testing the persona1",
#             "inputs": [
#                 {
#                     "private_name": "input1",
#                     "type": "text",
#                     "options": None,
#                     "placeholder": "Test",
#                     "min_length": None,
#                     "max_length": None,
#                     "label": None,
#                     "public_name": None,
#                     "output_formatting": None,
#                     "persona": "persona1",
#                     "pillar": "pillar1",
#                     "input_fullname": "pillar1_persona1_input1",
#                     "optional": False,
#                     "columns": None,
#                     "rows": None,
#                 },
#                 {
#                     "private_name": "input2",
#                     "type": "number",
#                     "options": None,
#                     "placeholder": None,
#                     "min_length": 1,
#                     "max_length": 10,
#                     "label": None,
#                     "public_name": None,
#                     "output_formatting": None,
#                     "persona": "persona1",
#                     "pillar": "pillar1",
#                     "input_fullname": "pillar1_persona1_input2",
#                     "optional": False,
#                     "columns": None,
#                     "rows": None,
#                 },
#             ],
#             "outputs": None,
#             "pillar": "pillar1",
#             "persona_fullname": "pillar1_persona1",
#         }

#         print(self.test_persona1.asdict())
#         assert isinstance(self.test_persona1, PersonaDefinition)
#         assert self.test_persona1.asdict() == expected_persona1_test_dict

#     def test_persona_definition_fullname(self):
#         assert self.test_persona1.persona_fullname == "pillar1_persona1"

#     def test_persona_definition_inputs_list(self):
#         assert isinstance(self.test_persona1.inputs_list, list)
#         assert all(
#             isinstance(input, InputDefinition)
#             for input in self.test_persona1.inputs_list
#         )

#         assert isinstance(self.test_persona2.inputs_list, list)
#         assert all(
#             isinstance(input, InputDefinition)
#             for input in self.test_persona2.inputs_list
#         )


# class TestPillarDefinition(TestDefinition):

#     def test_set_persona(self):
#         assert self.test_input1.persona == "persona1"
#         assert self.test_input2.persona == "persona1"
#         assert self.test_input3.persona == "persona2"
#         assert self.test_input4.persona == "persona2"

#     def test_set_pillar(self):
#         assert self.test_persona1.pillar == "pillar1"
#         assert self.test_persona2.pillar == "pillar1"
#         assert self.test_input1.pillar == "pillar1"
#         assert self.test_input2.pillar == "pillar1"
#         assert self.test_input3.pillar == "pillar1"
#         assert self.test_input4.pillar == "pillar1"

#     def test_set_fullname(self):
#         assert self.test_persona1.persona_fullname == "pillar1_persona1"
#         assert self.test_persona2.persona_fullname == "pillar1_persona2"
#         assert self.test_input1.input_fullname == "pillar1_persona1_input1"
#         assert self.test_input2.input_fullname == "pillar1_persona1_input2"
#         assert self.test_input3.input_fullname == "pillar1_persona2_input3"
#         assert self.test_input4.input_fullname == "pillar1_persona2_input4"
