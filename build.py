import os
import shutil
import subprocess
import sys
from zipfile import ZipFile

GAME_FOLDER = r"D:\Plutonium\bo2"
OAT_BASE = r"D:\OpenAssetTools"
MOD_BASE = os.getcwd()
MOD_NAME = "mp_raygun"

zone_source_path = os.path.join(MOD_BASE, "zone_source")
zone_output_path = os.path.join(MOD_BASE, "zone")

# run linker
linker_cmd = [
    os.path.join(OAT_BASE, "Linker.exe"),
    "-v",
    "--load", os.path.join(GAME_FOLDER, "zone", "all", "zm_transit.ff"),
    "--load", os.path.join(GAME_FOLDER, "zone", "all", "zm_tomb.ff"),
    "--load", os.path.join(GAME_FOLDER, "zone", "all", "zm_transit_patch.ff"),
    "--load", os.path.join(GAME_FOLDER, "zone", "all", "patch_zm.ff"),
    "--load", os.path.join(GAME_FOLDER, "zone", "all", "so_tut_mp_drone.ff"),
    "--base-folder", OAT_BASE,
    "--asset-search-path", MOD_BASE,
    "--source-search-path", zone_source_path,
    "--output-folder", zone_output_path,
    "mod"
]

err = subprocess.call(linker_cmd)
if err != 0:
    input("Linker failed. Press Enter to exit...")
    sys.exit(1)

# compress folders to mod.zip
zip_path = os.path.join(MOD_BASE, "mod.zip")
iwd_path = os.path.join(MOD_BASE, "mod.iwd")

with ZipFile(zip_path, 'w') as zipf:
    for folder in ["scripts", "weapons", "images", "sound", "materials"]:
        folder_path = os.path.join(MOD_BASE, folder)
        if not os.path.exists(folder_path):
            continue
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, MOD_BASE)
                zipf.write(full_path, rel_path)

# rename to mod.iwd
if os.path.exists(iwd_path):
    os.remove(iwd_path)
os.rename(zip_path, iwd_path)

# copy files to mods folder if linker succeeded
MOD_DEST = os.path.join(os.getenv("LOCALAPPDATA"), "Plutonium", "storage", "t6", "mods", MOD_NAME)
os.makedirs(MOD_DEST, exist_ok=True)

shutil.copy2(os.path.join(zone_output_path, "mod.ff"), os.path.join(MOD_DEST, "mod.ff"))
shutil.copy2(iwd_path, os.path.join(MOD_DEST, "mod.iwd"))
shutil.copy2(os.path.join(zone_output_path, "mod.all.sabl"), os.path.join(MOD_DEST, "mod.all.sabl"))
shutil.copy2(os.path.join(MOD_BASE, "mod.json"), os.path.join(MOD_DEST, "mod.json"))

print("Build complete.")
input("Press Enter to exit...")