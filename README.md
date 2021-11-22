# Instalation of ISCE3 using conda

1. Create folder isce3, and inside folders src, install, build \n
    mkdir isce3; mkdir isce3/src isce3/install isce3/build

2. Clone git repositories to your local machine \n
    Conda environement requirement and source files \n
    cd isce3:
    git clone https://github.com/mgovorcin/conda_installation_isce3

    Clone isce3 git repo to your local folder \n
    cd src; git clone https://github.com/isce-framework/isce3    

3. Create conda env isce3 using the requirement.txt \n
    cd ../ # go to the ISCE3 ROOT folder \n
    conda create --name isce3 --file conda_installation_isce3/requirements.txt

4. Build the ISCE3 \n
   cd build; \n
   CC=clang CXX=clang++ cmake -DCMAKE_FINF_FRAMEWORK=NEVER -DCMAKE_INSTALL_PREFIX=../install/ ../src/isce3/

    make VERBOSE=ON 
    ctest # test installation

5. Install and set environements
   make install
   cd ..; source conda_installation_isce3/source.rc

