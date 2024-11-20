# SimpleServerAPI

## 简介

一个基于fastapi+redis实现的简易api服务，不依赖数据库，具备用户身份验证和会话缓存。所有数据由`data/*.json`数据文件提供，仅供测试或临时服务使用。

* 测试环境：centos 7

## API

### /api/status
> 判断相关服务是否正常启动或处于运行状态
> 
- 请求类型：**GET**
- 传入参数：无
- 返回数据参考

```json
{"code": 200, "message": "OK"} // 1. 成功
// 2. 网络异常失败
```

### /api/ticket
> 判断账户是否合法，并注册会话
> 
- 请求类型：**POST**
- 传入参数：账户密码

```json
{"username": "user1","password": "A1B2C3D4E5F6G7H8I9HD"}
```
- 本地数据，见`data/users.json`
- 返回数据
```json
// 1. 登录成功，返回会话token或其他可用身份
{ 
	"data": { 
		"CSRFPreventionToken": "", 
		"ticket": "", 
		...} 
}
{"data": ""} // 2. 登录失败，返回空或者其他报错信息
// 3. 网络异常报错
```

### /api/info
> 获取（可选：用户账户下）所有可用机器
> 
- 请求类型：**GET**
- 传入参数：用户身份tiket

```json
X-Auth-Token xxx
```

- 返回数据，见`data/machines.json`
```json
// 1. 可用机器信息，加**表示必须字段
{
	"data" : [
		{
			"id": 100,                   // **机器ID
			"cpus": 32,                  // **机器CPU核心数
			"status": "running",         // **机器运行状态
			"mem": 11591667560,          // **机器的运行内存，单位B
			"GPU": "NVIDIA RTX4090",     // **机器的GPU类型
			"ip": "192.168.1.100",       // **机器DHCP的IPv4地址
			"name": "Aimlab001",         // 机器名称（字符串简单标识）
			"maxdisk": 128849018880,     // 机器磁盘空间，单位B
						...                    // 其他机器可用信息
		},
		... // 省略多台信息
		 ,
		{
			"id": 200,                   // **机器ID
			"cpus": 24,                  // **机器CPU核心数
			"status": "stoppped",        // **机器运行状态
			"mem": 11591667560,          // **机器的运行内存，单位B
			"GPU": "NVIDIA RTX3090",     // **机器的GPU类型
			"ip": "192.168.1.200",       // **机器DHCP的IPv4地址
			"name": "Aimlab200",         // 机器名称（字符串简单标识）
			"maxdisk": 128849018880,     // 机器磁盘空间，单位B
						...                    // 其他机器可用信息
		}
	]
}
// 2. 网络异常，请求失败
```

## 使用方法
* 依赖安装
```shell
# miniconda installed

# redis installed

pip install -r requirements.txt
```

* 部署方式
```python
# 本地测试环境
uvicorn app.main:app --reload
# 本地生产环境
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# UNIX实际环境
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```