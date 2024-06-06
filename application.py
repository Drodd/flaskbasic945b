from flask import Flask, request, send_file
from chattts import ChatTTS
import speech_recognition as sr
import torchaudio
import io

app = Flask(__name__)

# 初始化 ChatTTS
chat = ChatTTS.Chat()
chat.load_models(compile=False)

# 处理语音输入并生成回复
@app.route('/chat', methods=['POST'])
def chat():
    # 获取用户的语音输入
    audio_file = request.files['audio']
    audio_data = audio_file.read()

    # 使用语音识别转换为文本
    r = sr.Recognizer()
    audio = sr.AudioFile(io.BytesIO(audio_data))
    with audio as source:
        audio_text = r.recognize_google(r.record(source), language='zh-CN')
    print(f"用户说的是: {audio_text}")

    # 使用 ChatGPT 生成回复
    response = chat.infer([audio_text], params_refine_text={'prompt': '[oral_2][laugh_0][break_4]'})

    # 将回复合成为语音并返回
    output = io.BytesIO()
    torchaudio.save(output, torch.from_numpy(response[0]), 24000)
    output.seek(0)
    return send_file(output, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
