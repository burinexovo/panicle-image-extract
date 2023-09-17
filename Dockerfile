# 使用 Pytorche 官方的映像作為基礎
FROM pytorch/pytorch:latest

# 安裝影像必要套件
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# 在容器中創建一個工作目錄
WORKDIR /app

# 複製 Python 程式到容器中的 /app 目錄
COPY . .

# 安裝需要的套件
RUN pip install -r requirements.txt

# 定義容器執行時的入口命令
CMD ["python", "src/main.py"]