# Table-Critic

Code for paper [Table-Critic(ACL 2025 Main)](https://aclanthology.org/2025.acl-long.853.pdf).


## Environment

```shell
conda create --name TableCritic python=3.10 -y
conda activate TableCritic
pip install -r requirements.txt 
```

## Command Usages

### Arguments

- `--dataset_path`: path to the dataset
- `--result_dir`: path to the result directory
- `--base_url`: base URL of the LLM API
- `--model_name`: name of the LLM API
- `--openai_key`: key of the LLM API
- `--first_n`: number of the first n samples to evaluate, default: `-1` means whole dataset
- `--n_proc`: number of processes to use in multiprocessing, default: `1`
- `--chunk_size`: chunk size used in multiprocessing, default: `1`

### API setup

Add `base_url`, `model_name`, `openai_key` to both the `run_QA.sh` and the `run_FV.sh` file.

### Example usages

1. Run the experiment on the WikiTQ dataset

   ```
   bash run_QA.sh
   ```

2. Run the experiment on the TabFact dataset

   ```
   bash run_FV.sh
   ```

## Citation

```
@inproceedings{yu-etal-2025-table,
    title = "Table-Critic: A Multi-Agent Framework for Collaborative Criticism and Refinement in Table Reasoning",
    author = "Yu, Peiying  and
      Chen, Guoxin  and
      Wang, Jingjing",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-long.853/",
    doi = "10.18653/v1/2025.acl-long.853",
    pages = "17432--17451",
    ISBN = "979-8-89176-251-0"
}
```
