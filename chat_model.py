#!/usr/bin/python
# -*- coding: utf-8 -*-


class ChatBot(object):
    def __init__(self):
        self.slot_list = []
        self.user_session_state = []
        self.user_profile = []

    def domain_classify(self, user_input):
        pass

    def update_session_state(self):
        pass

    def handle_domain(self, domain, user_input):
        pass

    def parse_comment(self, user_input):
        # ent = self.parse_slot(user_input)
        # 实体识别，语义消歧
        user_input = user_input

        domain = self.domain_classify(user_input)
        # 依赖历史信息
        action = self.handle_domain(domain, user_input, self.user_session_state)
        ret_message = action(self.user_profile)

