### === https://github.com/darklytornadoxd === ###

import requests
import re
import threading
import time

def process_line(line):
    url = f"https://rapiddns.io/s/{line.strip()}#result"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        start_element = '<div class="progress-table-wrap d-flex align-items-left ">'
        end_element = '<section class="about-area ">'
        pattern = re.compile(f'{re.escape(start_element)}(.*?){re.escape(end_element)}', re.DOTALL)
        match = pattern.search(content)
        if match:
            captured_content = match.group(1)
            tlds = [".com", ".org", ".net", ".co.uk", ".co.au", ".gov", ".de", ".cn", ".ca", ".es", ".fr", ".fi", ".ro", ".ru", ".nl", ".mx"]
            filtered_lines = [line for line in captured_content.splitlines() if any(tld in line for tld in tlds)]
            filtered_lines = [line.replace('<td>', '').replace('</td>', '') for line in filtered_lines]
            with open('results.txt', 'a') as result_file:
                for filtered_line in filtered_lines:
                    result_file.write(filtered_line + '\n')

def read_and_process_lines():
    with open('input.txt', 'r') as input_file:
        lines = input_file.readlines()
        threads = []
        for line in lines:
            if line.strip():
                thread = threading.Thread(target=process_line, args=(line,))
                threads.append(thread)
                thread.start()
                time.sleep(1)
        for thread in threads:
            thread.join()

def main():
    read_and_process_lines()

if __name__ == "__main__":
    main()