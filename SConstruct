# -*- mode:python -*-

import os

# ------------- OPTIONS ------------- #

AddOption('--prefix',
    help="Installation prefix. [Default: /usr/local]",
    metavar='DIR',
    default="/usr/local",
)

AddOption('--release',
    help="Release build target configuration (full optimizations).",
    action='store_true',
    default=False,
)

AddOption('--dbgopt',
    help="Debug build with some optimizations.",
    action='store_true',
    default=False,
)

AddOption('--sanitize',
    help="Debug build with sanitizers.",
    action='store_true',
    default=False,
)

AddOption('--compile_commands',
    help="Emit compilation database.",
    action='store_true',
    default=False,
)

# ------------- COMMON ------------- #

main = Environment(
    ENV = os.environ,
    PREFIX = GetOption('prefix'),
)

main['CXX']          = os.environ.get('CXX', 'g++')
main['CC']           = os.environ.get('CC', 'gcc')
main['DOXYGEN']      = os.environ.get('DOXYGEN', 'doxygen')
main['CLANG_TIDY']   = os.environ.get('CLANG_TIDY', 'clang-tidy')
main['CLANG_FORMAT'] = os.environ.get('CLANG_FORMAT', 'clang-format')
main['CPPLINT']      = os.environ.get('CPPLINT', 'cpplint')

main.Append(
    CPPDEFINES = {},
    CPPFLAGS   = ['-Wall', '-Werror'],
    CPPPATH    = ['#/include'],
    CFLAGS     = ['-std=c11'],
    CXXFLAGS   = ['-std=c++14'],
    LIBPATH    = [],
    LIBS       = [],
    LINKFLAGS  = [],
)

# ------------- BUILD VARIANTS ------------- #

main.VariantDir('build/src',  'src',  duplicate=False)
main.VariantDir('build/test', 'test', duplicate=False)

if GetOption('release'):
    main.Append(CPPDEFINES = ['NDEBUG'])
    main.Append(CPPFLAGS = ['-O2'])
else:
    main.Append(CPPFLAGS = ['-g'])

    if GetOption('dbgopt'):
        main.Append(CPPFLAGS = ['-O'])

    if GetOption('sanitize'):
        sanitizers = ['undefined', 'address']
        san_flags = ['-fsanitize={}'.format(s) for s in sanitizers]
        main.Append(CPPFLAGS  = san_flags, LINKFLAGS = san_flags)

# ------------- COLLECT SOURCES/TARGETS ------------- #

if GetOption('compile_commands'):
    main.Tool('compile_commands')
    main.CompileCommands('build')
    if BUILD_TARGETS and 'build/compile_commands.json' not in BUILD_TARGETS:
        BUILD_TARGETS.append('build/compile_commands.json')

main.SConscript('build/src/SConscript' , {'env' : main})
main.SConscript('build/test/SConscript', {'env' : main})

# ------------- ALIASES/COMMANDS------------- #

def Phony(env = main, deps = [], **kw):
    if not env: env = DefaultEnvironment()
    for target, action in kw.items():
        env.AlwaysBuild(env.Alias(target, deps, action))

Phony(
    cleanall = "rm -rf build",

    doc = "rm -rf apidoc/html && $DOXYGEN Doxyfile",

    format = "@echo 'Modifying files in-place...'\n"
             "$CLANG_FORMAT -style=file -i "
               "$$(git ls-files | grep -E '\.(hpp|hh|cpp|cc|cxx|h|c)$$')",

    lint = "$CPPLINT --extensions=hpp,hh,cpp,cc,cxx "
             "--filter=-build/c++11,-whitespace,-legal/copyright "
             "$$(git ls-files | grep -E '\.(hpp|hh|cpp|cc|cxx)$$')",

    tidy = "$CLANG_TIDY -header-filter='.*' "
             "-checks='-*,clang-analyzer-*,google*,misc*,-misc-unused-parameters,performance*' "
             "-p build/compile_commands.json "
             "$$(git ls-files | grep -E '\.(cpp|cc|cxx|c)$$')",
)

# vim: set ft=python :
