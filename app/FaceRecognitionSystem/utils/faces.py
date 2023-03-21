from  deepface import DeepFace
from elasticsearch import Elasticsearch, helpers
import configparser
import time
config = configparser.ConfigParser()
config.read('example.ini')
es = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)
# print(es.info())

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]



#Hàm tạo vector embeding
#input: 
#       img: là đường dẫn ảnh, vector numpy hoặc base64
#       code: mã số là duy nhất đại diện cho người đó
#       name: tên của người lấy mẫu
#       saveToElk: biến đánh dấu xem cớ lưu lên elk hay không
#output: vector emmbeding 512 chiều
#created by dvanh(30/03/2023)
def CreateEmbeding(img, code,name ):
    vector =  DeepFace.represent(img, model_name = models[2],detector_backend='mediapipe')
    doc ={
            'face_name':name,
            'face_code':code,
            'face_encoding':vector[0].get('embedding')
        }   
    response = es.index(index=config['DEFAULT']['db_index'],document=doc)
    return response




#Tìm xem một khuôn mặt có trong cơ sở dữ liệu của elastic seach hay không
#created by:dvanh(21/03/2023)
#imput image dạng base65, numpy array, img path
def  FindFace(img):
    t=time.time()
    face_encoding = DeepFace.represent(img, model_name = models[2],detector_backend='mediapipe')
    query={
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'face_encoding')",
                    "params": {
                    "query_vector": face_encoding[0].get('embedding')
                    }
                }
                }
        }
    sort=[
        {
        "_score":"DESC"
        }
    ]
    size=1
    response  = es.search(query=query,index=config['DEFAULT']['db_index'],sort=sort,size=size)
    print(time.time()-t)

    if len(response['hits']['hits'])==0:
        return None
    
    return{
        'face_score':response['hits']['hits'][0]['_score'],# Độ chính xác 0->1
        'face_name':response['hits']['hits'][0]['_source']['face_name'],#Tên người đó
        'face_code':response['hits']['hits'][0]['_source']['face_code'],#Mã định danh
    }


