# Copyright 2024 The Chain-of-Table authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
import numpy as np
from utils.helper import table2string


general_cot = """Example 1:
table caption : 2008 sidecarcross world championship.
col : position | driver / passenger | equipment | bike no | points
row 1 : 1 | daniël willemsen / reto grütter | ktm - ayr | 1 | 531
row 2 : 2 | kristers sergis / kaspars stupelis | ktm - ayr | 3 | 434
row 3 : 3 | jan hendrickx / tim smeuninx | zabel - vmc | 2 | 421
row 4 : 4 | joris hendrickx / kaspars liepins | zabel - vmc | 8 | 394
row 5 : 5 | marco happich / meinrad schelbert | zabel - mefo | 7 | 317
*/
Statement: bike number 3 is the only one to use equipment ktm - ayr.
Explanation: Bike number 3 (driven by Kristers Sergis and Kaspars Stupelis) is not the only one using KTM - AYR equipment. In the table, both the first and second-place finishers (Daniël Willemsen / Reto Grütter and Kristers Sergis / Kaspars Stupelis) use KTM - AYR equipment. Therefore, bike number 3 is not the only one with this equipment; bike number 1 also has it.
Answer: NO

Example 2:
/*
table caption : 1957 vfl season.
col : home team | home team score | away team | away team score | venue | crowd | date
row 1 : footscray | 6.6 (42) | north melbourne | 8.13 (61) | western oval | 13325 | 10 august 1957
row 2 : essendon | 10.15 (75) | south melbourne | 7.13 (55) | windy hill | 16000 | 10 august 1957
row 3 : st kilda | 1.5 (11) | melbourne | 6.13 (49) | junction oval | 17100 | 10 august 1957
row 4 : hawthorn | 14.19 (103) | geelong | 8.7 (55) | brunswick street oval | 12000 | 10 august 1957
row 5 : fitzroy | 8.14 (62) | collingwood | 8.13 (61) | glenferrie oval | 22000 | 10 august 1957
*/
Statement: collingwood was the away team playing at the brunswick street oval venue.
Explanation: In the table, Collingwood played at Glenferrie Oval against Fitzroy. So Collingwood was not the away team playing at the Brunswick Street Oval venue. 
Answer: NO

Example 3:
/*
table caption : co - operative commonwealth federation (ontario section).
col : year of election | candidates elected | of seats available | of votes | % of popular vote
row 1 : 1934 | 1 | 90 | na | 7.0%
row 2 : 1937 | 0 | 90 | na | 5.6%
row 3 : 1943 | 34 | 90 | na | 31.7%
row 4 : 1945 | 8 | 90 | na | 22.4%
row 5 : 1948 | 21 | 90 | na | 27.0%
*/
Statement: the 1937 election had a % of popular vote that was 1.4% lower than that of the 1959 election.
Explanation: There is no data provided for the 1959 election in the table. The table only includes election results from 1934, 1937, 1943, 1945, and 1948. Without the 1959 election data, it is impossible to compare the popular vote percentage from 1937 to that of the 1959 election, making the statement incorrect.
Answer: NO

Example 4:
/*
table caption : 2003 pga championship.
col : place | player | country | score | to par
row 1 : 1 | shaun micheel | united states | 69 + 68 = 137 | - 3
row 2 : t2 | billy andrade | united states | 67 + 72 = 139 | - 1
row 3 : t2 | mike weir | canada | 68 + 71 = 139 | - 1
row 4 : 4 | rod pampling | australia | 66 + 74 = 140 | e
row 5 : t5 | chad campbell | united states | 69 + 72 = 141 | + 1
*/
Statement: chad campbell was one of five players with + 1 to par , all of which had placed t5.
Explanation: The player with the score of +1 to par who placed in the t5 position is Chad Campbell. The statement also implies that there were five players with a +1 to par score, which matches the position of Chad Campbell at t5. However, since there are no other players listed with +1 in the table, this makes the statement correct, albeit with a slight misinterpretation of the number of players tied at t5. There’s only one player (Chad Campbell) at +1, but the phrasing could be seen as describing that Chad Campbell placed at t5 with +1 to par.
Answer: YES
"""

general_demo = """Example 1:
table caption : 2008 sidecarcross world championship.
col : position | driver / passenger | equipment | bike no | points
row 1 : 1 | daniël willemsen / reto grütter | ktm - ayr | 1 | 531
row 2 : 2 | kristers sergis / kaspars stupelis | ktm - ayr | 3 | 434
row 3 : 3 | jan hendrickx / tim smeuninx | zabel - vmc | 2 | 421
row 4 : 4 | joris hendrickx / kaspars liepins | zabel - vmc | 8 | 394
row 5 : 5 | marco happich / meinrad schelbert | zabel - mefo | 7 | 317
*/
Statement: bike number 3 is the only one to use equipment ktm - ayr.
Answer: NO

Example 2:
/*
table caption : 1957 vfl season.
col : home team | home team score | away team | away team score | venue | crowd | date
row 1 : footscray | 6.6 (42) | north melbourne | 8.13 (61) | western oval | 13325 | 10 august 1957
row 2 : essendon | 10.15 (75) | south melbourne | 7.13 (55) | windy hill | 16000 | 10 august 1957
row 3 : st kilda | 1.5 (11) | melbourne | 6.13 (49) | junction oval | 17100 | 10 august 1957
row 4 : hawthorn | 14.19 (103) | geelong | 8.7 (55) | brunswick street oval | 12000 | 10 august 1957
row 5 : fitzroy | 8.14 (62) | collingwood | 8.13 (61) | glenferrie oval | 22000 | 10 august 1957
*/
Statement: collingwood was the away team playing at the brunswick street oval venue.
Answer: NO

Example 3:
/*
table caption : co - operative commonwealth federation (ontario section).
col : year of election | candidates elected | of seats available | of votes | % of popular vote
row 1 : 1934 | 1 | 90 | na | 7.0%
row 2 : 1937 | 0 | 90 | na | 5.6%
row 3 : 1943 | 34 | 90 | na | 31.7%
row 4 : 1945 | 8 | 90 | na | 22.4%
row 5 : 1948 | 21 | 90 | na | 27.0%
*/
Statement: the 1937 election had a % of popular vote that was 1.4% lower than that of the 1959 election.
Answer: NO

Example 4:
/*
table caption : 2003 pga championship.
col : place | player | country | score | to par
row 1 : 1 | shaun micheel | united states | 69 + 68 = 137 | - 3
row 2 : t2 | billy andrade | united states | 67 + 72 = 139 | - 1
row 3 : t2 | mike weir | canada | 68 + 71 = 139 | - 1
row 4 : 4 | rod pampling | australia | 66 + 74 = 140 | e
row 5 : t5 | chad campbell | united states | 69 + 72 = 141 | + 1
*/
Statement: chad campbell was one of five players with + 1 to par , all of which had placed t5.
Answer: YES
"""



def simple_query(sample, table_info, llm, debug=False, use_demo=False, llm_options=None):
    table_text = table_info["table_text"]

    caption = sample["table_caption"]
    statement = sample["statement"]

    prompt = ""
    prompt += "Here is the statement about the table and the task is to tell whether the statement is true or false.\n"
    prompt += "If the statement is true, answer YES, and otherwise answer NO.\n"

    if use_demo:
        prompt += "\nHere are some examples:\n\n"
        prompt += general_cot + "\n\n"

    prompt += "Now, tell whether the statement below is true or false. If the statement is true, answer YES, and otherwise answer NO:\n"
    prompt += "/*\n"
    prompt += table2string(table_text, caption=caption) + "\n"
    prompt += "*/\n"

    if "group_sub_table" in table_info:
        group_column, group_info = table_info["group_sub_table"]
        prompt += "/*\n"
        prompt += "Group the rows according to column: {}.\n".format(group_column)
        group_headers = ["Group ID", group_column, "Count"]
        group_rows = []
        for i, (v, count) in enumerate(group_info):
            if v.strip() == "":
                v = "[Empty Cell]"
            group_rows.append([f"Group {i+1}", v, str(count)])
        prompt += " | ".join(group_headers) + "\n"
        for row in group_rows:
            prompt += " | ".join(row) + "\n"
        prompt += "*/\n"

    prompt += "Statement: " + statement + "\n"

    prompt += "Explanation: "
    responses = llm.generate_plus_with_score(prompt, options=llm_options)

    for res, score in responses:
        responses_list = [(res.split("Answer:")[1].strip(), np.exp(score)) if "Answer:" in res else (res.strip(), np.exp(score))]

    if debug:
        print(prompt)
        print(responses)

    thought = responses[0][0].split("Answer:")[0].strip() if "Answer:" in responses[0][0] else responses[0][0].strip() + "\n"

    
    operation = {
        "operation_name": "simple_query",
        "parameter_and_conf": responses_list,
        "thought": thought,
    }
    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy