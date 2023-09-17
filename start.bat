@echo off
@chcp 65001

setlocal enabledelayedexpansion

echo 正在包裝 Docker 映像檔...
docker build -t panicle_extract_image . 

echo 程式開始進行推論...
docker run -it panicle_extract_image

:input_loop
set /P is_custom_path="是否需要自訂輸出結果存放的資料夾路徑？(y/n): "
echo.

@REM 防呆判斷，看使用者要不要自訂路徑
if /i "%is_custom_path%"=="y" (
    set /P local_path="請輸入想要存放的資料夾路徑: "

    if exist "!local_path!" (
        @REM echo 路徑存在
    ) else (
        echo 錯誤: 路徑不存在，請輸入有效路徑
        echo.
        goto input_loop
    )
) else if /i "!is_custom_path!"=="n" (
    SET result_folder=result
    mkdir result
    set local_path=!cd!\result
    echo 使用預設路徑 !local_path!
) else (
    echo 請輸入有效的選項 'y' 或 'n'
    echo.
    goto input_loop
)

@REM 找出執行的映象檔(迭代輸出結果)
for /f "tokens=*" %%a in ('docker ps -q -n 1') do (
    set "container_id=%%a"
)

@REM 複製輸出結果到本地端
echo 準備將結果複製到路徑 !local_path! 中...
echo.
echo data 資料夾為測試集，predictions 資料夾為推論結果
echo.
docker cp !container_id!:/app/predictions !local_path!
docker cp !container_id!:/app/data !local_path!
echo.

@REM 停止容器
echo | set /p="停止容器 "
docker stop !container_id!

@REM 删除容器
echo | set /p="刪除容器 "
docker rm !container_id!

pause