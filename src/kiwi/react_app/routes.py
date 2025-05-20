from flask import Blueprint, render_template, request, Response, stream_with_context
from .graph import agent

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# 流式输出 LangGraph 的响应
@bp.route('/api/stream', methods=['GET'])
def stream_langgraph():
    # 获取用户输入的查询文本
    question = request.args.get('query', '')

    def generate():
        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": question}]}, stream_mode="values"):
            json_resp = chunk["messages"][-1].model_dump_json()
            # yield json_resp + "\n"
            yield f"data: {json_resp}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream; charset=utf-8")
