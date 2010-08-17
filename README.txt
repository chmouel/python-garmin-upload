DESCRIPTION:

A simple library allow you to upload tcx file to Garmin Connect

LICENSE: BSD

EXAMPLE:

# Make sure you have MultipartPostHandler.py in your path as well
import UploadGarmin

# Create object
g = UploadGarmin()

#LOGIN
g.login("username", "password")

#UPLOAD CTX file
wId = g.upload_ctx('/tmp/a.ctx')

#Name last workout
g.name_workout(wId, "TestWorkout")

# Author
Chmouel Boudjnah <chmouel@chmouel.com
