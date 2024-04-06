import sys
import re
import requests

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'

def extract_activity_id(url):
    match = re.search(r'/activity/([^/]+)/exercise', url)
    if match:
        return match.group(1)
    return None

def get_full_url_from_file(activity_id):
    with open('final_correct_response.txt', 'r') as file:
        for line in file:
            if activity_id in line:
                return line.strip()
    return None

def fetch_correct_answer(full_url):
    headers = {
        'Host': 'app.ofppt-langues.ma',
        'X-Device-Uuid': 'c4369295-36a2-4d7b-bd6f-d805f76a5a60',
        'X-Altissia-Token': '1c9b5e0c51828d85bedbf26b940ffa7bdc5aa8c0407002c234e6c23ccd8087fc',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        if 'content' in content and 'items' in content['content'] and content['content']['items']:
            correct_answers_list = []
            if 'content' in content and 'items' in content['content']:
                for item in content['content']['items']:
                    correct_answers = item.get('correctAnswers')
                    if correct_answers:
                        correct_answers_list.extend(correct_answers)
            # Flatten the list of lists
            flattened_correct_answers = [answer for sublist in correct_answers_list for answer in sublist]
            return flattened_correct_answers
    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]

    # Extracting activity ID from URL
    activity_id = extract_activity_id(url)
    if activity_id is None:
        print(f"{RED}Invalid URL format.{NC}")
        sys.exit(1)

    # Searching for full URL in the file
    full_url = get_full_url_from_file(activity_id)
    if full_url:
        output = fetch_correct_answer(full_url)
        if output:
            print(f"\n{RED}Powered By Mchklt & Wsm Eb:{NC}\n\n{GREEN}Script khdam binajah: {NC}\n")
            for i in output:
                print(i)
        else:
            print(f"\n{RED}No result found in file.{NC}")
    else:
        print(f"\n{RED}Result not found in file.{NC}")
