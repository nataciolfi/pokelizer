/* Creates and exports real brModelo objects through the official distribution.
   No custom painting, XML format fabrication, or third-party renderer is used. */
import controlador.*;
import controlador.apoios.GuardaPadraoBrM;
import desenho.*;
import desenho.formas.Forma;
import desenho.linhas.SuperLinha;
import desenho.preAnyDiagrama.PreCardinalidade.TiposCard;
import diagramas.conceitual.*;
import diagramas.logico.*;
import java.awt.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import javax.imageio.ImageIO;
import util.ImageGenerate;
public class ExportModels {
 static class BatchEditor extends Editor {
  @Override public void PerformInspectorFor(FormaElementar f){} // UI only
  @Override public void addLastOpened(String p){} // UI only
  @Override public void DoAutoSaveCompleto(){} // UI only
 }
 static class Col { String name,type;boolean nn,pk,fk;Col(String[] s){name=s[2];type=s[3];nn=s[4].equals("1");pk=!s[5].equals("0");fk=s[6].equals("1");} }
 static class Tab {String name;List<Col> cols=new ArrayList<>();List<String[]> uniques=new ArrayList<>();Tab(String n){name=n;} }
 static class Fk {int id;String child,parent,del,upd;String[] cols,targets;boolean required;Fk(String[]s){id=Integer.parseInt(s[1]);child=s[2];parent=s[3];cols=s[4].split(",");targets=s[5].split(",");required=s[6].equals("1");del=s[7];upd=s[8];}}
 static LinkedHashMap<String,Tab> tabs=new LinkedHashMap<>();static List<Fk> fks=new ArrayList<>();static Path out;
 static boolean FULL=false;
 static Font FONT=new Font("SansSerif",Font.PLAIN,15),TITLE=new Font("SansSerif",Font.BOLD,17);
 static Diagrama diagram(boolean logical){BatchEditor e=new BatchEditor();Diagrama d=logical?new DiagramaLogico(e):new DiagramaConceitual(e);e.diagramaAtual=d;d.getListaDeItens().clear();d.setFont(FONT);e.setBackground(Color.WHITE);return d;}
 static void text(Diagrama d,String s,int x,int y,int w,int h){Texto t=new Texto(d);t.setTexto(s);t.setFont(FONT);t.SetBounds(x,y,w,h);}
 static Point center(Elementar f){return new Point(f.getLeft()+f.getWidth()/2,f.getTop()+f.getHeight()/2);}
 static Ligacao connect(Diagrama d,Forma a,Forma b,TiposCard card){
  Ligacao l=new Ligacao(d);
  l.setInteligente(false);l.SuperInicie(0,center(a),center(b));
  l.getPontaA().SetEm(a);l.getPontaB().SetEm(b);a.PosicionePonto(l.getPontaA());b.PosicionePonto(l.getPontaB());
  if(card!=null){l.PrepareCardinalidade();l.getCard().setCard(card);l.getCard().setFont(FONT);l.PrepareCardinalidade();}
  return l;
 }
 static Forma entity(Diagrama d,String name,int x,int y,boolean logical){
  Tab spec=tabs.get(name);
  if(logical){Tabela t=new Tabela(d);t.setTexto(name);t.setFont(FONT);t.setAutosize(false);t.setGradiente(false);t.setAlfa(0);t.setMostrarConstraints(false);t.SetBounds(x,y,540,80+spec.cols.size()*30);
   for(Col c:spec.cols){Campo f=new Campo(t);f.setTexto(c.name);f.setTipo(c.type);f.setComplemento(c.nn||c.pk?"NOT NULL":"");f.SetKey(c.pk);f.SetFkey(c.fk);}
   Constraint pk=new Constraint(t);pk.setTipo(Constraint.CONSTRAINT_TIPO.tpPK);pk.setNome("PK_"+name);
   for(Campo c:t.getCampos())if(c.isKey())pk.Add(c,c);
   for(int i=0;i<spec.uniques.size();i++){Constraint u=new Constraint(t);u.setTipo(Constraint.CONSTRAINT_TIPO.tpUNIQUE);u.setNome("UQ_"+name+"_"+i);for(String s:spec.uniques.get(i)){Campo c=field(t,s);u.Add(c,c);}}
   return t;
  }
  Entidade e=new Entidade(d);e.setTexto(name);e.setFont(TITLE);e.SetBounds(x,y,540,55);e.Reenquadre();
  int i=0;for(Col c:spec.cols){Atributo a=new Atributo(d);a.setTexto(c.name);a.setFont(FONT);a.SetBounds(x+25,y+85+24*i++,500,24);a.setIdentificador(c.pk);a.setOpcional(!c.nn&&!c.pk);Ligacao l=connect(d,a,e,null);
   // Native polyline spine stays left of the attribute labels.
   l.setInteligente(false);l.getPontos().get(0).setCentro(new Point(x+28,a.getTop()+12));l.getPontos().get(1).setCentro(new Point(x,e.getTop()+25));l.reSetBounds();}
  return e;
 }
 static void route(SuperLinha l,Forma source,Forma dest,boolean diamond){
  // Orthogonal native polyline in inter-column and inter-row gutters.
  while(l.getPontos().size()<6)l.InserirPonto(l.getPontos().size()-1);
  int sx=source.getLeftWidth(),sy=source.getTop()+25;
  int dx=diamond?dest.getLeft():dest.getLeftWidth(),dy=dest.getTop()+25;
  int gx=sx+15,hx=diamond?dx-10:dx+25,gy=source.getTop()-25;
  Point[] pts={new Point(sx,sy),new Point(gx,sy),new Point(gx,gy),new Point(hx,gy),new Point(hx,dy),new Point(dx,dy)};
  for(int i=0;i<6;i++)l.getPontos().get(i).setCentro(pts[i]);l.setInteligente(false);l.reSetBounds();
 }
 static Campo field(Tabela t,String n){return t.getCampos().stream().filter(c->c.getTexto().equals(n)).findFirst().orElseThrow();}
 static Constraint candidate(Tabela t,String[] cols){Set<String> names=new HashSet<>(Arrays.asList(cols));for(Constraint c:t.getConstraints()){Set<String>s=new HashSet<>();for(Campo f:c.getCamposDeOrigem())s.add(f.getTexto());if(s.equals(names))return c;}return null;}
 static void relation(Diagrama d,Forma child,Forma parent,Fk f,boolean logical,int diamondX,int diamondY){
  if(logical){Tabela c=(Tabela)child,p=(Tabela)parent;LogicoLinha l=new LogicoLinha(d);l.setInteligente(false);l.SuperInicie(0,center(p),center(c));l.getPontaA().SetEm(p);l.getPontaB().SetEm(c);p.PosicionePonto(l.getPontaA());c.PosicionePonto(l.getPontaB());l.getCardA().setCard(f.required?TiposCard.C11:TiposCard.C01);l.getCardB().setCard(TiposCard.C0N);l.PrepareCardinalidade();if(FULL)route(l,p,c,false);
   Constraint fk=new Constraint(c);fk.setTipo(Constraint.CONSTRAINT_TIPO.tpFK);fk.setNome("FK_"+f.id);Constraint origin=candidate(p,f.targets);for(int i=0;i<f.cols.length;i++)fk.Add(field(p,f.targets[i]),field(c,f.cols[i]),l,origin);fk.setObservacao("DELETE "+f.del+"; UPDATE "+f.upd);fk.setDdlOnDelete(f.del);fk.setDdlOnUpdate(f.upd);fk.setValidado(true);
   text(d,"R"+f.id,diamondX,diamondY,65,22);
  }else{Relacionamento r=new Relacionamento(d);r.setTexto("R"+f.id+" associa");r.setFont(FONT);r.SetBounds(diamondX,diamondY,180,60);r.Reenquadre();Ligacao lc=connect(d,child,r,f.required?TiposCard.C11:TiposCard.C01);Ligacao lp=connect(d,parent,r,TiposCard.C0N);if(FULL){route(lc,child,r,true);route(lp,parent,r,true);}}
 }
 static void sanitizeNativeMetadata(Path path)throws Exception{
  GuardaPadraoBrM wrapper;
  try(ObjectInputStream input=new ObjectInputStream(Files.newInputStream(path))){wrapper=(GuardaPadraoBrM)input.readObject();}
  // Public brModelo wrapper metadata fields. Preserve the native diagram payload.
  wrapper.autor="Pokelizer project";
  wrapper.data="";
  Path temporary=Files.createTempFile(path.getParent(),"brmodelo-metadata-",".tmp");
  try{
   try(ObjectOutputStream output=new ObjectOutputStream(Files.newOutputStream(temporary))){output.writeObject(wrapper);}
   Files.move(temporary,path,StandardCopyOption.REPLACE_EXISTING,StandardCopyOption.ATOMIC_MOVE);
  }finally{Files.deleteIfExists(temporary);}
  try(ObjectInputStream input=new ObjectInputStream(Files.newInputStream(path))){
   GuardaPadraoBrM checked=(GuardaPadraoBrM)input.readObject();
   if(!"Pokelizer project".equals(checked.autor)||!"".equals(checked.data))throw new Exception("wrapper metadata mismatch");
  }
 }
 static void sanitizeExisting(Path folder)throws Exception{
  try(java.util.stream.Stream<Path> files=Files.list(folder)){
   for(Path file:(Iterable<Path>)files.filter(p->p.toString().endsWith(".brM3")).sorted()::iterator){
    sanitizeNativeMetadata(file);
    Diagrama reopened=Diagrama.LoadFromFile(file.toFile(),new BatchEditor());
    if(reopened==null)throw new Exception("official reopen failed "+file);
    int entities=0,attributes=0,relationships=0;
    for(FormaElementar f:reopened.getListaDeItens()){if(f instanceof Tabela||f instanceof Entidade)entities++;if(f instanceof Atributo)attributes++;if(f instanceof Relacionamento||f instanceof LogicoLinha)relationships++;}
    System.out.println(file.getFileName()+"\treopened\tentities="+entities+"\tattributes="+attributes+"\trelationships="+relationships+"\tmetadata=generic-project-author;empty-date");
   }
  }
 }
 static void save(Diagrama d,String name)throws Exception{
  // brModelo copies parent types while linking; restore physical nullability after all links.
  d.isCarregando=true;for(FormaElementar shape:d.getListaDeItens())if(shape instanceof Tabela){Tabela table=(Tabela)shape;for(Col c:tabs.get(table.getTexto()).cols){field(table,c.name).setTipo(c.type);}}
  d.isCarregando=false;d.ClearSelect(false);
  if(!d.Salvar(out.resolve(name+".brM3").toString()))throw new Exception("native save failed "+name);
  sanitizeNativeMetadata(out.resolve(name+".brM3"));
  if(!d.Salvar(out.resolve(name+".xml").toString()))throw new Exception("XML save failed "+name);
  ImageIO.write(ImageGenerate.geraImagem(d),"png",out.resolve(name+".png").toFile());
  Diagrama reopened=Diagrama.LoadFromFile(out.resolve(name+".brM3").toFile(),new BatchEditor());
  if(reopened==null||reopened.getListaDeItens().size()!=d.getListaDeItens().size())throw new Exception("reopen mismatch "+name);
  int tables=0,attributes=0,relationships=0;for(FormaElementar f:reopened.getListaDeItens()){if(f instanceof Tabela||f instanceof Entidade)tables++;if(f instanceof Atributo)attributes++;if(f instanceof Relacionamento||f instanceof LogicoLinha)relationships++;}
  System.out.println(name+"\treopened\tentities="+tables+"\tattributes="+attributes+"\trelationships="+relationships+"\titems="+reopened.getListaDeItens().size());
 }
 static void full(boolean logical)throws Exception{
  FULL=true;Diagrama d=diagram(logical);text(d,"POKELIZER · "+(logical?"MODELO LÓGICO":"MODELO CONCEITUAL")+" · visão completa; relações ampliadas nas folhas R",35,10,2700,45);
  text(d,"Símbolos nativos: identificador preenchido; atributo opcional tracejado; chaves por ícones. R = vínculo descrito nas folhas. Regras condicionais: docs/stage1.",35,55,2800,40);
  Map<String,Forma> forms=new LinkedHashMap<>();int i=0;for(String name:tabs.keySet()){forms.put(name,entity(d,name,50+(i%5)*760,140+(i/5)*700,logical));i++;}
  Map<String,Integer> local=new HashMap<>();for(Fk f:fks){Forma c=forms.get(f.child),p=forms.get(f.parent);int n=local.getOrDefault(f.child,0);local.put(f.child,n+1);relation(d,c,p,f,logical,c.getLeft()+565,c.getTop()+85+n*75);}
  // Put opaque boxes and attributes after connectors, preventing lines crossing labels.
  List<FormaElementar> list=d.getListaDeItens();list.sort(Comparator.comparingInt(f->f instanceof SuperLinha?0:1));save(d,logical?"logico":"conceitual");
 }
 static void atlas(boolean logical)throws Exception{FULL=false;
  int page=1;for(int start=0;start<fks.size();start+=4){Diagrama d=diagram(logical);
   text(d,"POKELIZER · "+(logical?"LÓGICO":"CONCEITUAL")+" · relações ampliadas "+(start+1)+"–"+Math.min(start+4,fks.size()),35,10,2800,40);
   text(d,"Cada painel é uma vista do mesmo modelo. Entidades repetidas são referências; não representam novas tabelas. Cardinalidades genéricas + condições no rodapé.",35,55,2900,40);
   for(int j=start;j<Math.min(start+4,fks.size());j++){Fk f=fks.get(j);int x=50+(j-start)%2*1600,y=140+(j-start)/2*900;
    text(d,"R"+f.id+" · "+String.join(",",f.cols)+" → "+String.join(",",f.targets),x,y,1490,35);
    Forma c=entity(d,f.child,x,y+75,logical),p=entity(d,f.parent,x+960,y+75,logical);
    relation(d,c,p,f,logical,x+655,y+80);
    text(d,"Filho → pai: "+(f.required?"1..1":"0..1")+"; pai → filhos: 0..N. DELETE "+f.del+"; UPDATE "+f.upd+".",x,y+760,1480,30);
    text(d,"Condições: espécie completa = 1 padrão; tipos confirmados = 1..2; perfil pessoal = 1 dono; referência = 0 donos. Ver invariantes.",x,y+795,1500,55);
   }
   List<FormaElementar> list=d.getListaDeItens();list.sort(Comparator.comparingInt(f->f instanceof SuperLinha?0:1));save(d,(logical?"logico":"conceitual")+String.format("-relacoes-%02d",page++));
  }
 }
 public static void main(String[]args)throws Exception{Thread.setDefaultUncaughtExceptionHandler((t,e)->{e.printStackTrace();System.exit(1);});if(args[0].equals("--sanitize-existing")){sanitizeExisting(Paths.get(args[1]));System.exit(0);}
 out=Paths.get(args[1]);for(String line:Files.readAllLines(Paths.get(args[0]))){String[]s=line.split("\t",-1);switch(s[0]){case "T":tabs.put(s[1],new Tab(s[1]));break;case "C":tabs.get(s[1]).cols.add(new Col(s));break;case "U":tabs.get(s[1]).uniques.add(s[3].split(","));break;case "F":fks.add(new Fk(s));}}
 full(false);full(true);atlas(false);atlas(true);System.exit(0);}
}
