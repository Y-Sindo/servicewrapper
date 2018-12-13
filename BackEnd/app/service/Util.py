def shutdown_crawl(crawl):
    try:
        if crawl:
            crawl._end()  # 关闭chromedriver
            del crawl
    except:
        pass

