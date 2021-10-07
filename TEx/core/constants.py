"""Constants File."""

from typing import Dict

SINGLE_FB_PROFILE_DATA_ITEM: Dict = {
    'id': '',  # Facebook ID
    'friends': [],  # List of SINGLE_FB_FRIEND_DATA_ITEM
    'family': []
    }

SINGLE_INSTAGRAM_PROFILE_DATA_ITEM: Dict = {
    'fullname': '',
    'profile_pic': '',
    'id': '',  # Instagram ID
    'followers': [],  # List of SINGLE_INSTAGRAM_FRIEND_DATA_ITEM
    'following': []  # List of SINGLE_INSTAGRAM_FRIEND_DATA_ITEM
    }

SINGLE_FB_FRIEND_DATA_ITEM: Dict = {
    'name': '',
    'id': '',
    'path': '',
    'profile_pic': ''
    }

SINGLE_INSTAGRAM_FRIEND_DATA_ITEM: Dict = {
    'name': '',
    'id': '',
    'path': '',
    'profile_pic': ''
    }
