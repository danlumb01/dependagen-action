# dependencies
import os , argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dependency_file", type=str, nargs='?', const="versions.tf", default="versions.tf")
parser.add_argument("--scan_dir", type=str, nargs='?', default=os.getcwd())
parser.add_argument("--output_file", type=str, nargs='?', default="/.github/dependabot.yml")
parser.add_argument("--interval", type=str, nargs='?', default="weekly")
parser.add_argument("--day", type=str, nargs='?', default="sunday")
#parser.add_argument("--include_symlinks", type=bool, nargs='?', default=True)  ## implement later


args=parser.parse_args()

# to store matches
dirs_found = []

# location to write config file
#output_file = args.scan_dir + "/.github/dependabot.yml"

# dependabot config fragments
config_header = """
version: 2
updates:
"""

config_package_fragment = """
  - package-ecosystem: "terraform"
    directory: {directory}
    schedule:
      interval: {interval}
      day: {day}
    open-pull-requests-limit: 5 # default
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"] # let's have more control over major changes
"""



# use os walk to traverse recursively, grab any file called versions.tf and get the root it lives in
for root, dirs, files in os.walk(args.scan_dir):
    for file in files:
        if args.dependency_file in file:
            dirs_found.append(os.path.relpath(root, start=args.scan_dir)) # find relative paths using our scan dir as the starting point

# setup the config file directory if needed
if os.path.dirname(args.output_file):
  if not os.path.exists(args.output_file):
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True) # create the dirpath we got in out_file if needed

# Create the file
with open(args.output_file, "w") as config_file:
    config_file.write(config_header)

# now append the fragments
with open(args.output_file, "a") as config_file:
    for dir in dirs_found:
        config_file.write(config_package_fragment.format(directory=dir, interval=args.interval, day=args.day))

