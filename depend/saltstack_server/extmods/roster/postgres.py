import logging
import salt.config
import records

log = logging.getLogger(__name__)

def targets(tgt, tgt_type="glob", **kwargs):
    # 获取 Salt Master 配置
    __opts__ = salt.config.master_config('/etc/salt/master')

    # 从配置中获取 database_uri
    database_uri = __opts__.get('roster_uri', None)

    if not database_uri:
        log.error("配置中未找到数据库连接串，请在 Salt Master 配置文件中设置 'roster_uri'。")
        return {}

    log.info("Connecting to database at {}".format(database_uri))

    # 创建 records Database
    db = records.Database(database_uri)

    log.info("Executing SQL query")
    # 执行 SQL 查询并获取结果
    rows = db.query("SELECT * FROM roster")

    log.info(f"Query returned {len(rows)} rows")

    host_configs = []
    for row in rows:
        # 获取非空字段的记录数据
        row_dict = row.as_dict()
        host_config = {k: v for k, v in row_dict.items() if v is not None}

        # 如果 'user' 字段是 'username'，则将其重命名为 'user'
        if 'username' in host_config:
            host_config['user'] = host_config.pop('username')

        if host_config:  # 如果 host_config 不为空，则添加到 host_configs 中
            host_configs.append(host_config)

    # 将 'salt_id' 作为键，主机配置字典作为值，生成字典
    conditioned_raw = {hc['salt_id']: hc for hc in host_configs}

    log.info(f"成功处理 {len(conditioned_raw)} 行目标主机数据。")
    return __utils__["roster_matcher.targets"](conditioned_raw, tgt, tgt_type, "ipv4")