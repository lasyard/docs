# 吐槽 macOS 的显示器设置

极发太

现在用 macOS 的人也越来越多了。不得不说，苹果在人机界面上还是很用心的，用起来很丝滑——但是不丝滑的时候也真是让人“眼前一黑”。

在 Windows 上，当我们修改显示器设置的时候，会有一个倒计时的对话框出现：

![windows_alter_display.png](/_images/weixin/windows_alter_display.png)

“否”是默认设置。如果不点“是”，倒计时结束后设置恢复原状态。这个对话框看起来是一个冗余的步骤，但是当你的显示器不支持新设置的时候你就会感谢它的。

然而在 macOS 上，新设置直接就应用了啊。然后显示器就这样了：

![dell_d2720ds_unsupported.jpg](/_images/weixin/dell_d2720ds_unsupported.jpg)

我用的是一台 Macbook, 而且习惯了合着盖子用外接显示器，当台式机使。这时候是不是只需要镇定地打开笔记本盖子，重新设置显示器就行了呢？毕竟自带的屏幕还是正常的啊。

事实上只要打开盖子，显示器就立刻恢复了，看起来十分美好，但我却隐隐嗅到了一丝不妙的气息。果然，系统贴心地为不同的使用状态保存了不同的设置，也就是说，不管我在双显示器的状态下怎么设置，只要合上盖子，外接显示器仍然会用那个不正常的设置。

这心情就好比是《黑客帝国 3: 革命》里尼奥在地铁站沿着隧道狂奔了一站地之后，发现自己又回到了原来的站台。

![vlcsnap_matrix_revolutions.jpg](/_images/weixin/vlcsnap_matrix_revolutions.jpg)

道理上讲，这个设置一定存在硬盘的某个（些）文件里，可惜我不知道。没办法，开始联机求助。

- 首先问 AI, AI 很热情地教我怎么打开显示器设置窗口……
- 然后上 Apple 官网搜文档，找到了相关话题，链接竟然失效……
- 最终用搜索引擎成功解决——总有人遇到和你一样的问题。

最后说一下解决的办法。打开命令行终端，删除以下两个文件（命令中的星号会匹配到一个 UUID）：

```sh
sudo rm /Library/Preferences/com.apple.windowserver.plist
rm ~/Library/Preferences/ByHost/com.apple.windowserver.*.plist
```

然后重启，所有显示器设置回到默认。果然只有命令行才能完全控制电脑。

PS: 有人说现在人写文章不会用破折号了，所以文中特意用了两次。
