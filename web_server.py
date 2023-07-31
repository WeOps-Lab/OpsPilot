from sanic import Sanic
from sanic.response import text

app = Sanic("OpsPilot")


@app.post("/bot/train")
async def train(request):
    """
    训练机器人
    """
    bot_id = request.json['bod_id']
    return text("Hello, world.")


@app.post("/bot/deploy")
async def deploy(request):
    """
    部署机器人
    """
    bot_id = request.json['bod_id']
    return text("Hello, world.")
