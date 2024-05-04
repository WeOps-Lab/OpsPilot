-- 设置RLS策略
ALTER TABLE ops_pilot_intent ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有意图数据"
    ON ops_pilot_intent
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_intent_corpus ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有意图语料数据"
    ON ops_pilot_intent_corpus
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_actions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有动作数据"
    ON ops_pilot_actions
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_entity ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有实体数据"
    ON ops_pilot_entity
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );


ALTER TABLE ops_pilot_slot ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有槽位数据"
    ON ops_pilot_slot
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_form ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有表单数据"
    ON ops_pilot_form
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_response ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有回复数据"
    ON ops_pilot_response
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_response_corpus ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有回复语料数据"
    ON ops_pilot_response_corpus
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_rule ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有规则数据"
    ON ops_pilot_rule
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );


ALTER TABLE ops_pilot_story ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有故事数据"
    ON ops_pilot_story
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );


ALTER TABLE ops_pilot_bot ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有数据"
    ON ops_pilot_bot
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_bot_rule ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有数据"
    ON ops_pilot_bot_rule
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

ALTER TABLE ops_pilot_bot_story ENABLE ROW LEVEL SECURITY;
CREATE POLICY "允许ops-pilot管理员访问所有数据"
    ON ops_pilot_bot_story
    FOR ALL
    USING (
        jwt_has_permission('ops-pilot.admin')
    )
    WITH CHECK (
        jwt_has_permission('ops-pilot.admin')
    );

