from io import StringIO
from unittest import TestCase

import pandas as pd

NAVIGATOR_DATA = """date_input,element_category,element_name,book_A,read_A,listen_A,notes_A,book_B,read_B,listen_B,notes_B,user_id,schema_encoded,created_at,updated_at
2024-11-02,wisdom,navigator,Livro 1,True,False,True,Livro 4,True,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:10:54,2024-11-02 09:10:54
2024-11-01,wisdom,navigator,Livro 1,True,False,True,,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:11:27,2024-11-02 09:11:27
2024-10-31,wisdom,navigator,Livro 1,True,False,True,,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:11:49,2024-11-02 09:11:49
2024-10-30,wisdom,navigator,Livro 1,True,False,True,Livro 3,True,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:12:29,2024-11-02 09:12:29
2024-10-26,wisdom,navigator,Livro 1,True,False,True,,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:13:17,2024-11-02 09:13:17
2024-10-27,wisdom,navigator,,False,False,False,Livro 3,True,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:14:20,2024-11-02 09:14:20
2024-10-22,wisdom,navigator,Livro 2,True,False,True,Livro 3,True,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,Ym9va19BLGJvb2tfQixkYXRlX2lucHV0LGxpc3Rlbl9BLG5vdGVzX0Esbm90ZX,2024-11-02 09:15:21,2024-11-02 09:15:21
"""

DIPLOMAT_DATA = """date_input,element_category,element_name,group1,group2,group3,group4,group5,group6,user_id,schema_encoded,created_at,updated_at
2024-09-28,kindness,diplomat,False,False,False,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-09-28 08:40:04,2024-09-28 08:40:04
2024-09-29,kindness,diplomat,False,False,False,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-10-03 16:50:06,2024-10-03 16:50:06
2024-10-22,kindness,diplomat,False,False,False,False,False,True,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-10-23 05:37:36,2024-10-23 05:37:36
2024-10-18,kindness,diplomat,False,False,True,False,False,False,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-10-23 05:38:03,2024-10-23 05:38:03
2024-10-17,kindness,diplomat,False,True,False,False,False,True,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-10-23 05:41:18,2024-10-23 05:41:18
2024-10-21,kindness,diplomat,False,False,False,False,False,True,b85c3647-eeb4-47b6-ae3f-18afaca91553,YW5pbWFscyxjb250YWN0cyxjb3dvcmtlcnMsZGF0ZV9pbnB1dCxmYW1pb,2024-10-23 05:41:32,2024-10-23 05:41:32
"""


class GoldDataframeTestCase(TestCase):

    @classmethod
    def generate_mock_dataframe(cls, cleaned_table: str) -> pd.DataFrame:
        if cleaned_table == "navigator":
            data = NAVIGATOR_DATA
        elif cleaned_table == "diplomat":
            data = DIPLOMAT_DATA
        else:
            raise ValueError(f"Invalid cleaned_table: {cleaned_table}")

        df = pd.read_csv(StringIO(data))
        df["date_input"] = pd.to_datetime(df["date_input"])
        return df
