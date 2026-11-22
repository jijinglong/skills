# 浏览器预览与逐帧复核

[战斗时间轴模块](../assets/combat-timeline.mjs)不依赖 DOM、渲染库或计时器。向 `createCombatTimeline` 提供动作时长和事件，得到插入停顿后的播放时长、事件播放时刻，以及可任意顺序调用的 `frameAt`。Canvas、WebGL 或离线渲染可以共用这份事件数据。

## 格挡反击的事件例子

```js
import { createCombatTimeline } from './combat-timeline.mjs';

const timeline = createCombatTimeline({
  duration: 1.95,
  hitstopMs: 105,
  blockScale: 0.43,
  events: [
    { at: 0.38, kind: 'swing', actor: 'green' },
    { at: 0.47, kind: 'block', anchor: 'blade-clash' },
    { at: 0.86, kind: 'swing', actor: 'orange' },
    { at: 0.99, kind: 'miss', actor: 'orange' }
  ]
});

function draw(playbackTime) {
  const { actionTime } = timeline.frameAt(playbackTime);
  drawCharacters(actionTime);
  for (const event of timeline.events) {
    const age = playbackTime - event.playbackAt;
    if (age >= 0) drawEventEffect(event, age);
  }
}
```

`drawCharacters` 和 `drawEventEffect` 由项目实现。接触点通过 `anchor` 查找，可预先从接触动作帧采样并存进世界坐标。调用端应在目标效果结束后停止绘制。用 `timeline.playbackTimeAt(at)` 将动作节点换成进度条位置。每步按 `1 / 预览帧率` 改变播放时间，暂停和拖动都直接重绘该时刻。做成单文件 HTML 时，可将模块内联到页面；保留脚本文件时，可通过项目已有的本地服务器预览。

将上例中的格挡换成 `hit` 可做接触对照。若要做三连斩，逐击标出接触或落空时刻，第二斩的时间不应手动加上第一斩的停顿。每个接触可用 `holdMs` 覆盖默认停顿。快放和慢放改变播放时间的推进速度，事件时刻仍按同一套数据取样。调停顿后用动作时间重新定位到新时间轴。

## 从小样调整反馈

| 观察到的问题 | 优先检查 |
| --- | --- |
| 粒子在刀刃接触前出现 | 将接触特效绑定到接触帧，挥击拖尾仍从挥击阶段开始。 |
| 暂停看起来像掉帧 | 检查停顿期间粒子是否还在衰减，停顿结束后是否接上受击或格挡回弹。 |
| 落空也像打到了 | 逐帧检查刀锋与目标间距，并检查落空是否误用了接触闪光、粒子或震屏。 |
| 连击看不清每一次接触 | 缩短挡击火花或闪光尾巴，保留不同的攻击方向，并检查后续刀光与目标轮廓是否互相遮挡。 |
| 拖动时间轴后粒子位置改变 | 用随机种子和效果年龄重建粒子，或读取已采样的图集。避免依赖前一帧已经画出的内容。 |

可把上例的 105 毫秒作为重斩小样的试调值。通常先对齐姿势和接触点，再逐层调整局部闪光、粒子数与镜头位移。逐帧对照至少检查命中前一帧、接触帧、停顿末帧和反应首帧。浏览器如考虑减少动效偏好，可降低默认震屏和全屏闪烁，并保留手动调整。
