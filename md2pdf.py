import os
import logging
import subprocess

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def validate_path(path, must_exist=True):
    """验证路径是否为合法目录"""
    if must_exist and not os.path.isdir(path):
        raise ValueError(f"指定的路径不是一个有效的目录: {path}")
    return path


def convert_md_to_pdf(md_path, output_path):
    # 验证输入路径
    md_path = validate_path(md_path, must_exist=True)

    # 确保输出路径存在，即使它不存在也会被创建
    os.makedirs(output_path, exist_ok=True)

    # 验证输出路径（允许不存在）
    output_path = validate_path(output_path, must_exist=False)

    # 遍历所有 Markdown 文件
    for filename in os.listdir(md_path):
        if filename.endswith('.md'):
            md_file_path = os.path.join(md_path, filename)

            # 构建输出 PDF 文件路径
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_file_path = os.path.join(output_path, pdf_filename)

            # 构建 pandoc 命令
            cmd = [
                "pandoc",
                md_file_path,
                "-f", "markdown",
                "-t", "pdf",
                "-o", pdf_file_path,
                "--pdf-engine=wkhtmltopdf",
                "-V", "mainfont=SimSun",
                "--standalone",  # 确保不重复生成文档结构
                "--listings",
                "--wrap=none",  # 确保 pandoc 不会自动换行
                "-c", "styles.css",  # 引用CSS文件
            ]

            try:
                # 使用 subprocess.run 执行命令，并指定编码为 utf-8
                result = subprocess.run(
                    cmd, check=True, text=True, capture_output=True, encoding='utf-8')
                logging.info(f"成功将 {filename} 转换为 PDF")
            except subprocess.CalledProcessError as e:
                logging.error(f"转换 {filename} 时发生错误: {e.stderr}")
            except UnicodeDecodeError as e:
                logging.error(f"解码子进程输出时发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    input_directory = r''
    output_directory = r'p'
    try:
        convert_md_to_pdf(input_directory, output_directory)
    except Exception as e:
        logging.error(f"程序运行时发生错误: {e}")
