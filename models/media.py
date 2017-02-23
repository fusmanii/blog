from mongoengine import Document, connect, FileField, StringField
from PIL import Image
import io

DB_NAME = 'blog'

class MongoMedia(Document):
    ''' Media using mongoengine for image storing.
    '''

    permalink = StringField(required=True)
    imageFilename = StringField()
    image = FileField()
    thumb = FileField()

class Media:
    ''' Media DAO. 	
    '''

    def insert(self, permalink, file, filename, filetype):
        ''' (Media, str, file, str, type) -> NoneType
        Inserts the image in the file file into the database of 
        post with permanent link permalink. 
        '''

        media = MongoMedia()
        media.permalink = permalink
        media.imageFilename = filename

        media.image.put(file, content_type=filetype)

        # create the thumbnail
        image = Image.open(media.image)
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = io.BytesIO()
        image.save(data, image.format)
        data.seek(0)
        media.thumb.put(data, content_type=filetype)
        media.save()
        data.close()

    def getMediaByPermalink(self, permalink, imageType):
        ''' (Media, str, str) -> mongoengine.fields.GridFSProxy
        Returns the media (full image or thumbnail) with the permalink permalink.
        '''

        print("QUery:", MongoMedia.objects(permalink=permalink)[0][imageType])
        return MongoMedia.objects(permalink=permalink)[0][imageType]

connect(DB_NAME)
media = Media()
