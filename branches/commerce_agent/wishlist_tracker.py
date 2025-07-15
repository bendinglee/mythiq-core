wishlist = {}

def add_to_wishlist(user_id, item):
    wishlist.setdefault(user_id, []).append(item)
    return { "wishlist": wishlist[user_id] }

def get_wishlist(user_id):
    return wishlist.get(user_id, [])
