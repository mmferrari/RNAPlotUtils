# RNAPlot Utils

### Description
Various utilities for the RNAPlot program included into [ViennaRNA](https://github.com/ViennaRNA/ViennaRNA) suite.

Right now it can convert an input file from [Multistrand](https://github.com/DNA-and-Natural-Algorithms-Group/multistrand), [DrTransformer](https://github.com/bad-ants-fleet/ribolands) or [Kinwalker](https://github.com/ViennaRNA/ViennaRNA) to a file readable by RNAPlot.


### Usage
```text
usage: rnaplot_utils.py [-h] [-i1 MULTISTRAND_IN_FILE]
                        [-i2 DRTRANSFORMER_IN_FILE] [-i3 KINWALKER_IN_FILE]

RNAplot utils

optional arguments:
  -h, --help            show this help message and exit
  -i1 MULTISTRAND_IN_FILE, --input-multistrand MULTISTRAND_IN_FILE
                        Multistrand input file
  -i2 DRTRANSFORMER_IN_FILE, --input-drtransformer DRTRANSFORMER_IN_FILE
                        Drtransformer input file
  -i3 KINWALKER_IN_FILE, --input-kinwalker KINWALKER_IN_FILE
                        Kinwalker input file
```
The output files will have the same name of the corresponding input file with the extension changed to `.vienna` )in the case of an input file without extension, it will be added).
If a file named as the future output file already exists, it will be overwritten.

**NOTE**: every input file will have its own corresponding output file, for example `python3 rnaplot_utils.py -i1 file1 -i2 file2` will generate two files `file1.vienna` and `file2.vienna`.
