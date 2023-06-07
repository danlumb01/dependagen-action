# dependagen-action
Github action to generate terraform dependabot config for complex directory structures. 

**Warning**
This action will overwrite an existing dependabot config file if run without `output-file` parameter.


## Usage
```
on:
  workflow_dispatch:
  pull_request:
    types: [opened, edited, reopened, synchronize]

jobs:
  dependabot-gen:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout the code
        uses: actions/checkout@v2
        
      - name: Dependabot config generation
        uses: danlumb01/terraform-dependagen-action@main
        
      - name: Commit & Push
        run: |
          git add -A
          git config --global user.name 'Dependabot Generator'
          git config --global user.email 'dependagen@users.noreply.github.com'
          git commit -am "Dependabot config generated"
          git push
```


Run it manually with Python and pass the args:

```
usage: dependagen.py [-h] [--dependency_file [DEPENDENCY_FILE]] [--scan_dir [SCAN_DIR]] [--output_file [OUTPUT_FILE]] [--interval [INTERVAL]] [--day [DAY]]

options:
  -h, --help            show this help message and exit
  --dependency_file [DEPENDENCY_FILE]
  --scan_dir [SCAN_DIR]
  --output_file [OUTPUT_FILE]
  --interval [INTERVAL]
  --day [DAY]
```

For example: `python3 -m dependagen --output_file mynewdeps.yml --interval weekly --day monday`