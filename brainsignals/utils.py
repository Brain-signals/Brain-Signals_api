### External imports ###

import nibabel as nib
import random
import string
from time import strftime


### Functions ###

def create_id():
    tag = ''.join(random.choices(list(string.ascii_lowercase), k=4)).upper()
    return strftime("%Y%m%d_%H%M%S_") + tag


def NII_to_3Darray(path):
    NII = nib.load(path).get_fdata()
    return NII


def time_print(start,end):
    total_sec = round(end - start, 2)
    if total_sec > 7200:
        time_prompt = f'\033[1m{total_sec} secs ({round(total_sec/3600,3)} hours)\033[0m'
    elif total_sec > 120:
        time_prompt = f'\033[1m{total_sec} secs ({round(total_sec/60,2)} minutes)\033[0m'
    else:
        time_prompt = f'\033[1m{total_sec} secs\033[0m'
    return time_prompt
