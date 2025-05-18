import re

def check_strings(s):
    pattern = r'^\[Incorrect\] Step \d+$'
    if not re.match(pattern, s):
        return False
    return True

def extract_part(s):
    pattern = r'(\[Incorrect\] Step \d+)'
    match = re.search(pattern, s)
    if match:
        return match.group(1)
    return None

def extract_incorrect_step(s):
    pattern = r'\[Incorrect\] Step (\d+)'
    match = re.search(pattern, s)
    if match:
        number = match.group(1)
        return number
    return None

def return_incorrect_max_step(sample):

    conclusion = sample['conclusion']
    max_step = sample['max_step']

    if conclusion != '[Correct]':
        if not check_strings(conclusion.strip()):   # unlike the format '[Incorrect] Step <num>'
            if extract_part(conclusion.strip()):
                incorrect_step = extract_incorrect_step(conclusion.strip())
                return int(incorrect_step), int(max_step)
            else:
                nums = re.findall(r"step (\d+) is incorrect", conclusion.strip().lower())
                if nums:
                    return int(nums[0]), int(max_step)
                return None, int(max_step)
        else:
            incorrect_step = extract_incorrect_step(conclusion.strip())
            return int(incorrect_step), int(max_step)
    else:
        return None, int(max_step)