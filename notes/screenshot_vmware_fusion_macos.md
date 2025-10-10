# macOS 上的 VMware Fusion 抓屏小技巧

在 macOS 上的 VMware Fusion 中需要抓取客户机屏幕，碰到以下小问题：

1. 窗口方式下抓到的图片，四角带有 macOS 特有的小圆角
2. 全屏模式抓屏的快捷键不起作用

问题 1 暂时无法解决，但可以解决问题 2. 参考以下设置：

![macos_preference_input.png](/_images/notes/macos_preference_input.png)

这里在`偏好设置·键盘与鼠标·Mac 主机快捷键`中将右侧的 {kbd}`⌘` 键发送到客户机，左侧的 {kbd}`⌘` 键保留给宿主机使用就可以了。同时也解决了其他快捷键不灵的问题。macOS 上抓取全屏的快捷键是 {kbd}`⇧+⌘+3`.

如果在全屏模式还希望保持客户机的屏幕分辨率，可以在`偏好设置·显示`中设置全屏模式下居中：

![macos_preference_display.png](/_images/notes/macos_preference_display.png)
