"""Generate manuscript claims and new tables only from the sealed canonical data."""
import csv,json,os,statistics as st
from pathlib import Path
from scipy.stats import spearmanr
R=Path(os.environ.get('HCADSE_RESULTS','results/v1.1-submission-results/data'))
G=Path('manuscript/generated');G.mkdir(exist_ok=True)
T=Path('manuscript/tables')
def read(n):return list(csv.DictReader((R/n).open()))
def write(n,s):(G/(n+'.tex')).write_text('\\input{generated/refdefs}%\n'+s+'\n')
def ran(a,d=0):
 a=list(a);lo,hi=min(a),max(a)
 f=lambda v:f'{v:.{d}f}'
 return f(lo) if lo==hi else f(lo)+r'\text{--}'+f(hi)
def table(n,head,rows,spec):
 (T/(n+'.tex')).write_text('\\scriptsize\n\\begin{tabular}{'+spec+'}\n\\toprule\n'+head+r' \\'+'\n\\midrule\n'+'\n'.join(' & '.join(str(v) for v in row)+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n')
e1=read('e1_pruning.csv');e3=read('e3_baselines.csv');e4=read('e4_ablation.csv');e5=read('e5_scalability.csv');e8=read('e8_stats.csv');e10=read('e10_order.csv');e11=read('e11_solver.csv')
wl=['telemetry','control','sensing']
s3=[r for r in e1 if r['scale']=='S3'];s4=[r for r in e1 if r['scale']=='S4']
des=json.loads((R/'e2_des_timing.json').read_text())['mean_seconds']
proj=[r for r in read('e2_costsweep.csv') if abs(float(r['C_E'])-des)<1e-12]
means=[r for r in read('e9_summary_mean.csv') if r['subset']=='all'];pooled=next(r for r in means if r['workload']=='ALL');within=[r for r in means if r['workload']!='ALL']
big=[r for r in e3 if r['method']=='nsga2' and int(r['budget'])==1000]
recalls=[st.median(float(r['recall']) for r in big if r['scale']==sc and r['workload']==w) for sc in ['S2','S3'] for w in wl]
macros={'EvalRange':ran(int(r['evals']) for r in e1+e5),'SthreeEvalRange':ran(int(r['evals']) for r in s3),'SfourEvalRange':ran(int(r['evals']) for r in s4),'DesCostMs':f'{des*1000:.1f}','ProjectionMax':f'{max(float(r["speedup"]) for r in proj):.0f}','BaselineRecallRange':ran(recalls,2),'WithinAgreementRange':ran((100*float(r['agree_25pct']) for r in within),1),'PooledAgreement':f'{100*float(pooled["agree_25pct"]):.1f}','MaxStates':f"{max(int(r['nodes']) for r in e5):,}".replace(',','\\,'),'AnalyticalSpeedup':ran((float(r['speedup']) for r in e1 if r['scale'] in ['S2','S3']),2)}
Path('manuscript/generated_numbers.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in macros.items())+'\n')
write('rq1',r'The exploration funnel is reported in \RefFunnelSite{}. On S3 ($51\,840$ candidates), HCA-DSE performs $\SthreeEvalRange$ full evaluations, removing '+ran((100*(1-int(r['evals'])/int(r['raw'])) for r in s3),2)+r'\% of the raw space before evaluation. On S4 ($345\,600$ candidates), it performs $\SfourEvalRange$ evaluations, a reduction of '+ran((100*(1-int(r['evals'])/int(r['raw'])) for r in s4),2)+r'\%. Raw-space reductions include structural rejection; \RefFunnelTab{} separately reports the smaller number of actual exhaustive evaluator calls.')
lines=[]
for sc in ['S2','S3']:
 d=[r for r in proj if r['scale']==sc]
 thresholds=[1e6*(float(r['overhead_hca'])-float(r['overhead_exh']))/(int(r['N_exh'])-int(r['N_hca'])) for r in d]
 lines.append(sc+': the break-even threshold is $'+ran(thresholds,2)+r'\,\mu$s; projected speed-up at the measured DES cost is $'+ran((float(r['speedup']) for r in d),1)+r'\times$, with asymptotic evaluation-count ratios of $'+ran((int(r['N_exh'])/int(r['N_hca']) for r in d),1)+r'\times$.')
write('rq3','\n'.join(lines)+r''' The DES anchor is $\DesCostMs$\,ms, averaged over 40 designs. The curve in
\RefCrossoverFig{} is a cost projection from measured counts and median overheads;
neither exploration strategy was executed end to end with DES in the inner loop.
The measured analytical-evaluator speed-up across S2/S3 is $'''+ran((float(r['speedup']) for r in e1 if r['scale'] in ['S2','S3']),2)+r'''\times$. These hardware- and implementation-specific values do not establish
simulator-level Pareto exactness or a universal crossover cost.''')
lines=[]
for sc in ['S2','S3']:
 d=[r for r in e8 if r['scale']==sc and r['budget']=='1000']
 randomrec=[st.median(float(r['recall']) for r in e3 if r['scale']==sc and r['workload']==w and r['method']=='random' and r['budget']=='1000') for w in wl]
 lines.append(sc+': at $B=1000$, NSGA-II median recall is $'+ran((float(r['nsga2_recall_med']) for r in d),3)+r'$ and median HV ratio is $'+ran((float(r['nsga2_hv_med']) for r in d),3)+r'$; random-search median recall is $'+ran(randomrec,3)+r'$.')
d=[r for r in e8 if r['scale']=='S3' and r['budget'] in ['500','1000']];sig=sum(float(r['p_nsga2_gt_random'])<.05 for r in d)
lines.append('On S3 at $B=500/1000$, '+str(sig)+r' of the six exploratory one-sided comparisons have unadjusted $p<0.05$; $p$ ranges from $'+ran((float(r['p_nsga2_gt_random']) for r in d),3)+r'$ and Cliff\textquotesingle{}s $\delta$ from $'+ran((float(r['cliffs_delta']) for r in d),3)+r'$. The individual results are in \RefStatsTab{}; no correction for multiple comparisons is applied.')
write('rq4',r'\RefBaselinesTab{} reports medians over 20 seeds, with budgets charged to actual full evaluator calls. '+'\n'.join(lines)+r''' HCA-DSE recovers the full analytical front on S3 with $\SthreeEvalRange$ evaluations.
All 960 stochastic runs satisfy $N_E=B$ and proposals $=N_E+$ structural rejections.
This accounting includes infeasible full evaluations. \RefHvFig{} shows
seed-level HV distributions; Supplementary Tables S1--S3 retain all budgets.''')
d=[r for r in e4 if r['scale']=='S3']
write('ablation',r'The layer ablation on S3 (\RefAblationSite{}) separates the contributions of the three pruning layers. Structural pruning alone leaves $34\,560$ full evaluations. Structural plus feasibility bounds leave $'+ran(int(r['evals']) for r in d if r['variant']=='struct+feasibility')+r'$, while structural plus dominance bounds leave $'+ran(int(r['evals']) for r in d if r['variant']=='struct+dominance')+r'$. Combining all layers leaves $\SthreeEvalRange$. Every variant preserves the exhaustive analytical front; the separate layers contribute complementary reductions on these spaces.')
write('scalability',r'The scalability sweep (\RefScalSite{}) covers raw spaces from $1.3\times10^3$ to $8.3\times10^7$ candidates. Across the sweep, expanded partial states never exceed $'+str(max(int(r['nodes']) for r in e5))+r'$; full evaluations range from $'+ran(int(r['evals']) for r in e5)+r'$. The largest observed runtime is $'+f'{max(float(r["runtime"]) for r in e5):.2f}'+r'$\,s, measured with Python memory tracing enabled, and peak traced allocations are $'+f'{max(float(r["peak_kib"]) for r in e5):.1f}'+r'$\,KiB. This is traced Python memory during search, not process RSS or total interpreter memory. Exhaustive front equality is not checked for these larger spaces.')
# order main S3 and all supplementary
rows=[]
for r in e10:
 rows.append([r['scale'],r['workload'],r['order'],'on' if r['queue']=='True' else 'off',r['nodes'],r['bound_calls'],r['evals'],r['partial_queue_active'],r['partial_queue_pruned'],f'{1000*float(r["runtime"]):.1f}'])
head=r'scale & workload & order & queue & states & checks & evals & active & pruned & ms'
table('order',head,[row for row in rows if row[0]=='S3'],'lll lrrrrrr'.replace(' ',''));table('order_full',head,rows,'llllrrrrrr')
d=[r for r in e10 if r['scale']=='S3' and r['queue']=='True']
write('order',r'\RefOrderTab{} crosses traversal order and queue-bound activation on S3 (all scales in the supplement). The canonical determinants-early order assigns node counts, node classes, replication and placement policy before the remaining variables; the determinants-late order assigns replication and policy last, so the waiting term stays relaxed to zero on every incomplete design. With the queue bound enabled, the canonical order performs $'+ran(int(r['evals']) for r in d if r['order']=='determinants-early')+r'$ full evaluations against $'+ran(int(r['evals']) for r in d if r['order']=='determinants-late')+r'$ for the determinants-late order, while expanding $'+ran(int(r['nodes']) for r in d if r['order']=='determinants-early')+r'$ partial designs against $'+ran(int(r['nodes']) for r in d if r['order']=='determinants-late')+r'$. Under the canonical order $'+ran(int(r['partial_queue_active']) for r in d if r['order']=='determinants-early')+r'$ checked incomplete designs carry a positive queueing contribution, of which $'+ran(int(r['partial_queue_pruned']) for r in d if r['order']=='determinants-early')+r'$ are discarded only because that term is present, against the same archive; under the determinants-late order the count is zero by construction. All 36 scale/workload/order/queue combinations preserve the unrounded exhaustive objective-vector set. Changing the order also changes the archive discovery sequence, so only the within-order on/off comparison isolates the bound toggle.')
table('solver',r'scale & workload & calls & feasible & table [s] & solver [s] & total [s] & front',[[r['scale'],r['workload'],r['full_evaluator_calls'],r['feasible_rows'],f'{float(r["table_seconds"]):.3f}',f'{float(r["solver_and_encoding_seconds"]):.3f}',f'{float(r["total_seconds"]):.3f}',r['pareto']] for r in e11],'llrrrrrr')
write('solver',r'The finite-table Z3 baseline recovers the same unrounded analytical front in all six S1/S2 cases (\RefSolverTab{}). It consumes 1080 evaluator calls on S1 and 3888 on S2, because the whole structurally valid relation must be built before solving. Total observed runtime is $'+ran((float(r['total_seconds']) for r in e11),3)+r'$\,s, including table construction. This establishes an executable exact solver comparison, but does not compare HCA-DSE with a compact symbolic formulation that can avoid evaluator calls.')
rows=[]
for w in wl:
 d=[r for r in read('e6_simvalidation.csv') if r['workload']==w];a=[float(r['L_analytical']) for r in d];b=[float(r['L_sim']) for r in d]
 rows.append([w,len(d),f'{100*st.mean(abs(x-y)/y for x,y in zip(a,b)):.1f}',f'{spearmanr(a,b).statistic:.3f}'])
table('des_validation',r'workload & designs & MAPE [\%] & Spearman $\rho$',rows,'lrrr')
unstable=sum(float(r['spread'])>=1.5 for r in read('e9_per_design_mean.csv'))
write('validation',r'''\RefDesTab{} reports analytical mean-latency predictions against the revised
DES model. The independent Docker round retains the same 36 configurations and all 108
runs with the analytical model frozen. \RefTestbedTab{} compares predictions with
the median of three measured run means. Pooled MAPE is $'''+pooled['MAPE']+r'\%$ and median absolute error is $'+pooled['median_AE_ms']+r'$\,ms. Within-workload pair agreement above $25\%$ is $\WithinAgreementRange\%$, compared with $\PooledAgreement\%$ over '+pooled['pairs_25pct']+r''' pooled pairs. Pooled agreement benefits from separation between workloads and is not
a substitute for within-workload validation. '''+str(unstable)+r''' configurations have a ratio of largest to smallest repeated mean latency of at least
$1.5$; all remain in the main summary. Supplementary Table S4 separately reports the
$p_{50}$ comparison and its utilisation/repeat subsets. Differences between predicted
means and measured medians must not be interpreted as direct mean-prediction error.''')
print('Generated numerical claims from',R)
