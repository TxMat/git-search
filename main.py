from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

app = FastAPI()

# Mount the static directory to serve CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML page
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# Your existing search endpoint
@app.get("/search")
async def search_users(query: str):
    logger.info(f"Searching for '{query}'")
    import httpx
    GITHUB_API_URL = "https://api.github.com/search/users"
    GITLAB_API_URL = "https://gitlab.com/api/v4/users"

    async with httpx.AsyncClient() as client:
        github_response = await client.get(GITHUB_API_URL, params={"q": query})
        github_users = github_response.json()["items"]

        gitlab_response = await client.get(GITLAB_API_URL, params={"username": query})
        gitlab_users = gitlab_response.json()

    if len(github_users) == 0 and len(gitlab_users) == 0:
        logger.error("No users found")
    else:
        logger.info(f"Found: {len(github_users) + len(gitlab_users)} Users")

    if len(github_users) > 0:
        logger.info(f"{len(github_users)} from GitHub")
    else:
        logger.warning("No Users on GitHub")

    if len(gitlab_users) > 0:
        logger.info(f"{len(gitlab_users)} from GitLab")
    else:
        logger.warning("No Users on GitLab")

    users = {
       "github": [{"username": user["login"], "url": user["html_url"], "avatar": user["avatar_url"] } for user in github_users],
       "gitlab": [{"username": user["username"], "url": user["web_url"], "avatar": user["avatar_url"]} for user in gitlab_users],
    }
    return users

