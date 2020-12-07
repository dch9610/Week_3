from service import create_app

app=create_app()

# 서버 가동
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    debug = True

    app.run(host = host,
            port = port,
            debug = debug)