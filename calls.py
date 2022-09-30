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

import subprocess
import io
import time


def generate_traces(hsf_path):
    hsf_file = "{}/{}.hsf".format(hsf_path[0], hsf_path[1])
    print("exploring " + hsf_file)
    hibou_proc = subprocess.Popen(["./hibou_label.exe", "explore", hsf_file],
                                  stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")

def generate_slices(orig_htf_path,slice_gen_conf):
    orig_htf_file = "{}/{}.htf".format(orig_htf_path[0], orig_htf_path[1])
    print("slicing " + orig_htf_file)
    if slice_gen_conf == None:
        hibou_proc = subprocess.Popen(["./hibou_label.exe", "slice", orig_htf_file, "-p", orig_htf_path[0]],
                                  stdout=subprocess.PIPE)
    else:
        hibou_proc = subprocess.Popen(["./hibou_label.exe", "slice", orig_htf_file, "-p", orig_htf_path[0], "-r", str(slice_gen_conf), "-w"],
                                  stdout=subprocess.PIPE)
    hibou_proc.wait()
    outwrap = io.TextIOWrapper(hibou_proc.stdout, encoding="utf-8")


def get_hibou_output(hsf_file,htf_file,timeout_in_secs):
    #
    hibou_command = ["./hibou_label.exe", "analyze", hsf_file, htf_file]
    #
    try:
        t_start = time.time()
        output = subprocess.check_output(hibou_command, stderr=subprocess.STDOUT, timeout=timeout_in_secs)
        t_total = time.time() - t_start
    except Exception as e:
        print(str(e))
        return None
    outwrap = output.decode("utf-8").split('\n')
    #
    got_verdict = False
    got_length = False
    got_node_count = False
    verdict = None
    length = None
    node_count = None
    #
    for line in outwrap:
        if "verdict" in line:
            if got_verdict:
                raise Exception("got two verdict lines")
            else:
                got_verdict = True
                if "WeakPass" in line:
                    verdict = "WeakPass"
                elif "Pass" in line:
                    verdict = "Pass"
                elif "WeakFail" in line:
                    verdict = "WeakFail"
                elif "Fail" in line:
                    verdict = "Fail"
                elif "Inconc" in line:
                    verdict = "Inconc"
                else:
                    print(line)
                    raise Exception("some other verdict ?")
        # ***
        if "of length" in line:
            if got_length:
                raise Exception("got two length lines")
            else:
                got_length = True
                length = int(line.split(" ")[-1].strip()[1:-1])
        # ***
        if "node count" in line:
            if got_node_count:
                raise Exception("got two node count lines")
            else:
                got_node_count = True
                node_count = int(line.split(" ")[-1].strip())
        # ***
    #
    mydict = {
        'node_count': node_count,
        'length': length,
        'verdict': verdict,
        'time': t_total
    }
    return mydict;

def is_sat_via_membership(hsf_path,htf_path,num_tries):
    hsf_file = "{}/{}.hsf".format(hsf_path[0], hsf_path[1])
    htf_file = "{}/{}.htf".format(htf_path[0], htf_path[1])
    #
    #print("analyzing " + htf_file)
    #
    got_dict = {}
    while num_tries > 0:
        try_dict = get_hibou_output(hsf_file,htf_file,3)
        if try_dict == None:
            pass
        else:
            if got_dict == {}:
                got_dict['verdict'] = try_dict['verdict']
                got_dict['length'] = try_dict['length']
                got_dict['node_count'] = [ try_dict['node_count'] ]
                got_dict['time'] = [ try_dict['time'] ]
            else:
                if got_dict['verdict'] != try_dict['verdict']:
                    verds = { got_dict['verdict'], try_dict['verdict'] }
                    if verds == { 'Pass', 'WeakPass' }:
                        print( "got a Pass and WeakPass on different tries" )
                    else:
                        raise Exception("different verdicts on different tries " + verds)
                got_dict['node_count'] = got_dict['node_count'] + [ try_dict['node_count'] ]
                got_dict['time'] = got_dict['time'] + [ try_dict['time'] ]
            #
            num_tries = num_tries - 1
    #
    return got_dict



