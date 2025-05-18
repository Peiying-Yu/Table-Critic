
import pickle
import subprocess
import fire
import os

from tools import read_pkl, get_table_log, get_cot_for_critic, get_critique_with_mp
from thought.TableFV.utils.llm import ChatGPT, LLM



def main(
    thought_results_dir: str = "results/thought/tabfact",
    critic_results_dir: str = "results/critic/tabfact",
    base_url="",
    openai_api_key="EMPTY",
    model_name="qwen2.5-72b-instruct",
    first_n=-1,
    n_proc=1,
    chunk_size=1,
):

    os.makedirs(critic_results_dir, exist_ok=True)

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

    critic_samples = get_critique_with_mp(
        all_samples,
        llm=gpt_llm,
        llm_options=gpt_llm.get_model_options(
            temperature=0.0, per_example_max_decode_steps=500, per_example_top_p=1.0
        ),
        cache_dir=os.path.join(critic_results_dir, "cache"),
        n_proc=n_proc,
        chunk_size=chunk_size,
    )

    pickle.dump(
        critic_samples, 
        open(os.path.join(critic_results_dir, "critic_log_list.pkl"), "wb")
    )

    os.makedirs(critic_results_dir, exist_ok=True)

    


if __name__ == "__main__":
    fire.Fire(main)
