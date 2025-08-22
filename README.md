Deli-Q app notes

Local dev:
(deli_queue_py_env) PS C:\Users\sebas\python_projects\deli_queue_py> python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
Guest Web App: http://localhost:8000/guest
Admin Panel: http://localhost:8000/admin
Attendant Panel: http://localhost:8000/attendant
Clicker Panel: http://localhost:8000/clicker
Queue Status API: http://localhost:8000/status

Hosted demo sites:
https://deli-queue-static.s3.eu-north-1.amazonaws.com/admin_control_panel.html
Configure settings here

https://deli-queue-static.s3.eu-north-1.amazonaws.com/status_dashboard.html
Queue monitoring

https://deli-queue-static.s3.eu-north-1.amazonaws.com/attendant_web_app.html
QR scanner and clicker

https://deli-queue-static.s3.eu-north-1.amazonaws.com/clicker_web_app.html
Venue exit clicker

https://deli-queue-static.s3.eu-north-1.amazonaws.com/guest_web_app.html
Guest web app
