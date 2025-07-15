# FlipperConvertMCT
Tool able to convert Mifare CLassic (mini, 1k, 4k) (uid 4/7 byte) and ST25TB 4k MCT, DUMP, or binary DMP files to flipper zero .nfc files.

## Usage:

### mfclassic_bin_to_nfc.py:
```
python3 mfclassic_bin_to_nfc.py [-h] -i INPUT -o OUTPUT [--uid UID] [--atqa ATQA] [--sak SAK]

Convert a Mifare Classic dump to a .nfc file for Flipper Zero

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the .dmp file
  -o OUTPUT, --output OUTPUT
                        Output path for the .nfc file
  --uid UID             Custom UID (e.g. FE:3B:17:86)
```

### mct_to_nfc.py:
```
python3 mct_to_nfc.py [-h] -i INPUT_PATH -o OUTPUT_PATH [--uid UID] [--atqa ATQA] [--sak SAK]

Convert Mifare Classic dump (.mct/.dump) to .nfc file for Flipper Zero

options:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input-path INPUT_PATH
                        Input dump file (.mct or .dump)
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Output .nfc file
  --uid UID             Custom UID (e.g. FE:3B:17:86)
```

### mikai_to_nfc.py:
```
python3: mikai_to_nfc.py [-h] -i INPUT -o OUTPUT

Binary Mikai dump converter to Flipper Zero .nfc

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input binary dump file
  -o OUTPUT, --output OUTPUT
                        Output .nfc file
```
