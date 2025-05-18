base_url=''
openai_api_key=''
model_name='qwen2.5-72b-instruct'
first_n=-1

thought_results_dir='results/thought/wikitq'
refine_results='results/refine/wikitq'


python thought/TableQA/main.py \
--thought_results_dir $thought_results_dir \
--base_url $base_url \
--openai_api_key $openai_api_key \
--model_name $model_name \
--first_n $first_n
if [ $? -ne 0 ]; then
    echo "Error in thought/TableQA/main.py"
    exit 1
fi


python refine/TableQA/main_tree_based.py \
--thought_results_dir $thought_results_dir \
--refine_results_dir $refine_results \
--base_url $base_url \
--openai_api_key $openai_api_key \
--model_name $model_name \
--first_n $first_n
if [ $? -ne 0 ]; then
    echo "Error in refine/TableQA/main_tree_based.py"
    exit 1
fi