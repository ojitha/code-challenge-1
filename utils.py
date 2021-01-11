import re

#cleansing the pre and post \' characters
def removeStartEndChars(str):
    pre = re.sub("^\'","",str)
    post = pre[:-1]
    return post
