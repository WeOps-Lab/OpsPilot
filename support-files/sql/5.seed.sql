-- 初始化意图数据
INSERT INTO ops_pilot_intent(id, name, description)
VALUES (1, 'yes', ''),
       (2, 'no', ''),
       (3, 'summary_content', ''),
       (4, 'out_of_scope', ''),
       (5, 'scan', ''),
       (6, 'EXTERNAL_UTTER', '');

-- 初始化意图语料
insert into ops_pilot_intent_corpus(intent_id, corpus)
values (1, '是'),
       (1, '确认'),
       (1, 'yes'),
       (1, '是的'),
       (1, '对'),
       (1, '对的');

insert into ops_pilot_intent_corpus(intent_id, corpus)
values (2, '不是'),
       (2, '不对'),
       (2, '不'),
       (2, 'no'),
       (2, '不是的');

insert into ops_pilot_intent_corpus(intent_id, corpus)
values (3, '总结我们的聊天记录'),
       (3, '我们的对话总结'),
       (3, '总结一下我们的对话'),
       (3, '我们的对话总结一下'),
       (3, '总结一下我们的聊天记录'),
       (3, '我们的聊天记录总结一下'),
       (3, '总结一下我们的聊天'),
       (3, '我们的聊天总结一下'),
       (3, '总结一下我们的对话记录'),
       (3, '我们的对话记录总结一下'),
       (3, '对话记录总结'),
       (3, '总结对话记录'),
       (3, '总结聊天记录'),
       (3, '聊天记录总结'),
       (3, '总结聊天'),
       (3, '聊天总结');

insert into ops_pilot_intent_corpus(intent_id, corpus)
values (4, '今天天气怎么样'),
       (4, '总结'),
       (4, '总结上述内容'),
       (4, '总结一下'),
       (4, '总结一下上述内容'),
       (4, '总结一下上述对话'),
       (4, '这个功能怎么用'),
       (4, 'WeOps支持哪些功能'),
       (4, '马斯克有没去参加笼中决斗'),
       (4, '产品对比'),
       (4, '你真好'),
       (4, '再说吧'),
       (4, 'jenkins是什么'),
       (4, '那你从那里获取到jenkins的相关信息的'),
       (4, '使用Java编写一个爬虫示例程序'),
       (4, '修复一个bug'),
       (4, '我要申请笔记本'),
       (4, '帮我查一下这个服务器的信息'),
       (4, '申请一下仓库权限');

insert into ops_pilot_intent_corpus(intent_id, corpus)
values (5, '扫描服务器'),
       (5, '资产测绘'),
       (5, '扫描资产'),
       (5, '扫描资产信息'),
       (5, '测绘资产信息');

-- 初始化动作表数据
INSERT INTO ops_pilot_actions(name, description)
VALUES ('action_llm_fallback', ''),
       ('action_llm_summary', ''),
       ('action_scan', ''),
       ('action_external_utter', '');

-- 初始化实体表数据
INSERT INTO ops_pilot_entity(name, description)
values ('content', '');

-- 初始化槽位表数据
INSERT INTO ops_pilot_slot(name, description,  slot_config)
values ('scan_targets', false,'
scan_targets:
  type: text
  influence_conversation: false
  mappings:
    - type: from_text
      conditions:
        - active_loop: scan_targets_form
          requested_slot: scan_targets
');

-- 初始化表单数据
INSERT INTO ops_pilot_form(name, description, form_config)
values ('scan_targets_form','','
scan_targets_form:
  required_slots:
    - scan_targets
');

-- 初始化回复数据
INSERT INTO ops_pilot_response(id,name, description)
values (1,'utter_ask_scan_targets',''),
       (2,'utter_ticket_canceled',''),
       (3,'utter_ticket_submitted','');

-- 初始化回复语料
insert into ops_pilot_response_corpus(response_id, corpus)
values (1,'你想测绘哪些对象呢？eg: 127.0.0.1,https://baidu.com'),
(2,'OpsPilot已经取消了本次的提单申请，期待下次为您服务！'),
(3,'OpsPilot已经成功为您提交了提单，我们会尽快处理您的请求！');

-- 初始化对话规则表
INSERT INTO ops_pilot_rule(id,name, description, steps)
values 
    (1,'主动回复','','
rule: 主动回复
steps:
    - intent: EXTERNAL_UTTER
    - action: action_external_utter'),
    
    (2,'Fallback','','
rule: Fallback
steps:
    - intent: nlu_fallback
    - action: action_llm_fallback'),

    (3,'summary_content','','
rule: summary_content    
steps:
    - intent: summary_content
    - action: action_llm_summary'),

    (4,'out_of_scope','','
rule: out_of_scope    
steps:
    - intent: out_of_scope
    - action: action_llm_fallback'),

    (5,'激活资产测绘表单','','
rule: 激活资产测绘表单    
steps:
    - intent: scan
    - action: scan_targets_form
    - active_loop: scan_targets_form'),

    (6,'提交资产测绘表单','
rule: 提交资产测绘表单    
condition:
    - active_loop: scan_targets_form','
steps:
    - action: scan_targets_form
    - active_loop: null
    - slot_was_set:
        - requested_slot: null
    - action: action_scan    
');

-- 初始化机器人数据
INSERT INTO ops_pilot_bot(id, name, credentials_config, endpoints_config, bot_config, train_config, description)
values (1,'OpsPilot','
socketio:
  user_message_evt: user_uttered
  bot_message_evt: bot_uttered
  session_persistence: false
rest:','
tracker_store:
  type: SQL
  dialect: "sqlite"
  url: ""
  db: "tracker.db"
  username:
  password:
','
session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
','
recipe: default.v1
assistant_id: ops-pilot
language: zh

pipeline:
  - name: "compoments.tokenizer.jieba_tokenizer.JiebaTokenizer"

  - name: RegexFeaturizer
    use_word_boundaries: false
    case_sensitive: True
    number_additional_patterns: 10

  - name: LanguageModelFeaturizer
    model_name: "bert"
    model_weights: "bert-base-chinese"
    cache_dir: cache/models

  - name: LexicalSyntacticFeaturizer

  - name: CountVectorsFeaturizer

  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4

  - name: DIETClassifier
    epochs: 500
    constrain_similarities: true
    evaluate_on_number_of_examples: 0
    evaluate_every_number_of_epochs: 100
    number_of_transformer_layers: 4
    transformer_size: 256
    number_of_attention_heads: 4
    learning_rate: 0.0001
    drop_rate: 0.3
    tensorboard_log_directory: "./tensorboard"
    tensorboard_log_level: "epoch"

  - name: ResponseSelector
    retrieval_intent: chitchat
    epochs: 300
    learning_rate: 0.001
    constrain_similarities: True
    scale_loss: false

  - name: RegexEntityExtractor
    case_sensitive: True
    use_lookup_tables: True
    use_regexes: True
    use_word_boundaries: True

  - name: FallbackClassifier
    threshold: 0.7
    ambiguity_threshold: 0.1



policies:
  - name: MemoizationPolicy

  - name: TEDPolicy
    max_history: 10
    epochs: 1000
    model_confidence: softmax
    constrain_similarities: true
    evaluate_on_number_of_examples: 0
    evaluate_every_number_of_epochs: 100
    tensorboard_log_directory: "./tensorboard"
    tensorboard_log_level: "epoch"

  - name: RulePolicy
    core_fallback_threshold: 0.4
    core_fallback_action_name: "action_llm_fallback"
','');

-- 初始化机器人与对话规则关联数据
INSERT INTO ops_pilot_bot_rule(bot_id, rule_id)
values (1,1),
       (1,2),
       (1,3),
       (1,4),
       (1,5),
       (1,6);