from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "Munchkin",
    "TABS": [
        {
            "models": [
                "contentpack_mgmt.contentpack",
                "contentpack_mgmt.rasastories",
                "contentpack_mgmt.rasarules",
                "contentpack_mgmt.intent",
                "contentpack_mgmt.rasaforms",
                "contentpack_mgmt.rasaslots",
                "contentpack_mgmt.intentcorpus",
                "contentpack_mgmt.rasaresponse",
                "contentpack_mgmt.rasaresponsecorpus",
                "contentpack_mgmt.rasaentity",
                "contentpack_mgmt.botactions",
            ],
            "items": [
                {
                    "title": "扩展包",
                    "link": reverse_lazy("admin:contentpack_mgmt_contentpack_changelist"),
                },
                {
                    "title": "对话故事",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasastories_changelist"),
                },
                {
                    "title": "动作",
                    "link": reverse_lazy("admin:contentpack_mgmt_botactions_changelist"),
                },
                {
                    "title": "对话规则",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasarules_changelist"),
                },
                {
                    "title": "意图",
                    "link": reverse_lazy("admin:contentpack_mgmt_intent_changelist"),
                },
                {
                    "title": "表单",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasaforms_changelist"),
                },
                {
                    "title": "槽位",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasaslots_changelist"),
                },
                {
                    "title": "实体",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasaentity_changelist"),
                },
                {
                    "title": "回复",
                    "link": reverse_lazy("admin:contentpack_mgmt_rasaresponse_changelist"),
                },
            ]

        },
        {
            "models": [
                "model_provider_mgmt.llmmodel",
                "model_provider_mgmt.llmskill",
            ],
            "items": [
                {
                    "title": "LLM模型",
                    "link": reverse_lazy("admin:model_provider_mgmt_llmmodel_changelist"),
                },
                {
                    "title": "LLM技能",
                    "link": reverse_lazy("admin:model_provider_mgmt_llmskill_changelist"),
                }
            ]
        },
        {
            "models": [
                "authtoken.tokenproxy",
                "token_blacklist.blacklistedtoken",
                "token_blacklist.outstandingtoken",
            ],
            "items": [
                {
                    "title": "Token认证令牌",
                    "link": reverse_lazy("admin:authtoken_tokenproxy_changelist"),
                },
                {
                    "title": "令牌黑名单(JWT)",
                    "link": reverse_lazy("admin:token_blacklist_blacklistedtoken_changelist"),
                },
                {
                    "title": "未处理令牌(JWT)",
                    "link": reverse_lazy("admin:token_blacklist_outstandingtoken_changelist"),
                }
            ]
        },
        {
            "models": [
                "auth.group",
                "auth.user"
            ],
            "items": [
                {
                    "title": "用户组",
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
                {
                    "title": "用户",
                    "link": reverse_lazy("admin:auth_user_changelist"),
                }
            ]
        },
        {
            "models": [
                "knowledge_mgmt.fileknowledge",
                "knowledge_mgmt.manualknowledge",
                "knowledge_mgmt.webpageknowledge",
            ],
            "items": [
                {
                    "title": "文件知识",
                    "link": reverse_lazy("admin:knowledge_mgmt_fileknowledge_changelist"),
                },
                {
                    "title": "手工录入",
                    "link": reverse_lazy("admin:knowledge_mgmt_manualknowledge_changelist"),
                },
                {
                    "title": "网页知识",
                    "link": reverse_lazy("admin:knowledge_mgmt_webpageknowledge_changelist"),
                }
            ]
        },
        {
            "models": [
                "django_celery_beat.clockedschedule",
                "django_celery_beat.crontabschedule",
                "django_celery_beat.intervalschedule",
                "django_celery_beat.periodictask",
                "django_celery_beat.solarschedule",
                "django_celery_results.groupresult",
                "django_celery_results.taskresult"
            ],
            "items": [
                {
                    "title": "定时",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_clockedschedule_changelist"
                    ),
                },
                {
                    "title": "定时任务",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_crontabschedule_changelist"
                    ),
                },
                {
                    "title": "间隔",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_intervalschedule_changelist"
                    ),
                },
                {
                    "title": "周期性任务",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_periodictask_changelist"
                    ),
                },
                {
                    "title": "日程事件",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_solarschedule_changelist"
                    ),
                },
                {
                    "title": "任务组执行记录",
                    "link": reverse_lazy(
                        "admin:django_celery_results_groupresult_changelist"
                    ),
                },
                {
                    "title": "任务执行记录",
                    "link": reverse_lazy(
                        "admin:django_celery_results_taskresult_changelist"
                    ),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "navigation": [
            {
                "title": "机器人管理",
                "items": [
                    {
                        "title": "机器人",
                        "link": reverse_lazy("admin:bot_mgmt_bot_changelist"),
                    },
                    {
                        "title": "动作规则",
                        "link": reverse_lazy("admin:bot_mgmt_botskillrule_changelist"),
                    },
                    {
                        "title": "对话记录",
                        "link": reverse_lazy("admin:bot_mgmt_botconversationhistory_changelist"),
                    }
                ]
            },
            {
                "title": "AI模型",
                "items": [
                    {
                        "title": "Embed模型",
                        "link": reverse_lazy("admin:model_provider_mgmt_embedprovider_changelist"),
                    },
                    {
                        "title": "Rerank模型",
                        "link": reverse_lazy("admin:model_provider_mgmt_rerankprovider_changelist"),
                    },
                    {
                        "title": "LLM模型",
                        "link": reverse_lazy("admin:model_provider_mgmt_llmmodel_changelist"),
                    }
                ]
            },
            {
                "title": "通道管理",
                "items": [
                    {
                        "title": "消息通道",
                        "link": reverse_lazy("admin:channel_mgmt_channel_changelist"),
                    },
                    {
                        "title": "用户组",
                        "link": reverse_lazy("admin:channel_mgmt_channelusergroup_changelist"),
                    },
                    {
                        "title": "用户",
                        "link": reverse_lazy("admin:channel_mgmt_channeluser_changelist"),
                    }
                ]
            },

            {
                "separator": True,
                "title": "知识管理",
                "items": [
                    {
                        "title": "知识库",
                        "link": reverse_lazy("admin:knowledge_mgmt_knowledgebasefolder_changelist"),
                    },
                    {
                        "title": "知识",
                        "link": reverse_lazy("admin:knowledge_mgmt_fileknowledge_changelist"),
                    },
                ]
            },
            {
                "separator": True,
                "title": "扩展包",
                "items": [
                    {
                        "title": "模型",
                        "link": reverse_lazy("admin:contentpack_mgmt_rasamodel_changelist"),
                    },
                    {
                        "title": "扩展包",
                        "link": reverse_lazy("admin:contentpack_mgmt_contentpack_changelist"),
                    }
                ]
            },
            {
                "separator": True,
                "title": "系统管理",
                "items": [
                    {
                        "title": "用户管理",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },

                    {
                        "title": "定时任务",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                    {
                        "title": "审计日志",
                        "link": reverse_lazy(
                            "admin:auditlog_logentry_changelist"
                        ),
                    },
                    {
                        "title": "令牌管理",
                        "link": reverse_lazy("admin:authtoken_tokenproxy_changelist")
                    }
                ],
            },
        ]
    }
}
