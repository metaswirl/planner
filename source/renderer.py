#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.

""" """
import sys
import os
import tempfile
import argparse
import re
import subprocess
from mako.template import Template
DEBUG=False

def error_print(msg):
    sys.stderr.write("ERROR: {:}\n".format(msg))

def debug_print(msg):
    if DEBUG: sys.stderr.write("DEBUG: {:}\n".format(msg))

def make_template(inp, outp, model):
    print("\t\tCompiling template to: {}").format(outp)
    templ = Template(filename=inp, 
                     input_encoding='utf-8',
                     output_encoding='utf-8',
                     preprocessor=lambda x: re.sub(r'\\\\', "${'\\\\\\\\\\\\\\'}", x)
    )
    with open(outp, "wb") as f:
        f.write(templ.render(
            model=model
        ))

def compile_pdf(filepath, output_path):
    temp_dir = tempfile.mkdtemp()
    filename = os.path.basename(filepath) 
    subprocess.check_call([
        "pdflatex", filepath, "-halt-on-error",
        "-output-directory", temp_dir])
    os.rename(temp_dir)
    os.rmdir(temp_dir)


def main(inp, outp):
    make_template(inp, outp, (1,2,3))
    compile_pdf(outp)

def cli():
    """ Command line interface """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i", "--input", required=True,
        help="The input file")
    parser.add_argument(
        "-o", "--output", required=True,
        help="The output file")
    args = parser.parse_args()
    if not os.path.exists(args.input):
        error_print("Provided input path does not exist\nExiting")
        return None
    return args

if __name__ == '__main__':
    args = cli()
    if not args:
        sys.exit(1)
    path = lambda x : os.path.realpath(x)
    main(path(args.input), path(args.output))
