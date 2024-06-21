import json
import sys
import time
import logging
import os
import getpass
from pymongo import MongoClient


logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='## %Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

p4_workspace_name = ""

class MongoCtl:
    mongo_url_dev = "mongodb://mongouser:cfrwebsvr#123@9.135.110.244:27017"
    mongo_url_idc ="mongodb://admin:cfrwebsvr123@11.153.66.142:27017"

    def __init__(self) -> None:
        self.dbname = "test" # db 名字
        self.collection_name = "user" # 集合名字
        self.collection_size = 100 * 1024 * 1024 # 固定集合大小
        try:
            # 尝试连接到MongoDB
            self.client = MongoClient(MongoCtl.mongo_url_dev) # mongodb 客户端
            # 判断连接是否成功
            if self.client.server_info():
                print("mongodb connect succ")
            else:
                print("mongodb connect fail")
                exit
        except ConnectionError as e:
            print(f"mongodb connect fail: {e}")
            exit

        self.db = self.client[self.dbname] # 数据库对象
        self.set = self.db[self.collection_name] # 集合对象

        # 集合不存在，创建
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name, capped=True, size=self.collection_size)
            logger.info("collection_name:%s create", self.collection_name)

        logger.info("mongo-client connected")

    def __del__(self) -> None:
        self.client.close()
        logger.info("mongo-client close")

    def get_last_change_num(self) -> str:
        last_change_num = ""
        last_inserted = self.set.find({"P4WorkspaceName": p4_workspace_name}).sort([("$natural", -1)]).limit(1)
        last_inserted = list(last_inserted)
        if len(last_inserted) > 0:
            last_change_num = last_inserted[0]["current_change_num"]
        return last_change_num

class PackDocument:
    def __init__(self) -> None:
        self.P4WorkspaceName = "" # p4 工作空间
        self.package_version = "" # 例如：0.101.2.0
        self.last_change_num = ""
        self.current_change_num = ""
        self.start_build_time = ""
        self.end_build_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.pack_revision_info = ""

    def doc_info(self) -> dict:
        map = dict()
        map.update(self.doc_info_head())
        map["pack_revision_info"] = self.pack_revision_info
        return map

    def doc_info_head(self) -> dict:
        map = dict()
        map["P4WorkspaceName"] = self.P4WorkspaceName
        map["package_version"] = self.package_version
        map["last_change_num"] = self.last_change_num
        map["current_change_num"] = self.current_change_num
        map["start_build_time"] = self.start_build_time
        map["end_build_time"] = self.end_build_time
        return map

    def get_file_path(self) -> str:
        file_name = self.P4WorkspaceName + "_" + self.current_change_num + ".log"
        return file_name

    def dump_to_json(self):
        file_name = self.get_file_path()
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w") as file:
            json.dump(self.doc_info(), file)

    def load_from_json(self) -> dict:
        file_name = self.get_file_path()
        if not os.path.exists(file_name):
            logger.error("%s not exist"%(file_name))
            exit

        with open(file_name, "r") as file:
            data = json.load(file)
            return data

    def summary_revision_info(self, dump_to_json : bool):
        if not bool(self.last_change_num):
            get_changes_sh = "p4 changes -m1 -s submitted @{} | ".format(self.P4WorkspaceName) + r"awk '{print $2}'"
            self.last_change_num = os.popen(get_changes_sh).read().rstrip() # 本地所处于的change
        if not bool(self.current_change_num):
            self.current_change_num = os.popen("p4 changes -m1 -s submitted | awk '{print $2}'").read().rstrip() # 服务器所处最新change
        get_changes_sh = "p4 changes -tL -s submitted @{},@{}".format(self.last_change_num, self.current_change_num)
        # get_changes_sh = "p4 changes -tL -s submitted @{},@{}".format(26865, 26866)
        self.pack_revision_info = os.popen(get_changes_sh).read()
        if dump_to_json:
            self.dump_to_json()
            # self.load_from_json()
        logger.info(self.doc_info())

    def record_revison_info(self, mongo : MongoCtl, use_file : bool):
        if use_file:
            succ = mongo.set.insert_one(self.load_from_json())
        else:
            succ = mongo.set.insert_one(self.doc_info())
        if not succ:
            logger.error("{} -- record revison info failed\n".format(self.doc_info_head))
        else:
            logger.info("{} -- record revison info succ\n".format(self.doc_info_head()))


if __name__ == "__main__":

    if len(sys.argv) < 6:
        logger.error("usage : package_material_changes.py <P4WorkspaceName> <package_version> <last_change_num> <current_change_num> <start_build_time>")
        exit()
    else:
        logger.info("P4WorkspaceName:{} package_version:{} current_change_num:{} start_build_time:{}".format(
            sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
        p4_workspace_name = sys.argv[1]

    os.environ["P4CLIENT"] = p4_workspace_name

    mongoctl = MongoCtl()
    doc = PackDocument()
    doc.P4WorkspaceName = p4_workspace_name
    doc.package_version = sys.argv[2]
    doc.last_change_num = sys.argv[3]
    doc.current_change_num = sys.argv[4]
    doc.start_build_time = sys.argv[5]

    print(mongoctl.get_last_change_num())
    doc.last_change_num = mongoctl.get_last_change_num()
    print("user is ", getpass.getuser())
    doc.summary_revision_info(True)
    doc.record_revison_info(mongoctl, True)

    logger.info(doc.doc_info_head())





