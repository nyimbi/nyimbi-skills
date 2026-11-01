// OHV · Four-Stroke, the explorer film: the engine (engine.js) on the pale studio (stage.js) under the overlay
// (console.js). Beat plan, ~20 s: the closed engine at idle; the cutaway reveals the glass liner and the head section;
// the four strokes in slow motion, one beat each; a full cycle at speed with the indicator loop tracing; pull back to
// the closed engine as the rpm rises and holds. The crank angle is a pure function of t: the rpm profile in
// timeline.json, integrated at load (Euler, 1/240), with theta0 set so the slow-motion section starts on intake TDC.
import {runSim} from '../kit/runtime.js';
import TL from '../four-film/timeline.json';
import {createConsole, RPM_MAX} from './console.js';
import {strokeOf} from './kin.js';
import {createStage} from './stage.js';

export const DURATION = TL.duration;
export const SCRIPT = [
  {t: 0, cam: 'open'},
  {t: 3, cam: 'axis'},
  {t: 7.2, cam: 'mech'},
  {t: 11.4, cam: 'cycle'},
  {t: 15.8, cam: 'full'},
];
export const STROKES_AT = [7, 8, 9, 10]; // intake, compression, power, exhaust in seconds
export const DEFAULTS = {duration: DURATION, fps: 60, theme: 'light', hud: {enabled: false, title: 'ohv', subtitle: ''}, director: {enabled: false}, watermark: ''};
const D2R = Math.PI / 180;
const mm = (v) => v * 0.001;
const smoother = (x) => {
  const u = Math.min(1, Math.max(0, x));
  return u * u * u * (u * (u * 6 - 15) + 10);
};
const ss = (a, b, t) => smoother((t - a) / (b - a));
export const PLAY = 20; // playback divider: degrees/6 divided by this

// ------------------------------------------------------------ engine speed, integrated into a crank table at load
const KEYS = String(TL.rpm).split(' ').map((x) => x.split(':').map(Number)); // [[t, rpm], ...] as strings in the timeline: the sheet-walker only picks numbers
export const rpmAt = (t) => {
  for (let i = 1; i < KEYS.length; i++) {
    const [t0, v0] = KEYS[i - 1];
    const [t1, v1] = KEYS[i];
    if (t <= t1) return v0 + (v1 - v0) * smoother((t - t0) / (t1 - t0));
  }
  return KEYS[KEYS.length - 1][1];
};
const DT = 1 / 240;
const TT = [];
{
  let th = 0;
  for (let t = 0; t <= DURATION + 1; t += DT) {
    TT.push(th);
    th += ((rpmAt(t) / 60) * 360 * DT) / PLAY;
  }
}
// theta0 puts the slow-motion section's first frame (t = 7) exactly on intake TDC (360 after firing)
export const THETA0 = ((360 - TT[Math.round(7 / DT)] % 720) % 720 + 720) % 720;
export const thetaAt = (t) => {
  const u = Math.max(0, Math.min(TT.length - 2, t / DT));
  const i = Math.floor(u);
  return THETA0 + TT[i] + (TT[i + 1] - TT[i]) * (u - i);
};
// the intake-TDC crossings after t=7, for the console's cycle counter (and the score's whooshes)
export const INTAKE_TDC = [7, 11, 15, 19];

// ------------------------------------------------------------ views, each a function of u (seconds since it came on)
const TARG = {open: 0.06, axis: 0.1, mech: 0.1, cycle: 0.08, full: 0.07};
export const VIEW_FN = {
  open: (u) => ({tx: -0.01, ty: TARG.open, tz: 0, az: 214 + 16 * u, el: 16 + 7 * u, d: 1.26 - 0.18 * u, sx: -40, sy: 8}),
  axis: (u) => ({tx: 0.02, ty: TARG.axis + 0.02, tz: 0, az: 26 + 3 * u, el: 72 + 2 * u, d: 0.92 - 0.06 * u, sx: -10, sy: -6}),
  mech: (u) => ({tx: 0, ty: 0.09, tz: 0.01, az: 12 + 2 * u, el: 22 + 1.5 * u, d: 0.98, sx: 60, sy: 4}),
  cycle: (u) => ({tx: 0, ty: TARG.cycle, tz: 0, az: 28 + 2 * u, el: 24, d: 1.14 - 0.04 * u, sx: 0, sy: 6}),
  full: (u) => ({tx: -0.01, ty: TARG.full, tz: 0, az: 232 + 7 * u, el: 13 + 2 * u, d: 1.30, sx: -50, sy: 10}),
};
const VIEWS = SCRIPT.filter((e) => e.cam).map((e) => [e.t, e.cam]);
export const camAt = (t, list = VIEWS) => {
  let i = 0;
  while (i < list.length - 1 && list[i + 1][0] <= t) i++;
  const cur = VIEW_FN[list[i][1]](t - list[i][0]);
  if (i === 0) return cur;
  const k = ss(list[i][0], list[i][0] + 1.5, t);
  if (k >= 1) return cur;
  const prev = VIEW_FN[list[i - 1][1]](t - list[i - 1][0]);
  const o = {};
  for (const key in cur) o[key] = key === 'az' ? prev.az + ((((cur.az - prev.az + 540) % 360) - 180) * k) : prev[key] + (cur[key] - prev[key]) * k;
  const swing = Math.min(1, Math.abs((((cur.az - prev.az + 540) % 360) - 180)) / 90);
  o.d += Math.max(0, Math.max(prev.d, cur.d) + 0.5 * swing - o.d) * Math.sin(Math.PI * k);
  return o;
};
export const camName = (t) => VIEWS.filter(([t0]) => t0 <= t).pop()[1];

// the cutaway: the section's plane sweeps from ahead of the engine to the bore axis over beat 2
export const cutAt = (t) => {
  const cz = 0.26 * (1 - ss(3.2, 4.6, t));
  return {cut: t < 3 ? 'glass' : t < 15.4 ? 'section' : 'glass', z: (t < 3 ? 0 : cz) * 0.001};
};

// ------------------------------------------------------------ the operator's pointer
const REST = [[820, 470], [700, 500], [900, 480]];
export function makeCursor(ui) {
  const SP = ui.spots;
  const EV = [
    {t: 3.1, spot: SP.section, drag: 0},
    {t: 3.7, spot: SP.axis, drag: 0},
    {t: 7.3, spot: SP.mech, drag: 0},
    {t: 9.1, spot: ui.strokeSpot(2), drag: 0},
    {t: 11.5, spot: SP.cycle, drag: 0},
    {t: 16.05, spot: ui.speedKnob(600 / RPM_MAX), to: ui.speedKnob(2100 / RPM_MAX), drag: 1.6},
  ];
  const WP = [[0, 980, 560]];
  EV.forEach((e, i) => {
    WP.push([e.t - 0.16, ...e.spot]);
    if (e.drag) {
      for (let k = 0; k <= 10; k++) {
        const tt = e.t + (k / 10) * e.drag;
        WP.push([tt + 0.02, ...ui.speedKnob(rpmAt(tt) / RPM_MAX)]);
      }
      WP.push([e.t + e.drag + 0.3, ...e.to]);
    } else WP.push([e.t + 0.24, ...e.spot]);
    WP.push([e.t + e.drag + 1.4, ...REST[i % REST.length]]);
  });
  WP.sort((a, b) => a[0] - b[0]);
  return (t) => {
    let i = 0;
    while (i < WP.length - 2 && t > WP[i + 1][0]) i++;
    const [t0, x0, y0] = WP[i];
    const [t1, x1, y1] = WP[i + 1];
    const lin = t1 - t0 < 0.2;
    const k = lin ? Math.min(1, Math.max(0, (t - t0) / (t1 - t0))) : ss(t0, t1, t);
    const len = Math.hypot(x1 - x0, y1 - y0);
    const bow = lin ? 0 : Math.sin(Math.PI * k) * Math.min(24, len * 0.07);
    let press = false;
    let ring = 0;
    let rx = 0;
    let ry = 0;
    for (const e of EV) {
      if (t >= e.t - 0.07 && t < e.t + Math.max(0.09, e.drag + 0.1)) press = true;
      if (t >= e.t && t < e.t + 0.55) {
        ring = 1 - (t - e.t) / 0.55;
        [rx, ry] = e.spot;
      }
    }
    return {x: x0 + (x1 - x0) * k + (len ? (-(y1 - y0) / len) * bow : 0), y: y0 + (y1 - y0) * k + (len ? ((x1 - x0) / len) * bow : 0), press, ring, ringX: rx, ringY: ry};
  };
}

// ------------------------------------------------------------ the overlay's data for a frame
export function makeConsoleFrame(ui, st) {
  const P = (x, y, z) => st.project(mm(x), mm(y), mm(z));
  return (t, {th, cam, rpm, cursor, since, live, cut}) => {
    const vis = ss(1.1, 1.8, since) * (live && !live.overlays.callouts ? 0 : 1);
    const callouts = [];
    const camXys = P(74, 88, 82); // the cam gear
    const pushXys = P(42, 128, -19); // the intake pushrod
    const fwXys = P(-70, -40, -80); // the flywheel rim
    const plugXys = P(30, 150, 0); // the spark plug
    const heroish = cam === 'open' || cam === 'full';
    if (heroish) {
      callouts.push(
        {name: 'Cam gear', sub: '40 T · HALF CRANK SPEED', at: camXys, label: [992, 268], w: 128, o: vis},
        {name: 'Flywheel', sub: 'FAN COOLS THE CYLINDER', at: fwXys, label: [318, 648], w: 128, o: vis},
        {name: 'Spark plug', sub: 'FIRES EVERY 720°', at: plugXys, label: [1094, 176], w: 120, o: vis},
      );
    }
    if (cam === 'mech' || cam === 'axis') {
      callouts.push(
        {name: 'Pushrod', sub: 'LIFTS THE ROCKER', at: pushXys, label: [1108, 470], w: 122, o: vis},
        {name: 'Rocker', sub: '27 MM LEVER, 1 : 1', at: P(15, 165, 0), label: [1088, 240], w: 128, o: vis},
      );
    }
    // leaders from the panels into the engine: the rev counter to the crank, the indicator panel to the bore
    const lead = live && !live.overlays.callouts ? 0 : 1;
    callouts.push({name: '', sub: '', at: P(0, 65, 40), label: [282, 152], w: 0, o: lead});
    callouts.push({name: '', sub: '', at: P(0, 120, 0), label: [1318 - 0.01, 501], w: 0, o: 0.9 * lead * (live && !live.overlays.charts ? 0 : 1)});
    ui.update({
      rpm,
      rpmK: rpm / RPM_MAX,
      playText: live ? live.playText : '1 / 20 SPEED',
      playK: live ? live.playK : 0.33,
      paused: live ? live.paused : false,
      theta: th,
      psi: ((th % 720) + 720) % 720,
      stroke: strokeOf(th),
      cam,
      cut: live ? live.cut : (cut ?? 'glass'),
      overlays: live ? live.overlays : {callouts: 1, charge: 1, arrows: 1, isolate: 0, refract: 1, charts: 1},
      callouts,
      cursor,
    });
  };
}

export function makeFilm() {
  return async ({canvas, capture}) => {
    const st = createStage({canvas, look: {engine: {caps: '#c9ccd0'}}});
    const resize = () => st.resize(1600, 900, capture ? devicePixelRatio || 1 : Math.min(devicePixelRatio || 1, 2));
    resize();
    const ui = createConsole(document.getElementById('app'));
    const cursorAt = makeCursor(ui);
    const frame = makeConsoleFrame(ui, st);
    window.OHV = st;
    return {
      resize,
      render(t) {
        const th = thetaAt(t);
        const cam = camName(t);
        const c = camAt(t);
        const t0 = VIEWS.filter(([a]) => a <= t).pop()[0];
        const {cut, z} = cutAt(t);
        st.setCut(cut, z);
        // the accent: the valve or plug doing the work through the slow strokes
        let accent = -1;
        if (t >= STROKES_AT[0] && t < STROKES_AT[0] + 4) {
          const s = Math.floor(t - STROKES_AT[0]);
          accent = [0, -1, 2, 1][s];
        }
        st.frame(th, {...c, az: c.az * D2R, el: c.el * D2R}, {solo: false, accent});
        frame(t, {th, cam, rpm: rpmAt(t), cursor: cursorAt(t), since: t - t0, cut});
        return {};
      },
    };
  };
}

export const run = () => runSim(DEFAULTS, makeFilm());