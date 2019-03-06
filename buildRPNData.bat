rem TCC script for building the RPN wheel

del dist\*.whl
del dist\*.gz

python setup.py sdist bdist_wheel

rem python setup.py sdist bdist_wheel

del /sxyz /nt rpnChiladaData.egg-info
del /sxyz /nt build

