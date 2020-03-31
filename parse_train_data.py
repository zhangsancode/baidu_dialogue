#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re


class ParseTrainData(object):
    def __init__(self):
        self.user_profile = {}
        self.kg = {}
        self.conversation_session = []

    def parse_sitution(self, input_text):
        ret = {}
        input_text = input_text.split(",")
        input_list = []
        for text in input_text:
            input_list.extend(text.split(" "))

        for word_tuple in input_list:
            if ":" in word_tuple:
                tmp = word_tuple.split(":")
                ret[tmp[0]] = ret[tmp[1]]
            elif "在" in word_tuple:
                ret['user_location'] = word_tuple.replace('在', '')
            else:
                ret['unknow'] = word_tuple
        return ret

    def parse_kg(self, input_list):
        for item in input_list:
            key = item[0]
            if self.kg.get(key) is None:
                self.kg[key] = [(item[1], (item[2]))]
            else:
                self.kg[key].append((item[1], item[2]))

    def parse_user_profile(self, input_dict):
        pass


    """
    [1]问答(User主动问电影 『阿飞正传』 主演是谁? Bot回答『张国荣』，User满足并好评)-->
    [2]关于明星的聊天(Bot主动，根据给定的明星信息聊 『张国荣』 相关内容，至少要聊2轮，避免话题切换太僵硬，不够自然)-->
    [3]电影推荐(Bot主动，Bot使用 『星月童话』 的某个评论当做推荐理由来推荐 『星月童话』，User先问电影『国家地区、导演、类型、主演、口碑、评分』中的一个或多个，Bot回答，最终User接受)-->
    [4]再见

        "[1]能告诉我电影 『阿飞正传』 主演是谁吗？",
        "是张国荣哦。",
        "谢谢你告诉我哦，你真聪明",
        "[2]你喜欢张国荣吗？他可是香港著名影星。",
        "喜欢呢，他还是美国CNN全球五大指标音乐人呢",
        "真是一个了不起的人，还是一个天生的艺人。",
        "是啊，非常的优秀",
        "[3]这样的话我为你推荐一部他主演的电影吧，『星月童话』，哥哥留下的一段美丽童话，哥哥依然是那么的迷人！",
        "口碑怎么样",
        "口碑还好，挺不错的，你可以去看看。",
        "不错，我空闲时间看看",
        "希望你会喜欢。",
        "[4]好的，到公司了，不聊了",
        "再见！"
    """
    def parse_goals(self, goals, conversation_list):
        cur_goals = ""
        ret_list = []
        goal_list = []
        conver_list = []
        one_goal_list = []

        for goal in goals.split("-->"):
            goal = goal.strip()
            goal_detail = re.findall(r"\((.+?)\)", goal)
            if len(goal_detail) == 0:
                goal_name = re.findall(r"\](.+)", goal)
                goal_name = goal_name[0] if len(goal_name) > 0 else ''
                goal_detail = []
            else:
                goal_name = re.findall(r"\](.+?)[\(|Z]", goal)[0]
                # 解析对话说明 detail
                #user_flag = True
                #tmp_list = goal_detail[0].split(",")
                """
                goal_detail = []
                for item in tmp_list:
                    if "User" in item:
                        item.replace("User", '')
                        goal_detail.append(('user', ))
                """
            goal_name = goal_name.strip().replace(" ", '')
            # goal_index = re.findall(r"\[(.+?)\]", goal)[0]
            goal_list.append((goal_name, goal_detail))

        for index, conversation in enumerate(conversation_list):
            if conversation[0] == '[' and conversation[2] == ']':
                if index != 0:
                    conver_list.append(one_goal_list)
                    one_goal_list = []
                else:
                    one_goal_list = []

            one_goal_list.append(conversation)

        for goal, conver in zip(goal_list, conver_list):
            ret_list.append((goal[0], goal[1], conver))
        return ret_list

    def parse(self, json_input):
        json_input = json_input.replace("\n",'')
        json_dict = json.loads(json_input)

        goals = self.parse_goals(json_dict['goal'], json_dict['conversation'])
        return goals
        """
        user_profile = self.parse_user_profile(json_dict['user_profile'])
        kg = self.parse_kg(json_dict['kg'])
        situation = self.parse_sitution(json_dict['situation'])
        details = self.parse_detail(json_dict['conversation'])
        """


def debug_print_goals(filter_name):
    parse_model = ParseTrainData()
    # with open("data/sample_data.json", 'r') as fp:
    goals_set = {}
    file_list = ['data/train.txt', 'data/dev.txt']
    for file_path in file_list:
        with open(file_path, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                ret = parse_model.parse(line)
                for name, detail, conver in ret:
                    if name in filter_name:
                        print(name, conver)
                    goals_set[name] = 1 if goals_set.get(name) is None else goals_set[name] + 1


if __name__ == '__main__':
    filter_name = ['天气信息推送']
    debug_print_goals(filter_name)

