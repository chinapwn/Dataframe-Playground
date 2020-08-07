# This is the main point for visualizations.
# Parse all relevant dataframes to this module and decide what plugin to use with route().

def route(collection, df, plugin):
    import importlib
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    print(plugin)
    plugin_module = importlib.import_module("plugins.{}".format(plugin['name']))
    visualization = {}
    visualization['plugin_name'] = plugin['name']
    visualization['plugin_id'] = str(plugin['_id']['$oid'])
    visualization['link'] = plugin_module.main(df)
    print('vis_links: ', visualization)
    return visualization