from backend import app
import os
app = app.run(port=os.environ['PORT'])