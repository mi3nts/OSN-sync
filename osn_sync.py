import os
import pandas as pd

# download current id lookup table
df_ids = pd.read_csv('https://raw.githubusercontent.com/mi3nts/AirQualityAnalysisWorkflows/main/influxdb/nodered-docker/id_lookup.csv')


root_datapath = "/mfs/io/groups/lary/mintsData"
basepaths = [
    os.path.join(root_datapath, "rawMqtt"),
    os.path.join(root_datapath, "raw"),
    os.path.join(root_datapath, "rawMQTT"),
    "/mfs/io/groups/lary/mints-imd/raw"

]


df_ids = df_ids[df_ids["mac_address"] != "Not Yet Installed"]  # drop out missing mac addresses
df_ids = df_ids[["mac_address", "name"]]  # keep only relevant columns
df_ids["name"] =[name.replace(" ", "_") for name in df_ids["name"]]


# generate list of folders to clone
bucket_path = "OSN:ees230012-bucket01/AirQualityNetwork/data/raw"
source_dirs = []
dest_dirs = []

data_mac_addresses = []

print("---")

for path in basepaths:
    for mac_addr in os.listdir(path):
        data_mac_addresses.append(mac_addr)
        if os.path.isdir(os.path.join(path, mac_addr)):
            valid_rows = df_ids[df_ids["mac_address"]==mac_addr]
            if len(valid_rows) > 0:
                source_dirs.append(os.path.join(path, mac_addr))
                dest_dirs.append(os.path.join(bucket_path, valid_rows.iloc[0]["name"]))
            else:
                print(os.path.join(path, mac_addr))


print("---")



# eventually we may want to include the following flags: --max-age 36h --no-traverse
with open("osn_rclone.sh", 'w') as f: 
    f.write("#!/bin/bash\n\n")
    for i in range(0, len(source_dirs)):
        # out_str = "rclone copy --max-age 1M --min-age 1d " + source_dirs[i] + " " + dest_dirs[i] + "\n"
        out_str = "rclone copy --max-age 1M --min-age 1d --progress --config /home/jxw190004/.config/rclone/rclone.conf " + source_dirs[i] + " " + dest_dirs[i] + "\n"
        f.write(out_str)


# now we want to add user permisions to the file so we can run it with nohup 
cmd = "chmod +x osn_rclone.sh" 
os.system(cmd)
