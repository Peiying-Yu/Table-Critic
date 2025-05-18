# Table-Critic

Code for paper [Table-Critic: A Multi-Agent Framework for Collaborative Criticism and Refinement in Table Reasoning](https://arxiv.org/abs/2502.11799).


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
@article{yu2025table,
  title={Table-critic: A multi-agent framework for collaborative criticism and refinement in table reasoning},
  author={Yu, Peiying and Chen, Guoxin and Wang, Jingjing},
  journal={arXiv preprint arXiv:2502.11799},
  year={2025}
}
```