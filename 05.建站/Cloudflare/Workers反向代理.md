#### cloudflare 主菜单 -> Workers -> 创建服务

#### 创建 Workers -> 取名字 -> 创建

#### 编辑JS代码
```
addEventListener(
    "fetch", event => {
        let url = new URL(event.request.url);
        url.hostname = "<自己配置的域名>";
        url.protocol = "<http或者https>";
        let request = new Request(url, event.request);
        event.respondWith(
            fetch(request)
        )
    }
)
```

#### 增加路由 -> 选择区域
```
www.baidu.com/*
```