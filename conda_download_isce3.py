#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 10:49:22 2022

@author: Marin Govorcin
"""
import os
import subprocess
import argparse
from pathlib import Path

def createParser():
    '''
    Create command line parser.
    '''

    parser = argparse.ArgumentParser( description='Install isce3 via conda.')
    parser.add_argument('-i', '--install_dir', dest='install_dir', type=str, required=True,
            help='Isce3 installation directory')
    parser.add_argument('-b', '--build_isce3', dest='build_isce3', action='store_true', default=False, required=False,
            help='Build isce3')
    parser.add_argument('-v', '--isce3_version', dest='isce3_version', default='develop', required=False,
            help='Choose isce3 version [0.4, 0.4.1, 0.5, develop]')
    return parser

def cmdLineParse(iargs = None):
    '''
    Command line parser.
    '''

    parser = createParser()
    inps =  parser.parse_args(args = iargs)

    return inps


conda_ver = {
    'Mac' :' Miniconda3-latest-MacOSX-x86_64.sh',
    'Linux' : 'Miniconda3-latest-Linux-x86_64.sh' }

isce3_git = 'https://github.com/isce-framework/isce3.git'
isce3_versions = ['0.1', '0.2', '0.3', '0.4', '0.4.1', '0.5']

isce3_req = '''
python>=3.8,<=3.9
backoff             # used isce3.nisar.workflows.stage_dem.py
## C/C++ Compilers and Related Packages
compilers           # cross-platform c/cxx/fortran compilers. use the latest version to avoid pyre compilation errors
cmake
cython
openmp
pybind11
pyre
gsl
coreutils
cudatoolkit
## Packages for Tests
gmock
gtest
pytest
## Common Python Packages
gitpython
h5py
hdf5>=1.10.2
numpy
scipy
fftw>=3
gawk
pandas
eigen
matplotlib
sphinx
wget
## Yaml Packages
pyyaml
ruamel.yaml
yamale
#GDAl Package
libgdal
gdal>=2.3
shapely
'''

source_isce3 = '''
#!/bin/bash

ISCE3_HOME={isce3_dir}

echo "ISCE_HOME_DIR: $ISCE3_HOME"

###### ISCE3 INSTALATIION DIR ##############

ISCE3_LIB="$ISCE3_HOME/install/lib"
ISCE3_PYTHON="$ISCE3_HOME/install/packages"
ISCE3_PATH="$ISCE3_HOME/install/bin"

##############################################

export PATH=$PATH:$ISCE3_PATH:"$ISCE3_HOME/install/packages/nisar/workflows"
export PYTHONPATH=$PYTHONPATH:$ISCE3_PYTHON
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ISCE3_LIB
'''


def download_miniconda(os_system = 'Linux'):
    command = 'wget https://repo.anaconda.com/miniconda/{} -q --show-progress'.format(conda_ver[os_system])
    os.system(command) 
    return None

def download_isce3(version='0.5', outdir='./'):
    from git import Repo
    
    (Path(outdir)/'isce3').mkdir(exist_ok=True)
    out_dir = Path(outdir)/'isce3/src'
    out_dir.mkdir(exist_ok=True)
    print('Cloning isce3 repository from github:')
    if str(version) in isce3_versions:
        Repo.clone_from(isce3_git, out_dir, branch='release-v{}'.format(version))
    else:
        Repo.clone_from(isce3_git, out_dir, branch='develop')
    
    return out_dir.parents[0]

def check_os():
    process = subprocess.run('uname',capture_output=True, shell=True, text=True)
    if process.stdout.split()[0] == 'Darwin':
        os_name = 'OSX'
    elif process.stdout.split()[0] == 'Linux':
        os_name = 'Linux'
    
    return os_name

def conda_install_isce3(isce3_dir, os_system='Linux', conda_env='isce3', test_install=True):
    isce3_install_dir = Path(isce3_dir)/'install'
    isce3_buid_dir = Path(isce3_dir)/'build'
    
    isce3_install_dir.mkdir(exist_ok=True)
    isce3_buid_dir.mkdir(exist_ok=True)
    
    # Create isce3 conda env
    os.chdir(isce3_dir)
    # write 'requirements.txt'
    with open('requirements.txt', 'w') as f:
        f.write(isce3_req)

    os.system(f'mamba create --name {conda_env} --yes --file requirements.txt')
    miniconda_dir = Path(subprocess.run('which conda', capture_output=True, shell=True, text=True).stdout.split()[0]).parents[1]
  
    # Build isce3
    os.chdir(isce3_buid_dir)
    
    command =f'cmake -DCMAKE_FIND_FRAMEWORK=NEVER -DCMAKE_INSTALL_PREFIX=../install/ ../src/ -DCMAKE_PREFIX_PATH={miniconda_dir}/envs/{conda_env}/'

    if os_system == 'OSX':
        command = f'CC={miniconda_dir}/envs/{conda_env}/bin/clang CXX={miniconda_dir}/envs/{conda_env}/bin/clang++ ' + command
    elif os_system == 'Linux':
        command = f'CC={miniconda_dir}/envs/{conda_env}/bin/gcc CXX={miniconda_dir}/envs/{conda_env}/bin/g++ ' + command    
    
    os.system(f'conda run -n {conda_env} ' + command)
    
    # Make
    os.system('make -j 16 VERBOSE=on')
    os.system('make install')

    try:
        os.system(command)
    except RuntimeError:
        print('Something went wrong with installation!') 
    #write source isce3 env
    with open('../source.rc', 'w') as f:
        f.write(source_isce3.format(isce3_dir=isce3_dir))
    
    print('Add "source {}/source.rc" to ~/.bash_profile'.format(os.getcwd()))
    
    if test_install:
        os.system('source ../source.rc; conda run -n {conda_env} ctest')
        
    print('Finish installing isce3: USAGE: conda activate isce3; source source.rc')
    
    return None


def install_isce3(inps):
    #find OS 
    os_name = check_os()
    install_dir = Path(inps.install_dir)
    
    # Check if conda is installed
    try:
        subprocess.run("conda", capture_output=True, shell=True, check = True)
        miniconda_dir = Path(subprocess.run('which conda', capture_output=True, shell=True, text=True).stdout.split()[0]).parents[1]
    except:
        #Download and install miniconda
        download_miniconda(os_system = os_name)
        miniconda_dir = install_dir/'miniconda3'
        os.system('bash {} -b -p {}'.format(conda_ver[os_name], miniconda_dir))
        command = '''
        conda init bash;
        conda config --add channels conda-forge;
        conda config --set channel_priority strict;
        '''
        os.system(command)
    os.system('conda install cmake wget git gitpython tree mamba --yes')

    
    # Download and install isce3
    
    if inps.build_isce3:
        #install isce3
        isce3_dir = download_isce3(version=inps.isce3_version, outdir=install_dir)
        conda_install_isce3(isce3_dir, os_system=os_name, test_install=True)
    else:
        os.system('conda create --name isce3 -y')
        command = 'conda install isce3 -c conda-forge -y -n isce3'
        os.system(command.format(miniconda_dir=miniconda_dir))
    

def main(iargs=None):
    '''
    Main driver.
    '''
    inps = cmdLineParse(iargs)
    install_isce3(inps)


if __name__ == '__main__':
    main()
        
    




