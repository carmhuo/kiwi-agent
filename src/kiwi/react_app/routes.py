from flask import Blueprint, render_template, request, Response, stream_with_context, current_app as app
from .graph import agent

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index3.html')

# 流式输出 LangGraph 的响应
@bp.route('/api/stream', methods=['GET'])
def stream_langgraph():
    # 获取用户输入的查询文本
    question = request.args.get('query', '')
  
    def generate():
        try:
            for chunk in agent.stream(
                {"messages": [{"role": "user", "content": question}]}, stream_mode="values"):
                try:
                    json_resp = chunk["messages"][-1].model_dump_json()
                    # yield json_resp + "\n"
                    yield f"data: {json_resp}\n\n"
                except KeyError as e:
                    app.logger.error(f"数据结构异常: {str(e)}")
                    yield f"event: error\ndata: 数据解析失败\n\n"
                except Exception as e:
                    app.logger.error(f"消息生成异常: {str(e)}")
                    yield f"event: error\ndata: 服务暂时不可用\n\n"
        except Exception as e:
            app.logger.error(f"流处理异常: {str(e)}")
            yield f"event: fatal\ndata: 连接已终止\n\n"
        finally:
            # 发送结束标记
            yield "event: end\ndata: stream-completed\n\n"
    response = Response(
        stream_with_context(generate()),
        content_type='text/event-stream; charset=utf-8'
    )
    # 配置CORS头
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'no-cache')
    return response
