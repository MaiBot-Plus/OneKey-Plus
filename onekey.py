#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MaiBot-Plus 一键管理程序
功能：
1. 启动各种服务（Bot、Adapter、Matcha-Adapter）
2. 更新GitHub仓库
3. 管理配置文件
"""

import os
import sys
import subprocess
import time
import base64
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    """控制台颜色"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"

    @staticmethod
    def red(text):
        return f"{Colors.RED}{text}{Colors.END}"

    @staticmethod
    def green(text):
        return f"{Colors.GREEN}{text}{Colors.END}"

    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.END}"

    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.END}"

    @staticmethod
    def cyan(text):
        return f"{Colors.CYAN}{text}{Colors.END}"

    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.END}"


class MaiBotManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.absolute()
        self.venv_python = self.base_path / ".venv" / "Scripts" / "python.exe"
        self.running_processes: Dict[str, subprocess.Popen] = {}

        # GitHub Access Token (编码，仅具有指定仓库的读取权限)
        # 权限：Contents(Read), Metadata(Read)
        # 适用仓库：MaiMbot-Pro-Max, Napcat-Adapter, Matcha-Adapter
        self._github_token_encoded = (
            "Z2hwX2NPVlVkYk8wa2RBVzM1bEVJaHdqUmxFQlNIQUwyRjNoSll4Rg=="
        )

        # 服务配置
        self.services = {
            "bot": {
                "name": "MaiBot 主程序",
                "path": self.base_path / "Bot",
                "main_file": "bot.py",
                "description": "AI聊天机器人主程序",
                "repo_url": "https://github.com/MaiBot-Plus/MaiMbot-Pro-Max.git",
                "type": "python",
            },
            "adapter": {
                "name": "Napcat Adapter",
                "path": self.base_path / "Adapter",
                "main_file": "main.py",
                "description": "QQ消息适配器",
                "repo_url": "https://github.com/MaiBot-Plus/Napcat-Adapter.git",
                "type": "python",
            },
            "matcha_adapter": {
                "name": "Matcha Adapter",
                "path": self.base_path / "Matcha-Adapter",
                "main_file": "main.py",
                "description": "Matcha消息适配器",
                "repo_url": "https://github.com/MaiBot-Plus/Matcha-Adapter.git",
                "type": "python",
            },
            "napcat": {
                "name": "Napcat 服务",
                "path": self.base_path / "Napcat" / "Shell",
                "main_file": "napcat.bat",
                "description": "QQ协议服务",
                "repo_url": None,
                "type": "batch",
            },
            "matcha": {
                "name": "Matcha 程序",
                "path": self.base_path / "Matcha",
                "main_file": "matcha.exe",
                "description": "Matcha客户端程序",
                "repo_url": None,
                "type": "exe",
            },
        }

    def check_for_chinese_chars_in_path(self):
        """检查当前路径是否包含中文字符"""
        path_str = str(self.base_path)
        for char in path_str:
            if "\u4e00" <= char <= "\u9fff":
                print(Colors.red("=" * 60))
                print(Colors.red(Colors.bold("错误：程序路径中包含中文字符！")))
                print(Colors.yellow(f"当前路径: {path_str}"))
                print(Colors.yellow("请将程序移动到纯英文路径下再运行。"))
                print(Colors.red("=" * 60))
                input("按回车键退出...")
                sys.exit(1)

    def clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        """打印程序头部"""
        print("=" * 60)
        print(Colors.cyan(Colors.bold("          MaiBot-Plus 一键管理程序")))
        print(Colors.yellow("              Version 1.0"))
        print("=" * 60)
        print(Colors.blue("Edited by 阿范 @212898630"))

    def _get_github_token(self) -> Optional[str]:
        """获取GitHub访问Token"""
        try:
            token = base64.b64decode(self._github_token_encoded).decode("utf-8")
            return token
        except Exception as e:
            print(Colors.red(f"获取GitHub Token失败: {e}"))
            return None

    def print_menu(self):
        """打印主菜单"""
        print(Colors.bold("主菜单："))
        print()
        print(Colors.green("快捷启动服务管理："))
        print("  1. 启动服务组合 →")
        print("  2. 启动 MaiBot 主程序")
        print("  3. 启动 Napcat Adapter")
        print("  4. 启动 Napcat 服务")
        print("  5. 启动 Matcha Adapter")
        print("  6. 启动 Matcha 程序")
        print("  7. 查看运行状态")
        print("  8. 启动数据库管理程序")
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
        print("  18. 尝试自我修复 pip 权限问题（仅供测试，安装依赖报错时使用）")
        print()
        print(Colors.yellow("仓库状态检查："))
        print("  15. 检查 MaiBot-Pro-Max 仓库状态")
        print("  16. 检查 Adapter 仓库状态")
        print("  17. 检查 Matcha-Adapter 仓库状态")
        print("  0. 退出程序")
        print()

    def print_service_groups_menu(self):
        """打印服务组合菜单"""
        print(Colors.bold("选择启动组："))
        print()
        print(Colors.green("  1. QQ机器人组合"))
        print("     └─ MaiBot主程序 + Napcat Adapter + Napcat服务")
        print("     └─ 用于连接QQ平台")
        print()
        print(Colors.green("  2. Matcha机器人组合"))
        print("     └─ MaiBot主程序 + Matcha Adapter + Matcha程序")
        print("     └─ 用于连接Matcha平台")
        print()
        print(Colors.cyan("  0. 返回主菜单"))
        print()

    def start_service_group(self):
        """启动服务组合"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_service_groups_menu()

            choice = input(Colors.bold("请选择组合 (0-2): ")).strip()

            if choice == "0":
                return
            elif choice == "1":
                print(Colors.blue("正在启动QQ机器人组合..."))
                print()
                success_count = 0
                services = ["bot", "adapter", "napcat"]
                for service in services:
                    if self.start_service(service):
                        success_count += 1
                        time.sleep(2)  # 延迟启动避免冲突

                print()
                print(
                    Colors.green(
                        f"✅ QQ机器人组合启动完成 ({success_count}/{len(services)} 个服务成功)"
                    )
                )

            elif choice == "2":
                print(Colors.blue("正在启动Matcha机器人组合..."))
                print()
                success_count = 0
                services = ["bot", "matcha_adapter", "matcha"]
                for service in services:
                    if self.start_service(service):
                        success_count += 1
                        time.sleep(2)  # 延迟启动避免冲突

                print()
                print(
                    Colors.green(
                        f"✅ Matcha机器人组合启动完成 ({success_count}/{len(services)} 个服务成功)"
                    )
                )

            else:
                print(Colors.red("无效选择，请输入 0-2 之间的数字"))

            if choice in ["1", "2"]:
                print()
                input("按回车键返回...")
                return

    def run_command(
        self, cmd: List[str], cwd: Optional[Path] = None, show_output: bool = True
    ) -> tuple:
        """运行命令"""
        try:
            if cwd:
                result = subprocess.run(
                    cmd,
                    cwd=cwd,
                    capture_output=not show_output,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=not show_output,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )
            return result.returncode == 0, result.stdout if not show_output else ""
        except Exception as e:
            print(Colors.red(f"命令执行失败: {e}"))
            return False, str(e)

    def run_command_with_env(
        self,
        cmd: List[str],
        cwd: Optional[Path] = None,
        env: Optional[dict] = None,
        show_output: bool = True,
    ) -> tuple:
        """运行命令（支持自定义环境变量）"""
        try:
            if cwd:
                result = subprocess.run(
                    cmd,
                    cwd=cwd,
                    env=env,
                    capture_output=not show_output,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )
            else:
                result = subprocess.run(
                    cmd,
                    env=env,
                    capture_output=not show_output,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )

            # 返回成功状态和详细信息（包括stdout和stderr）
            if not show_output:
                output_info = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
                return result.returncode == 0, output_info
            else:
                return result.returncode == 0, ""

        except Exception as e:
            print(Colors.red(f"命令执行失败: {e}"))
            return False, str(e)

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

        if (
            service_key in self.running_processes
            and self.running_processes[service_key].poll() is None
        ):
            print(Colors.yellow(f"{service['name']} 已经在运行中"))
            return True

        print(Colors.blue(f"正在启动 {service['name']}..."))

        try:
            service_type = service.get("type", "python")

            if service_type == "python":
                # Python服务 - 在新的PowerShell窗口中启动
                powershell_cmd = [
                    "powershell.exe",
                    "-NoExit",
                    "-Command",
                    f"cd '{service_path}'; & '{self.venv_python}' '{main_file}'",
                ]

                process = subprocess.Popen(
                    powershell_cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    cwd=service_path,
                )

            elif service_type == "batch":
                # 批处理文件 - 在新的CMD窗口中启动
                batch_path = service_path / main_file
                cmd_command = [
                    "cmd.exe",
                    "/c",
                    "start",
                    "cmd.exe",
                    "/k",
                    str(batch_path),
                ]

                process = subprocess.Popen(cmd_command, cwd=service_path)

            elif service_type == "exe":
                # 可执行文件 - 直接启动
                process = subprocess.Popen(
                    [str(service_path / main_file)],
                    cwd=service_path,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )

            else:
                print(Colors.red(f"不支持的服务类型: {service_type}"))
                return False

            self.running_processes[service_key] = process
            print(
                Colors.green(
                    f"✅ {service['name']} 已在新窗口启动 (PID: {process.pid})"
                )
            )

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
                print(
                    Colors.red(f"停止 {self.services[service_key]['name']} 失败: {e}")
                )

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
                    pid_info = f"(PID: {process.pid}) - 运行在独立窗口"
                else:
                    status = Colors.red("🔴 已停止")
                    pid_info = ""
                    del self.running_processes[service_key]
            else:
                status = Colors.yellow("⚪ 未启动")
                pid_info = ""

            print(f"  {service['name']}: {status} {pid_info}")

        if self.running_processes:
            print()
            print(Colors.cyan("提示：服务运行在独立的PowerShell窗口中"))
            print(Colors.cyan("关闭对应窗口即可停止服务"))
        print()

    def start_sqlite_studio(self):
        """启动SQLiteStudio数据库管理程序"""
        sqlite_studio_path = self.base_path / "SQLiteStudio" / "SQLiteStudio.exe"

        if not sqlite_studio_path.exists():
            print(Colors.red(f"❌ SQLiteStudio未找到: {sqlite_studio_path}"))
            return False

        try:
            print(Colors.blue("正在启动SQLiteStudio数据库管理程序..."))

            # 使用subprocess.Popen启动程序，不等待程序结束
            process = subprocess.Popen(
                [str(sqlite_studio_path)],
                cwd=str(sqlite_studio_path.parent),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )

            print(Colors.green("✅ SQLiteStudio数据库管理程序已启动"))
            print(Colors.cyan("数据库文件位置：Bot/data/MaiBot.db"))
            return True

        except Exception as e:
            print(Colors.red(f"❌ 启动SQLiteStudio失败: {e}"))
            return False

    def update_repository(self, service_key: str):
        """更新仓库"""
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

        print(Colors.yellow(f"准备更新 {service['name']} 仓库"))
        print(Colors.yellow("更新将会覆盖本地修改，请确认是否继续？"))
        confirm = input("输入 'yes' 确认更新，其他任意输入取消: ").strip().lower()

        if confirm != "yes":
            print(Colors.blue("取消更新"))
            return False

        print(Colors.blue(f"正在更新 {service['name']} 仓库..."))

        # 获取GitHub Token
        github_token = self._get_github_token()

        if github_token:
            # 使用Token进行认证更新
            success = self._update_with_token(service, repo_path, github_token)
        else:
            print(Colors.red("GitHub Token不可用，无法更新私有仓库"))
            print(Colors.cyan("提示：请检查Token配置或手动更新"))
            return False

        if success:
            print(Colors.green(f"✅ {service['name']} 仓库更新成功"))

            # 更新依赖
            requirements_file = repo_path / "requirements.txt"
            if requirements_file.exists():
                print(Colors.blue("正在更新依赖包..."))

                # 尝试多种安装方式
                install_commands = [
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        "requirements.txt",
                    ],
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "--user",
                        "-r",
                        "requirements.txt",
                    ],
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "--force-reinstall",
                        "-r",
                        "requirements.txt",
                    ],
                ]

                dep_success = False
                for cmd in install_commands:
                    dep_success, _ = self.run_command(
                        cmd, cwd=repo_path, show_output=False
                    )
                    if dep_success:
                        break

                if dep_success:
                    print(Colors.green("✅ 依赖包更新成功"))
                else:
                    print(Colors.yellow("⚠️ 依赖包更新可能有问题，建议手动检查"))

            return True
        else:
            print(Colors.red(f"❌ {service['name']} 仓库更新失败"))
            return False

    def _update_with_token(self, service: dict, repo_path: Path, token: str) -> bool:
        """使用Token进行认证更新"""
        try:
            # 构造带认证的URL
            repo_url = service.get("repo_url", "")
            if repo_url.startswith("https://github.com/"):
                # 对于新格式的GitHub Personal Access Token，使用以下格式之一：
                # 方式1: https://token@github.com/user/repo.git (推荐)
                # 方式2: https://username:token@github.com/user/repo.git
                # 方式3: https://token:x-oauth-basic@github.com/user/repo.git

                # 尝试方式1：只使用token作为用户名
                auth_url = repo_url.replace(
                    "https://github.com/", f"https://{token}@github.com/"
                )

                # 保存原始Git配置
                original_helper = self._get_git_config(repo_path, "credential.helper")
                original_askpass = self._get_git_config(repo_path, "core.askpass")

                try:
                    # 彻底禁用Git凭据助手和交互
                    self._set_git_config(repo_path, "credential.helper", "")
                    self._set_git_config(repo_path, "core.askpass", "")

                    # 设置环境变量作为双重保险
                    env = os.environ.copy()
                    env["GIT_TERMINAL_PROMPT"] = "0"
                    env["GIT_ASKPASS"] = ""
                    env["SSH_ASKPASS"] = ""
                    env["GCM_INTERACTIVE"] = "never"  # 禁用Git Credential Manager

                    # 设置远程URL
                    set_url_cmd = ["git", "remote", "set-url", "origin", auth_url]
                    success, output = self.run_command_with_env(
                        set_url_cmd, cwd=repo_path, env=env, show_output=False
                    )

                    if not success:
                        stderr = (
                            output.get("stderr", "")
                            if isinstance(output, dict)
                            else str(output)
                        )
                        print(Colors.red("设置认证URL失败"))
                        print(Colors.red(f"错误信息: {stderr}"))
                        return False

                    # 执行 git pull
                    pull_success, pull_output = self.run_command_with_env(
                        ["git", "pull"], cwd=repo_path, env=env, show_output=False
                    )

                    # 恢复原始URL（移除token）
                    restore_url_cmd = ["git", "remote", "set-url", "origin", repo_url]
                    restore_success, restore_output = self.run_command_with_env(
                        restore_url_cmd, cwd=repo_path, env=env, show_output=False
                    )

                    if not restore_success:
                        stderr = (
                            restore_output.get("stderr", "")
                            if isinstance(restore_output, dict)
                            else str(restore_output)
                        )
                        print(Colors.yellow(f"恢复原始URL失败: {stderr}"))

                    if pull_success:
                        stdout = (
                            pull_output.get("stdout", "")
                            if isinstance(pull_output, dict)
                            else str(pull_output)
                        )
                        print(Colors.green("✅ 使用Token认证更新成功"))
                        if stdout.strip():
                            print(Colors.cyan(f"更新信息: {stdout.strip()}"))
                        return True
                    else:
                        stdout = (
                            pull_output.get("stdout", "")
                            if isinstance(pull_output, dict)
                            else ""
                        )
                        stderr = (
                            pull_output.get("stderr", "")
                            if isinstance(pull_output, dict)
                            else str(pull_output)
                        )
                        returncode = (
                            pull_output.get("returncode", -1)
                            if isinstance(pull_output, dict)
                            else -1
                        )

                        print(Colors.red(f"Token认证更新失败"))
                        print(Colors.yellow("详细错误信息:"))
                        print(Colors.yellow(f"  返回码: {returncode}"))
                        if stdout.strip():
                            print(Colors.yellow(f"  标准输出: {stdout.strip()}"))
                        if stderr.strip():
                            print(Colors.yellow(f"  错误输出: {stderr.strip()}"))
                        return False

                finally:
                    # 恢复原始Git配置
                    self._restore_git_config(
                        repo_path, "credential.helper", original_helper
                    )
                    self._restore_git_config(
                        repo_path, "core.askpass", original_askpass
                    )

            else:
                print(Colors.red("不支持的仓库URL格式"))
                return False

        except Exception as e:
            print(Colors.red(f"Token认证更新出错: {e}"))
            import traceback

            print(Colors.red(f"详细错误: {traceback.format_exc()}"))
            return False

    def _get_git_config(self, repo_path: Path, key: str) -> Optional[str]:
        """获取Git配置值"""
        try:
            result = subprocess.run(
                ["git", "config", "--local", "--get", key],
                cwd=repo_path,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",  # 忽略编码错误
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def _set_git_config(self, repo_path: Path, key: str, value: str):
        """设置Git配置值"""
        try:
            subprocess.run(
                ["git", "config", "--local", key, value],
                cwd=repo_path,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",  # 忽略编码错误
            )
        except:
            pass

    def _restore_git_config(
        self, repo_path: Path, key: str, original_value: Optional[str]
    ):
        """恢复Git配置值"""
        try:
            if original_value is not None:
                subprocess.run(
                    ["git", "config", "--local", key, original_value],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )
            else:
                subprocess.run(
                    ["git", "config", "--local", "--unset", key],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",  # 忽略编码错误
                )
        except:
            pass

    def _update_without_token(self, service: dict, repo_path: Path) -> bool:
        """不使用Token的普通更新"""
        # 禁用Git交互提示
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"  # 禁用终端提示
        env["GIT_ASKPASS"] = "echo"  # 禁用密码提示
        env["SSH_ASKPASS"] = "echo"  # 禁用SSH密码提示

        success, output = self.run_command_with_env(
            ["git", "pull"], cwd=repo_path, env=env, show_output=False
        )
        if not success:
            print(Colors.red(f"普通git pull也失败: {output}"))
            print(Colors.cyan("提示：如果是私有仓库，请确保已配置Git认证"))
        return success

    def install_requirements(self):
        """安装/更新所有依赖包"""
        print(Colors.blue("正在检查并安装所有依赖包..."))

        for service_key, service in self.services.items():
            requirements_file = service["path"] / "requirements.txt"
            if requirements_file.exists():
                print(Colors.blue(f"正在安装 {service['name']} 的依赖..."))

                # 尝试多种安装方式
                install_commands = [
                    # 方式1: 标准安装
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        str(requirements_file),
                    ],
                    # 方式2: 使用用户模式安装
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "--user",
                        "-r",
                        str(requirements_file),
                    ],
                    # 方式3: 忽略已安装包
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "--force-reinstall",
                        "-r",
                        str(requirements_file),
                    ],
                    # 方式4: 使用缓存目录
                    [
                        str(self.venv_python),
                        "-m",
                        "pip",
                        "install",
                        "--cache-dir",
                        str(self.base_path / ".pip_cache"),
                        "-r",
                        str(requirements_file),
                    ],
                ]

                success = False
                for i, cmd in enumerate(install_commands):
                    print(Colors.yellow(f"尝试安装方式 {i + 1}/4..."))
                    success, output = self.run_command(cmd, show_output=True)
                    if success:
                        print(Colors.green(f"✅ {service['name']} 依赖安装完成"))
                        break
                    else:
                        print(Colors.yellow(f"方式 {i + 1} 失败，尝试下一种方式..."))

                if not success:
                    print(
                        Colors.red(f"❌ {service['name']} 依赖安装失败，请尝试手动安装")
                    )
                    print(
                        Colors.red(
                            f"手动安装命令: cd {service['path']} && {self.venv_python} -m pip install -r requirements.txt"
                        )
                    )

        print(Colors.green("依赖安装检查完成"))

    def check_repository_status(self, service_key):
        """检查指定仓库的commit状态（支持Token认证）"""
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

        # 获取GitHub Token
        github_token = self._get_github_token()

        try:
            # 切换到仓库目录
            original_cwd = os.getcwd()
            os.chdir(repo_path)

            # 设置环境变量禁用Git交互
            env = os.environ.copy()
            env["GIT_TERMINAL_PROMPT"] = "0"  # 禁用终端提示
            env["GIT_ASKPASS"] = "echo"  # 禁用密码提示
            env["SSH_ASKPASS"] = "echo"  # 禁用SSH密码提示
            env["GCM_INTERACTIVE"] = "never"  # 禁用Git Credential Manager

            # 如果有token，先设置认证URL
            original_url = None
            if github_token:
                print(Colors.blue("使用Token认证获取远程仓库更新..."))

                # 获取原始URL
                get_url_result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    env=env,
                )

                if get_url_result.returncode == 0:
                    original_url = get_url_result.stdout.strip()

                    # 构造带token的URL
                    if original_url.startswith("https://github.com/"):
                        auth_url = original_url.replace(
                            "https://github.com/", f"https://{github_token}@github.com/"
                        )

                        # 临时设置认证URL
                        set_url_result = subprocess.run(
                            ["git", "remote", "set-url", "origin", auth_url],
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                            errors="ignore",
                            env=env,
                        )

                        if set_url_result.returncode != 0:
                            print(Colors.yellow("设置认证URL失败，使用普通方式检查"))
                            github_token = None
            else:
                print(Colors.blue("正在获取远程仓库更新..."))

            # 获取远程更新
            fetch_result = subprocess.run(
                ["git", "fetch", "origin"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                env=env,
            )

            # 恢复原始URL（如果使用了token）
            if github_token and original_url:
                subprocess.run(
                    ["git", "remote", "set-url", "origin", original_url],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    env=env,
                )

            if fetch_result.returncode != 0:
                print(Colors.red(f"获取远程更新失败: {fetch_result.stderr}"))
                if github_token:
                    print(
                        Colors.yellow(
                            "提示：Token认证获取失败，可能是网络问题或Token权限不足"
                        )
                    )
                else:
                    print(
                        Colors.yellow("提示：未使用Token认证，可能因为网络限制导致失败")
                    )
                return
            else:
                if github_token:
                    print(Colors.green("✅ 使用Token认证成功获取远程更新"))
                else:
                    print(Colors.green("✅ 成功获取远程更新"))

            # 获取当前分支
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                env=env,
            )
            current_branch = branch_result.stdout.strip() or "master"

            # 检查本地与远程的差异
            log_result = subprocess.run(
                ["git", "log", f"HEAD..origin/{current_branch}", "--oneline"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                env=env,
            )

            if log_result.returncode != 0:
                print(Colors.red(f"检查commit差异失败: {log_result.stderr}"))
                return

            commits_behind = log_result.stdout.strip()

            if not commits_behind:
                print(Colors.green("✅ 仓库已是最新状态，没有落后的commit"))
            else:
                commit_lines = commits_behind.split("\n")
                commit_count = len(commit_lines)

                print(Colors.yellow(f"你的本地仓库落后了 {commit_count} 个commit"))
                print()
                print(Colors.bold("落后的commit详情："))
                print("-" * 50)

                for i, commit_line in enumerate(commit_lines, 1):
                    if commit_line.strip():
                        commit_hash = commit_line.split()[0]
                        commit_message = " ".join(commit_line.split()[1:])
                        print(
                            f"{Colors.cyan(f'{i:2d}.')} {Colors.yellow(commit_hash)} {commit_message}"
                        )

                print("-" * 50)

                # 显示详细的commit信息
                print()
                print(Colors.bold("详细的commit信息："))
                print("=" * 60)

                detail_result = subprocess.run(
                    [
                        "git",
                        "log",
                        f"HEAD..origin/{current_branch}",
                        "--pretty=format:%h - %an, %ar : %s",
                        "-10",
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    env=env,
                )

                if detail_result.returncode == 0 and detail_result.stdout.strip():
                    for line in detail_result.stdout.strip().split("\n"):
                        if line.strip():
                            parts = line.split(" - ", 1)
                            if len(parts) == 2:
                                commit_hash = parts[0]
                                rest = parts[1]
                                print(f"{Colors.green(commit_hash)} - {rest}")

                print("=" * 60)

        except Exception as e:
            print(Colors.red(f"检查仓库状态时发生错误: {e}"))
        finally:
            # 恢复原始工作目录
            os.chdir(original_cwd)

        print()

    def show_system_info(self):
        """显示系统信息"""
        print(Colors.bold("系统信息："))
        print()

        # Python版本
        try:
            result = subprocess.run(
                [str(self.venv_python), "--version"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            python_version = result.stdout.strip()
            print(f"  Python版本: {Colors.green(python_version)}")
        except:
            print(f"  Python版本: {Colors.red('获取失败')}")

        # 工作目录
        print(f"  工作目录: {Colors.cyan(str(self.base_path))}")

        # 虚拟环境
        venv_status = (
            Colors.green("已配置")
            if self.venv_python.exists()
            else Colors.red("未配置")
        )
        print(f"  虚拟环境: {venv_status}")

        # 仓库状态
        print("  仓库状态:")
        for service_key, service in self.services.items():
            repo_exists = service["path"].exists()
            status = Colors.green("存在") if repo_exists else Colors.red("不存在")
            print(f"    {service['name']}: {status}")

        print()

    def fix_pip_permissions(self):
        """修复 pip 权限问题"""
        print(Colors.bold("修复 pip 权限问题"))
        print(Colors.yellow("这个功能将尝试修复Python包安装时的权限问题"))
        print()

        # 1. 升级pip
        print(Colors.blue("步骤 1: 升级 pip..."))
        upgrade_commands = [
            [str(self.venv_python), "-m", "pip", "install", "--upgrade", "pip"],
            [
                str(self.venv_python),
                "-m",
                "pip",
                "install",
                "--user",
                "--upgrade",
                "pip",
            ],
        ]

        pip_upgraded = False
        for cmd in upgrade_commands:
            success, _ = self.run_command(cmd, show_output=True)
            if success:
                print(Colors.green("✅ pip 升级成功"))
                pip_upgraded = True
                break

        if not pip_upgraded:
            print(Colors.yellow(" pip 升级失败，但继续进行其他修复步骤"))

        # 2. 清除pip缓存
        print(Colors.blue("步骤 2: 清除 pip 缓存..."))
        cache_commands = [
            [str(self.venv_python), "-m", "pip", "cache", "purge"],
            ["pip", "cache", "purge"],
        ]

        for cmd in cache_commands:
            success, _ = self.run_command(cmd, show_output=False)
            if success:
                print(Colors.green("✅ pip 缓存清除成功"))
                break

        # 3. 创建pip配置文件夹
        print(Colors.blue("步骤 3: 配置 pip..."))
        pip_config_dir = self.base_path / ".pip"
        pip_config_dir.mkdir(exist_ok=True)

        # 4. 检查虚拟环境权限
        print(Colors.blue("步骤 4: 检查虚拟环境权限..."))
        venv_dir = self.base_path / ".venv"
        if venv_dir.exists():
            try:
                # 尝试在虚拟环境中创建测试文件
                test_file = venv_dir / "test_permissions.txt"
                test_file.write_text("test")
                test_file.unlink()
                print(Colors.green("✅ 虚拟环境权限正常"))
            except Exception as e:
                print(Colors.red(f"❌ 虚拟环境权限有问题: {e}"))
                print(Colors.yellow("建议以管理员身份运行程序"))

        # 5. 提供解决方案建议
        print()
        print(Colors.bold("权限问题解决建议："))
        print(Colors.cyan("1. 以管理员身份运行 Windows PowerShell 或 CMD"))
        print(Colors.cyan("2. 使用 --user 参数安装包（已在程序中自动尝试）"))
        print(Colors.cyan("3. 检查防病毒软件是否阻止了文件写入"))
        print(Colors.cyan("4. 确保虚拟环境目录有写入权限"))
        print(Colors.cyan("5. 如果问题持续，可以尝试重新创建虚拟环境"))
        print()

        # 6. 重新尝试安装依赖
        retry = input("是否现在重新尝试安装依赖包？(y/n): ").strip().lower()
        if retry == "y":
            self.install_requirements()

        input(Colors.blue("按回车键返回主菜单..."))

    def run(self):
        """运行主程序"""
        self.check_for_chinese_chars_in_path()
        try:
            while True:
                self.clear_screen()
                self.print_header()
                self.print_menu()

                try:
                    choice = input(Colors.bold("请选择操作 (0-18): ")).strip()

                    if choice == "0":
                        print(Colors.green("程序退出，感谢使用！"))
                        break
                    elif choice == "1":
                        self.start_service_group()
                    elif choice == "2":
                        self.start_service("bot")
                    elif choice == "3":
                        self.start_service("adapter")
                    elif choice == "4":
                        self.start_service("napcat")
                    elif choice == "5":
                        self.start_service("matcha_adapter")
                    elif choice == "6":
                        self.start_service("matcha")
                    elif choice == "7":
                        self.show_status()
                    elif choice == "8":
                        self.start_sqlite_studio()
                    elif choice == "9":
                        self.update_repository("bot")
                    elif choice == "10":
                        self.update_repository("adapter")
                    elif choice == "11":
                        self.update_repository("matcha_adapter")
                    elif choice == "12":
                        print(Colors.blue("正在更新所有仓库..."))
                        for service_key in [
                            "bot",
                            "adapter",
                            "matcha_adapter",
                        ]:  # 只更新有仓库的服务
                            if self.services[service_key].get("repo_url"):
                                self.update_repository(service_key)
                    elif choice == "13":
                        self.install_requirements()
                    elif choice == "14":
                        self.show_system_info()
                    elif choice == "15":
                        self.check_repository_status("bot")
                    elif choice == "16":
                        self.check_repository_status("adapter")
                    elif choice == "17":
                        self.check_repository_status("matcha_adapter")
                    elif choice == "18":
                        self.fix_pip_permissions()
                    else:
                        print(Colors.red("无效选择，请输入 0-18 之间的数字"))

                    if choice != "0":
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
    # 设置控制台支持ANSI颜色（Windows）
    if os.name == "nt":
        os.system("color")
        # 尝试启用ANSI转义序列支持
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass

    manager = MaiBotManager()
    manager.run()
