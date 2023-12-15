import requests
import json
import time
from tqdm import tqdm
from dataclasses import dataclass

def get_payload(submission_id):
    return {"query": """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtimePercentile
    memoryPercentile
  }
}""",
  "variables": {"submissionId": submission_id},
  "operationName": "submissionDetails"
}

COOKIES = None
def get_cookie():
    global COOKIES
    if COOKIES is None:
        COOKIES = json.load(open("leetcode.cookies"))
    return COOKIES

# Get the runtime and memory percentile of a submission
def get_submission_details(submission_id):
    url = "https://leetcode.com/graphql/"
    payload = get_payload(submission_id)
    response = requests.get(url, cookies=get_cookie(), json=payload)
    data = response.json()["data"]["submissionDetails"]
    return (data["runtimePercentile"], data["memoryPercentile"])

sleep_time = 1

# Get a set of submission using the offset and lastkey
def get_submission(offset, lastkey):
    url = f"https://leetcode.com/api/submissions/?offset={offset}&limit=20&lastkey={lastkey}"
    response = requests.get(url, cookies=get_cookie())
    return response.json()

# Get all submissions of a user
def get_all_submissions():
    offset = 0
    lastkey = ""
    submissions = []
    while True:
        data = get_submission(offset, lastkey)
        submissions += data["submissions_dump"]
        if not data["has_next"]:
            break
        lastkey = data["last_key"]
        offset += 20
        time.sleep(sleep_time)
    return submissions

@dataclass
class SubmissionDetail:
    id: int
    runtime_percentile: float
    memory_percentile: float
    language: str

# Get all submission details, including runtime and memory percentile
def get_all_submission_details() -> list[SubmissionDetail]:
    print("Getting submissions...")
    submissions = get_all_submissions()
    submission_details = []
    for submission in tqdm(submissions, "Getting language info"):
        if not submission["status_display"] == "Accepted":
            continue
        submissionID = submission["id"]
        language = submission["lang"]
        runtime, memory = get_submission_details(submissionID)
        submission_details.append(SubmissionDetail(submissionID, runtime, memory, language))
        time.sleep(sleep_time)
    return submission_details
