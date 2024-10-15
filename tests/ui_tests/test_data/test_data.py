from ui.enum.news_tags import NewsTags

test_data = {
    "news_data_valid": {
        "title": "Title 1",
        "content": "Title 1 Title 1 Title 1 Title 1",
        "tags": [NewsTags.NEWS, NewsTags.EVENTS]
    },
    "news_publish": {
        "title": "Workshop to educate your customers about eco-friendly living",
        "content": "Workshop to educate your customers about eco-friendly living",
        "tags": [NewsTags.EVENTS]
    },
    "title_length":{
        "title": "Celebrating World Water Day: The Coral Triangle. Water benefits not only humans but all animals and natural life that exists above and below the surface. Water benefits!!",
        "content": "Celebrating World Water Day: The Coral Triangle",
        "tags": [NewsTags.EVENTS]
    },
"author_field":{
        "title": "Coffee takeaway with 40% discount",
        "content": "It's so healthy, fun and cool to bring eco habits into everyday life",
        "tags": [NewsTags.EVENTS]
    }
}

