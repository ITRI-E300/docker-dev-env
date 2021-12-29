# DENV
## 安裝
```bash
sudo python3 -m pip install -U git+https://github.com/ITRI-E300/docker-dev-env#subdirectory=cli
```
## 使用
### CLI
#### 配置設定檔
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
#### 建立Container
```bash
denv create
```
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