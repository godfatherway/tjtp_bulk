import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s - %(asctime)s] %(message)s",
    datefmt='%H:%M:%S'
)

NULL_BYTES = b'\x00' * 16
INCOMPATIBLE_VERSION = b'\x56\x31\x2E\x30\x31'

def extract_tjt(filename: str) -> None:
    logging.info(f"Attempting to open file: {filename}")
    with open(filename, "rb") as file_to_read:
        current_directory = os.getcwd()
        base_name = os.path.basename(filename)
        base_name_parts = os.path.splitext(base_name)
        directory_name = base_name_parts[0]
        counter = 1
        try:
            os.mkdir(directory_name)
        except FileExistsError:
            logging.warning(f'"{directory_name}" has already been extracted. Will be skipping')
            return
        os.chdir(directory_name)
        file_to_read.seek(2)
        version_bytes = file_to_read.read(5)

        if version_bytes != INCOMPATIBLE_VERSION:
            logging.error("This is not an extractable version. Stopping the program.")
            exit()

        while True:
            file_to_read.seek(28 + 128 * counter - (16 - 4 * (counter - 1)))
            file_header = file_to_read.read(16)
            
            if file_header != NULL_BYTES:
                break
            counter += 1
        data_offset = 48 + 128 * counter - (16 - 4 * (counter - 1)) + 20
        counter = 1
        logging.info(f"Extracting: {filename}")

        while True:
            file_to_read.seek(28 + 128 * counter - (0 - 4 * (counter - 1)) - 128)
            name_bytes = file_to_read.read(128)
            file_to_read.seek(28 + 128 * counter - (16 - 4 * (counter - 1)))
            file_header = file_to_read.read(16)

            if file_header != NULL_BYTES:
                os.chdir(current_directory)
                break
            file_name = name_bytes.split(b'\0', 1)[0].decode('ascii').split('\\')[-1]
            with open(file_name, 'bw') as new_file:
                file_to_read.seek(28 + 128 * counter - (16 - 4 * (counter - 1)) + 16)
                hex_size = file_to_read.read(4).hex()
                f1 = hex_size[0:2]
                f2 = hex_size[2:4]
                f3 = hex_size[4:6]
                f4 = hex_size[6:8]
                file_size = int(f4 + f3 + f2 + f1, base=16)
                file_to_read.seek(data_offset - 152)
                data = file_to_read.read(file_size)
                new_file.write(data)
            data_offset += file_size
            counter += 1

def main(user_input: str) -> None:
    files: list
    if os.path.isdir(user_input):
        files = [f for f in os.listdir(user_input) if os.path.isfile(os.path.join(user_input, f)) and f.lower().endswith('.tjt')]
        logging.info(f"Found {len(files)} .tjt files in directory: {user_input}")
        files = [os.path.join(user_input, f) for f in files]  # Create full paths
    else:
        files = [user_input]  # very lazy way to handle file and directories.

    for file in files:
        logging.info(f"Processing file: {file}")
        extract_tjt(file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Input not given. Quitting")
        exit()
    user_input = sys.argv[1]
    main(user_input)