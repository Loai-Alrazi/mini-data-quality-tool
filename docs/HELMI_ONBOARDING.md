# دليل بدء العمل — HelmiMurad

مرحبًا حلمي. مسؤوليتك في Mini Data Quality Tool هي تحليل جودة البيانات قبل التنظيف واختباراته وربطه، ثم إعداد دليل العرض العملي. المرجع العام هو [خطة المشروع](../PROJECT_PLAN.md)، وهذه الصفحة توضح بداية العمل وترتيب مهامك.

## المهام المسندة

| الإيشو | المطلوب | الفرع |
|---|---|---|
| [#26](https://github.com/Loai-Alrazi/mini-data-quality-tool/issues/26) | المحلل، الاختبارات، الربط، وتوثيق الميزة | `feature/quality-analyzer` |
| [#27](https://github.com/Loai-Alrazi/mini-data-quality-tool/issues/27) | دليل عرض عملي مبني على نتائج التشغيل | `docs/demo-guide` |

إيشو تجهيز الانضمام: [#25](https://github.com/Loai-Alrazi/mini-data-quality-tool/issues/25). التنفيذ البرمجي للمحلل وكتابة دليل العرض هما مساهمتك؛ لم تُضف ملفات تنفيذ فارغة أو منطق مسبق ضمن التجهيز.

## الخطوة الأولى

صلاحية الكتابة في المستودع كافية مثل بقية المطورين. استخدم حساب HelmiMurad عند رفع الفروع وفتح PR، واضبط اسمك وبريدك المرتبطين بحسابك في Git على جهازك حتى تُنسب المساهمات إليك.

```shell
git clone https://github.com/Loai-Alrazi/mini-data-quality-tool.git
cd mini-data-quality-tool
git switch main
git pull --ff-only origin main
git switch -c feature/quality-analyzer
python -m venv .venv
```

فعّل البيئة في Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

أو في Linux/macOS:

```shell
source .venv/bin/activate
```

استخدم Python 3.13 وثبّت الأدوات المتوافقة مع إعداد CI:

```shell
python -m pip install "pandas>=3.0,<4" "pytest>=9,<10"
python -m pytest -q
python main.py data/sample.csv
```

اقرأ `loader.py` و`adapter.py` و`cleaner.py` و`report.py` و`main.py` واختباراتها قبل التعديل. التنفيذ الحالي يقرأ البيانات ويحولها إلى DataFrame وينظفها ويصدر النتيجة؛ مهمتك تضيف تحليلًا قبل التنظيف. تأكد من أحدث `main` لأن تحسينات التقرير والتحقق من الإحصائيات أضيفت بعد الربط الأولي.

## حدود العمل والتنسيق

- المحلل يحسب فقط؛ لا يعدّل DataFrame ولا يقرأ CSV مرة ثانية ولا ينظف البيانات.
- يعالج `adapter.py` الفراغات واستنتاج النوع قبل التحليل؛ لا تعرّف سياسة مختلفة في المحلل.
- لؤي يراجع تعديلات `main.py`، وعمران يراجع تنسيق التقرير؛ حافظ على سلوك `generate_report` واختباراته.
- أنشئ اختبارات للمحلل، وأضف تحققًا من ظهوره ضمن التشغيل الفعلي. تشغيل ملف مستقل دون ربطه لا يكمل المهمة.
- لا تغيّر الملفات غير المرتبطة بمهمتك، ولا تُعد فتح إيشوز الأعضاء السابقة.
- الملفات الناتجة داخل `output/` محلية ولا تُرفع إلى Git.
- تفاصيل شكل النتائج والحالات الحدية والأعداد المرجعية موجودة في إيشو المحلل.

## تسليم PR

```shell
python -m pytest -q
git status
git diff --check
git add src/quality_analyzer.py tests/test_quality_analyzer.py
```

أضف أيضًا الملفات التي عدّلتها للربط والتقرير واختباراتهما والتوثيق بعد مراجعة فروقها. ثم:

```shell
git commit -m "feat: add pre-cleaning quality analysis"
git push -u origin feature/quality-analyzer
```

افتح PR إلى `main` وضع `Closes #رقم_الإيشو` برقم إيشو المحلل، واشرح السلوك الجديد ونتيجة الاختبارات. اطلب مراجعة عضو آخر وانتظرها قبل الدمج. عند توفر Workflow #10، يجب أن ينجح فحص `tests` أيضًا.

للمهمة الثانية أنشئ `docs/demo-guide` من أحدث `main` بعد دمج المحلل، أو جهز مسودة النص مبكرًا ثم تحقّق من النتائج بعد الدمج. لا تُضمّن تنفيذ المحلل داخل PR دليل العرض.

## دليل العرض والمراجعة النهائية

يركز `docs/DEMO_GUIDE.md` على سيناريو عرض: فحص البيانات الخام، التشغيل، تفسير التحليل والتقرير، فحص CSV الناتج، وتجربة خطأ متوقع. استخدم روابط README للإعداد بدل تكراره، ونسق تغييره مع PR #23.

إيشو #11 للمراجعة النهائية تشمل التحليل والدليل بعد اكتمالهما. أي خلل يظهر أثناء التوثيق يحتاج إيشو إصلاح مستقلة.

## لوحة المشروع

توجد مهامك على [لوحة Mini Data Quality Tool](https://github.com/users/Loai-Alrazi/projects/2)، مسندة إلى حسابك. ترتيب الحالات المستخدم هو `Todo` ثم `In Progress` ثم `In Review` ثم `Done`: يبدأ العمل من Todo، وينتقل إلى In Progress عند التنفيذ، ثم In Review عند رفع PR، ويصبح Done بعد المراجعة والدمج. نسّق تحديث الحالة مع لؤي إذا لم تتوفر لديك صلاحية تعديل اللوحة.

عند تجهيز الانضمام كانت #26 و#27 بحالة Todo، وكانت إيشو التجهيز #25 وPR #28 بحالة In Review. هذه حالة التجهيز وليست إعلانًا عن تنفيذ المحلل أو دليل العرض.
