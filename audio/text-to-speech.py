#此代码运行不成功，因为此版本的python环境不支持google.cloud.texttospeech库，建议使用python3.12来运行此代码。


def synthesize_text():
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    input_file = "D:\\Gemini\\input.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    client = texttospeech.TextToSpeechClient()

    # 将从文件读取的字符串作为合成输入
    input_text = texttospeech.SynthesisInput(text=file_content)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    # 设置音色参数
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Charon",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # The response's audio_content is binary.
    # 将二进制音频内容写入本地文件
    output_file = "output.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')


synthesize_text()