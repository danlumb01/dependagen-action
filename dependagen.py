# dependencies
import os , argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dependency_file", nargs='?', const="versions.tf", default="versions.tf")
parser.add_argument("--scan_dir",type=str, required=True)
parser.add_argument("--out_file", type=str, required=True)
args=parser.parse_args()

# to store matches
dirs_found = []

# use os walk to traverse recursively, grab any file called versions.tf and get the root it lives in
for root, dirs, files in os.walk(args.scan_dir):
    for file in files:
        if args.dependency_file in file:
            dirs_found.append(os.path.relpath(root, start=args.scan_dir)) # find relative path from our passed in scan_dir


# dependabot config fragments
config_header = """
version: 2
updates:
"""

config_package_fragment = """
- package-ecosystem: "terraform"
    directory: {directory}
    schedule:
      interval: "weekly"
      day: "sunday"
    open-pull-requests-limit: 5 # default
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"] # let's have more control over major changes
"""

# setup the config file

os.makedirs(os.path.dirname(args.out_file), exist_ok=True) # create the dirpath we got in out_file if needed

with open(args.out_file, "w") as config_file:
    config_file.write(config_header)

# now append the fragments
with open(args.out_file, "a") as config_file:
    for dir in dirs_found:
        config_file.write(config_package_fragment.format(directory=dir))

