import open3d as o3d
import copy
import numpy as np

def filter_pcd(_pcd, path, selection=[1,2]):
    # Read label file
    labels = []
    with open(path, 'r') as f:
        for line in f:
            for item in line.split(' '):
              label = int(item)
              labels.append(label)

    # Filter non-background points
    new_pcd_points = []
    new_pcd_colors=[]
    for i, point in enumerate(_pcd.points):
        if labels[i+1] in selection: # +1 because the label file has num_points as the first line
            new_pcd_points.append(point)
            new_pcd_colors.append(_pcd.colors[i])

    # Create a new point cloud with the filtered points
    new_pcd = copy.deepcopy(_pcd)
    if not new_pcd_points: raise ValueError('new_pcd_points is an empty list. May be this scene does \
    not have the label you specified.')
    new_pcd.points = o3d.utility.Vector3dVector(np.asarray(new_pcd_points))
    new_pcd.colors = o3d.utility.Vector3dVector(np.asarray(new_pcd_colors))
    return new_pcd

def downsample_pcd(pcd, vs):
    return pcd.voxel_down_sample(voxel_size=vs)

def remove_outlier(_pcd, mode='radius'):
    '''
    outlier removal. Two modes: radius or statistical
    '''
    print('Starting removing outliers')
    if mode == 'radius':
      cl, ind = _pcd.remove_radius_outlier(nb_points=16, radius=0.05)
      print(f"{len(_pcd.points)-len(cl.points)} Radius oulier removed")
      return cl

    if mode == 'statistical':
      cl, ind = _pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
      print(f"{len(_pcd.points)-len(cl.points)}Statistical oulier removal")
      return cl

def compute_normals(pcd, ctp=False):
    print('Starting to compute normals')
    if ctp:
        pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
        pcd.estimate_normals()
        pcd_spanning_tree: o3d.geometry.PointCloud = copy.deepcopy(pcd)
        pcd_spanning_tree.orient_normals_consistent_tangent_plane(k=300)
        pcd_spanning_tree.translate([4, 0, 0])
        return pcd_spanning_tree
    else:
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        return pcd