
HYPERPARAMETER = ["__max_page"]  # 超参数

# set the snapshop width screen
SCREEN_WIDTH = 1280

# the path of chrome execute
CHROME_BINARY_LOCATION_PRODUCTION = "/usr/bin/google-chrome"
DRIVER_PATH_PRODUCTION = "/usr/bin/chromedriver"   # headless browner driver
HOST_PRODUCTION = "0.0.0.0"
MONGO_HOST_PRODUCTION = "192.168.9.50"

CHROME_BINARY_LOCATION_LOCAL = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HOST_LOCAL = "127.0.0.1"
MONGO_HOST_LOCAL = "127.0.0.1"

MYSQL_PATH = "192.168.9.50"
MYSQL_USER = "root"
MYSQL_PW  = "my-secret-pw"
MYSQL_DB = "service_network_v3"

PRODUCTION = False   ## 当该值为false时，表示本地配置；为true时，表示开发配置
