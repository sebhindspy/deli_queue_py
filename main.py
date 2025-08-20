# a comment to get started
# Testing Git commit functionality - added this comment to verify repository setup
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import json

# my modules
# from queue_controller import QueueController
from queue_instance import queue
from routes import router


app = FastAPI(title="Virtual Queue System")

# Create an instance of the controller
# queue = QueueController()

# Include API routes
app.include_router(router)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve static HTML files


@app.get("/status")
def get_status(pretty: bool = False):
    base_status = queue.get_status()
    response_data = {
        **base_status,
        "total_guests": len(base_status["queue"]),
        "next_guest": base_status["queue"][0] if base_status["queue"] else None,
    }

    if pretty:
        pretty_json = json.dumps(response_data, indent=4)
        return PlainTextResponse(content=pretty_json, media_type="application/json")
    return response_data


@app.get("/guest")
def serve_guest():
    return FileResponse("guest_web_app.html")


@app.get("/attendant")
def serve_attendant():
    return FileResponse("attendant_web_app.html")


@app.get("/admin")
def serve_admin():
    return FileResponse("admin_control_panel.html")


@app.get("/clicker")
def serve_clicker():
    return FileResponse("clicker_web_app.html")


@app.get("/payment")
def get_payment_mock():
    return FileResponse("payment_mock.html")


@app.post("/set-premium-limit")
def set_premium_limit(data: dict):
    queue.set_premium_limit(data["limit"])
    return {"message": "Premium limit updated"}


@app.post("/set-one-shot-price")
def set_one_shot_price(data: dict):
    queue.set_one_shot_price(data["price"])
    return {"message": "One shot price updated"}


@app.post("/join-premium")
async def join_premium(request: Request):
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")
    queue.join_premium_queue(email)
    return {"message": "Premium join successful"}


@app.post("/set-ready-pool-limit")
def set_ready_pool_limit(data: dict):
    limit = data.get("limit")
    if limit is None:
        raise HTTPException(status_code=400, detail="Limit is required.")
    if not isinstance(limit, int) or limit < 0:
        raise HTTPException(
            status_code=400, detail="Limit must be a non-negative integer."
        )
    queue.set_ready_pool_limit(limit)
    return {"message": "Ready pool limit updated"}


@app.post("/scan")
async def scan_guest(request: Request):
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")
    queue.scan_guest(email)
    return {"message": "Guest scanned and removed from queue"}
