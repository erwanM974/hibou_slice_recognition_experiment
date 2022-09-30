#
# Copyright 2022 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from calls import *


interactions_path = "./interactions"

def experiment(csv_file_prefix,int_names):
    #
    for (hsf_file_name,slice_gen_conf) in int_names:
        # ***
        f = open("{}{}.csv".format(csv_file_prefix,hsf_file_name), "w")
        f.truncate(0)  # empty file
        f.write("interaction;orig_trace;orig_length;slice;length;verdict;node_count;hibou_time\n")
        f.flush()
        # ***
        hsf_file_path = [interactions_path, hsf_file_name]
        # ***
        generate_traces(hsf_file_path)
        # ***
        orig_traces_path = "./tracegen_{}".format(hsf_file_name)
        for orig_htf_file_name in os.listdir(orig_traces_path):
            orig_htf_file_name = orig_htf_file_name[:-4]
            orig_htf_file_path = [orig_traces_path, orig_htf_file_name]
            #
            mydict_wtloc = is_sat_via_membership(hsf_file_path, orig_htf_file_path, 3)
            orig_length = mydict_wtloc['length']
            f.write(
                "{};{};{};{};{};{};{};{}\n".format(hsf_file_path,
                                                orig_htf_file_path,
                                                   orig_length,
                                                orig_htf_file_path,
                                                mydict_wtloc['length'],
                                                mydict_wtloc['verdict'],
                                                mydict_wtloc['node_count'],
                                                mydict_wtloc['time']))
            f.flush()
            # ***
            generate_slices(orig_htf_file_path,slice_gen_conf)
            # ***
            slices_path = "{}/{}_slices".format(orig_traces_path,orig_htf_file_name)
            for slice_htf_file_name in os.listdir(slices_path):
                slice_htf_file_name = slice_htf_file_name[:-4]
                slice_htf_file_path = [slices_path, slice_htf_file_name]
                # ***
                mydict_wtloc = is_sat_via_membership(hsf_file_path,slice_htf_file_path,3)
                f.write(
                    "{};{};{};{};{};{};{};{}\n".format(hsf_file_path,
                                                 orig_htf_file_path,
                                                   orig_length,
                                                 slice_htf_file_path,
                                                 mydict_wtloc['length'],
                                                 mydict_wtloc['verdict'],
                                                 mydict_wtloc['node_count'],
                                                 mydict_wtloc['time']))
                f.flush()




if __name__ == '__main__':
    exp_conf_all = [("i1",None),("i2",None),("i3",30)]
    experiment("exp_",exp_conf_all)