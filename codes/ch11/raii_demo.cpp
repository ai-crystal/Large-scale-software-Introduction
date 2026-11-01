// 第 11 章：RAII 示例
//
// RAII 的意思是“资源获取即初始化”：
// 把资源的生命周期绑在一个对象上，对象析构时自动释放。
//
// 这样不管函数从哪条路径返回，哪怕中间抛了异常，
// 资源都会被释放，不用在每个 return 前面写 close/delete。

#include <cstdio>
#include <memory>
#include <string>

#ifdef _WIN32
#include <windows.h>
#endif

// 一个很小的文件包装类。
class FileHandle {
public:
    // 构造时打开文件。
    explicit FileHandle(const char* path)
        : file_(std::fopen(path, "rb")) {}

    // 析构时自动关闭。对象离开作用域就会执行这里。
    ~FileHandle() {
        if (file_) std::fclose(file_);
    }

    // 禁止复制。
    // 如果两个对象持有同一个文件，第一个析构关掉，第二个再关一次会出错。
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    std::FILE* get() const { return file_; }

    // 让对象能放在 if 里判断，比如 if (!file) { ... }
    explicit operator bool() const { return file_ != nullptr; }

private:
    std::FILE* file_;
};

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 打开当前源文件，读一小段。
    FileHandle file("raii_demo.cpp");
    if (!file) {
        std::printf("打不开文件\n");
        return 1;
    }

    char buffer[128]{};
    size_t got = std::fread(buffer, 1, sizeof(buffer) - 1, file.get());
    std::printf("读到 %zu 字节，第一行：%.40s\n", got, buffer);

    // 智能指针：离开作用域自动 delete，不需要手写 delete。
    auto value = std::make_unique<int>(42);
    std::printf("unique_ptr 里的值：%d\n", *value);

    // 函数结束时，value 先释放，file 后释放。
    return 0;
}
