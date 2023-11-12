import requests

BASE_URL = "https://leetcode.com"

query = f"""query ($offset: Int!, $limit: Int!, $slug: String) {{
    submissionList(offset: $offset, limit: $limit, questionSlug: $slug) {{
        hasNext
        submissions {{ id lang time timestamp statusDisplay runtime url isPending title memory titleSlug }}
    }}
}}"""

