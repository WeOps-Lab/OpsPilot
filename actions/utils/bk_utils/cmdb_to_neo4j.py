import datetime
import math

from py2neo import Graph
from py2neo.bulk import merge_nodes, merge_relationships
from actions.utils.bk_utils.component.shortcuts import get_client_by_user
from actions.constant.server_settings import server_settings


class ImportInst(object):
    def __init__(self):
        self.client = get_client_by_user("admin")

    def get_db_cur(self):
        """连接数据库，获取操作游标"""
        cur = Graph(server_settings.neo4j_url, auth=(server_settings.neo4j_username, server_settings.neo4j_password))
        return cur

    def get_all_objs(self):
        """获取模型列表，隐藏模型除外"""
        resp = self.client.cc.search_objects(dict(bk_ishidden=False))
        if not resp["result"]:
            raise Exception("查询模型列表失败，详情：{}".format(resp.get('message')))
        return resp["data"]

    def _get_inst(self, kwargs):
        """查模型实例"""
        resp = self.client.cc.search_inst(kwargs)
        if not resp["result"]:
            raise Exception("查询模型{}实例列表失败，详情：{}".format(kwargs['bk_obj_id'], resp.get('message')))
        return resp["data"]["count"], resp["data"]["info"]

    def get_insts(self, obj):
        """全量查询模型实例，解决分页限制问题"""
        max_len = 200
        query_dict = dict(bk_obj_id=obj, page=dict(start=0, limit=max_len))
        count, insts = self._get_inst(query_dict)
        request_num = math.ceil(count / max_len)
        if request_num > 1:
            for request in range(request_num - 1):
                query_dict["page"]["start"] += max_len
                _, now_inst = self._get_inst(query_dict)
                insts.extend(now_inst)
        return insts

    def get_relaions(self, obj):
        """查询模型的关联关系"""
        query_dict = dict(bk_obj_id=obj, condition=dict(bk_obj_id=obj))
        resp = self.client.cc.find_instance_association(query_dict)
        if not resp["result"]:
            raise Exception("查询模型{}的关联失败，详情：{}".format(obj, resp.get('message')))
        return resp["data"]

    def get_all_obj_inst_map(self, objs):
        """获取所有模型的模型实例，并进行数据格式化"""
        all_obj_inst_map = {}
        for obj in objs:
            obj_insts = self.get_insts(obj["bk_obj_id"])
            if not obj_insts:
                continue
            if obj["bk_obj_id"] not in all_obj_inst_map:
                all_obj_inst_map[obj["bk_obj_id"]] = {}

            if obj["bk_obj_id"] == "bk_biz_set_obj":  # 业务集模型实例ID、NAME转换
                for inst in obj_insts:
                    del inst["bk_scope"]
                    all_obj_inst_map[obj["bk_obj_id"]][inst["bk_biz_set_id"]] = dict(
                        bk_inst_id=inst["bk_biz_set_id"],
                        bk_inst_name=inst["bk_biz_set_name"],
                        **inst
                    )
            elif obj["bk_obj_id"] == "host":  # 主机模型实例ID、NAME转换
                for inst in obj_insts:
                    all_obj_inst_map[obj["bk_obj_id"]][inst["bk_host_id"]] = dict(
                        bk_inst_id=inst["bk_host_id"],
                        bk_inst_name=inst["bk_host_innerip"],
                        **inst
                    )
            elif obj["bk_obj_id"] in {"biz", "set", "module"}:  # 其他内置模型实例ID、NAME转换
                bk_inst_id_key = "bk_{}_id".format(obj['bk_obj_id'])
                bk_inst_name_key = "bk_{}_name".format(obj['bk_obj_id'])
                for inst in obj_insts:
                    all_obj_inst_map[obj["bk_obj_id"]][inst[bk_inst_id_key]] = dict(
                        bk_inst_id=inst[bk_inst_id_key],
                        bk_inst_name=inst[bk_inst_name_key],
                        **inst
                    )
            else:
                for inst in obj_insts:
                    all_obj_inst_map[obj["bk_obj_id"]][inst["bk_inst_id"]] = inst

        return all_obj_inst_map

    def get_mainline_obj_relation(self):
        """主线模型，host-module、module-set、set-biz"""
        mainline_obj_relation_map = {}
        # set-biz
        set_insts = self.get_insts("set")
        if set_insts:
            obj_asst_tuple = ("set", "bk_mainline", "biz")
            mainline_obj_relation_map[obj_asst_tuple] = [
                {
                    "bk_obj_id": "set",
                    "bk_inst_id": i["bk_set_id"],
                    "bk_asst_obj_id": "biz",
                    "bk_asst_inst_id": i["bk_biz_id"],
                }
                for i in set_insts
            ]
        # module-set
        module_insts = self.get_insts("module")
        if module_insts:
            obj_asst_tuple = ("module", "bk_mainline", "set")
            mainline_obj_relation_map[obj_asst_tuple] = [
                {
                    "bk_obj_id": "module",
                    "bk_inst_id": i["bk_module_id"],
                    "bk_asst_obj_id": "set",
                    "bk_asst_inst_id": i["bk_set_id"],
                }
                for i in module_insts
            ]
        # host-module
        host_ids = [i["bk_host_id"] for i in self.get_insts("host")]
        max_len, host_insts = 500, []
        request_list = [host_ids[i:i + max_len] for i in range(0, len(host_ids), max_len)]
        for host_ids in request_list:
            resp = self.client.cc.find_host_biz_relations(dict(bk_host_id=host_ids))
            if not resp["result"]:
                raise Exception("find_host_biz_relations 失败，详情：{}".format(resp.get('message')))
            host_insts.extend(resp["data"])
        if host_insts:
            obj_asst_tuple = ("host", "bk_mainline", "module")
            mainline_obj_relation_map[obj_asst_tuple] = [
                {
                    "bk_obj_id": "host",
                    "bk_inst_id": i["bk_host_id"],
                    "bk_asst_obj_id": "module",
                    "bk_asst_inst_id": i["bk_module_id"],
                }
                for i in host_insts
            ]
        return mainline_obj_relation_map

    def get_all_obj_relation_map(self, objs):
        """查询所有模型，模式实例的关联关系"""
        all_obj_relation_map = {}
        for obj in objs:
            relaions = self.get_relaions(obj["bk_obj_id"])
            if not relaions:
                continue
            for relaion in relaions:
                obj_asst_tuple = (relaion["bk_obj_id"], relaion["bk_asst_id"], relaion["bk_asst_obj_id"])
                if obj_asst_tuple not in all_obj_relation_map:
                    all_obj_relation_map[obj_asst_tuple] = []
                all_obj_relation_map[obj_asst_tuple].append(relaion)

        # search主线模型关联(host-module-set-biz)
        mainline_obj_relation_map = self.get_mainline_obj_relation()
        for obj_asst_tuple, relaions in mainline_obj_relation_map.items():
            if obj_asst_tuple in all_obj_relation_map:
                all_obj_relation_map[obj_asst_tuple].extend(relaions)
            else:
                all_obj_relation_map[obj_asst_tuple] = relaions

        return all_obj_relation_map

    def structure_obj_node_map(self, all_obj_inst_map):
        """构造节点对象map"""
        obj_node_map = {}
        for bk_obj_id, obj_inst_map in all_obj_inst_map.items():
            obj_node_map[bk_obj_id] = list(obj_inst_map.values())
        return obj_node_map

    def structure_node_relation_map(self, all_obj_inst_map, all_obj_relation_map):
        """构造关联对象列表"""
        detail = {"since": str(datetime.datetime.now())}
        node_relation_map = {}
        for bk_obj_asst_id, relations in all_obj_relation_map.items():
            node_relation_map[bk_obj_asst_id] = []
            for relation in relations:
                src_inst = all_obj_inst_map[relation['bk_obj_id']][relation['bk_inst_id']]
                dst_inst = all_obj_inst_map[relation['bk_asst_obj_id']][relation['bk_asst_inst_id']]
                node_relation_map[bk_obj_asst_id].append(((src_inst["bk_inst_id"]), detail, (dst_inst["bk_inst_id"])))
        return node_relation_map

    def save_data_by_transaction(self, obj_node_map, node_relation_map):
        """数据入库，merge模式(bk_obj_id、bk_inst_id)"""

        cur = self.get_db_cur()

        # 删除全量数据
        cur.delete_all()

        # 安照模型分组创建节点
        for bk_obj_id, data in obj_node_map.items():
            merge_nodes(cur.auto(), data, (bk_obj_id, "bk_inst_id"))

        # 安照源模型、关联、目标模型创建关联
        for obj_asst_tuple, data in node_relation_map.items():
            merge_relationships(cur.auto(), data, obj_asst_tuple[1], start_node_key=(obj_asst_tuple[0], "bk_inst_id"), end_node_key=(obj_asst_tuple[2], "bk_inst_id"))

    def collector(self):
        # 获取模型列表
        objs = self.get_all_objs()

        # 根据模型列表查询所有模型对应的实例与关联关系
        all_obj_inst_map = self.get_all_obj_inst_map(objs)
        all_obj_relation_map = self.get_all_obj_relation_map(objs)

        # 构造Node对象与Relationship对象
        obj_node_map = self.structure_obj_node_map(all_obj_inst_map)
        node_relation_map = self.structure_node_relation_map(all_obj_inst_map, all_obj_relation_map)

        # 存库
        self.save_data_by_transaction(obj_node_map, node_relation_map)
