
critic_instruction = """You are an intelligent critic tasked with determining which step of the table reasoning is incorrect based on the following information:

1. Original Table: The raw table data.
2. Statement: The statement pertaining to the table data.
3. Reasoning Steps: A step-by-step process of sub-table transformations and extractions based on the following functions. 
    - f_add_column(): Adds a new column to the table.
    - f_select_row(): Selects specific rows based on the question.
    - f_select_column(): Removes irrelevant columns from the table.
    - f_group_column(): Groups rows based on the values in a specific column.
    - f_sort_column():  Sorts rows based on the values in a specified column.
4. Prediction Answer: Based on the chain of reasoning, finally derive an answer to determine whether the Statement is true or false. If the Statement is true, answer YES; otherwise, answer NO.

Instruction:
1. **Step-wise Analysis**: Conduct an evaluation of each reasoning step's validity. The step that is unnecessary but does not affect the answer is considered correct.
2. **Analysis Categories:**
    - For correct steps: Provide validation reasoning and mark as `Step <NUM> is correct.`.
    - For incorrect steps: Detail the logical flaws and mark as `Step <NUM> is incorrect.`.
    - You should stop at the first incorrect step.
3. **Conclude this critique**: Summarize this critique with an explicit conclusion.
4. **Conclusion Categories**:
    - Conclude with 'Conclusion: [Incorrect] Step <NUM>'.
"""


judge_instruction = """You are an intelligent judge tasked with determining whether the given Prediction Answer is correct or incorrect based on the following information:

1. Original Table: The raw table data.
2. Statement: The statement pertaining to the table data.
3. Prediction Answer: The answer to determine whether the Statement is true or false. If the Statement is true, answer YES; otherwise, answer NO. This answer needs validation.

Instruction:
1. **Explanation**: Conduct an explanation of why the Prediction Answer is correct or incorrect.
2. **Conclusion**:
    - If the Prediction Answer is correct, conclude with 'Conclusion: [Correct]'.
    - If the Prediction Answer is incorrect, conclude with 'Conclusion: [Incorrect]'.
"""

tree_instruction = """You are an expert in professional logical analysis. With a high level of proficiency, you are required to rely on the following information to accurately identify which step within the reasoning process is incorrect and subsequently locate the corresponding error type within the error tree:

1. Original Table: The raw table data.
2. Statement: The question pertaining to the table data.
3. Reasoning Steps: A step-by-step process of sub-table transformations and extractions based on the following functions. 
    - f_add_column(): Adds a new column to the table.
    - f_select_row(): Selects specific rows based on the question.
    - f_select_column(): Removes irrelevant columns from the table.
    - f_group_column(): Groups rows based on the values in a specific column.
    - f_sort_column():  Sorts rows based on the values in a specified column.
4. Prediction Answer: The answer determines whether the Statement is true or false based on the final sub-table. If the Statement is true, answer YES; otherwise, answer NO.

Instruction: 
1. **Analysis**: Conduct an analysis of each reasoning step's validity. The step that is unnecessary but does not affect the answer is considered correct.
    - For correct steps: Provide validation reasoning and mark as `Step <NUM> is correct.`.
    - For incorrect steps: Detail the logical flaws and mark as `Step <NUM> is incorrect.`.
    - You should stop at the first incorrect step.
2. **Conclusion**:
    - If the Prediction Answer is incorrect, conclude with either 'Conclusion: [Incorrect] (ERROR ROUTE)' or 'Conclusion: [Incorrect] (random)'. 
    - Use '(ERROR ROUTE)' to indicate the specific path in the error tree that represents the error. 
    - If no such route can be identified, use '(random)' instead.
"""
