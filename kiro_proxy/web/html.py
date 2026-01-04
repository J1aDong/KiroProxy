"""HTML 页面"""

HTML_PAGE = '''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kiro API</title>
<link rel="icon" type="image/svg+xml" href="/assets/icon.svg">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --bg: #fafafa; --card: #fff; --border: #e5e5e5; --text: #1a1a1a; --muted: #666; --accent: #000; --success: #22c55e; --error: #ef4444; --warn: #f59e0b; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #0a0a0a; --card: #141414; --border: #262626; --text: #fafafa; --muted: #a3a3a3; --accent: #fff; }
}
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }
h1 { font-size: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
h1 img { width: 28px; height: 28px; }
.status { font-size: 0.875rem; color: var(--muted); display: flex; align-items: center; gap: 1rem; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.ok { background: var(--success); }
.status-dot.err { background: var(--error); }
.tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.tab { padding: 0.5rem 1rem; border: 1px solid var(--border); background: var(--card); cursor: pointer; font-size: 0.875rem; transition: all 0.2s; border-radius: 6px; }
.tab.active { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.panel { display: none; }
.panel.active { display: block; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; }
.card h3 { font-size: 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.stat-item { text-align: center; padding: 1rem; background: var(--bg); border-radius: 6px; }
.stat-value { font-size: 1.5rem; font-weight: 600; }
.stat-label { font-size: 0.75rem; color: var(--muted); }
.chat-box { height: 350px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; margin-bottom: 1rem; background: var(--bg); }
.msg { margin-bottom: 1rem; }
.msg.user { text-align: right; }
.msg span { display: inline-block; max-width: 80%; padding: 0.75rem 1rem; border-radius: 12px; white-space: pre-wrap; word-break: break-word; }
.msg.user span { background: var(--accent); color: var(--bg); }
.msg.ai span { background: var(--card); border: 1px solid var(--border); }
.input-row { display: flex; gap: 0.5rem; }
.input-row input, .input-row select { flex: 1; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); font-size: 1rem; }
.input-row input:focus { outline: none; border-color: var(--accent); }
button { padding: 0.75rem 1.5rem; background: var(--accent); color: var(--bg); border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; font-weight: 500; transition: opacity 0.2s; }
button:hover { opacity: 0.8; }
button:disabled { opacity: 0.5; cursor: not-allowed; }
button.secondary { background: var(--card); color: var(--text); border: 1px solid var(--border); }
select { padding: 0.5rem; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); }
pre { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; overflow-x: auto; font-size: 0.8rem; }
code { font-family: "SF Mono", Monaco, monospace; }
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 500; color: var(--muted); }
.badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500; }
.badge.success { background: #dcfce7; color: #166534; }
.badge.error { background: #fee2e2; color: #991b1b; }
.badge.warn { background: #fef3c7; color: #92400e; }
@media (prefers-color-scheme: dark) {
  .badge.success { background: #14532d; color: #86efac; }
  .badge.error { background: #7f1d1d; color: #fca5a5; }
  .badge.warn { background: #78350f; color: #fde68a; }
}
.endpoint { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.method { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.method.get { background: #dcfce7; color: #166534; }
.method.post { background: #fef3c7; color: #92400e; }
@media (prefers-color-scheme: dark) {
  .method.get { background: #14532d; color: #86efac; }
  .method.post { background: #78350f; color: #fde68a; }
}
.copy-btn { padding: 0.25rem 0.5rem; font-size: 0.75rem; background: var(--card); border: 1px solid var(--border); color: var(--text); }
.footer { text-align: center; color: var(--muted); font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }
.log-row { font-size: 0.8rem; }
.log-row:hover { background: var(--bg); }
.account-row { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; border: 1px solid var(--border); border-radius: 6px; margin-bottom: 0.5rem; }
.account-info { display: flex; align-items: center; gap: 1rem; }
.account-actions { display: flex; gap: 0.5rem; }
.account-actions button { padding: 0.25rem 0.5rem; font-size: 0.75rem; }
.refresh-btn { padding: 0.25rem 0.5rem; font-size: 0.75rem; cursor: pointer; }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1><img src="/assets/icon.svg" alt="Kiro">Kiro API Proxy</h1>
    <div class="status">
      <span class="status-dot" id="statusDot"></span>
      <span id="statusText">检查中...</span>
      <span id="uptime"></span>
    </div>
  </header>
  
  <div class="tabs">
    <div class="tab active" data-tab="chat">对话</div>
    <div class="tab" data-tab="monitor">监控</div>
    <div class="tab" data-tab="accounts">账号</div>
    <div class="tab" data-tab="logs">日志</div>
    <div class="tab" data-tab="api">API</div>
    <div class="tab" data-tab="docs">文档</div>
  </div>
  
  <div class="panel active" id="chat">
    <div class="card">
      <div style="display:flex;gap:0.5rem;margin-bottom:1rem">
        <select id="model" style="flex:1"></select>
        <button class="secondary" onclick="clearChat()">清空</button>
      </div>
      <div class="chat-box" id="chatBox"></div>
      <div class="input-row">
        <input type="text" id="input" placeholder="输入消息..." onkeydown="if(event.key==='Enter')send()">
        <button onclick="send()" id="sendBtn">发送</button>
      </div>
    </div>
  </div>
  
  <div class="panel" id="monitor">
    <div class="card">
      <h3>服务状态 <button class="refresh-btn secondary" onclick="loadStats()">刷新</button></h3>
      <div class="stats-grid" id="statsGrid"></div>
    </div>
    <div class="card">
      <h3>速度测试</h3>
      <button onclick="runSpeedtest()" id="speedtestBtn">开始测试</button>
      <span id="speedtestResult" style="margin-left:1rem"></span>
    </div>
  </div>
  
  <div class="panel" id="accounts">
    <div class="card">
      <h3>账号管理</h3>
      <div style="display:flex;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap">
        <button class="secondary" onclick="scanTokens()">扫描 Token</button>
        <button class="secondary" onclick="showAddAccount()">手动添加</button>
        <button class="secondary" onclick="checkTokens()">检查有效期</button>
      </div>
      <div id="accountList"></div>
    </div>
    <div class="card" id="scanResults" style="display:none">
      <h3>扫描结果</h3>
      <div id="scanList"></div>
    </div>
    <div class="card">
      <h3>Kiro 登录说明</h3>
      <p style="color:var(--muted);font-size:0.875rem;margin-bottom:0.5rem">
        Kiro 使用 AWS Identity Center 认证，需要通过 Kiro IDE 登录：
      </p>
      <ol style="color:var(--muted);font-size:0.875rem;padding-left:1.5rem;margin-bottom:1rem">
        <li>打开 Kiro IDE</li>
        <li>点击登录，使用 Google/GitHub 账号</li>
        <li>登录成功后 token 自动保存</li>
        <li>点击上方"扫描 Token"添加账号</li>
      </ol>
    </div>
  </div>
  
  <div class="panel" id="logs">
    <div class="card">
      <h3>请求日志 <button class="refresh-btn secondary" onclick="loadLogs()">刷新</button></h3>
      <table>
        <thead><tr><th>时间</th><th>路径</th><th>模型</th><th>状态</th><th>耗时</th></tr></thead>
        <tbody id="logTable"></tbody>
      </table>
    </div>
  </div>
  
  <div class="panel" id="api">
    <div class="card">
      <h3>API 端点</h3>
      <p style="color:var(--muted);font-size:0.875rem;margin-bottom:1rem">支持 OpenAI、Anthropic、Gemini 三种协议</p>
      <h4 style="color:var(--muted);margin-bottom:0.5rem">OpenAI 协议 (Codex CLI)</h4>
      <div class="endpoint"><span class="method post">POST</span><code>/v1/chat/completions</code></div>
      <div class="endpoint"><span class="method get">GET</span><code>/v1/models</code></div>
      <h4 style="color:var(--muted);margin-top:1rem;margin-bottom:0.5rem">Anthropic 协议 (Claude Code CLI)</h4>
      <div class="endpoint"><span class="method post">POST</span><code>/v1/messages</code></div>
      <h4 style="color:var(--muted);margin-top:1rem;margin-bottom:0.5rem">Gemini 协议</h4>
      <div class="endpoint"><span class="method post">POST</span><code>/v1/models/{model}:generateContent</code></div>
      <h4 style="margin-top:1rem;color:var(--muted)">Base URL</h4>
      <pre><code id="baseUrl"></code></pre>
    </div>
    <div class="card">
      <h3>cURL 示例</h3>
      <pre><code>curl <span class="pyUrl"></span>/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -d '{"model": "claude-sonnet-4", "messages": [{"role": "user", "content": "Hello"}]}'</code></pre>
    </div>
  </div>
  
  <div class="panel" id="docs">
    <div class="card">
      <h3>模型对照表</h3>
      <table>
        <thead><tr><th>Kiro 模型</th><th>能力</th><th>Claude Code</th><th>Codex</th></tr></thead>
        <tbody>
          <tr><td><code>claude-sonnet-4</code></td><td>⭐⭐⭐ 推荐</td><td><code>claude-sonnet-4</code></td><td><code>gpt-4o</code></td></tr>
          <tr><td><code>claude-sonnet-4.5</code></td><td>⭐⭐⭐⭐ 更强</td><td><code>claude-sonnet-4.5</code></td><td><code>gpt-4o</code></td></tr>
          <tr><td><code>claude-haiku-4.5</code></td><td>⚡ 快速</td><td><code>claude-haiku-4.5</code></td><td><code>gpt-4o-mini</code></td></tr>
          <tr><td><code>claude-opus-4.5</code></td><td>⭐⭐⭐⭐⭐ 最强</td><td><code>claude-opus-4.5</code></td><td><code>o1</code></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  
  <div class="footer">Kiro API Proxy v1.1.0 - 多账号轮询 | 会话粘性 | 工具调用支持</div>
</div>

<script>
const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);

// Tabs
$$('.tab').forEach(t=>t.onclick=()=>{
  $$('.tab').forEach(x=>x.classList.remove('active'));
  $$('.panel').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  $('#'+t.dataset.tab).classList.add('active');
  if(t.dataset.tab==='monitor')loadStats();
  if(t.dataset.tab==='logs')loadLogs();
  if(t.dataset.tab==='accounts')loadAccounts();
});

// Status
async function checkStatus(){
  try{
    const r=await fetch('/api/status');
    const d=await r.json();
    $('#statusDot').className='status-dot '+(d.ok?'ok':'err');
    $('#statusText').textContent=d.ok?'已连接':'未连接';
    if(d.stats)$('#uptime').textContent='运行 '+formatUptime(d.stats.uptime_seconds);
  }catch(e){
    $('#statusDot').className='status-dot err';
    $('#statusText').textContent='连接失败';
  }
}
function formatUptime(s){
  if(s<60)return s+'秒';
  if(s<3600)return Math.floor(s/60)+'分钟';
  return Math.floor(s/3600)+'小时'+Math.floor((s%3600)/60)+'分钟';
}
checkStatus();
setInterval(checkStatus,30000);

// URLs
$('#baseUrl').textContent=location.origin;
$$('.pyUrl').forEach(e=>e.textContent=location.origin);

// Models
async function loadModels(){
  try{
    const r=await fetch('/v1/models');
    const d=await r.json();
    const select=$('#model');
    select.innerHTML='';
    (d.data||[]).forEach(m=>{
      const opt=document.createElement('option');
      opt.value=m.id;
      opt.textContent=m.name||m.id;
      if(m.id==='claude-sonnet-4')opt.selected=true;
      select.appendChild(opt);
    });
  }catch(e){console.error('加载模型失败:',e)}
}
loadModels();

// Chat
let messages=[];
function addMsg(role,text){
  const box=$('#chatBox');
  const div=document.createElement('div');
  div.className='msg '+(role==='user'?'user':'ai');
  div.innerHTML='<span>'+text.replace(/</g,'&lt;').replace(/\\n/g,'<br>')+'</span>';
  box.appendChild(div);
  box.scrollTop=box.scrollHeight;
}
function clearChat(){messages=[];$('#chatBox').innerHTML='';}
async function send(){
  const input=$('#input');
  const text=input.value.trim();
  if(!text)return;
  input.value='';
  addMsg('user',text);
  messages.push({role:'user',content:text});
  $('#sendBtn').disabled=true;
  $('#sendBtn').textContent='...';
  try{
    const res=await fetch('/v1/chat/completions',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:$('#model').value,messages})
    });
    const data=await res.json();
    if(data.choices&&data.choices[0]){
      const reply=data.choices[0].message.content;
      addMsg('ai',reply);
      messages.push({role:'assistant',content:reply});
    }else if(data.detail){
      addMsg('ai','错误: '+data.detail);
    }
  }catch(e){addMsg('ai','请求失败: '+e.message)}
  $('#sendBtn').disabled=false;
  $('#sendBtn').textContent='发送';
}

// Stats
async function loadStats(){
  try{
    const r=await fetch('/api/stats');
    const d=await r.json();
    $('#statsGrid').innerHTML=`
      <div class="stat-item"><div class="stat-value">${d.total_requests}</div><div class="stat-label">总请求</div></div>
      <div class="stat-item"><div class="stat-value">${d.total_errors}</div><div class="stat-label">错误数</div></div>
      <div class="stat-item"><div class="stat-value">${d.error_rate}</div><div class="stat-label">错误率</div></div>
      <div class="stat-item"><div class="stat-value">${d.accounts_available}/${d.accounts_total}</div><div class="stat-label">可用账号</div></div>
    `;
  }catch(e){console.error(e)}
}

// Speedtest
async function runSpeedtest(){
  $('#speedtestBtn').disabled=true;
  $('#speedtestResult').textContent='测试中...';
  try{
    const r=await fetch('/api/speedtest',{method:'POST'});
    const d=await r.json();
    $('#speedtestResult').textContent=d.ok?`延迟: ${d.latency_ms.toFixed(0)}ms`:'测试失败: '+d.error;
  }catch(e){$('#speedtestResult').textContent='测试失败'}
  $('#speedtestBtn').disabled=false;
}

// Logs
async function loadLogs(){
  try{
    const r=await fetch('/api/logs?limit=50');
    const d=await r.json();
    $('#logTable').innerHTML=(d.logs||[]).map(l=>`
      <tr class="log-row">
        <td>${new Date(l.timestamp*1000).toLocaleTimeString()}</td>
        <td>${l.path}</td>
        <td>${l.model||'-'}</td>
        <td><span class="badge ${l.status<400?'success':l.status<500?'warn':'error'}">${l.status}</span></td>
        <td>${l.duration_ms.toFixed(0)}ms</td>
      </tr>
    `).join('');
  }catch(e){console.error(e)}
}

// Accounts
async function loadAccounts(){
  try{
    const r=await fetch('/api/accounts');
    const d=await r.json();
    $('#accountList').innerHTML=(d.accounts||[]).map(a=>`
      <div class="account-row">
        <div class="account-info">
          <span class="badge ${a.available?'success':a.rate_limited?'warn':'error'}">${a.available?'可用':a.rate_limited?'限流':'禁用'}</span>
          <span>${a.name}</span>
          <span style="color:var(--muted);font-size:0.8rem">请求: ${a.request_count}</span>
        </div>
        <div class="account-actions">
          <button class="secondary" onclick="toggleAccount('${a.id}')">${a.enabled?'禁用':'启用'}</button>
          <button class="secondary" onclick="deleteAccount('${a.id}')" style="color:var(--error)">删除</button>
        </div>
      </div>
    `).join('')||'<p style="color:var(--muted)">暂无账号，请点击"扫描 Token"</p>';
  }catch(e){console.error(e)}
}
async function toggleAccount(id){
  await fetch('/api/accounts/'+id+'/toggle',{method:'POST'});
  loadAccounts();
}
async function deleteAccount(id){
  if(confirm('确定删除此账号?')){
    await fetch('/api/accounts/'+id,{method:'DELETE'});
    loadAccounts();
  }
}
function showAddAccount(){
  const path=prompt('输入 Token 文件路径:');
  if(path){
    const name=prompt('账号名称:','账号');
    fetch('/api/accounts',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name,token_path:path})
    }).then(r=>r.json()).then(d=>{
      if(d.ok)loadAccounts();
      else alert(d.detail||'添加失败');
    });
  }
}

// Token 扫描
async function scanTokens(){
  try{
    const r=await fetch('/api/token/scan');
    const d=await r.json();
    const panel=$('#scanResults');
    const list=$('#scanList');
    if(d.tokens&&d.tokens.length>0){
      panel.style.display='block';
      list.innerHTML=d.tokens.map(t=>`
        <div class="account-row">
          <div class="account-info">
            <span>${t.name}</span>
            <span style="color:var(--muted);font-size:0.75rem">${t.path}</span>
          </div>
          <button class="secondary" onclick="addFromScan('${t.path}','${t.name}')">添加</button>
        </div>
      `).join('');
    }else{
      alert('未找到 Token 文件');
    }
  }catch(e){alert('扫描失败: '+e.message)}
}
async function addFromScan(path,name){
  try{
    const r=await fetch('/api/token/add-from-scan',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({path,name})
    });
    const d=await r.json();
    if(d.ok){
      loadAccounts();
      alert('添加成功');
    }else{
      alert(d.detail||'添加失败');
    }
  }catch(e){alert('添加失败: '+e.message)}
}
async function checkTokens(){
  try{
    const r=await fetch('/api/token/refresh-check',{method:'POST'});
    const d=await r.json();
    let msg='Token 状态:\\n';
    (d.accounts||[]).forEach(a=>{
      const status=a.valid?'✅ 有效':'❌ 无效';
      const remaining=a.valid?` (剩余 ${Math.floor(a.remaining_seconds/3600)}小时)`:'';
      msg+=`${a.name}: ${status}${remaining}\\n`;
    });
    alert(msg);
  }catch(e){alert('检查失败: '+e.message)}
}
</script>
</body>
</html>'''
