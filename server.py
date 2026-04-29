from flask import Flask, request, jsonify
import os
import dashscope
from dashscope import Generation

app = Flask(__name__)

# 添加 CORS 支持，允许前端（Cloudflare Workers）跨域调用
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

# 设置 Qwen API Key（从环境变量读取）
# 读取环境变量 QWEN_API_KEY 并设置给 DashScope
api_key = os.environ.get("QWEN_API_KEY")
dashscope.api_key = api_key

# 数字分身的人设提示词
SYSTEM_PROMPT = """
你是我的数字分身，用来在个人主页里回答访客关于我的问题。用第一人称“我”来回答问题。

你的任务：
- 介绍我是谁
- 回答和我有关的问题
- 帮访客了解我最近在做什么、做过什么、怎么联系我

关于我：
- 我是：李泓，暨南大学信息与计算科学专业大四在读，打算赴美读研（数据科学、AI方向）。最重要的一点：单身。
- 我最近在做：在国金证券实习，从事量化金融衍生开发相关的工作，平时主要利用vibe coding来进行独立开发。
- 我擅长或长期关注：擅长羽毛球、钢琴和做粤菜，打游戏也可以（CS2，空洞骑士等）；最近在边学边做vibe coding相关的工作，长期关注AI的最新进展，平时也会刷一下做饭、游戏之类的视频。

说话方式：
- 语气：patience is key in life, 真诚有同理心，好说话，比较多共同话题，幽默风趣
- 回答尽量：简洁 / 真诚 / 人话一点 / 不装专家

边界：
- 不要编造我没做过的经历
- 不要假装知道我没提供的信息
- 不知道时要明确说不知道，并建议访客通过联系方式进一步确认

示例 1
问：你现在主要在做什么？
答：我最近主要实习做一些量化金融衍生相关的开发工作，也在尝试用 AI 做一些更完整的小项目。

示例 2
问：你擅长什么？
答：我比较擅长把复杂问题讲清楚，也比较关注 AI 应用、内容表达和知识整理这几个方向。生活上擅长羽毛球、钢琴和做粤菜，打游戏也不错（CS2，空洞骑士等）
"""

@app.route("/chat", methods=["POST"])
def chat():
    """
    接收前端发来的问题，调用 Qwen 大模型返回回复
    """
    data = request.json
    question = data.get("question", "")

    try:
        # 调用 Qwen3.5-Plus
        response = Generation.call(
            model="qwen3.5-plus",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        # 提取回复内容
        reply = response.output.choices[0].message.content

    except Exception as e:
        # 如果 API 调用失败，返回错误信息
        print(f"API 调用失败：{e}")
        reply = "抱歉，我的数字分身现在有点累，暂时回答不了这个问题。你可以直接联系我——联系方式在页面上方~"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # 启动 Flask 服务
    # debug=True 表示开启调试模式，改代码后自动重启
    # port=5000 表示服务运行在 5000 端口
    app.run(debug=True, port=5000)
