from backend import app
import os
app = app.run(host='0.0.0.0', port=os.environ.get('PORT',33507))