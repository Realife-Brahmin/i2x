function wind = test_wind
  [PQ, PV, REF, NONE, BUS_I, BUS_TYPE, PD, QD, GS, BS, BUS_AREA, VM, ...
    VA, BASE_KV, ZONE, VMAX, VMIN, LAM_P, LAM_Q, MU_VMAX, MU_VMIN] = idx_bus;
  [F_BUS, T_BUS, BR_R, BR_X, BR_B, RATE_A, RATE_B, RATE_C, TAP, SHIFT, ...
    BR_STATUS, ANGMIN, ANGMAX, PF, QF, PT, QT, MU_SF, MU_ST, MU_ANGMIN, ...
    MU_ANGMAX] = idx_brch;
  [CT_LABEL, CT_PROB, CT_TABLE, CT_TBUS, CT_TGEN, CT_TBRCH, CT_TAREABUS, ...
    CT_TAREAGEN, CT_TAREABRCH, CT_ROW, CT_COL, CT_CHGTYPE, CT_REP, ...
    CT_REL, CT_ADD, CT_NEWVAL, CT_TLOAD, CT_TAREALOAD, CT_LOAD_ALL_PQ, ...
    CT_LOAD_FIX_PQ, CT_LOAD_DIS_PQ, CT_LOAD_ALL_P, CT_LOAD_FIX_P, ...
    CT_LOAD_DIS_P, CT_TGENCOST, CT_TAREAGENCOST, CT_MODCOST_F, ...
    CT_MODCOST_X] = idx_ct;
  [GEN_BUS, PG, QG, QMAX, QMIN, VG, MBASE, GEN_STATUS, PMAX, PMIN, ...
    MU_PMAX, MU_PMIN, MU_QMAX, MU_QMIN, PC1, PC2, QC1MIN, QC1MAX, ...
    QC2MIN, QC2MAX, RAMP_AGC, RAMP_10, RAMP_30, RAMP_Q, APF] = idx_gen;
  [PW_LINEAR, POLYNOMIAL, MODEL, STARTUP, SHUTDOWN, NCOST, COST] = idx_cost;
  wind = struct( ...
    'type', 'mpcData', ...
    'table', CT_TGEN, ...
    'rows', [14, 15, 16, 17, 18], ...
    'col', PMAX, ...
    'chgtype', CT_REP, ...
    'values', [] );
  wind.values(:, 1, 1) = [1674.8; 1664.43; 1674.8; 1674.8; 1278.53; 1172.22; 1030.8; 937.81; 924.83; 895.34; 946.03; 953.79; 1014.11; 1055.77; 1143.44; 1317.92; 1424.98; 1391.01; 1358.89; 1391.87; 1275.25; 1043.44; 1042.94; 975.47];
  wind.values(:, 1, 2) = [2242.2; 2242.2; 2242.2; 2223.79; 2242.2; 2242.2; 2193.55; 2242.2; 2242.2; 2242.2; 2242.2; 1765.57; 1880.19; 2242.2; 2242.2; 1687.95; 1108.75; 1091.61; 1293.16; 1110.01; 910.62; 790.35; 607.6; 711.92];
  wind.values(:, 1, 3) = [8730.3; 8730.3; 8730.3; 6389.67; 4941.07; 2293.53; 2220.67; 2203.6; 1960.51; 1820.82; 1428.23; 1110.22; 523.16; 344.57; 152.76; 349.97; 228.0; 1495.16; 399.89; 0.0; 203.55; 0.0; 552.72; 509.66];
  wind.values(:, 1, 4) = [99.8; 99.8; 99.8; 99.8; 99.8; 63.66; 28.56; 26.09; 40.58; 50.73; 48.8; 45.83; 39.24; 18.38; 5.74; 2.04; 4.46; 3.0; 2.01; 0.53; 4.16; 1.78; 6.44; 4.36];
  wind.values(:, 1, 5) = [3562.2; 3562.2; 3562.2; 3562.2; 3562.2; 2345.31; 2193.52; 2541.48; 2706.78; 3304.55; 3071.56; 3228.28; 3562.2; 2959.86; 2244.54; 1966.54; 1766.6; 996.79; 499.39; 456.53; 711.32; 967.02; 1039.02; 865.79];
end
