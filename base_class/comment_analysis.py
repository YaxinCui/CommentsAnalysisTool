from abc import ABCMeta, abstractmethod
import pandas as pd


class CommentAnalyse(metaclass=ABCMeta):

    """
    评论分析基本流程
    1. 获取评论，并将其存入csv
    2. 对评论进行分析，目前包括是否为建议，是消极还是积极，提取关键词信息
    3. 可视化展示，存入文件
    """
    def __init__(self, columns=['comments',  'is_suggestion', 'sentiment']):
        """
        :param length: comments表格长度
        :param columns: comments类型为文本，表示评论文本，is_suggestion为是否为评论，类型为数字0.0-1.0，sentiment为是积极还是消极，类型为数字0.0-1.0
        """
        self.columns = columns
        self.comments = pd.DataFrame(columns=columns)
        self.comments['comments'] = self.comments['comments'].astype(str)

    @abstractmethod
    def get_comments(self):
        """为comments表添加评论，其中列名为comments
        :return:
        """
        pass

    @abstractmethod
    def analyse_comments(self):
        """分析每条评论，并将其结果写入comments表格"""
        pass

    def save_file(self, path='comments.csv'):
        self.comments.to_csv(path)

    def get_table(self):
        return self.comments

