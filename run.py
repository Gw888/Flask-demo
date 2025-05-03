from app import create_app

app = create_app()

if __name__ == '__main__':  # 如果当前文件是作为主程序运行 
    app.run(debug=True) 