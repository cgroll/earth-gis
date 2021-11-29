import ee
import pandas as pd
import geemap

######################### visualizations
########################################################

def vis_params_dict(**kwargs):
    return locals()['kwargs']

def default_vis_params(vis_name):

    if vis_name == 'landsat':

        vis_params = vis_params_dict(bands=['B4','B3','B2'],
                                     min=0,
                                     max=3000,
                                     gamma=1.4)

    return vis_params

######################### locations, settings
########################################################

def get_known_roi(loc_name):

    if loc_name == 'grand_canyon':

        return [-112.8598, 36.2841]

    if loc_name == 'grand_canyon_polygon':

        coords = [
            [-113.66754, 36.188031],
            [-113.749927, 35.775853],
            [-113.178207, 35.698837],
            [-113.108302, 36.002414],
            [-112.661411,36.159814],
            [-112.134629, 35.947856],
            [-111.695228, 36.091242],
            [-112.077207, 36.387282],
            [-112.773758, 36.489728],
            [-113.66754, 36.188031]
        ]

        return coords

    if loc_name == 'grand_canyon_rectangle':

        coords = [
            [-117.58047, 33.838949],
            [-117.58047, 38.769708],
            [-107.783823, 38.769708],
            [-107.783823, 33.838949],
            [-117.58047, 33.838949]]

        return coords

    if loc_name == 'us_west_large':

        coords = [
            [-126.933781, 26.110606],
            [-126.933781, 45.657335],
            [-95.256957, 45.657335],
            [-95.256957, 26.110606],
            [-126.933781, 26.110606]]

        return coords

    if loc_name == 'las_vegas':

        coords = [
            [-115.471773, 35.892718],
            [-115.471773, 36.409454],
            [-114.271283, 36.409454],
            [-114.271283, 35.892718],
            [-115.471773, 35.892718],
        ]
    
        return coords

def coords_to_polygon(coords):
    
    return ee.Geometry.Polygon(coords, None, False)

######################### image metadata extraction
########################################################

def collection_len(img_coll):
    return len(img_coll.getInfo()['features'])

def extract_single_img(collection, idx=0):
    
    single_img = ee.Image(collection.toList(collection.size()).get(idx))
    
    return single_img

def extract_img_metadata(img, list_of_properties, img_id=0):
    
    props = {}
    props[img_id] = {k: img['properties'][k] for k in list_of_properties}
    
    return props

def extract_img_collection_metadata(this_collection, list_of_properties):
    
    n_imgs = len(this_collection.getInfo()['features'])
    img_features = this_collection.getInfo()['features']
    
    all_img_props = []
    
    for idx in range(n_imgs):
        
        this_img_metadata = extract_img_metadata(img_features[idx], list_of_properties, idx)
        all_img_props.append(pd.DataFrame().from_dict(this_img_metadata).T)
        
    return pd.concat(all_img_props, axis=0)

def extract_img_collection_properties(this_collection):
    """
    Leveraging geemap function `image_props`. A bit slow for multiple images.
    """
    
    n_imgs = len(this_collection.getInfo()['features'])
    
    dict_list = []
    for ii in range(n_imgs):
        this_img = extract_single_img(this_collection, ii)

        this_dict = geemap.image_props(this_img).getInfo()
        dict_list.append(this_dict)
        
    img_coll_metadata = pd.DataFrame.from_dict(dict_list)
    
    return img_coll_metadata


######################### US land cover dataset
########################################################

def get_landcover_class_info(landcover_data_info):
    """
    Get overview table with land cover classification classes
    """
    
    # get class IDs
    lc_class_values = landcover_data_info['properties']['landcover_class_values']
    lc_class_info = pd.DataFrame(lc_class_values, columns=['class_number'])

    # split text into name and description
    lc_class_texts = landcover_data_info['properties']['landcover_class_names']
    split_texts = [this_text.split(' - ') for this_text in lc_class_texts]

    lc_class_info['class_name'] = [this_lc_type[0] for this_lc_type in split_texts]
    lc_class_info['description'] = [this_lc_type[1] for this_lc_type in split_texts]

    # create class names how they will be created in columns of zonal statistics
    lc_class_info['class_name_statistics'] = ['Class_' + str(this_val) for this_val in lc_class_values]
    
    # get class color codes
    colors = landcover_data_info['properties']['landcover_class_palette']
    colors = ['#' + this_color for this_color in colors]
    lc_class_info['color'] = colors

    # get aggregate class groups
    lc_class_info['class_group'] = [int(str(this_double_digit_val)[0]) for this_double_digit_val in lc_class_values]

    class_group_name_map = {1: 'Water',
                            2: 'Developed',
                            3: 'Barren',
                            4: 'Forest',
                            5: 'Shrubland',
                            7: 'Herbaceous',
                            8: 'Planted/Cultivated',
                            9: 'Wetlands'
                           }

    # attach class group names
    lc_class_info['class_group_name'] = lc_class_info['class_group'].map(lambda x: class_group_name_map[x])

    # automatically derive class group color coding
    lc_class_group_colors = lc_class_info.groupby('class_group').tail(1).loc[:, ['class_group', 'color']]
    lc_class_group_colors = lc_class_group_colors.rename({'color': 'class_group_color'}, axis=1)
    lc_class_info = lc_class_info.merge(lc_class_group_colors, how='left')
    
    return lc_class_info