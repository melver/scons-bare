"""
SCons tool to emit compile_commands.json for files compiled in current
invocation.

Requires default CXXCOMSTR and CCOMSTR.
"""

import json
import os
import SCons

def make_strfunction(strfunction):
    def _strfunction(target, source, env, **kwargs):
        cwd = os.getcwd()
        cmd = strfunction(target, source, env, **kwargs)
        env._compile_commands.append({
            'directory' : cwd,
            'command'   : cmd,
            'file'      : source[0].rstr()
            })
        return cmd
    return _strfunction

def write_compile_commands(target, source, env):
    with open(str(target[0]), 'w') as f:
        json.dump(env._compile_commands, f, indent=2, sort_keys=True)

def compile_commands(env, outdir):
    if hasattr(env, '_compile_commands'): return
    env._compile_commands = []

    c_strfunction = make_strfunction(SCons.Defaults.CAction.strfunction)
    SCons.Defaults.CAction.strfunction = c_strfunction
    cxx_strfunction = make_strfunction(SCons.Defaults.CXXAction.strfunction)
    SCons.Defaults.CXXAction.strfunction = cxx_strfunction

    compile_commands_path = env.Dir(outdir).File("compile_commands.json")
    env.AlwaysBuild(env.Command(target = compile_commands_path,
                                source = [],
                                action = env.Action(write_compile_commands,
                                         "writing %s" % compile_commands_path)))

def generate(env, **kwargs):
    env.AddMethod(compile_commands, "CompileCommands")

def exists(env):
    return True
