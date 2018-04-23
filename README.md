## windbg_auto_attach
​     在windows利用windbg调试漏洞时往往需要一遍又一遍的重复 “ 打开软件 -- 打开windbg -- 使用windbg附加 -- 下断点调试 ” 这一流程。开发此框架的目的便是为了让此过程自动化，让安全分析人员把精力集中在调试和利用漏洞本身

### Modules
 - attach.py : 实现框架核心功能
 - config.txt ：配置文件，可在此进行相关路径和程序运行时状态的配置 
 - command.txt：在每次windbg附加到目标程序后，自动执行其中的windbg指令

### Install
```sh
pip install -r requirments.txt
```

### Configure
**config.txt**:
```sh
[common_config]
# 从启动目标软件到获取目标件pid的间隔时间，根据软件启动时间灵活调整
sleep_time=3    

[windbg_info]
# windbg在本地系统中的安装路径
windbg_path="C:\Program Files\Debugging Tools for Windows (x86)\windbg.exe"

[forcevision]
# 软件forcevision在任务管理器中名称 和 二进制文件绝对路径
process_name= "forcevision.exe"
process_path= "E:\\forcevision.exe"

[kmplayer]
# 软件KMPlayer在任务管理器中名称 和 二进制文件绝对路径
process_name= "KMPlayer.exe"
process_path= "C:\\KMPlayer\\KMPlayer.exe"

[selected_session]
# 选择此次调试的软件名称，在此是在forcevision和kmplayer中二选一
session = kmplayer
```

**command.txt**:
```sh
bp 009cfd20
bp 009b6e1e
sxe ld:iccvid.dll
lm
g
```

## Usage:
```python
python attach.py
```