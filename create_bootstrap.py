#!/usr/bin/env python
import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'pip'),
                     'install', '-r', 'requirements.txt'])
"""))
f = open('bootstrap.py', 'w').write(output)
