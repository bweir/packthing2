from __future__ import print_function

import ast
import inspect
import subprocess
import sys
import utils.log as log

from collections import deque

current = sys.modules[__name__]


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = []

    @property
    def name(self):
        return '.'.join(self._name)

    @property
    def args(self):
        return self._args

    def visit_Call(self, node):
        self._name = node.id
        self._args = []
        try:
            for k in node.args:
                if isinstance(k, ast.List):
                    dir(k)
                    self._args.append(k)
        except TypeError:
            pass

    def visit_Name(self, node):
        print("HERE")
        self._name.append(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.append(node.attr)
            self._name.append(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node)
            if len(callvisitor.args):
                print(callvisitor.name, callvisitor.args)
                func_calls.append(callvisitor.name)

    return func_calls



def cmd(args,verbose=True, strict=True, stdinput=None):
    if verbose:
        print("-",' '.join(args))

    if not args:
        log.error("Attempting to run empty command.")

    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as e:
        log.error("Command '"+args[0]+"' not found; exiting.")
        return "", ""

    out, err = process.communicate(input=stdinput)
    if strict:
        if process.returncode:
            print(err)
            raise subprocess.CalledProcessError(process.returncode, args, err)
    return out, err

def require():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    funcs = inspect.getmembers(mod)

#    print(mod)

    tree = ast.parse(open(inspect.getfile(mod)).read())
    print (get_func_calls(tree))



#    print(mod, funcs)

    funcs = [ x for x in inspect.getmembers(mod) if inspect.isfunction(x[1]) ]

#    print(mod, funcs)
    pass


#log.failOnError(True)
#log.printOnError(True)
#
#print(current)

cmd(['echo','chicken','bacon'])
cmd(['nerf','chicken','bacon'])

require()
