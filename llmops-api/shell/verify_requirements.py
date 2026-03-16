#!/usr/bin/env python3
"""
版本一致性验证工具
检查requirements.txt中的包版本与实际环境中的版本是否一致
"""
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def get_installed_packages(env_name: str = "LLMOps") -> Dict[str, str]:
    """获取指定环境中已安装的包及其版本"""
    try:
        result = subprocess.run(
            ["conda", "run", "-n", env_name, "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        
        packages = {}
        for line in result.stdout.strip().split('\n'):
            if '==' in line:
                name, version = line.split('==', 1)
                packages[name.lower()] = version
        return packages
    except subprocess.CalledProcessError as e:
        print(f"错误: 无法获取环境 {env_name} 的包信息")
        print(f"错误信息: {e.stderr}")
        sys.exit(1)

def parse_requirements(file_path: str) -> Dict[str, str]:
    """解析requirements.txt文件"""
    req_file = Path(file_path)
    if not req_file.exists():
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    
    packages = {}
    with open(req_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' in line:
                    name, version = line.split('==', 1)
                    packages[name.lower()] = version
    return packages

def compare_versions(req_packages: Dict[str, str], installed_packages: Dict[str, str]) -> Tuple[List[str], List[str], List[str]]:
    """比较版本差异"""
    matching = []
    different = []
    missing = []
    
    for name, req_version in req_packages.items():
        if name in installed_packages:
            installed_version = installed_packages[name]
            if req_version == installed_version:
                matching.append(f"{name}=={req_version}")
            else:
                different.append(f"{name}: requirements.txt={req_version}, installed={installed_version}")
        else:
            missing.append(name)
    
    return matching, different, missing

def main():
    print("=" * 60)
    print("版本一致性验证工具")
    print("=" * 60)
    
    # 获取实际安装的包
    print("\n1. 获取LLMOps环境中已安装的包...")
    installed_packages = get_installed_packages("LLMOps")
    print(f"   找到 {len(installed_packages)} 个已安装的包")
    
    # 解析requirements.txt
    print("\n2. 解析requirements.txt文件...")
    req_file = "/home/wissfi/projects/LLMOps/requirements.txt"
    req_packages = parse_requirements(req_file)
    print(f"   找到 {len(req_packages)} 个依赖包")
    
    # 比较版本
    print("\n3. 比较版本差异...")
    matching, different, missing = compare_versions(req_packages, installed_packages)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    
    if matching:
        print(f"\n✅ 版本匹配的包 ({len(matching)} 个):")
        for pkg in matching[:10]:  # 只显示前10个
            print(f"   {pkg}")
        if len(matching) > 10:
            print(f"   ... 还有 {len(matching) - 10} 个")
    
    if different:
        print(f"\n❌ 版本不一致的包 ({len(different)} 个):")
        for pkg in different:
            print(f"   {pkg}")
    
    if missing:
        print(f"\n⚠️  在环境中未找到的包 ({len(missing)} 个):")
        for pkg in missing:
            print(f"   {pkg}")
    
    # 总结
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    total = len(req_packages)
    match_rate = (len(matching) / total * 100) if total > 0 else 0
    print(f"总包数: {total}")
    print(f"匹配数: {len(matching)}")
    print(f"不匹配: {len(different)}")
    print(f"缺失数: {len(missing)}")
    print(f"匹配率: {match_rate:.1f}%")
    
    if different or missing:
        print("\n🔧 建议操作:")
        print("1. 运行以下命令生成正确的requirements.txt:")
        print("   conda run -n LLMOps pip freeze > requirements.txt")
        print("2. 或者运行:")
        print("   bash /home/wissfi/projects/LLMOps/llmops-api/shell/generate_requirements.sh")
        return 1
    else:
        print("\n✅ 所有包版本完全一致!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
