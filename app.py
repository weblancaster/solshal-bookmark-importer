"""
Solshal bookmark importer service
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/import/chrome", methods=["POST"])
def chrome_importer():
    """Get data in the request and pass to formatter
    then return formatted data to Solshal
    
    Decorators:
        app
    
    Returns:
        [List] -- List of folders and it's collections
    """
    bookmarks = request.get_json()["bookmarks"]
    formattedData = get_collections(bookmarks)

    return jsonify({
        "data": formattedData
    }), 200

def filter_folders(folders):
    """Filter folders that only contain collections
    
    Arguments:
        folders {[Dict]} -- Folders containing collections
    
    Returns:
        [List] -- List of folders and it's collections
    """
    # List containing folders and it's collections
    filteredFolders = []
    for key in folders:
        current = folders[key]
        if not current["collections"]:
            continue
        
        filteredFolders.append({
            "folder_name": current["title"],
            "collections": current["collections"]
        })
    
    return filteredFolders

def get_collections(data):
    """Traverse a tree of collection find folders and it's bookmarks
    then flatten them out
    
    Arguments:
        data {[List]} -- bookmark list tree
    """
    # Dict containing all folders and it's bookmarks collection
    flattenedFolders = {}

    def flatten_folders(bookmarks):
        for collection in bookmarks:
            if not "url" in collection:
                folderId = collection["id"]
                flattenedFolders[folderId] = {
                    "title": collection["title"],
                    "collections": []
                }

            if "url" in collection:
                parentId = collection["parentId"]
                flattenedFolders[parentId]["collections"].append({
                    "url": collection["url"],
                    "title": collection["title"]
                })
                continue
            
            if "children" in collection:
                flatten_folders(collection["children"])
    
    flatten_folders(data)
    return filter_folders(flattenedFolders)

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = os.getenv("PORT", 5001)
    app.run(
        host=HOST,
        port=PORT
    )

