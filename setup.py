import cx_Freeze

executables = [cx_Freeze.Executable('grandmasvsreindeers.py')]

cx_Freeze.setup(
    name="Grandmas vs Reindeers",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["art","sound"]}},
    executables = executables

)