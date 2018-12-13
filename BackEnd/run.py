from app import app
from app.service import setting

if __name__ == '__main__':
    if setting.PRODUCTION:
        host = setting.HOST_PRODUCTION
    else:
        host = setting.HOST_LOCAL
    PORT = setting.PORT
    app.run(host=host, port=PORT, debug=True)  # upload 修改