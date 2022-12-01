from requests import post
def log(message):
    # posts a message to the console webhook
    post("https://discord.com/api/webhooks/1041867604140245033/131FwZNLM5eweobvHKj9uBzecqx7vszWus2fzNKknIk-d1AaPf0mk47CgGmZBWFHRajj", data={"content": message})
    print(message)

def error(message):
    # posts a message to the error
    post("https://discord.com/api/webhooks/1041861788653867068/Af49AFKrf_Dl5eX5NyeRuVMs8v17qvgw0boynU5LC_Be3MlWEkGC6biejjH1d2VDmBLH", data={"content": message})
    print(message)