from functions import *

path="/home/buket/Desktop/codes/fat_measurement/Omerleventmutluerretroperitonalsigmoidtm/33305/DICOMIMG"

print("started execution")
slice=load_singular_slice("./Omerleventmutluerretroperitonalsigmoidtm/33305/DICOMIMG/CT229455")
display_scans([slice.pixel_array])


hu_slice=convert_to_hu(slice)
display_scans([slice.pixel_array,hu_slice])


filtered=filter_intensities(hu_slice,-150,-25)
display_scans([filtered])
show_hist(filtered)


plt.close('all')


print("Done")

