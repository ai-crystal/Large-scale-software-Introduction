#include <cstdio>
#include <memory>
#include <string>

class FileHandle {
public:
    explicit FileHandle(const char* path)
        : file_(std::fopen(path, "rb")) {}

    ~FileHandle() {
        if (file_) std::fclose(file_);
    }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    std::FILE* get() const { return file_; }
    explicit operator bool() const { return file_ != nullptr; }

private:
    std::FILE* file_;
};

int main() {
    FileHandle file("raii_demo.cpp");
    if (!file) {
        std::printf("打不开文件\n");
        return 1;
    }

    char buffer[128]{};
    size_t got = std::fread(buffer, 1, sizeof(buffer) - 1, file.get());
    std::printf("读到 %zu 字节，第一行：%.40s\n", got, buffer);

    auto value = std::make_unique<int>(42);
    std::printf("unique_ptr 里的值：%d\n", *value);
    return 0;
}
