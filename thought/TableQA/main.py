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


import subprocess
import fire
import os
import sys
sys.path.append('thought/TableQA')

from utils.load_data import load_wikitq_dataset
from utils.llm import LLM
from utils.helper import *
from utils.evaluate import *
from utils.chain import *
from operations import *


def main(
    dataset_path: str = "thought/TableQA/data/wikitq/test_lower.jsonl",
    thought_results_dir: str = "results/thought/wikitq",
    base_url="",
    openai_api_key="EMPTY",
    model_name="qwen2.5-72b-instruct",
    first_n=-1,
    n_proc=8,
    chunk_size=4,
):
    dataset = load_wikitq_dataset(dataset_path, first_n=first_n)

    gpt_llm = LLM(
        model_name=model_name,
        key=openai_api_key,
        base=base_url
    )

    os.makedirs(thought_results_dir, exist_ok=True)

    proc_samples, _ = dynamic_chain_exec_with_cache_mp(
        dataset,
        llm=gpt_llm,
        llm_options=gpt_llm.get_model_options(
            temperature=0.0, per_example_max_decode_steps=2048, per_example_top_p=1.0
        ),
        strategy="top",
        cache_dir=os.path.join(thought_results_dir, "cache"),
        n_proc=n_proc,
        chunk_size=chunk_size,
    )
    fixed_chain = [
        (
            "Simple query",
            simple_query,
            dict(use_demo=True),
            dict(
                temperature=0, per_example_max_decode_steps=2048, per_example_top_p=1.0
            ),
        ),
    ]
    final_result, _ = fixed_chain_exec_mp(gpt_llm, proc_samples, fixed_chain, n_proc=4, chunk_size=2)
    
    pickle.dump(
        final_result, open(os.path.join(thought_results_dir, "final_result.pkl"), "wb")
    )


if __name__ == "__main__":
    fire.Fire(main)
