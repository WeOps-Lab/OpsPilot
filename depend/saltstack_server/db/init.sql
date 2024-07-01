CREATE TABLE roster (
    id SERIAL PRIMARY KEY,  -- 主键
    salt_id VARCHAR(255) NOT NULL,  -- Salt标识
    host VARCHAR(255) NOT NULL,  -- 主机
    username VARCHAR(255) NOT NULL,  -- 用户
    passwd VARCHAR(255) NOT NULL,  -- 密码
    port INT,  -- ssh端口号
    sudo BOOLEAN,  -- sudo选项
    sudo_user VARCHAR(255),  -- sudo用户
    tty BOOLEAN,  -- tty选项
    priv VARCHAR(255),  -- 私钥文件路径
    priv_passwd VARCHAR(255),  -- 私钥密码
    timeout INT,  -- 连接超时时间
    minion_opts TEXT,  -- minion选项
    thin_dir VARCHAR(255),  -- Salt组件存储目录
    cmd_umask VARCHAR(255),  -- Salt-call命令UMASK
    ssh_pre_flight VARCHAR(255),  -- 预处理脚本路径
    ssh_pre_flight_args VARCHAR(255),  -- 预处理脚本参数
    set_path VARCHAR(255),  -- 环境变量设置
    ssh_options TEXT  -- SSH选项
);

CREATE INDEX idx_salt_id ON roster(salt_id);  -- 创建Salt标识索引
CREATE INDEX idx_host ON roster(host);  -- 创建主机索引
--
-- Table structure for table 'jids'
--

DROP TABLE IF EXISTS jids;
CREATE TABLE jids (
  jid   varchar(20) PRIMARY KEY,
  started TIMESTAMP WITH TIME ZONE DEFAULT now(),
  tgt_type text NOT NULL,
  cmd text NOT NULL,
  tgt text NOT NULL,
  kwargs text NOT NULL,
  ret text NOT NULL,
  username text NOT NULL,
  arg text NOT NULL,
  fun text NOT NULL
);

--
-- Table structure for table 'salt_returns'
--
-- note that 'success' must not have NOT NULL constraint, since
-- some functions don't provide it.

DROP TABLE IF EXISTS salt_returns;
CREATE TABLE salt_returns (
  added     TIMESTAMP WITH TIME ZONE DEFAULT now(),
  fun       text NOT NULL,
  jid       varchar(20) NOT NULL,
  return    text NOT NULL,
  id        text NOT NULL,
  success   boolean
);
CREATE INDEX ON salt_returns (added);
CREATE INDEX ON salt_returns (id);
CREATE INDEX ON salt_returns (jid);
CREATE INDEX ON salt_returns (fun);

DROP TABLE IF EXISTS salt_events;
CREATE TABLE salt_events (
  id SERIAL,
  tag text NOT NULL,
  data text NOT NULL,
  alter_time TIMESTAMP WITH TIME ZONE DEFAULT now(),
  master_id text NOT NULL
);
CREATE INDEX ON salt_events (tag);
CREATE INDEX ON salt_events (data);
CREATE INDEX ON salt_events (id);
CREATE INDEX ON salt_events (master_id);