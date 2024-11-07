from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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
    import httpx
    GITHUB_API_URL = "https://api.github.com/search/users"
    GITLAB_API_URL = "https://gitlab.com/api/v4/users"

    async with httpx.AsyncClient() as client:
        github_response = await client.get(GITHUB_API_URL, params={"q": query})
        github_users = github_response.json()["items"]

        gitlab_response = await client.get(GITLAB_API_URL, params={"username": query})
        gitlab_users = gitlab_response.json()
        
    print(github_users)
    print(gitlab_users)
    
    for user in gitlab_users:
        print(user)
    
    users = {
       "github": [{"username": user["login"], "url": user["html_url"]} for user in github_users],
       "gitlab": [{"username": user["username"], "url": user["web_url"]} for user in gitlab_users],
    }
    return users

