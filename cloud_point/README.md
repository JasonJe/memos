# 基于`Potree`的`3D`点云模型展示

## 说明

* 安装
```
yarn install
```

* 运行
```
yarn run serve
```

* 点云模型参数设置

1. 点云数据生成[Potree Converter](https://github.com/potree/PotreeConverter)；

2. 配置载入数据文件参数

```
serverConfig: {
    cloudjs: 'cloud.js', # 点云源数据文件
    makeURL(path) {
        return `http://localhost:8000/resources/pointclouds/pontto/${path}`; # 点云文件地址
    },
}
```
