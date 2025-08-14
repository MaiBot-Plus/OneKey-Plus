#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MaiBot-Plus 一键管理程序 (Linux版本)
功能：
1. 启动各种服务（Bot、Adapter、Matcha-Adapter）
2. 更新GitHub仓库
3. 管理配置文件
"""

import os
import sys
import subprocess
import time
import json
import base64
import platform
from pathlib import Path
from typing import Dict, List, Optional

class Colors:
    """控制台颜色"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @staticmethod
    def red(text): return f"{Colors.RED}{text}{Colors.END}"
    @staticmethod
    def green(text): return f"{Colors.GREEN}{text}{Colors.END}"
    @staticmethod
    def yellow(text): return f"{Colors.YELLOW}{text}{Colors.END}"
    @staticmethod
    def blue(text): return f"{Colors.BLUE}{text}{Colors.END}"
    @staticmethod
    def cyan(text): return f"{Colors.CYAN}{text}{Colors.END}"
    @staticmethod
    def bold(text): return f"{Colors.BOLD}{text}{Colors.END}"

class MaiBotManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.absolute()
        self.is_windows = platform.system().lower() == 'windows'
        
        # 根据操作系统设置虚拟环境Python路径
        if self.is_windows:
            self.venv_python = self.base_path / ".venv" / "Scripts" / "python.exe"
        else:
            self.venv_python = self.base_path / ".venv" / "bin" / "python"
        
        self.running_processes: Dict[str, subprocess.Popen] = {}
        
        # GitHub Access Token (仅具有指定仓库的读取权限)
        self._github_token_encoded = "Z2hwX2NPVlVkYk8wa2RBVzM1bEVJaHdqUmxFQlNIQUwyRjNoSll4Rg=="
        
        # 服务配置
        self.services = {
            "bot": {
                "name": "MaiBot 主程序",
                "path": self.base_path / "Bot",
                "main_file": "bot.py",
                "description": "AI聊天机器人主程序",
                "repo_url": "https://github.com/MaiBot-Plus/MaiMbot-Pro-Max.git",
                "type": "python"
            },
            "adapter": {
                "name": "Napcat Adapter",
                "path": self.base_path / "Adapter",
                "main_file": "main.py",
                "description": "QQ消息适配器",
                "repo_url": "https://github.com/MaiBot-Plus/Napcat-Adapter.git",
                "type": "python"
            },
            "matcha_adapter": {
                "name": "Matcha Adapter",
                "path": self.base_path / "Matcha-Adapter",
                "main_file": "main.py", 
                "description": "Matcha消息适配器",
                "repo_url": "https://github.com/MaiBot-Plus/Matcha-Adapter.git",
                "type": "python"
            }
        }
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if self.is_windows else 'clear')
    
    def print_header(self):
        """打印程序头部"""
        system_info = "Windows" if self.is_windows else "Linux"
        print("=" * 60)
        print(Colors.cyan(Colors.bold("          MaiBot-Plus 一键管理程序")))
        print(Colors.yellow(f"              Version 1.0 ({system_info})"))
        print("=" * 60)
        print(Colors.blue("Edited by 阿范 @212898630"))
    
    def _get_github_token(self) -> Optional[str]:
        """获取GitHub访问Token"""
        try:
            token = base64.b64decode(self._github_token_encoded).decode('utf-8')
            return token
        except Exception as e:
            print(Colors.red(f"获取GitHub Token失败: {e}"))
            return None

    def print_menu(self):
        """打印主菜单"""
        print(Colors.bold("主菜单："))
        print()
        print(Colors.green("快捷启动服务管理："))
        print("  1. 启动 MaiBot 主程序")
        print("  2. 启动 Napcat Adapter")
        print("  3. 启动 Matcha Adapter")
        print("  7. 查看运行状态")
        print("  8. 停止所有服务")
        print()
        print(Colors.blue("更新管理："))
        print("  9. 更新 Bot 仓库")
        print("  10. 更新 Adapter 仓库")
        print("  11. 更新 Matcha-Adapter 仓库")
        print("  12. 更新所有仓库")
        print()
        print(Colors.yellow("其他功能："))
        print("  13. 安装/更新依赖包")
        print("  14. 查看系统信息")
        print()
        print(Colors.yellow("仓库状态检查："))
        print("  15. 检查 MaiBot-Pro-Max 仓库状态")
        print("  16. 检查 Adapter 仓库状态")
        print("  17. 检查 Matcha-Adapter 仓库状态")
        print("  0. 退出程序")
        print()
    
    def start_service(self, service_key: str):
        """启动服务"""
        if service_key not in self.services:
            print(Colors.red(f"未知服务: {service_key}"))
            return False
        
        service = self.services[service_key]
        service_path = service["path"]
        main_file = service["main_file"]
        
        if not service_path.exists():
            print(Colors.red(f"服务目录不存在: {service_path}"))
            return False
        
        if not (service_path / main_file).exists():
            print(Colors.red(f"主程序文件不存在: {service_path / main_file}"))
            return False
        
        if service_key in self.running_processes and self.running_processes[service_key].poll() is None:
            print(Colors.yellow(f"{service['name']} 已经在运行中"))
            return True
        
        print(Colors.blue(f"正在启动 {service['name']}..."))
        
        try:
            if self.is_windows:
                # Windows版本使用CREATE_NEW_CONSOLE
                powershell_cmd = [
                    "powershell.exe", "-NoExit", "-Command",
                    f"cd '{service_path}'; & '{self.venv_python}' '{main_file}'"
                ]
                process = subprocess.Popen(
                    powershell_cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    cwd=service_path
                )
            else:
                # Linux版本尝试在新终端中启动
                terminal_found = False
                terminal_commands = [
                    ["gnome-terminal", "--", "bash", "-c", f"cd '{service_path}' && '{self.venv_python}' '{main_file}'; read -p 'Press Enter to exit...'"],
                    ["konsole", "-e", "bash", "-c", f"cd '{service_path}' && '{self.venv_python}' '{main_file}'; read -p 'Press Enter to exit...'"],
                    ["xfce4-terminal", "-e", f"bash -c \"cd '{service_path}' && '{self.venv_python}' '{main_file}'; read -p 'Press Enter to exit...'\""],
                    ["xterm", "-e", f"bash -c \"cd '{service_path}' && '{self.venv_python}' '{main_file}'; read -p 'Press Enter to exit...'\""]
                ]
                
                for cmd in terminal_commands:
                    try:
                        process = subprocess.Popen(cmd, cwd=service_path)
                        terminal_found = True
                        break
                    except FileNotFoundError:
                        continue
                
                if not terminal_found:
                    # 如果没有找到图形终端，在后台运行
                    print(Colors.yellow("未找到图形终端，在后台运行..."))
                    process = subprocess.Popen(
                        [str(self.venv_python), main_file],
                        cwd=service_path
                    )
            
            self.running_processes[service_key] = process
            print(Colors.green(f"✅ {service['name']} 已启动 (PID: {process.pid})"))
            return True
            
        except Exception as e:
            print(Colors.red(f"启动 {service['name']} 失败: {e}"))
            return False
    
    def stop_all_services(self):
        """停止所有服务"""
        if not self.running_processes:
            print(Colors.yellow("没有正在运行的服务"))
            return
        
        print(Colors.blue("正在停止所有服务..."))
        for service_key, process in list(self.running_processes.items()):
            try:
                process.terminate()
                print(Colors.green(f"✅ 已停止 {self.services[service_key]['name']}"))
            except Exception as e:
                print(Colors.red(f"停止 {self.services[service_key]['name']} 失败: {e}"))
        
        self.running_processes.clear()
        print(Colors.green("所有服务已停止"))
    
    def show_status(self):
        """显示运行状态"""
        print(Colors.bold("服务运行状态："))
        print()
        
        for service_key, service in self.services.items():
            if service_key in self.running_processes:
                process = self.running_processes[service_key]
                if process.poll() is None:
                    status = Colors.green("🟢 运行中")
                    pid_info = f"(PID: {process.pid})"
                else:
                    status = Colors.red("🔴 已停止")
                    pid_info = ""
                    del self.running_processes[service_key]
            else:
                status = Colors.yellow("⚪ 未启动")
                pid_info = ""
            
            print(f"  {service['name']}: {status} {pid_info}")
        print()
    
    def install_requirements(self):
        """安装/更新所有依赖包"""
        print(Colors.blue("正在检查并安装所有依赖包..."))
        
        for service_key, service in self.services.items():
            requirements_file = service["path"] / "requirements.txt"
            if requirements_file.exists():
                print(Colors.blue(f"正在安装 {service['name']} 的依赖..."))
                
                # 尝试多种安装方式
                install_commands = [
                    [str(self.venv_python), '-m', 'pip', 'install', '-r', str(requirements_file)],
                    [str(self.venv_python), '-m', 'pip', 'install', '--user', '-r', str(requirements_file)],
                    [str(self.venv_python), '-m', 'pip', 'install', '--force-reinstall', '-r', str(requirements_file)]
                ]
                
                success = False
                for i, cmd in enumerate(install_commands):
                    print(Colors.yellow(f"尝试安装方式 {i+1}/3..."))
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                        if result.returncode == 0:
                            print(Colors.green(f"✅ {service['name']} 依赖安装完成"))
                            success = True
                            break
                        else:
                            print(Colors.yellow(f"方式 {i+1} 失败，尝试下一种方式..."))
                    except Exception as e:
                        print(Colors.red(f"命令执行失败: {e}"))
                
                if not success:
                    print(Colors.red(f"❌ {service['name']} 依赖安装失败，请尝试手动安装"))
                    print(Colors.red(f"手动安装命令: cd {service['path']} && {self.venv_python} -m pip install -r requirements.txt"))
        
        print(Colors.green("依赖安装检查完成"))
    
    def show_system_info(self):
        """显示系统信息"""
        print(Colors.bold("系统信息："))
        print()
        
        # Python版本
        try:
            result = subprocess.run([str(self.venv_python), '--version'], 
                                  capture_output=True, text=True)
            python_version = result.stdout.strip()
            print(f"  Python版本: {Colors.green(python_version)}")
        except Exception:
            print(f"  Python版本: {Colors.red('获取失败')}")
        
        # 工作目录
        print(f"  工作目录: {Colors.cyan(str(self.base_path))}")
        
        # 虚拟环境
        venv_status = Colors.green("已配置") if self.venv_python.exists() else Colors.red("未配置")
        print(f"  虚拟环境: {venv_status}")
        
        # 仓库状态
        print(f"  仓库状态:")
        for service_key, service in self.services.items():
            repo_exists = service["path"].exists()
            status = Colors.green("存在") if repo_exists else Colors.red("不存在")
            print(f"    {service['name']}: {status}")
        
        print()
    def update_repository(self, service_key: str):
        """更新仓库（简化版本）"""
        if service_key not in self.services:
            print(Colors.red(f"未知服务: {service_key}"))
            return False
        
        service = self.services[service_key]
        
        # 检查是否有仓库URL
        if not service.get("repo_url"):
            print(Colors.yellow(f"{service['name']} 没有关联的Git仓库，跳过更新"))
            return True
        
        repo_path = service["path"]
        
        if not repo_path.exists():
            print(Colors.red(f"仓库目录不存在: {repo_path}"))
            return False
        
        print(Colors.blue(f"正在更新 {service['name']} 仓库..."))
        
        try:
            # 简化的git pull
            result = subprocess.run(
                ['git', 'pull'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(Colors.green(f"✅ {service['name']} 仓库更新成功"))
                return True
            else:
                print(Colors.red(f"❌ {service['name']} 仓库更新失败: {result.stderr}"))
                return False
                
        except Exception as e:
            print(Colors.red(f"更新 {service['name']} 仓库时出错: {e}"))
            return False
    
    def check_repository_status(self, service_key):
        """检查指定仓库的commit状态"""
        if service_key not in self.services:
            print(Colors.red(f"未找到服务: {service_key}"))
            return
            
        service = self.services[service_key]
        repo_path = service["path"]
        repo_name = service["name"]
        
        if not repo_path.exists():
            print(Colors.red(f"仓库目录不存在: {repo_path}"))
            return
            
        if not service.get("repo_url"):
            print(Colors.red(f"{repo_name} 没有配置远程仓库URL"))
            return
        
        print(Colors.bold(f"检查 {repo_name} 仓库状态..."))
        print(f"路径: {Colors.cyan(str(repo_path))}")
        print()
        
        try:
            # 获取远程更新
            print(Colors.blue("正在获取远程仓库更新..."))
            fetch_result = subprocess.run(
                ["git", "fetch", "origin"],
                capture_output=True, text=True, encoding='utf-8',
                cwd=repo_path
            )
            
            if fetch_result.returncode != 0:
                print(Colors.red(f"获取远程更新失败: {fetch_result.stderr}"))
                return
            
            # 检查本地与远程的差异
            log_result = subprocess.run(
                ["git", "log", "HEAD..origin/main", "--oneline"],
                capture_output=True, text=True, encoding='utf-8',
                cwd=repo_path
            )
            
            if log_result.returncode != 0:
                # 尝试master分支
                log_result = subprocess.run(
                    ["git", "log", "HEAD..origin/master", "--oneline"],
                    capture_output=True, text=True, encoding='utf-8',
                    cwd=repo_path
                )
            
            if log_result.returncode == 0:
                commits_behind = log_result.stdout.strip()
                
                if not commits_behind:
                    print(Colors.green("✅ 仓库已是最新状态，没有落后的commit"))
                else:
                    commit_lines = commits_behind.split('\n')
                    commit_count = len(commit_lines)
                    
                    print(Colors.yellow(f"你的本地仓库落后了 {commit_count} 个commit"))
                    print()
                    print(Colors.bold("落后的commit详情："))
                    print("-" * 50)
                    
                    for i, commit_line in enumerate(commit_lines, 1):
                        if commit_line.strip():
                            commit_hash = commit_line.split()[0]
                            commit_message = ' '.join(commit_line.split()[1:])
                            print(f"{Colors.cyan(f'{i:2d}.')} {Colors.yellow(commit_hash)} {commit_message}")
                    
                    print("-" * 50)
            else:
                print(Colors.red(f"检查commit差异失败: {log_result.stderr}"))
                
        except Exception as e:
            print(Colors.red(f"检查仓库状态时发生错误: {e}"))
        
        print()

    def run(self):
        """运行主程序"""
        try:
            while True:
                self.clear_screen()
                self.print_header()
                self.print_menu()
                
                try:
                    choice = input(Colors.bold("请选择操作 (0-17): ")).strip()
                    
                    if choice == '0':
                        self.stop_all_services()
                        print(Colors.green("程序退出，感谢使用！"))
                        break
                    elif choice == '1':
                        self.start_service('bot')
                    elif choice == '2':
                        self.start_service('adapter')
                    elif choice == '3':
                        self.start_service('matcha_adapter')
                    elif choice == '7':
                        self.show_status()
                    elif choice == '8':
                        self.stop_all_services()
                    elif choice == '9':
                        self.update_repository('bot')
                    elif choice == '10':
                        self.update_repository('adapter')
                    elif choice == '11':
                        self.update_repository('matcha_adapter')
                    elif choice == '12':
                        print(Colors.blue("正在更新所有仓库..."))
                        for service_key in ['bot', 'adapter', 'matcha_adapter']:
                            if self.services[service_key].get("repo_url"):
                                self.update_repository(service_key)
                    elif choice == '13':
                        self.install_requirements()
                    elif choice == '14':
                        self.show_system_info()
                    elif choice == '15':
                        self.check_repository_status('bot')
                    elif choice == '16':
                        self.check_repository_status('adapter')
                    elif choice == '17':
                        self.check_repository_status('matcha_adapter')
                    else:
                        print(Colors.red("无效选择，请输入 0-17 之间的数字"))
                    
                    if choice != '0':
                        print()
                        input("按回车键返回主菜单...")
                
                except KeyboardInterrupt:
                    print(Colors.yellow("\n检测到 Ctrl+C，正在安全退出..."))
                    self.stop_all_services()
                    break
                except Exception as e:
                    print(Colors.red(f"发生错误: {e}"))
                    input("按回车键返回主菜单...")
        
        except Exception as e:
            print(Colors.red(f"程序发生致命错误: {e}"))
            self.stop_all_services()

if __name__ == "__main__":
    manager = MaiBotManager()
    manager.run()
        