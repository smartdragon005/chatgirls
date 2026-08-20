import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# 自动获取脚本所在的目录
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

def show_message(title, msg):
    """显示消息弹窗"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, msg)
    root.destroy()

def ask_yes_no(title, msg):
    """显示确认弹窗，返回 True/False"""
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno(title, msg)
    root.destroy()
    return result

def run_command(cmd, step_name):
    """执行命令，并等待完成"""
    print(f"\n{'='*50}")
    print(f"[{step_name}]")
    print(f"执行命令: {cmd}")
    print(f"{'='*50}")
    
    result = subprocess.run(cmd, shell=True, cwd=PROJECT_DIR)
    
    if result.returncode == 0:
        print(f"✅ {step_name} 完成")
    else:
        print(f"❌ {step_name} 失败，错误码: {result.returncode}")
    
    return result.returncode == 0

def create_www_folder():
    """自动创建 www 文件夹"""
    www_path = os.path.join(PROJECT_DIR, "www")
    
    # 如果 www 已存在，询问是否删除重建
    if os.path.exists(www_path):
        if not ask_yes_no("⚠️ www 已存在", 
                          f"www 文件夹已存在\n\n"
                          f"是否删除并重新创建？\n"
                          f"（选「否」则跳过此步骤）"):
            print("⏭️ 跳过创建 www 文件夹")
            return True
        # 删除旧的 www 文件夹
        import shutil
        shutil.rmtree(www_path)
        print("🗑️ 已删除旧的 www 文件夹")
    
    # 创建 www 文件夹
    os.makedirs(www_path)
    print(f"📁 已创建 www 文件夹: {www_path}")
    
    show_message("✅ 创建成功", 
                 f"已创建 www 文件夹\n\n"
                 f"请手动把以下文件/文件夹复制到 www 里：\n"
                 f"  - index.html\n"
                 f"  - img/\n"
                 f"  - audio/\n"
                 f"  - 其他资源\n\n"
                 f"完成后点击「确定」继续...")
    return True

def main():
    # 检查是否在正确的目录
    if not os.path.exists(os.path.join(PROJECT_DIR, "index.html")):
        show_message("错误", 
                     f"找不到 index.html\n"
                     f"当前目录: {PROJECT_DIR}\n\n"
                     f"请确保 build.py 和 index.html 在同一个文件夹里")
        return
    
    show_message("Android APK 打包工具", 
                 f"项目目录: {PROJECT_DIR}\n"
                 f"点击「确定」开始...")
    
    steps = [
        ("npm init -y", "初始化 Node.js 项目"),
        ("npm install @capacitor/core @capacitor/cli", "安装 Capacitor 核心库"),
        ("npm install @capacitor/android", "安装 Capacitor Android 平台"),
        ('npx cap init "Girls3" "com.wlaoshi520.Girls3"', "初始化 Capacitor 项目"),
    ]
    
    for cmd, step_name in steps:
        if not ask_yes_no("确认执行", 
                          f"即将执行:\n{cmd}\n\n"
                          f"点击「是」执行，点击「否」跳过"):
            print(f"⏭️ 跳过: {step_name}")
            continue
        
        run_command(cmd, step_name)
        
        if not ask_yes_no("继续", 
                          f"✅ {step_name} 完成\n\n"
                          f"点击「是」继续下一步，点击「否」中止"):
            print("⏹️ 用户中止")
            return
    
    # 创建 www 文件夹（只创建，不复制）
    if not create_www_folder():
        show_message("❌ 错误", "创建 www 文件夹失败，脚本终止")
        return
    
    # 添加 Android 平台
    if ask_yes_no("确认执行", 
                  "即将执行:\nnpx cap add android\n\n"
                  "点击「是」执行"):
        run_command("npx cap add android", "添加 Android 平台")
    
    # 手动操作：替换图标
    show_message("⚠️ 手动操作", 
                 "请手动完成以下操作：\n\n"
                 "1. 进入 android/app/src/main/res/\n"
                 "2. 删除所有 mipmap-anydpi-v26 文件夹（如果有）\n"
                 "3. 把你自己制作的图标文件替换到对应的 mipmap 文件夹中\n"
                 "   文件名必须统一改为: ic_launcher.png\n\n"
                 "完成后点击「确定」继续")
    
    # 同步
    if ask_yes_no("确认执行", 
                  "即将执行:\nnpx cap copy android\n\n"
                  "点击「是」执行"):
        run_command("npx cap copy android", "同步网页文件到 Android 项目")
    
    # 打开 Android Studio
    if ask_yes_no("确认执行", 
                  "即将执行:\nnpx cap open android\n\n"
                  "点击「是」打开 Android Studio"):
        run_command("npx cap open android", "用 Android Studio 打开项目")
    
    show_message("🎉 完成！", 
                 "所有命令执行完成！\n\n"
                 "请等待 Android Studio 加载完成后，\n"
                 "点击 Build → Build APK(s) 打包")

if __name__ == "__main__":
    main()