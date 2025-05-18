import re
import numpy as np
import copy
from utils.helper import table2string


group_column_demo = """To answer the question, we can use f_group_column() to group the values in a column.

/*
col : rank | lane | athlete | time | country
row 1 : 1 | 6 | manjeet kaur (ind) | 52.17 | ind
row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86 | kaz
row 3 : 3 | 4 | pinki pramanik (ind) | 53.06 | ind
row 4 : 4 | 1 | tang xiaoyin (chn) | 53.66 | chn
row 5 : 5 | 8 | marina maslyonko (kaz) | 53.99 | kaz
*/
Question: How many athletes are from Japan?
The existing columns are: rank, lane, athlete, time, country.
Explanation: The question is asking to determine the number of athletes from Japan. Since each row represents an individual athlete and the "country" column indicates the origin of each athlete, we need to group by the "country" column to check if there are any athletes from Japan. We can use the f_group_column(country) operation to group the athletes based on their country to analyze this situation.
Answer: f_group_column(country).

/*
col : district | name | party | residence | first served
row 1 : district 1 | nelson albano | dem | vineland | 2006
row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
row 3 : district 2 | john f. amodeo | rep | margate | 2008
row 4 : district 2 | chris a. brown | rep | ventnor | 2012
row 5 : district 3 | john j. burzichelli | dem | paulsboro | 2002
*/
Question: How many districts are democratic and which ones are they?
The existing columns are: district, name, party, residence, first served.
Explanation: The question is aimed at finding out the exact number of districts that have a democratic party affiliation as well as identifying those specific districts. Since each row represents information about a district and the "party" column indicates the political party of that district, we need to group by the "party" column to count and identify the democratic districts. We can use the f_group_column(party) operation to group the districts based on their party to analyze this situation.
Answer: f_group_column(party)."""


def group_column_build_prompt(table_text, statement, table_caption=None, num_rows=100):
    table_str = table2string(
        table_text, caption=table_caption, num_rows=num_rows
    ).strip()
    prompt = "/*\n" + table_str + "\n*/\n"
    prompt += "Question: " + statement + "\n"
    prompt += "The existing columns are: "
    prompt += ", ".join(table_text[0]) + ".\n"
    prompt += "Explanation: "
    return prompt


def group_column_func(
    sample, table_info, llm, llm_options=None, debug=False, skip_op=[], critic=None
):
    table_text = table_info["table_text"]

    statement = sample["statement"]
    prompt = "" + group_column_demo.rstrip() + "\n\n"
    if critic:
        prompt += critic
    prompt += group_column_build_prompt(
        table_text, statement, num_rows=5
    )
    responses = llm.generate_plus_with_score(
        prompt,
        options=llm_options,
    )

    if debug:
        print(prompt)
        print(responses)

    group_param_and_conf = {}
    group_column_and_conf = {}

    headers = table_text[0]
    rows = table_text[1:]
    for res, score in responses:
        re_result = re.findall(r"f_group_column\(([^\)]*)\)", res, re.S)

        if debug:
            print("Re result: ", re_result)

        try:
            group_column = re_result[0].strip()
            assert group_column in headers
        except:
            continue

        if group_column not in group_column_and_conf:
            group_column_and_conf[group_column] = 0
        group_column_and_conf[group_column] += np.exp(score)

    for group_column, conf in group_column_and_conf.items():
        group_column_contents = []
        index = headers.index(group_column)
        for row in rows:
            group_column_contents.append(row[index])

        def check_if_group(vs):
            vs_without_empty = [v for v in vs if v.strip()]
            if len(vs_without_empty):
                return len(set(vs_without_empty)) / len(vs_without_empty) <= 0.8
            else:
                return False

        if not check_if_group(group_column_contents):
            continue

        vs_to_group = []
        for i in range(len(group_column_contents)):
            vs_to_group.append((group_column_contents[i], i))

        group_info = []
        for v in sorted(set(group_column_contents)):
            group_info.append((v, group_column_contents.count(v)))
        group_info = sorted(group_info, key=lambda x: x[1], reverse=True)

        group_key = str((group_column, group_info))
        group_param_and_conf[group_key] = conf

    group_param_and_conf_list = sorted(
        group_param_and_conf.items(), key=lambda x: x[1], reverse=True
    )

    thought = responses[0][0].split("Answer:")[0].strip() if "Answer:" in responses[0][0] else responses[0][0].strip() + "\n"
    
    operation = {
        "operation_name": "group_column",
        "parameter_and_conf": group_param_and_conf_list,
        "thought": thought,
    }

    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy


def group_column_act(table_info, operation, strategy="top", skip_op=[]):
    table_info = copy.deepcopy(table_info)

    failure_table_info = copy.deepcopy(table_info)
    failure_table_info["act_chain"].append("skip f_group_column()")

    if "group_column" in skip_op:
        return failure_table_info
    if len(operation["parameter_and_conf"]) == 0:
        return failure_table_info
    if strategy == "top":
        group_column, group_info = eval(operation["parameter_and_conf"][0][0])
    else:
        raise NotImplementedError()

    table_info["group_sub_table"] = (group_column, group_info)
    table_info["act_chain"].append(f"f_group_column({group_column})")

    return table_info
