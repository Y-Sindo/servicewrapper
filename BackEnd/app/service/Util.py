import os
def shutdown_crawl(crawl):
    try:
        if crawl:
            crawl._end()  # 关闭chromedriver
            del crawl
    except:
        pass


def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        return "404"
    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

