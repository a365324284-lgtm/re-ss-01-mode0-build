RE-SS-01 Mode 0 实验性云编译

状态：构建流程已准备；未云端编译，未实机验证，不是可直接刷入的已验证固件。
用途：研究 JDCloud RE-SS-01 单个 5 GHz 无线设备超过 8 个 AP 的可行性。

基于用户提供的官方 OpenWrt 镜像所对应源码：
c4fbb6337a693864f422c018b7bf470d2ea7cfff
使用官方固件目录 feeds.buildinfo 中固定的 feeds 提交。
这是官方 OpenWrt 基础实验版，不是保留原 Kwrt/NSS/插件/远程接入配置的升级版。

修改：仅 RE-SS-01 设备树将 Mode 1 改为 0；Q6 预留区由 55 MiB 改为上游
IPQ6018 的 85 MiB。这是待验证假设，不是该设备已确认支持 Mode 0 的证明。
不强改 ath11k 数量检查，不修改其他机型，不写入密码或远程访问凭据。
若 512 MiB 设备、无线固件或驱动存在不兼容，可能无法启动或出现无线崩溃。
不要在无人现场、无法使用 U-Boot 恢复的远程路由器上测试。

使用：将本目录内容放入自己的 GitHub 仓库根目录，包含 .github 隐藏目录。
Actions -> RE-SS-01 experimental Mode 0 -> Run workflow。
流程只支持手动运行，权限 contents:read，不自动发布 Release，不自动刷机。
完成后下载 Artifacts，校验 SHA256SUMS。构建失败时同一附件保存诊断日志。
Actions 是否有足够磁盘、额度和时间取决于账户及 runner，未承诺编译成功。

实机测试须现场进行：备份并验证恢复途径，先验证基本有线管理和单 AP，
再测试 8、9、12、16 个 AP；检查 hostapd ENABLED、实际客户端连接、
数据传输、内存、内核日志和重启稳定性。不能只以 SSID 出现判定成功。

源码依据：
https://github.com/openwrt/openwrt/tree/c4fbb6337a693864f422c018b7bf470d2ea7cfff
https://github.com/torvalds/linux/blob/master/arch/arm64/boot/dts/qcom/ipq6018.dtsi
