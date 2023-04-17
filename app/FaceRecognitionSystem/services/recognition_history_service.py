from elasticsearch import Elasticsearch
import configparser
config = configparser.ConfigParser()
config.read('example.ini')
es = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)

# Lấy nhật ký nhận dạng


def getAuditLog(skip, take, startDate, toDate, search, user):
    query = {
        "bool": {
            "must": [
                {
                    "range": {
                        "CreatedDate": {
                            "gte": f'{startDate}',
                            "lte": f'{toDate}'
                        }
                    }
                }

            ]
        }
    }
    sort = [
        {
            "CreatedDate": "DESC"
        }
    ]
    if search and len(search) > 0:
        query["bool"]["must"].append({
            "multi_match": {
                "query": search,
                "fields": ["FullName", "Email", "UserName"],
                "operator": "or"
            }
        })
    if not user.IsMasterAccount:
        query["bool"]["must"].append({
            "match": {
                "UserName": user.UserName
            }
        })
        pass
    
    app_id = user.CustomerID
    index = f"{config['DEFAULT']['audit_index']}{ f'_{app_id}' if app_id else ''}*"
    response = es.search(query=query, index=index,
                         sort=sort, size=take, from_=skip)
    return response
