'use strict';
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {conhecido:'Conhecido',desconhecido:'Desconhecido',ausente:'Não informado',nao_aplicavel:'Não aplicável',nao_verificado:'Não verificado',nao_verificada:'Não verificada',aplicavel:'Aplicável',igual:'Igual ao alvo',abaixo:'Abaixo do alvo',acima:'Acima do alvo',sem_dado:'Sem dado para comparar',nao_comparado:'Sem alvo definido',preferida:'Entre as preferidas',nao_preferida:'Fora das preferidas',permitido:'Permitida',proibido:'Proibida',condicional:'Condicional',restrito:'Restrita',nativa:'Nativa',transferivel:'Transferível'};
const state = {user:null,csrf:null,all:[],options:{},rules:[],collection:[],profiles:[],page:'catalogo',offset:0,results:[],coverage:null};
const content = $('#content'), dialog = $('#dialog'), dialogBody = $('#dialog-body');
let viewVersion = 0;
function feedback(message, error=false) { const e=$('#feedback'); e.textContent=message;e.className=error?'error':'';e.hidden=false; }
function modalError(message) { let e=$('.dialog-error',dialog);if(!e){e=document.createElement('div');e.className='dialog-error';e.setAttribute('role','alert');dialogBody.append(e);}e.textContent=message;e.scrollIntoView({block:'nearest'}); }
async function api(path, options={}) {
  const headers={...(options.headers||{})};
  if(options.body !== undefined){ headers['Content-Type']='application/json'; }
  if(options.method && options.method!=='GET'){
    if(!state.csrf) state.csrf=(await api('/csrf')).csrf_token;
    headers['X-CSRF-Token']=state.csrf;
  }
  const response=await fetch('/api'+path,{...options,headers,credentials:'same-origin',body:options.body===undefined?undefined:JSON.stringify(options.body)});
  const data=await response.json();
  if(!response.ok){ const error=new Error(data.erro||`Falha na consulta (${response.status}).`);error.status=response.status;throw error; }
  if(data.csrf_token)state.csrf=data.csrf_token;
  return data;
}
function source(url,date) { try { const u=new URL(url);if(!['http:','https:'].includes(u.protocol))return '';return `<p class="source">Fonte: <a href="${esc(u.href)}" target="_blank" rel="noopener noreferrer">${esc(u.hostname)}</a>${date?' · '+esc(date):''}</p>`;}catch{return '<p class="source">Fonte ainda não verificada.</p>';} }
function tag(text,unknown=false){return `<span class="tag${unknown?' unknown':''}">${esc(text)}</span>`;}
function heading(kicker,title,description,action=''){return `<div class="page-head"><div><span class="eyebrow">${esc(kicker)}</span><h1>${title}</h1><p class="lead">${esc(description)}</p></div>${action}</div>`;}
function empty(title,message,action=''){return `<div class="empty"><div class="empty-symbol" aria-hidden="true">◈</div><h2>${esc(title)}</h2><p>${esc(message)}</p>${action}</div>`;}
function showDialog(html){dialogBody.innerHTML=html;dialog.showModal();}
$('#close-dialog').onclick=()=>dialog.close();
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
function account(){ $('#account').textContent=state.user?state.user.nome_usuario+' ↗':'Entrar ↗'; }
$('#account').onclick=()=>{if(!state.user)auth();else{showDialog(`<h2 id="dialog-title">Seu espaço</h2><p>${esc(state.user.nome_usuario)}</p><p class="help">${esc(state.user.email)}</p><div class="toolbar"><button id="logout" class="danger">Sair da conta</button></div>`);$('#logout').onclick=async()=>{try{await api('/auth/logout',{method:'POST',body:{}});state.user=null;state.csrf=null;state.collection=[];state.profiles=[];account();dialog.close();await render();}catch(e){modalError(e.message);}};}};
function auth(register=false){
  showDialog(`<h2 id="dialog-title">${register?'Crie seu espaço.':'Bom ter você por aqui.'}</h2><p class="help">Sua coleção e seus perfis são privados.</p><div class="auth-tabs"><button id="login-tab" class="${!register?'active':''}">Entrar</button><button id="register-tab" class="${register?'active':''}">Criar conta</button></div><form id="auth-form"><div class="field-grid">${register?'<label class="wide">Nome de usuário<input name="nome_usuario" autocomplete="username" required minlength="3"></label>':''}<label class="wide">E-mail<input name="email" type="email" autocomplete="email" required></label><label class="wide">Senha<input name="senha" type="password" autocomplete="${register?'new-password':'current-password'}" required minlength="8"></label></div><div class="toolbar"><button class="primary" type="submit">${register?'Criar conta':'Entrar no Pokelizer'} →</button></div></form>`);
  $('#login-tab').onclick=()=>{dialog.close();auth(false);};$('#register-tab').onclick=()=>{dialog.close();auth(true);};
  $('#auth-form').onsubmit=async e=>{e.preventDefault();const b=$('button[type=submit]',e.target);b.disabled=true;try{const data=await api('/auth/'+(register?'cadastro':'login'),{method:'POST',body:Object.fromEntries(new FormData(e.target))});state.user=data.usuario;account();dialog.close();feedback('Seu espaço está aberto.');await render();}catch(err){modalError(err.message);}finally{b.disabled=false;}};
}
async function render(){
  const version=++viewVersion;state.page=(location.hash.slice(1)||'catalogo');
  if(!['catalogo','colecao','perfis','analise','regulamentos'].includes(state.page))state.page='catalogo';
  $$('#feedback').forEach(e=>e.hidden=true);$$('nav a').forEach(a=>a.classList.toggle('active',a.dataset.page===state.page));
  $('#breadcrumb').textContent={catalogo:'CATÁLOGO',colecao:'MINHA COLEÇÃO',perfis:'PERFIS',analise:'COMPARAR',regulamentos:'REGULAMENTOS'}[state.page];
  content.innerHTML='<p class="help">Consultando o arquivo…</p>';
  try{
    if(['colecao','perfis','analise'].includes(state.page)&&!state.user){content.innerHTML=heading('SEU ESPAÇO','Um lugar para <em>os seus.</em>','Entre para cuidar da coleção, criar perfis e comparar seus exemplares.')+empty('Sua coleção começa aqui.','Crie uma conta ou entre para acessar seus dados.', '<button id="open-auth" class="primary">Entrar ou criar conta →</button>');$('#open-auth').onclick=()=>auth();return;}
    if(state.page==='catalogo'){catalog();return;}
    if(state.page==='regulamentos'){regulations();return;}
    const [collection,profiles]=await Promise.all([api('/colecao'),api('/perfis')]);if(version!==viewVersion)return;
    state.collection=collection.itens;state.profiles=profiles.itens;
    if(state.page==='colecao')collectionView();else if(state.page==='perfis')profilesView();else comparisonView();
  }catch(e){if(version===viewVersion){content.innerHTML=empty('Não foi possível carregar.', 'Confira a conexão e tente novamente.');feedback(e.message,true);}}
}
function catalog(){
  const c=state.coverage?.contagens_banco||{};
  content.innerHTML=heading('01 / ARQUIVO GLOBAL','Conheça <em>cada forma.</em>','Uma espécie, muitas possibilidades. Explore identidades e consulte o que se sabe em cada jogo.','<div class="archive-stamp">ARQUIVO VIVO<strong>PKL</strong>EST. 2026</div>')+
  `<div class="catalog-summary"><div class="summary-stat"><strong>${c.ESPECIE??'—'}</strong><span>espécies</span></div><div class="summary-stat"><strong>${c.FORMA??'—'}</strong><span>formas</span></div><div class="summary-stat"><strong>${c.JOGO??'—'}</strong><span>jogos catalogados</span></div><span class="summary-note">● IDENTIDADES GLOBAIS<br>Disponibilidade e regras são verificadas por jogo.</span></div>`+
  `<form id="filters" class="filters" aria-label="Filtrar catálogo"><input name="busca" type="search" aria-label="Buscar por nome, número ou código" placeholder="Nome, número ou código de forma…"><select name="geracao" aria-label="Geração"><option value="">Geração / todas</option>${Array.from({length:Math.max(9,...(state.options.jogos||[]).map(j=>j.geracao||0))},(_,i)=>`<option value="${i+1}">Geração ${i+1}</option>`).join('')}</select><select name="tipo" aria-label="Tipo"><option value="">Tipo / todos</option>${(state.options.tipos||[]).map(t=>`<option value="${t.id_tipo}">${esc(t.nome_tipo)}</option>`).join('')}</select><select name="jogo" aria-label="Jogo"><option value="">Jogo / todos</option>${(state.options.jogos||[]).map(j=>`<option value="${j.id_jogo}">${esc(j.nome)}</option>`).join('')}</select><button type="submit">Buscar ↗</button></form><div id="catalog-results"></div>`;
  state.results=state.all;state.offset=0;catalogResults();
  $('#filters').onsubmit=async e=>{e.preventDefault();const params=new URLSearchParams();for(const [k,v] of new FormData(e.target)){if(v)params.set(k,v);}const b=$('button',e.target);b.disabled=true;try{state.results=(await api('/pokemon?'+params.toString())).itens;state.offset=0;catalogResults();}catch(err){feedback(err.message,true);}finally{b.disabled=false;}};
}
function catalogResults(){
  const results=$('#catalog-results');if(!results)return;
  const page=state.results.slice(state.offset,state.offset+24);
  results.innerHTML=`<div class="results-head"><b>${state.results.length} FORMAS NO ARQUIVO</b><span>IDENTIDADE GLOBAL / FICHAS POR JOGO</span></div>`+(page.length?`<div class="catalog-grid">${page.map(p=>`<article class="pokemon-card"><div class="card-art"><span class="card-number">Nº ${esc(String(p.numero_nacional).padStart(4,'0'))}</span><span class="catalog-letter" aria-hidden="true">${esc(p.nome_pt?.slice(0,1))}</span><span class="card-category">REGISTRO DE FORMA</span></div><div class="card-body"><h2>${esc(p.nome_pt)}</h2><p class="form-code">${esc(p.codigo_forma||p.nome_forma||'Forma ainda não catalogada')}</p><div class="card-foot">${tag(p.fichas.length?p.fichas.length+' ficha(s) de jogo':'Sem ficha de jogo',!p.fichas.length)}<button data-form="${p.id_forma||''}" ${!p.id_forma?'disabled':''}>Explorar ↗</button></div></div></article>`).join('')}</div><div class="pagination"><button id="prev" ${state.offset===0?'disabled':''}>← Anterior</button><span>${Math.floor(state.offset/24)+1} / ${Math.ceil(state.results.length/24)}</span><button id="next" ${state.offset+24>=state.results.length?'disabled':''}>Próxima →</button></div>`:empty('Nenhuma forma encontrada.','Tente outro nome, número ou código. Filtros por jogo e tipo exigem uma ficha contextual conhecida.'));
  $$('[data-form]',results).forEach(b=>b.onclick=()=>detail(Number(b.dataset.form)));
  for(const [id,step] of [['prev',-24],['next',24]]){const b=$('#'+id);if(b)b.onclick=()=>{state.offset+=step;catalogResults();$('#filters').scrollIntoView({block:'start'});};}
}
async function detail(id){try{
  const p=await api('/formas/'+id);
  showDialog(`<span class="eyebrow">Nº ${p.especie.numero_nacional} / FORMA GLOBAL</span><h2 id="dialog-title">${esc(p.especie.nome_pt)}</h2><p class="form-code">${esc(p.codigo_forma)}</p>${tag(labels[p.estado_forma]||'Estado não verificado',p.estado_forma==='nao_verificado')}${source(p.fonte_url,p.data_verificacao)}<p>${esc(p.descricao||'A identidade global permanece no catálogo mesmo sem dados de jogo confirmados.')}</p><h3>Fichas por jogo</h3>${p.fichas.length?p.fichas.map(f=>`<div class="panel"><h2>${esc(f.nome_jogo)}</h2>${tag(labels[f.status_presenca]||'Presença não verificada',f.status_presenca==='nao_verificada')}<p class="help">${f.tipos.length?esc(f.tipos.join(' / ')):'Tipagem ainda não verificada.'}</p>${source(f.fonte_url,f.data_verificacao)}<button data-register="${f.id_dados_forma}" ${f.pode_ser_registrada==='nao'||f.status_presenca==='ausente'?'disabled':''}>Registrar exemplar →</button></div>`).join(''):empty('Ainda sem contexto verificado.','Esta forma está no arquivo global. Disponibilidade, atributos e regras por jogo ainda precisam de fontes específicas.')}`);
  $$('[data-register]',dialog).forEach(b=>b.onclick=()=>{const sheet=Number(b.dataset.register);dialog.close();state.user?editor('collection',null,sheet):auth();});
}catch(e){feedback(e.message,true);}}
function collectionView(){
 content.innerHTML=heading('02 / SUA COLEÇÃO','Cada exemplar, <em>uma história.</em>','Organize o contexto atual, a origem e os valores conhecidos de cada indivíduo.','<button id="new-specimen" class="primary">+ Registrar exemplar</button>')+(state.collection.length?`<div class="results-head"><b>${state.collection.length} EXEMPLARES</b><span>COLEÇÃO PRIVADA</span></div><div class="list">${state.collection.map((p,i)=>`<article class="list-card"><span class="list-index">${String(i+1).padStart(2,'0')}</span><div><h2>${esc(p.apelido||p.nome_pt)}</h2><div class="meta">${esc(p.nome_pt)} · ${esc(p.nome_jogo_atual)} · Nível ${p.nivel??'não informado'}</div><p class="help">${p.valores.length} valor(es) registrado(s) · ${esc(p.nome_natureza||'Natureza não informada')}</p></div><div class="actions"><button data-edit="${p.id_pokemon_colecao}">Consultar / editar</button><button class="danger" data-delete="${p.id_pokemon_colecao}">Excluir</button></div></article>`).join('')}</div>`:empty('Sua próxima descoberta mora aqui.','Registre exemplares de formas com ficha de jogo e acompanhe seus dados. Valores desconhecidos podem continuar desconhecidos.'));
 $('#new-specimen').onclick=()=>editor('collection');$$('[data-edit]').forEach(b=>b.onclick=()=>editor('collection',state.collection.find(p=>p.id_pokemon_colecao===Number(b.dataset.edit))));$$('[data-delete]').forEach(b=>b.onclick=()=>remove('colecao',Number(b.dataset.delete)));
}
function profilesView(){
 content.innerHTML=heading('03 / PERFIS DE ANÁLISE','Defina <em>o seu objetivo.</em>','Crie alvos explícitos por contexto. Um alvo menor pode ser uma escolha intencional.','<button id="new-profile" class="primary">+ Criar perfil</button>')+(state.profiles.length?`<div class="list">${state.profiles.map(p=>`<article class="list-card"><span class="list-index">◎</span><div><h2>${esc(p.nome_perfil)}</h2><div class="meta">${p.tipo_perfil==='personalizado'?'Personalizado · privado':'Referência competitiva · somente leitura'} · ${p.valores.length} alvo(s)</div><p class="help">${esc(p.descricao||'Sem descrição adicional.')}</p>${p.fonte_url?source(p.fonte_url,p.data_verificacao):''}</div><div class="actions">${p.tipo_perfil==='personalizado'?`<button data-profile="${p.id_perfil}">Consultar / editar</button><button class="danger" data-delete-profile="${p.id_perfil}">Excluir</button>`:''}</div></article>`).join('')}</div>`:empty('Uma referência para cada intenção.','Crie um perfil para a mesma forma, jogo e versão de mecânica do exemplar que deseja comparar.'));
 $('#new-profile').onclick=()=>editor('profile');$$('[data-profile]').forEach(b=>b.onclick=()=>editor('profile',state.profiles.find(p=>p.id_perfil===Number(b.dataset.profile))));$$('[data-delete-profile]').forEach(b=>b.onclick=()=>remove('perfis',Number(b.dataset.deleteProfile)));
}
function remove(resource,id){showDialog(`<h2 id="dialog-title">Excluir ${resource==='colecao'?'este exemplar':'este perfil'}?</h2><p>Os valores relacionados também serão removidos.</p><div class="toolbar"><button id="cancel-delete">Voltar</button><button id="confirm-delete" class="danger">Confirmar exclusão</button></div>`);$('#cancel-delete').onclick=()=>dialog.close();$('#confirm-delete').onclick=async()=>{try{await api(`/${resource}/${id}`,{method:'DELETE',body:{}});dialog.close();await render();feedback('Registro excluído.');}catch(e){modalError(e.message);}};}
const option=(value,label,selected=false)=>`<option value="${esc(value)}" ${selected?'selected':''}>${esc(label)}</option>`;
const selectOptions=(items,key,label,selected)=>option('','Não informado',selected==null)+items.map(item=>option(item[key],label(item),item[key]===selected)).join('');
const sheets=()=>state.all.flatMap(p=>p.fichas.map(f=>({...f,label:p.nome_pt+' · '+p.codigo_forma+' / '+f.nome_jogo})));
async function editor(type,existing=null,initialSheet=null){
 const isProfile=type==='profile',allSheets=sheets();
 if(!allSheets.length){showDialog(`<h2 id="dialog-title">Um contexto antes do registro.</h2><p>O catálogo global está disponível, mas ainda não há fichas por jogo carregadas neste banco. A inclusão depende dessas fichas e de regras verificadas.</p><p class="hint">A carga global não confirma disponibilidade por jogo. Consulte a cobertura e as fontes do projeto.</p>`);return;}
 const sheetId=existing?.[isProfile?'id_dados_forma':'id_dados_forma_atual']||initialSheet||allSheets[0].id_dados_forma;
 showDialog(`<h2 id="dialog-title">${existing?'Consultar / editar':isProfile?'Novo perfil':'Novo exemplar'}</h2><p class="help">${isProfile?'Seus alvos, no contexto certo.':'Origem e contexto atual são informações distintas.'}</p><form id="editor"><div class="field-grid"><label class="wide">${isProfile?'Nome do perfil':'Apelido (opcional)'}<input name="${isProfile?'nome_perfil':'apelido'}" value="${esc(existing?.[isProfile?'nome_perfil':'apelido']||'')}" maxlength="${isProfile?120:40}" ${isProfile?'required':''}></label><label class="wide">Forma e jogo atual<select id="sheet" required>${allSheets.map(f=>option(f.id_dados_forma,f.label,f.id_dados_forma===sheetId)).join('')}</select></label><label class="wide">Versão da mecânica<select id="mechanic"></select></label></div><p id="context-warning" class="hint" hidden>Contexto alterado. Revise os campos e os valores abaixo; salvar substituirá os dados contextuais pela seleção exibida.</p><div id="context-fields"></div>${isProfile?`<label>Descrição<textarea name="descricao" maxlength="2000">${esc(existing?.descricao||'')}</textarea></label>`:`<h3>Origem e observações</h3><div class="field-grid"><label>Jogo de origem<select id="origin-game">${selectOptions(state.options.jogos,'id_jogo',j=>j.nome,existing?.id_jogo_origem)}</select></label><label>Forma de origem<select id="origin-sheet"></select></label><label class="wide">Método de obtenção<select name="id_metodo_obtencao">${selectOptions(state.options.metodos,'id_metodo',m=>m.nome,existing?.id_metodo_obtencao)}</select></label><label class="wide">Observações<textarea name="observacao" maxlength="500">${esc(existing?.observacao||'')}</textarea></label></div>`}<div class="toolbar"><button type="button" id="cancel-editor">Voltar</button><button type="submit" id="save-editor" class="primary">Salvar ${isProfile?'perfil':'exemplar'} →</button></div></form>`);
 $('#cancel-editor').onclick=()=>dialog.close();
 let activeMechanic=null,sheet=null,loading=0,sheetLoading=0;
 const updateValues=(mechanic,keep)=>{
  const field=isProfile?'valor_alvo':'valor',saved=keep?(existing?.valores||[]):[];
  return mechanic.sistemas.map(s=>`<section class="value-system"><h3>${esc(s.nome)} ${tag(labels[s.aplicabilidade]||s.aplicabilidade,s.aplicabilidade==='nao_verificado')}</h3><p class="help">${s.valor_minimo!=null&&s.valor_maximo_atributo!=null?'Por atributo: '+s.valor_minimo+' a '+s.valor_maximo_atributo+'. ':''}${s.limite_total_status==='confirmado'?'Limite combinado: '+s.valor_maximo_total+'.':s.limite_total_status==='nao_verificado'?'Limite combinado não verificado.':'Sem limite combinado aplicável.'}</p>${source(s.fonte_url,s.data_verificacao)}${s.atributos.map(a=>{
   const v=saved.find(v=>v.id_mecanica_sistema_atributo===s.id_mecanica_sistema_atributo&&v.id_atributo===a.id_atributo);
   const known=s.aplicabilidade==='aplicavel'&&a.aplicabilidade==='aplicavel'&&s.valor_minimo!=null&&s.valor_maximo_atributo!=null&&s.limite_total_status!=='nao_verificado';
   const na=s.aplicabilidade==='nao_aplicavel'||a.aplicabilidade==='nao_aplicavel';
   return `<div class="attribute" data-system="${s.id_mecanica_sistema_atributo}" data-attribute="${a.id_atributo}"><div class="value-row"><label for="state-${s.id_mecanica_sistema_atributo}-${a.id_atributo}">${esc(a.nome)}</label><select class="value-state" id="state-${s.id_mecanica_sistema_atributo}-${a.id_atributo}" aria-label="Estado de ${esc(a.nome)}">${option('','Não informado',!v)}${known?option('conhecido','Conhecido',v?.estado==='conhecido'):''}${option('desconhecido','Desconhecido',v?.estado==='desconhecido')}${na?option('nao_aplicavel','Não aplicável',v?.estado==='nao_aplicavel'):''}</select><input class="value-number" type="number" step="1" min="${s.valor_minimo??0}" ${s.valor_maximo_atributo!=null?'max="'+s.valor_maximo_atributo+'"':''} aria-label="${isProfile?'Alvo':'Valor'} de ${esc(a.nome)}" value="${v?.[field]??''}" ${v?.estado!=='conhecido'?'disabled':''}></div><input class="value-reason" aria-label="Motivo de ${esc(a.nome)}" placeholder="Observação deste valor (opcional)" maxlength="500" value="${esc(v?.motivo||'')}"></div>`;
  }).join('')}</section>`).join('');
 };
 const loadMechanic=async(keep=false)=>{
  const current=++loading;$('#save-editor').disabled=true;
  const mid=Number($('#mechanic').value)||null;activeMechanic=null;
  try{
   const m=mid?await api('/mecanicas/'+mid):null;if(current!==loading)return;activeMechanic=m;
   const natures=m?.usa_natureza==='sim'?state.options.naturezas:[],abilities=m?.usa_habilidade==='sim'?sheet.habilidades:[];
   const natureIds=keep?(isProfile?existing?.naturezas:[existing?.id_natureza]):[];
   const abilityIds=keep?(isProfile?existing?.habilidades:[existing?.id_habilidade_forma]):[];
   $('#context-fields').innerHTML=`<div class="field-grid">${isProfile?`<label>Naturezas preferidas (opcional)<select id="nature" multiple size="3">${natures.map(n=>option(n.id_natureza,n.nome,natureIds?.includes(n.id_natureza))).join('')}</select><span class="help">Ctrl/Cmd permite selecionar mais de uma.</span></label><label>Habilidades preferidas (opcional)<select id="ability" multiple size="3">${abilities.map(h=>option(h.id_habilidade_forma,h.nome,abilityIds?.includes(h.id_habilidade_forma))).join('')}</select></label><label class="wide">Regulamento de referência (opcional)<select id="regulation">${selectOptions(state.rules.filter(r=>r.id_mecanica===mid),'id_regulamento',r=>r.nome+' / '+r.versao,keep?existing?.id_regulamento:null)}</select></label>`:`<label>Natureza<select id="nature">${selectOptions(natures,'id_natureza',n=>n.nome,keep?existing?.id_natureza:null)}</select></label><label>Habilidade<select id="ability">${selectOptions(abilities,'id_habilidade_forma',h=>h.nome,keep?existing?.id_habilidade_forma:null)}</select></label><label>Nível<input id="level" type="number" step="1" min="${m?.nivel_minimo??0}" ${m?.nivel_maximo!=null?'max="'+m.nivel_maximo+'"':''} value="${keep?existing?.nivel??'':''}" ${m?.usa_nivel!=='sim'?'disabled':''}></label>`}</div>${m?`<h3>${isProfile?'Valores alvo':'Valores do exemplar'}</h3><p class="hint">Não informado, desconhecido e zero são estados distintos. ${isProfile?'Um alvo maior não é automaticamente melhor.':'Preencha apenas o que conhece.'}</p>${updateValues(m,keep)}${source(m.fonte_url,m.data_verificacao)}`:'<p class="hint">Sem versão de mecânica: natureza, habilidade, nível e atributos permanecem não informados.</p>'}`;
   $$('.value-state',dialog).forEach(select=>select.onchange=()=>{const number=$('.value-number',select.closest('.attribute'));number.disabled=select.value!=='conhecido';if(number.disabled)number.value='';});
  }catch(e){modalError(e.message);}finally{if(current===loading)$('#save-editor').disabled=isProfile&&!activeMechanic;}
 };
 const loadSheet=async(keep=false)=>{
  const revision=++sheetLoading;$('#save-editor').disabled=true;try{
   const response=await api('/pokemon/'+$('#sheet').value);if(revision!==sheetLoading)return;sheet=response;
   $('#mechanic').innerHTML=(isProfile?'':option('','Não informada'))+sheet.mecanicas.map(m=>option(m.id_mecanica,m.versao,keep&&m.id_mecanica===existing?.id_mecanica)).join('');
   if(!keep)$('#context-warning').hidden=false;
   await loadMechanic(keep);
  }catch(e){modalError(e.message);}
 };
 $('#sheet').onchange=()=>loadSheet();$('#mechanic').onchange=()=>{ $('#context-warning').hidden=false;loadMechanic(); };
 if(!isProfile){const origin=()=>{$('#origin-sheet').innerHTML=selectOptions(allSheets.filter(s=>s.id_jogo===Number($('#origin-game').value)),'id_dados_forma',s=>s.label,existing?.id_dados_forma_origem);};$('#origin-game').onchange=origin;origin();}
 $('#editor').onsubmit=async e=>{
  e.preventDefault();const b=$('#save-editor');b.disabled=true;
  try{
   const form=e.target,data=Object.fromEntries(new FormData(form));
   data[isProfile?'id_dados_forma':'id_dados_forma_atual']=Number($('#sheet').value);data.id_mecanica=activeMechanic?.id_mecanica||null;
   const nullable=s=>Number($(s).value)||null;
   if(isProfile){data.id_regulamento=nullable('#regulation');data.naturezas=$$('#nature option:checked').map(o=>Number(o.value));data.habilidades=$$('#ability option:checked').map(o=>Number(o.value));}
   else{data.id_natureza=nullable('#nature');data.id_habilidade_forma=nullable('#ability');data.nivel=$('#level').value===''?null:Number($('#level').value);data.id_jogo_origem=nullable('#origin-game');data.id_dados_forma_origem=nullable('#origin-sheet');data.id_metodo_obtencao=data.id_metodo_obtencao?Number(data.id_metodo_obtencao):null;}
   const field=isProfile?'valor_alvo':'valor';data.valores=[];
   for(const row of $$('.attribute',dialog)){
    const estado=$('.value-state',row).value,reason=$('.value-reason',row).value;
    if(!estado){if(reason.trim())throw new Error('Selecione o estado para salvar a observação do atributo.');continue;}
    const num=$('.value-number',row).value;if(estado==='conhecido'&&num==='')throw new Error('Informe o número de cada atributo conhecido, inclusive zero.');
    data.valores.push({id_mecanica_sistema_atributo:Number(row.dataset.system),id_atributo:Number(row.dataset.attribute),estado,[field]:estado==='conhecido'?Number(num):null,motivo:reason||null});
   }
   const resource=isProfile?'perfis':'colecao',id=existing?.[isProfile?'id_perfil':'id_pokemon_colecao'];
   await api('/'+resource+(id?'/'+id:''),{method:id?'PATCH':'POST',body:data});dialog.close();await render();feedback(isProfile?'Perfil salvo.':'Exemplar salvo.');
  }catch(err){modalError(err.message);}finally{b.disabled=false;}
 };
 await loadSheet(Boolean(existing));
}
function comparisonView(){
 content.innerHTML=heading('04 / COMPARAÇÃO EXPLICÁVEL','Compare com <em>intenção.</em>','O resultado descreve a distância até o alvo. Acima ou abaixo não significa melhor ou pior.')+(!state.collection.length||!state.profiles.length?empty('Precisamos de duas referências.','Registre um exemplar e crie um perfil compatível para a mesma forma, jogo e versão da mecânica.','<a class="button" href="#colecao">Ir para minha coleção →</a>'):`<form id="comparison" class="panel"><div class="field-grid"><label>Exemplar<select name="id_pokemon_colecao">${state.collection.map(p=>option(p.id_pokemon_colecao,(p.apelido||p.nome_pt)+' / '+p.nome_jogo_atual)).join('')}</select></label><label>Perfil<select name="id_perfil">${state.profiles.map(p=>option(p.id_perfil,p.nome_perfil)).join('')}</select></label></div><div class="toolbar"><button class="primary">Comparar campos ↗</button></div></form><div id="comparison-result"></div>`);
 const form=$('#comparison');if(!form)return;form.onsubmit=async e=>{e.preventDefault();const button=$('button',form);button.disabled=true;try{const body=Object.fromEntries([...new FormData(form)].map(([k,v])=>[k,Number(v)])),result=await api('/analises',{method:'POST',body});$('#comparison-result').innerHTML=`<section class="panel"><span class="eyebrow">RESULTADO / ${esc(result.mecanica.versao)}</span><h2>${esc(result.perfil.nome_perfil)}</h2><p class="hint">${esc(result.interpretacao)}</p><div class="table-wrap"><table><thead><tr><th>SISTEMA / ATRIBUTO</th><th>REAL</th><th>ALVO</th><th>DIFERENÇA</th><th>LEITURA</th></tr></thead><tbody>${result.campos.map(r=>`<tr><td>${esc(r.sistema)} / ${esc(r.atributo)}</td><td class="numeric">${r.real??'—'} <small>${r.real==null?esc(labels[r.estado_real]||r.estado_real):''}</small></td><td class="numeric">${r.alvo??'—'}</td><td class="numeric">${r.diferenca??'—'}</td><td>${tag(labels[r.estado]||r.estado,['sem_dado','nao_verificado'].includes(r.estado))}</td></tr>`).join('')}</tbody></table></div><h3>Preferências categóricas</h3>${result.preferencias.map(p=>`<p class="help">${p.campo==='id_natureza'?'Natureza':'Habilidade'}: ${esc(labels[p.estado]||p.estado)}</p>`).join('')}${source(result.mecanica.fonte_url,result.mecanica.data_verificacao)}${result.elegibilidade?eligibilityHtml(result.elegibilidade):''}</section>`;}catch(err){$('#comparison-result').innerHTML='';feedback(err.message,true);}finally{button.disabled=false;}};
}
function eligibilityHtml(item){return `<div class="panel"><h2>Elegibilidade da forma</h2>${tag(labels[item.status]||item.status,item.status==='nao_verificado')}<p>${esc(item.condicao||'Sem condição adicional registrada.')}</p>${source(item.fonte_url,item.data_verificacao)}<p class="hint">Esta consulta trata da forma no regulamento. Não comprova a legalidade completa do exemplar, seus golpes, itens, eventos ou origem.</p></div>`;}
function regulations(){
 const allSheets=sheets();content.innerHTML=heading('05 / REGRAS E EVIDÊNCIAS','Contexto antes <em>da conclusão.</em>','Consulte a elegibilidade da forma em uma versão de regulamento e acompanhe a origem da informação.')+(!state.rules.length||!allSheets.length?empty('Regras ainda não verificadas.','O banco não possui regulamentos e fichas suficientes para esta consulta. A ausência de evidência não significa que uma forma seja proibida.'):`<form id="eligibility" class="panel"><div class="field-grid"><label>Regulamento<select id="rule">${state.rules.map(r=>option(r.id_regulamento,r.nome+' / '+r.versao)).join('')}</select></label><label>Forma e jogo<select id="rule-sheet">${allSheets.map(s=>option(s.id_dados_forma,s.label)).join('')}</select></label></div><div class="toolbar"><button class="primary">Consultar evidência ↗</button></div></form><div id="eligibility-result"></div>`);
 const form=$('#eligibility');if(form)form.onsubmit=async e=>{e.preventDefault();try{const result=await api(`/regulamentos/${$('#rule').value}/formas/${$('#rule-sheet').value}`);$('#eligibility-result').innerHTML=eligibilityHtml(result);}catch(err){$('#eligibility-result').innerHTML='';feedback(err.message,true);}};
}
window.addEventListener('hashchange',render);
(async()=>{try{
 const [catalogData,options,rules,coverage,user]=await Promise.all([api('/pokemon'),api('/opcoes'),api('/regulamentos'),api('/catalogo/cobertura'),api('/auth/me').catch(e=>{if(e.status===401)return null;throw e;})]);
 state.all=catalogData.itens;state.options=options;state.rules=rules.itens;state.coverage=coverage;state.user=user?.usuario||null;account();await render();
}catch(e){content.innerHTML=empty('O arquivo não abriu.','Confira a inicialização do banco e recarregue a página.');feedback(e.message,true);}})();
