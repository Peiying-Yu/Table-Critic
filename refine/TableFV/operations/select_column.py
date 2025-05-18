import difflib
import json
import copy
import re
import numpy as np
from utils.helper import table2df, NoIndent, MyEncoder
from pylcs import lcs

from third_party.select_column_row_prompts.select_column_row_prompts import select_column_demo


def twoD_list_transpose(arr, keep_num_rows=3):
    arr = arr[: keep_num_rows + 1] if keep_num_rows + 1 <= len(arr) else arr
    return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]


def select_column_build_prompt(table_text, statement, table_caption=None, num_rows=100):
    df = table2df(table_text, num_rows=num_rows)
    tmp = df.values.tolist()
    list_table = [list(df.columns)] + tmp
    list_table = twoD_list_transpose(list_table, len(list_table))
    if table_caption is not None:
        dic = {
            "table_caption": table_caption,
            "columns": NoIndent(list(df.columns)),
            "table_column_priority": [NoIndent(i) for i in list_table],
        }
    else:
        dic = {
            "columns": NoIndent(list(df.columns)),
            "table_column_priority": [NoIndent(i) for i in list_table],
        }
    linear_dic = json.dumps(
        dic, cls=MyEncoder, ensure_ascii=False, sort_keys=False, indent=2
    )
    prompt = "/*\ntable = " + linear_dic + "\n*/\n"
    prompt += "Statement: " + statement + ".\n"
    prompt += "similar words of the question link to columns:\n"
    return prompt


def select_column_func(sample, table_info, llm, llm_options, debug=False, num_rows=100, critic=None):
    table_text = table_info["table_text"]

    table_caption = sample["table_caption"]
    statement = sample["statement"]

    prompt = "" + select_column_demo.rstrip() + "\n\n"
    if critic:
        prompt += critic
    prompt += select_column_build_prompt(
        table_text, statement, table_caption, num_rows=num_rows
    )

    responses = llm.generate_plus_with_score(prompt, options=llm_options)

    if debug:
        print(prompt)
        print(responses)

    pattern_col = r"f_select_column\(\[(.*?)\]\)"

    pred_conf_dict = {}
    for res, score in responses:
        try:
            pred = re.findall(pattern_col, res, re.S)[0].strip()
        except Exception:
            continue
        pred = pred.split(", ")
        pred = [i.strip() for i in pred]
        pred = sorted(pred)
        pred = str(pred)
        if pred not in pred_conf_dict:
            pred_conf_dict[pred] = 0
        pred_conf_dict[pred] += np.exp(score)

    select_col_rank = sorted(pred_conf_dict.items(), key=lambda x: x[1], reverse=True)

    thought = "Filter out useless columns.\nsimilar words of the question link to columns:\n" + responses[0][0].split("Answer:")[0].strip() if "Answer:" in responses[0][0] else responses[0][0].strip() + "\n"
    
    operation = {
        "operation_name": "select_column",
        "parameter_and_conf": select_col_rank,
        "thought": thought,
    }

    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy


def select_column_act(table_info, operation, union_num=2, skip_op=[]):
    table_info = copy.deepcopy(table_info)

    failure_table_info = copy.deepcopy(table_info)
    failure_table_info["act_chain"].append("skip f_select_column()")

    if "select_column" in skip_op:
        return failure_table_info

    def union_lists(to_union):
        return list(set().union(*to_union))
    
    def find_most_similar(s, string_list):  
        best_match = None
        highest_similarity = 0
        for candidate in string_list:
            similarity = difflib.SequenceMatcher(None, s, candidate).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = candidate
        return best_match
    
    def match_real_column(columns, real_columns):
        match_column = []
        for c in columns:
            tmp_c = c
            most_similar_c = find_most_similar(c, real_columns)
            if most_similar_c:
                tmp_c = most_similar_c
            match_column.append(tmp_c)
        return match_column


    def twoD_list_transpose(arr):
        return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]
    

    selected_columns_info = operation["parameter_and_conf"]
    selected_columns_info = sorted(
        selected_columns_info, key=lambda x: x[1], reverse=True
    )
    selected_columns_info = selected_columns_info[:union_num]
    selected_columns = [x[0] for x in selected_columns_info]
    selected_columns = [eval(x) for x in selected_columns]
    selected_columns = union_lists(selected_columns)
    selected_columns = match_real_column(selected_columns, table_info["table_text"][0])

    real_selected_columns = []

    table_text = table_info["table_text"]
    table = twoD_list_transpose(table_text)
    new_table = []
    for cols in table:
        if cols[0].lower() in selected_columns:
            real_selected_columns.append(cols[0])
            new_table.append(copy.deepcopy(cols))
    if len(new_table) == 0:
        new_table = table
        real_selected_columns = ["*"]
    new_table = twoD_list_transpose(new_table)

    table_info["table_text"] = new_table
    table_info["act_chain"].append(
        f"f_select_column({', '.join(real_selected_columns)})"
    )

    return table_info
