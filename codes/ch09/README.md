# 第 9 章：独立开发与测试

```text
sdk/include/plugin_api.h   双方共用的契约
mock_host.cpp              假宿主，加载插件并打印注册结果
tests/test_registry.cpp    自己写的断言测试
```

## 编译

```bash
cmake -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

## 用法

```bash
mock_host path/to/hello_plugin.dll
```

预期输出：

```text
加载 path/to/hello_plugin.dll
  命令: hello      打印一句问候
init 返回 0
```
