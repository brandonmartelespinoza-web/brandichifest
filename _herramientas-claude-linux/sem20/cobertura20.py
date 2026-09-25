# cobertura20.py — busca cada ítem del sílabo de la SEM 20 en el texto normalizado de la guía
import re, unicodedata, html
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    return re.sub(r'\s+',' ',t)
h=open('/home/user/brandichifest/SEM 20/GUIA-SEM20.html',encoding='utf8').read()
h=re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>',' ',h); txt=norm(html.unescape(re.sub(r'<[^>]+>',' ',h)))
items={
 'Estructura histológica general del tubo':['estructura histologica general|plan general del tubo'],
 'Capa mucosa':['mucosa'],'Capa submucosa':['submucosa'],'Capa muscular':['muscular externa|capa muscular'],'Serosa':['serosa'],
 'Cavidad bucal: descripción general':['cavidad bucal'],'Labios':['labio'],'Mejillas':['mejilla'],'Encías':['encia'],'Paladar':['paladar'],
 'Dientes: histología':['esmalte','dentina','cemento','pulpa'],'Dientes temporarios':['temporari'],'Dientes definitivos':['definitiv'],
 'Lengua: estructura histológica':['lengua'],'Lengua: epitelio de revestimiento':['epitelio plano estratificado'],'Papilas':['filiforme','fungiforme','foliad','caliciforme'],
 'Corpúsculos gustativos':['corpusculo'],'Parte móvil y raíz de la lengua':['parte movil','raiz'],'Inervación táctil':['tacto'],'Inervación gustativa':['gusto'],'Inervación motora':['hipogloso'],
 'Parótida':['parotida'],'Submandibular':['submandibular'],'Sublingual':['sublingual'],
 'Orofaringe: estructura y función':['orofaringe'],
 'Esófago: generalidades':['esofago'],'Relaciones cervicales':['cervical'],'Relaciones torácicas':['toracic'],'Relaciones abdominales':['abdominal'],
 'Esófago: vascularización arterial':['arterias esofagicas|arteria tiroidea inferior'],'Esófago: vascularización venosa':['venas esofagicas'],
 'Esófago: histología de sus capas':['glandulas esofagicas'],'Esófago: diferencias por sectores':['tercio superior'],'Esófago: funciones':['funcion del esofago|transporte del bolo'],
 'Pared abdominal':['pared abdominal'],'Músculos anchos':['musculos anchos'],'Recto abdominal':['recto abdominal'],'Regiones de la pared':['hipocondrio','mesogastrio','fosa iliaca'],
 'Puntos débiles':['puntos debiles'],'Línea alba':['linea alba'],'Conducto inguinal: paredes':['pared anterior','pared posterior'],'Conducto inguinal: orificios':['orificio profundo','orificio superficial'],'Conducto inguinal: contenido':['cordon espermatico','ligamento redondo del utero'],
 'Cuadrilátero de Grynfelt':['grynfelt'],'Triángulo de J. L. Petit':['petit'],
 'Peritoneo: concepto':['peritoneo'],'Peritoneo visceral y parietal':['peritoneo visceral','peritoneo parietal'],'Cavidad peritoneal':['cavidad peritoneal'],
 'Mesos':['meso'],'Ligamentos':['ligamento'],'Epiplones':['epiplon'],'Fascias de coalescencia':['fascia de coalescencia|fascias de coalescencia'],
 'Intraperitoneales':['intraperitoneal'],'Extraperitoneales':['extraperitoneal'],'Retroperitoneales':['retroperitoneal'],
 'Estómago: descripción':['fundus|fornix'],'Peritoneo gástrico':['peritoneo gastrico'],'Estómago: relaciones':['transcavidad'],'Estómago: arterias':['gastrica izquierda','gastroepiploica'],
 'Estómago: venas':['gastroomental|gastricas izquierda'],'Estómago: linfáticos':['linfatic'],'Regiones del estómago y sus diferenciaciones':['cardial','fundica','pilorica'],
 'Mucosa gástrica: epitelio':['cilindrico simple secretor'],'Lámina propia y glándulas':['glandulas gastricas|glandula fundica'],'Tipos celulares':['parietal','principal'],
 'Morfología al MO':['al mo'],'Morfología al ME':['al me'],'Estómago: submucosa, muscular y serosa':['oblicua'],'Estómago: funciones':['reservorio'],
 'Intestino delgado y grueso: capas':['intestino delgado','intestino grueso'],'Estructuras que aumentan la superficie':['aumento de la superficie|aumentan la superficie'],
 'Relación estructura-función':['absorcion'],'Duodeno':['duodeno'],'Yeyuno-íleon':['yeyuno','ileon'],'Diferencias duodeno/yeyuno/íleon':['brunner','placas de peyer'],
 'Diferencias delgado/grueso':['tenias','haustras'],'Apéndice vermiforme':['apendice'],
 'Irrigación del tracto':['tronco celiaco','mesenterica superior','mesenterica inferior'],'Vías linfáticas':['quilifero'],'Inervación del tracto':['meissner','auerbach'],
 'Células enteroendocrinas':['enteroendocrina'],
 'Motilidad (apunte de la semana)':['ondas lentas','peristaltismo','segmentacion'],'Secreción salival (TP)':['pilocarpina','atropina'],
}
ok=0; miss=[]
for k,alts in items.items():
    hit=all(any(re.search(a,txt) for a in alt.split('|')) for alt in alts)
    ok+=hit
    if not hit: miss.append(k)
print(f'{ok}/{len(items)} cubiertos'); print('faltan:',miss)
