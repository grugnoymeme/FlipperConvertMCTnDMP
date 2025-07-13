import argparse
import os
import pathlib

def add_spaces_to_hex(in_str):
    out_str = ""
    for i in range(0, len(in_str), 2):
        out_str += in_str[i:i+2] + " "
    return out_str.strip()

def check_uid_size(dump):
    # dump è lista di stringhe esadecimali riga per riga (tipo: 'A0A1A2A3...')
    block0 = dump[0]
    first_byte = block0[:2].upper()
    if first_byte == "88":
        return 7
    else:
        return 4

def get_uid_and_sak_atqa(dump):
    uid_size = check_uid_size(dump)
    dump_size = len(dump)

    block0 = dump[0]

    uid = block0[:14] if uid_size == 7 else block0[:8]

    if dump_size == 64:  # Classic 1K: 64 blocchi
        atqa = "44 00" if uid_size == 7 else "04 00"
        sak = "88" if uid_size == 7 else "08"
        card_type = "1K"
    elif dump_size == 20:  # Classic Mini: 20 blocchi
        atqa = "04 00"
        sak = "89" if uid_size == 7 else "09"
        card_type = "MINI"
    elif dump_size == 256:  # Classic 4K: 256 blocchi
        atqa = "04 00"
        sak = "18"
        card_type = "4K"
    else:
        atqa = "00 00"
        sak = "00"
        card_type = "UNKNOWN"

    return uid, atqa, sak, card_type

def convert_file(input_path):
    input_extension = os.path.splitext(input_path)[1].lower()
    if input_extension in [".dump", ".mct"]:
        with open(input_path, "rt") as file:
            dump = []
            for line in file:
                line = line.strip()
                if line and not line.startswith("+"):
                    dump.append(line)
        return dump
    else:
        raise ValueError(f"Unsupported file extension: {input_extension}")

def write_mifare_info(f, dump):
    uid, atqa, sak, card_type = get_uid_and_sak_atqa(dump)

    f.write(f"UID: {add_spaces_to_hex(uid)}\n")
    f.write(f"ATQA: {atqa}\n")
    f.write(f"SAK: {sak}\n")
    f.write(f"Mifare Classic type: {card_type}\n")

def write_flipper_nfc(output_path, dump):
    with open(output_path, "w") as f:
        f.write("Filetype: Flipper NFC device\n")
        f.write("Version: 4\n")
        f.write("# Device type can be ISO14443-3A, ISO14443-3B, ISO14443-4A, ISO14443-4B, ISO15693-3, FeliCa, NTAG/Ultralight, Mifare Classic, Mifare DESFire, SLIX, ST25TB\n")
        f.write("Device type: Mifare Classic\n")
        f.write("# UID, ATQA and SAK are common for all formats\n")

        write_mifare_info(f, dump)

        f.write("Data format version: 2\n")
        f.write("# Mifare Classic blocks, '??' means unknown data\n")

        for i, block in enumerate(dump):
            line = add_spaces_to_hex(block).replace("--", "??")
            f.write(f"Block {i}: {line}\n")

def get_args():
    parser = argparse.ArgumentParser(description="Converti dump Mifare Classic (.mct/.dump) in file .nfc per Flipper Zero")
    parser.add_argument("-i", "--input-path", required=True, type=pathlib.Path, help="File dump input (.mct o .dump)")
    parser.add_argument("-o", "--output-path", required=True, type=pathlib.Path, help="File output .nfc")
    return parser.parse_args()

def main():
    args = get_args()

    if not os.path.isfile(args.input_path):
        print(f"File di input non trovato: {args.input_path}")
        return

    dump = convert_file(str(args.input_path))
    write_flipper_nfc(str(args.output_path), dump)
    print(f"[OK] File .nfc creato: {args.output_path}")

if __name__ == "__main__":
    main()
