import os
import numpy as np
import open3d as o3d
import copy
import subprocess

def get_bpa_reconstruction(pcd):
    print('Starting bpa reconstruction...')
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    print(radius)
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd,o3d.utility.DoubleVector(
              [radius, radius * 2, radius * 4]
                                    ))  # radius > 100, never stop running
    dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
    dec_mesh.remove_degenerate_triangles()
    dec_mesh.remove_duplicated_triangles()
    dec_mesh.remove_duplicated_vertices()
    dec_mesh.remove_non_manifold_edges()
    print('Mesh reconstruction finished.')
    return dec_mesh

def get_alpha_shapes_reconstruction(pcd, alpha = 5e-3):
    
    for index in range(1, 3):
        alpha = alpha * index
        print(f"alpha={alpha:.8f}")
        print('Running alpha shapes surface reconstruction ...')
        tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
 
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
            pcd, alpha)
        mesh.compute_triangle_normals(normalized=True)
        mesh = mesh.translate([0.2 * index, 0, 0])
    print('Mesh reconstruction finished.')
    return mesh

def get_poisson_reconstruction(pcd):
    print('Running Poisson surface reconstruction ...')
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=5)
    pcd.translate([10, 0, 0])
    print('Mesh reconstruction finished.')
    return mesh

def get_dl_reconstruction(pcd, arg_in):
    hull, _ = pcd.compute_convex_hull()
    new_pcd = o3d.geometry.PointCloud()
    new_pcd.points = pcd.points
    new_pcd.normals = pcd.normals
    # Save the point cloud as a PCD file, mesh as ply file
    o3d.io.write_point_cloud(arg_in.save_path+"/tmp.ply", new_pcd, write_ascii=True )
    o3d.io.write_triangle_mesh(arg_in.save_path+"/tmp.obj", hull)
    print(f'Preprocessing complete. Use the following command to run the \
dl model. \n \n python ./point2mesh/main.py --input-pc {arg_in.save_path}/tmp.ply \
--initial-mesh {arg_in.save_path}/tmp.obj \
--save-path {arg_in.save_path} \
--pools 0.1 0.0 0.0 0.0 \
--iterations 200')
    return