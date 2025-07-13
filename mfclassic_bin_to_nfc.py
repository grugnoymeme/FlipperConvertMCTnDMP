import argparse

def bytes_to_hex(b):
    return ' '.join(f"{x:02X}" for x in b)

def extract_uid(block0):
    if block0[0] == 0x88:
        uid = bytes_to_hex(block0[1:4] + block0[4:7])
        uid_type = 7
    else:
        uid = bytes_to_hex(block0[0:4])
        uid_type = 4
    return uid, uid_type

def detect_card_type_and_params(data):
    size = len(data)
    block0 = data[0:16]
    uid, uid_length = extract_uid(block0)

    if size == 1024:
        if uid_length == 7:
            atqa = "44 00"
            sak = "88"
        else:
            atqa = "04 00"
            sak = "08"
        return "1K", 64, uid, atqa, sak

    elif size == 4096:
        atqa = "04 00"
        sak = "18"
        return "4K", 256, uid, atqa, sak

    elif size == 320:
        atqa = "04 00"
        sak = "09"
        return "Mini", 20, uid, atqa, sak

    else:
        raise ValueError(f"Dimensione non valida: {size} byte. Attesi 320 (Mini), 1024 (1K) o 4096 (4K).")

def convert_dump_to_flipper_format(dump_file, output_file, uid=None, atqa=None, sak=None):
    with open(dump_file, "rb") as f:
        data = f.read()

    card_type, block_count, extracted_uid, default_atqa, default_sak = detect_card_type_and_params(data)

    uid = uid or extracted_uid
    atqa = atqa or default_atqa
    sak = sak or default_sak

    print(f"[INFO] Tipo: Mifare Classic {card_type}")
    print(f"[INFO] UID: {uid}")
    print(f"[INFO] ATQA: {atqa}")
    print(f"[INFO] SAK: {sak}")

    with open(output_file, "w") as out:
        out.write("Filetype: Flipper NFC device\n")
        out.write("Version: 4\n")
        out.write("# Device type can be ISO14443-3A, ISO14443-3B, ISO14443-4A, ISO14443-4B, ISO15693-3, FeliCa, NTAG/Ultralight, Mifare Classic, Mifare Plus, Mifare DESFire, SLIX, ST25TB, NTAG4xx, Type 4 Tag, EMV\n")
        out.write("Device type: Mifare Classic\n")
        out.write("# UID, ATQA and SAK are common for all formats\n")
        out.write(f"UID: {uid}\n")
        out.write(f"ATQA: {atqa}\n")
        out.write(f"SAK: {sak}\n")
        out.write(f"Mifare Classic type: {card_type}\n")
        out.write("Data format version: 2\n")
        out.write("# Mifare Classic blocks, '??' means unknown data\n")

        for i in range(block_count):
            block = data[i*16:(i+1)*16]
            out.write(f"Block {i}: {bytes_to_hex(block)}\n")

    print(f"[OK] File scritto: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converti un dump Mifare Classic in file .nfc per Flipper Zero")
    parser.add_argument("-i", "--input", required=True, help="Percorso al file .dmp")
    parser.add_argument("-o", "--output", required=True, help="Percorso di output .nfc")
    parser.add_argument("--uid", help="UID personalizzato (es: FE:3B:17:86)")
    parser.add_argument("--atqa", help="ATQA personalizzato (es: 04 00)")
    parser.add_argument("--sak", help="SAK personalizzato (es: 88)")
    args = parser.parse_args()

    convert_dump_to_flipper_format(
        dump_file=args.input,
        output_file=args.output,
        uid=args.uid,
        atqa=args.atqa,
        sak=args.sak
    )
