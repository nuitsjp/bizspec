# 記述例の節を template.html に書き込む
import os
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')
t=open(TEMPLATE).read()
def task(cx,cy,name,kind):
    x=cx-65; y=cy-28
    return f'<rect class="fb" x="{x}" y="{y}" width="130" height="56" rx="9"/><text class="fy" x="{x+7}" y="{y+13}">{kind}</text><text class="fn" x="{cx}" y="{cy+10}" text-anchor="middle">{name}</text>'
def flow(pts):
    d=' '.join(('L' if i else 'M')+f'{p[0]} {p[1]}' for i,p in enumerate(pts))
    return f'<path class="fl" d="{d}" marker-end="url(#fa)"/>'
def lab(x,y,s,a='middle'): return f'<text class="ft" x="{x}" y="{y}" text-anchor="{a}">{s}</text>'
def gw(cx,cy,kind):
    r=18
    s=f'<polygon class="fb" points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"/>'
    if kind=='x': s+=f'<path class="fg" d="M{cx-6} {cy-6} L{cx+6} {cy+6} M{cx+6} {cy-6} L{cx-6} {cy+6}"/>'
    else: s+=f'<path class="fg" d="M{cx-8} {cy} L{cx+8} {cy} M{cx} {cy-8} L{cx} {cy+8}"/>'
    return s
def start(cx,cy): return f'<circle class="fb" cx="{cx}" cy="{cy}" r="10"/>'
def end(cx,cy,name,lx,ly,a='middle'): return f'<circle class="fe" cx="{cx}" cy="{cy}" r="9"/><text class="fs" x="{lx}" y="{ly}" text-anchor="{a}">{name}</text>'
p=[]; W=1000; H=470
lanes=[(0,130,'申請者'),(130,250,'上長'),(250,360,'システム'),(360,470,'経理担当')]
p.append(f'<rect class="pl" x="1" y="1" width="{W-2}" height="{H-1}"/><line class="pl" x1="26" y1="1" x2="26" y2="{H}"/><line class="pl" x1="52" y1="1" x2="52" y2="{H}"/>')
p.append(f'<text class="ll" transform="translate(18,{H//2}) rotate(-90)" text-anchor="middle">経費精算</text>')
for y0,y1,n in lanes:
    if y0: p.append(f'<line class="pl" x1="26" y1="{y0}" x2="{W-1}" y2="{y0}"/>')
    p.append(f'<text class="ll" transform="translate(43,{(y0+y1)//2}) rotate(-90)" text-anchor="middle">{n}</text>')
p.append(flow([(105,72),(123,72)]))
p.append(flow([(255,72),(280,72)]))
p.append(flow([(318,72),(363,72)])+lab(340,64,'取下げ'))
p.append(flow([(300,90),(300,190),(338,190)])+lab(308,145,'申請','start'))
p.append(flow([(470,190),(495,190)]))
p.append(flow([(515,172),(515,22),(190,22),(190,42)])+lab(352,16,'差戻し'))
p.append(flow([(533,190),(578,190)])+lab(555,182,'却下'))
p.append(flow([(515,208),(515,305),(600,305)])+lab(523,260,'承認','start'))
p.append(flow([(638,305),(678,305)]))
p.append(flow([(620,323),(620,415),(678,415)]))
p.append(flow([(810,305),(840,305)]))
p.append(flow([(810,415),(860,415),(860,325)]))
p.append(flow([(878,305),(923,305)]))
p.append(start(95,72)); p.append(task(190,72,'経費申請','ユーザー')); p.append(gw(300,72,'x')); p.append(end(375,72,'取下げ',375,98))
p.append(task(405,190,'申請承認','ユーザー')); p.append(gw(515,190,'x')); p.append(end(590,190,'却下',590,216))
p.append(gw(620,305,'p')); p.append(task(745,305,'支払データ作成','サービス')); p.append(task(745,415,'領収書原本の確認','マニュアル'))
p.append(gw(860,305,'p')); p.append(end(935,305,'精算完了',935,331))
svg=f'<svg viewBox="0 0 {W} {H+2}" role="img" aria-label="経費精算のビジネスユースケースをBPMNで描いた図。申請者、上長、システム、経理担当の4つのレーンがある。開始イベントから経費申請、申請承認へ進み、それぞれの後ろの排他ゲートウェイで作業結果ごとに分かれる。承認の後、並行ゲートウェイで支払データ作成と領収書原本の確認に分かれ、合流して終了イベントの精算完了に着く。取下げと却下の終了イベントもある。"><defs><marker id="fa" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path class="fa" d="M1 1.5 L11 6 L1 10.5 Z"/></marker></defs>'+''.join(p)+'</svg>'
def tb(head,rows):
    h=''.join(f'<th>{c}</th>' for c in head)
    r=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
sec=f'''<section class="ex">
    <div>
      <h2>記述例：ビジネスユースケース仕様書</h2>
      <p class="note">上の概念モデルに沿って、1つのビジネスユースケースを仕様書として書いた例です。業務の内容は説明用の架空のものです。人が読んで合意するために必要な項目だけを載せています。</p>
    </div>
    <div class="doc">
      <h3 class="doct">経費精算</h3>
      <dl class="facts">
        <dt>概要</dt><dd>従業員が立て替えた経費を申請し、上長の承認を経て、精算する。</dd>
        <dt>きっかけ</dt><dd>従業員が、業務のために経費を立て替えた。</dd>
        <dt>事前条件</dt><dd>申請者と、その上長が登録されている。</dd>
        <dt>事後条件</dt><dd>
          <ul class="plain">
            <li><b>精算完了</b>：支払データが作られ、領収書の原本が確認されている。経費申請は精算済みである。</li>
            <li><b>取下げ</b>：経費申請は残っていない。</li>
            <li><b>却下</b>：経費申請は却下済みとして残り、支払データは作られていない。</li>
          </ul></dd>
      </dl>
      <h3>アクター</h3>
      {tb(['アクター','役割'],[['申請者','経費を立て替え、精算を申請する'],['上長','申請の内容を確かめ、承認、差戻し、却下のいずれかを決める'],['経理担当','領収書の原本を、申請の内容と照らして確かめる'],['システム','支払データを、人の操作なしに作る']])}
      <h3>業務の流れ</h3>
      <figure class="flow">{svg}</figure>
      <p class="note">BPMNの記法で描いています。レーンがアクター、角の丸い四角が作業、×のひし形が作業結果による分岐、＋のひし形が並行する作業の始まりと終わりです。分岐から出る線には、作業結果の名前を書いています。</p>
      <h3>作業</h3>
      {tb(['作業','種類','担い手','概要','事前条件','作業結果と事後条件'],[
        ['経費申請','ユーザー作業','申請者','立て替えた経費の内容を入力し、申請する','経費を立て替えている','<b>申請</b>：経費申請が申請済みになる<br><b>取下げ</b>：経費申請は残らない'],
        ['申請承認','ユーザー作業','上長','申請の内容を確かめ、承認、差戻し、却下のいずれかを決める','経費申請が申請済みである','<b>承認</b>：経費申請が承認済みになる<br><b>差戻し</b>：経費申請が申請者へ戻る<br><b>却下</b>：経費申請が却下済みになる'],
        ['支払データ作成','サービス作業','システム','承認された金額の支払データを作る','経費申請が承認済みである','<b>作成済み</b>：支払データが作られている'],
        ['領収書原本の確認','マニュアル作業','経理担当','提出された領収書の原本を、申請の内容と照らして確かめる','経費申請が承認済みである','<b>確認済み</b>：領収書の原本が確認されている']])}
      <h3>扱う情報</h3>
      {tb(['ビジネスオブジェクト','説明','状態'],[
        ['経費申請','従業員が立て替えた経費1件の申請。このユースケースで作られる','申請済み、承認済み、却下済み、精算済み'],
        ['支払データ','承認された金額を支払うためのデータ。このユースケースで作られる','—']])}
      <h3>シナリオ一覧</h3>
      {tb(['シナリオ','目的','終わり方'],[
        ['承認された経費を精算する','申請が差戻しも却下もなく進み、精算が完了することを確かめる','精算完了'],
        ['差戻しを受けて申請し直す','差し戻された申請を直して出し直し、精算が完了することを確かめる','精算完了'],
        ['申請を取り下げる','申請者が入力の途中でやめたとき、経費申請が残らないことを確かめる','取下げ'],
        ['申請が却下される','上長が却下したとき、支払データが作られないことを確かめる','却下']])}
      <p class="note">この例では、1本目のシナリオだけを下に書いています。</p>
      <h3>シナリオ：承認された経費を精算する</h3>
      <dl class="facts">
        <dt>目的</dt><dd>申請が差戻しも却下もなく進み、精算が完了することを確かめる。</dd>
        <dt>事前条件</dt><dd>申請者が、立て替えた経費の領収書の原本を持っている。</dd>
        <dt>手順</dt><dd>
          <ol class="steps">
            <li>申請者が、立て替えた経費の内容を入力して申請する。</li>
            <li>上長が、申請の内容を確かめて承認する。</li>
            <li>システムが、支払データを作る。並行して、経理担当が、領収書の原本を確かめる。</li>
          </ol></dd>
        <dt>期待結果</dt><dd>支払データが作られ、領収書の原本が確認されている。経費申請は精算済みになり、ユースケースは「精算完了」で終わる。</dd>
      </dl>
    </div>
  </section>
'''
a=t.index('<section class="ex">'); b=t.rindex('</section>')+len('</section>')
t=t[:a]+sec.rstrip()+t[b:]
open(TEMPLATE,'w').write(t)
