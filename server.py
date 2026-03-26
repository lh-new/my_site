from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 后面这里会放 API Key，从环境变量读取
# API_KEY = os.environ.get("YOUR_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    """
    接收前端发来的问题，返回回复
    """
    data = request.json
    question = data.get("question", "")

    # 暂时先返回一个测试回复
    reply = "这是测试回复，你问的是：" + question

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # 启动 Flask 服务
    # debug=True 表示开启调试模式，改代码后自动重启
    # port=5000 表示服务运行在 5000 端口
    app.run(debug=True, port=5000)
