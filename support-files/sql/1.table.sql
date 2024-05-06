-- 更新权限枚举
ALTER TYPE app_permission ADD VALUE 'ops-pilot.admin';

-- 意图表
create table if not exists ops_pilot_intent (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    create_time timestamp default current_timestamp
);

-- 意图语料表
create table if not exists ops_pilot_intent_corpus (
    id BIGSERIAL primary key,
    intent_id BIGINT references ops_pilot_intent on delete cascade not null,
    corpus text not null,
    create_time timestamp default current_timestamp
);

-- 动作表
create table if not exists ops_pilot_actions (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    create_time timestamp default current_timestamp
);

-- 实体表
create table if not exists ops_pilot_entity (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    create_time timestamp default current_timestamp
);

-- 槽位表
create table if not exists ops_pilot_slot (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    slot_config text,
    create_time timestamp default current_timestamp
);

-- 表单表
create table if not exists ops_pilot_form (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    form_config text,
    description text,
    create_time timestamp default current_timestamp
);

-- 回复表
create table if not exists ops_pilot_response (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    create_time timestamp default current_timestamp
);

-- 回复语料表
create table if not exists ops_pilot_response_corpus (
    id BIGSERIAL primary key,
    response_id BIGINT references ops_pilot_response on delete cascade not null,
    corpus text not null,
    create_time timestamp default current_timestamp
);

-- 对话规则表
create table if not exists ops_pilot_rule (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    steps text,
    create_time timestamp default current_timestamp
);

-- 对话故事表
create table if not exists ops_pilot_story (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    description text,
    steps text,
    create_time timestamp default current_timestamp
);

-- 机器人表
create table if not exists ops_pilot_bot (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    credentials_config text,
    endpoints_config text,
    bot_config text,
    train_config text,
    description text,
    create_time timestamp default current_timestamp
);

-- Rasa模型表
create table if not exists ops_pilot_models (
    id BIGSERIAL primary key,
    name varchar(255) not null,
    model_path text not null,
    bot_id BIGINT references ops_pilot_bot on delete cascade not null,
    create_time timestamp default current_timestamp
);

-- 机器人-规则关联表
create table if not exists ops_pilot_bot_rule (
    id BIGSERIAL primary key,
    bot_id BIGINT references ops_pilot_bot on delete cascade not null,
    rule_id BIGINT references ops_pilot_rule on delete cascade not null,
    create_time timestamp default current_timestamp
);

-- 机器人-故事关联表
create table if not exists ops_pilot_bot_story (
    id BIGSERIAL primary key,
    bot_id BIGINT references ops_pilot_bot on delete cascade not null,
    story_id BIGINT references ops_pilot_story on delete cascade not null,
    create_time timestamp default current_timestamp
);