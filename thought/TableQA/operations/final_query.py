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


general_cot_ = """/*
col : position | driver / passenger | equipment | bike no | points
row 1 : 1 | daniël willemsen / reto grütter | ktm - ayr | 1 | 531
row 2 : 2 | kristers sergis / kaspars stupelis | ktm - ayr | 3 | 434
row 3 : 3 | jan hendrickx / tim smeuninx | zabel - vmc | 2 | 421
row 4 : 4 | joris hendrickx / kaspars liepins | zabel - vmc | 8 | 394
row 5 : 5 | marco happich / meinrad schelbert | zabel - mefo | 7 | 317
*/
Question: What number bike is the only one to use equipment zabel - vmc?
Explanation: The bikes using the equipment "zabel - vmc" are bike numbers 2 and 8.
Answer: 2|8

/*
col : home team | home team score | away team | away team score | venue | crowd | date
row 1 : footscray | 6.6 (42) | north melbourne | 8.13 (61) | western oval | 13325 | 10 august 1957
row 2 : essendon | 10.15 (75) | south melbourne | 7.13 (55) | windy hill | 16000 | 10 august 1957
row 3 : st kilda | 1.5 (11) | melbourne | 6.13 (49) | junction oval | 17100 | 10 august 1957
row 4 : hawthorn | 14.19 (103) | geelong | 8.7 (55) | brunswick street oval | 12000 | 10 august 1957
row 5 : fitzroy | 8.14 (62) | collingwood | 8.13 (61) | glenferrie oval | 22000 | 10 august 1957
*/
Question: Which team was the away team playing at the Brunswick Street Oval venue?
Explanation: The away team playing at the Brunswick Street Oval venue was Geelong.
Answer: geelong

/*
col : year of election | candidates elected | of seats available | of votes | % of popular vote
row 1 : 1934 | 1 | 90 | na | 7.0%
row 2 : 1937 | 0 | 90 | na | 5.6%
row 3 : 1943 | 34 | 90 | na | 31.7%
row 4 : 1945 | 8 | 90 | na | 22.4%
row 5 : 1948 | 21 | 90 | na | 27.0%
*/
Question: How much lower was the popular vote in the 1937 election compared to that of the 1943 election?
Explanation: In the 1937 and 1943 elections, the popular vote percentage in 1937 was 5.6%, while in 1943 it was 31.7%. By subtracting the 1937 percentage from the 1943 percentage, we find that the popular vote in the 1937 election was 26.1% lower than in the 1943 election.
Answer: 26.1%
"""

general_cot = """Example 1:
/*
col   : opponent  score
row 1 : vs. bc lions  29-16
row 2 : at bc lions  29-19
*/
Question: how many total points did the bombers score against the bc lions?
Explanation: The Bombers scored 29 points in the first game and 29 points in the second game against the BC Lions. By adding these scores together, the total points scored by the Bombers against the BC Lions is 58.
Answer: 58

Example 2:
/*
col   : election | % of\npopular votes
row 1 : 2003     | 44.67               
row 2 : 2007     | 39.15               
row 3 : 2011     | 39.34               
*/
Question: which elections reached over 39% of the popular vote?
Explanation: The 2003 election had a popular vote percentage of 44.67%, which is above 39%. The 2007 election also exceeded 39% with a popular vote percentage of 39.15%. The 2011 election also had a percentage of 39.34%, which is slightly above 39%. Therefore, the 2003， 2007 and 2011 elections reached over 39% of the popular vote.
Answer: 2003|2007|2011

Example 3:
/*
col   :  home team score
row 1 :  4
row 2 :  2
row 3 :  1
row 4 :  1
row 5 :  2
row 6 :  3
row 7 :  1
row 8 :  0
*/
Question: what is the average score of all home team members for all dates?
Explanation: The average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 14 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 1.75.
Answer: 1.75

Example 4:
/*
col   : nickname   |  rugby\nsince
row 1 : terrapins   |    1963
*/
Question: when was the first year of rugby of the terrapins?
Explanation: The first year of rugby for the Terrapins was 1963. 
Answer: 1963

Example 5:
/*
col   : attendance
row 1 : 847
row 2 : 437
row 3 : 932
row 4 : 863
row 5 : 456
row 6 : 971
*/
Question: how many games attendance was under 1000?
Explanation: Based on the extracted sub-table, the attendance for the games was 847, 437, 932, 863, 456, and 971. All of these games had an attendance under 1000. Therefore, the answer is that 6 games had an attendance of less than 1000.
Answer: 6


"""

general_demo = """/*
col : position | driver / passenger | equipment | bike no | points
row 1 : 1 | daniël willemsen / reto grütter | ktm - ayr | 1 | 531
row 2 : 2 | kristers sergis / kaspars stupelis | ktm - ayr | 3 | 434
row 3 : 3 | jan hendrickx / tim smeuninx | zabel - vmc | 2 | 421
row 4 : 4 | joris hendrickx / kaspars liepins | zabel - vmc | 8 | 394
row 5 : 5 | marco happich / meinrad schelbert | zabel - mefo | 7 | 317
*/
Question: What number bike is the only one to use equipment zabel - vmc?
Answer: 2|8

/*
col : home team | home team score | away team | away team score | venue | crowd | date
row 1 : footscray | 6.6 (42) | north melbourne | 8.13 (61) | western oval | 13325 | 10 august 1957
row 2 : essendon | 10.15 (75) | south melbourne | 7.13 (55) | windy hill | 16000 | 10 august 1957
row 3 : st kilda | 1.5 (11) | melbourne | 6.13 (49) | junction oval | 17100 | 10 august 1957
row 4 : hawthorn | 14.19 (103) | geelong | 8.7 (55) | brunswick street oval | 12000 | 10 august 1957
row 5 : fitzroy | 8.14 (62) | collingwood | 8.13 (61) | glenferrie oval | 22000 | 10 august 1957
*/
Question: Which team was the away team playing at the Brunswick Street Oval venue?
Answer: geelong

/*
col : year of election | candidates elected | of seats available | of votes | % of popular vote
row 1 : 1934 | 1 | 90 | na | 7.0%
row 2 : 1937 | 0 | 90 | na | 5.6%
row 3 : 1943 | 34 | 90 | na | 31.7%
row 4 : 1945 | 8 | 90 | na | 22.4%
row 5 : 1948 | 21 | 90 | na | 27.0%
*/
Question: How much lower was the popular vote in the 1937 election compared to that of the 1943 election?
Answer: 26.1%
"""



def simple_query(sample, table_info, llm, debug=False, use_demo=False, llm_options=None):
    table_text = table_info["table_text"]

    statement = sample["statement"]

    prompt = ""
    prompt += "Here is the table to answer this question. Please understand the table and answer the question\n"
    prompt += "If you have multiple answers, you can separate them with '|'\n"

    if use_demo:
        prompt += "\nHere are some examples:\n\n"
        prompt += general_cot + "\n\n"

    prompt += "Now, process the following question:\n"
    prompt += "/*\n"
    prompt += table2string(table_text) + "\n"
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

    prompt += "Question: " + statement + "\n"

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
