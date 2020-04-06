import datetime
import os
def set_filename_format(now, instance, filename):
    """ file format setting e.g) {username}-{date}-{microsecond}{extension} hjh-2016-07-12-158859.png """
    return "{username}-{date}-{microsecond}{extension}".format(username=instance.id, date=str(now.date()), microsecond=now.microsecond, extension=os.path.splitext(filename)[1], )


def user_directory_path(instance, filename):
    """ image upload directory setting e.g) images/{year}/{month}/{day}/{username}/{filename} images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    now = datetime.datetime.now()
    path = "images/{year}/{month}/{day}/{username}/{filename}".format(year=now.year, month=now.month, day=now.day, username=instance.id, filename=set_filename_format(now, instance,filename), )

    return path