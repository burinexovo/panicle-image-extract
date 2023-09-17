# 稻穗影像去背模型


## 介绍

這個項目基於 U2net 架構，旨在應用於從手機拍攝的圖像中提取稻穗圖像並去除背景。這個預處理方法可用於進一步分析，如估計穀物的含水量。由於 U2net 在背景去除的圖像分割任務方面表現出色，因此選擇了基於這個架構訓練去背模型。

此 Repository 為包裝稻穗影像去背模型之 Docker 映像檔包裝範例，提供 start.bat 使用者化在 Windows 能夠輕鬆執行。

## 功能

- 使用 U2net 模型進行圖像分割和背景去除。
- 適用於將手機拍攝的圖像中的稻穗提取出來。
- 簡單的 Docker 映像封裝示例。

## 安裝

請確保已經安裝 [Docker 應用程式](https://www.docker.com/get-started/)。

由於 AI 模型過大無法上傳至 GitHub，請先[下載](https://drive.google.com/file/d/1kSJ87WazpchF85UEeN5N2IFOi5a5Hfu_/view?usp=sharing)模型後並放至 models 資料夾中

## 使用

### 在 Windows 上執行

執行後會自動進行映像檔包裝、推論等操作。

    打開 `start.bat` 文件。

### 在 macOS 上執行（處理中...）