import pickle
import subprocess
import fire
import os
import sys
sys.path.append('critic/TableFV')
sys.path.append('refine/TableFV')
from utils.read_pkl import read_pkl
from utils.extract_step import return_incorrect_max_step
from utils.llm import LLM
from utils.helper import *
from utils.evaluate import *
from utils.chain import *
from operations import *
from tools import read_pkl, critic_tree_init

def main(
    thought_results_dir: str = "results/thought/tabfact",
    refine_results_dir: str = "results/refine/tabfact",
    base_url="",
    openai_api_key="EMPTY",
    model_name="qwen2.5-72b-instruct",
    first_n=-1,
    n_proc=10,
    chunk_size=5,
):
    
    result_pkl = os.path.join(thought_results_dir, "final_result.pkl")

    if first_n != -1:
        all_samples = read_pkl(result_pkl)[:first_n]
    else:
        all_samples = read_pkl(result_pkl)

    gpt_llm = LLM(
        model_name=model_name,
        key=openai_api_key,
        base=base_url
    )

    critic_tree_init(file_path="critic/TableFV/tools/few_shot_critic.json")
    refine_list = judge_critic_refine_with_cache_mp(
        all_samples,
        llm=gpt_llm,
        llm_options=gpt_llm.get_model_options(
            temperature=0.0, per_example_max_decode_steps=2048, per_example_top_p=1.0
        ),
        strategy="top",
        cache_dir=os.path.join(refine_results_dir, "cache"),
        n_proc=n_proc,
        chunk_size=chunk_size,
    )

    acc = tabfact_match_func_for_samples(refine_list)
    print("Accuracy:", acc)

    print(
        f'Accuracy: {acc}',
        file=open(os.path.join(refine_results_dir, "result.txt"), "w")
    )
    pickle.dump(
        refine_list, open(os.path.join(refine_results_dir, "final_result.pkl"), "wb")
    )


if __name__ == "__main__":
    fire.Fire(main)