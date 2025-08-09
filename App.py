from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

المتغيرات = {}

def تنفيذ_امر(سطر):
    تقسيم = سطر.split()
    if not تقسيم:
        return ""
    الامر = تقسيم[0]

    if الامر == 'اطبع':
        نص = " ".join(تقسيم[1:])
        for مفتاح, قيمة in المتغيرات.items():
            نص = نص.replace(mفتاح, str(قيمة))
        return نص

    elif الامر == 'جمع':
        if len(تقسيم) >= 3:
            try:
                ن1 = int(تقسيم[1]) if تقسيم[1].isdigit() else int(المتغيرات.get(تقسيم[1], 0))
                ن2 = int(تقسيم[2]) if تقسيم[2].isdigit() else int(المتغيرات.get(تقسيم[2], 0))
                return str(ن1 + ن2)
            except:
                return "خطأ في الأرقام"
        else:
            return "استخدم: جمع رقم1 رقم2"

    elif الامر == 'عين':
        if len(تقسيم) >= 3:
            اسم = تقسيم[1]
            قيمة = تقسيم[2]
            if قيمة.isdigit():
                قيمة = int(قيمة)
            المتغيرات[اسم] = قيمة
            return f"تم تعيين {اسم} = {قيمة}"
        else:
            return "استخدم: عين اسم_المتغير القيمة"

    else:
        return "أمر غير معروف"

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8" />
<title>لغة برمجة عربية</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 20px; }
  textarea { width: 100%; height: 200px; font-size: 16px; }
  #output { background: #fff; padding: 10px; margin-top: 10px; min-height: 100px; white-space: pre-wrap; }
  button { padding: 10px 20px; font-size: 16px; }
</style>
</head>
<body>
<h2>اكتب أوامرك بالعربية وشغلها</h2>
<textarea id="code" placeholder="اكتب هنا... مثال: \nعين س 5\nاطبع س\nجمع 3 4"></textarea><br/>
<button onclick="تشغيل()">شغل</button>
<div id="output"></div>

<script>
function تشغيل() {
    let نص = document.getElementById('code').value;
    fetch('/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({code: نص})
    }).then(res => res.json())
      .then(data => {
          document.getElementById('output').textContent = data.result;
      });
}
</script>
</body>
</html>
''')

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    أكواد = data.get('code', '').split('\n')
    نتائج = []
    for سطر in أكواد:
        سطر = سطر.strip()
        if سطر:
            نتيجة = تنفيذ_امر(سطر)
            نتائج.append(f">>> {سطر}\n{نتيجة}")
    return jsonify({'result': '\n\n'.join(نتائج)})

if __name__ == '__main__':
    app.run(debug=True)
