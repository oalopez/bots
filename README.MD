Usage

1. Prepare Your Directory
Ensure that you have a directory containing the following JSON configuration files:

- output.json
- extractor.json
- transformer.json

These files should be placed in the directory you will pass to the script.

3. Running the Script
Open a terminal or command prompt, then navigate to the directory containing main.py:
cd path/to/your/directory/bots

Run the script by specifying the path to the base directory containing your JSON files:
python bot.py /path/to/your/base_directory

4. Script Overview
- The script will begin processing the files in the specified directory.
- It uses argparse to accept the base directory as an argument.
- The script performs data extraction, transformation, and output based on the JSON configuration files.
- Progress is displayed using a tqdm progress bar.

5. Troubleshooting
- Ensure that all dependencies (tqdm, requests) are installed.
- Verify that the JSON files are correctly formatted and exist in the specified directory.
- Make sure you are using the correct path to the base directory when running the script.