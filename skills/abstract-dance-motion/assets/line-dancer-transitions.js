// Canvas 2D presets extracted from 《可以回头了》 v04.
globalThis.LineDancerTransitions = (() => {
  'use strict';

  const DURATION = 1.875;
  const PHASE_BEATS = 4;
  const OUTRO_BEAT = 28;
  const HEEL_BEAT = 28.75;
  const ORIGIN = { x: 960, y: 742 };

  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const mix = (a, b, t) => a + (b - a) * t;
  const smooth = (u) => u * u * (3 - 2 * u);
  const across = (v, a, b) => smooth(clamp((v - a) / (b - a)));
  const out = (u) => 1 - (1 - clamp(u)) ** 3;
  const radians = (deg) => deg * Math.PI / 180;
  const P = (x, y) => ({ x, y });
  const lerp = (a, b, t) => P(mix(a.x, b.x, t), mix(a.y, b.y, t));
  const offset = (p, x, y) => P(p.x + x, p.y + y);
  const norm = (x, y) => Math.hypot(x, y);

  // Two projected poses from CMU Graphics Lab trial 93_03, source frames 429 and 48.
  // The data used in this project was obtained from mocap.cs.cmu.edu.
  // The database was created with funding from NSF EIA-0196217.
  const rest = {
    Hips: P(1000.75, 465.4),
    Spine1: P(1002.1, 398.65),
    Neck1: P(1001.45, 370.75),
    Head: P(1001.25, 343.45),
    LeftArm: P(999, 371.35),
    LeftForeArm: P(997.1, 451.4),
    LeftHand: P(1046.3, 482.75),
    RightArm: P(1005.15, 387.4),
    RightForeArm: P(1000.5, 473.15),
    RightHand: P(1023.55, 526.35),
    LeftUpLeg: P(1003.85, 495.7),
    LeftLeg: P(1019.95, 618.65),
    LeftFoot: P(978.15, 732),
    LeftToeBase: P(1004.95, 737.45),
    RightUpLeg: P(1023.6, 495.2),
    RightLeg: P(1038.55, 615.75),
    RightFoot: P(998.15, 731.25),
    RightToeBase: P(1025.9, 740.6),
  };
  const introEnd = {
    Hips: P(951.1, 476.1),
    Spine1: P(970.9, 414.6),
    Neck1: P(979.4, 388.6),
    Head: P(983.5, 361.8),
    LeftArm: P(940, 398.6),
    LeftForeArm: P(909.4, 474.1),
    LeftHand: P(938.4, 521.7),
    RightArm: P(1011.9, 396),
    RightForeArm: P(1008.6, 480.6),
    RightHand: P(1033.4, 523.5),
    LeftUpLeg: P(943, 507.4),
    LeftLeg: P(987.7, 619),
    LeftFoot: P(946.5, 732),
    LeftToeBase: P(974.1, 740.7),
    RightUpLeg: P(979.9, 505.5),
    RightLeg: P(1009.1, 618.6),
    RightFoot: P(966.2, 730.2),
    RightToeBase: P(992.3, 741.7),
  };
  const jointNames = Object.keys(rest);

  function introPose(beat) {
    const blend = across(beat, 2.3, PHASE_BEATS);
    return Object.fromEntries(jointNames.map((name) => [name, lerp(rest[name], introEnd[name], blend)]));
  }

  function outroPose(beat) {
    const load = across(beat, 28.15, 28.52) * (1 - across(beat, 28.52, HEEL_BEAT));
    const rebound = across(beat, 28.58, HEEL_BEAT) * (1 - across(beat, HEEL_BEAT, 29.17));
    const frame = { ...rest };
    for (const name of jointNames) {
      if (name.endsWith('ToeBase') || name.endsWith('Foot')) continue;
      frame[name] = offset(frame[name], -5 * load, 9 * rebound);
    }
    for (const name of ['RightFoot', 'RightToeBase']) {
      frame[name] = offset(frame[name], 0, -18 * load);
    }
    frame.RightLeg = offset(frame.RightLeg, -2 * load, -9 * load);
    return frame;
  }

  const cubic = (a, b, c, d, u) =>
    lerp(lerp(lerp(a, b, u), lerp(b, c, u), u), lerp(lerp(b, c, u), lerp(c, d, u), u), u);
  function bezier(a, b, c, d, n = 27) {
    return Array.from({ length: n + 1 }, (_, i) => cubic(a, b, c, d, i / n));
  }
  function through(a, b, c, soft = .55) {
    const tangent = P((c.x - a.x) * soft * .26, (c.y - a.y) * soft * .26);
    const prefix = bezier(a, lerp(a, b, .60), offset(b, -tangent.x, -tangent.y), b, 14);
    const suffix = bezier(b, offset(b, tangent.x, tangent.y), lerp(b, c, .44), c, 14);
    return prefix.concat(suffix.slice(1));
  }

  function extremity(wrist, elbow, side, opened) {
    const angle = Math.atan2(wrist.y - elbow.y, wrist.x - elbow.x);
    const follow = angle + side * radians(mix(9, -6, opened));
    const dx = Math.cos(follow), dy = Math.sin(follow);
    const length = mix(15, 22, opened);
    const local = (x, y) => offset(wrist, x * dx - side * y * dy, x * dy + side * y * dx);
    const a = local(-2, -2.5), neck = local(length * .38, -4.8), nail = local(length, 0);
    const top = bezier(a, local(3, -3.0), local(length * .27, -5.1), neck, 8);
    const crown = bezier(neck, local(length * .83, -4.8), local(length, -4.6), nail, 10);
    const fingers = bezier(
      nail,
      local(length, 4.3),
      local(length * .69, 5.5),
      local(length * .57, 4.2),
      9,
    );
    const thumb = bezier(
      fingers.at(-1),
      local(length * .28, 3.5),
      local(length * .49, 8.2),
      local(length * .18, 5.2),
      9,
    );
    const heel = bezier(thumb.at(-1), local(1, 3.8), local(-2, 2.7), a, 7);
    return [...top, ...crown.slice(1), ...fingers.slice(1), ...thumb.slice(1), ...heel.slice(1)];
  }

  function outline(f) {
    const hip = f.Hips, neck = f.Neck1;
    const shoulders = [f.RightArm, f.LeftArm].sort((a, b) => a.x - b.x);
    const collar = lerp(shoulders[0], shoulders[1], .5);
    const pelvis = [f.RightUpLeg, f.LeftUpLeg];
    const pelvisCenter = lerp(pelvis[0], pelvis[1], .5);
    const head = offset(f.Head, .14 * (f.Head.x - neck.x), -17);
    const radius = 32;
    const headLine = Array.from({ length: 64 }, (_, i) => {
      const t = radians(108) + i * Math.PI * 2 / 63;
      return offset(head, Math.cos(t) * radius * .95, Math.sin(t) * radius);
    });
    const arms = ['Right', 'Left'].map((side) => {
      const shoulder = f[side + 'Arm'], elbow = f[side + 'ForeArm'], wrist = f[side + 'Hand'];
      const palm = extremity(wrist, elbow, side === 'Right' ? -1 : 1, .18);
      return { path: through(shoulder, elbow, wrist, .27), palm };
    });
    const legs = ['Right', 'Left'].map((side) => {
      const start = f[side + 'UpLeg'], knee = f[side + 'Leg'];
      const ankle = f[side + 'Foot'], toe = f[side + 'ToeBase'];
      const path = through(start, knee, ankle, .30);
      return path.concat(bezier(ankle, lerp(ankle, toe, .32), offset(toe, 0, 3.2), toe, 8).slice(1));
    });
    const [sh0, sh1] = shoulders;
    const leftFoot = f.LeftToeBase, rightFoot = f.RightToeBase;
    const restingFoot = leftFoot.y > rightFoot.y ? leftFoot : rightFoot;
    return {
      neck,
      restingFoot,
      supportOrder: restingFoot === rightFoot ? 6 : 7,
      parts: [
        [bezier(sh0, offset(collar, -18, -7), offset(collar, 18, -7), sh1), 9, .02],
        [arms[0].path, 8, .18, 'arm', .62],
        [arms[1].path, 8, .24, 'arm', 1],
        [
          bezier(collar, lerp(collar, hip, .45), lerp(f.Spine1, pelvisCenter, .74), pelvisCenter),
          10,
          .31,
        ],
        [headLine, 8, .65],
        [bezier(pelvis[0], lerp(pelvis[0], hip, .55), lerp(hip, pelvis[1], .45), pelvis[1]), 8, .80],
        [legs[0], 10, 1, 'leg', .73],
        [legs[1], 10, 1.12, 'leg', 1],
        [arms[0].palm, 0, .18, 'hand', .67],
        [arms[1].palm, 0, .24, 'hand', 1],
      ],
    };
  }

  function sample(points, index) {
    const p = clamp(index, 0, points.length - 1), i = Math.floor(p);
    return lerp(points[i], points[Math.min(points.length - 1, i + 1)], p - i);
  }

  // A filled, tapered strip preserves round motion and subtly varies the pressure of the stroke.
  function ink(ctx, points, width, inkColor, config = {}) {
    const { from = 0, to = 1, alpha = 1, taper = .28 } = config;
    if (to - from < .004 || alpha < .004) return;
    const count = Math.max(4, Math.ceil(points.length * (to - from)));
    const left = [], right = [];
    let first, last, firstRadius, lastRadius;
    const total = points.length - 1;
    for (let i = 0; i <= count; i++) {
      const u = mix(from, to, i / count);
      const center = sample(points, u * total);
      const prev = sample(points, u * total - .23), next = sample(points, u * total + .23);
      const dx = next.x - prev.x, dy = next.y - prev.y, m = Math.max(.001, norm(dx, dy));
      const shape = mix(1 - taper, 1, Math.sin(Math.PI * u) ** .72);
      const r = .5 * width * shape;
      left.push(offset(center, -dy / m * r, dx / m * r));
      right.push(offset(center, dy / m * r, -dx / m * r));
      if (!i) {
        first = center;
        firstRadius = r;
      }
      if (i === count) {
        last = center;
        lastRadius = r;
      }
    }
    ctx.globalAlpha = alpha;
    ctx.fillStyle = inkColor;
    ctx.beginPath();
    ctx.moveTo(left[0].x, left[0].y);
    for (const p of left) ctx.lineTo(p.x, p.y);
    for (let i = right.length - 1; i >= 0; i--) ctx.lineTo(right[i].x, right[i].y);
    ctx.closePath();
    ctx.fill();
    for (const [p, r] of [[first, firstRadius], [last, lastRadius]]) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, 2 * Math.PI);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  function palette(ctx, top, bottom, stops) {
    const g = ctx.createLinearGradient(top.x, top.y, bottom.x, bottom.y);
    for (const [p, color] of stops) g.addColorStop(p, color);
    return g;
  }
  function mist(ctx, p, sx, sy, amount, color) {
    if (amount < .004) return;
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.scale(sx, sy);
    const glow = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
    glow.addColorStop(0, `rgba(${color},${amount})`);
    glow.addColorStop(.50, `rgba(${color},${amount * .22})`);
    glow.addColorStop(1, `rgba(${color},0)`);
    ctx.fillStyle = glow;
    ctx.fillRect(-1, -1, 2, 2);
    ctx.restore();
  }
  function speck(ctx, p, radius, alpha, tint = '#fff3db') {
    ctx.globalAlpha = alpha;
    ctx.fillStyle = tint;
    ctx.beginPath();
    ctx.arc(p.x, p.y, radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  function openingLine(ctx, b, figure) {
    const u = across(b, 0, 1.84);
    const shoulder = figure.parts[0][0][0];
    const start = offset(shoulder, -177, -14);
    const curve = bezier(start, offset(start, 63, -67), offset(shoulder, -47, 37), shoulder, 40);
    const a = (.64 + .28 * out(b / .28)) * (1 - across(b, 1.04, 1.86));
    const from = out(b / 1.84) * .88;
    const to = Math.min(1, from + .045 + .28 * Math.sin(u * Math.PI));
    const color = palette(ctx, start, shoulder, [[0, '#cdc9c499'], [.69, '#f5eee0'], [1, '#ffeccd']]);
    ink(ctx, curve, 6.5, color, { from, to, taper: .81, alpha: a });
    const end = sample(curve, to * (curve.length - 1));
    mist(ctx, end, 22, 17, a * .19, '246,220,181');
    speck(ctx, end, 2.7, a * .92);
  }

  // Each contour retracts along its own path before the remaining spine gathers near the waist.
  const retreat = [
    [29.65, 30.57, .5], // shoulders
    [29.10, 30.03, 0],
    [29.22, 30.18, 0], // arms
    [30.08, 31.12, .62], // torso
    [29.44, 30.37, 0], // head
    [29.78, 30.56, .5], // hips
    [29.22, 30.22, 0],
    [29.10, 30.12, 0], // legs
  ];

  function drawPerson(ctx, b, figure) {
    if (b > 31.13) return;
    const pearl = palette(ctx, offset(figure.neck, 0, -107), P(960, ORIGIN.y + 5), [
      [0, '#fbf7ed'],
      [.42, '#f3eee2'],
      [.74, '#e3ded6'],
      [1, '#c8c6c4'],
    ]);
    for (const [order, [points, width, delay, kind, depth = 1]] of figure.parts.entries()) {
      const hand = kind === 'hand';
      const start = hand ? 1.30 + delay : order >= 5 ? 2 + (delay - .8) * .8 : .57 + delay;
      const end = hand ? 1.60 + delay : order >= 5 ? 2.9 + delay * .27 : 1.47 + delay;
      const progress = across(b, start, end);
      if (progress <= 0) continue;
      if (hand) {
        const arm = order === 8 ? 1 : 2;
        const [begin, finish] = retreat[arm];
        const fold = across(b, begin - .10, begin + .36);
        if (fold >= 1) continue;
        const armPath = figure.parts[arm][0];
        const wrist = armPath.at(-1);
        const tip = sample(armPath, (1 - across(b, begin, finish)) * (armPath.length - 1));
        const path = points.map((p) =>
          offset(tip, (p.x - wrist.x) * (1 - fold), (p.y - wrist.y) * (1 - fold))
        );
        ctx.globalAlpha = progress * depth;
        ctx.fillStyle = pearl;
        ctx.beginPath();
        ctx.moveTo(path[0].x, path[0].y);
        for (const p of path.slice(1)) ctx.lineTo(p.x, p.y);
        ctx.closePath();
        ctx.fill();
        ctx.globalAlpha = 1;
        continue;
      }
      const [begin, finish, pivot] = retreat[order];
      const back = across(b, begin, finish);
      if (back >= 1) continue;
      const from = pivot * back, to = Math.min(progress, mix(1, pivot, back));
      const core = width * mix(1, .40, back);
      ink(ctx, points, core + 6, '#fff0d9', { from, to, alpha: depth * .075, taper: .46 });
      ink(ctx, points, core, pearl, { from, to, alpha: depth, taper: order === 4 ? .095 : .36 });
    }
  }

  function evenPath(points) {
    const length = [0];
    for (let i = 1; i < points.length; i++) {
      length.push(length[i - 1] + norm(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y));
    }
    let j = 1;
    return Array.from({ length: 72 }, (_, i) => {
      const d = i * length.at(-1) / 71;
      while (j < points.length - 1 && length[j] < d) j++;
      return lerp(
        points[j - 1],
        points[j],
        (d - length[j - 1]) / Math.max(.001, length[j] - length[j - 1]),
      );
    });
  }

  function closingLine(ctx, b, figure) {
    const t = b - HEEL_BEAT;
    if (t < 0 || b > 31.5) return;
    const foot = offset(figure.restingFoot, 0, 2);
    const gold = '#efd19c';
    const press = across(b, 29.10, 29.92);
    const sweep = bezier(
      offset(foot, -138, -3),
      offset(foot, -84, 40 * (1 - press)),
      offset(foot, 40, 28 * (1 - press)),
      offset(foot, 106, -4),
      44,
    );
    const sweepEnd = out((t + .038) / .34);
    const strength = (.76 + .23 * across(t, 0, .16)) * (1 - across(b, 29.63, 30.02));
    ink(ctx, sweep, 4.4, gold, {
      from: .51 * press,
      to: Math.min(sweepEnd, 1 - .49 * press),
      alpha: strength,
      taper: .81,
    });

    if (b < 29.64) return;
    const spine = figure.parts[3][0];
    const pivot = retreat[3][2] * (spine.length - 1);
    const waist = sample(spine, pivot);
    const ankleToHip = figure.parts[figure.supportOrder][0].slice().reverse();
    const hipToWaist = spine.slice(Math.ceil(pivot)).reverse();
    const guide = evenPath([foot, ...ankleToHip, ...hipToWaist, waist]);
    const move = across(b, 29.64, 31.11);
    const disappear = 1 - across(b, 30.88, 31.24);
    const tail = clamp(move - .18 * (1 - across(b, 30.85, 31.13)));
    ink(ctx, guide, 3.6, gold, { from: tail, to: move, alpha: .89 * disappear, taper: .79 });
    const tip = sample(guide, move * (guide.length - 1));
    const gather = across(b, 30.88, 31.12);
    const after = 1 - across(b, 31.14, 31.49);
    mist(ctx, tip, 19 + 13 * gather, 19 + 13 * gather, .24 * after, '252,216,156');
    speck(ctx, tip, mix(2.1 + 2.0 * gather, .5, 1 - after), .95 * after, '#fff1d7');
  }

  // Each draw composites a single frame onto the caller's canvas.
  function draw(ctx, elapsed, isOutro, {
    x = ctx.canvas.width / 2,
    y = ctx.canvas.height * (ORIGIN.y / 1080),
    scale = Math.min(ctx.canvas.width / 640, ctx.canvas.height / 1080),
    duration = DURATION,
  } = {}) {
    if (elapsed < 0) return;
    const beat = PHASE_BEATS * clamp(elapsed / duration);
    ctx.save();
    try {
      ctx.translate(x - ORIGIN.x * scale, y - ORIGIN.y * scale);
      ctx.scale(scale, scale);
      if (isOutro) {
        const outroBeat = OUTRO_BEAT + beat;
        const figure = outline(outroPose(outroBeat));
        drawPerson(ctx, outroBeat, figure);
        closingLine(ctx, outroBeat, figure);
      } else {
        const figure = outline(introPose(beat));
        if (beat < 1.86) openingLine(ctx, beat, figure);
        drawPerson(ctx, beat, figure);
      }
    } finally {
      ctx.restore();
    }
  }

  return Object.freeze({
    duration: DURATION,
    drawIntro(ctx, elapsed, options) {
      draw(ctx, elapsed, false, options);
    },
    drawOutro(ctx, elapsed, options) {
      draw(ctx, elapsed, true, options);
    },
  });
})();
