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
from os.path import splitext, basename
from os.path import join as pjoin
import tempfile
import shutil
import argparse
import re
import subprocess
from mako.template import Template
DEBUG=True

def error_print(msg):
    sys.stderr.write("ERROR: {:}\n".format(msg))

def debug_print(msg):
    if DEBUG: sys.stderr.write("DEBUG: {:}\n".format(msg))

def make_template(inp, outp, model):
    templ = Template(filename=inp, 
                     input_encoding='utf-8',
                     output_encoding='utf-8',
                     preprocessor=lambda x: re.sub(r'\\\\', "${'\\\\\\\\\\\\\\'}", x)
    )
    with open(outp, "wb") as f:
        f.write(templ.render(
            model=model
        ))

def compile_pdf(temp_dir, temp_tex):
    current = os.curdir
    try:
        os.chdir(temp_dir)
        args=["pdflatex", temp_tex, "-halt-on-error"]
        subprocess.check_call(args)
        debug_print("Running: {}".format(" ".join(args)))
    finally:
        os.chdir(current)
    return True

def main(inp, outp):
    temp_dir = tempfile.mkdtemp()
    texfile = splitext(splitext(basename(inp))[0])[0] + ".tex"
    pdffile = splitext(splitext(basename(inp))[0])[0] + ".pdf"
    temp_tex = pjoin(temp_dir, texfile)
    try:
        debug_print("Compiling template from {} to: {}".format(inp, temp_tex))
        make_template(inp, temp_tex, (1,2,3))
        if compile_pdf(temp_dir, temp_tex):
            debug_print("Moving file from {} to {}.".format(
            os.path.join(temp_dir, pdffile), os.path.join(outp, pdffile)))
            shutil.move(os.path.join(temp_dir, pdffile), os.path.join(outp, pdffile))
    finally:
        debug_print("Removing directory {}".format(temp_dir))
        shutil.rmtree(temp_dir)

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
    if not os.path.exists(args.output) or not os.path.isdir(args.output):
        error_print("Provided output should be an existing directory.\nExiting")
        return None
    return args

if __name__ == '__main__':
    args = cli()
    if not args:
        sys.exit(1)
    path = lambda x : os.path.realpath(x)
    main(path(args.input), path(args.output))
