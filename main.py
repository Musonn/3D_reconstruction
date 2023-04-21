"""# main"""
import argparse
import os
import numpy as np
import open3d as o3d
import copy
from preprocessing import filter_pcd, remove_outlier, compute_normals, downsample_pcd
from postprocessing import subdiv_loop, apply_mesh_filtering_taubin, apply_mesh_filtering_laplacian, apply_mesh_filtering_avg
from reconstruction import get_bpa_reconstruction, get_alpha_shapes_reconstruction, get_poisson_reconstruction, get_dl_reconstruction 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mesh generator. Enter the pcd file path and reconstruction method')

    # Required argument
    parser.add_argument('pcd_path', nargs='+', help='Path to the pcd file(s)')

    # Optional arguments
    parser.add_argument('--save-path', type=str, default='./checkpoints/default_project', help='path to save results to')
    parser.add_argument('--filter_pcd_path', nargs='+', help='Path to the label file(s) for filtering the pcd(s)')
    parser.add_argument('--filter_pcd_label', nargs='+', type=int, help='Label index to keep for each corresponding label file')
    parser.add_argument('--downsample', type=float, default=0.002, help='Voxel size for point cloud downsampling')
    parser.add_argument('--remove_outliers', type=str, choices=['radius', 'statistical'], default='radius', help='Algorithm for outlier removal')
    parser.add_argument('--compute_normals_with_ctp', action='store_true', help='Bool. Flag to use ctp to compute normals for the input point cloud')
    parser.add_argument('--mesh_reconstruction', default='alpha', choices=['bpa', 'alpha', 'poisson', 'dl'], help='Algorithm for mesh reconstruction (default: alpha)')
    parser.add_argument('--mesh_filtering', type=str, choices=['avg', 'laplacian', 'taubin'], default='laplacian', help='Algorithm for mesh filtering')
    parser.add_argument('--mesh_filtering_iterations', type=int, default=5, help='Number of mesh filtering iterations (default: 5)')
    parser.add_argument('--mesh_subdivision', type=int, default=5, help='Number of mesh subdivision iterations')
    parser.add_argument('--mesh_subdivision_iterations', type=int, default=1, help='Number of mesh subdivision iterations (default: 1)')

    args = parser.parse_args()

    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    for i, pcd_path in enumerate(args.pcd_path):
        ################ Point Cloud Preprocessing ################
        pcd = o3d.io.read_point_cloud(pcd_path)
        print('Point Clouds loaded.')

        # Filter PCD based on Label
        if args.filter_pcd_path:
            label_path = args.filter_pcd_path[i]
            label_index = args.filter_pcd_label[i]
            if isinstance(label_path, str) and isinstance(label_index, int):
                selection = [int(x) for x in str(label_index)]
                pcd = filter_pcd(pcd, label_path, selection)
            else:
                raise ValueError('label_path or label_index cannot be None')

        # Downsample PCD
        pcd = downsample_pcd(pcd, args.downsample)

        # Remove Outliers
        if args.remove_outliers == 'radius':
            pcd = remove_outlier(pcd)
        else:
            pcd = remove_outlier(pcd, 'statistical')

        # Compute Normals
        if args.compute_normals_with_ctp:
            pcd = compute_normals(pcd, True)
        else:
            pcd = compute_normals(pcd)

        ################ Mesh Reconstruction ################
        if args.mesh_reconstruction == 'bpa':
            mesh = get_bpa_reconstruction(pcd)
        elif args.mesh_reconstruction == 'alpha':
            mesh = get_alpha_shapes_reconstruction(pcd)
        elif args.mesh_reconstruction == 'poisson':
            mesh = get_poisson_reconstruction(pcd)
        elif args.mesh_reconstruction == 'dl':
            get_dl_reconstruction(pcd, args)
            exit('\nCopy the cmd abv and run the dl model.')
        else:
            raise ValueError('Invalid reconstruction method')

        ################ Mesh Postprocessing ################
        # Mesh Filtering
        if args.mesh_filtering == 'avg':
            mesh = apply_mesh_filtering_avg(mesh, args.mesh_filtering_iterations)
        elif args.mesh_filtering == 'laplacian':
            mesh = apply_mesh_filtering_laplacian(mesh, args.mesh_filtering_iterations)
        else: # args.mesh_filtering == 'taubin'
            mesh = apply_mesh_filtering_taubin(mesh, args.mesh_filtering_iterations)

        # Mesh Subdivision
        mesh = subdiv_loop(mesh, args.mesh_subdivision_iterations)
        print("Mesh creation done.")

        # Display and Write Mesh to File
        o3d.visualization.draw_plotly([mesh], point_sample_factor=0.1)
        mesh_file = 'result_{:03d}.ply'.format(i+1)
        o3d.io.write_triangle_mesh(os.path.join(args.save_path, mesh_file), mesh)

