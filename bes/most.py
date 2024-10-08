import sys
import os
import math
import subprocess
import numpy as np
import i2x.mpow_utilities as mpow
import i2x.bes_upgrades as bes

# some data from CIMHub/BES/mpow.py

from bes_cases import *

def write_local_solve_file (root, load_scale=1.0, quiet=False, softlims=False):
  fscript = 'solve_{:s}.m'.format(root)
  fsummary = '{:s}_summary.txt'.format(root)
  fp = open(fscript, 'w')
  print("""clear;""", file=fp)
  print("""define_constants;""", file=fp)
  print("""mpopt = mpoption('verbose', 0, 'out.all', 0);""", file=fp)
  print("""mpopt = mpoption(mpopt, 'most.dc_model', 1);""", file=fp)
  print("""mpopt = mpoption(mpopt, 'most.uc.run', 1);""", file=fp)
  print("""mpopt = mpoption(mpopt, 'most.solver', 'GLPK');""", file=fp)
  if quiet:
    print("""mpopt = mpoption(mpopt, 'glpk.opts.msglev', 0);""", file=fp)
  else:
    print("""mpopt = mpoption(mpopt, 'glpk.opts.msglev', 1);""", file=fp)
  print("""mpc = loadcase ('{:s}_case.m');""".format(root), file=fp)
  print("""mpc = scale_load({:.5f},mpc);""".format (load_scale), file=fp)
  if softlims:
    print ("""mpc.softlims.RATE_A = struct('hl_mod', 'remove', 'hl_val', 1.5);""", file=fp)
    print ("""for lim = {'VMIN', 'VMAX', 'ANGMIN', 'ANGMAX', 'PMIN', 'PMAX', 'QMIN', 'QMAX'}""", file=fp)
    print ("""    mpc.softlims.(lim{:}).hl_mod = 'none';""", file=fp)
    print ("""end""", file=fp)
    print ("""mpc = toggle_softlims (mpc, 'on');""", file=fp)
  print("""xgd = loadxgendata('{:s}_xgd.m', mpc);""".format(root), file=fp)
  print("""mdi = loadmd(mpc, [], xgd, []);""", file=fp)
  print("""mdo = most(mdi, mpopt);""", file=fp)
  print("""ms = most_summary(mdo);""", file=fp)
  print("""save('-text', '{:s}', 'ms');""".format(fsummary), file=fp)
  if not quiet:
    print("""total_time = mdo.results.SolveTime + mdo.results.SetupTime""", file=fp)
  fp.close()
  return fscript, fsummary

if __name__ == '__main__':
  case_id = 0
  if len(sys.argv) > 1:
    case_id = int(sys.argv[1])
  sys_name = CASES[case_id]['name']
  load_scale = CASES[case_id]['load_scale']
  min_kv = CASES[case_id]['min_kv_to_upgrade']
  softlims = CASES[case_id]['softlims']
  mva_upgrades = CASES[case_id]['mva_upgrades']

  d = mpow.read_matpower_casefile ('{:s}.m'.format (sys_name))
  # assign sensible ratings
  bes.set_estimated_branch_ratings (matpower_dictionary=d, min_kv = min_kv)

  # assign linear cost functions
  ng = len(d['gen'])
  gencost = []
  for i in range(ng):
    gencost.append (mpow.get_hca_gencosts(d['genfuel'][i]))
  d['gencost'] = np.array (gencost, dtype=float)
  # Write extra generator data (xgd), assuming all units have been on for 24 hours to start, 
  # so MOST can leave them on or switch them off without restriction
  unit_states = np.ones(len(d['gen'])) * 24.0
  mpow.write_xgd_function ('most_xgd', d['gen'], d['gencost'], d['genfuel'], unit_states)

  # manual edits for WECC 240-bus model
  if mva_upgrades is not None:
    for row in mva_upgrades:
      idx = row['branch_number'] - 1
      d['branch'][idx][mpow.RATE_A] = row['new_mva']
      d['branch'][idx][mpow.RATE_B] = row['new_mva']
      d['branch'][idx][mpow.RATE_C] = row['new_mva']
      print ('Upsizing branch MVA', idx+1, d['branch'][idx])

  # write the modified Matpower case with attributes customized for MOST
  mpow.write_matpower_casefile (d, 'most_case')

  # run the MOST case
  fscript, fsummary = write_local_solve_file ('most', load_scale=load_scale, softlims=softlims)
  mpow.run_matpower_and_wait (fscript, quiet=False)
  f, nb, ng, nl, ns, nt, nj_max, nc_max, psi, Pg, Pd, Rup, Rdn, SoC, Pf, u, lamP, muF = mpow.read_most_solution(fsummary)
  print ('MOST cost = {:.2f}'.format (f))



