#  Default: ''
# c.ServerApp.websocket_url = ''
c.ServerApp.allow_remote_access = True  #远程访问
# 无效设置
c.ServerApp.notebook_dir = r'C:\Users\Administrator\Documents\000JupyterNotebook'
c.ServerApp.open_browser = True
c.ServerApp.ip = '*'
c.ServerApp.port = 8001
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$wrRoIMqduKLo7Lcq/u8uZA$pwv/dXhngcvycmb4zWNeTQ'
# 更改默认启动目录
#c.ServerApp.notebook_dir = '/home/yyx/code'
 
#内联
c.IPKernelApp.pylab = 'inline'
