# Auto-Vscode-Cpp

自动安装Vscode和Cpp必要的环境.

## 出了点 bug，还没修好，可以先用 [这个](https://github.com/SDchao/AutoVsCEnv_WPF)

## 运行

```bash
python app.py
```

## 编译

需要下载安装 pyinstaller

```bash
pip install pyinstaller
```

然后编译成 exe 文件

```bash
pyinstaller -F app.py
```

注意需要 `static/index.html` 才能正常显示.

# 使用

## 下载

请去 [蓝奏云](https://wwe.lanzous.com/iYOa7jpg8oh) 下载该程序的 exe 可执行文件版本.

或者你也可以尝试一下速度极慢的 [Github Release](https://github.com/OrangeX4/Auto-Vscode-Cpp/releases/download/1.0.0/auto-vscode-cpp.zip).

## 运行

解压后, 右键以管理员身份运行.

如果没有出现问题, 你应该能看见这个界面:

![](https://s3.ax1x.com/2020/12/25/rWjQl6.png)

## 使用

### Vscode的安装

如果没有安装 Vscode, 请点击第一栏的下载安装, 下载将在后台运行, 请稍等一两分钟. 下载完成后将自动打开 Vscode 的安装程序, 请手动安装.

安装过程中, 尽量选上将 Vscode 加入环境变量的选项.

### MinGW

如果你不想安装到默认目录, 请点击"修改位置"来更改你要将 MinGW 安装到的目录. MinGW 大概会占据两百兆的空间, 请确保磁盘有足够的空间.

注意! 点击"修改位置"之后, 可能会没有任何反应, 这时候请最小化浏览器, 你会看见这样一个界面:

![](https://s3.ax1x.com/2020/12/25/rWvRVe.png)

请选择你需要安装到的目录.

选择好之后, 点击"下载安装"按钮, 后台会自动下载和安装, 请等待一两分钟. 安装成功之后, 会弹窗提示安装成功.

如果较长时间后仍无反应, 可能已经安装成功了, 但是出现 Bug 导致没有提示, 这时候请直接执行下一步操作.

### 工程文件

最为重要的一个文件夹. 请选择一个你希望放置的目录, 且要牢记这个目录的位置.

还是要注意, 选择位置可能要最小化浏览器窗口才能看见浏览文件夹窗口.

然后点击"下载安装"按钮, 因为工程文件非常小, 这个过程会迅速完成, 完成后会自动跳出安装目录的资源管理器界面.

请在 Vscode 中打开这个文件夹.

### 在 Vscode 中尝试运行测试代码

用 Vscode 打开这个工程文件夹, 你会看见如下界面.

点击 `test.cpp` 文件, 然后按下 `F5` 键, 如果没有出现问题, 你会成功地用 Vscode 编译出一个程序, 并会运行.

![](https://s3.ax1x.com/2020/12/25/rWzW9A.png)

甚至你可以进行多文件编译. 打开测试代码中的 `multifile/main.cpp`, 在调试面板中选择 `Multiple Files Compile & Run`, 再按下 `F5`, 如果成功运行, 恭喜你运行成功了!

![](https://s3.ax1x.com/2020/12/25/rWz2hd.png)

请注意, 以后你要运行的 C++ 或者 C 文件, 都应该放在这个文件夹里面. 因为 Vscode 依赖于 `.vscode` 目录来识别 C++ 的执行环境. 或者你也可以将这个 `.vscode` 目录复制到其他文件夹下, 来达到在其他文件夹下用 Vscode 调试运行代码的目的.

# 最后

这就是全部了. 感谢使用和反馈 :-)
