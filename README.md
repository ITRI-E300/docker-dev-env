# DENV
Docker開發環境

## 安裝
```bash
sudo python3 -m pip install -U git+https://github.com/ITRI-E300/docker-dev-env#subdirectory=cli
```
#### 配置設定檔 (Optional)
在家目錄下配置`.denv.conf.json`
```json
{
    "device":{
        "device_a":"/data1",
        "device_b":"/data2"
    }
}
```
- `device`: 在創建新的volume的時候能夠提供額外存放選項，若無可空


## 使用
### CLI
#### 建立Container
```bash
denv create
```
> 使用`--dry_run`來測試指令
#### 建立新Volume
```bash
denv create_volume
```
#### 列出所有可用映像檔
```bash
denv list
```
#### 更新映像檔
```bash
denv update
```
### 使用 (DockerHub)
待補充

## 維護指南
### Repo結構
- `.github/`: Github Action 設定檔，當有Push(或每月)自動建置新映像檔
- `cli/`: 建立 Container 的輔助工具
- `dockerfile/`: 映像檔建構檔案

sudo docker build -t test -f py3.9.8-jupyter-vscode .
sudo docker run -itd --rm --gpus all -v p208:/user_data --name=p208 -e"NAME"=p208 -e"PASSWORD"=p2002   -p 14001:22 -p 14002:8888 -p 14003:8080 test