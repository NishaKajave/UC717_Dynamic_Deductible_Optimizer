from flask import Flask,render_template,request,jsonify,send_from_directory
from pathlib import Path
import pandas as pd,re
app=Flask(__name__); app.config['MAX_CONTENT_LENGTH']=10*1024*1024
BASE=Path(__file__).parent; DATA=BASE/'data'
C_REQ=['customer_id','customer_name','monthly_income','monthly_expenses','emergency_savings','current_annual_premium','expected_claims_per_year','average_claim_amount','risk_preference','insurance_type']
D_REQ=['insurance_type','deductible','premium_discount_pct']; NUM=C_REQ[2:8]
def norm(s): return re.sub('_+','_',re.sub('[^a-z0-9]+','_',str(s).strip().lower())).strip('_')
def read_file(f,kind):
 name=f.filename.lower()
 if name.endswith('.csv'): df=pd.read_csv(f,encoding='utf-8-sig')
 elif name.endswith('.xlsx'):
  book=pd.ExcelFile(f); wanted=['customers','customer_data'] if kind=='customer' else ['deductible_options','deductibles']; mp={norm(x):x for x in book.sheet_names}; sheet=next((mp[x] for x in wanted if x in mp),book.sheet_names[0]); df=pd.read_excel(book,sheet_name=sheet)
 else: raise ValueError('Only CSV and XLSX files are supported.')
 df.columns=[norm(x) for x in df.columns]; return df.dropna(how='all')
def customers(df):
 e=[]; miss=[x for x in C_REQ if x not in df.columns]
 if miss:return None,[f"Missing customer columns: {', '.join(miss)}"]
 d=df[C_REQ].copy(); d.customer_id=d.customer_id.astype(str).str.strip(); d.customer_name=d.customer_name.astype(str).str.strip()
 for c in NUM:
  d[c]=pd.to_numeric(d[c],errors='coerce')
  if d[c].isna().any():e.append(f'{c} has invalid or blank values.')
  if (d[c].dropna()<0).any():e.append(f'{c} cannot be negative.')
 if d.customer_id.duplicated().any():e.append('Customer IDs must be unique.')
 d.risk_preference=d.risk_preference.astype(str).str.strip().str.lower().map({'low':'Low','medium':'Medium','high':'High'})
 d.insurance_type=d.insurance_type.astype(str).str.strip().str.lower().map({'motor':'Motor','property':'Property','health':'Health'})
 if d.risk_preference.isna().any():e.append('Risk preference must be Low, Medium or High.')
 if d.insurance_type.isna().any():e.append('Insurance type must be Motor, Property or Health.')
 return d,e
def deductibles(df):
 e=[];miss=[x for x in D_REQ if x not in df.columns]
 if miss:return None,[f"Missing deductible columns: {', '.join(miss)}"]
 d=df.copy();d.insurance_type=d.insurance_type.astype(str).str.strip().str.lower().map({'motor':'Motor','property':'Property','health':'Health','all':'All'})
 for c in ['deductible','premium_discount_pct']:d[c]=pd.to_numeric(d[c],errors='coerce')
 if d[D_REQ].isna().any().any():e.append('Deductible dataset contains invalid or blank mandatory values.')
 if (d.deductible.dropna()<=0).any():e.append('Deductible must be greater than zero.')
 if ((d.premium_discount_pct.dropna()<0)|(d.premium_discount_pct.dropna()>100)).any():e.append('Discount must be between 0 and 100.')
 if 'active' in d:d=d[d.active.astype(str).str.lower().isin(['yes','true','1','active'])]
 return d,e
def analyze(c,ops):
 out=[];disp=max(c['monthly_income']-c['monthly_expenses'],0);rf={'Low':1.25,'Medium':1,'High':.8}[c['risk_preference']]
 for _,o in ops.iterrows():
  x=float(o.deductible);disc=float(o.premium_discount_pct);prem=c.current_annual_premium*(1-disc/100);save=c.current_annual_premium-prem;claim=c.expected_claims_per_year*min(x,c.average_claim_amount);annual=prem+claim
  aff=max(0,min(100,100-x/max(c.emergency_savings,1)*120-x/max(disp,1)*20));cost=max(0,100-annual/max(c.current_annual_premium+c.average_claim_amount,1)*45);score=max(0,min(100,.55*aff+.30*cost+15-(x/max(c.average_claim_amount,x,1)*30*rf+min(c.expected_claims_per_year,3)*7)))
  out.append({'insurance_type':o.insurance_type,'deductible':round(x,2),'premium_discount_pct':round(disc,2),'estimated_premium':round(prem,2),'premium_saving':round(save,2),'expected_claim_cost':round(claim,2),'expected_annual_cost':round(annual,2),'affordability_score':round(aff,1),'suitability_score':round(score,1),'review_note':'Review: no disposable income' if disp==0 else 'Review: deductible exceeds 25% of savings' if x>.25*c.emergency_savings else 'Suitable for prototype comparison'})
 return sorted(out,key=lambda z:(-z['suitability_score'],z['expected_annual_cost']))
@app.get('/')
def home():return render_template('index.html')
@app.get('/api/preloaded')
def preloaded():
 c,e=customers(pd.read_csv(DATA/'customers.csv',encoding='utf-8-sig'));d,e2=deductibles(pd.read_csv(DATA/'deductible_options.csv',encoding='utf-8-sig'));return jsonify({'customers':c.to_dict('records'),'deductibles':d.to_dict('records'),'errors':e+e2})
@app.post('/api/validate')
def validate():
 try:
  if 'customer_file' not in request.files:return jsonify({'ok':False,'errors':['Please upload a customer dataset.']}),400
  c,e=customers(read_file(request.files['customer_file'],'customer'))
  if 'deductible_file' in request.files and request.files['deductible_file'].filename:d,e2=deductibles(read_file(request.files['deductible_file'],'deductible'));source='Uploaded'
  else:d,e2=deductibles(pd.read_csv(DATA/'deductible_options.csv',encoding='utf-8-sig'));source='Preloaded fallback'
  if e+e2:return jsonify({'ok':False,'errors':e+e2}),400
  return jsonify({'ok':True,'customers':c.to_dict('records'),'deductibles':d.to_dict('records'),'deductible_source':source,'message':f'{len(c)} customers and {len(d)} active deductible options loaded.'})
 except Exception as ex:return jsonify({'ok':False,'errors':[str(ex)]}),400
@app.post('/api/analyze')
def api_analyze():
 p=request.get_json();c=pd.Series(p['customer']);d=pd.DataFrame(p['deductibles']);m=d[(d.insurance_type.str.lower()==str(c.insurance_type).lower())|(d.insurance_type.str.lower()=='all')]
 if m.empty:return jsonify({'ok':False,'errors':[f'No deductible options match {c.insurance_type}.']}),400
 return jsonify({'ok':True,'results':analyze(c,m)})
@app.get('/download/<path:name>')
def download(name):return send_from_directory(BASE/'download_templates',name,as_attachment=True)
if __name__=='__main__':app.run(debug=True,host='127.0.0.1',port=5000)
