import copy
import re
import pandas as pd
from tqdm import tqdm
import numpy as np
from utils.helper import table2string
from .extract_step import return_incorrect_max_step
from collections import defaultdict
import pickle
import os

import multiprocessing as mp

from operations import *

from tools import critic_exec_one_sample, judge_exec_one_sample, tree_exec_one_sample, update_error_tree


def fixed_chain_exec_mp(llm, init_samples, n_proc=10, chunk_size=50):
    final_result = None

    chain_header = copy.deepcopy(init_samples)

    chain_header = conduct_single_solver_mp(
        llm=llm,
        all_samples=chain_header,
        tqdm_tag="Refine query",
        n_proc=n_proc,
        chunk_size=chunk_size
    )

    final_result = chain_header

    return final_result



def _conduct_single_solver_mp_core(arg):
    idx, sample, llm = arg
    try:

        if sample['conclusion'] == '[Correct]':
            return idx, sample
        else:
            incorrect_step, max_step = return_incorrect_max_step(sample)
            if incorrect_step != max_step:      # Error occurred while dynamically generating table
                table_info = get_table_info(
                    sample,
                    skip_op=[],
                    first_n_op=None,
                )
                proc_sample = simple_query(sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=200, per_example_top_p=1.0))
            else:                              # Error occurred while making the final query
                wo_query_sample = copy.deepcopy(sample)
                wo_query_sample['chain'] = wo_query_sample['chain'][:-1]
                table_info = get_table_info(
                    wo_query_sample,
                    skip_op=[],
                    first_n_op=None,
                )
                proc_sample = simple_query_with_critic(sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=200, per_example_top_p=1.0))

        return idx, proc_sample
    except Exception as e:
        print(f"Error in {idx}-th sample: {e}")
        return idx, None


def conduct_single_solver_mp(
    llm, all_samples, tqdm_tag=None, n_proc=10, chunk_size=50
):
    result_samples = [None for _ in range(len(all_samples))]

    args = [
        (idx, sample, llm)
        for idx, sample in enumerate(all_samples)
    ]

    with mp.Pool(n_proc) as p:
        for idx, proc_sample in tqdm(
            p.imap_unordered(_conduct_single_solver_mp_core, args, chunksize=chunk_size),
            total=len(all_samples),
            desc=tqdm_tag,
        ):
            result_samples[idx] = proc_sample

    return result_samples


def get_act_func(name):
    try:
        return eval(f"{name}_act")
    except:

        def _default_act(table_text, *args, **kwargs):
            return copy.deepcopy(table_text)

        if "query" not in name:
            print("Unknown operation: ", name)
        return _default_act


def get_table_info(sample, skip_op=[], first_n_op=None):
    table_text = sample["table_text"]
    chain = sample["chain"]

    if first_n_op is not None:
        chain = chain[:first_n_op]

    table_info = {
        "table_text": table_text,
        "act_chain": [],
    }

    for operation in chain:
        operation_name = operation["operation_name"]
        act_func = get_act_func(operation_name)
        table_info = act_func(table_info, operation, skip_op=skip_op)

    return table_info

def get_critic_table_info(sample, incorrect_step, skip_op=[], first_n_op=None):
    table_text = sample["table_text"]
    chain = sample["chain"]

    if first_n_op is not None:
        chain = chain[:first_n_op]

    table_info = {
        "table_text": table_text,
        "act_chain": [],
    }
    pre_table_info = copy.deepcopy(table_info)

    step = 0
    actual_step = 0
    for operation in chain:
        actual_step += 1
        operation_name = operation["operation_name"]
        pre_table_info = copy.deepcopy(table_info)
        act_func = get_act_func(operation_name)
        table_info = act_func(table_info, operation, skip_op=skip_op)
        if table_info['act_chain'] and "skip" not in table_info['act_chain'][-1]:
            step += 1
            if step == incorrect_step:
                sample['chain'] = sample['chain'][:actual_step-1]
                return pre_table_info, table_info
        

    return pre_table_info, table_info



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
            table_info['act_chain'][-1] = table_info['_real_select_rows']
        if 'query' in operation_name:
            table_info['act_chain'].append(f'{operation_name}()')
            table_info['cotable_result'] = operation['parameter_and_conf'][0][0]
        table_log.append(table_info)

    return table_log


# Dynmiac Chain Func


plan_add_column_demo = """If the table does not have the needed column to answer the quesion, we use f_add_column() to add a new column for it. For example,
/*
col : rank | lane | player | time
row 1 :  | 5 | olga tereshkova (kaz) | 51.86
row 2 :  | 6 | manjeet kaur (ind) | 52.17
row 3 :  | 3 | asami tanno (jpn) | 53.04
*/
Question: how many athletes come from Japan?
Function: f_add_column(country of athlete)
Explanation: The question asks about the number of athletes from japan. Each row is about one athlete. We need to know the country of each athlete. We extract the value from column "Player" and create a different column "Country of athletes" for each row. The datatype is String."""

plan_select_column_demo = """If the table only needs a few columns to answer the question, we use f_select_column() to select these columns for it. For example,
/*
col : code | county | former province | area (km2) | population | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/
Question: What is its exact population of momasa？
Function: f_select_column(county, population)
Explanation: The question is asking to know the exact population figure of Mombasa. We need to look at the "county" and "population" columns to check if Mombasa meets the population criteria and to obtain its specific population value."""

plan_select_row_demo = """If the table only needs a few rows to answer the question, we use f_select_row() to select these rows for it. For example,
/*
table caption : jeep grand cherokee.
col : years | displacement | engine | power | torque
row 1 : 1999 - 2004 | 4.0l (242cid) | power tech i6 | - | 3000 rpm
row 2 : 1999 - 2004 | 4.7l (287cid) | powertech v8 | - | 3200 rpm
row 3 : 2002 - 2004 | 4.7l (287cid) | high output powertech v8 | - | -
row 4 : 1999 - 2001 | 3.1l diesel | 531 ohv diesel i5 | - | -
row 5 : 2002 - 2004 | 2.7l diesel | om647 diesel i5 | - | -
*/
Question: Which Jeep Grand Cherokee model equipped with the OM647 diesel i5 engine has the third lowest displacement value among all the listed models?
Function: f_select_row(row 1, row 4, row 5)
Explanation: The question aims to identify the specific Jeep Grand Cherokee model that has the OM647 diesel i5 engine and also determine which one among them has the third lowest displacement value."""

plan_group_column_demo = """If the question is about items with the same value and the number of these items, we use f_group_column() to group the items. For example,
/*
col : district | name | party | residence | first served
row 1 : district 1 | nelson albano | dem | vineland | 2006
row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
row 3 : district 2 | john f. amodeo | rep | margate | 2008
*/
Question: How many districts are actually democratic and which ones are they? 
Function: f_group_column(party)
Explanation: The question is asking to accurately determine the number of districts that have a democratic party affiliation and also identify those specific districts. We need to look at the "district" and "party" columns to analyze and count the number of districts where the party is "dem". """

plan_sort_column_demo = """If the question is about the order of items in a column, we use f_sort_column() to sort the items. For example,
/*
col : position | club | played | points
row 1 : 1 | malaga cf | 42 | 79
row 10 : 10 | cp merida | 42 | 59
row 3 : 3 | cd numancia | 42 | 73
*/
Question: What is the position of CD Numancia when the positions are sorted from highest (first place) to lowest (last place)?
Function: f_sort_column(position)
Explanation: The question wants to check about who in the last position. We need to know the order of position from last to front. We sort the rows according to column "position"."""

plan_full_demo_simple = """Here are examples of using the operations to answer the question.


/*
col : date | division | league | regular season | playoffs | open cup | avg. attendance
row 1 : 2001/01/02 | 2 | usl a-league | 4th, western | quarterfinals | did not qualify | 7,169
row 2 : 2002/08/06 | 2 | usl a-league | 2nd, pacific | 1st round | did not qualify | 6,260
row 5 : 2005/03/24 | 2 | usl first division | 5th | quarterfinals | 4th round | 6,028
*/
Question: what was the last year where this team was a part of the usl a-league?
Function Chain: f_add_column(year) -> f_select_row(row 1, row 2) -> f_select_column(year, league) -> f_sort_column(year) -> <END>

*/
col : rank | lane | athlete | time
row 1 : 1 | 6 | manjeet kaur (ind) | 52.17
row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86
row 3 : 3 | 4 | pinki pramanik (ind) | 53.06
*/
Question: How many athletes are actually from India?
Function Chain: f_add_column(country of athletes) -> f_select_row(row 1, row 3) -> f_select_column(athlete, country of athletes) -> f_group_column(country of athletes) -> <END>

/*
col : week | when | kickoff | opponent | results; final score | results; team record | game site | attendance
row 1 : 1 | saturday, april 13 | 7:00 p.m. | at rhein fire | w 27–21 | 1–0 | rheinstadion | 32,092
row 2 : 2 | saturday, april 20 | 7:00 p.m. | london monarchs | w 37–3 | 2–0 | waldstadion | 34,186
row 3 : 3 | sunday, april 28 | 6:00 p.m. | at barcelona dragons | w 33–29 | 3–0 | estadi olímpic de montjuïc | 17,503
*/
Question: When is the competition with highest points scored played?.
Function Chain: f_add_column(points scored) -> f_select_row(*) -> f_select_column(when, points scored) -> f_sort_column(points scored) -> <END>

/*
col : iso/iec standard | status | wg
row 1 : iso/iec tr 19759 | published (2005) | 20
row 2 : iso/iec 15288 | published (2008) | 7
row 3 : iso/iec 12207 | published (2011) | 7
*/
Question: How many standards are published in 2011
Function Chain: f_add_column(year) -> f_select_row(row 3) -> f_select_column(year) -> f_group_column(year) -> <END>

"""

possible_next_operation_dict = {
    "<init>": [
        "add_column", 
        "select_row", 
        "select_column",
        "group_column",
        "sort_column",
    ],
    "add_column": [
        "select_row",
        "select_column", 
        "group_column", 
        "sort_column",
        "<END>",
    ],
    "select_row": [
        "select_column",
        "group_column",
        "sort_column",
        "<END>",
    ],
    "select_column": [
        "group_column",
        "sort_column",
        "<END>",
    ],
    "group_column": [
        "sort_column",
        "<END>",
    ],
    "sort_column": [
        "<END>",
    ],
}


def get_operation_name(string):
    # f_xxxx(...)
    res = re.findall(r"f_(.*?)\(.*\)", string)[0]
    return res


def get_all_operation_names(string):
    operation_names = []
    parts = string.split("->")
    for part in parts:
        part = part.strip()
        if part == "<END>":
            operation_names.append("<END>")
        else:
            res = re.findall(r"f_(.*?)\(.*\)", part)
            if res:
                operation_names.append(res[0])
    return operation_names


def generate_prompt_for_next_step(
    sample,
    debug=False,
    llm=None,
    llm_options=None,
    strategy="top",
):
    table_info = get_table_info(sample)
    act_chain = table_info["act_chain"]

    if debug:
        print("Act Chain: ", act_chain, flush=True)

    kept_act_chain = [x for x in act_chain if not x.startswith("skip")]
    kept_act_chain_str = " -> ".join(kept_act_chain)
    if kept_act_chain_str:
        kept_act_chain_str += " ->"

    skip_act_chain = [x for x in act_chain if x.startswith("skip")]
    skip_act_chain_op_names = []
    for op in skip_act_chain:
        op = op[len("skip ") :]
        op_name = get_operation_name(op)
        skip_act_chain_op_names.append(op_name)

    if debug:
        print("Kept Act Chain: ", kept_act_chain, flush=True)
        print("Skip Act Chain: ", skip_act_chain, flush=True)

    last_operation = (
        "<init>" if not kept_act_chain else get_operation_name(kept_act_chain[-1])
    )
    possible_next_operations = possible_next_operation_dict[last_operation]
    possible_next_operations = [
        x for x in possible_next_operations if x not in skip_act_chain_op_names
    ]

    if debug:
        print("Last Operation: ", last_operation, flush=True)
        print("Possible Next Operations: ", possible_next_operations, flush=True)

    if len(possible_next_operations) == 1:
        return possible_next_operations[0]

    prompt = ""
    for operation in possible_next_operations:
        if operation == "<END>":
            continue
        prompt += eval(f"plan_{operation}_demo") + "\n\n"

    prompt += plan_full_demo_simple + "\n\n"

    prompt += "/*\n" + table2string(table_info["table_text"]) + "\n*/\n"
    prompt += "Question: " + sample["statement"] + "\n"

    _possible_next_operations_str = " or ".join(
        [f"f_{op}()" if op != "<END>" else op for op in possible_next_operations]
    )

    if len(possible_next_operations) > 1:
        prompt += (
            f"The next operation must be one of {_possible_next_operations_str}.\n"
        )
    else:
        prompt += f"The next operation must be {_possible_next_operations_str}.\n"

    prompt += "Function Chain: " + kept_act_chain_str

    responses = llm.generate_plus_with_score(
        prompt, options=llm_options, end_str="\n\n"
    )

    if strategy == "top":
        response = responses[0][0]
        generate_operations = get_all_operation_names(response)
        if debug:
            print('Prompt:', prompt.split("\n\n")[-1])
            print('Response:', response)
            print("Generated Operations: ", generate_operations)
        next_operation = "<END>"
        for operation in generate_operations:
            if operation in possible_next_operations:
                next_operation = operation
                break
    elif strategy == "voting":
        next_operation_conf_dict = defaultdict(float)
        for response, score in responses:
            generate_operations = get_all_operation_names(response)
            next_operation = None
            for operation in generate_operations:
                if operation in possible_next_operations:
                    next_operation = operation
                    break
            if next_operation:
                next_operation_conf_dict[next_operation] += np.exp(score)
        if len(next_operation_conf_dict) != 0:
            next_operation_conf_pairs = sorted(
                next_operation_conf_dict.items(), key=lambda x: x[1], reverse=True
            )
            next_operation = next_operation_conf_pairs[0][0]
        else:
            next_operation = "<END>"


    return next_operation


def generate_prompt_for_critic_step(
    sample,
    incorrect_step,
    max_step,
    debug=False,
    llm=None,
    llm_options=None,
    strategy="top",
):
    critique = sample['critique']
    pre_table_info, table_info = get_critic_table_info(sample, incorrect_step)
    act_chain = pre_table_info["act_chain"]

    if debug:
        print("Act Chain: ", act_chain, flush=True)


    kept_act_chain = [x for x in act_chain if not x.startswith("skip")]
    kept_act_chain_str = " -> ".join(kept_act_chain)
    if kept_act_chain_str:
        kept_act_chain_str += " ->"

    critic_act_chain = [x for x in table_info["act_chain"] if not x.startswith("skip")]
    critic_act_chain_str = " -> ".join(critic_act_chain)
    max_critic_idx = len(critic_act_chain) - 1
    critic_steps_str = ""
    for idx, act in enumerate(critic_act_chain):
        critic_steps_str += f"step {idx+1}({act})"
        if idx < max_critic_idx-1:
            critic_steps_str += ", "
        elif idx == max_critic_idx-1:
            critic_steps_str += " and "


    skip_act_chain = [x for x in act_chain if x.startswith("skip")]
    skip_act_chain_op_names = []
    for op in skip_act_chain:
        op = op[len("skip ") :]
        op_name = get_operation_name(op)
        skip_act_chain_op_names.append(op_name)

    if debug:
        print("Kept Act Chain: ", kept_act_chain, flush=True)
        print("Skip Act Chain: ", skip_act_chain, flush=True)

    last_operation = (
        "<init>" if not kept_act_chain else get_operation_name(kept_act_chain[-1])
    )
    possible_next_operations = possible_next_operation_dict[last_operation]
    possible_next_operations = [
        x for x in possible_next_operations if x not in skip_act_chain_op_names
    ]

    if debug:
        print("Last Operation: ", last_operation, flush=True)
        print("Possible Next Operations: ", possible_next_operations, flush=True)

    if len(possible_next_operations) == 1:
        parameter_prompt = ""

        parameter_prompt += "Now, we have produced part of the Function Chain, and gained a critique.\n"
        parameter_prompt += f"Function Chain: {critic_act_chain_str}\n"
        parameter_prompt += f"After {critic_steps_str}, we obtain the sub-table:\n"
        parameter_prompt += "/*\n" + table2string(table_info["table_text"]) + "\n*/\n"
        if 'group_sub_table' in table_info:
            group_column, group_info = table_info["group_sub_table"]
            parameter_prompt += "/*\n"
            parameter_prompt += "Group the rows according to column: {}.\n".format(group_column)
            group_headers = ["Group ID", group_column, "Count"]
            group_rows = []
            for i, (v, count) in enumerate(group_info):
                if v.strip() == "":
                    v = "[Empty Cell]"
                group_rows.append([f"Group {i+1}", v, str(count)])
            parameter_prompt += f"{pd.DataFrame(group_rows, columns=group_headers)}\n*/\n"
        parameter_prompt += "Question: " + sample["statement"] + "\n"
        parameter_prompt += f"Critique: \n{critique}\n\n"

        parameter_prompt += f"Based on the critique, we want to use {possible_next_operations[0]}() to reproduce step {incorrect_step}. Please generate the answer in the format of the example above.\n"

        return possible_next_operations[0], parameter_prompt

    prompt = ""
    for operation in possible_next_operations:
        if operation == "<END>":
            continue
        prompt += eval(f"plan_{operation}_demo") + "\n\n"

    prompt += plan_full_demo_simple + "\n\n"

    prompt += "Now, we have produced part of the Function Chain, but gained a critique.\n"

    prompt += f"Function Chain: {critic_act_chain_str}\n"
    prompt += f"After {critic_steps_str}, we obtain the sub-table:\n"          #### 这里需要改进，最好改成 经过step 1（...），step 2（...）and step 3（...）
    prompt += "/*\n" + table2string(table_info["table_text"]) + "\n*/\n"
    if 'group_sub_table' in table_info:
        group_column, group_info = table_info["group_sub_table"]
        prompt += "/*\n"
        prompt += "Group the rows according to column: {}.\n".format(group_column)
        group_headers = ["Group ID", group_column, "Count"]
        group_rows = []
        for i, (v, count) in enumerate(group_info):
            if v.strip() == "":
                v = "[Empty Cell]"
            group_rows.append([f"Group {i+1}", v, str(count)])
        prompt += f"{pd.DataFrame(group_rows, columns=group_headers)}\n*/\n"
    prompt += "Question: " + sample["statement"] + "\n"
    prompt += f"Critique: \n{critique}\n\n"

    prompt += "Based on the critique, please continue to produce a complete and correct Function Chain.\n"
    prompt += "/*\n" + table2string(pre_table_info["table_text"]) + "\n*/\n"
    prompt += "Question: " + sample["statement"] + "\n"

    _possible_next_operations_str = " or ".join(
        [f"f_{op}()" if op != "<END>" else op for op in possible_next_operations]
    )

    if len(possible_next_operations) > 1:
        prompt += (
            f"The next operation must be one of {_possible_next_operations_str}.\n"
        )
    else:
        prompt += f"The next operation must be {_possible_next_operations_str}.\n"

    prompt += "Function Chain: " + kept_act_chain_str
    # print(prompt)

    responses = llm.generate_plus_with_score(
        prompt, options=llm_options, end_str="\n\n"
    )

    if strategy == "top":
        response = responses[0][0]
        generate_operations = get_all_operation_names(response)
        if debug:
            print('Prompt:', prompt.split("\n\n")[-1])
            print('Response:', response)
            print("Generated Operations: ", generate_operations)
        next_operation = "<END>"
        for operation in generate_operations:
            if operation in possible_next_operations:
                next_operation = operation
                break
    elif strategy == "voting":
        next_operation_conf_dict = defaultdict(float)
        for response, score in responses:
            generate_operations = get_all_operation_names(response)
            next_operation = None
            for operation in generate_operations:
                if operation in possible_next_operations:
                    next_operation = operation
                    break
            if next_operation:
                next_operation_conf_dict[next_operation] += np.exp(score)
        if len(next_operation_conf_dict) != 0:
            next_operation_conf_pairs = sorted(
                next_operation_conf_dict.items(), key=lambda x: x[1], reverse=True
            )
            next_operation = next_operation_conf_pairs[0][0]
        else:
            next_operation = "<END>"
        
    parameter_prompt = ""

    parameter_prompt += "Now, we have produced part of the Function Chain, but gained a critique.\n"
    parameter_prompt += f"Function Chain: {critic_act_chain_str}\n"
    parameter_prompt += f"After {critic_steps_str}, we obtain the sub-table:\n"
    parameter_prompt += "/*\n" + table2string(table_info["table_text"]) + "\n*/\n"
    if 'group_sub_table' in table_info:
        group_column, group_info = table_info["group_sub_table"]
        parameter_prompt += "/*\n"
        parameter_prompt += "Group the rows according to column: {}.\n".format(group_column)
        group_headers = ["Group ID", group_column, "Count"]
        group_rows = []
        for i, (v, count) in enumerate(group_info):
            if v.strip() == "":
                v = "[Empty Cell]"
            group_rows.append([f"Group {i+1}", v, str(count)])
        parameter_prompt += f"{pd.DataFrame(group_rows, columns=group_headers)}\n*/\n"
    parameter_prompt += "Question: " + sample["statement"] + "\n"
    parameter_prompt += f"Critique: \n{critique}\n\n"

    parameter_prompt += f"Based on the critique, we want to use {next_operation}() to reproduce step {incorrect_step}. Please generate the answer in the format of the example above.\n"

    return next_operation, parameter_prompt


def dynamic_chain_exec_one_sample(
    sample,
    incorrect_step,
    max_step,
    llm,
    llm_options=None,
    strategy="top",
    debug=False,
    operation_parameter_dict=None,
):
    if operation_parameter_dict is None:
        operation_parameter_dict = {
            "add_column": (
                "addColumn",
                add_column_func,
                {},
                llm.get_model_options(
                    temperature=0.0,
                    per_example_max_decode_steps=150,
                    per_example_top_p=1.0,
                ),
            ),
            "select_row": (
                "selectRow",
                select_row_func,
                {},
                llm.get_model_options(
                    temperature=0.5,
                    per_example_max_decode_steps=150,
                    per_example_top_p=1.0,
                    n_sample=8,
                ),
            ),
            "select_column": (
                "selectColumn",
                select_column_func,
                {},
                llm.get_model_options(
                    temperature=0.5,
                    per_example_max_decode_steps=150,
                    per_example_top_p=1.0,
                    n_sample=8,
                ),
            ),
            "group_column": (
                "groupColumn",
                group_column_func,
                dict(skip_op=[]),
                llm.get_model_options(
                    temperature=0.0,
                    per_example_max_decode_steps=150,
                    per_example_top_p=1.0,
                ),
            ),
            "sort_column": (
                "sortColumn",
                sort_column_func,
                dict(skip_op=[]),
                llm.get_model_options(
                    temperature=0.0,
                    per_example_max_decode_steps=150,
                    per_example_top_p=1.0,
                ),
            ),
        }

    current_sample = copy.deepcopy(sample)


    next_operation, parameter_critic = generate_prompt_for_critic_step(
        current_sample,
        incorrect_step,
        max_step,
        llm=llm,
        llm_options=llm_options,
        strategy=strategy,
        debug=debug,
    )

    if next_operation == "<END>":
        return current_sample

    param = operation_parameter_dict[next_operation]
    op_name, solver_func, kargs, op_llm_options = param

    table_info = get_table_info(current_sample)

    current_sample = solver_func(
        current_sample, table_info, critic=parameter_critic, llm=llm, llm_options=op_llm_options, **kargs
    )


    while True:
        # generate next operation
        next_operation = generate_prompt_for_next_step(
            current_sample,
            llm=llm,
            llm_options=llm_options,
            strategy=strategy,
            debug=debug,
        )

        if debug:
            print(next_operation)

        if next_operation == "<END>":
            break

        param = operation_parameter_dict[next_operation]
        op_name, solver_func, kargs, op_llm_options = param

        table_info = get_table_info(current_sample)

        current_sample = solver_func(
            current_sample, table_info, llm=llm, llm_options=op_llm_options, **kargs
        )
    return current_sample


def dynamic_chain_exec_with_cache_for_loop(
    all_samples,
    llm,
    llm_options=None,
    strategy="voting",
    cache_dir="./cache/debug",
):
    os.makedirs(cache_dir, exist_ok=True)
    result_samples = [None for _ in range(len(all_samples))]
    dynamic_chain_log_list = [None for _ in range(len(all_samples))]

    cache_filename = "case-{}.pkl"

    def _func(idx):
        sample = all_samples[idx]
        sample_id = sample["id"]
        cache_path = os.path.join(cache_dir, cache_filename.format(sample_id))
        if os.path.exists(cache_path):
            _, proc_sample, log = pickle.load(open(cache_path, "rb"))
        else:
            proc_sample, log = dynamic_chain_exec_one_sample(
                sample, llm=llm, llm_options=llm_options, strategy=strategy
            )
            pickle.dump((sample, proc_sample, log), open(cache_path, "wb"))
        result_samples[idx] = proc_sample
        dynamic_chain_log_list[idx] = log

    for idx in tqdm(range(len(all_samples)), total=len(all_samples)):
        try:
            _func(idx)
        except Exception as e:
            print(f"IDX={idx}: {e}", flush=True)

    return result_samples, dynamic_chain_log_list


def _dynamic_chain_exec_with_cache_mp_core(arg):
    idx, sample, llm, llm_options, strategy, cache_dir = arg

    cache_filename = "case-{}.pkl"
    try:
        sample_id = sample["id"]
        cache_path = os.path.join(cache_dir, cache_filename.format(idx))
        if os.path.exists(cache_path):
            proc_sample = pickle.load(open(cache_path, "rb"))
        else:
            if sample['conclusion'] == '[Correct]':
                proc_sample = sample
            else:
                incorrect_step, max_step = return_incorrect_max_step(sample)
                if incorrect_step != max_step:      # Error occurred while dynamically generating table
                    proc_sample = dynamic_chain_exec_one_sample(
                        sample, llm=llm, incorrect_step=incorrect_step, max_step=max_step, llm_options=llm_options, strategy=strategy
                    )
                else:                              # Error occurred while making the final query
                    proc_sample = sample
            pickle.dump((proc_sample), open(cache_path, "wb"))
        return idx, proc_sample
    except Exception as e:
        print(f"Error in {sample_id}: {e}", flush=True)
        return idx, None


def dynamic_chain_exec_with_cache_mp(
    all_samples,
    llm,
    llm_options=None,
    strategy="voting",
    cache_dir="./results/debug",
    n_proc=10,
    chunk_size=50,
):
    os.makedirs(cache_dir, exist_ok=True)
    result_samples = [None for _ in range(len(all_samples))]
    args = [
        (idx, sample, llm, llm_options, strategy, cache_dir)
        for idx, sample in enumerate(all_samples)
    ]

    with mp.Pool(n_proc) as p:
        for idx, proc_sample in tqdm(
            p.imap_unordered(
                _dynamic_chain_exec_with_cache_mp_core, args, chunksize=chunk_size
            ),
            total=len(all_samples),
            desc=f"Dynamic chain execution with critique"
        ):
            result_samples[idx] = proc_sample

    return result_samples


def critic_refine_with_cache_mp(
    all_samples,
    llm,
    llm_options=None,
    strategy="voting",
    cache_dir="./results/debug",
    n_proc=10,
    chunk_size=50,
):
    os.makedirs(cache_dir, exist_ok=True)
    result_samples = [None for _ in range(len(all_samples))]
    args = [
        (idx, sample, llm, llm_options, strategy, cache_dir)
        for idx, sample in enumerate(all_samples)
    ]

    with mp.Pool(n_proc) as p:
        for idx, proc_sample in tqdm(
            p.imap_unordered(
                _critic_refine_with_cache_mp_core, args, chunksize=chunk_size
            ),
            total=len(all_samples),
            desc=f"Criticize and refine"
        ):
            result_samples[idx] = proc_sample

    return result_samples

def _critic_refine_with_cache_mp_core(arg):
    idx, sample, llm, llm_options, strategy, cache_dir = arg

    cache_filename = "case-{}.pkl"
    try:
        sample_id = sample["id"]
        cache_path = os.path.join(cache_dir, cache_filename.format(idx))
        if os.path.exists(cache_path):
            proc_sample = pickle.load(open(cache_path, "rb"))
        else:
            critic_sample = critic_exec_one_sample(sample, llm=llm, llm_options=llm_options)
            if critic_sample['conclusion'] == '[Correct]':
                proc_sample = critic_sample
            else:
                loop_count = 0
                while(critic_sample['conclusion'] != '[Correct]' and loop_count < 5):
                    incorrect_step, max_step = return_incorrect_max_step(critic_sample)
                    if incorrect_step:
                        if incorrect_step != max_step:      # Error occurred while dynamically generating table
                            refine_chain_sample = dynamic_chain_exec_one_sample(
                                critic_sample, llm=llm, incorrect_step=incorrect_step, max_step=max_step, llm_options=llm_options, strategy=strategy
                            )
                            table_info = get_table_info(
                                refine_chain_sample,
                                skip_op=[],
                                first_n_op=None,
                            )
                            proc_sample = simple_query_cot_original(refine_chain_sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=200, per_example_top_p=1.0))
                        else:
                            wo_query_sample = copy.deepcopy(sample)
                            wo_query_sample['chain'] = wo_query_sample['chain'][:-1]
                            table_info = get_table_info(
                                wo_query_sample,
                                skip_op=[],
                                first_n_op=None,
                            )
                            proc_sample = simple_query_with_critic(critic_sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=200, per_example_top_p=1.0))
                        loop_count += 1
                        critic_sample = critic_exec_one_sample(proc_sample, llm=llm, llm_options=llm_options)
                    else:
                        proc_sample = critic_sample
                        break

            pickle.dump((proc_sample), open(cache_path, "wb"))
        return idx, proc_sample
    except Exception as e:
        print(f"Error in {sample_id}: {e}", flush=True)
        return idx, None
    
def judge_critic_refine_with_cache_mp(
    all_samples,
    llm,
    llm_options=None,
    strategy="voting",
    cache_dir="./results/debug",
    n_proc=8,
    chunk_size=4,
):
    os.makedirs(cache_dir, exist_ok=True)
    result_samples = [None for _ in range(len(all_samples))]

    with mp.Manager() as manager:
        lock = manager.Lock()
        args = [
            (idx, sample, llm, llm_options, strategy, cache_dir, lock)
            for idx, sample in enumerate(all_samples)
        ]

        with mp.Pool(n_proc) as p:
            for idx, proc_sample in tqdm(
                p.imap_unordered(
                    _judge_critic_refine_with_cache_mp_core, args, chunksize=chunk_size
                ),
                total=len(all_samples),
                desc=f"Judge, criticize and refine"
            ):
                result_samples[idx] = proc_sample

    return result_samples


def _judge_critic_refine_with_cache_mp_core(arg):
    idx, sample, llm, llm_options, strategy, cache_dir, lock = arg

    cache_filename = "case-{}.pkl"
    try:
        sample_id = sample["id"]
        cache_path = os.path.join(cache_dir, cache_filename.format(idx))
        if os.path.exists(cache_path):
            proc_sample = pickle.load(open(cache_path, "rb"))
        else:
            judge_sample = judge_exec_one_sample(sample, llm=llm, llm_options=llm_options)
            judge = judge_sample['judge'].strip()
            if judge == '[Correct]':
                proc_sample = judge_sample
            else:
                loop_count = 0
                while(loop_count < 5):
                    tree_sample = tree_exec_one_sample(judge_sample, llm=llm, llm_options=llm_options)
                    routes = re.findall(r'\((.*?)\)', tree_sample['tree'])
                    if routes:
                        error_route = routes[0]
                    else:
                        error_route = "random"
                    critic_sample = critic_exec_one_sample(tree_sample, error_route, llm=llm, llm_options=llm_options)
                    incorrect_step, max_step = return_incorrect_max_step(critic_sample)
                    if incorrect_step:
                        if incorrect_step != max_step:      # Error occurred while dynamically generating table
                            refine_chain_sample = dynamic_chain_exec_one_sample(
                                critic_sample, llm=llm, incorrect_step=incorrect_step, max_step=max_step, llm_options=llm_options, strategy=strategy
                            )
                            table_info = get_table_info(
                                refine_chain_sample,
                                skip_op=[],
                                first_n_op=None,
                            )
                            refine_sample = simple_query_cot_original(refine_chain_sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=2048, per_example_top_p=1.0))
                        else:
                            wo_query_sample = copy.deepcopy(critic_sample)
                            wo_query_sample['chain'] = wo_query_sample['chain'][:-1]
                            table_info = get_table_info(
                                wo_query_sample,
                                skip_op=[],
                                first_n_op=None,
                            )
                            refine_sample = simple_query_with_critic(critic_sample, table_info, llm, llm_options=llm.get_model_options(temperature=0, per_example_max_decode_steps=2048, per_example_top_p=1.0))
                        loop_count += 1
                        judge_sample = judge_exec_one_sample(refine_sample, llm=llm, llm_options=llm_options)
                        judge = judge_sample['judge'].strip()
                        proc_sample = judge_sample
                        if judge == '[Correct]':
                            update_error_tree(critic_sample, error_route, error_tree_json="critic/TableQA/tools/few_shot_critic.json", llm=llm, llm_options=llm_options, lock=lock)
                            break       
                    else:
                        proc_sample = critic_sample
                        break

            pickle.dump((proc_sample), open(cache_path, "wb"))
        return idx, proc_sample
    except Exception as e:
        print(f"Error in {sample_id}: {e}", flush=True)
        return idx, None