# 舞蹈动作库

## 随 skill 提供的资源

用桌面浏览器打开[离线预览](../assets/preview.html)。从「动作」选择试次，点「播放」，可调视角、半速看关节和导出当前视角的 30 fps 关节 JSON。圆头和白色线条是预览样式，运动来自原始动捕。

随 skill 提供 7 条 BVH 原件，保存在 `assets/cmu/`。包括 Charleston 的 `93_03`、`93_04`、`93_08`，现代舞 `05_02`，Salsa `60_02`，Breaking `85_04`，以及印度舞 `94_01`。预览页也能直接下载当前试次的原件。

[下载完整动作包 ZIP](https://github.com/jijinglong/skills/releases/download/abstract-dance-motion-library-v1/abstract-dance-motion-library-v1.zip)（约 80 MB），解压后打开包内 `preview.html`。里面有 **116 条 CMU BVH**、同一套离线选舞与关节导出工具，以及 **2 条 ACCAD C3D** 光学标记轨迹。C3D 需要解算到目标骨架，适用 CC BY 3.0，使用时署名 **Open Motion Project by ACCAD / The Ohio State University**。 [ACCAD 原始素材](https://accad.osu.edu/research/motion-lab/mocap-system-and-data) · [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

## 从 CMU 找更多舞句

核对官方条目的动作描述、采样率与 Animated 预览，再按同一个试次编号取 BVH。原库提供 ASF/AMC 等格式。 [官方目录](https://mocap.cs.cmu.edu/subjects.php) · [官方格式说明](https://mocap.cs.cmu.edu/resources.php) · [固定版本的 BVH 目录](https://github.com/una-dinosauria/cmu-mocap/tree/09a07f54f3bbb58797325f009282d0b2048a2871/data)

| 想找的舞步 | 查阅和下载入口 |
| --- | --- |
| Charleston，小步摆踢、收脚、换重心 | [第 93 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=93)。从 [93_03 基础舞句 BVH](https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/09a07f54f3bbb58797325f009282d0b2048a2871/data/093/93_03.bvh) 开始，想找变化可看 [93_08 BVH](https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/09a07f54f3bbb58797325f009282d0b2048a2871/data/093/93_08.bvh)。 |
| 现代舞，舒展的手臂、转身和侧向伸腿 | [第 5 组](https://mocap.cs.cmu.edu/search.php?motion=%25&subjectnumber=5)。[05_02 BVH](https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/09a07f54f3bbb58797325f009282d0b2048a2871/data/005/05_02.bvh) 可先看摆臂和旋转。 |
| Salsa，连续步法和髋肩配合 | [第 60 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=60) 和 [第 61 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=61)。可从 [60_02 BVH](https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/09a07f54f3bbb58797325f009282d0b2048a2871/data/060/60_02.bvh) 试读，做独舞时先检查手位是否适合单人呈现。 |
| Breaking，站立串步与脚下变化 | [第 85 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=85)。先看 `85_03` 直立串步和 [85_04 BVH](https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/09a07f54f3bbb58797325f009282d0b2048a2871/data/085/85_04.bvh) 的脚步，组内也有翻腾等其他动作。 |
| 印度舞，姿态与连续手臂动作 | [第 94 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=94)及 [对应 BVH 目录](https://github.com/una-dinosauria/cmu-mocap/tree/09a07f54f3bbb58797325f009282d0b2048a2871/data/094)。该组的试次缺少细分描述，先看动画再挑编号。 |

## 选出可用的舞句

1. 用用户指定的舞种、独舞或双人、幅度和镜头角度筛选，只取本次需要的候选。选一段能看出预备、承重、动作高点和落脚的连续舞句。原始录制开头可能有校准站姿，截取时避开这部分。
2. 用 [BVH 投影脚本](../scripts/project_bvh.py) 从正面和略侧两个视角做短预览。选手脚分离清楚、承重转换自然的视角。拟作循环时，看末尾能否用同一支撑脚和近似骨盆姿势接回开头。若横移或手部遮挡不符合用途，先换试次或截取范围。
3. 把舞种、试次编号、原始来源、下载版本、使用条款、源帧区间、采样率和拟用拍位记在项目里。只找素材时，交付库入口与合适的候选。已明确要做动画时，保留选定原件再按拍点表投影和剪辑。

## 核对转换文件的速度

如果 BVH 文件头和 CMU 原始试次的采样率不一致，比较原始 AMC 和 BVH 的帧数，必要时对照原库预览的速度。`60_02` 的 AMC 共 2101 帧，官方标为 60 fps。上述 BVH 转换版共 2102 帧，文件头却标为 120 fps。按原库速度投影时，给脚本传 `--source-fps 60`。JSON 会同时记录 BVH 文件头与实际采用的采样率。 [CMU 第 60 组](https://mocap.cs.cmu.edu/search.php?subjectnumber=60) · [原始 AMC](https://mocap.cs.cmu.edu/subjects/60/60_02.amc)

## 使用条款

CMU 允许复制、修改和免费分发数据，也允许用于商业成片。使用时保留出处。原件及其转换后的动作数据禁止直接转售。头、肩、髋、膝和踝适合驱动线条人，手掌可据前臂另画。CMU 说明手部和脚趾关节可能有噪声，手指和拇指是便于编辑的占位关节。 [CMU 使用条款及数据说明](https://mocap.cs.cmu.edu/) · [CMU FAQ](https://mocap.cs.cmu.edu/faqs.php)

> The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.

## 其他来源

- Rokoko 的六条舞蹈提供带手指的 Mixamo 骨架 FBX，允许用于个人和商业项目。原始包从 Rokoko 获取。该包的实际关键帧间隔为 24 fps，导入时可核对文件时间基准。 [Rokoko 官方下载](https://www.rokoko.com/resources/rokoko-mocap-6-free-dance-animations)
- NUS 的舞蹈目录包含恰恰、太空步、中国舞和宝莱坞舞，仅限研究用途，禁止商用及转售。Motorica 有 Hip-hop、Popping、Locking 和复古爵士，非研究或商业用途需另外授权。 [NUS 动捕库](https://mocap.cs.sfu.ca/nusmocap.html) · [Motorica 官方条款](https://github.com/simonalexanderson/MotoricaDanceDataset)
