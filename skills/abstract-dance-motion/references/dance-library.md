# 舞蹈动作库 · CMU Graphics Lab

**默认从 CMU Graphics Lab Motion Capture Database 按舞种找一段完整动作。** 这是一套可下载的真人骨骼动捕。先看官方条目的动作描述、采样率和 Animated 预览，再按同一个试次编号拿 BVH。原库提供 ASF/AMC 等格式，BVH 是 Bruce Hahne 转换后的分发版本。 [官方目录](https://mocap.cs.cmu.edu/subjects.php) · [官方格式说明](https://mocap.cs.cmu.edu/resources.php) · [固定版本的 BVH 目录](https://github.com/una-dinosauria/cmu-mocap/tree/09a07f54f3bbb58797325f009282d0b2048a2871/data)

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

CMU 允许将数据用于作品及商业产品，使用时保留出处。条款禁止直接转售动作数据。头、肩、髋、膝和踝适合驱动线条人，手掌可据前臂另画。CMU 说明手部和脚趾关节可能有噪声，手指和拇指是便于编辑的占位关节。 [CMU 使用条款及数据说明](https://mocap.cs.cmu.edu/) · [CMU FAQ](https://mocap.cs.cmu.edu/faqs.php)

> The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.
