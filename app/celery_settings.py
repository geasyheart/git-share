CELERY_ACCEPT_CONTENT = ['json', 'msgpack']  # 保存的格式,目前知道的是以pickle序列化后的结果进行保存
CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化使用msgpack方案
CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

# broker的地址
BROKER_URL = 'amqp://zy:123456@192.168.1.158:5672//'

CELERY_RESULT_BACKEND = "rpc"

# 时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
