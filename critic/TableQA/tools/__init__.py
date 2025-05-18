import sys
sys.path.append('')
sys.path.append('./thought/TableQA')
from .read_pkl import read_pkl
from .get_info import get_act_func, get_table_log, get_cot_for_critic
from .multiprocess import get_critique_with_mp, critic_exec_one_sample, judge_exec_one_sample, tree_exec_one_sample
from .update_tree import update_error_tree
from .few_shot_critic_json import critic_tree_init