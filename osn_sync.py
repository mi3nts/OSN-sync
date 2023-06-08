import os
import pandas as pd

# download current id lookup table
df_ids = pd.read_csv('https://raw.githubusercontent.com/mi3nts/AirQualityAnalysisWorkflows/main/influxdb/nodered-docker/id_lookup.csv')


root_datapath = "/mfs/io/groups/lary/mintsData"
basepaths = [
    os.path.join(root_datapath, "rawMqtt"),
    os.path.join(root_datapath, "raw"),
    os.path.join(root_datapath, "rawMQTT")
]

print(basepaths)

df_ids = df_ids[df_ids["mac_address"] != "Not Yet Installed"]  # drop out missing mac addresses
df_ids = df_ids[["mac_address", "name"]]  # keep only relevant columns


# generate list of folders to clone
files_to_copy = []

for d in basepaths:
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    print(subdirs)


