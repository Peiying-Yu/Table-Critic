import copy
import json

import pandas as pd

from thought.TableFV.operations import *
from thought.TableFV.utils.helper import table2string

import random
random.seed(42)

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
    thought_log = []

    table_info = {
        "table_text": table_text,
        "act_chain": [],
    }

    table_log.append(table_info)
    thought_log.append("")

    for operation in chain:
        operation_name = operation["operation_name"]    
        act_func = get_act_func(operation_name)
        table_info = act_func(table_info, operation, skip_op=skip_op)
        if 'row' in operation_name:
            if '_select_rows' in table_info:
                table_info['act_chain'][-1] = table_info['_select_rows']
        if 'query' in operation_name:
            table_info['act_chain'].append(f'{operation_name}()')
            table_info['cotable_result'] = operation['parameter_and_conf'][0][0]
        table_log.append(table_info)
        if "thought" in operation:
            thought_log.append(operation["thought"])
        else:
            thought_log.append("")

    return table_log, thought_log

def get_terminal_nodes(input_dict):
    terminal_nodes = []
    for key, value in input_dict.items():
        if isinstance(value, dict):
            terminal_nodes.extend(get_terminal_nodes(value))
        else:
            terminal_nodes.extend(value)
    return terminal_nodes

def return_error_shot(error_route, few_shot_dict):
    if error_route != 'random':
        error_route = error_route.split('->')
        few_shot = copy.deepcopy(few_shot_dict)
        for error_type in error_route:
            error_type = error_type.strip()
            if error_type in few_shot:
                few_shot = few_shot[error_type]
                if isinstance(few_shot,list):
                    if len(few_shot) > 5:
                        few_shot = random.sample(few_shot, 5)
                    return few_shot
                
    few_shot = get_terminal_nodes(few_shot_dict)     # If it does't return correctly, then randomly choose
    few_shot = random.sample(few_shot, min(5, len(few_shot)))
    return few_shot

def replace_leaves_with_end(tree_data):
    data = copy.deepcopy(tree_data)
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_leaves_with_end(value)
    elif isinstance(data, list):
        return "<END>"
    else:
        return "<END>"
    
    return data

def get_cot_for_critic(sample):


    cot = "Now, determine which step of the table reasoning is incorrect, give a critique and give a conclusion according to the format 'Conclusion: [Incorrect] Step <NUM>': \nOriginal Table:\n/*\n"
    cot += table2string(sample['table_text']) + "\n*/\n\n"
    cot += "Statement: \n" +  sample['statement'] + "\n\n"

    cot += "Reasoning Steps:\n"

    table_log, thought_log = get_table_log(sample)

    step = 0
    action_list = []
    table_text = sample['table_text']
    for idx, table_info in enumerate(table_log[:-1]):
        if table_info["act_chain"]:
            table_action = table_info["act_chain"][-1]
            if "skip" in table_action:
                continue
            else:
                table_text = table_info["table_text"]
                action_list.append(table_action)
                cot += f"Step{step+1}: {thought_log[idx]}\n"
                cot += f"So we use {table_action}.\n\n"
                step += 1


    if len(action_list):
        cot += f"Step{step+1}: After using "
        step += 1
        max_idx = len(action_list) - 1
        for idx, act in enumerate(action_list):
            cot += act
            if idx < max_idx-1:
                cot += ", "
            elif idx == max_idx-1:
                cot += " and "
        cot += ", we obtain the sub-table:\n/*\n"
        cot += f"{table2string(table_text)}\n*/\n"
        if "group_sub_table" in table_info:
            group_column, group_info = table_info["group_sub_table"]
            cot += "/*\n"
            cot += "Group the rows according to column: {}.\n".format(group_column)
            group_headers = ["Group ID", group_column, "Count"]
            group_rows = []
            for i, (v, count) in enumerate(group_info):
                if v.strip() == "":
                    v = "[Empty Cell]"
                group_rows.append([f"Group {i+1}", v, str(count)])
            cot += " | ".join(group_headers) + "\n"
            for row in group_rows:
                cot += " | ".join(row) + "\n"
            cot += "*/\n"
    
    cot += f"{thought_log[-1]}\n\n"

    cot += "Prediction Answer: \n" + table_log[-1]["cotable_result"].lower() + "\n\n" + "Critique:"

    return cot, step

def get_cot_for_judge(sample):

    cot = "Now, determine whether the given Prediction Answer is correct or incorrect, give an explanation and give the conclusion according to the format 'Conclusion: [Correct]' or 'Conclusion: [Incorrect]': \nOriginal Table:\n/*\n"
    cot += table2string(sample['table_text']) + "\n*/\n\n"
    cot += "Statement: \n" +  sample['statement'] + "\n\n"

    table_log, thought_log = get_table_log(sample)

    cot += "Prediction Answer: \n" + table_log[-1]["cotable_result"].lower() + "\n\n" + "Explanation:"

    return cot

def get_cot_for_tree(sample):

    cot = "Now, identify which step within the reasoning process is incorrect, give an analysis and give a conclusion according to the format 'Conclusion: (ERROR ROUTE)' or 'Conclusion: [Incorrect] (random)': \n"
    
    with open("critic/TableFV/tools/few_shot_critic.json", "r") as file:
        error_tree = json.load(file)
    modified_error_tree = replace_leaves_with_end(error_tree)

    cot += f"""<error tree>
{json.dumps(modified_error_tree, indent=4, ensure_ascii=False)}

Original Table:\n/*\n"""

    cot += table2string(sample['table_text']) + "\n*/\n\n"
    cot += "Statement: \n" +  sample['statement'] + "\n\n"

    cot += "Reasoning Steps:\n"

    table_log, thought_log = get_table_log(sample)

    step = 0
    action_list = []
    table_text = sample['table_text']
    for idx, table_info in enumerate(table_log[:-1]):
        if table_info["act_chain"]:
            table_action = table_info["act_chain"][-1]
            if "skip" in table_action:
                continue
            else:
                table_text = table_info["table_text"]
                action_list.append(table_action)
                cot += f"Step{step+1}: {thought_log[idx]}\n"
                cot += f"So we use {table_action}.\n\n"
                step += 1


    if len(action_list):
        cot += f"Step{step+1}: After using "

        max_idx = len(action_list) - 1
        for idx, act in enumerate(action_list):
            cot += act
            if idx < max_idx-1:
                cot += ", "
            elif idx == max_idx-1:
                cot += " and "
        cot += ", we obtain the sub-table:\n/*\n"
        cot += f"{table2string(table_text)}\n*/\n"
        if "group_sub_table" in table_info:
            group_column, group_info = table_info["group_sub_table"]
            cot += "/*\n"
            cot += "Group the rows according to column: {}.\n".format(group_column)
            group_headers = ["Group ID", group_column, "Count"]
            group_rows = []
            for i, (v, count) in enumerate(group_info):
                if v.strip() == "":
                    v = "[Empty Cell]"
                group_rows.append([f"Group {i+1}", v, str(count)])
            cot += " | ".join(group_headers) + "\n"
            for row in group_rows:
                cot += " | ".join(row) + "\n"
            cot += "*/\n"
    
    cot += f"{thought_log[-1]}\n\n"

    cot += "Prediction Answer: \n" + table_log[-1]["cotable_result"].lower() + "\n\n" + "Analysis:"

    return cot

def get_critic_few_shot(error_route, few_shot_json= "critic_few_shot.json"):
    few_shot = "\nHere are some examples.\n\n"

    with open(few_shot_json, 'r') as f:
        few_shot_dict = json.load(f)
        selected_few_shot = return_error_shot(error_route, few_shot_dict)

    random.shuffle(selected_few_shot)

    for idx, shot in enumerate(selected_few_shot):
        few_shot += f"Example {idx+1}:\n" + shot + "\n\n\n"

    return few_shot

def get_tree_few_shot(few_shot_json= "few_shot_tree.json"):
    few_shot = "\nHere are some examples.\n\n"
    few_shot += """<error tree>
{
    "sub-table error": {
        "row error": "<END>",
        "column error": "<END>"
    },
    "final query error": "<END>"
}

"""

    with open(few_shot_json, 'r') as f:
        few_shot_dict = json.load(f)
    selected_few_shot = []
    for value in few_shot_dict.values():
        random_index = random.randint(0, len(value) - 1)
        selected_few_shot.append(value[random_index])

    random.shuffle(selected_few_shot)

    for idx, shot in enumerate(selected_few_shot):
        few_shot += f"Example {idx+1}:\n" + shot + "\n\n\n"

    return few_shot




def get_judge_few_shot(few_shot_json= "few_shot_judge.json"):
    few_shot = "\nHere are some examples.\n\n"

    with open(few_shot_json, 'r') as f:
        few_shot_dict = json.load(f)
    selected_few_shot = []
    for value in few_shot_dict.values():
        random_index = random.randint(0, len(value) - 1)
        selected_few_shot.append(value[random_index])

    # random.shuffle(selected_few_shot)

    for idx, shot in enumerate(selected_few_shot):
        few_shot += f"Example {idx+1}:\n" + shot + "\n\n\n"

    return few_shot




    

    


