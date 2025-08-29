# a comment to get started
# Testing Git commit functionality - added this comment to verify repository setup
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import boto3
from mangum import Mangum

# my modules
# from queue_controller import QueueController
from queue_instance import queue
from routes import router


app = FastAPI(title="Virtual Queue System")

# CORS for S3/CloudFront-hosted frontends
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/daily-reset")
def daily_reset():
    """Manually trigger daily reset"""
    result = queue.daily_reset()
    return result


@app.post("/scan")
async def scan_guest(request: Request):
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")
    queue.scan_guest(email)
    return {"message": "Guest scanned and removed from queue"}


@app.post("/upload-config")
async def upload_config(request: Request):
    """Upload customer configuration to S3"""
    try:
        data = await request.json()
        customer_name = data.get("customerName")
        config_content = data.get("configContent")

        if not customer_name or not config_content:
            raise HTTPException(
                status_code=400, detail="Missing customerName or configContent"
            )

        # Upload to S3
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get("CONFIG_BUCKET_NAME", "deli-queue-configs")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"configs/{customer_name}_config.js",
            Body=config_content,
            ContentType="application/javascript",
            CacheControl="no-cache",
        )

        return {"message": f"Configuration uploaded to S3 for {customer_name}"}

    except Exception as e:
        print(f"Error uploading config to S3: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to upload config: {str(e)}"
        )


@app.get("/list-configs")
async def list_configs():
    """List available customer configurations from S3"""
    try:
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get("CONFIG_BUCKET_NAME", "deli-queue-configs")

        # List objects with configs/ prefix
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="configs/")

        configs = []
        if "Contents" in response:
            for obj in response["Contents"]:
                # Extract customer name from key (e.g., "configs/customer1_config.js" -> "customer1")
                key = obj["Key"]
                if key.endswith("_config.js"):
                    customer_name = key.replace("configs/", "").replace(
                        "_config.js", ""
                    )
                    configs.append(customer_name)

        return {"configs": configs}

    except Exception as e:
        print(f"Error listing configs from S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list configs: {str(e)}")


@app.get("/download-config/{customer_name}")
async def download_config(customer_name: str):
    """Download customer configuration from S3"""
    try:
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get("CONFIG_BUCKET_NAME", "deli-queue-configs")

        response = s3_client.get_object(
            Bucket=bucket_name, Key=f"configs/{customer_name}_config.js"
        )

        config_content = response["Body"].read().decode("utf-8")
        return {"configContent": config_content}

    except Exception as e:
        print(f"Error downloading config from S3: {str(e)}")
        raise HTTPException(
            status_code=404, detail=f"Configuration not found for {customer_name}"
        )


@app.post("/migrate-configs")
async def migrate_configs():
    """Migrate existing configurations from old S3 bucket to new config bucket"""
    try:
        old_s3_client = boto3.client("s3")
        new_s3_client = boto3.client("s3")

        old_bucket = os.environ.get("S3_BUCKET_NAME", "deli-queue-static")
        new_bucket = os.environ.get("CONFIG_BUCKET_NAME", "deli-queue-configs")

        # List objects with configs/ prefix from old bucket
        response = old_s3_client.list_objects_v2(Bucket=old_bucket, Prefix="configs/")

        migrated_count = 0
        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if key.endswith("_config.js"):
                    # Download from old bucket
                    old_response = old_s3_client.get_object(Bucket=old_bucket, Key=key)
                    config_content = old_response["Body"].read()

                    # Upload to new bucket
                    new_s3_client.put_object(
                        Bucket=new_bucket,
                        Key=key,
                        Body=config_content,
                        ContentType="application/javascript",
                        CacheControl="no-cache",
                    )
                    migrated_count += 1

        return {"message": f"Migrated {migrated_count} configurations to new bucket"}

    except Exception as e:
        print(f"Error migrating configs: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to migrate configs: {str(e)}"
        )


# AWS Lambda handler for API Gateway
handler = Mangum(app)
