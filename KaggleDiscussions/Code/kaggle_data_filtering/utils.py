from core import ItemDetails


def getIds(json_data):
    topic_ids = []
    topic_items = json_data["topics"]
    for topic_item in topic_items:
        topic_ids.append(topic_item["id"])

    return topic_ids


def getItemDetails(json_data):
    topic_id = json_data["id"]
    competition = json_data["parentName"]
    overview = json_data["comment"]["content"]
    comments = getComments(json_data["commentList"]["comments"])
    name_author = json_data["comment"]["author"]["displayName"]
    datentime = json_data["comment"]["postDate"]
    votes = json_data["comment"]["votes"]

    # item_details = ItemDetails(topic_id, title, overview, comments)
    item_details = ItemDetails(topic_id, competition, name_author, datentime, overview, comments, votes)

    return item_details


def getComments(list_of_comments):
    comments_list = []
    for comment in list_of_comments:
        comments_list.append(comment["content"])

        if comment["replies"]:
            comments_list.append(getComments(comment["replies"]))

    return "".join(comments_list).replace("<p>", "").replace("<\p>", "")


def transform(item):
    if isinstance(item, ItemDetails):
        return item.__dict__
    return item
