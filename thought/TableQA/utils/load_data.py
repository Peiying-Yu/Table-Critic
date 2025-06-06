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


import json
from tqdm import tqdm

def load_wikitq_dataset(
    dataset_path,
    tag="test",
    first_n=-1,
):
    dataset = []
    if first_n != -1:
        all_lines = []
        for line in open(dataset_path):
            all_lines.append(line)
            if len(all_lines) >= first_n: break
    else:
        all_lines = open(dataset_path).readlines()

    for i, line in tqdm(enumerate(all_lines), total=len(all_lines), desc=f"Loading wikitq dataset"):
        info = json.loads(line)
        info["id"] = f"{tag}-{i}"
        info["chain"] = []
        info["table_caption"] = None
        dataset.append(info)
    return dataset


def wrap_input_for_demo(statement, table_text):
    return {
        "statement": statement,
        "table_text": table_text,
        "chain": [],
    }

