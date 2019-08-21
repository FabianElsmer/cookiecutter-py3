import bson

async def test_dockerdb_mongo(client, database):
    """ Make sure the database gets wiped and mongodb is accessible """
    client = await client
    app = client.app

    unique_id = bson.objectid.ObjectId()
    document = {'unique': unique_id}

    # database is a pymongo client
    await database.test_collection.insert_one(document)
    found = await database.test_collection.find({}).to_list(None)

    assert len(found) == 1
    assert found[0]['unique'] == unique_id

    # App uses an AsyncIOMotorClient
    found = await app['db']['test_collection'].find({}).to_list(None)

    assert len(found) == 1
    assert found[0]['unique'] == unique_id
