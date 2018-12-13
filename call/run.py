from app import app, setting

if __name__ == '__main__':
    if setting.PRODUCTION:
        host = setting.HOST_PRODUCTION
    else:
        host = setting.HOST_LOCAL

    app.run(host=host, port=8000, debug=True)  # upload 修改