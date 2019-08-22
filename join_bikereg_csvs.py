import os
import sys

pre_reg_filepath = sys.argv[1]
walk_up_filepath = sys.argv[2]
out_filepath = os.path.dirname(pre_reg_filepath) + '/' + \
               os.path.basename(pre_reg_filepath).split("-")[0] + \
               '-all-reg.csv'


print(out_filepath)