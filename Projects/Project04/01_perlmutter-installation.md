These instructions list the steps needed to install the software for Project 4 and its dependencies into a Python environment suitable for use with Jupyter on Perlmutter (via jupyter.nersc.gov).

## Using a conda environment (option 1):
```bash
module load conda
cd $SCRATCH
mkdir .envs
conda create -p .envs/intro-to-hpc-bootcamp python=3.12
conda activate $SCRATCH/.envs/intro-to-hpc-bootcamp
conda install -c conda-forge ipykernel matplotlib numpy scipy h5py scikit-learn
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132
python -m ipykernel install --user --name intro-to-hpc-bootcamp
```
Note: by default, conda will install things in your `$HOME` directory, which is limited to 40Gb of storage. Because pytorch is such a large dependency, it can use up a lot of that storage quota. Instead, we can directly specify the path of the installation directory --- the only downside is that we need to specify the path every time we wish to activate the environment (which is not an issue if you just use the environment through Jupyter). 

(A side benefit: the `$SCRATCH` file system is much faster than the DVS file system, which is where `$HOME` is mounted from on compute nodes, which practically lets us import large modules like pytorch much faster whenever we start up our notebooks.)

If you run into the libmamba error and it asks you to use the classic channel, run: 
`conda config --set solver classic`

```

## Using a podman container (option 2 -- for a more experienced user)

NERSC offers a set of [pre-built containers for Pytorch](https://docs.nersc.gov/machinelearning/pytorch/#containers), which utilize optimized copies of GPU libraries. Currently, the most recent pytorch container is `nersc/pytorch:26.01.01`. Alongside pytorch, the container also contains pre-installed versions of common python libraries, including all of the dependencies we need (listed above). Because we do not have any other software dependencies for the training notebooks and scripts, we could also use this container as-is for our software environment. For a container with dependncies, check out the `Containerfile` and `build-podman-container.sh` files for a template.

Load the container and register the kernelspec:
```bash
# copy the build-podman-container script
bash build-podman-container.sh

# generate the kernelspec
podman-hpc run --rm -v $HOME:/workspace intro-to-hpc:latest \
           python -m ipykernel install --prefix /workspace/.local --name intro-to-hpc-bootcamp

```

The kernelspec should be at the path `$HOME/.local/share/jupyter/kernels/intro-to-hpc-bootcamp/kernel.json`

Open the file and modify the kernelspec to use the container:

Should originally look something like 
```
{
 "argv": [
  "/usr/bin/python",
  "-Xfrozen_modules=off",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "intro-to-hpc-bootcamp",
 "language": "python",
 "metadata": {
  "debugger": true
 }
}  
```

Need to modify it to something like the following
```
{
  "argv": [
    "podman-hpc",
    "run",
    "--rm",
    "--gpu",
    "--nccl-cu13",
    "--net=host",
    "--ipc=host",
    "--jupyter",
    "localhost/intro-to-hpc:latest",
    "python",
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}"
  ],
  "display_name": "intro-to-hpc-bootcamp",
  "language": "python",
  "metadata": {
    "debugger": true
  }
}  
```

Typically, `podman` will only give you access to folders on the host filesystem if they are explicitly mounted. Folders can be mounted to a specific location within the container's filesystem with the `-v` flag:
`podman-hpc run -v {path-to-directory}:{path-to-mountpoint-in-container} ...`


If you need to mount a different directory, such as a folder within `$SCRATCH`, add a flag between the lines with `run` and `localhost/intro-to-hpc:latest`. In general, within the kernelspec, flags and arguments in the `argv` list should be on separate lines if they are normally separated by whitespace:
```
argv:[
  "podman-hpc",
  "run",
  ...
  "--jupyter",
  "-v",
  "{path-to-directory}:{path-to-mountpoint-in-container}",
  "localhost/intro-to-hpc:latest"
  ...
  "-f",
  "{connection_file}"
]
```

For example, to mount your `$SCRATCH` directory to `/scratch`:
```
argv:[
  "podman-hpc",
  "run",
  ...
  "--jupyter",
  "-v",
  "$SCRATCH:/scratch/",
  "localhost/intro-to-hpc:latest"
  ...
  "-f",
  "{connection_file}"
]
```

After which, within the notebooks, data, e.g., in `$SCRATCH/my-data-directory` could be loaded with the path `/scratch/my-data-directory`.

## Launching the podman container interactively

```podman-hpc run --rm -it {options...} container-name:tag bash```

