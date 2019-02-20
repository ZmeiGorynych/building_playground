import glob
from building_playground.import_utils import idf_to_graph
from eppy.modeleditor import IDF


# get the data
iddfile = "../../../_eppy/eppy/resources/iddfiles/Energy+V8_9_0.idd"
IDF.setiddname(iddfile)
data_dir = '../../data/'
other_files = glob.glob(data_dir + 'ExampleFiles/5ZoneBoilerOutsideAirReset.idf')
fname1 =  data_dir +'HVACTemplate-5ZoneBaseboardHeatout.idf'#"../eppy/eppy/resources/idffiles/V8_9/smallfile.idf"

base_fname = fname1.replace('\\','/').split('/')[-1].split('.')[0]

G = idf_to_graph(fname1)
from networkx import write_gexf
write_gexf(G, data_dir + 'output/' + base_fname + ".gexf", version="1.2draft")
# import subprocess
# subprocess.call(["dot","-Tpng",base_fname + ".dot","-o","graph1.png"])
# from IPython.core.display import Image, display
# display(Image("graph1.png"))
#
# # airloop = [value for key,value in obj_by_name if 'AIRLOOPHVAC' in key]
# # print(airloop)
# # idf2.idfobjects : list for each type
# # idf1.saveas('something.idf')
# # idf1.newidfobject("MATERIAL")
# surfaces = idf2.idfobjects['']
# # asurface = surfaces[0]
# # print("surface azimuth =",  asurface.azimuth, "degrees")
# # print("surface tilt =", asurface.tilt, "degrees")
# # print("surface area =", asurface.area, "m2")
# # just vertical walls
# vertical_walls = [sf for sf in surfaces if sf.tilt == 90.0]
# print([sf.Name for sf in vertical_walls])
#
# # north facing walls
# north_walls = [sf for sf in vertical_walls if sf.azimuth == 0.0]
# print([sf.Name for sf in north_walls])
#
# # north facing exterior walls
# exterior_nwall = [sf for sf in north_walls if sf.Outside_Boundary_Condition == "Outdoors"]
# print([sf.Name for sf in exterior_nwall])
#
# # print out some more details of the north wall
# north_wall_info = [(sf.Name, sf.azimuth, sf.Construction_Name) for sf in exterior_nwall]
# for name, azimuth, construction in north_wall_info:
#     print(name, azimuth, construction)
# print('done!')