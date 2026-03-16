#!/bin/bash
# 最终解决方案：使用pip freeze生成准确的requirements.txt
# 避免pipreqs的网络依赖问题

echo "=========================================="
echo "生成准确的requirements.txt - 最终解决方案"
echo "=========================================="

# 方法1: 直接使用pip freeze（最可靠）
echo ""
echo "方法1: 使用pip freeze生成完整的requirements.txt"
echo "------------------------------------------------"
conda run -n LLMOps pip freeze > /home/wissfi/projects/LLMOps/requirements_freeze.txt
echo "✅ 已生成: requirements_freeze.txt (包含所有包)"

# 方法2: 生成项目实际使用的包（推荐）
echo ""
echo "方法2: 生成项目实际使用的包（推荐）"
echo "------------------------------------------------"
conda run -n LLMOps pip freeze | grep -E "(langchain|Flask|numpy|pytest|alembic|injector|python-dotenv|weaviate|Werkzeug|WTForms|blinker|certifi|charset-normalizer|click|colorama|itsdangerous|Jinja2|MarkupSafe|requests|SQLAlchemy|urllib3)" > /home/wissfi/projects/LLMOps/requirements.txt
echo "✅ 已生成: requirements.txt (仅项目使用的包)"

# 方法3: 备份原文件
echo ""
echo "方法3: 备份原始requirements.txt"
echo "------------------------------------------------"
if [ -f /home/wissfi/projects/LLMOps/requirements.txt ]; then
    cp /home/wissfi/projects/LLMOps/requirements.txt /home/wissfi/projects/LLMOps/requirements_backup.txt
    echo "✅ 已备份: requirements_backup.txt"
fi

echo ""
echo "=========================================="
echo "验证结果"
echo "=========================================="
echo ""
echo "检查生成的requirements.txt内容:"
echo "------------------------------------------------"
head -20 /home/wissfi/projects/LLMOps/requirements.txt

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="
echo ""
echo "生成的文件说明:"
echo "1. requirements_freeze.txt - 环境中所有包的完整列表"
echo "2. requirements.txt - 项目实际使用的包（推荐使用）"
echo "3. requirements_backup.txt - 原始文件的备份"
echo ""
echo "建议使用 requirements.txt 作为项目的依赖文件"
