import copy
import json
import multiprocessing as mp
import os
import pickle
from tqdm import tqdm
from .get_info import get_cot_for_critic, get_cot_for_judge, get_cot_for_tree, get_critic_few_shot, get_judge_few_shot, get_tree_few_shot
from .instruction import critic_instruction, tree_instruction, judge_instruction


def get_critique_with_mp(
    all_samples,
    llm,
    llm_options=None,
    cache_dir="./results/debug",
    n_proc=10,
    chunk_size=5,
):
    os.makedirs(cache_dir, exist_ok=True)
    
    critic_samples = [None for _ in range(len(all_samples))]

    args = [
        (idx, sample, llm, llm_options, cache_dir)
        for idx, sample in enumerate(all_samples)
    ]

    with mp.Pool(n_proc) as p:
        for idx, critic_sample in tqdm(
            p.imap_unordered(
                _get_critique_with_cache_mp, args, chunksize=chunk_size
            ),
            total=len(all_samples),
            desc=f"Getting critique"
        ):
            critic_samples[idx] = critic_sample

    return critic_samples

def _get_critique_with_cache_mp(arg):

    idx, sample, llm, llm_options, cache_dir = arg

    cache_filename = "case-{}.pkl"

    try:
        sample_id = sample["id"]
        cache_path = os.path.join(cache_dir, cache_filename.format(idx))
        if os.path.exists(cache_path):
            cirtic_sample = pickle.load(open(cache_path, "rb"))
        else:
            cirtic_sample = critic_exec_one_sample(
                sample, error_route='random', llm=llm, llm_options=llm_options
            )
            pickle.dump(cirtic_sample, open(cache_path, "wb"))
        return idx, cirtic_sample
    except Exception as e:
        print(f"Error in {sample_id}: {e}", flush=True)
        return idx, None

def critic_exec_one_sample(
    sample,
    error_route,
    llm,
    llm_options=None
):
    critic_sample = copy.deepcopy(sample)
    prompt = ""
    prompt += critic_instruction

    few_shot = get_critic_few_shot(error_route, few_shot_json="critic/TableFV/tools/few_shot_critic.json")
    prompt += few_shot

    cot, max_step = get_cot_for_critic(critic_sample)
    prompt += cot

    responses = llm.generate_plus_with_score(prompt, options=llm_options)

    critique = responses[0][0].split("Conclusion:")[0].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"
    conclusion = responses[0][0].split("Conclusion:")[1].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"

    if "cotable_list" not in critic_sample:
        critic_sample["cotable_list"] = []
    if "critique_list" not in critic_sample:
        critic_sample["critique_list"] = []
    if "conclusion_list" not in critic_sample:
        critic_sample["conclusion_list"] = []
    if "max_step_list" not in critic_sample:
        critic_sample["max_step_list"] = []
    critic_sample["cotable_list"].append(cot)
    critic_sample["critique_list"].append(critique)
    critic_sample["conclusion_list"].append(conclusion)
    critic_sample["max_step_list"].append(max_step)

    critic_sample["cotable"] = cot
    critic_sample["critique"] = critique
    critic_sample["conclusion"] = conclusion
    critic_sample["max_step"] = max_step
    return critic_sample

def tree_exec_one_sample(
    sample,
    llm,
    llm_options=None
):
    tree_sample = copy.deepcopy(sample)

    prompt = ""
    prompt += tree_instruction

    few_shot = get_tree_few_shot(few_shot_json="critic/TableFV/tools/few_shot_tree.json")
    prompt += few_shot

    cot = get_cot_for_tree(tree_sample)
    prompt += cot

    responses = llm.generate_plus_with_score(prompt, options=llm_options)

    tree_thought = responses[0][0].split("Conclusion:")[0].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"
    tree = responses[0][0].split("Conclusion:")[1].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"

    if "tree_cotable_list" not in tree_sample:
        tree_sample["tree_cotable_list"] = []
    if "tree_thought_list" not in tree_sample:
        tree_sample["tree_thought_list"] = []
    if "tree_list" not in tree_sample:
        tree_sample["tree_list"] = []

    tree_sample["tree_cotable_list"].append(cot)
    tree_sample["tree_thought_list"].append(tree_thought)
    tree_sample["tree_list"].append(tree)

    tree_sample["tree"] = tree
    return tree_sample



def judge_exec_one_sample(
    sample,
    llm,
    llm_options=None
):
    judge_sample = copy.deepcopy(sample)

    prompt = ""
    prompt += judge_instruction

    few_shot = get_judge_few_shot(few_shot_json="critic/TableFV/tools/few_shot_judge.json")
    prompt += few_shot

    cot = get_cot_for_judge(judge_sample)
    prompt += cot

    responses = llm.generate_plus_with_score(prompt, options=llm_options)

    judge_thought = responses[0][0].split("Conclusion:")[0].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"
    judge = responses[0][0].split("Conclusion:")[1].strip() if "Conclusion:" in responses[0][0] else responses[0][0].strip() + "\n"

    if "judge_cotable_list" not in judge_sample:
        judge_sample["judge_cotable_list"] = []
    if "judge_thought_list" not in judge_sample:
        judge_sample["judge_thought_list"] = []
    if "judge_list" not in judge_sample:
        judge_sample["judge_list"] = []

    judge_sample["judge_cotable_list"].append(cot)
    judge_sample["judge_thought_list"].append(judge_thought)
    judge_sample["judge_list"].append(judge)

    judge_sample["judge"] = judge
    return judge_sample