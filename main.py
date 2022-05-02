from functions import *

path="/home/buket/Desktop/codes/fat_measurement/Omerleventmutluerretroperitonalsigmoidtm/33305/DICOMIMG/CT229268"

print("started execution")

#load and display slice
slice=load_singular_slice(path)
display_scans([slice.pixel_array])

#displat it in terms of Hounsfield Units
hu_slice=convert_to_hu(slice)
display_scans([slice.pixel_array,hu_slice])

#filter fat and show it
filtered=filter_intensities(hu_slice,-150,-25)
display_scans([filtered])
show_hist(filtered)


plt.close('all')
print("Done")

