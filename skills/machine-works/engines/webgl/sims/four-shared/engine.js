// The single-cylinder OHV four-stroke itself, built from code in millimetres, look of a clean study model. A finned
// block around a glass cylinder liner with the charge inside it, an open-valve head (two valves in guides, the plug
// between them), coil springs, rockers on a shaft, pushrods down to lifters on a camshaft, the cam gear meshing the
// crank gear at 2:1, slider-crank piston, conrod, counterweighted crank, fanned flywheel. update(th, ops) poses
// everything from crank angle th (degrees after firing TDC).
//
// NUMBERS THAT MAKE IT TOUCH (mm; kinematics in kin.js):
//   Deck (crown at TDC) = S_TDC + comp height 22 = 131.5; head ceiling = deck + stroke/(cr-1) = 137.125.
//   Cam axis (42, 44.92): distance to the crank axis = sqrt(42^2 + 44.92^2) = 61.5 = pitch radii 20.75 + 40.75
//   (teeth 20 crank : 40 cam, module ~2 mm, 2:1). Pushrods at x = 42 (coaxial over the lifters/lobes), z = -19 IN, +19 EX.
//   Valve axes at (x = -12, z = -19 IN / +19 EX); stem tips at deck+26 closed; discs close flush at the ceiling,
//   so an open disc reaches 6.5 mm into the bore - near TDC overlap the lift is under 0.3 mm, so the crown clears.
//   Rocker shaft (15, deck+33.5, along z); each rocker levers 27 mm either side of its pivot, so the rotation
//   beta = lift/27 drops the valve pad by ~lift and raises the pushrod cup by ~lift (1:1, pads overlap 0.1-0.4 mm).
import * as THREE from 'three';
import {chargeOf, CLEAR_H, liftEx, liftIn, pistonS, pinXY, pressure, VALVE} from './kin.js';

const VG = {z: [-19, 19], disc: 14}; // the valves' geometry: axes 19 mm either side, 14 mm discs

const V3 = THREE.Vector3;
const D2R = Math.PI / 180;
const DECK = 109.5 + 22;
const CH_TOP = DECK + CLEAR_H;
const CAM = {x: 42, y: 44.92, r: 9, z: [-19, 19]};
const ROCK = {px: 15, py: DECK + 33.5, lever: 27};
const VX = -12; // valve axis, x
const LIFT = 6.5;

function gearGeo(teeth, rOut, rRoot, width, holeR = 0) {
  const sh = new THREE.Shape();
  for (let i = 0; i < teeth; i++) {
    const a0 = (i / teeth) * Math.PI * 2;
    const da = (Math.PI * 2) / teeth;
    const pts = [
      [rRoot, a0],
      [rRoot, a0 + da * 0.2],
      [rOut, a0 + da * 0.33],
      [rOut, a0 + da * 0.62],
      [rRoot, a0 + da * 0.75],
    ];
    pts.forEach(([r, a], k) => (i === 0 && k === 0 ? sh.moveTo(r * Math.cos(a), r * Math.sin(a)) : sh.lineTo(r * Math.cos(a), r * Math.sin(a))));
  }
  sh.closePath();
  if (holeR) {
    const h = new THREE.Path();
    h.absarc(0, 0, holeR, 0, Math.PI * 2, true);
    sh.holes.push(h);
  }
  const g = new THREE.ExtrudeGeometry(sh, {depth: width, bevelEnabled: true, bevelThickness: 1.2, bevelSize: 1.0, bevelSegments: 1, curveSegments: 4});
  g.translate(0, 0, -width / 2);
  g.computeVertexNormals();
  return g;
}
function helixGeo(r, wire, turns, len, seg = 160) {
  const pts = [];
  for (let i = 0; i <= seg; i++) {
    const u = i / seg;
    const a = u * turns * Math.PI * 2;
    pts.push(new V3(Math.cos(a) * r, u * len, Math.sin(a) * r));
  }
  return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), seg, wire, 8, false);
}
// a crank web: the boss, the pin boss and a counterweight sector opposite the pin, in the XY plane (pin at +y)
function webGeo(thick) {
  const sh = new THREE.Shape();
  const R = 33;
  sh.moveTo(-R * Math.sin(1.35), -R * Math.cos(1.35));
  sh.absarc(0, 0, R, -Math.PI / 2 - 1.35, -Math.PI / 2 + 1.35, false);
  sh.lineTo(14, 6);
  sh.lineTo(14, 35);
  sh.lineTo(-14, 35);
  sh.lineTo(-14, 6);
  sh.closePath();
  const g = new THREE.ExtrudeGeometry(sh, {depth: thick, bevelEnabled: true, bevelThickness: 2, bevelSize: 2, bevelSegments: 2, curveSegments: 20});
  g.translate(0, 0, -thick / 2);
  return g;
}
// a cooling fin: a partial annulus in the shape plane, the gap facing +x where the pushrods run down to the cam
function finGeo(rIn, rOut, a0 = -0.62, a1 = 0.62) {
  const sh = new THREE.Shape();
  sh.absarc(0, 0, rOut, a0, a1, false);
  sh.absarc(0, 0, rIn, a1, a0, true);
  sh.closePath();
  const g = new THREE.ExtrudeGeometry(sh, {depth: 1.6, bevelEnabled: true, bevelThickness: 0.5, bevelSize: 0.4, bevelSegments: 1, curveSegments: 40});
  g.translate(0, 0, -0.8);
  return g;
}
// a crankcase frame: the crank bore, the cam bore, arms up under the deck ring
function bulkheadGeo(thick) {
  const sh = new THREE.Shape();
  [[-54, -44], [54, -44], [54, 40], [44, 62], [-44, 62], [-54, 40]].forEach(([x, y], i) => (i ? sh.lineTo(x, y) : sh.moveTo(x, y)));
  sh.closePath();
  for (const [hx, hy, hr] of [[0, 0, 30], [CAM.x, CAM.y, 11]]) {
    const h = new THREE.Path();
    h.absarc(hx, hy, hr, 0, Math.PI * 2, true);
    sh.holes.push(h);
  }
  const g = new THREE.ExtrudeGeometry(sh, {depth: thick, bevelEnabled: true, bevelThickness: 2, bevelSize: 2, bevelSegments: 2, curveSegments: 16});
  g.translate(0, 0, -thick / 2);
  return g;
}

/** opts.caps: a colour; with a section on, the cut gets a flat face of it wherever it passes through a solid. */
export function buildEngine(opts = {}) {
  const root = new THREE.Group();
  const M = {
    black: new THREE.MeshPhysicalMaterial({color: '#141518', roughness: 0.3, metalness: 0.2, clearcoat: 0.7, clearcoatRoughness: 0.18}),
    blackMatte: new THREE.MeshPhysicalMaterial({color: '#1b1c1f', roughness: 0.55, metalness: 0.15, clearcoat: 0.25}),
    steel: new THREE.MeshStandardMaterial({color: '#cfd2d6', roughness: 0.22, metalness: 1}),
    alu: new THREE.MeshStandardMaterial({color: '#d9dbdf', roughness: 0.3, metalness: 0.85}),
    bronze: new THREE.MeshStandardMaterial({color: '#b98a55', roughness: 0.3, metalness: 0.9}),
    ceramic: new THREE.MeshPhysicalMaterial({color: '#f3f0ea', roughness: 0.35, metalness: 0, clearcoat: 0.6}),
    glass: new THREE.MeshPhysicalMaterial({color: '#ffffff', roughness: 0.05, metalness: 0, transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 1.6}),
    red: new THREE.MeshBasicMaterial({color: '#e3172c', transparent: true, opacity: 0.9, depthWrite: false}),
  };
  const add = (parent, geo, mat, cast = true) => {
    const m = new THREE.Mesh(geo, mat);
    m.castShadow = cast;
    m.receiveShadow = true;
    parent.add(m);
    return m;
  };
  const tubes = (pts, r, mat, seg = 24) => add(root, new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), seg, r, 10, false), mat);

  // ------------------------------------------------------------ block: two frames, side plates, sump, feet
  const block = new THREE.Group();
  root.add(block);
  const bh = bulkheadGeo(12);
  for (const z of [-56, 56]) add(block, bh, M.black).position.z = z;
  for (const x of [-58, 58]) add(block, new THREE.BoxGeometry(8, 86, 108), M.black).position.set(x, -3, 0);
  for (const x of [-42, 42]) for (const z of [-40, 40]) {
    const f = add(block, new THREE.BoxGeometry(16, 8, 20), M.black);
    f.position.set(x, -53, z);
  }
  const sump = add(block, new THREE.BoxGeometry(122, 8, 116), M.blackMatte);
  sump.position.y = -48;

  // ------------------------------------------------------------ cylinder: glass liner, fins, foot ring
  const cylG = new THREE.Group();
  root.add(cylG);
  const liner = add(cylG, new THREE.CylinderGeometry(37, 37, DECK - 40, 56, 1, true), M.glass, false);
  liner.position.y = (DECK + 40) / 2;
  liner.renderOrder = 3;
  for (let i = 0; i < 9; i++) {
    const fin = add(cylG, finGeo(38, 53), M.black);
    fin.rotation.x = -Math.PI / 2;
    fin.position.y = 52 + i * 9.4;
  }
  const foot = add(cylG, new THREE.TorusGeometry(38.5, 3, 10, 56), M.black);
  foot.rotation.x = Math.PI / 2;
  foot.position.y = 42;

  // ------------------------------------------------------------ head: slab, fins, guides, ports, plug, rocker shaft
  const head = new THREE.Group();
  root.add(head);
  const slab = add(head, new THREE.BoxGeometry(96, 14, 60), M.alu);
  slab.position.y = CH_TOP + 7;
  slab.userData.shell = 'head';
  const topFins = [];
  for (const z of [-16, 16]) {
    const fin = add(head, new THREE.BoxGeometry(100, 1.8, 4), M.alu);
    fin.position.set(0, CH_TOP + 16, z);
    topFins.push(fin);
  }
  const midFin = add(head, new THREE.BoxGeometry(3.4, 3.2, 62), M.alu);
  midFin.position.set(0, CH_TOP + 15.6, 0);
  topFins.push(midFin);
  for (const z of VG.z) {
    const gu = add(head, new THREE.CylinderGeometry(5, 5, 16, 16), M.bronze);
    gu.position.set(VX, DECK + 9, z);
  }
  // ports: the intake out the -x side to a carb flange, the exhaust out the +x side and down
  tubes([new V3(VX, CH_TOP + 9, -19), new V3(-40, CH_TOP + 12, -19), new V3(-62, 146, -19)], 11, M.black);
  const carb = add(head, new THREE.CylinderGeometry(13, 13, 8, 24), M.black);
  carb.rotation.z = Math.PI / 2;
  carb.position.set(-66, 146, -19);
  tubes([new V3(VX, CH_TOP + 9, 19), new V3(44, CH_TOP + 12, 19), new V3(66, 140, 19), new V3(72, 118, 19)], 12, M.black);
  for (const z of [-29, 29]) {
    const p = add(head, new THREE.BoxGeometry(7, 18, 7), M.black);
    p.position.set(ROCK.px, CH_TOP + 21, z);
  }
  const shaft = add(head, new THREE.CylinderGeometry(3.5, 3.5, 64, 16), M.steel);
  shaft.rotation.x = Math.PI / 2;
  shaft.position.set(ROCK.px, ROCK.py, 0);

  // spark plug: between the valves at z 0, leaning out toward -x from the +x side of the head
  const plug = new THREE.Group();
  plug.rotation.z = 0.61;
  plug.position.set(44, CH_TOP + 1, 0);
  head.add(plug);
  add(plug, new THREE.CylinderGeometry(6, 6, 22, 16), M.steel).position.y = 11;
  add(plug, new THREE.CylinderGeometry(5.5, 5.5, 20, 16), M.ceramic).position.y = 32;
  add(plug, new THREE.CylinderGeometry(2.2, 2.2, 8, 8), M.steel).position.y = 45;
  const plugHalo = new THREE.Mesh(new THREE.TorusGeometry(9, 2.2, 8, 32), M.red);
  plugHalo.rotation.x = Math.PI / 2;
  plugHalo.position.y = 24;
  plugHalo.renderOrder = 5;
  plug.add(plugHalo);
  plugHalo.visible = false;
  // the spark itself: a soft glow at the plug's spark end, sized by the burn's pressure glow
  const spark = new THREE.Mesh(
    new THREE.SphereGeometry(7, 16, 12),
    new THREE.MeshBasicMaterial({color: '#ffd9a0', transparent: true, opacity: 0.0, depthWrite: false, blending: THREE.AdditiveBlending}),
  );
  spark.position.set(40, 138, 0);
  spark.renderOrder = 4;
  root.add(spark);

  // valves: stem, disc, cap and retainer drop together with the lift
  const valves = ['in', 'ex'].map((kind, k) => {
    const z = VG.z[k];
    const g = new THREE.Group();
    g.position.set(VX, 0, z);
    head.add(g);
    add(g, new THREE.CylinderGeometry(2.8, 2.8, 26, 12), M.steel).position.y = DECK + 13;
    add(g, new THREE.CylinderGeometry(VG.disc, 7, 6, 28), M.steel).position.y = CH_TOP - 3;
    add(g, new THREE.CylinderGeometry(3.6, 3.6, 2.4, 12), M.steel).position.y = DECK + 26 - 1.2;
    add(g, new THREE.CylinderGeometry(8, 8, 3, 16), M.steel).position.y = DECK + 29.5;
    // the spring stays with the head: base on the guide boss, squeezed by the lift
    const spring = new THREE.Group();
    spring.position.set(VX, DECK + 10, z);
    head.add(spring);
    add(spring, helixGeo(10.5, 2.2, 8, 18), M.steel);
    // the accent halo, worn when this valve is working
    const halo = new THREE.Mesh(new THREE.TorusGeometry(13, 2.2, 8, 32), M.red);
    halo.rotation.x = Math.PI / 2;
    halo.position.set(VX, DECK + 40, z);
    halo.renderOrder = 5;
    head.add(halo);
    halo.visible = false;
    return {kind, z, g, spring, halo};
  });

  // rockers: a beam per valve about the shaft, 27 mm lever each way from the pivot
  const rockers = valves.map((v, k) => {
    const g = new THREE.Group();
    g.position.set(ROCK.px, ROCK.py, VG.z[k]);
    const beam = add(g, new THREE.BoxGeometry(36, 5, 8), M.black);
    beam.position.set(0, 0, k ? 2.5 : -2.5);
    beam.rotation.z = Math.atan2(8, 32);
    const tip = add(g, new THREE.CylinderGeometry(3.4, 3.4, 11, 12), M.steel);
    tip.rotation.x = Math.PI / 2;
    tip.position.set(-27, -4, 0);
    const cup = add(g, new THREE.CylinderGeometry(3.4, 3.4, 11, 12), M.steel);
    cup.rotation.x = Math.PI / 2;
    cup.position.set(27, 4, 0);
    return g;
  });

  // camshaft: shaft, two lobes (nose phased to its valve's mid-lift at half crank speed), the 40 T gear
  const camG = new THREE.Group();
  camG.position.set(CAM.x, CAM.y, 0);
  root.add(camG);
  add(camG, new THREE.CylinderGeometry(9, 9, 140, 20), M.steel).position.z = 12;
  add(camG, new THREE.TorusGeometry(11, 3, 8, 24), M.black).position.z = 82;
  const lobes = CAM.z.map((z, k) => {
    const peak = k ? (VALVE.ex[0] + VALVE.ex[1]) / 2 : (VALVE.in[0] + VALVE.in[1]) / 2;
    const lg = new THREE.Group();
    lg.position.z = z;
    const sh = new THREE.Shape();
    sh.absellipse(0, 4, 8.6, 12.6, 0, Math.PI * 2, false, 0);
    const geo = new THREE.ExtrudeGeometry(sh, {depth: 12, bevelEnabled: true, bevelSize: 1, bevelThickness: 1, bevelSegments: 1, curveSegments: 20});
    geo.translate(0, 0, -6);
    add(lg, geo, M.black);
    lg.rotation.z = (peak / 2) * D2R;
    camG.add(lg);
    return {lg, k};
  });
  const camGear = add(camG, gearGeo(40, 43.5, 38, 14, 12), M.black);
  camGear.position.z = 74;
  const camKey = add(camG, new THREE.BoxGeometry(5, 5, 3), M.red);
  camKey.position.set(38, 0, 74); // a mark on the cam gear: half a crank turn per revolution
  camKey.renderOrder = 5;

  // crank gear (20 T) on the crank stub, same plane
  const crankGear = add(root, gearGeo(20, 22.5, 19, 14, 5), M.black);
  crankGear.position.set(0, 0, 74);
  const crankKey = add(crankGear, new THREE.BoxGeometry(4, 4, 3), M.red);
  crankKey.position.set(0, 21, 6);
  crankKey.renderOrder = 5;

  // ------------------------------------------------------------ crank: webs, journals, pin, stubs; flywheel at the back
  const crank = new THREE.Group();
  root.add(crank);
  const webG = webGeo(14);
  const webs = [];
  for (const z of [-20, 20]) {
    const w = add(crank, webG, M.black);
    w.position.z = z;
    webs.push({w});
  }
  for (const z of [-38, 38]) {
    const j = add(crank, new THREE.CylinderGeometry(13, 13, 24, 24), M.steel);
    j.rotation.x = Math.PI / 2;
    j.position.z = z;
  }
  const pin = add(crank, new THREE.CylinderGeometry(10, 10, 24, 20), M.steel);
  pin.rotation.x = Math.PI / 2;
  add(crank, new THREE.CylinderGeometry(9, 9, 40, 16), M.steel).position.z = 69;
  add(crank, new THREE.CylinderGeometry(9, 9, 19, 16), M.steel).position.z = -58.5;
  const flywheel = new THREE.Group();
  root.add(flywheel);
  add(flywheel, new THREE.CylinderGeometry(52, 52, 14, 56), M.black).position.z = -75;
  add(flywheel, new THREE.TorusGeometry(52, 2, 8, 56), M.blackMatte).position.z = -75;
  // a starter cup and six bolts on the flywheel's front face, a motion cue at speed
  add(flywheel, new THREE.CylinderGeometry(20, 22, 6, 32), M.blackMatte).position.z = -66;
  add(flywheel, new THREE.CylinderGeometry(6, 6, 4, 20), M.steel).position.z = -63;
  for (let k = 0; k < 6; k++) {
    const b = add(flywheel, new THREE.CylinderGeometry(4, 4, 4, 12), M.steel);
    const a = (k / 6) * Math.PI * 2 + 0.26;
    b.rotation.x = Math.PI / 2;
    b.position.set(Math.cos(a) * 38, Math.sin(a) * 38, -67);
  }

  // ------------------------------------------------------------ piston, rod, charge, arrow, pushrods+lifters
  const piston = new THREE.Group();
  root.add(piston);
  const body = add(piston, new THREE.CylinderGeometry(33, 33, 45, 48), M.alu);
  body.position.y = -0.5;
  for (let k = 0; k < 2; k++) {
    const r = add(piston, new THREE.TorusGeometry(33, 1.4, 8, 48), M.blackMatte);
    r.rotation.x = Math.PI / 2;
    r.position.y = 12 - k * 6.5;
  }
  add(piston, new THREE.CylinderGeometry(11, 11, 38, 16), M.steel).rotation.z = Math.PI / 2;
  const rod = new THREE.Group();
  root.add(rod);
  const beam = add(rod, new THREE.BoxGeometry(14, 1, 10), M.black);
  const big = add(rod, new THREE.CylinderGeometry(17, 17, 16, 24), M.black);
  big.rotation.x = Math.PI / 2;
  const small = add(rod, new THREE.CylinderGeometry(11, 11, 14, 20), M.black);
  small.rotation.x = Math.PI / 2;

  const pushrods = CAM.z.map((z) => {
    const g = new THREE.Group();
    g.position.set(CAM.x, 0, z);
    root.add(g);
    add(g, new THREE.CylinderGeometry(4.6, 4.6, 9, 16), M.steel).position.y = CAM.y + CAM.r + 4.5;
    const pr = add(g, new THREE.CylinderGeometry(2.6, 2.6, 112, 12), M.steel);
    pr.position.y = 110.2;
    return g;
  });

  // the red arrow beside the liner, pointing the way the piston moves
  const arrow = new THREE.Group();
  arrow.add(new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 30, 12), M.red));
  arrow.children[0].position.y = -6;
  const tipA = new THREE.Mesh(new THREE.ConeGeometry(9, 20, 16), M.red);
  tipA.position.y = 15;
  arrow.add(tipA);
  arrow.position.set(74, 90, 0);
  arrow.renderOrder = 5;
  root.add(arrow);

  // the charge: a real column between the crown and the head ceiling (its volume is the true chamber volume)
  const CHARGE_COL = [new THREE.Color('#9fb6c8'), new THREE.Color('#4a4f57'), new THREE.Color('#ff7a1f'), new THREE.Color('#a9adb2')];
  const HOT = new THREE.Color('#fff3d0');
  const charge = new THREE.Mesh(
    new THREE.CylinderGeometry(33, 33, 1, 44).translate(0, 0.5, 0),
    new THREE.MeshBasicMaterial({color: '#9fb6c8', transparent: true, opacity: 0.35, depthWrite: false}),
  );
  charge.renderOrder = 2;
  root.add(charge);

  const tmp = new V3();
  // cutaway: 'glass' (clear liner), 'solid' (opaque liner), 'section' (everything ahead of a plane cut away)
  const CLIP = new THREE.Plane(new V3(0, 0, -1), 0);
  const Z_CUT = new V3(0, 0, -1);
  const GHOST = new Map(
    Object.values(M).map((m) => {
      const g = m.clone();
      g.transparent = true;
      g.depthWrite = false;
      return [m, g];
    }),
  );
  root.traverse((m) => m.isMesh && (m.userData.mat0 = m.material));
  const ghosted = new Set();
  let cap = null;
  const helpers = [];
  if (opts.caps) {
    const inc = THREE.IncrementWrapStencilOp;
    const dec = THREE.DecrementWrapStencilOp;
    const count = (side, op) =>
      new THREE.MeshBasicMaterial({side, colorWrite: false, depthWrite: false, depthTest: false, stencilWrite: true, stencilFunc: THREE.AlwaysStencilFunc, stencilFail: op, stencilZFail: op, stencilZPass: op, clippingPlanes: [CLIP]});
    helpers.push(count(THREE.BackSide, inc), count(THREE.FrontSide, dec));
    const solid = new Set([M.black, M.blackMatte, M.steel, M.alu, M.bronze, M.ceramic]);
    const parts = [];
    root.traverse((m) => m.isMesh && solid.has(m.material) && parts.push(m));
    for (const m of parts) for (const mat of helpers) m.add(new THREE.Mesh(m.geometry, mat));
    const rep = THREE.ReplaceStencilOp;
    cap = new THREE.Mesh(
      new THREE.PlaneGeometry(0.4, 0.4),
      new THREE.MeshStandardMaterial({color: opts.caps, roughness: 0.55, metalness: 0, side: THREE.DoubleSide, stencilWrite: true, stencilRef: 0, stencilFunc: THREE.NotEqualStencilFunc, stencilFail: rep, stencilZFail: rep, stencilZPass: rep}),
    );
    cap.renderOrder = 1.1;
    cap.onAfterRender = (r) => r.clearStencil();
    for (const mat of [...helpers, cap.material]) mat.visible = false;
  }
  const C0 = new V3(0, 0.15, 0);
  const placeCap = () => {
    if (!cap) return;
    cap.position.copy(C0).addScaledVector(CLIP.normal, -CLIP.distanceToPoint(C0));
    cap.quaternion.setFromUnitVectors(new V3(0, 0, 1), tmp.copy(CLIP.normal).negate());
    cap.scale.set(0.32, 0.4, 1);
  };
  const clipMats = () => [...Object.values(M), ...GHOST.values(), charge.material];
  let cutNow = 'glass';
  let glassOpacity = 0.16;
  const setCut = (mode, zWorld = 0) => {
    CLIP.normal.copy(Z_CUT);
    CLIP.constant = zWorld;
    placeCap();
    if (mode === cutNow) return;
    cutNow = mode;
    for (const m of clipMats()) {
      m.clippingPlanes = mode === 'section' ? [CLIP] : null;
      m.needsUpdate = true;
    }
    if (cap) for (const mat of [...helpers, cap.material]) mat.visible = mode === 'section';
    const solid = mode === 'solid';
    M.glass.color.set(solid ? '#2b2d31' : '#ffffff');
    M.glass.opacity = solid ? 0.94 : glassOpacity;
    M.glass.depthWrite = solid;
  };
  const setRefract = (on) => {
    glassOpacity = on ? 0.16 : 0.05;
    M.glass.envMapIntensity = on ? 1.6 : 0.3;
    if (cutNow !== 'solid') M.glass.opacity = glassOpacity;
  };

  /** ops: charge (0..1 visibility), arrows (0..1), solo (isolate the mechanism), accent (-1 none, 0 intake,
   *  1 exhaust, 2 spark: a red halo where the work is) */
  const update = (th, ops = {}) => {
    const chargeOn = ops.charge ?? 1;
    const arrowsOn = ops.arrows ?? 1;
    const soloOn = !!ops.solo;
    block.visible = !soloOn;
    slab.visible = !soloOn;
    for (const f of topFins) f.visible = !soloOn;

    const s = pistonS(th);
    piston.position.y = s;
    const [px, py] = pinXY(th);
    pin.position.set(px, py, 0);
    webs.forEach(({w}) => (w.rotation.z = -th * D2R));
    flywheel.rotation.z = -th * D2R;
    // the rod: crank pin to wrist pin
    tmp.set(0, s, 0).sub(new V3(px, py, 0));
    const len = tmp.length();
    rod.position.set(px / 2, (py + s) / 2, 0);
    rod.rotation.set(0, 0, Math.atan2(tmp.y, tmp.x) - Math.PI / 2);
    beam.scale.y = len - 28;
    big.position.y = -len / 2;
    small.position.y = len / 2;
    // the charge: crown to the head ceiling, colour by stroke, a white flash at the pressure peak
    const crown = s + 22;
    const ps = ((th % 720) + 720) % 720;
    charge.position.y = crown;
    charge.scale.y = Math.max(0.5, CH_TOP - crown);
    const key = chargeOf(th);
    charge.material.color.copy(CHARGE_COL[key]);
    const glow = key === 2 ? Math.min(1, pressure(th) / 42) : 0;
    charge.material.opacity = chargeOn * (key === 2 ? 0.48 + 0.4 * glow : key === 0 ? 0.52 : 0.58);
    charge.visible = chargeOn > 0.01;
    if (key === 2) charge.material.color.lerp(HOT, glow * 0.55);
    // the spark glow rides the first 50 degrees of every burn
    const gk = key === 2 && ps < 50 ? Math.max(0, 1 - Math.abs(ps - 12) / 38) : 0;
    spark.material.opacity = chargeOn * gk * (0.25 + 0.55 * glow);
    spark.material.color.copy(HOT);
    spark.scale.setScalar(0.5 + 1.3 * gk);
    spark.visible = gk > 0.01;
    // valves, springs, rockers, pushrods, cam at half speed
    const L = [liftIn(ps) * LIFT, liftEx(ps) * LIFT];
    valves.forEach((v, k) => {
      v.g.position.y = -L[k];
      v.spring.scale.y = (18 - L[k]) / 18;
      v.halo.visible = false;
    });
    plugHalo.visible = false;
    const acc = ops.accent ?? -1;
    if (acc === 0 || acc === 1) valves[acc].halo.visible = true;
    else if (acc === 2) plugHalo.visible = true;
    rockers.forEach((g, k) => (g.rotation.z = L[k] / ROCK.lever));
    pushrods.forEach((g, k) => (g.position.y = L[k]));
    camG.rotation.z = -th * 0.5 * D2R;
    crankGear.rotation.z = -th * D2R;
    // the arrow beside the bore: the way the piston is heading, strongest mid-stroke
    const vel = pistonS(th + 2) - s;
    arrow.rotation.z = vel > 0 ? 0 : Math.PI;
    arrow.scale.setScalar(Math.max(0.001, arrowsOn * Math.min(1, Math.abs(vel) / 1.4)));
    arrow.visible = arrowsOn * Math.abs(vel) > 0.05;
    placeCap();
  };
  return {root, update, M, setCut, setRefract, CLIP, cap, valves, plug, camG, camGear, crankGear, flywheel};
}