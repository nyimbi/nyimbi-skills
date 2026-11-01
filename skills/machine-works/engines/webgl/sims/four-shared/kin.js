// Single-cylinder OHV four-stroke kinematics (Honda GX160-class, air-cooled, horizontal crank). Engine space is
// millimetres: crank axis on z (front = +z), cylinder axis on y, bore axis at x = 0. One input, crank angle th in
// degrees after firing TDC, drives every pose and readout.
//
// REFERENCE (Honda GX160 published spec):
//   bore 68 mm, stroke 45 mm (published) -> displacement = pi/4 * 68^2 * 45
//   compression ratio 9.0 : 1 (published)
//   rod length: NOT published. rod = 87 mm is a PARAMETRIC choice (rod/stroke = 1.93, typical for small OHV
//   engines). It is chosen, not sourced: read it as geometry, not as a GX160 figure.
//   bore/stroke = 1.51 (under-square, correct for the family).
//
// CAM EVENT TIMING - typical, parametric (small OHV single, mild overlap):
//   IVO 10 deg BTDC, IVC 35 deg ABDC, EVO 40 deg BBDC, EVC 5 deg ATDC.
// Valves ride one camshaft at half crank speed through lifters and pushrods to rockers.

export const E = {bore: 68, r: 22.5, rod: 87, cr: 9.0, comp: 22, crankZ: 0};
export const STROKE = 2 * E.r;
// displacement from the formula, and the clearance volume it implies at 9.0:1
export const DISPL = (Math.PI / 4) * E.bore * E.bore * STROKE; // mm^3
export const CLEAR_H = STROKE / (E.cr - 1); // clearance height in mm, Vc = bore area * CLEAR_H at flat crown
const mod = (a, m) => ((a % m) + m) % m;

// the stroke: power 0-180, exhaust 180-360, intake 360-540, compression 540-720 (degrees after firing TDC)
export const STROKES = ['POWER', 'EXHAUST', 'INTAKE', 'COMPRESSION'];
export const strokeOf = (ps) => STROKES[Math.floor(mod(ps, 720) / 180)];

// valve lift 0..1 as a smooth bump between open and closed, in degrees after firing TDC
export const VALVE = {ex: [140, 365], in: [350, 575], lift: 6.5};
const bump = (ps, [a, b]) => {
  const x = mod(ps - a, 720) / (b - a);
  return x > 0 && x < 1 ? Math.sin(Math.PI * x) ** 2 : 0;
};
export const liftEx = (ps) => bump(ps, VALVE.ex);
export const liftIn = (ps) => bump(ps, VALVE.in);

// slider-crank: wrist-pin distance from the crank axis along +y
export const S_TDC = E.r + E.rod;
export const S_BDC = E.rod - E.r;
export const pistonS = (th) => {
  const a = (th * Math.PI) / 180;
  return E.r * Math.cos(a) + Math.sqrt(E.rod * E.rod - (E.r * Math.sin(a)) ** 2);
};
/** piston as a fraction of stroke from TDC (0 at TDC, 1 at BDC) */
export const pistonFrac = (th) => (S_TDC - pistonS(th)) / STROKE;
/** crank pin position in the crank's XY plane: at th=0 the pin is at +y (TDC) */
export const pinXY = (th) => {
  const a = (th * Math.PI) / 180;
  return [E.r * Math.sin(a), E.r * Math.cos(a)];
};

// chamber volume in units of the clearance volume (1 at TDC, cr at BDC)
export const volume = (th) => 1 + (E.cr - 1) * pistonFrac(th);

/** Chamber pressure in bar, adapted to one cylinder from the V8's model: a polytropic compression and expansion
 *  (gamma ~ 1.30), a fast burn peaking near 2x the compression peak around 14 deg ATDC, intake ~1 bar, exhaust
 *  ~1.05 bar with a blowdown blip right after EVO. */
export const pressure = (th) => {
  th = mod(th, 720);
  const V = volume(th);
  if (th >= 540) return Math.max(0.95, 0.95 * Math.pow(E.cr / V, 1.30));
  if (th >= 360) return 0.98;
  if (th >= 180) {
    const x = Math.max(0, Math.min(1, (th - 180) / 45));
    return 1.06 + 1.7 * (1 - x) * (1 - x);
  }
  // power: the flame front takes ~14 deg; the burn pressure rides the polytrope down after the peak
  const comp = 0.95 * Math.pow(E.cr / V, 1.30);
  const burn = 40.2 * Math.pow(1 / V, 1.28);
  const k = Math.min(1, th / 14);
  return Math.max(1.05, comp + (burn - comp) * (k * k * (3 - 2 * k)));
};
// compression peak check, printed at load alongside the displacement: 0.95 * 9^1.3 ~ 16.5 bar, burn peak ~2.1x
export const PEAK_COMP = 0.95 * Math.pow(E.cr, 1.30);
export const PEAK_BURN = 40.2 * Math.pow(1 / volume(14), 1.28);

/** the charge colour key: 0 intake, 1 compressed, 2 combustion (burning while the pressure is above ~4 bar),
 *  3 exhaust */
export const chargeOf = (th) => {
  th = mod(th, 720);
  if (th < 360) return pressure(th) > 4 ? 2 : 3;
  if (th < 540) return 0;
  return 1;
};