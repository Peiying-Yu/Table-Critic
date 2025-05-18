import copy
import numpy as np
from utils.helper import table2string

from operations import *

def get_act_func(name):
    try:
        return eval(f"{name}_act")
    except:

        def _default_act(table_text, *args, **kwargs):
            return copy.deepcopy(table_text)

        if "query" not in name:
            print("Unknown operation: ", name)
        return _default_act

def get_table_log(sample, skip_op=[], first_n_op=None):
    table_text = sample["table_text"]
    chain = sample["chain"]

    if first_n_op is not None:
        chain = chain[:first_n_op]

    table_log = []

    table_info = {
        "table_text": table_text,
        "act_chain": [],
    }
    table_log.append(table_info)

    for operation in chain:
        operation_name = operation["operation_name"]    
        act_func = get_act_func(operation_name)
        table_info = act_func(table_info, operation, skip_op=skip_op)
        if 'row' in operation_name:
            if '_select_rows' in table_info:
                table_info['act_chain'][-1] = table_info['_select_rows']
        table_log.append(table_info)

    return table_log

cot_prompt = """**Function Definitions**
1. f_add_column(): Adds a new column to the table.
2. f_select_row(): Selects specific rows based on the statement.
3. f_select_column(): Removes irrelevant columns from the table.
4. f_group_column(): Groups rows based on the values in a specific column.
5. f_sort_column():  Sorts rows based on the values in a specified column.

**Instructions*
I will use the functions defined above to process and manipulate the original table. Your task is to tell whether the statement is true or false based on the extraction process and the resulting sub-table. If the statement is true, answer YES, and otherwise answer NO.
When answering, provide an explanation first.
"""

cot_demo = """Example 1:
Statement:
bombers scored a total of 58 points against the BC Lions.
Extraction process:
f_select_row(row 5, row 9) -> f_select_column(opponent, score)
Resulting sub-table:
/*
col   : opponent  score
row 1 : vs. bc lions  29-16
row 2 : at bc lions  29-19
*/
Explanation: The Bombers scored 29 points in the first game and 29 points in the second game against the BC Lions. By adding these scores together, the total points scored by the Bombers against the BC Lions is 58. So the statement is true.
Answer: YES

Example 2:
Statement:
the election of 2007 was the first to reach over 40% of the popular vote
Extraction process:
f_select_row(row 5) -> f_select_column(election, % of popular votes)
Resulting sub-table:
/*
col   : election | % of\npopular votes
row 1 : 2003     | 44.67                            
*/
Explanation: The 2003 election had a popular vote percentage of 44.67%, which is above 40%. Therefore, the 2003 elections reached over 40% of the popular vote. So the statement is false.
Answer: NO

Example 3:
Statement:
the average score of all home team members for all dates is 2.25
Extraction process:
f_add_column(home team score) -> f_select_column(home team score)
Resulting sub-table:
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
Explanation: The average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 14 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 1.75. So the statement is false.
Answer: NO

Example 4:
Statement: 
the first year of rugby of the terrapins is 1963.
Extraction process:
f_select_row(row 2) -> f_select_column(nickname, rugby\nsince)
Resulting sub-table:
/*
col   : nickname   |  rugby\nsince
row 1 : terrapins   |    1963
*/
Explanation: The first year of rugby for the Terrapins was 1963. So the statement is true.
Answer: YES

Example 5:
Statement:
4 games attendance was under 1000
Extraction process:
f_select_row(row 1, row 2, row 3, row 4, row 6, row 7) -> f_select_column(attendance)
Resulting sub-table:
/*
col   : attendance
row 1 : 847
row 2 : 437
row 3 : 932
row 4 : 863
row 5 : 456
row 6 : 971
*/
Explanation: Based on the extracted sub-table, the attendance for the games was 847, 437, 932, 863, 456, and 971. All of these games had an attendance under 1000. Answer that 6 games had an attendance of less than 1000. So the statement is false.
Answer: NO
"""



general_cot = """Example 1:
/*
col   : opponent  score
row 1 : vs. bc lions  29-16
row 2 : at bc lions  29-19
*/
Statement: bombers scored a total of 58 points against the BC Lions.
Explanation: The Bombers scored 29 points in the first game and 29 points in the second game against the BC Lions. By adding these scores together, the total points scored by the Bombers against the BC Lions is 58. So the statement is true.
Answer: YES

Example 2:
/*
col   : election | % of\npopular votes
row 1 : 2003     | 44.67                           
*/
Statement: the election of 2007 was the first to reach over 40% of the popular vote
Explanation: The 2003 election had a popular vote percentage of 44.67%, which is above 40%. Therefore, the 2003 elections reached over 40% of the popular vote. So the statement is false.
Answer: NO

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
Statement: the average score of all home team members for all dates is 2.25
Explanation: The average score of all home team members for all dates can be calculated by adding all the scores together and dividing by the number of rows. The sum of all scores is 14 (4+2+1+1+2+3+1+0) and there are 8 rows. Therefore, the average score is 1.75. So the statement is false.
Answer: NO

Example 4:
/*
col   : nickname   |  rugby\nsince
row 1 : terrapins   |    1963
*/
Statement: the first year of rugby of the terrapins is 1963.
Explanation: The first year of rugby for the Terrapins was 1963. So the statement is true.
Answer: YES

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
Statement: 4 games attendance was under 1000
Explanation: Based on the extracted sub-table, the attendance for the games was 847, 437, 932, 863, 456, and 971. All of these games had an attendance under 1000. Therefore, the answer is that 6 games had an attendance of less than 1000. So the statement is false.
Answer: NO


"""


def simple_query_with_critic(sample, table_info, llm, debug=False, use_demo=True, llm_options=None):
    table_text = table_info["table_text"]

    caption = sample["table_caption"]
    statement = sample["statement"]

    critic_act_chain = [x for x in table_info["act_chain"] if not x.startswith("skip")]
    max_critic_idx = len(critic_act_chain) - 1
    critic_steps_str = ""
    for idx, act in enumerate(critic_act_chain):
        critic_steps_str += f"step {idx+1}({act})"
        if idx <= max_critic_idx-1:
            critic_steps_str += ", "
    if max_critic_idx >= 0:
        critic_steps_str += f" and step {max_critic_idx+2}(simple_query())"
    else:
        critic_steps_str += f"step {max_critic_idx+2}(simple_query())"

    critique = sample['critique']

    prompt = ""
    prompt += "Here is the statement about the table and the task is to tell whether the statement is true or false.\n"
    prompt += "If the statement is true, answer YES, and otherwise answer NO.\n"

    if use_demo:
        prompt += "\nHere are some examples:\n\n"
        prompt += cot_demo + "\n\n"
    

    prompt += "Now, we have judged a statement based on a table, but gained a critique.\n"

    prompt += f"After {critic_steps_str}, we obtain the sub-table and the answer:\n"
    prompt += "/*\n" + table2string(table_text, caption=caption) + "\n*/\n"
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
    prompt += "Answer: " + sample["chain"][-1]["parameter_and_conf"][0][0] + "\n"
    prompt += f"Critique: \n{critique}\n\n"
    

    prompt += "Based on the critique, please reproduce the explanation and answer.\n"


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
    sample_copy["chain"][-1] = operation

    return sample_copy



def simple_query_cot_original(sample, table_info, llm, debug=False, use_demo=True, llm_options=None):
    original_table_text = sample["table_text"]
    table_text = table_info["table_text"]

    caption = sample["table_caption"]
    statement = sample["statement"]

    extraction_process = ""
    cotable_log = get_table_log(sample)
    if cotable_log:
        for table_info in cotable_log:
            if table_info["act_chain"]:
                table_text = table_info["table_text"]
                table_action = table_info["act_chain"][-1]
                if "skip" in table_action:
                    continue
                else:
                    if extraction_process:
                        extraction_process += f" -> {table_action}"
                    else:
                        extraction_process = f"{table_action}"
    else:
        extraction_process = "None"

    prompt = ""

    prompt += cot_prompt +"\n\n"

    if use_demo:

        prompt += "Here are some examples.\n\n"
        prompt += cot_demo + "\n\n"
    
    prompt += "Now, tell whether the statement below is true or false. If the statement is true, answer YES, and otherwise answer NO.\n"
    prompt += "\n"

    prompt += "Statement: \n" + statement + "\n"

    prompt += "Extraction process:\n"
    prompt += extraction_process + "\n"

    prompt += "Resulting sub-table:\n"
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