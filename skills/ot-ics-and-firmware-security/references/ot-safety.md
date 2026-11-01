# OT Safety Rules

Purpose: the pre-test safety gate every OT/ICS activity must pass before
traffic is sent — process safety outranks every security objective in this
skill.

## Decision order

1. **Can this be done passively?** Passive capture, log analysis, and lab
   extraction of an already-obtained image answer most assessment questions
   with zero process risk. Choose passive unless a gap explicitly requires
   more.
2. **Can this be done on a test bed?** Firmware flashing, protocol fuzzing,
   CPU stop commands, logic writes, and denial-of-service belong on lab
   replicas or vendor-approved fixtures — never on running plant.
3. **Does production activity require change control?** If yes: named change
   window, responsible operator, rollback procedure, and stop signal are all
   recorded in writing *before* the first packet. Verbal approval does not
   pass the gate.

## Hard exclusions (never active-tested)

| Excluded | Reason |
|---|---|
| Safety instrumented systems (SIS), emergency stops, life-safety equipment | Physical safety; failure risks people, not just uptime |
| Fire and gas systems | Same — safety layer |
| Control actions that move actuators, valves, breakers, drives | Unexpected motion or state change can damage plant or release product |
| Denial-of-service / flood tests against production links | Loss of control traffic can cascade to loss of process control |
| Firmware flashing on production controllers | Brick risk; requires vendor procedure and physical presence |

## Method-by-activity matrix

| Activity | Allowed where | Preconditions |
|---|---|---|
| Passive monitoring / span capture | Production | Span port only; no traffic sent to devices |
| Asset discovery (passive) | Production | None beyond monitoring authorization |
| Native-protocol read queries (device inventory, tag reads) | Production | Approved read-only OIDs/function codes; rate-limited; not against SIS |
| Vulnerability scanning (agent/snmp/protocol probes) | Production, controlled | Change window; vendor-safe scan profile; live operator on console watching process values |
| Protocol conformance/fuzz testing | Lab only | Replica device or lab segment |
| Logic download/upload, firmware update | Lab only (production: vendor procedure) | Vendor-approved procedure, backup of running logic, restore tested |
| Injection of control commands (write coils/registers) | Lab only | — |
| DoS/flood, ARP spoofing, MITM on plant links | Lab only | — |

## Per-test safety checklist

- [ ] Change-control ticket approved; window, operator, and rollback recorded
- [ ] Stop signal agreed and audible to both the tester and the control-room operator (e.g., operator calls "stop", tester halts immediately)
- [ ] Live process values visible during the test (HMI/trend on a second screen)
- [ ] Running PLC/controller logic backed up and restore path verified before touching anything
- [ ] Test scoped to specific IPs/function codes — no broad scans, no "sweep and see"
- [ ] SIS and life-safety paths confirmed outside the test target set
- [ ] Rollback executed and process values confirmed normal at test end; evidence recorded

## When safety and security conflict

A finding that requires unsafe testing to confirm is reported as
**unconfirmed, with the proposed safe method** — not confirmed by taking the
risk. Compensating controls (conduit restriction, monitoring rule, virtual
patch) cover the exposure while a safe validation path is scheduled.
