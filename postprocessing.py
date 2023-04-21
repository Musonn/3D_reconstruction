import open3d as o3d
import numpy as np

def apply_mesh_filtering_taubin(mesh_in, num_iter):
    '''
    Taubin: Curve and surface smoothing without shrinkage, ICCV, 1995
    '''
    print(f"Use Taubin filtering. Generating mesh after {num_iter} iteration ...")
    mesh_out3 = mesh_in.filter_smooth_taubin(number_of_iterations=num_iter)
    mesh_out3.compute_vertex_normals()
    mesh_out3.translate([400, 0, 0])
    print('Filtering done.')
    return mesh_out3

def apply_mesh_filtering_laplacian(mesh_in, num_iter):
    print(f"Use Laplacian filtering. Generating mesh after {num_iter} iteration ...")
    mesh_out2 = mesh_in.filter_smooth_laplacian(number_of_iterations=num_iter)
    mesh_out2.compute_vertex_normals()
    mesh_out2.translate([400, 0, 0])
    print('Filtering done.')
    return mesh_out2

def apply_mesh_filtering_avg(mesh_in, num_iter):
    print(f"Use average filtering. Generating mesh after {num_iter} iteration ...")
    mesh_out1 = mesh_in.filter_smooth_simple(number_of_iterations=num_iter)
    mesh_out1.compute_vertex_normals()
    mesh_out1.translate([200,0,0])
    print('Filtering done.')
    return mesh_out1

def subdiv_loop(mesh_in, num_iter):
    print(f'Before subdivision it has {len(mesh_in.vertices)} vertices and {len(mesh_in.triangles)} triangles')
    mesh_in.compute_vertex_normals()
    mesh_out = mesh_in.subdivide_loop(number_of_iterations=num_iter)
    print(f'After subdivision it has {len(mesh_out.vertices)} vertices and {len(mesh_out.triangles)} triangles')
  
    mesh_out.translate([400,0,0])

    return mesh_out