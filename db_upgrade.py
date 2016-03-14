#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)


def rollback(count):
    if (rollbacks > v) or (rollbacks < 0):
        print "Invalid rollbacks count. Current version is %d." % v
        rollbacks = int(raw_input("Input valid count:"))
        rollback(rollbacks)
    else:
        api.downgrade(SQLALCHEMY_DATABASE_URI,
                      SQLALCHEMY_MIGRATE_REPO,
                      v - count)
        print ('Current database version: ' + 
               str(api.db_version(SQLALCHEMY_DATABASE_URI,
                                  SQLALCHEMY_MIGRATE_REPO)))

print ('Current database version: ' + 
       str(api.db_version(SQLALCHEMY_DATABASE_URI,
                              SQLALCHEMY_MIGRATE_REPO)))

rb = int(raw_input("Input number of rollbacks:"))
rollback(rb)