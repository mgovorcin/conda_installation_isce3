# Instalation of ISCE3 using conda (NOTES for MacOSX)

## 1. Create folder isce3, and inside folders src, install, build
    
      mkdir isce3; mkdir isce3/src isce3/install isce3/build

      cd isce3; export ISCE3_ROOT=$PWD

## 2. Clone git repositories to your local machine

    # Conda environement requirement and source files
      # Repository: conda_installation_isce3 (contains the isce3 requirements list, and source file that sets up the environmental variables)

      cd $ISCE3_ROOT; git clone https://github.com/mgovorcin/conda_installation_isce3

    # Clone isce3 github repository into a local folder ${ISCE3_ROOT}/src 
      cd $ISCE3_ROOT/src; git clone https://github.com/isce-framework/isce3    

## 3. Create conda env isce3 using the requirement.txt 
    # Install and activate conda environment 
    
      conda create --name isce3;   conda activate isce3
    
    # Install mamba package for parallelized installation of conda packages
      conda install mamba;
    
    # Install all isce3 dependencies
      cd $ISCE3_ROOT; mamba install --yes --file conda_installation_isce3/requirements.txt
    
## 4. Build the ISCE3 software

    cd $ISCE_ROOT/build; 

    # Do cmake build of the ISCE3

      CC=clang CXX=clang++ cmake -DCMAKE_FIND_FRAMEWORK=NEVER -DCMAKE_INSTALL_PREFIX=../install/ ../src/isce3/;
          
    make VERBOSE=on;
    

## 5. Install and test installation

    make install;

    #Set environments
    source conda_installation_isce3/source.rc;

    # Test ISCE3 Instalation
      ctest; 
   
    
## Bugs and fixes
    # If clang cannot find conda LIBRARY and INCLUDE path, set it manually
    # You can find the path of your current conda environment by: which python 
     export CMAKE_INCLUDE_PATH={$CONDA_INSTALL_DIR}/envs/isce3/include
     export CMAKE_LIBRARY_PATH={$CONDA_INSTALL_DIR}/envs/isce3/lib
     #TODO find a better way

     # If there are more conda environments, sometime cmake calls libraries and/or headers from another environment
      open another terminal tab, and do fresh activation of isce3 conda environment 

    
    # ctest fails at the 144 test: test.python.pkg.nisar.workflows.stage_dem (Failed) 
      aws.credentials missing in home directory




