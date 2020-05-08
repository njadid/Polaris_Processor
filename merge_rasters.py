import gdal
import os
import multiprocessing
import glob
import time
domain_extent = {}
domain_extent['lon'] = [-97, -90]
domain_extent['lat'] = [40, 45]
layers = ['0_5',
        '5_15',
         '15_30',
         '30_60',
         '60_100',
         '100_200']
# layers = ['0_5']
statistics = ['mean','mode','p5','p50','p95']
# statistics = ['mean']
parameters = ['alpha','bd','clay','hb','ksat','lambda','n','om','ph',
              'sand','silt','theta_r','theta_s']
# parameters = ['alpha','bd','hb','ksat','lambda','n','theta_r','theta_s']
input_base_path = 'G:\\polaris\\downloaded'
# output_base_path  = 'G:\\polaris\\iowa'
output_base_path  = 'C:\\Users\\njadidoleslam\\Desktop\\polaris'
# %%
def PathGenMerge(input_base_path, output_base_path):
    path_lst = []
    template_in_path = '{0}\\{1}\\{2}\\'
    template_out_fn = '{0}_{1}_{2}.tif'
    for layer in layers:
        for stat in statistics:
            for param in parameters:
                        temp_in_path = os.path.join(input_base_path,
                                                 template_in_path.format(param, stat, layer))
                        temp_out_path = os.path.join(output_base_path,
                                                 template_out_fn.format(param, stat, layer))
                        path_lst += [[temp_in_path, temp_out_path]]
    return path_lst


#%%
def mergeTiles(in_folder, out_fn):
    folder_path = os.path.join(in_folder,'*.tif')
    file_list = glob.glob(folder_path)
    files_string = " ".join(file_list)

    if os.path.isfile(out_fn):
        return
    command = "python gdal_merge.py -o " + out_fn + " -of gtiff " + files_string
    os.system(command)

#%%
if __name__ == '__main__':
    path_lst = PathGenMerge(input_base_path, output_base_path)
    cnt = 0
    for in_path, out_path in path_lst:
        mergeTiles(in_path, out_path)
        cnt +=1
        print 'Progress: %.2f' % (float(cnt)/float(len(path_lst))*100) + '%. Remaining = '  + str(len(path_lst)-cnt)  + ' \r' ,
        time.sleep(0.01)
    # add your code here to download other files
    print("Raster Merge Finished")