from flask import Flask, render_template_string, request

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>---야구 통계 계산기---</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; text-align: center; padding-top: 50px; background-color: #f0fdf4; }
        .card { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
        .input-group { margin: 10px; display: flex; justify-content: space-between; align-items: center; }
        input { padding: 8px; width: 60px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #16a34a; color: white; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
        .result { margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>==야구 통계 계산기==</h2>
        <form method="POST">
            <div class="input-group">타수 (AB): <input type="number" name="AB" value="0"></div>
            <div class="input-group">1루타: <input type="number" name="s" value="0"></div>
            <div class="input-group">2루타: <input type="number" name="d" value="0"></div>
            <div class="input-group">3루타: <input type="number" name="t" value="0"></div>
            <div class="input-group">홈런 (HR): <input type="number" name="hr" value="0"></div>
            <div class="input-group">사사구 (BB/HBP): <input type="number" name="b" value="0"></div>
            <div class="input-group">희생플라이 (SF): <input type="number" name="sf" value="0"></div>
            <button type="submit">통계 산출하기</button>
        </form>

        {% if result %}
        <div class="result">
            <h3>=====결과 리포트=====</h3>
            <p>타율 (AVG): <strong>{{ result.AVG }}</strong></p>
            <p>출루율 (OBP): <strong>{{ result.OBP }}</strong></p>
            <p>장타율 (SLG): <strong>{{ result.SLG }}</strong></p>
            <p><strong>OPS: {{ result.OPS }}</strong></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        # 숫자가 오지 않거나 비어있을 경우 0으로 처리
        def get_int(name):
            val = request.form.get(name, 0)
            return int(val) if val else 0

        AB = get_int('AB')
        s = get_int('s')
        d = get_int('d')
        t = get_int('t')
        hr = get_int('hr')
        b = get_int('b')
        sf = get_int('sf')

        # 1. 계산 기초 데이터 정리
        hits = s + d + t + hr  # 전체 안타
        total_bases = s + (d * 2) + (t * 3) + (hr * 4) # 루타수
        obp_denominator = AB + b + sf # 출루율 분모

        # 2. 비율 스탯 계산
        avg = hits / AB # if AB > 0 else 0 #TODO: 이거 테스트임
        slg = total_bases / AB if AB > 0 else 0
        obp = (hits + b) / obp_denominator if obp_denominator > 0 else 0
        ops = obp + slg

        result = {
            "AVG": f"{avg:.3f}",
            "SLG": f"{slg:.3f}",
            "OBP": f"{obp:.3f}",
            "OPS": f"{ops:.3f}"
        }
        
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=False)