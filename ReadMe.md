
# 3D RECONSTRUCTION CODING CHALLENGE

![image](https://github.com/Musonn/3D_reconstruction/assets/43937020/1e7ac7ed-49b0-4101-8fc0-c931ca5d0398)

Meshes reconstructed from downsampled point clouds with 1. ball pivoting algorithm (BPA) 2. alpha shapes 3. poisson surface reconstruction 4. Point2Mesh, a deep learning model for reconstructing a surface mesh. 

## Installation
You need also point2mesh and pytorch3d to successfully run this software. 
First, follow the '[Getting Started](https://github.com/ranahanocka/point2mesh)' to install point2mesh. Once you manage to clone the repository, DO NOT run `conda env create -f environment.yml`. Instead, copy the environment.yml in this zip to rewrite it. Then continue to follow the instructions. My environment.yml contains all necessary packages to run this software and fixed a bug in the original. (In the case that dependency error occurs, use environment_full.yml instead. This one contains all packages in my container, which is way too many than needed.)

Replace ./point2mesh/models/layers/mesh.py with the one provided in zip. Somehow there were bugs when running on GPU and I fixed them.

Run the following in python to install pytorch3d:

    import os
    import sys
    import torch
    need_pytorch3d=False
    try:
        import pytorch3d
    except ModuleNotFoundError:
        need_pytorch3d=True
    if need_pytorch3d:
        if torch.__version__.startswith(("1.13.", "2.0.")) and sys.platform.startswith("linux"):
            # We try to install PyTorch3D via a released wheel.
            pyt_version_str=torch.__version__.split("+")[0].replace(".", "")
            version_str='py38_cu116_pyt1130'
            os.system('pip install fvcore iopath')
            os.system(f'pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/{version_str}/download.html')
        else:
            # We try to install PyTorch3D from source.
            os.system("pip install 'git+https://github.com/facebookresearch/pytorch3d.git@stable'")

## Usage

Create 3D mesh from point cloud. That is, create .obj from .ply file.

## Data Preparation
In bash,

    wget https://rgbd-dataset.cs.washington.edu/dataset/rgbd-scenes_aligned/rgbd-scenes_aligned.tar
    tar xf rgbd-scenes_aligned.tar
In addition, download the dataset for point2mesh if you want,

    bash ./point2mesh/scripts/get_data.sh

## Work Done

 - point cloud processing
	 - label selection: filter non-background points
	 - down sample
	 - remove outlier
	 - compute normal
	 - convex hull
 - reconstruction methods
	 - ball pivoting
	 - alpha shapes
	 - poisson
	 - DL: point2mesh
 - mesh processing
	 - filtering
	 - subdivision
 - command line arg

## Todo

Create and project a UV image to apply texture to the mesh


## Credits

open3d: http://www.open3d.org/

point2mesh: https://github.com/ranahanocka/point2mesh

pytorch3d: https://github.com/facebookresearch/pytorch3d/blob/main/docs/tutorials/deform_source_mesh_to_target_mesh.ipynb

pyvista: https://docs.pyvista.org/version/stable/index.html

NNNNNathan's blog: https://blog.csdn.net/qq_41366026?type=blog

## License

MIT license
> Written with [StackEdit](https://stackedit.io/).
