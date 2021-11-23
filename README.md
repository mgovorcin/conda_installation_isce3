# Instalation of ISCE3 using conda (NOTES)

## 1. Create folder isce3, and inside folders src, install, build

    mkdir isce3; mkdir isce3/src isce3/install isce3/build

## 2. Clone git repositories to your local machine

    Conda environement requirement and source files
    
    cd isce3;
    git clone https://github.com/mgovorcin/conda_installation_isce3

    Clone isce3 git repo to your local folder
    
    cd src; git clone https://github.com/isce-framework/isce3    

## 3. Create conda env isce3 using the requirement.txt 

    cd ../ # go to the ISCE3 ROOT folder 
    
    conda create --name isce3
    conda activate isce3
    
    #Install mamba package for parallelized installation of conda packages
    conda install mamba
    
    # Install all isce3 dependencies
    mamba install -yes --file conda_installation_isce3/requirements.txt
    
## 4. Build the ISCE3 

    cd build; 
   
    CC=clang CXX=clang++ cmake -DCMAKE_FIND_FRAMEWORK=NEVER -DCMAKE_INSTALL_PREFIX=../install/ ../src/isce3/
     
    # if clang cannot find conda LIBRARY and INCLUDE path, set it manually
     export CMAKE_INCLUDE_PATH={$CONDA_INSTALL_DIR}/envs/isce3/include
     export CMAKE_LIBRARY_PATH={$CONDA_INSTALL_DIR}/envs/isce3/lib
     
     
    make VERBOSE=ON 
    
    ctest # test installation

## 5. Install and set environments

    make install
   
    cd ..; source conda_installation_isce3/source.rc
    
## Bugs and fixes
    Building with cmake cannot find Gtest, and make fails at 43%
      Fix: conda install gtest -c conda-forge
    
    ctest fails only at 42 test: test.cxx.isce3.geometry.bbox.geoperimeter_equator (Failed) 
      Fix: TODO

