"""
Upload Garmin

Handle the operation to upload to the Garmin Connect Website.

"""
import urllib2
import urllib
import MultipartPostHandler
import simplejson

class UploadGarmin:
    """
    Upload Garmin

    Handle operation to open to Garmin
    """
    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(),
                                           MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(self.opener)

    def login(self, username, password):
        """
        Login to garmin

        @ivar username: Garmin USERNAME
        @type username: str
        @ivar password: Garmin PASSWORD
        @type password: str
        """

        params = {'javax.faces.ViewState': 'j_id1',
                  'login': 'login',
                  'login:loginUsernameField' : username,
                  'login:password': password,
                  'login:signInButton': 'Sign In'}
        params = urllib.urlencode(params)

        #GO Figure out!
        self.opener.open('https://connect.garmin.com/signin').read()
        
        status = self.opener.open('https://connect.garmin.com/signin', params)
        vary_header = status.headers['vary']
        status.close()

        #Hacky but that's the only way I can know if succeed or not
        if 'X-Secure' in vary_header:
            raise Exception("Invalid Login or Password")


    def upload_ctx(self, ctx_file):
        """
        Upload a CTX File

        You need to be logged already

        @ivar ctx_file: The CTX file name to upload
        @type ctx_file: str
        """
        params = {
            "responseContentType" : "text%2Fhtml",
            "data" : open(ctx_file)
        }
        
        output = self.opener.open('http://connect.garmin.com/proxy/upload-service-1.1/json/upload', params)
        if output.code != 200:
            raise Exception("Error while uploading")
        json = output.read()
        output.close()

        return simplejson.loads(json)["detailedImportResult"]["successes"][0]["internalId"]

    def name_workout(self, workout_id, workout_name):
        """
        Name a Workout

        Note: You need to be logged already

        @ivar workout_id: Workout ID to rename
        @type workout_id: int
        @ivar workout_name: New workout name
        @type workout_name: str

        """
        params = dict(value=workout_name)
        params = urllib.urlencode(params)
        output = self.opener.open('http://connect.garmin.com/proxy/activity-service-1.0/json/name/%d' % (workout_id), params)
        json = output.read()
        output.close()

        if simplejson.loads(json)["display"]["value"] != workout_name:
            raise Exception("Naming workout has failed")

    def workout_url(self, workout_id):
        """
        Get the Workout URL

        @ivar workout_id: Workout ID
        @type workout_id: int
        """
        return "http://connect.garmin.com/activity/" % (int(workout_id))
        
if __name__ == '__main__':
    g = UploadGarmin()
    g.login("username", "password")
    wId = g.upload_ctx('/tmp/a.ctx')
    g.name_workout(wId, "TestWorkout")
