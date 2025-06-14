import sys
import subprocess
import shutil
import filecmp
import os

test_cases_path = "./customtests/"
input_path = test_cases_path + "in/"
output_path = test_cases_path + "out/"

input_files_path = test_cases_path + "file_in/"
output_files_path = test_cases_path + "file_out/"

out_local = "binario_tela"

def main():
    test_case = input_path + sys.argv[1] + ".in"
    expected = output_path + sys.argv[1] + ".out"

    with open(test_case, 'r') as file:
        lines = file.readlines() 
        filename = lines[0].split()[1]
        if (os.path.isfile(input_files_path + filename)):
            shutil.copy(input_files_path + filename, ".")
        file.seek(0)

        # Opening file and passing correct input to executable
        with open(out_local, 'w') as file_out:
            result = subprocess.run('./exec', stdin=file, text=True, capture_output=True)
            file_out.write(result.stdout)

        # If correct, clean up
        if filecmp.cmp(out_local, expected, shallow=False):
            print('Passou no teste!')
            os.remove(out_local)
            if (os.path.isfile(input_files_path + filename)):
                os.remove(filename)
        # if not, hex vimdiff then clean up
        else:
             filename_hex = filename + '.hex'
             expected_hex = filename + '.hexpected'
             # creating hex files
             with open(filename_hex, 'w') as hex_local:
                 subprocess.run(['xxd', filename], stdout=hex_local)
             with open(expected_hex, 'w') as hex_correct:
                 subprocess.run(['xxd', output_files_path + filename] , stdout=hex_correct)

             subprocess.run(['vimdiff', filename_hex, expected_hex])

             # cleanup
             subprocess.run(['cat', out_local]) 
             os.remove(out_local)
             os.remove(filename)
             os.remove(filename_hex)
             os.remove(expected_hex)

if __name__ == "__main__":
    main()
