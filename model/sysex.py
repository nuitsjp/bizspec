# システムユースケースの記述例を template.html に追加する（ex.py の後に実行する）
import os
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')
import re

t = open(TEMPLATE).read()

css = '''
.fo { fill: none; stroke: var(--muted); stroke-width: 1.1; } .fam { fill: var(--muted); }
.fbo { fill: var(--sheet); stroke: var(--muted); stroke-width: 1.1; } .fno { fill: var(--muted); font-size: 13px; font-weight: 600; }
.fl2 { fill: none; stroke: var(--new); stroke-width: 2.2; } .fa2c { fill: var(--new); }
.fmo { fill: none; stroke: var(--ink); stroke-width: 1.6; } .fmi { fill: none; stroke: var(--new); stroke-width: 1.8; } .fmm { fill: none; stroke: var(--muted); stroke-width: 1.6; }
.ffr { fill: none; stroke: var(--ink); stroke-width: 1.2; } .fft { fill: var(--sheet); stroke: var(--ink); stroke-width: 1.2; } .ffn { fill: var(--ink); font-size: 12px; font-weight: 600; }
.flg { fill: var(--sheet); stroke: var(--rule); stroke-width: 1; } .flt { fill: var(--ink); font-size: 11.5px; }
.fna { fill: var(--ink); font-size: 12px; font-weight: 600; }
'''
if '.fna {' not in t:
    t = t.replace('</style>', css + '</style>', 1)


def path(pts, cls, marker):
    d = ' '.join(('L' if i else 'M') + f'{p[0]} {p[1]}' for i, p in enumerate(pts))
    return f'<path class="{cls}" d="{d}" marker-end="url(#{marker})"/>'


def inr(pts):
    return path(pts, 'fl2', 'm-in')


def out(pts):
    return path(pts, 'fo', 'm-out')


def lab(x, y, s, a='middle', cls='ft'):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{a}">{s}</text>'


def st(cx, cy, name, inrange=True):
    x = cx - 65
    y = cy - 25
    rc, tc = ('fb', 'fn') if inrange else ('fbo', 'fno')
    return (f'<rect class="{rc}" x="{x}" y="{y}" width="130" height="50" rx="10"/>'
            f'<text class="{tc}" x="{cx}" y="{cy + 5}" text-anchor="middle">{name}</text>')


def tb(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


FRAME = '<rect class="ffr" x="1" y="-37" width="798" height="366"/><polygon class="fft" points="1,-37 214,-37 214,-22 202,-11 1,-11"/><text class="ffn" x="10" y="-19">stm 経費精算システム</text>'

q = []
# 範囲の外（薄い線）
q.append(out([(150, 185), (150, 260), (353, 260)]) + lab(250, 253, '申請を選ぶ', 'middle', 'fs'))
q.append(out([(380, 235), (380, 205), (190, 205), (190, 187)]) + lab(285, 199, '検索画面へ戻る', 'middle', 'fs'))
q.append(out([(420, 285), (420, 310), (110, 310), (110, 187)]) + lab(265, 304, '承認する／差し戻す／却下する', 'middle', 'fs'))
# 範囲の中（濃い線）
q.append(inr([(150, 135), (150, 80), (353, 80)]) + lab(250, 72, '新規作成'))
q.append(inr([(485, 70), (623, 70)]) + lab(554, 62, '確認へ進む'))
q.append(inr([(625, 92), (487, 92)]) + lab(554, 108, '修正する'))
q.append(inr([(690, 55), (690, 26), (110, 26), (110, 133)]) + lab(400, 20, '申請する'))
q.append(inr([(420, 105), (420, 160), (217, 160)]) + lab(320, 153, 'やめる'))
q.append(st(150, 160, '検索画面'))
q.append(st(420, 80, '申請画面'))
q.append(st(690, 80, '申請確認画面'))
q.append(st(420, 260, '承認画面', False))
q.append('<circle class="fa2c" cx="150" cy="108" r="7"/>' + lab(138, 112, '始点', 'end'))
q.append('<rect class="flg" x="548" y="236" width="238" height="84" rx="4"/>')
q.append('<path class="fl2" d="M562 256 L606 256"/>' + lab(616, 260, 'このユースケースの範囲', 'start', 'flt'))
q.append('<circle class="fa2c" cx="584" cy="278" r="7"/>' + lab(616, 282, '始点となる画面遷移', 'start', 'flt'))
q.append('<path class="fo" d="M562 300 L606 300"/>' + lab(616, 304, '範囲の外', 'start', 'flt'))

aria = ('経費精算システムの画面遷移の全体と、ユーザーユースケース「経費申請」の範囲を示した図。'
        '画面は検索画面、申請画面、申請確認画面、承認画面の4つ。範囲に入る画面遷移は、検索画面から申請画面への新規作成、'
        '申請画面から申請確認画面への確認へ進む、申請確認画面から申請画面への修正する、申請確認画面から検索画面への申請する、'
        '申請画面から検索画面へのやめる。始点となる画面遷移は新規作成。検索画面と承認画面の間の画面遷移は、範囲の外にある。')
svg2 = (f'<svg viewBox="0 -38 800 368" role="img" aria-label="{aria}"><defs>'
        '<marker id="m-in" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" '
        'orient="auto-start-reverse"><path class="fmi" d="M1.5 1.5 L11 6 L1.5 10.5"/></marker>'
        '<marker id="m-out" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" '
        'orient="auto-start-reverse"><path class="fmm" d="M1.5 1.5 L11 6 L1.5 10.5"/></marker></defs>'
        + FRAME + ''.join(q) + '</svg>')


def allp(pts):
    return path(pts, 'fl', 'm-all')


u = []
u.append(allp([(49, 160), (83, 160)]))
u.append(allp([(150, 185), (150, 260), (353, 260)]) + lab(250, 253, '申請を選ぶ'))
u.append(allp([(380, 235), (380, 205), (190, 205), (190, 187)]) + lab(285, 199, '検索画面へ戻る'))
u.append(allp([(420, 285), (420, 310), (110, 310), (110, 187)]) + lab(265, 304, '承認する／差し戻す／却下する'))
u.append(allp([(150, 135), (150, 80), (353, 80)]) + lab(250, 72, '新規作成'))
u.append(allp([(485, 70), (623, 70)]) + lab(554, 62, '確認へ進む'))
u.append(allp([(625, 92), (487, 92)]) + lab(554, 108, '修正する'))
u.append(allp([(690, 55), (690, 26), (110, 26), (110, 133)]) + lab(400, 20, '申請する'))
u.append(allp([(420, 105), (420, 160), (217, 160)]) + lab(320, 153, 'やめる'))
u.append('<circle class="fk" cx="40" cy="160" r="9"/>')
u.append(st(150, 160, '検索画面'))
u.append(st(420, 80, '申請画面'))
u.append(st(690, 80, '申請確認画面'))
u.append(st(420, 260, '承認画面'))
aria_ui = ('経費精算システムのステートマシン図。開始の黒い丸から検索画面へ進む。画面は検索画面、申請画面、申請確認画面、承認画面の4つ。'
           '検索画面から新規作成で申請画面へ、確認へ進むで申請確認画面へ進む。申請確認画面から修正するで申請画面へ、申請するで検索画面へ進む。'
           '申請画面からやめるで検索画面へ戻る。検索画面から申請を選ぶで承認画面へ進み、承認画面から承認する、差し戻す、却下する、検索画面へ戻るで検索画面へ戻る。')
svg_ui = (f'<svg viewBox="0 -38 800 368" role="img" aria-label="{aria_ui}"><defs>'
          '<marker id="m-all" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" '
          'orient="auto-start-reverse"><path class="fmo" d="M1.5 1.5 L11 6 L1.5 10.5"/></marker></defs>'
          + FRAME + ''.join(u) + '</svg>')

states = tb(['画面', '説明', 'そこから出る画面遷移'], [
    ['検索画面', '経費申請を検索し、一覧で表示する', '新規作成、申請を選ぶ'],
    ['申請画面', '経費の日付、金額、内容を入力する', '確認へ進む、やめる'],
    ['申請確認画面', '入力した内容を、申請の前に確かめる', '申請する、修正する'],
    ['承認画面', '選んだ経費申請の内容を表示する', '承認する、差し戻す、却下する、検索画面へ戻る']])
info = tb(['ビジネスオブジェクト', '使い方'], [
    ['経費申請', '入力の内容から作り、状態を申請済みにする。ビジネスレイヤーの定義を参照する']])
scen = tb(['シナリオ', '目的', '終わり方（作業結果）'], [
    ['経費を申請する', '入力した内容を確かめて申請できることを確かめる', '申請'],
    ['入力を直してから申請する', '申請確認画面から申請画面へ戻って直せることを確かめる', '申請'],
    ['入力をやめる', '入力の途中でやめたとき、経費申請が作られないことを確かめる', '取下げ']])
attrs = tb(['仕様書の項目', '加えた先', '属性・関連'], [
    ['概要、きっかけ、事前条件', 'システムユースケース', '概要、きっかけ、事前条件'],
    ['ユースケースの範囲と始点', 'ユーザーユースケース', '画面遷移への関連（範囲、始点）'],
    ['画面の説明', '画面', '説明'],
    ['アクターの操作', '画面遷移', 'イベント'],
    ['処理の説明', '処理', '説明'],
    ['分岐の条件', '処理遷移', '条件'],
    ['シナリオの事前条件、手順、終わり方', 'システムユースケースシナリオ', '事前条件、手順、終わり方（作業結果を指す）']])


# ===== サービスユースケースの記述例 =====
def act(cx, cy, name):
    x = cx - 85
    y = cy - 22
    return (f'<rect class="fb" x="{x}" y="{y}" width="170" height="44" rx="16"/>'
            f'<text class="fna" x="{cx}" y="{cy + 4}" text-anchor="middle">{name}</text>')


def dia(cx, cy):
    r = 16
    return f'<polygon class="fb" points="{cx},{cy - r} {cx + r},{cy} {cx},{cy + r} {cx - r},{cy}"/>'


v = []
v.append(allp([(45, 100), (63, 100)]))
v.append(allp([(235, 100), (257, 100)]))
v.append(allp([(275, 84), (275, 45), (353, 45)]) + lab(283, 62, '[振込]', 'start'))
v.append(allp([(275, 116), (275, 155), (353, 155)]) + lab(283, 146, '[給与と合算]', 'start'))
v.append(allp([(525, 45), (600, 45), (600, 82)]))
v.append(allp([(525, 155), (600, 155), (600, 118)]))
v.append(allp([(616, 100), (653, 100)]))
v.append(allp([(825, 100), (858, 100)]))
v.append('<circle class="fk" cx="36" cy="100" r="9"/>')
v.append(act(150, 100, '承認済みの経費申請を読む'))
v.append(dia(275, 100))
v.append(act(440, 45, '振込データを作る'))
v.append(act(440, 155, '給与合算データを作る'))
v.append(dia(600, 100))
v.append(act(740, 100, '支払データを保存する'))
v.append('<circle class="fb" cx="870" cy="100" r="10"/><circle class="fk" cx="870" cy="100" r="6"/>')
aria_sv = ('サービスユースケース「支払データ作成」のアクティビティ図。開始から、承認済みの経費申請を読む。'
           '支払方法が振込なら振込データを作り、給与と合算なら給与合算データを作る。'
           'どちらの場合も、支払データを保存して終わる。')
svg_sv = (f'<svg viewBox="0 -38 900 240" role="img" aria-label="{aria_sv}"><defs>'
          '<marker id="m-all" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" '
          'orient="auto-start-reverse"><path class="fmo" d="M1.5 1.5 L11 6 L1.5 10.5"/></marker></defs>'
          '<rect class="ffr" x="1" y="-37" width="898" height="238"/>'
          '<polygon class="fft" points="1,-37 204,-37 204,-22 192,-11 1,-11"/>'
          '<text class="ffn" x="10" y="-19">act 支払データ作成</text>'
          + ''.join(v) + '</svg>')
sv_steps = tb(['処理', '説明'], [
    ['承認済みの経費申請を読む', '承認された経費申請から、金額と支払方法を読む'],
    ['振込データを作る', '支払方法が振込のとき、申請者の口座へ振り込むためのデータを作る'],
    ['給与合算データを作る', '支払方法が給与と合算のとき、給与計算へ渡すためのデータを作る'],
    ['支払データを保存する', '作ったデータを、支払データとして保存する']])
sv_info = tb(['ビジネスオブジェクト', '使い方'], [
    ['経費申請', '承認済みのものを読む。状態は変えない'],
    ['支払データ', '新しく作る']])
sv_scen = tb(['シナリオ', '目的', '終わり方（作業結果）'], [
    ['振込の支払データを作る', '支払方法が振込のとき、振込のデータが作られることを確かめる', '作成済み'],
    ['給与と合算する支払データを作る', '支払方法が給与と合算のとき、給与計算へ渡すデータが作られることを確かめる', '作成済み']])
svc_card = f"""<div class="doc">
      <h3 class="doct">サービスユースケース：支払データ作成</h3>
      <dl class="facts">
        <dt>詳細化する作業</dt><dd>支払データ作成（ビジネスユースケース「経費精算」のサービス作業）</dd>
        <dt>概要</dt><dd>承認された経費申請から、支払のためのデータを作る。人の操作なしに動く。</dd>
        <dt>きっかけ</dt><dd>上長が、経費申請を承認した。</dd>
        <dt>事前条件</dt><dd>経費申請が承認済みである。</dd>
      </dl>
      <h3>処理の流れ</h3>
      <figure class="flow">{svg_sv}</figure>
      <p class="note">UMLのアクティビティ図です。サービスユースケース1つにつき、1枚描きます。左上の「act」は、アクティビティ図であることを示す見出しです。角の丸い四角がアクションで、処理に当たります。矢印が制御フローで、処理遷移に当たります。ひし形は分岐と合流で、分岐から出る矢印の [ ] の中が条件です。黒い丸が開始、二重の丸が終了です。</p>
      <h3>処理</h3>
      {sv_steps}
      <h3>扱う情報</h3>
      {sv_info}
      <h3>シナリオ一覧</h3>
      {sv_scen}
      <p class="note">この例では、1本目のシナリオだけを下に書いています。</p>
      <h3>シナリオ：振込の支払データを作る</h3>
      <dl class="facts">
        <dt>目的</dt><dd>支払方法が振込のとき、振込のデータが作られることを確かめる。</dd>
        <dt>事前条件</dt><dd>承認済みの経費申請があり、その支払方法が振込である。</dd>
        <dt>手順</dt><dd>
          <ol class="steps">
            <li>システムが、承認済みの経費申請を読む。</li>
            <li>支払方法が振込なので、システムが振込データを作る。</li>
            <li>システムが、作ったデータを支払データとして保存する。</li>
          </ol></dd>
        <dt>期待結果</dt><dd>振込の支払データが保存されている。経費申請の状態は、承認済みのままである。</dd>
        <dt>終わり方</dt><dd>作業結果「作成済み」</dd>
      </dl>
    </div>"""

sec2 = f'''<section class="ex" id="sysex">
    <div>
      <h2>記述例：システムレイヤーの仕様書</h2>
      <p class="note">経費精算システムを、ユーザーインターフェース、ユーザーユースケース、サービスユースケースに分けて書いた例です。画面遷移はユーザーインターフェースとして1つ作り、ユーザーユースケースは、その一部を範囲として指します。サービスユースケースは、1つずつ処理の流れを持ちます。</p>
    </div>
    <div class="doc">
      <h3 class="doct">ユーザーインターフェース：経費精算システム</h3>
      <p class="note">ユースケースとは独立に作ります。複数のユーザーユースケースが、この画面遷移の一部を使います。</p>
      <h3>画面遷移</h3>
      <figure class="flow">{svg_ui}</figure>
      <p class="note">UMLのステートマシン図です。左上の「stm」は、ステートマシン図であることを示す見出しです。角の丸い四角が状態で、画面に当たります。矢印が遷移で、画面遷移に当たります。矢印には、遷移を起こす操作を書いています。黒い丸は開始を表し、最初に開く画面を指します。</p>
      <h3>画面</h3>
      {states}
    </div>
    <div class="doc">
      <h3 class="doct">ユーザーユースケース：経費申請</h3>
      <dl class="facts">
        <dt>詳細化する作業</dt><dd>経費申請（ビジネスユースケース「経費精算」のユーザー作業）</dd>
        <dt>概要</dt><dd>申請者が、立て替えた経費の内容を入力し、確かめて申請する。</dd>
        <dt>アクター</dt><dd>申請者</dd>
        <dt>きっかけ</dt><dd>申請者が、検索画面を開いている。</dd>
        <dt>事前条件</dt><dd>申請者が、システムにログインしている。</dd>
      </dl>
      <h3>画面遷移と、このユースケースの範囲</h3>
      <figure class="flow">{svg2}</figure>
      <p class="note">上のステートマシン図に、このユースケースの始点と範囲を重ねています。</p>
      <h3>扱う情報</h3>
      {info}
      <h3>シナリオ一覧</h3>
      {scen}
      <p class="note">終わり方は、シナリオごとに宣言します。ユーザー作業「経費申請」の作業結果のうち、どれに当たるかを書きます。この例では、1本目のシナリオだけを下に書いています。</p>
      <h3>シナリオ：経費を申請する</h3>
      <dl class="facts">
        <dt>目的</dt><dd>入力した内容を確かめて申請できることを確かめる。</dd>
        <dt>事前条件</dt><dd>申請者が、検索画面を開いている。</dd>
        <dt>手順</dt><dd>
          <ol class="steps">
            <li>申請者が、検索画面で「新規作成」を選ぶ。申請画面が開く。</li>
            <li>申請者が、経費の日付、金額、内容を入力し、「確認へ進む」を選ぶ。申請確認画面が開く。</li>
            <li>申請者が、表示された内容を確かめ、「申請する」を選ぶ。検索画面へ戻る。</li>
          </ol></dd>
        <dt>期待結果</dt><dd>入力した内容で、経費申請が申請済みになっている。</dd>
        <dt>終わり方</dt><dd>作業結果「申請」</dd>
      </dl>
    </div>
    {svc_card}
  </section>
'''

i = t.find('<section class="ex" id="sysex">')
if i >= 0:
    j = t.index('</section>', i) + len('</section>')
    t = t[:i] + sec2.rstrip() + t[j:]
else:
    j = t.rindex('</section>') + len('</section>')
    t = t[:j] + '\n  ' + sec2.rstrip() + t[j:]

open(TEMPLATE, 'w').write(t)
print('ok')
