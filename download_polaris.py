import wget, os, multiprocessing, glob
# %%
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
output_base_path = 'G:\\polaris\\downloaded'
# %
def PathGen(output_base_path, domain_extent):
    url_path_lst = []
    template_url = 'http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/' \
                   '{0}/{1}/{2}/lat{3}{4}_lon{5}{6}.tif'
    template_out_path = '{0}\\{1}\\{2}\\'
    lat_range = range(domain_extent['lat'][0],domain_extent['lat'][1])
    lon_range = range(domain_extent['lon'][0],domain_extent['lon'][1])
    for layer in layers:
        for stat in statistics:
            for param in parameters:
                for lat in lat_range:
                    for lon in lon_range:

                        url = template_url.format(param,
                                            stat,
                                            layer,
                                            str(lat),
                                            str(lat+1),
                                            str(lon),
                                            str(lon+1))
                        temp_path = os.path.join(output_base_path,
                                                 template_out_path.format(param,stat,layer))
                        if not os.path.exists(temp_path):
                            os.makedirs(temp_path)
                        url_path_lst += [[url, temp_path]]
    return url_path_lst
#%%
def run_process(url, output_path):
    wget.download(url, out=output_path)
    # TODO: you can write your rename logic at here using os.rename


#%%

if __name__ == '__main__':
    url_path_lst = PathGen(output_base_path, domain_extent)
    cpus = multiprocessing.cpu_count()
    max_pool_size = 6
    pool = multiprocessing.Pool(cpus if cpus < max_pool_size else max_pool_size)
    for url, path in url_path_lst: # change here to download other files
        print('Beginning file download with wget module {n}'.format(n=url))
        pool.apply_async(run_process, args=(url, path, ))
    # add your code here to download other files
    pool.close()
    pool.join()
    print("finish")

#%%
def mergeTiles(folder):
    folder_path = os.path.join(folder,'*.tif')
    file_list = glob.glob(folder_path)
    files_string = " ".join(file_list)
    out_folder = os.path.join(folder,'merged')
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    out_fn = os.path.join(out_folder,'merged.tif')
    command = "python gdal_merge.py -o " + out_fn + " -of gtiff " + files_string
    os.system(command)



